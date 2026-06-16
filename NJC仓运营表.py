# 1. 安装 streamlit 库
!pip install -q streamlit

# 2. 写入完整的 Streamlit 整合代码到本地 app.py 文件中
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('''
import streamlit as st

# 1. 页面基本配置
st.set_page_config(page_title="NJC运营仓数据中心", layout="wide")

# 2. 侧边栏导航控制
st.sidebar.title("导航菜单")
page = st.sidebar.radio("请选择要查看的功能：", ["📊 劳务排班预测", "📋 运营交接清单"])

# ==========================================
# 功能一：劳务排班预测 (你原有的功能)
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
# 功能二：运营交接清单 (原生精美网页界面嵌入)
# ==========================================
elif page == "📋 运营交接清单":
    html_code = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NJC仓运营交接清单 - Pro</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-bg: #ffffff;
                --section-bg: #f8f9fa;
                --border-color: #000000;
                --text-main: #1a1a1a;
                --accent-color: #0046ad;
            }
            body {
                font-family: 'Inter', "Microsoft YaHei", sans-serif;
                margin: 10px 30px;
                padding: 0;
                background-color: var(--primary-bg) !important;
                color: var(--text-main) !important;
                line-height: 1.4;
            }
            h1 {
                text-align: center;
                font-size: 24px;
                font-weight: 700;
                margin: 0 0 10px 0;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            h2 {
                background-color: var(--section-bg);
                border: 1.5px solid var(--border-color);
                padding: 4px 10px;
                font-size: 14px;
                font-weight: 700;
                margin: 10px 0 5px 0;
                display: flex;
                align-items: center;
            }
            .info-header {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-bottom: 10px;
                font-size: 13px;
            }
            .info-header input {
                border: none;
                border-bottom: 1px solid var(--border-color);
                font-family: inherit;
                padding: 0 5px;
                outline: none;
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 2px;
            }
            th, td {
                border: 1px solid var(--border-color);
                padding: 5px 8px;
                font-size: 12px;
                height: 22px;
            }
            th {
                background-color: #eeeeee;
                font-weight: 600;
                text-align: center;
            }
            input[type="text"] {
                width: 100%;
                border: none;
                outline: none;
                font-size: 12px;
                background: transparent;
            }
            input[type="checkbox"] {
                transform: scale(1.1);
                cursor: pointer;
            }
            .grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                align-items: start;
            }
            .signature-section {
                margin-top: 10px;
                padding: 8px;
                border: 1px dashed #666;
                background-color: #fafafa;
            }
            .signature-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                row-gap: 8px;
                column-gap: 40px;
            }
            .sig-item {
                font-size: 13px;
                font-weight: 500;
                white-space: nowrap;
            }
            .sig-line {
                display: inline-block;
                width: 160px;
                border-bottom: 1px solid var(--border-color);
                margin-left: 5px;
                vertical-align: bottom;
                height: 18px;
            }
            .btn-container {
                text-align: center;
                margin-top: 20px;
                margin-bottom: 20px;
                display: flex;
                justify-content: center;
                gap: 15px;
            }
            .print-btn, .clear-btn {
                border: none;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 4px;
                cursor: pointer;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            .print-btn { background: var(--accent-color); color: white; }
            .clear-btn { background: #dc3545; color: white; }
            @media print {
                @page { size: A4; margin: 0.5cm; }
                .btn-container { display: none; }
                body { margin: 0; transform: scale(0.96); transform-origin: top center; }
                h2#section-5 { margin-top: 5px; font-size: 12px; padding: 2px 8px; }
                .signature-section { margin-top: 5px; padding: 4px; }
                .sig-item { font-size: 11px; }
                .signature-grid { row-gap: 4px; }
                #special-events-table td { height: 18px; }
            }
        </style>
    </head>
    <body>
        <h1>NJC仓运营交接清单</h1>
        <div class="info-header">
            <div>日期 :  <input type="date" id="current-date" style="width: 130px;" onchange="handleDateChange()"></div>
            <div>仓库 :  <input type="text" id="warehouse-name" value="NJC仓" style="width: 70px; font-weight: bold;"></div>
            <div>值班主管 :  <input type="text" id="supervisor" placeholder="签字确认" style="width: 100px;"></div>
        </div>
        
        <h2>一、早班工作清单</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 65%;">工作内容</th>
                    <th style="width: 10%;">完成</th>
                    <th style="width: 25%;">责任人</th>
                </tr>
            </thead>
            <tbody id="morning-tasks">
                <tr><td>NJC仓派送货装车完成</td><td align="center"><input type="checkbox"></td><td><input type="text"></td></tr>
                <tr><td>GOFO司机取货完成</td><td align="center"><input type="checkbox"></td><td><input type="text"></td></tr>
                <tr><td>SPX司机取货完成</td><td align="center"><input type="checkbox"></td><td><input type="text"></td></tr>
                <tr><td>DD301司机取货完成</td><td align="center"><input type="checkbox"></td><td><input type="text"></td></tr>
                <tr><td>UNI司机取货完成</td><td align="center"><input type="checkbox"></td><td><input type="text"></td></tr>
                <tr><td>Temu退货接收登记完成</td><td align="center"><input type="checkbox"></td><td><input type="text"></td></tr>
                <tr><td>异常包裹登记完成</td><td align="center"><input type="checkbox"></td><td><input type="text"></td></tr>
            </tbody>
        </table>

        <div class="grid-container">
            <div class="left-col">
                <h2>二、早班叫车与清关行提货</h2>
                <table>
                    <thead>
                        <tr>
                            <th style="width: 25%;">清关行</th>
                            <th style="width: 35%;">状态</th>
                            <th style="width: 20%;">数量</th>
                            <th style="width: 20%;">时间</th>
                        </tr>
                    </thead>
                    <tbody id="customs-clearance">
                        <tr><td><strong>YUEJIE</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>六脉</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>mirage</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>AGS</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>Tolead</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>SF</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>R&T</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>DD</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>机场</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                    </tbody>
                </table>
            </div>
            <div class="right-col">
                <h2>三、渠道发货记录</h2>
                <table>
                    <thead>
                        <tr>
                            <th style="width: 25%;">渠道</th>
                            <th style="width: 30%;">货量</th>
                            <th style="width: 25%;">时间</th>
                            <th style="width: 20%;">人</th>
                        </tr>
                    </thead>
                    <tbody id="shipping-channels">
                        <tr><td><strong>GOFO</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>SPX</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>DD301</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>UNI</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><strong>TEMU</strong></td><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                    </tbody>
                </table>
                <h2 style="margin-top: 8px;">四、特殊事件及延误</h2>
                <table id="special-events-table">
                    <thead>
                        <tr>
                            <th style="width: 20%;">时间</th>
                            <th style="width: 50%;">内容</th>
                            <th style="width: 30%;">措施</th>
                        </tr>
                    </thead>
                    <tbody id="special-events">
                        <tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                        <tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <h2 id="section-5">五、交接确认</h2>
        <div class="signature-section">
            <div class="signature-grid">
                <div class="sig-item">交班人签字 : <span class="sig-line"></span></div>
                <div class="sig-item">接班人签字 : <span class="sig-line"></span></div>
                <div class="sig-item">主管签字 : <span class="sig-line"></span></div>
                <div class="sig-item">区域经理签字 : <span class="sig-line"></span></div>
            </div>
        </div>

        <div class="btn-container">
            <button class="print-btn" onclick="window.print()">生成 A4 打印预览</button>
            <button class="clear-btn" onclick="clearCurrentDayData()">清空今日数据</button>
        </div>

        <script>
            function getStorageKey() {
                const dateStr = document.getElementById('current-date').value || getTodayStr();
                return `NJC_Data_${dateStr}`;
            }
            function getTodayStr() {
                const today = new Date();
                return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
            }
            window.addEventListener('DOMContentLoaded', () => {
                initDate();
                loadSavedData();
                setupAutoSave();
            });
            function initDate() {
                const dateInput = document.getElementById('current-date');
                if (!dateInput.value) { dateInput.value = getTodayStr(); }
            }
            function setupAutoSave() {
                document.body.addEventListener('input', debounceSave);
                document.body.addEventListener('change', debounceSave);
            }
            let saveTimeout;
            function debounceSave() {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(saveData, 500);
            }
            function saveData() {
                const key = getStorageKey();
                const data = {
                    warehouse: document.getElementById('warehouse-name').value,
                    supervisor: document.getElementById('supervisor').value,
                    inputs: [],
                    checkboxes: []
                };
                document.querySelectorAll('input[type="text"]').forEach((input, index) => {
                    data.inputs.push({ index, value: input.value });
                });
                document.querySelectorAll('input[type="checkbox"]').forEach((checkbox, index) => {
                    data.checkboxes.push({ index, checked: checkbox.checked });
                });
                localStorage.setItem(key, JSON.stringify(data));
            }
            function loadSavedData() {
                resetFormToBlank();
                const key = getStorageKey();
                const savedData = localStorage.getItem(key);
                if (!savedData) return;
                try {
                    const data = JSON.parse(savedData);
                    if (data.warehouse) document.getElementById('warehouse-name').value = data.warehouse;
                    if (data.supervisor) document.getElementById('supervisor').value = data.supervisor;
                    const textInputs = document.querySelectorAll('input[type="text"]');
                    if (data.inputs) {
                        data.inputs.forEach(item => {
                            if (textInputs[item.index]) textInputs[item.index].value = item.value;
                        });
                    }
                    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
                    if (data.checkboxes) {
                        data.checkboxes.forEach(item => {
                            if (checkboxes[item.index]) checkboxes[item.index].checked = item.checked;
                        });
                    }
                } catch (e) { console.error("加载数据失败:", e); }
            }
            function resetFormToBlank() {
                document.querySelectorAll('input[type="text"]').forEach(input => {
                    if (input.id !== 'warehouse-name') input.value = '';
                });
                document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                    checkbox.checked = false;
                });
                document.getElementById('supervisor').value = '';
            }
            function handleDateChange() { loadSavedData(); }
            function clearCurrentDayData() {
                if (confirm('确定要清空【当前所选日期】的所有输入数据吗？')) {
                    resetFormToBlank();
                    localStorage.removeItem(getStorageKey());
                    saveData();
                }
            }
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=1100, scrolling=True)
''')

# 3. 使用 localtunnel 映射并启动服务
!npx localtunnel --port 8501 & streamlit run app.py --server.port 8501
