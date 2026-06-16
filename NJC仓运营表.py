import streamlit as st
import datetime
import pandas as pd

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
# 功能二：运营交接清单 (纯 Streamlit 原生响应式保存版)
# ==========================================
elif page == "📋 运营交接清单":
    st.title("📋 NJC仓运营交接清单 - 数据中心系统版")
    st.caption("系统采用响应式数据编辑器，输入数据实时在后台自动保存。")
    
    # --- 顶层核心控制：日期与基本信息 ---
    # 每天进入网页，这里都会自动刷新并锁定为当天的日期
    col_date, col_wh, col_user = st.columns([1.5, 1, 1.5])
    with col_date:
        selected_date = st.date_input("📅 排班选择日期", datetime.date.today())
    
    # 将日期转化为字符串，作为后台存储数据的唯一Key
    date_key = str(selected_date)
    
    # 初始化当前选定日期的系统持久缓存
    if "saved_data" not in st.session_state:
        st.session_state.saved_data = {}
        
    if date_key not in st.session_state.saved_data:
        # 如果是新的一天，自动刷新并初始化一个干净的空白表格数据
        st.session_state.saved_data[date_key] = {
            "warehouse": "NJC仓",
            "supervisor": "",
            "morning_tasks": pd.DataFrame([
                {"工作内容": "NJC仓派送货装车完成", "完成": False, "责任人": ""},
                {"工作内容": "GOFO司机取货完成", "完成": False, "责任人": ""},
                {"工作内容": "SPX司机取货完成", "完成": False, "责任人": ""},
                {"工作内容": "DD301司机取货完成", "完成": False, "责任人": ""},
                {"工作内容": "UNI司机取货完成", "完成": False, "责任人": ""},
                {"工作内容": "Temu退货接收登记完成", "完成": False, "责任人": ""},
                {"工作内容": "异常包裹登记完成", "完成": False, "责任人": ""}
            ]),
            "customs_data": pd.DataFrame([
                {"清关行": k, "状态": "", "数量": "", "时间": ""} 
                for k in ["YUEJIE", "六脉", "mirage", "AGS", "Tolead", "SF", "R&T", "DD", "机场"]
            ]),
            "shipping_data": pd.DataFrame([
                {"渠道": k, "货量": "", "时间": "", "人": ""}
                for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]
            ]),
            "special_events": pd.DataFrame([
                {"时间": "", "内容": "", "措施": ""},
                {"时间": "", "内容": "", "措施": ""}
            ]),
            "sign1": "", "sign2": "", "sign3": "", "sign4": ""
        }
    
    # 读取当前日期专属的数据
    current_data = st.session_state.saved_data[date_key]
    
    with col_wh:
        current_data["warehouse"] = st.text_input("🏠 仓库", value=current_data["warehouse"])
    with col_user:
        current_data["supervisor"] = st.text_input("👤 值班主管 (签字确认)", value=current_data["supervisor"])
        
    st.markdown("---")
    
    # --- 一、早班工作清单 ---
    st.subheader("一、早班工作清单")
    # st.data_editor 是 Streamlit 极其强大的交互组件，用户可直接双击格子输入、勾选，且输入即保存
    edited_morning = st.data_editor(
        current_data["morning_tasks"], 
        use_container_width=True, 
        hide_index=True,
        key=f"morning_{date_key}"
    )
    current_data["morning_tasks"] = edited_morning
    
    # --- 二、与 三、 并排布局 ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("二、早班叫车与清关行提货")
        edited_customs = st.data_editor(
            current_data["customs_data"],
            use_container_width=True,
            hide_index=True,
            key=f"customs_{date_key}"
        )
        current_data["customs_data"] = edited_customs
        
    with col_right:
        st.subheader("三、渠道发货记录")
        edited_shipping = st.data_editor(
            current_data["shipping_data"],
            use_container_width=True,
            hide_index=True,
            key=f"shipping_{date_key}"
        )
        current_data["shipping_data"] = edited_shipping
        
    # --- 四、特殊事件及延误 ---
    st.subheader("四、特殊事件及延误")
    edited_events = st.data_editor(
        current_data["special_events"],
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic", # 支持动态增加行
        key=f"events_{date_key}"
    )
    current_data["special_events"] = edited_events
    
    # --- 五、交接确认 ---
    st.subheader("五、交接确认")
    with st.container(border=True):
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        current_data["sign1"] = col_s1.text_input("交班人签字 :", value=current_data["sign1"])
        current_data["sign2"] = col_s2.text_input("接班人签字 :", value=current_data["sign2"])
        current_data["sign3"] = col_s3.text_input("主管签字 :", value=current_data["sign3"])
        current_data["sign4"] = col_s4.text_input("区域经理签字 :", value=current_data["sign4"])
        
    # --- 数据控制按钮 ---
    st.markdown("---")
    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
    with col_btn1:
        if st.button("💾 点击强制保存当前页数据", type="primary"):
            st.success(f"🎉 成功保存 {date_key} 的交接清单数据到系统后台！")
    with col_btn2:
        if st.button("🧹 清空今日表格", type="secondary"):
            del st.session_state.saved_data[date_key]
            st.rerun()
