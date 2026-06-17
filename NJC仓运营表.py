import streamlit as st
import datetime
import pandas as pd
import json
import os
import math

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
    :root {
        --navy: #111827;
        --blue: #2563EB;
        --cyan: #0891B2;
        --green: #16A34A;
        --ink: #111827;
        --muted: #374151;
        --line: #D8E0EA;
        --panel: #FFFFFF;
        --soft: #F5F8FC;
    }

    .stApp {
        background: #F6F8FC;
        color: #111827;
    }

    .stApp, .stApp * {
        color: #111827;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #F6F8FC !important;
        color: #111827 !important;
    }

    [data-testid="stHeader"]::before,
    [data-testid="stHeader"]::after {
        background: #F6F8FC !important;
    }

    .block-container {
        padding-top: 1.65rem;
        padding-bottom: 2.25rem;
        max-width: 1540px;
    }

    h1 {
        color: #111827;
        font-weight: 800;
        letter-spacing: 0;
        margin-bottom: 0.25rem;
    }

    h2, h3 {
        color: #111827;
        font-weight: 750;
        letter-spacing: 0;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F1B33 0%, #142655 55%, #132A5F 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] * {
        color: #D9E6F7 !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #93A8C8 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        background: transparent;
        border: 0;
        border-radius: 12px;
        padding: 0.72rem 0.8rem;
        margin-bottom: 0.25rem;
        box-shadow: none;
    }

    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(37, 99, 235, 0.22);
    }

    div[data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stMetric"] label {
        color: #111827;
        font-weight: 650;
    }

    .stButton>button,
    .stDownloadButton>button,
    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        height: 2.9rem;
        border: 1px solid rgba(37, 99, 235, 0.25);
        box-shadow: none;
    }

    .stButton>button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button[kind="primary"] {
        background: linear-gradient(135deg, var(--blue), var(--cyan));
        border: 0;
    }

    input, textarea, [data-baseweb="select"] {
        border-radius: 10px !important;
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }

    [data-baseweb="input"],
    [data-baseweb="base-input"],
    [data-testid="stNumberInput"] div,
    [data-testid="stNumberInput"] button,
    [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border-color: #D8E0EA !important;
    }

    [data-testid="stNumberInput"] button {
        background: #F4F7FB !important;
        color: #111827 !important;
        border-left: 1px solid #D8E0EA !important;
        box-shadow: none !important;
    }

    [data-testid="stNumberInput"] button svg,
    [data-testid="stNumberInput"] button svg * {
        fill: #111827 !important;
        color: #111827 !important;
        stroke: #111827 !important;
    }

    [data-testid="stNumberInput"] input {
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stSlider"] *,
    [data-testid="stSlider"] div {
        color: #111827 !important;
    }

    [data-testid="stSlider"] [data-baseweb="slider"] {
        background: transparent !important;
    }

    label, p, span, div {
        color: #111827;
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stDataEditor"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 10px 28px rgba(23, 50, 77, 0.05);
    }

    div[data-testid="stDataFrame"] *,
    div[data-testid="stDataEditor"] * {
        color: #172033 !important;
    }

    div[data-testid="stDataFrame"] [role="grid"],
    div[data-testid="stDataEditor"] [role="grid"],
    div[data-testid="stDataFrame"] [role="row"],
    div[data-testid="stDataEditor"] [role="row"],
    div[data-testid="stDataFrame"] [role="columnheader"],
    div[data-testid="stDataEditor"] [role="columnheader"],
    div[data-testid="stDataFrame"] [role="gridcell"],
    div[data-testid="stDataEditor"] [role="gridcell"] {
        background-color: #FFFFFF !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"],
    div[data-testid="stDataEditor"] [role="columnheader"] {
        background-color: #EEF4FB !important;
        color: #111827 !important;
        font-weight: 700 !important;
    }

    div[data-testid="stTabs"] button {
        font-weight: 700;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border-color: #DDE5EF !important;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        background: #FFFFFF;
    }

    .njc-login-panel {
        max-width: 460px;
        margin: 5vh auto 0 auto;
        padding: 1.4rem 1.7rem 0.4rem;
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 8px;
        box-shadow: 0 18px 48px rgba(23, 50, 77, 0.10);
    }

    div[data-testid="stForm"] {
        max-width: 460px;
        margin: 0 auto;
        padding: 0.2rem 1.7rem 1.6rem;
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-top: 0;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 18px 48px rgba(23, 50, 77, 0.10);
    }

    .njc-login-title {
        font-size: 1.55rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 0.25rem;
    }

    .njc-login-subtitle {
        color: #111827;
        margin-bottom: 1.1rem;
    }

    .njc-section-note {
        padding: 0.75rem 0.95rem;
        background: #EAF6FB;
        border-left: 4px solid var(--cyan);
        border-radius: 12px;
        color: #111827;
        margin-bottom: 1rem;
    }

    .njc-app-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: #FFFFFF;
        border: 1px solid #E1E7EF;
        border-radius: 16px;
        padding: 1.25rem 1.45rem;
        margin-bottom: 1.45rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
    }

    .njc-header-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        background: #DBEAFE;
        color: #2563EB;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.55rem;
        flex: 0 0 auto;
    }

    .njc-header-title {
        font-size: 1.65rem;
        line-height: 1.1;
        font-weight: 850;
        color: #0B1F3A;
    }

    .njc-header-subtitle {
        margin-top: 0.28rem;
        color: #8AA0BD;
        font-size: 1.02rem;
    }

    .njc-card {
        background: #FFFFFF;
        border: 1px solid #DDE5EF;
        border-radius: 16px;
        padding: 1.35rem 1.45rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }

    .njc-card-title {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 1.05rem;
        font-weight: 850;
        color: #0B1F3A;
        margin-bottom: 1rem;
    }

    .njc-kpi-blue {
        background: linear-gradient(135deg, #2563EB 0%, #2F6FED 100%);
        border-radius: 16px;
        padding: 1.25rem 1.35rem;
        min-height: 132px;
        box-shadow: 0 14px 30px rgba(37, 99, 235, 0.22);
    }

    .njc-kpi-blue .kpi-label,
    .njc-kpi-blue .kpi-sub {
        color: #DCEBFF !important;
        font-weight: 700;
    }

    .njc-kpi-blue .kpi-value {
        color: #FFFFFF !important;
        font-size: 2.8rem;
        line-height: 1.05;
        font-weight: 900;
        margin-top: 0.35rem;
    }

    .njc-mini-kpi {
        background: #FFFFFF;
        border: 1px solid #DDE5EF;
        border-radius: 16px;
        padding: 1.05rem 1.2rem;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        margin-bottom: 0.9rem;
    }

    .njc-mini-kpi-label {
        color: #60718A !important;
        font-size: 0.86rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
    }

    .njc-mini-kpi-value {
        color: #071D3A !important;
        font-size: 2rem;
        font-weight: 900;
        line-height: 1.05;
    }

    .njc-mini-kpi-sub {
        color: #8AA0BD !important;
        font-size: 0.88rem;
        margin-top: 0.45rem;
    }

    .njc-side-brand {
        display: flex;
        gap: 0.75rem;
        align-items: center;
        padding: 0.65rem 0.2rem 1.2rem;
        border-bottom: 1px solid rgba(255,255,255,0.09);
        margin-bottom: 1rem;
    }

    .njc-side-logo {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        background: #2F6FED;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.45rem;
    }

    .njc-side-title {
        color: #FFFFFF !important;
        font-weight: 850;
        font-size: 1.05rem;
        line-height: 1.1;
    }

    .njc-side-sub {
        color: #93A8C8 !important;
        font-size: 0.82rem;
        margin-top: 0.15rem;
    }

    .njc-user-chip {
        display: flex;
        gap: 0.75rem;
        align-items: center;
        padding: 0.85rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.09);
        margin-bottom: 1.15rem;
    }

    .njc-user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: rgba(47, 111, 237, 0.22);
        color: #62A0FF !important;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        border: 1px solid rgba(98,160,255,0.35);
    }

    .njc-user-name {
        color: #FFFFFF !important;
        font-weight: 850;
    }

    .njc-sidebar-label {
        color: #7186A7 !important;
        font-size: 0.78rem;
        font-weight: 800;
        margin: 0.5rem 0 0.55rem;
    }

    .njc-table-card {
        background: #FFFFFF;
        border: 1px solid #DDE5EF;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
        margin-bottom: 1.2rem;
    }

    .njc-table-card-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 1.25rem;
        background: #F8FAFD;
        border-bottom: 1px solid #E7EDF5;
        font-weight: 850;
        color: #0B1F3A;
    }

    .njc-edit-head {
        background: #F8FAFD;
        border: 1px solid #DDE5EF;
        border-radius: 14px 14px 0 0;
        padding: 1rem 1.25rem;
        font-weight: 850;
        color: #0B1F3A;
    }

    .njc-edit-row {
        background: #FFFFFF;
        border-left: 1px solid #DDE5EF;
        border-right: 1px solid #DDE5EF;
        border-bottom: 1px solid #E7EDF5;
        padding: 0.72rem 1.25rem;
    }

    .njc-edit-row:last-child {
        border-radius: 0 0 14px 14px;
    }

    .njc-edit-row input {
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #D8E0EA !important;
        box-shadow: none !important;
    }

    .njc-progress-line {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.85rem 1.25rem;
        background: #FFFFFF;
        border-left: 1px solid #DDE5EF;
        border-right: 1px solid #DDE5EF;
        border-bottom: 1px solid #E7EDF5;
    }

    .njc-progress-track {
        height: 8px;
        flex: 1;
        border-radius: 999px;
        background: #EEF2F7;
        overflow: hidden;
    }

    .njc-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #2563EB, #16A34A);
    }

    .njc-progress-count {
        color: #16A34A !important;
        font-weight: 850;
        min-width: 3rem;
        text-align: right;
    }

    .njc-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 3.2rem;
        padding: 0.18rem 0.62rem;
        border-radius: 999px;
        background: #DBEAFE;
        color: #155EEF !important;
        font-weight: 850;
        font-size: 0.86rem;
    }

    .njc-table-wrap {
        background: #FFFFFF;
        border: 1px solid #D8E0EA;
        border-radius: 14px;
        overflow-x: auto;
        box-shadow: 0 10px 28px rgba(23, 50, 77, 0.06);
        margin-bottom: 0.85rem;
    }

    .njc-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.94rem;
        color: #111827;
    }

    .njc-table thead th {
        background: #EEF4FB;
        color: #111827;
        font-weight: 800;
        text-align: left;
        padding: 0.72rem 0.8rem;
        border-bottom: 1px solid #D8E0EA;
        white-space: nowrap;
    }

    .njc-table tbody td {
        background: #FFFFFF;
        color: #111827;
        padding: 0.68rem 0.8rem;
        border-bottom: 1px solid #E6ECF3;
        white-space: nowrap;
    }

    .njc-table tbody tr:nth-child(even) td {
        background: #F8FAFD;
    }

    .njc-table tbody tr:hover td {
        background: #EAF6FB;
    }
    </style>
