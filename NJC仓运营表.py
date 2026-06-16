import streamlit as st
import pandas as pd
import math
import json
import os

# --- 配置与数据存储 ---
DB_FILE = "njc_database.json"
st.set_page_config(page_title="NJC 智能运营系统", layout="wide", page_icon="🚀")

# --- UI 美化 CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F9; }
    .css-1v0mbdj { border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    h1 { color: #1E3A8A; }
    .metric-card { background: white; padding: 15px; border-radius: 10px; border-left: 5px solid #2563EB; }
    </style>
""", unsafe_allow_html=True)

# --- 核心排班算法 ---
def calculate_labor(volume_data, base_uph, hours, break_m=45, loss_m=15):
    net_hours = hours - (break_m/60) - (loss_m/60)
    results = []
    total_workers = 0
    for process, vol in volume_data.items():
        # 疲劳衰减：前4小时100%，中3小时90%，剩余80%
        uph = base_uph.get(process, 100)
        adj_uph = ( (4 * uph) + (3 * uph * 0.9) + ((net_hours-7) * uph * 0.8) ) / net_hours if net_hours > 7 else uph
        workers = math.ceil(vol / adj_uph / net_hours)
        total_workers += workers
        results.append({"环节": process, "货量": vol, "衰减后UPH": round(adj_uph, 1), "建议人数": workers})
    return results, total_workers

# --- 侧边栏与登录 ---
st.sidebar.title("🏢 NJC 运营中心")
if st.sidebar.text_input("🔑 登录密码", type="password") != "20260616":
    st.warning("⚠️ 请输入系统密码")
    st.stop()

menu = st.sidebar.radio("🚀 功能导航", ["📋 每日交接清单", "⚙️ 人体工效学排班预测"])

# --- 页面逻辑 ---
if menu == "📋 每日交接清单":
    st.title("📋 每日运营交接清单")
    # 这里保留你原有的保存逻辑...
    st.info("数据将实时固化并供预测模型使用。")
    
elif menu == "⚙️ 人体工效学排班预测":
    st.title("⚙️ 智能劳务排班预测")
    
    with st.expander("📊 设置预测参数", expanded=True):
        col1, col2, col3 = st.columns(3)
        v1 = col1.number_input("卸货件数", 1500)
        v2 = col2.number_input("上架件数", 1200)
        v3 = col3.number_input("拣货件数", 3000)
        uph = col3.number_input("标准人员UPH", 100)
        
    data = {"Unloading": v1, "Putaway": v2, "Picking": v3}
    base_uph = {"Unloading": uph, "Putaway": uph, "Picking": uph}
    
    res, total = calculate_labor(data, base_uph, 10.0)
    
    st.markdown("---")
    st.subheader("💡 预测分析结果")
    st.table(pd.DataFrame(res))
    st.metric("👤 下午班次总需求人数", f"{total} 人", delta="基于疲劳修正模型")
