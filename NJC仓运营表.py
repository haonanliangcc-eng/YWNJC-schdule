import streamlit as st
import datetime
import pandas as pd
import json
import os

# ==========================================
# 0. 核心数据本地持久化函数 (JSON 数据库)
# ==========================================
DB_FILE = "njc_database.json"

def load_global_data():
    """从本地文件加载所有历史数据"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_global_data(data):
    """将数据写入本地文件永久保存"""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ==========================================
# 1. 页面基本配置
# ==========================================
st.set_page_config(page_title="NJC运营仓数据中心", layout="wide")

# ==========================================
# 2. 侧边栏导航控制
# ==========================================
st.sidebar.title("导航菜单")
page = st.sidebar.radio("请选择要查看的功能：", ["📊 劳务排班预测", "📋 运营交接清单"])

# ==========================================
# 功能一：劳务排班预测
# ==========================================
if page == "📊 劳务排班预测":
    st.title("⚙️ NJC运营仓 - 下午班次 (14:00 - 24:00) 劳务排班预测看板")
    st.caption("基于人体工效学分段疲劳衰减的高级仓储运营劳务预测模型")
    
    st.sidebar.markdown("---")
    st.sidebar.header("⏰ 班次参数设置")
    shift_hours = st.sidebar.number_input("班次总长 (小时)", value=10.00)
    rest_mins = st.sidebar.number_input("吃饭休息 (分钟)", value=45)
    handover_hours = st.sidebar.number_input("早会交接 (小时)", value=0.25)
    
    st.header("📊 环节参数动态配置")
    st.subheader("📦 当前预测货量预留区")
    col1, col2, col3 = st.columns(3)
    v1 = col1.number_input("1_Unloading (卸货入库/件)", value=1500)
    v2 = col2.number_input("2_Putaway (库位上架/件)", value=1200)
    v3 = col3.number_input("3_Picking (库区拣货/件)", value=3000)
    
    col4, col5, col6 = st.columns(3)
    v4 = col4.number_input("4_Packing (复核打包/件)", value=2500)
    v5 = col5.number_input("5_Labeling (贴面单/件)", value=2500)
    v6 = col6.number_input("6_Dispatch (称重装车/件)", value=2800)
    
    st.subheader("⚡ 标准人均时效基准线 (UPH)")
    col_u1, col_u2, col_u3 = st.columns(3)
    u1 = col_u1.number_input("Unloading 标准UPH", value=120)
    u2 = col_u2.number_input("Putaway 标准UPH", value=80)
    u3 = col_u3.number_input("Picking 标准UPH", value=100)
    
    col_u4, col_u5, col_u6 = st.columns(3)
    u4 = col_u4.number_input("Packing 标准UPH", value=80)
    u5 = col_u5.number_input("Labeling 标准UPH", value=150)
    u6 = col_u6.number_input("Dispatch 标准UPH", value=200)
    
    st.markdown("---")
    st.header("🚀 预测劳务人数")
    
    net_hours = shift_hours - (rest_mins/60) - handover_hours
    st.metric("👤 单人每日净工时", f"{net_hours:.2f} 小时")
    
    total_needed = round((v1/u1 + v2/u2 + v3/u3 + v4/u4 + v5/u5 + v6/u6) / net_hours)
    st.subheader(f"🔥 下午班次总计需通知劳务到场 : :blue[{total_needed} 人]")

# ==========================================
# 功能二：运营交接清单 (带数据库永久保存版)
# ==========================================
elif page == "📋 运营交接清单":
    st.title("📋 NJC仓运营交接清单 - 数据中心系统版")
    st.caption("系统采用响应式数据编辑器，点击下方保存按钮可永久沉淀至系统后台。")
    
    # 1. 日期选择（每天打开自动定位到当天）
    col_date, col_wh, col_user = st.columns([1.5, 1, 1.5])
    with col_date:
        selected_date = st.date_input("📅 排班选择日期", datetime.date.today())
    
    date_key = str(selected_date)
    
    # 从后台文件读取总数据库
    global_db = load_global_data()
    
    # 2. 如果当前日期在数据库中不存在，初始化干净的默认数据
    if date_key not in global_db:
        global_db[date_key] = {
            "warehouse": "NJC仓",
            "supervisor": "",
            "morning_tasks": [
                {"工作内容": "NJC仓派送货装车完成", "完成": False, "责任人": ""},
                {"工作内容": "GOFO司机取货完成", "完成": False, "责任人": ""},
                {"工作内容": "SPX司机取货完成", "完成": False, "责任人": ""},
                {"工作内容": "DD301司机取货完成", "完成": False, "责任人": ""},
                {"工作内容": "UNI司机取货完成", "完成": False, "责任人": ""},
                {"工作内容": "Temu退货接收登记完成", "完成": False, "责任人": ""},
                {"工作内容": "异常包裹登记完成", "完成": False, "责任人": ""}
            ],
            "customs_data": [{"清关行": k, "状态": "", "数量": "", "时间": ""} for k in ["YUEJIE", "六脉", "mirage", "AGS", "Tolead", "SF", "R&T", "DD", "机场"]],
            "shipping_data": [{"渠道": k, "货量": "", "时间": "", "人": ""} for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]],
            "special_events": [{"时间": "", "内容": "", "措施": ""}, {"时间": "", "内容": "", "措施": ""}],
            "sign1": "", "sign2": "", "sign3": "", "sign4": ""
        }
    
    # 获取当天的数据快照
    day_data = global_db[date_key]
    
    # 3. 渲染基本信息输入框
    with col_wh:
        wh_val = st.text_input("🏠 仓库", value=day_data.get("warehouse", "NJC仓"), key=f"wh_{date_key}")
    with col_user:
        sv_val = st.text_input("👤 值班主管 (签字确认)", value=day_data.get("supervisor", ""), key=f"sv_{date_key}")
        
    st.markdown("---")
    
    # --- 一、早班工作清单 ---
    st.subheader("一、早班工作清单")
    df_morning = pd.DataFrame(day_data["morning_tasks"])
    edited_morning = st.data_editor(df_morning, use_container_width=True, hide_index=True, key=f"edit_edit_morning_{date_key}")
    
    # --- 二、与 三、 并排布局 ---
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("二、早班叫车与清关行提货")
        df_customs = pd.DataFrame(day_data["customs_data"])
        edited_customs = st.data_editor(df_customs, use_container_width=True, hide_index=True, key=f"edit_customs_{date_key}")
        
    with col_right:
        st.subheader("三、渠道发货记录")
        df_shipping = pd.DataFrame(day_data["shipping_data"])
        edited_shipping = st.data_editor(df_shipping, use_container_width=True, hide_index=True, key=f"edit_shipping_{date_key}")
        
    # --- 四、特殊事件及延误 ---
    st.subheader("四、特殊事件及延误")
    df_events = pd.DataFrame(day_data["special_events"])
    edited_events = st.data_editor(df_events, use_container_width=True, hide_index=True, num_rows="dynamic", key=f"edit_events_{date_key}")
    
    # --- 五、交接确认 ---
    st.subheader("五、交接确认")
    with st.container(border=True):
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        s1 = col_s1.text_input("交班人签字 :", value=day_data.get("sign1", ""), key=f"s1_{date_key}")
        s2 = col_s2.text_input("接班人签字 :", value=day_data.get("sign2", ""), key=f"s2_{date_key}")
        s3 = col_s3.text_input("主管签字 :", value=day_data.get("sign3", ""), key=f"s3_{date_key}")
        s4 = col_s4.text_input("区域经理签字 :", value=day_data.get("sign4", ""), key=f"s4_{date_key}")
        
    # --- 数据控制核心按钮 ---
    st.markdown("---")
    col_btn1, col_btn2, _ = st.columns([1.5, 1.5, 4])
    
    with col_btn1:
        if st.button("💾 点击保存当前页数据到后台", type="primary"):
            # 捕获用户在界面上做出的所有最新修改
            global_db[date_key] = {
                "warehouse": wh_val,
                "supervisor": sv_val,
                "morning_tasks": edited_morning.to_dict(orient="records"),
                "customs_data": edited_customs.to_dict(orient="records"),
                "shipping_data": edited_shipping.to_dict(orient="records"),
                "special_events": edited_events.to_dict(orient="records"),
                "sign1": s1, "sign2": s2, "sign3": s3, "sign4": s4
            }
            # 写入本地JSON数据库，实现永久保存
            save_global_data(global_db)
            st.success(f"🎉 成功将 {date_key} 的数据锁定保存至后台数据库！刷新网页也不会丢失。")
            
    with col_btn2:
        if st.button("🧹 擦除今日表格", type="secondary"):
            if date_key in global_db:
                del global_db[date_key]
                save_global_data(global_db)
                st.rerun()
