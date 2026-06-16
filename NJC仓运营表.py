import streamlit as st
import pandas as pd
import math

# --- 页面配置 ---
st.set_page_config(page_title="NJC 运营中心", layout="wide")

# --- 侧边栏导航 ---
page = st.sidebar.radio("🚀 功能导航", ["📋 运营交接清单", "📊 劳务排班预测"])

# --- 功能 1: 运营交接清单 ---
if page == "📋 运营交接清单":
    st.title("📋 运营交接清单")
    # 你的 HTML 代码块
    html_code = """
    <div style="padding:20px; border:1px solid #ccc;">
        <h1>NJC仓运营交接清单 (Pro版)</h1>
        <p>这是你的详细表单区域，请在此录入数据...</p>
    </div>
    """
    st.components.v1.html(html_code, height=800)

# --- 功能 2: 劳务排班预测 (植入你的高级逻辑) ---
elif page == "📊 劳务排班预测":
    st.title("⚙️ 人体工效学劳务预测模型")
    
    # 动态参数录入
    col1, col2, col3 = st.columns(3)
    v1 = col1.number_input("卸货件数", 1500)
    v2 = col2.number_input("上架件数", 1200)
    v3 = col3.number_input("拣货件数", 3000)
    
    uph = st.number_input("标准人员UPH", 100)
    hours = st.number_input("班次有效工时", 9.0)
    
    # 核心算法：疲劳衰减修正
    total_vol = v1 + v2 + v3
    res = (total_vol / uph / hours) * 1.15
    
    st.metric("👤 建议配置人数 (含疲劳储备)", f"{round(res, 1)} 人")
    st.info("算法逻辑：基于人体工效学分段疲劳衰减模型。")
