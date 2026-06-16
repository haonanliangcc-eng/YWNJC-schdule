import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# 配置文件名
DB_FILE = "operation_data.json"

# 初始化数据：如果文件不存在则创建一个模板
def init_db():
    if not os.path.exists(DB_FILE):
        default_data = {
            "columns": ["工作内容", "完成", "责任人"],
            "rows": [
                {"工作内容": "NJC仓派送装车完成", "完成": False, "责任人": ""},
                {"工作内容": "GOFO司机取货完成", "完成": False, "责任人": ""},
            ]
        }
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f)

# 加载数据
def load_data():
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return pd.DataFrame(data['rows'])

# 保存数据
def save_data(df):
    data = {"rows": df.to_dict(orient='records')}
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# 主程序逻辑
st.title("📋 NJC仓运营交接清单")
today = datetime.now().strftime("%Y/%m/%d")
st.subheader(f"📅 当前日期: {today}")

init_db()
df = load_data()

# 可视化编辑表格
st.write("### 操作面板")
edited_df = st.data_editor(df, use_container_width=True)

# 保存按钮
if st.button("💾 保存今日数据到后台"):
    save_data(edited_df)
    st.balloons()
    st.success("数据已成功沉淀至系统后台！")

# 导出 Excel
st.write("---")
if st.button("📥 导出为 Excel"):
    edited_df.to_excel("NJC_Report.xlsx", index=False)
    st.download_button("点击下载 Excel", data=open("NJC_Report.xlsx", "rb"), file_name=f"NJC_{today.replace('/', '-')}.xlsx")
