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
# 1. 页面配置
# ==========================================
st.set_page_config(page_title="NJC运营仓数据中心", layout="wide")
page = st.sidebar.radio("请选择要查看的功能：", ["📊 劳务排班预测", "📋 运营交接清单"])

# ==========================================
# 功能一：劳务排班预测 (保持不变)
# ==========================================
if page == "📊 劳务排班预测":
    st.title("⚙️ NJC运营仓 - 下午班次劳务排班预测")
    # ... (此处省略劳务预测部分代码，保持你原有的即可)

# ==========================================
# 功能二：运营交接清单 + 货量大盘
# ==========================================
elif page == "📋 运营交接清单":
    st.title("📋 NJC仓运营交接清单")
    
    # 1. 获取日期与全局数据
    selected_date = st.date_input("📆 选择操作日志日期", datetime.date.today())
    date_key = str(selected_date)
    global_db = load_global_data()
    
    # 如果日期不存在，初始化数据结构
    if date_key not in global_db:
        global_db[date_key] = {
            "warehouse": "NJC仓", "supervisor": "",
            "morning_tasks": [{"工作内容": "每日例行", "完成": False, "责任人": ""}],
            "customs_data": [{"清关行": k, "状态": "", "数量": "", "时间": ""} for k in ["YUEJIE", "六脉", "mirage", "AGS", "Tolead", "SF", "R&T", "DD", "机场"]],
            "shipping_data": [{"渠道": k, "货量": "", "时间": "", "人": ""} for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]],
            "special_events": [{"时间": "", "内容": "", "措施": ""}]
        }
    
    day_data = global_db[date_key]
    
    # 2. 表单输入区
    wh_val = st.text_input("🏠 仓库名称", value=day_data.get("warehouse", "NJC仓"))
    sv_val = st.text_input("👤 值班主管", value=day_data.get("supervisor", ""))
    
    tab1, tab2, tab3 = st.tabs(["📌 早班清单", "🚚 清关提货登记", "📦 渠道发货记录"])
    
    with tab1:
        edited_morning = st.data_editor(pd.DataFrame(day_data["morning_tasks"]), num_rows="dynamic", use_container_width=True)
    with tab2:
        edited_customs = st.data_editor(pd.DataFrame(day_data["customs_data"]), num_rows="dynamic", use_container_width=True)
    with tab3:
        edited_shipping = st.data_editor(pd.DataFrame(day_data["shipping_data"]), num_rows="dynamic", use_container_width=True)
    
    # 保存按钮
    if st.button("💾 保存今日交接单"):
        global_db[date_key] = {
            "warehouse": wh_val, "supervisor": sv_val,
            "morning_tasks": edited_morning.to_dict(orient="records"),
            "customs_data": edited_customs.to_dict(orient="records"),
            "shipping_data": edited_shipping.to_dict(orient="records"),
            "special_events": day_data.get("special_events", [])
        }
        save_global_data(global_db)
        st.success("数据已保存！")
        st.rerun()
        
    # 3. 核心大盘 (自动统计)
    st.markdown("---")
    st.header("📊 NJC 仓运管核心数据流水大盘")
    all_history = load_global_data()
    
    shipping_rows = []
    for date, content in all_history.items():
        for row in content.get("shipping_data", []):
            if row.get("货量"):
                shipping_rows.append({"日期": date, "出库货量(件)": row.get("货量")})
    
    if shipping_rows:
        df_s = pd.DataFrame(shipping_rows)
        df_s['出库货量(件)'] = pd.to_numeric(df_s['出库货量(件)'], errors='coerce').fillna(0)
        daily_summary = df_s.groupby('日期')['出库货量(件)'].sum().reset_index().sort_values(by='日期', ascending=False)
        
        st.write("📈 **近况货量汇总**")
        st.table(daily_summary.head(7))
        st.line_chart(daily_summary.set_index('日期'))
    else:
        st.info("💡 暂无发货记录，填写表格并点击保存即可看到统计数据。")
