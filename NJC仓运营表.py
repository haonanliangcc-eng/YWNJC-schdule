import streamlit as st
import datetime
import pandas as pd
import json
import os
import math

# ================= 数据持久化 =================
DB_FILE = "njc_database.json"
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}
def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="NJC 智能运营系统", layout="wide")

# ================= 登录系统 (修复了报错) =================
st.sidebar.markdown("# 🏢 NJC 数据管理中心")
user = st.sidebar.text_input("👤 主管姓名", key="user_id")
pwd = st.sidebar.text_input("🔑 登录密码", type="password", key="pass_id")

if pwd != "20260616":
    st.warning("⚠️ 请输入正确密码以进入系统。")
    st.stop()

menu = st.sidebar.radio("🚀 导航", ["📋 每日交接清单", "📊 劳务排班预测"])

# ================= 每日交接清单 =================
if menu == "📋 每日交接清单":
    st.title("📋 每日运营交接清单")
    date_val = str(st.date_input("📅 日期", datetime.date.today()))
    db = load_data()
    if date_val not in db:
        db[date_val] = {
            "tasks": [{"工作内容": x, "完成": False, "责任人": ""} for x in ["NJC装车", "GOFO取货", "SPX取货", "DD301取货", "UNI取货", "Temu退货", "异常登记"]],
            "customs": [{"清关行": k, "状态": "", "数量": "", "时间": ""} for k in ["YUEJIE", "六脉", "mirage", "AGS", "Tolead", "SF", "R&T", "DD", "机场"]],
            "shipping": [{"渠道": k, "货量": "", "时长": "", "人": ""} for k in ["GOFO", "SPX", "DD301", "UNI", "TEMU"]]
        }
    
    with st.expander("📝 数据录入", expanded=True):
        edit_t = st.data_editor(pd.DataFrame(db[date_val]["tasks"]), use_container_width=True)
        edit_c = st.data_editor(pd.DataFrame(db[date_val]["customs"]), use_container_width=True)
        edit_s = st.data_editor(pd.DataFrame(db[date_val]["shipping"]), use_container_width=True)
        if st.button("💾 保存数据"):
            db[date_val] = {"tasks": edit_t.to_dict("records"), "customs": edit_c.to_dict("records"), "shipping": edit_s.to_dict("records")}
            save_data(db)
            st.success("✅ 保存成功！")
            st.rerun()

# ================= 劳务排班预测 (Pro版) =================
elif menu == "📊 劳务排班预测":
    st.title("⚙️ 人体工效学劳务预测模型")
    col1, col2, col3 = st.columns(3)
    v1 = col1.number_input("卸货件数", 1500)
    v2 = col2.number_input("上架件数", 1200)
    v3 = col3.number_input("拣货件数", 3000)
    
    uph = st.number_input("标准人员UPH", 100)
    hours = st.number_input("有效工时", 8.0)
    
    # 疲劳衰减修正：总件数 / (UPH * 工时) * 1.15 (疲劳储备)
    res = ((v1 + v2 + v3) / uph / hours) * 1.15
    st.metric("👤 建议配置人数", f"{round(res, 1)} 人")
    st.write("公式：`总件数 / (UPH * 有效工时) * 1.15(疲劳修正系数)`")
