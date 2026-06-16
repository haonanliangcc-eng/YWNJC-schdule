import streamlit as st
import datetime
import pandas as pd
import json
import os

# ==========================================
# 0. 数据持久化核心
# ==========================================
DB_FILE = "njc_database.json"

def load_global_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_global_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ==========================================
# 1. 页面配置与 UI 样式
# ==========================================
st.set_page_config(page_title="NJC仓运营中心", layout="wide")
st.markdown("""
    <style>
    .status-warning { padding: 15px; background-color: #FEF2F2; border-left: 5px solid #EF4444; color: #991B1B; border-radius: 4px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏：安全登录与功能导航
# ==========================================
st.sidebar.markdown("# 🏢 NJC 数据管理中心")
st.sidebar.markdown("---")

# 登录逻辑
input_user = st.sidebar.text_input("👤 主管姓名").strip()
input_password = st.sidebar.text_input("🔑 登录密码", type="password")

is_logged_in = False
if input_user != "" and input_password == "20260616":
    st.sidebar.success(f"🟢 欢迎回来，{input_user}！")
    is_logged_in = True
elif input_user != "" or input_password != "":
    st.sidebar.error("🔴 密码错误或信息不全")
    st.stop()
else:
    st.sidebar.warning("⚠️ 请输入主管姓名和密码以解锁系统。")
    st.stop()

st.sidebar.markdown("---")
menu = st.sidebar.radio("🚀 功能导航：", ["📋 每日交接清单", "📦 尾程派送监控", "📊 劳务排班预测"])

# ==========================================
# 3. 业务逻辑区
# ==========================================
if menu == "📋 每日交接清单":
    st.title("📋 每日运营交接清单")
    
    selected_date = st.date_input("📅 选择操作日期", datetime.date.today())
    date_key = str(selected_date)
    global_db = load_global_data()
    
    if date_key not in global_db:
        global_db[date_key] = {
            "warehouse": "NJC仓", "supervisor": input_user,
            "morning_tasks": [{"工作内容": x, "完成": False, "责任人": ""} for x in ["NJC仓派送装车", "GOFO取货", "SPX取货", "DD301取货", "UNI取货", "Temu退货", "异常登记"]],
            "customs_data": [{"清关行": k, "状态": "", "数量": "", "时间": ""} for k in ["YUEJIE", "六脉", "mirage", "AGS", "Tolead", "SF", "R&T", "DD", "机场"]],
            "shipping_data": [{"渠道": k, "货量": "", "时间": "", "人": ""} for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]],
            "special_events": [{"时间": "", "内容": "", "措施": ""}]
        }
    
    # 编辑表格区
    data = global_db[date_key]
    tab1, tab2, tab3 = st.tabs(["📌 任务与异常", "🚚 清关提货", "📦 渠道发货"])
    
    with tab1:
        edit_m = st.data_editor(pd.DataFrame(data["morning_tasks"]), use_container_width=True, hide_index=True)
        edit_e = st.data_editor(pd.DataFrame(data["special_events"]), use_container_width=True, hide_index=True, num_rows="dynamic")
    with tab2:
        edit_c = st.data_editor(pd.DataFrame(data["customs_data"]), use_container_width=True, hide_index=True)
    with tab3:
        edit_s = st.data_editor(pd.DataFrame(data["shipping_data"]), use_container_width=True, hide_index=True)

    # 保存触发
    if st.button("💾 保存今日交接单", type="primary"):
        global_db[date_key].update({"morning_tasks": edit_m.to_dict(orient="records"), "customs_data": edit_c.to_dict(orient="records"), "shipping_data": edit_s.to_dict(orient="records"), "special_events": edit_e.to_dict(orient="records")})
        save_global_data(global_db)
        st.success("🎉 保存成功！")
        st.rerun()

    # 底部大盘（倒序）
    st.markdown("---")
    st.header("📊 历史流水大盘")
    all_data = []
    for d, c in global_db.items():
        for row in c["shipping_data"]:
            if row["货量"]: all_data.append({"日期": d, "渠道": row["渠道"], "货量": float(row["货量"])})
    
    if all_data:
        df = pd.DataFrame(all_data).sort_values("日期", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.line_chart(df.pivot_table(index="日期", columns="渠道", values="货量"), height=250)

elif menu == "📦 尾程派送监控":
    st.header("📦 尾程派送监控台")
    st.info("此模块用于追踪各渠道末端派送状态。")

elif menu == "📊 劳务排班预测":
    st.header("⚙️ 劳务排班预测")
    # ... (此处可放入你的排班逻辑代码)
