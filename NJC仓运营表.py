import streamlit as st
import datetime
import pandas as pd
import json
import os

DB_FILE = "njc_database.json"

def load_global_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_global_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="NJC仓运营管理系统", layout="wide")

# 侧边栏及登录
st.sidebar.markdown("# 🏢 NJC 数据管理中心")
input_user = st.sidebar.text_input("👤 主管姓名").strip()
input_password = st.sidebar.text_input("🔑 登录密码", type="password")

if not (input_user != "" and input_password == "20260616"):
    st.warning("⚠️ 请输入主管姓名和密码（20260616）以进入系统。")
    st.stop()

menu = st.sidebar.radio("🚀 功能导航：", ["📋 每日交接清单", "📦 尾程派送监控", "📊 劳务排班预测"])

# 1. 每日交接清单
if menu == "📋 每日交接清单":
    st.title("📋 每日运营交接清单")
    selected_date = st.date_input("📅 选择操作日期", datetime.date.today())
    date_key = str(selected_date)
    global_db = load_global_data()
    
    if date_key not in global_db:
        global_db[date_key] = {
            "morning_tasks": [{"工作内容": x, "完成": False, "责任人": ""} for x in ["NJC仓派送装车", "GOFO取货", "SPX取货", "DD301取货", "UNI取货", "Temu退货", "异常登记"]],
            "customs_data": [{"清关行": k, "状态": "", "数量": "", "时间": ""} for k in ["YUEJIE", "六脉", "mirage", "AGS", "Tolead", "SF", "R&T", "DD", "机场"]],
            "shipping_data": [{"渠道": k, "货量": "", "派送时长(天)": "", "人": ""} for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]],
            "special_events": [{"时间": "", "内容": "", "措施": ""}]
        }
    
    data = global_db[date_key]
    tab1, tab2, tab3 = st.tabs(["📌 任务与异常", "🚚 清关提货", "📦 渠道发货"])
    with tab1:
        edit_m = st.data_editor(pd.DataFrame(data["morning_tasks"]), use_container_width=True, hide_index=True)
        edit_e = st.data_editor(pd.DataFrame(data["special_events"]), use_container_width=True, hide_index=True, num_rows="dynamic")
    with tab2:
        edit_c = st.data_editor(pd.DataFrame(data["customs_data"]), use_container_width=True, hide_index=True)
    with tab3:
        edit_s = st.data_editor(pd.DataFrame(data["shipping_data"]), use_container_width=True, hide_index=True)

    if st.button("💾 保存今日交接单", type="primary"):
        global_db[date_key].update({"morning_tasks": edit_m.to_dict(orient="records"), "customs_data": edit_c.to_dict(orient="records"), "shipping_data": edit_s.to_dict(orient="records"), "special_events": edit_e.to_dict(orient="records")})
        save_global_data(global_db)
        st.success("🎉 数据已固化保存！")
        st.rerun()

# 2. 尾程派送监控与科学分析
elif menu == "📦 尾程派送监控":
    st.header("📦 尾程派送监控台")
    all_data = load_global_data()
    df_list = []
    for d, c in all_data.items():
        for row in c["shipping_data"]:
            if row["货量"]:
                v = float(row["货量"])
                t = float(row["派送时长(天)"]) if row["派送时长(天)"] else 1.0
                df_list.append({"日期": d, "渠道": row["渠道"], "货量": v, "UP-R效率比": round(v/t if t>0 else 0, 2)})
    if df_list:
        df = pd.DataFrame(df_list).sort_values("日期", ascending=False)
        st.dataframe(df, use_container_width=True)
        st.line_chart(df.pivot_table(index="日期", columns="渠道", values="货量"))
    else: st.info("暂无记录，请前往‘交接清单’录入。")

# 3. 完整版劳务排班预测
elif menu == "📊 劳务排班预测":
    st.header("⚙️ 劳务排班预测模型")
    st.subheader("输入每日预计作业货量 (各环节汇总)")
    col1, col2 = st.columns(2)
    v1 = col1.number_input("预计总件数", value=5000)
    uph = col2.number_input("标准人员UPH (件/小时)", value=120)
    hours = st.number_input("预计每日有效工时 (小时)", value=8.0)
    
    st.markdown("---")
    res = v1 / uph / hours
    st.metric("👤 建议配置劳务人数", f"{round(res, 1)} 人")
    st.write("公式：`配置人数 = 总件数 / (人员UPH * 有效工时)`")
