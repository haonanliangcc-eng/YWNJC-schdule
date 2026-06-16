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
# 1. 页面基本配置与高级 UI 注入
# ==========================================
st.set_page_config(page_title="NJC运营仓数据中心", layout="wide")

# 注入自定义 CSS 让表格和按钮变漂亮，告别原生丑陋样式
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 800; letter-spacing: -0.5px; }
    h2, h3 { color: #2563EB; font-weight: 700; }
    .stButton>button { width: 100%; border-radius: 6px; font-weight: 600; height: 3rem; }
    div[data-testid="stExpander"] { background-color: #F8FAFC; border-radius: 8px; border: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 侧边栏导航控制
# ==========================================
st.sidebar.markdown("# 🏢 NJC 数据管理中心")
page = st.sidebar.radio("请选择要查看的功能：", ["📊 劳务排班预测", "📋 运营交接清单"])

# ==========================================
# 功能一：劳务排班预测
# ==========================================
if page == "📊 劳务排班预测":
    st.title("⚙️ NJC运营仓 - 下午班次劳务排班预测")
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
# 功能二：运营交接清单 (超美观全面看板版)
# ==========================================
elif page == "📋 运营交接清单":
    st.title("📋 NJC仓运营交接清单")
    st.caption("📱 数字化工作流：双击表格即可输入，保存后自动同步至下方历史大盘。")
    
    # 顶部控制面板
    with st.container(border=True):
        col_date, col_wh, col_user = st.columns([1.5, 1, 1.5])
        with col_date:
            selected_date = st.date_input("📆 选择操作日志日期", datetime.date.today())
        
        date_key = str(selected_date)
        global_db = load_global_data()
        
        # 初始化空白结构
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
        
        day_data = global_db[date_key]
        
        with col_wh:
            wh_val = st.text_input("🏠 仓库名称", value=day_data.get("warehouse", "NJC仓"), key=f"wh_{date_key}")
        with col_user:
            sv_val = st.text_input("👤 当班值班主管", value=day_data.get("supervisor", ""), key=f"sv_{date_key}", placeholder="请输入主管姓名")
        
    # --- 核心表单填写区 ---
    st.markdown("### 📝 今日运营数据登记")
    
    tab1, tab2, tab3 = st.tabs(["📌 一、早班清单 & 特殊事件", "🚚 二、清关提货登记", "📦 三、渠道发货记录"])
    
    with tab1:
        st.subheader("一、早班日常工作自查")
        df_morning = pd.DataFrame(day_data["morning_tasks"])
        edited_morning = st.data_editor(df_morning, use_container_width=True, hide_index=True, key=f"edit_morning_{date_key}")
        
        st.markdown("---")
        st.subheader("四、特殊事件及延误跟进")
        df_events = pd.DataFrame(day_data["special_events"])
        edited_events = st.data_editor(df_events, use_container_width=True, hide_index=True, num_rows="dynamic", key=f"edit_events_{date_key}")

    with tab2:
        st.subheader("二、早班叫车与清关行提货记录")
        df_customs = pd.DataFrame(day_data["customs_data"])
        edited_customs = st.data_editor(df_customs, use_container_width=True, hide_index=True, key=f"edit_customs_{date_key}")
        
    with tab3:
        st.subheader("三、渠道发货出库记录")
        df_shipping = pd.DataFrame(day_data["shipping_data"])
        edited_shipping = st.data_editor(df_shipping, use_container_width=True, hide_index=True, key=f"edit_shipping_{date_key}")
        
    # 交接确认行
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### ✍️ 五、团队交接签署确认")
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        s1 = col_s1.text_input("交班人 :", value=day_data.get("sign1", ""), key=f"s1_{date_key}")
        s2 = col_s2.text_input("接班人 :", value=day_data.get("sign2", ""), key=f"s2_{date_key}")
        s3 = col_s3.text_input("主管 :", value=day_data.get("sign3", ""), key=f"s3_{date_key}")
        s4 = col_s4.text_input("区域经理 :", value=day_data.get("sign4", ""), key=f"s4_{date_key}")
        
    # 控制按钮
    st.markdown(" ")
    col_btn1, col_btn2, _ = st.columns([2, 2, 4])
    with col_btn1:
        if st.button("💾 点击锁定并保存今日交接单", type="primary"):
            global_db[date_key] = {
                "warehouse": wh_val,
                "supervisor": sv_val,
                "morning_tasks": edited_morning.to_dict(orient="records"),
                "customs_data": edited_customs.to_dict(orient="records"),
                "shipping_data": edited_shipping.to_dict(orient="records"),
                "special_events": edited_events.to_dict(orient="records"),
                "sign1": s1, "sign2": s2, "sign3": s3, "sign4": s4
            }
            save_global_data(global_db)
            st.success(f"🎉 成功保存 {date_key} 数据！已自动沉淀到下方大盘。")
            st.rerun()
            
    with col_btn2:
        if st.button("🧹 清空当前选中日期的草稿", type="secondary"):
            if date_key in global_db:
                del global_db[date_key]
                save_global_data(global_db)
                st.rerun()

    # ==========================================
    # 3. 📉 【直观高级数据可视化大盘】（发货+提货双管齐下）
    # ==========================================
    st.markdown("---")
    st.header("📊 NJC 仓运管核心数据流水大盘")
    st.caption("系统自动抽取历史保存的所有记录，平铺展示最直观的流水账本。")

    all_history = load_global_data()
    
    if all_history:
        # 提取提货（清关）流水
        customs_rows = []
        # 提取发货渠道流水
        shipping_rows = []
        
        for date, content in all_history.items():
            wh = content.get("warehouse", "NJC仓")
            sv = content.get("supervisor", "")
            
            # 解析提货
            for row in content.get("customs_data", []):
                if row.get("状态") or row.get("数量") or row.get("时间"): # 过滤空行
                    customs_rows.append({
                        "日期": date, "仓库": wh, "值班主管": sv,
                        "清关行": row.get("清关行", ""), "状态": row.get("状态", ""),
                        "提货车数/数量": row.get("数量", ""), "提货到场时间": row.get("时间", "")
                    })
                    
            # 解析发货
            for row in content.get("shipping_data", []):
                if row.get("货量") or row.get("时间") or row.get("人"): # 过滤空行
                    shipping_rows.append({
                        "日期": date, "仓库": wh, "值班主管": sv,
                        "发货渠道": row.get("渠道", ""), "出库货量(件)": row.get("货量", ""),
                        "发货交接时间": row.get("时间", ""), "现场负责人": row.get("人", "")
                    })

        # 渲染两个大盘
        # 渲染两个大盘
        panel1, panel2 = st.columns(2)
        
        with panel1:
            st.subheader("🚚 历史提货（清关行）流水总账")
            if customs_rows:
                df_c_excel = pd.DataFrame(customs_rows)
                st.dataframe(df_c_excel, use_container_width=True, hide_index=True)
                # 提货下载
                csv_c = df_c_excel.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 导出提货历史 Excel", data=csv_c, file_name=f"NJC提货大盘_{datetime.date.today()}.csv", mime="text/csv", key="dl_c")
            else:
                st.info("💡 暂无提货流水明细")

        with panel2:
            st.subheader("📦 历史发货（渠道出库）流水总账")
            if shipping_rows:
                df_s_excel = pd.DataFrame(shipping_rows)
                # --- 核心新增功能：数据清洗与统计 ---
                # 将货量列强制转换为数字
                df_s_excel['出库货量(件)'] = pd.to_numeric(df_s_excel['出库货量(件)'], errors='coerce').fillna(0)
                
                # 1. 每日货量汇总表
                daily_summary = df_s_excel.groupby('日期')['出库货量(件)'].sum().reset_index().sort_values(by='日期', ascending=False)
                st.write("📈 **近况货量汇总**")
                st.table(daily_summary.head(7)) # 显示最近7天
                
                # 2. 货量趋势图
                st.line_chart(daily_summary.set_index('日期'))
                
                # 3. 原始流水账展示
                st.dataframe(df_s_excel, use_container_width=True, hide_index=True)
                
                # 导出发货下载
                csv_s = df_s_excel.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 导出发货历史 Excel", data=csv_s, file_name=f"NJC发货大盘_{datetime.date.today()}.csv", mime="text/csv", key="dl_s")
            else:
                st.info("💡 暂无发货渠道流水明细")
    else:
        st.info("💡 目前数据库空空如也，请在上方填写并点击保存，数据大盘将自动为您亮起！")
    else:
        st.info("💡 目前数据库空空如也，请在上方填写并点击保存，数据大盘将自动为您亮起！")
