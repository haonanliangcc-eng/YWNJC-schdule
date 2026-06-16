import streamlit as st
import streamlit.components.v1 as components
from datetime import date

# 1. 页面基本配置
st.set_page_config(page_title="NJC运营仓数据中心", layout="wide")

# 2. 侧边栏导航控制
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
    col1, col2, col3 = st.columns(3)
    v1 = col1.number_input("1_Unloading (卸货入库/件)", value=1500)
    v2 = col2.number_input("2_Putaway (库位上架/件)", value=1200)
    v3 = col3.number_input("3_Picking (库区拣货/件)", value=3000)
    
    col4, col5, col6 = st.columns(3)
    v4 = col4.number_input("4_Packing (复核打包/件)", value=2500)
    v5 = col5.number_input("5_Labeling (贴面单/件)", value=2500)
    v6 = col6.number_input("6_Dispatch (称重装车/件)", value=2800)

    st.markdown("---")
    st.header("🚀 预测劳务人数")
    net_hours = shift_hours - (rest_mins/60) - handover_hours
    st.metric("👤 单人每日净工时", f"{net_hours:.2f} 小时")
    
    # 假设的标准UPH计算
    total_needed = round((v1/120 + v2/80 + v3/100 + v4/80 + v5/150 + v6/200) / net_hours)
    st.subheader(f"🔥 下午班次总计需通知劳务到场 : :blue[{total_needed} 人]")

# ==========================================
# 功能二：运营交接清单 (精美HTML界面)
# ==========================================
elif page == "📋 运营交接清单":
    html_code = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: 'Inter', sans-serif; margin: 20px; background: #fff; }
            h1 { text-align: center; color: #0046ad; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { border: 1px solid #000; padding: 8px; font-size: 14px; }
            th { background: #eee; }
            .btn-container { text-align: center; margin-top: 20px; }
            button { padding: 10px 20px; cursor: pointer; background: #0046ad; color: white; border: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>NJC仓运营交接清单</h1>
        <div style="text-align: center; margin-bottom: 20px;">
            日期: <input type="date" id="date-input">
        </div>
        <table>
            <tr><th width="60%">工作内容</th><th width="10%">完成</th><th width="30%">责任人</th></tr>
            <tr><td>NJC仓装车完成</td><td><input type="checkbox"></td><td><input type="text"></td></tr>
            <tr><td>GOFO司机取货</td><td><input type="checkbox"></td><td><input type="text"></td></tr>
            <tr><td>SPX司机取货</td><td><input type="checkbox"></td><td><input type="text"></td></tr>
        </table>
        <div class="btn-container">
            <button onclick="window.print()">生成 A4 打印预览</button>
        </div>
        <script>
            document.getElementById('date-input').valueAsDate = new Date();
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=900, scrolling=True)
