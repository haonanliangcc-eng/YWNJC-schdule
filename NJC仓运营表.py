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

# 登录
st.sidebar.markdown("# 🏢 NJC 数据管理中心")
if st.sidebar.text_input("🔑 登录密码", type="password") != "20260616":
    st.warning("⚠️ 请输入正确密码以解锁系统。")
    st.stop()

menu = st.sidebar.radio("🚀 功能导航：", ["📋 每日交接清单", "📦 尾程派送监控", "📊 劳务排班预测"])

# 1. 每日交接清单 (含当页历史查询)
if menu == "📋 每日交接清单":
    st.title("📋 每日运营交接清单")
    selected_date = st.date_input("📅 操作日期", datetime.date.today())
    date_key = str(selected_date)
    db = load_data()
    
    if date_key not in db:
        db[date_key] = {
            "tasks": [{"工作内容": x, "完成": False, "责任人": ""} for x in ["NJC装车", "GOFO取货", "SPX取货", "DD301取货", "UNI取货", "Temu退货", "异常登记"]],
            "shipping": [{"渠道": k, "货量": "", "时长": "", "人": ""} for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]]
        }
    
    # 录入区
    tab1, tab2 = st.tabs(["📝 当前录入", "📂 历史查询归档"])
    with tab1:
        edit_t = st.data_editor(pd.DataFrame(db[date_key]["tasks"]), use_container_width=True)
        edit_s = st.data_editor(pd.DataFrame(db[date_key]["shipping"]), use_container_width=True)
        if st.button("💾 保存并固化数据"):
            db[date_key]["tasks"] = edit_t.to_dict("records")
            db[date_key]["shipping"] = edit_s.to_dict("records")
            save_data(db)
            st.success("✅ 数据已保存！")
            st.rerun()
    
    # 历史查看区 (方案二实现)
    with tab2:
        st.subheader("查看已存档的历史记录")
        for d in sorted(db.keys(), reverse=True):
            with st.expander(f"📅 日期：{d}"):
                st.write("渠道发货数据：")
                st.dataframe(pd.DataFrame(db[d]["shipping"]), use_container_width=True)

# 2. 尾程监控
elif menu == "📦 尾程派送监控":
    st.header("📦 尾程派送监控台")
    db = load_data()
    all_rows = [{"日期": d, **row, "UP-R效率比": round(float(row['货量'])/float(row['时长'] if row['时长'] else 1), 2)} 
                for d, c in db.items() for row in c["shipping"] if row["货量"]]
    if all_rows:
        df = pd.DataFrame(all_rows).sort_values("日期", ascending=False)
        st.dataframe(df, use_container_width=True)
        st.line_chart(df.pivot_table(index="日期", columns="渠道", values="货量"))
    else: st.info("暂无数据，请前往‘交接清单’录入。")

# 3. 完整劳务预测
elif menu == "📊 劳务排班预测":
    st.header("⚙️ 人体工效学劳务排班模型")
    col1, col2, col3 = st.columns(3)
    v1 = col1.number_input("卸货件数", value=1500)
    v2 = col2.number_input("上架件数", value=1200)
    v3 = col3.number_input("拣货件数", value=3000)
    uph = st.number_input("标准人员UPH (件/小时)", value=100)
    hours = st.number_input("班次有效工时 (小时)", value=8.0)
    
    res = ((v1 + v2 + v3) / uph / hours) * 1.15
    st.metric("👤 建议配置总人数 (含15%疲劳储备)", f"{round(res, 1)} 人")
