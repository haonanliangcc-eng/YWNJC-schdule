import streamlit as st
import datetime
import pandas as pd
import json
import os

DB_FILE = "njc_database.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="NJC仓运营系统", layout="wide")

# 侧边栏登录
st.sidebar.markdown("# 🏢 NJC 数据管理中心")
if st.sidebar.text_input("🔑 登录密码", type="password") != "20260616":
    st.warning("⚠️ 请输入正确密码以解锁系统。")
    st.stop()

menu = st.sidebar.radio("🚀 功能导航：", ["📋 每日交接清单", "📦 尾程派送监控", "📊 劳务排班预测"])

# 1. 每日交接清单 (全字段展开版)
if menu == "📋 每日交接清单":
    st.title("📋 每日运营交接清单")
    date = str(st.date_input("📅 操作日期", datetime.date.today()))
    db = load_data()
    
    if date not in db:
        db[date] = {
            "tasks": [{"工作内容": x, "完成": False, "责任人": ""} for x in ["NJC仓派送装车", "GOFO取货", "SPX取货", "DD301取货", "UNI取货", "Temu退货", "异常登记"]],
            "customs": [{"清关行": k, "状态": "", "数量": "", "时间": ""} for k in ["YUEJIE", "六脉", "mirage", "AGS", "Tolead", "SF", "R&T", "DD", "机场"]],
            "shipping": [{"渠道": k, "货量": "", "派送时长(天)": "", "人": ""} for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]]
        }
    
    # 使用 container 让内容展开，不再挤在 Tab 里
    with st.expander("📝 录入与编辑表格", expanded=True):
        st.subheader("1. 早班任务清单")
        edit_t = st.data_editor(pd.DataFrame(db[date]["tasks"]), use_container_width=True)
        st.subheader("2. 清关行提货记录")
        edit_c = st.data_editor(pd.DataFrame(db[date]["customs"]), use_container_width=True)
        st.subheader("3. 渠道派送明细")
        edit_s = st.data_editor(pd.DataFrame(db[date]["shipping"]), use_container_width=True)
        
        if st.button("💾 保存并固化数据"):
            db[date] = {"tasks": edit_t.to_dict("records"), "customs": edit_c.to_dict("records"), "shipping": edit_s.to_dict("records")}
            save_data(db)
            st.success("✅ 数据已永久保存！")
            st.rerun()

    # 历史记录在下方直接展开
    st.markdown("---")
    st.subheader("📂 历史归档查询")
    for d in sorted(db.keys(), reverse=True):
        with st.expander(f"📅 日期：{d}"):
            st.write("清关记录：", pd.DataFrame(db[d]["customs"]))
            st.write("派送渠道：", pd.DataFrame(db[d]["shipping"]))

# 2. 尾程派送监控
elif menu == "📦 尾程派送监控":
    st.header("📦 尾程派送监控台 (UP-R 效率分析)")
    # (保持之前的监控逻辑不变)
    db = load_data()
    all_rows = [{"日期": d, **row, "效率比": round(float(row['货量'])/float(row['派送时长(天)'] if row['派送时长(天)'] else 1), 2)} 
                for d, c in db.items() for row in c["shipping"] if row["货量"]]
    if all_rows:
        st.dataframe(pd.DataFrame(all_rows).sort_values("日期", ascending=False), use_container_width=True)
    else: st.info("暂无数据")

# 3. 完整劳务排班预测
elif menu == "📊 劳务排班预测":
    st.header("⚙️ 人体工效学劳务排班模型")
    col1, col2, col3 = st.columns(3)
    v1 = col1.number_input("卸货件数", value=1500)
    v2 = col2.number_input("上架件数", value=1200)
    v3 = col3.number_input("拣货件数", value=3000)
    uph = st.number_input("标准人员UPH", value=100)
    hours = st.number_input("有效工时", value=8.0)
    res = ((v1 + v2 + v3) / uph / hours) * 1.15
    st.metric("👤 建议配置人数 (含疲劳储备)", f"{round(res, 1)} 人")