""", unsafe_allow_html=True)

def render_light_table(df):
    table_html = df.to_html(index=False, classes="njc-table", border=0, escape=False)
    st.markdown(f'<div class="njc-table-wrap">{table_html}</div>', unsafe_allow_html=True)

def render_page_header(icon, title, subtitle):
    st.markdown(f"""
        <div class="njc-app-header">
            <div class="njc-header-icon">{icon}</div>
            <div>
                <div class="njc-header-title">{title}</div>
                <div class="njc-header-subtitle">{subtitle}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_morning_editor(rows, key_prefix):
    done_count = sum(1 for row in rows if row.get("完成"))
    total_count = len(rows) if rows else 1
    progress_pct = int(done_count / total_count * 100)

    st.markdown('<div class="njc-edit-head">一、早班日常工作自查</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="njc-progress-line">
            <div style="font-weight:700;color:#0B1F3A;">完成进度</div>
            <div class="njc-progress-track">
                <div class="njc-progress-fill" style="width:{progress_pct}%"></div>
            </div>
            <div class="njc-progress-count">{done_count}/{total_count}</div>
        </div>
    """, unsafe_allow_html=True)
    header_cols = st.columns([3.2, 1.2, 1.6])
    header_cols[0].markdown("**工作内容**")
    header_cols[1].markdown("**完成**")
    header_cols[2].markdown("**责任人**")

    edited_rows = []
    for idx, row in enumerate(rows):
        st.markdown('<div class="njc-edit-row">', unsafe_allow_html=True)
        cols = st.columns([3.2, 1.2, 1.6])
        work = cols[0].text_input(
            f"工作内容 {idx + 1}",
            value=row.get("工作内容", ""),
            label_visibility="collapsed",
            key=f"{key_prefix}_work_{idx}"
        )
        done = cols[1].checkbox(
            f"完成 {idx + 1}",
            value=bool(row.get("完成", False)),
            label_visibility="collapsed",
            key=f"{key_prefix}_done_{idx}"
        )
        owner = cols[2].text_input(
            f"责任人 {idx + 1}",
            value=row.get("责任人", ""),
            label_visibility="collapsed",
            key=f"{key_prefix}_owner_{idx}"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        edited_rows.append({"工作内容": work, "完成": done, "责任人": owner})

    return edited_rows

def render_text_grid_editor(rows, columns, key_prefix, title, extra_blank_rows=0):
    st.markdown(f'<div class="njc-edit-head">{title}</div>', unsafe_allow_html=True)
    header_cols = st.columns([1] * len(columns))
    for col, column_name in zip(header_cols, columns):
        col.markdown(f"**{column_name}**")

    editable_rows = list(rows)
    for _ in range(extra_blank_rows):
        editable_rows.append({column_name: "" for column_name in columns})

    edited_rows = []
    for idx, row in enumerate(editable_rows):
        st.markdown('<div class="njc-edit-row">', unsafe_allow_html=True)
        row_cols = st.columns([1] * len(columns))
        edited_row = {}
        for col, column_name in zip(row_cols, columns):
            current_value = str(row.get(column_name, ""))
            if column_name in ["清关行", "渠道"] and current_value:
                col.markdown(f'<span class="njc-badge">{current_value}</span>', unsafe_allow_html=True)
                edited_row[column_name] = current_value
            else:
                edited_row[column_name] = col.text_input(
                    f"{title} {column_name} {idx + 1}",
                    value=current_value,
                    label_visibility="collapsed",
                    key=f"{key_prefix}_{column_name}_{idx}"
                )
        st.markdown('</div>', unsafe_allow_html=True)
        if any(str(value).strip() for value in edited_row.values()):
            edited_rows.append(edited_row)

    return edited_rows

# ==========================================
# 登录验证
# ==========================================
LOGIN_PASSWORD = "20260617"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "login_user" not in st.session_state:
    st.session_state.login_user = ""

if not st.session_state.authenticated:
    st.markdown("""
        <style>
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background: linear-gradient(180deg, #101B35 0%, #17275B 100%) !important;
        }

        [data-testid="stHeader"] {
            display: none;
        }

        .block-container {
            max-width: 760px;
            padding-top: 4.2rem;
        }

        .njc-login-hero {
            text-align: center;
            margin-bottom: 2rem;
        }

        .njc-login-logo {
            width: 78px;
            height: 78px;
            border-radius: 18px;
            background: linear-gradient(135deg, #2F6FED, #2563EB);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #FFFFFF !important;
            font-size: 2rem;
            box-shadow: 0 18px 36px rgba(37, 99, 235, 0.28);
            margin-bottom: 1.35rem;
        }

        .njc-login-hero-title {
            color: #FFFFFF !important;
            font-size: 2.25rem;
            line-height: 1.15;
            font-weight: 900;
            margin-bottom: 0.45rem;
        }

        .njc-login-hero-subtitle {
            color: #B9C7DC !important;
            font-size: 1rem;
        }

        .njc-login-panel {
            max-width: 560px;
            margin: 0 auto;
            padding: 2.1rem 2.35rem 0.8rem;
            background: rgba(42, 58, 104, 0.72);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 20px 20px 0 0;
            box-shadow: 0 28px 64px rgba(0, 0, 0, 0.22);
            backdrop-filter: blur(10px);
        }

        .njc-login-title {
            color: #FFFFFF !important;
            font-size: 1.35rem;
            font-weight: 900;
        }

        .njc-login-subtitle {
            color: #B9C7DC !important;
        }

        div[data-testid="stForm"] {
            max-width: 560px;
            margin: 0 auto;
            padding: 0.2rem 2.35rem 2.4rem;
            background: rgba(42, 58, 104, 0.72);
            border: 1px solid rgba(255,255,255,0.12);
            border-top: 0;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 28px 64px rgba(0, 0, 0, 0.22);
            backdrop-filter: blur(10px);
        }

        div[data-testid="stForm"] label,
        div[data-testid="stForm"] p,
        div[data-testid="stForm"] span {
            color: #EAF1FF !important;
        }

        div[data-testid="stForm"] input,
        div[data-testid="stForm"] [data-baseweb="input"] {
            background: rgba(255,255,255,0.08) !important;
            border-color: rgba(255,255,255,0.22) !important;
            color: #FFFFFF !important;
            border-radius: 14px !important;
            height: 3.25rem;
        }

        div[data-testid="stForm"] input::placeholder {
            color: #97A7C2 !important;
        }

        div[data-testid="stFormSubmitButton"] button {
            height: 3.55rem;
            border-radius: 14px;
            background: linear-gradient(135deg, #2F6FED 0%, #0EA5B7 100%) !important;
            color: #FFFFFF !important;
            font-size: 1.05rem;
            box-shadow: 0 18px 34px rgba(37, 99, 235, 0.32);
            border: 0 !important;
        }

        .njc-login-footer {
            text-align: center;
            margin-top: 1.8rem;
            color: #6F82A5 !important;
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="njc-login-hero">
            <div class="njc-login-logo">▣</div>
            <div class="njc-login-hero-title">NJC 数据管理中心</div>
            <div class="njc-login-hero-subtitle">运营仓智能调度系统</div>
        </div>
        <div class="njc-login-panel">
            <div class="njc-login-title">登录系统</div>
            <div class="njc-login-subtitle">请输入用户名和统一密码后进入系统。</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        login_user = st.text_input("用户名", placeholder="请输入你的名字")
        login_password = st.text_input("密码", type="password", placeholder="请输入密码")
        login_submitted = st.form_submit_button("登录", type="primary")

    if login_submitted:
        if not login_user.strip():
            st.error("用户名不能为空，请输入你的名字。")
        elif login_password != LOGIN_PASSWORD:
            st.error("密码错误，请重新输入。")
        else:
            st.session_state.authenticated = True
            st.session_state.login_user = login_user.strip()
            st.rerun()

    st.markdown('<div class="njc-login-footer">NJC 运营仓 · 数字化管理平台</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 2. 侧边栏导航控制
# ==========================================
st.sidebar.markdown("""
    <div class="njc-side-brand">
        <div class="njc-side-logo">▣</div>
        <div>
            <div class="njc-side-title">NJC 数据管理中心</div>
            <div class="njc-side-sub">运营仓调度系统</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
    <div class="njc-user-chip">
        <div class="njc-user-avatar">{st.session_state.login_user[:1].upper()}</div>
        <div>
            <div class="njc-user-name">{st.session_state.login_user}</div>
            <div class="njc-side-sub">当班用户</div>
        </div>
    </div>
    <div class="njc-sidebar-label">功能模块</div>
""", unsafe_allow_html=True)

if st.sidebar.button("退出登录"):
    st.session_state.authenticated = False
    st.session_state.login_user = ""
    st.rerun()

page = st.sidebar.radio(
    "请选择要查看的功能：",
    ["📊 劳务排班预测", "📋 运营交接清单"],
    label_visibility="collapsed"
)

# ==========================================
# 功能一：劳务排班预测
# ==========================================
if page == "📊 劳务排班预测":
    render_page_header("↗", "劳务排班预测", "基于分段疲劳效率模型，输出稳妥的劳务到场人数建议")

    top_col1, top_col2, top_col3 = st.columns([1.05, 1.05, 1.05])
    with top_col1:
        with st.container(border=True):
            st.markdown('<div class="njc-card-title">⚙ 班次参数</div>', unsafe_allow_html=True)
            shift_hours = st.number_input("班次总长（小时）", value=10.00, key="shift_hours_main")
            rest_mins = st.number_input("吃饭休息（分钟）", value=45, key="rest_mins_main")
            handover_hours = st.number_input("早会交接（小时）", value=0.25, key="handover_hours_main")

    with top_col2:
        with st.container(border=True):
            st.markdown('<div class="njc-card-title">↯ 疲劳效率模型</div>', unsafe_allow_html=True)
            fatigue_1 = st.slider("前 4 小时效率", min_value=50, max_value=120, value=100, step=5, key="fatigue_1_main") / 100
            fatigue_2 = st.slider("第 5-7 小时效率", min_value=50, max_value=120, value=90, step=5, key="fatigue_2_main") / 100
            fatigue_3 = st.slider("第 8 小时后效率", min_value=50, max_value=120, value=80, step=5, key="fatigue_3_main") / 100

    net_hours = shift_hours - (rest_mins/60) - handover_hours

    def calculate_effective_hours(hours):
        if hours <= 0:
            return 0

        stage_1 = min(hours, 4) * fatigue_1
        stage_2 = max(min(hours - 4, 3), 0) * fatigue_2
        stage_3 = max(hours - 7, 0) * fatigue_3
        return stage_1 + stage_2 + stage_3

    effective_hours = calculate_effective_hours(net_hours)

    with top_col3:
        st.markdown(f"""
            <div class="njc-mini-kpi">
                <div class="njc-mini-kpi-label">单人净工时</div>
                <div class="njc-mini-kpi-value">{net_hours:.2f} h</div>
                <div class="njc-mini-kpi-sub">扣除休息与交接后</div>
            </div>
            <div class="njc-mini-kpi">
                <div class="njc-mini-kpi-label">疲劳折算有效工时</div>
                <div class="njc-mini-kpi-value">{effective_hours:.2f} h</div>
                <div class="njc-mini-kpi-sub">分段效率加权后</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(" ")
    with st.container(border=True):
        st.markdown('<div class="njc-card-title">⚙ 环节参数配置 <span style="margin-left:auto;color:#8AA0BD;font-size:0.86rem;font-weight:600;">修改货量或UPH，人数实时更新</span></div>', unsafe_allow_html=True)
        table_head = st.columns([2.5, 1.2, 1.2])
        table_head[0].markdown("**环节**")
        table_head[1].markdown("**预测货量（件）**")
        table_head[2].markdown("**标准 UPH**")

        row1 = st.columns([2.5, 1.2, 1.2])
        row1[0].markdown("**Unloading** 卸货入库")
        v1 = row1[1].number_input("Unloading 预测货量", value=1500, label_visibility="collapsed", key="v1_main")
        u1 = row1[2].number_input("Unloading 标准UPH", value=120, label_visibility="collapsed", key="u1_main")

        row2 = st.columns([2.5, 1.2, 1.2])
        row2[0].markdown("**Putaway** 库位上架")
        v2 = row2[1].number_input("Putaway 预测货量", value=1200, label_visibility="collapsed", key="v2_main")
        u2 = row2[2].number_input("Putaway 标准UPH", value=80, label_visibility="collapsed", key="u2_main")

        row3 = st.columns([2.5, 1.2, 1.2])
        row3[0].markdown("**Picking** 库区拣货")
        v3 = row3[1].number_input("Picking 预测货量", value=3000, label_visibility="collapsed", key="v3_main")
        u3 = row3[2].number_input("Picking 标准UPH", value=100, label_visibility="collapsed", key="u3_main")

        row4 = st.columns([2.5, 1.2, 1.2])
        row4[0].markdown("**Packing** 复核打包")
        v4 = row4[1].number_input("Packing 预测货量", value=2500, label_visibility="collapsed", key="v4_main")
        u4 = row4[2].number_input("Packing 标准UPH", value=80, label_visibility="collapsed", key="u4_main")

        row5 = st.columns([2.5, 1.2, 1.2])
        row5[0].markdown("**Labeling** 贴面单")
        v5 = row5[1].number_input("Labeling 预测货量", value=2500, label_visibility="collapsed", key="v5_main")
        u5 = row5[2].number_input("Labeling 标准UPH", value=150, label_visibility="collapsed", key="u5_main")

        row6 = st.columns([2.5, 1.2, 1.2])
        row6[0].markdown("**Dispatch** 称重装车")
        v6 = row6[1].number_input("Dispatch 预测货量", value=2800, label_visibility="collapsed", key="v6_main")
        u6 = row6[2].number_input("Dispatch 标准UPH", value=200, label_visibility="collapsed", key="u6_main")

    process_rows = [
        {"环节": "Unloading 卸货入库", "预测货量": v1, "标准UPH": u1},
        {"环节": "Putaway 库位上架", "预测货量": v2, "标准UPH": u2},
        {"环节": "Picking 库区拣货", "预测货量": v3, "标准UPH": u3},
        {"环节": "Packing 复核打包", "预测货量": v4, "标准UPH": u4},
        {"环节": "Labeling 贴面单", "预测货量": v5, "标准UPH": u5},
        {"环节": "Dispatch 称重装车", "预测货量": v6, "标准UPH": u6},
    ]

    if net_hours <= 0:
        st.error("班次总长必须大于吃饭休息和早会交接时间之和，请调整左侧班次参数。")
    elif any(row["标准UPH"] <= 0 for row in process_rows):
        st.error("所有环节的标准UPH都必须大于0，请检查输入。")
    else:
        total_standard_hours = sum(row["预测货量"] / row["标准UPH"] for row in process_rows)
        total_needed = math.ceil(total_standard_hours / effective_hours)

        detail_rows = []
        for row in process_rows:
            needed_hours = row["预测货量"] / row["标准UPH"]
            needed_people = math.ceil(needed_hours / effective_hours)
            detail_rows.append({
                "环节": row["环节"],
                "预测货量": row["预测货量"],
                "标准UPH": row["标准UPH"],
                "标准工时需求": round(needed_hours, 2),
                "建议人数": needed_people
            })

        st.markdown(f"""
            <div class="njc-kpi-blue">
                <div class="kpi-label">👥 建议到场人数</div>
                <div class="kpi-value">{total_needed}</div>
                <div class="kpi-sub">人 · 下午班次总计</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(" ")
        render_light_table(pd.DataFrame(detail_rows))
        st.caption("说明：总人数按全部环节总标准工时 / 单人疲劳折算有效工时向上取整；环节建议人数用于分工参考。")

# ==========================================
# 功能二：运营交接清单 (超美观全面看板版)
# ==========================================
elif page == "📋 运营交接清单":
    render_page_header("▣", "运营交接清单", "数字化工作流：填写交接单并实时同步至历史大盘")
    
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
        edited_morning = render_morning_editor(day_data["morning_tasks"], f"edit_morning_{date_key}")
        
        st.markdown("---")
        st.subheader("四、特殊事件及延误跟进")
        edited_events = render_text_grid_editor(
            day_data["special_events"],
            ["时间", "内容", "措施"],
            f"edit_events_{date_key}",
            "特殊事件及延误跟进",
            extra_blank_rows=2
        )

    with tab2:
        st.subheader("二、早班叫车与清关行提货记录")
        edited_customs = render_text_grid_editor(
            day_data["customs_data"],
            ["清关行", "状态", "数量", "时间"],
            f"edit_customs_{date_key}",
            "清关提货登记"
        )
        
    with tab3:
        st.subheader("三、渠道发货出库记录")
        edited_shipping = render_text_grid_editor(
            day_data["shipping_data"],
            ["渠道", "货量", "时间", "人"],
            f"edit_shipping_{date_key}",
            "渠道发货记录"
        )
        
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
        def parse_history_date(date_text):
            try:
                return datetime.date.fromisoformat(date_text)
            except (TypeError, ValueError):
                return None

        history_dates = sorted(
            [
                parsed_date
                for date in all_history.keys()
                for parsed_date in [parse_history_date(date)]
                if parsed_date
            ]
        )

        if not history_dates:
            st.warning("历史数据库中暂时没有可识别的日期记录。")
            filtered_history = {}
        else:
            filter_col1, filter_col2, filter_col3 = st.columns([1.2, 1.2, 1])
            with filter_col1:
                start_date = st.date_input("开始日期", value=min(history_dates), key="history_start_date")
            with filter_col2:
                end_date = st.date_input("结束日期", value=max(history_dates), key="history_end_date")

            if start_date > end_date:
                st.warning("开始日期不能晚于结束日期，请重新选择。")
                filtered_history = {}
            else:
                filtered_history = {
                    date: content
                    for date, content in all_history.items()
                    for parsed_date in [parse_history_date(date)]
                    if parsed_date and start_date <= parsed_date <= end_date
                }

            with filter_col3:
                st.metric("筛选日期数", len(filtered_history))

        # 提取提货（清关）流水
        customs_rows = []
        # 提取发货渠道流水
        shipping_rows = []
        
        for date, content in filtered_history.items():
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
        panel1, panel2 = st.columns(2)
        
        with panel1:
            st.markdown('<div class="njc-table-card-head">🚚 提货（清关行）流水总账</div>', unsafe_allow_html=True)
            if customs_rows:
                df_c_excel = pd.DataFrame(customs_rows)
                render_light_table(df_c_excel)
                # 提货下载
                csv_c = df_c_excel.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 导出提货历史 Excel", data=csv_c, file_name=f"NJC提货大盘_{datetime.date.today()}.csv", mime="text/csv", key="dl_c")
            else:
                st.info("💡 暂无提货流水明细")

        with panel2:
            st.markdown('<div class="njc-table-card-head">📦 发货（渠道出库）流水总账</div>', unsafe_allow_html=True)
            if shipping_rows:
                df_s_excel = pd.DataFrame(shipping_rows)
                render_light_table(df_s_excel)
                # 发货下载
                csv_s = df_s_excel.to_csv(index=False).encode('utf-8-sig')
                st.download_button("📥 导出发货历史 Excel", data=csv_s, file_name=f"NJC发货大盘_{datetime.date.today()}.csv", mime="text/csv", key="dl_s")
            else:
                st.info("💡 暂无发货渠道流水明细")
    else:
        st.info("💡 目前数据库空空如也，请在上方填写并点击保存，数据大盘将自动为您亮起！")
