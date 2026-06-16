import streamlit as st
import datetime
import pandas as pd
import json
import os

# ==========================================
# 0. 核心数据本地持久化
# ==========================================
DB_FILE = "njc_database.json"

def load_global_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}

def save_global_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="NJC仓运营中心", layout="wide")

# ==========================================
# 1. 安全登录系统
# ==========================================
st.sidebar.markdown("# 🏢 NJC 数据管理中心")
input_user = st.sidebar.text_input("👤 主管姓名").strip()
input_password = st.sidebar.text_input("🔑 登录密码", type="password")

if not (input_user != "" and input_password == "20260616"):
    st.warning("⚠️ 请输入主管姓名和密码（20260616）以进入系统。")
    st.stop()

menu = st.sidebar.radio("🚀 功能导航：", ["📋 每日交接清单", "📦 尾程派送监控", "📊 劳务排班预测"])

# ==========================================
# 2. 每日交接清单 (完全复原版)
# ==========================================
if menu == "📋 每日交接清单":
    st.title("📋 NJC仓运营交接清单")
    selected_date = st.date_input("📅 选择操作日期", datetime.date.today())
    date_key = str(selected_date)
    global_db = load_global_data()
    
    if date_key not in global_db:
        global_db[date_key] = {
            "morning_tasks": [{"工作内容": x, "完成": False, "责任人": ""} for x in ["NJC仓派送装车", "GOFO取货", "SPX取货", "DD301取货", "UNI取货", "Temu退货", "异常登记"]],
            "customs_data": [{"清关行": k, "状态": "", "数量": "", "时间": ""} for k in ["YUEJIE", "六脉", "mirage", "AGS", "Tolead", "SF", "R&T", "DD", "机场"]],
            "shipping_data": [{"渠道": k, "货量": "", "时间": "", "人": ""} for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]],
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
        st.success("🎉 保存成功！")
        st.rerun()

    # 历史大盘（数据回显）
    st.markdown("---")
    st.header("📊 历史流水大盘")
    all_rows = []
    for d, c in global_db.items():
        for row in c["shipping_data"]:
            if row["货量"]: all_rows.append({"日期": d, "渠道": row["渠道"], "货量": float(row["货量"])})
    if all_rows:
        df = pd.DataFrame(all_rows).sort_values("日期", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.line_chart(df.pivot_table(index="日期", columns="渠道", values="货量"))

# ==========================================
# 3. 尾程监控台 (实装功能)
# ==========================================
elif menu == "📦 尾程派送监控":
    st.header("📦 尾程派送监控台")
    st.write("追踪各渠道末端派送任务：")
    all_data = load_global_data()
    monitoring_list = []
    for d, c in all_data.items():
        for row in c["shipping_data"]:
            if row["人"]: monitoring_list.append({"日期": d, **row})
    if monitoring_list:
        st.dataframe(pd.DataFrame(monitoring_list).sort_values("日期", ascending=False), use_container_width=True)
    else:
        st.info("尚无派送记录，请前往‘每日交接清单’填写发货信息并保存。")

elif menu == "📊 劳务排班预测":
    st.header("⚙️ 劳务排班预测")
    st.write("此处可根据货量自动计算今日所需劳务人数。")
