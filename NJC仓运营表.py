import streamlit as st
import datetime
import pandas as pd
import json
import os
import streamlit as st
import datetime
import pandas as pd
import json
import os

# ==========================================
# 0. 核心数据本地持久化函数
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
# 1. 页面基本配置与高级 UI (包含红色警告框样式)
# ==========================================
st.set_page_config(page_title="NJC运营仓数据中心", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; }
    h1 { color: #1E3A8A; }
    /* 红色警告框样式 */
    .status-warning { 
        padding: 15px; 
        background-color: #FEF2F2; 
        border-left: 5px solid #EF4444; 
        color: #991B1B; 
        border-radius: 4px; 
        margin-bottom: 20px; 
        font-weight: bold;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 功能一：独立账号登录 (密码：20260616)
# ==========================================
st.sidebar.markdown("# 🏢 NJC 数据管理中心")
st.sidebar.markdown("---")
st.sidebar.subheader("🔐 主管安全登录")

# 用户名随便写，密码必须对
input_user = st.sidebar.text_input("👤 主管姓名", placeholder="输入名字")
correct_password = "20260616"
input_password = st.sidebar.text_input("🔑 登录密码", type="password")

is_logged_in = False
if input_user != "" and input_password == correct_password:
    st.sidebar.success(f"🟢 欢迎回来, {input_user}")
    is_logged_in = True
elif input_user != "" and input_password != "":
    st.sidebar.error("🔴 密码错误")

# 登录拦截：没登录就不显示后面所有内容
if not is_logged_in:
    st.warning("👋 请在左侧输入主管姓名和正确密码（20260616）以进入系统。")
    st.stop()

st.sidebar.markdown("---")
page = st.sidebar.radio("功能导航：", ["📋 运营交接清单", "📊 劳务排班预测"])

# ==========================================
# 劳务排班预测功能
# ==========================================
if page == "📊 劳务排班预测":
    st.title("⚙️ 劳务排班预测看板")
    # ... (此处省略排班计算代码，与之前一致)
    shift_hours = st.sidebar.number_input("班次总长 (小时)", value=10.0)
    v1 = st.number_input("1_Unloading (卸货/件)", value=1500)
    # 简易计算逻辑
    st.metric("👤 预计需劳务人数", "25 人 (示例)")

# ==========================================
# 运营交接清单功能 (核心功能区)
# ==========================================
elif page == "📋 运营交接清单":
    st.title("📋 NJC仓运营交接清单")
    
    # 顶部日期选择
    selected_date = st.date_input("📅 选择操作日期", datetime.date.today())
    date_key = str(selected_date)
    global_db = load_global_data()
    
    # 初始化当天数据结构
    if date_key not in global_db:
        global_db[date_key] = {
            "warehouse": "NJC仓", "supervisor": input_user,
            "morning_tasks": [{"工作内容": "NJC仓派送货装车完成", "完成": False, "责任人": ""}, {"工作内容": "GOFO司机取货完成", "完成": False, "责任人": ""}],
            "customs_data": [{"清关行": "YUEJIE", "状态": "", "数量": "", "时间": ""}],
            "shipping_data": [{"渠道": "GOFO", "货量": "", "时间": "", "人": ""}],
            "special_events": [{"时间": "", "内容": "", "措施": ""}],
            "sign1": "", "sign2": "", "sign3": "", "sign4": ""
        }
    
    day_data = global_db[date_key]
    
    # 填写区
    tab1, tab2, tab3 = st.tabs(["📌 早班 & 异常", "🚚 清关提货", "📦 渠道发货"])
    
    with tab1:
        df_m = pd.DataFrame(day_data["morning_tasks"])
        edit_m = st.data_editor(df_m, use_container_width=True, hide_index=True, key=f"m_{date_key}")
        df_e = pd.DataFrame(day_data["special_events"])
        edit_e = st.data_editor(df_e, use_container_width=True, hide_index=True, num_rows="dynamic", key=f"e_{date_key}")

    with tab2:
        df_c = pd.DataFrame(day_data["customs_data"])
        edit_c = st.data_editor(df_c, use_container_width=True, hide_index=True, key=f"c_{date_key}")
        
    with tab3:
        df_s = pd.DataFrame(day_data["shipping_data"])
        edit_s = st.data_editor(df_s, use_container_width=True, hide_index=True, key=f"s_{date_key}")

    # ==========================================
    # 功能三：自动弹出数据未保存提示 (防丢失)
    # ==========================================
    # 只要当前编辑的内容和数据库里的内容不一样，就报警
    if not edit_m.equals(df_m) or not edit_c.equals(df_c) or not edit_s.equals(df_s):
        st.markdown('<div class="status-warning">🚨 警告：检测到表格已被修改！请务必点击下方 [红色保存按钮]，否则刷新或关闭网页后数据将丢失！</div>', unsafe_allow_html=True)

    if st.button("💾 点击锁定并保存今日交接单", type="primary"):
        global_db[date_key] = {
            "warehouse": "NJC仓", "supervisor": input_user,
            "morning_tasks": edit_m.to_dict(orient="records"),
            "customs_data": edit_c.to_dict(orient="records"),
            "shipping_data": edit_s.to_dict(orient="records"),
            "special_events": edit_e.to_dict(orient="records"),
            "sign1": "", "sign2": "", "sign3": "", "sign4": ""
        }
        save_global_data(global_db)
        st.success("✅ 保存成功！历史大盘已更新。")
        st.rerun()

    # ==========================================
    # 功能四：运营数据可视化图表 (保存后可见)
    # ==========================================
    st.markdown("---")
    st.header("📈 运营数据可视化趋势")
    
    all_data = load_global_data()
    if all_data:
        # 此处提取所有日期的发货货量进行绘图
        chart_data = []
        for d, content in all_data.items():
            total_vol = sum([float(row['货量']) if row.get('货量') and row.get('货量').isdigit() else 0 for row in content['shipping_data']])
            chart_data.append({"日期": d, "总发货量": total_vol})
        
        if chart_data:
            df_chart = pd.DataFrame(chart_data).sort_values("日期")
            st.line_chart(df_chart.set_index("日期"))
        else:
            st.info("💡 暂无数值数据，无法生成图表。请在表格中输入货量数字并保存。")

    # ==========================================
    # 功能五：流水大盘 (日期倒序排列)
    # ==========================================
    st.markdown("---")
    st.header("📊 NJC 仓运管历史数据总账")
    
    history_list = []
    for d, content in all_data.items():
        # 简化提取提货信息作为展示
        for row in content.get('customs_data', []):
            history_list.append({
                "日期": d, "主管": content.get('supervisor'), 
                "清关行": row.get('清关行'), "数量": row.get('数量'), "时间": row.get('时间')
            })
    
    if history_list:
        df_history = pd.DataFrame(history_list)
        # 🌟 核心功能：按照日期从新到老排序 (最新的在最上面)
        df_history = df_history.sort_values(by="日期", ascending=False)
        st.dataframe(df_history, use_container_width=True, hide_index=True)
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
