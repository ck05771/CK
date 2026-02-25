import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

# ── Global CSS: Clean & Simple ────────────────────────────────────────────────
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* Root variables */
:root {
    --bg: #F7F7F5;
    --surface: #FFFFFF;
    --border: #E8E8E4;
    --text-primary: #1A1A18;
    --text-secondary: #6B6B65;
    --accent: #2563EB;
    --accent-light: #EEF3FF;
    --success: #16A34A;
    --warning: #D97706;
    --danger: #DC2626;
    --radius: 10px;
}

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

.stApp {
    background: var(--bg);
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 3rem 3rem; max-width: 1200px; }

/* Title area */
h1 {
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
    color: var(--text-primary) !important;
    margin-bottom: 0.15rem !important;
}

h2, h3 {
    font-weight: 500 !important;
    letter-spacing: -0.01em;
    color: var(--text-primary) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    padding: 0.4rem 0;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem !important;
}

[data-testid="stMetricLabel"] { font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.06em; }
[data-testid="stMetricValue"] { font-size: 1.6rem; font-weight: 600; color: var(--text-primary); }

/* Tables */
[data-testid="stTable"] table, .stDataFrame table {
    font-size: 0.82rem;
    border-collapse: collapse;
    width: 100%;
}

[data-testid="stTable"] thead th, .stDataFrame thead th {
    background: var(--bg) !important;
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.6rem 0.8rem !important;
    border-bottom: 1px solid var(--border) !important;
}

[data-testid="stTable"] tbody td, .stDataFrame tbody td {
    padding: 0.55rem 0.8rem !important;
    border-bottom: 1px solid var(--border) !important;
    color: var(--text-primary);
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
}

[data-testid="stTable"] tbody tr:hover, .stDataFrame tbody tr:hover {
    background: var(--accent-light) !important;
}

/* Buttons */
.stButton > button {
    background: var(--text-primary);
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 0.45rem 1.1rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    font-weight: 500;
    cursor: pointer;
    transition: opacity 0.15s;
}
.stButton > button:hover { opacity: 0.8; }

/* Alerts */
.stSuccess, .stInfo, .stWarning, .stError {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    font-size: 0.84rem !important;
}
.stSuccess { border-left: 3px solid var(--success) !important; background: #F0FDF4 !important; }
.stInfo    { border-left: 3px solid var(--accent) !important;  background: var(--accent-light) !important; }
.stWarning { border-left: 3px solid var(--warning) !important; background: #FFFBEB !important; }
.stError   { border-left: 3px solid var(--danger) !important;  background: #FEF2F2 !important; }

/* Expander */
details { border: 1px solid var(--border) !important; border-radius: var(--radius) !important; padding: 0.25rem !important; }
summary { font-size: 0.85rem; font-weight: 500; color: var(--text-primary); }

/* Divider */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* Forms */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-size: 0.84rem !important;
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# ── Matplotlib style ──────────────────────────────────────────────────────────
PALETTE = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DM Sans", "Helvetica Neue", "Arial"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "axes.grid": True,
    "grid.color": "#E8E8E4",
    "grid.linewidth": 0.8,
    "axes.facecolor": "#FFFFFF",
    "figure.facecolor": "#FFFFFF",
    "axes.labelcolor": "#6B6B65",
    "xtick.color": "#6B6B65",
    "ytick.color": "#6B6B65",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.titlesize": 11,
    "axes.titleweight": "600",
    "axes.titlepad": 14,
})

# ── Data ──────────────────────────────────────────────────────────────────────
def load_data():
    file_path = 'sales_data.csv'
    if not os.path.exists(file_path):
        initial_data = pd.DataFrame({
            "Date": ["2023-01-15", "2023-01-20"],
            "Product_ID": ["P001", "P002"],
            "Product Name": ["Laptop", "Mouse"],
            "Category": ["IT", "IT"],
            "Quantity": [10, 50],
            "Unit Price": [25000, 500],
            "Region": ["North", "South"]
        })
        initial_data.to_csv(file_path, index=False)
    return pd.read_csv(file_path)

df = load_data()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Sales Analytics Dashboard")
st.markdown('<p style="color:#6B6B65;font-size:0.88rem;margin-top:-0.5rem;">โครงการทดสอบสมรรถนะรายปี · อาชีพนักวิเคราะห์ข้อมูล</p>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown('<p style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#6B6B65;font-weight:500;margin-bottom:0.5rem;">เมนูหลัก</p>', unsafe_allow_html=True)
menu = st.sidebar.radio("", [
    "0. จัดการข้อมูล (เพิ่ม/ลบ)",
    "1. ตรวจสอบคุณภาพข้อมูล",
    "2. ทำความสะอาดข้อมูล",
    "3. วิเคราะห์ข้อมูล",
    "4. ความปลอดภัยข้อมูล",
    "5. การแสดงผลข้อมูล (Visualization)"
], label_visibility="collapsed")

# ── Section 0: Manage Data ────────────────────────────────────────────────────
if menu == "0. จัดการข้อมูล (เพิ่ม/ลบ)":
    st.subheader("จัดการฐานข้อมูล")

    with st.expander("➕  เพิ่มข้อมูลยอดขายใหม่"):
        with st.form("add_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            new_date  = c1.date_input("วันที่ขาย")
            new_id    = c2.text_input("รหัสสินค้า")
            new_name  = c3.text_input("ชื่อสินค้า")
            new_cat   = c1.selectbox("หมวดหมู่", ["IT", "Furniture", "Electronics"])
            new_qty   = c2.number_input("จำนวน", min_value=1)
            new_price = c3.number_input("ราคาต่อหน่วย", min_value=1)
            new_reg   = c1.selectbox("ภูมิภาค", ["North", "South", "Central", "East", "West"])
            if st.form_submit_button("บันทึกข้อมูล"):
                new_row = pd.DataFrame([[str(new_date), new_id, new_name, new_cat, new_qty, new_price, new_reg]],
                                       columns=df.columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv('sales_data.csv', index=False)
                st.success("บันทึกข้อมูลสำเร็จ!")
                st.rerun()

    with st.expander("🗑️  ลบข้อมูลที่ไม่ต้องการ"):
        st.dataframe(df, use_container_width=True)
        delete_idx = st.number_input("ระบุเลขลำดับที่ต้องการลบ", min_value=0, max_value=len(df)-1, step=1)
        if st.button("ยืนยันการลบ"):
            df = df.drop(df.index[delete_idx])
            df.to_csv('sales_data.csv', index=False)
            st.warning("ลบข้อมูลเรียบร้อยแล้ว")
            st.rerun()

# ── Section 1: Quality Check ──────────────────────────────────────────────────
elif menu == "1. ตรวจสอบคุณภาพข้อมูล":
    st.subheader("ตรวจสอบคุณภาพข้อมูล")

    if st.button("เริ่มตรวจสอบ"):
        # Missing values
        st.markdown("**Missing Values**")
        null_rows = df[df.isnull().any(axis=1)]
        if not null_rows.empty:
            st.error(f"พบข้อมูลไม่สมบูรณ์ {len(null_rows)} แถว")
            st.dataframe(null_rows, use_container_width=True)
        else:
            st.success("ข้อมูลทุกแถวครบถ้วน")

        st.divider()

        # Duplicates
        st.markdown("**ข้อมูลซ้ำ (Duplicates)**")
        dup_rows = df[df.duplicated(keep=False)]
        if not dup_rows.empty:
            st.warning(f"พบข้อมูลซ้ำ {len(df[df.duplicated()])} รายการ")
            st.dataframe(dup_rows.sort_values(by=list(df.columns)), use_container_width=True)
        else:
            st.success("ไม่พบข้อมูลซ้ำ")

        st.divider()

        # Data types
        st.markdown("**ชนิดข้อมูลรายช่อง**")
        def check_type(v): return type(v).__name__
        st.dataframe(df.applymap(check_type), use_container_width=True)
        st.info("หากคอลัมน์ตัวเลขแสดงผลเป็น `str` แสดงว่าแถวนั้นมีชนิดข้อมูลผิดพลาด")

# ── Section 2: Data Cleaning ──────────────────────────────────────────────────
elif menu == "2. ทำความสะอาดข้อมูล":
    st.subheader("ทำความสะอาดข้อมูล")
    st.info("เกณฑ์: ลบซ้ำ · กรองค่าติดลบ · แปลงรูปแบบวันที่")

    if st.button("เริ่มทำความสะอาด"):
        df_before = df.copy()

        dup_rows          = df_before[df_before.duplicated()]
        df_clean          = df_before.drop_duplicates()
        wrong_fmt         = df_clean[(df_clean['Quantity'] <= 0) | (df_clean['Unit Price'] <= 0)]
        df_clean          = df_clean[(df_clean['Quantity'] > 0) & (df_clean['Unit Price'] > 0)]
        invalid_date_rows = df_clean[pd.to_datetime(df_clean['Date'], errors='coerce').isna()]
        df_clean['Date']  = pd.to_datetime(df_clean['Date'], errors='coerce')
        df_clean          = df_clean.dropna(subset=['Date'])

        st.session_state['df_clean'] = df_clean
        st.success("ทำความสะอาดเสร็จสิ้น")

        c1, c2, c3 = st.columns(3)
        c1.metric("ข้อมูลซ้ำที่ลบ",         f"{len(dup_rows)} แถว")
        c2.metric("ข้อมูลผิดรูปแบบที่ลบ",   f"{len(wrong_fmt)} แถว")
        c3.metric("วันที่ผิดพลาดที่ลบ",      f"{len(invalid_date_rows)} แถว")

        with st.expander("รายละเอียดรายการที่ถูกลบ"):
            if not dup_rows.empty:
                st.markdown("**ข้อมูลซ้ำ:**"); st.dataframe(dup_rows, use_container_width=True)
            if not wrong_fmt.empty:
                st.markdown("**จำนวน/ราคาติดลบ:**"); st.dataframe(wrong_fmt, use_container_width=True)
            if not invalid_date_rows.empty:
                st.markdown("**วันที่ผิดรูปแบบ:**"); st.dataframe(invalid_date_rows, use_container_width=True)

        st.markdown("**ข้อมูลที่พร้อมใช้งาน**")
        st.dataframe(df_clean, use_container_width=True)

# ── Section 3: Analysis ───────────────────────────────────────────────────────
elif menu == "3. วิเคราะห์ข้อมูล":
    st.subheader("วิเคราะห์ข้อมูลเพื่อหาข้อสรุปเชิงธุรกิจ")

    if 'df_clean' in st.session_state:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = data['Quantity'] * data['Unit Price']

        st.markdown("**ยอดขายรวมต่อเดือน**")
        data['Month']    = data['Date'].dt.to_period('M').astype(str)
        monthly_sales    = data.groupby('Month')['Total_Sales'].sum().reset_index()
        st.table(monthly_sales)

        st.divider()

        st.markdown("**สินค้าขายดีที่สุด 5 อันดับ**")
        top_products = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(5).reset_index()
        st.table(top_products)

        st.divider()

        st.markdown("**ยอดขายตามภูมิภาค**")
        region_sales = data.groupby('Region')['Total_Sales'].sum().reset_index()
        st.table(region_sales)

        st.divider()

        best_region  = region_sales.loc[region_sales['Total_Sales'].idxmax(), 'Region']
        best_product = top_products.loc[0, 'Product Name']
        st.success(f"""**ข้อเสนอแนะเชิงธุรกิจ:**  
- ควรทำโปรโมชั่นพ่วงสำหรับ **{best_product}** (สินค้าขายดีอันดับ 1)  
- ทุ่มงบโฆษณาในภูมิภาค **{best_region}** (ยอดซื้อสูงสุด)  
- เตรียมสต็อกล่วงหน้า 1 เดือนตามแนวโน้มรายเดือน""")
    else:
        st.warning("กรุณาดำเนินการ 'ทำความสะอาดข้อมูล' ในขั้นตอนที่ 2 ก่อน")

# ── Section 4: Security ───────────────────────────────────────────────────────
elif menu == "4. ความปลอดภัยข้อมูล":
    st.subheader("ออกแบบความปลอดภัยข้อมูล")

    st.markdown("**การกำหนดสิทธิ์ (RBAC)**")
    st.table(pd.DataFrame([
        {"บทบาท": "Admin (ไอที)",          "สิทธิ์": "ดู / เพิ่ม / แก้ไข / ลบ / จัดการผู้ใช้",  "ระดับ": "สูงสุด"},
        {"บทบาท": "Analyst (นักวิเคราะห์)", "สิทธิ์": "ดูข้อมูล ทำความสะอาด วิเคราะห์",          "ระดับ": "ปานกลาง"},
        {"บทบาท": "Viewer (ผู้บริหาร)",    "สิทธิ์": "ดูรายงานสรุปและ Dashboard เท่านั้น",       "ระดับ": "เริ่มต้น"},
    ]))

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.info("**การป้องกันเชิงเทคนิค**\n\n- **Encryption** เข้ารหัสไฟล์ขณะจัดเก็บ\n- **MFA** ยืนยันตัวตน 2 ชั้น\n- **Audit Logs** บันทึกทุกกิจกรรม")
    with col2:
        st.info("**การป้องกันเชิงบริหาร**\n\n- **NDA** สัญญาไม่เปิดเผยข้อมูล\n- **Privacy Policy** สอดคล้อง PDPA\n- **Training** อบรม Cyber Security")

    st.success("แนวทางนี้สอดคล้องกับมาตรฐานความปลอดภัยข้อมูลระดับ 4")

# ── Section 5: Visualization ──────────────────────────────────────────────────
elif menu == "5. การแสดงผลข้อมูล (Visualization)":
    st.subheader("การแสดงผลข้อมูล")

    if 'df_clean' in st.session_state:
        data = st.session_state['df_clean'].copy()
        data['Total_Sales'] = data['Quantity'] * data['Unit Price']
        data['Month']       = data['Date'].dt.to_period('M').astype(str)

        # ── Line chart ────────────────────────────────────────────────────────
        st.markdown("**แนวโน้มยอดขายรายเดือน**")
        monthly_trend = data.groupby('Month')['Total_Sales'].sum().reset_index()

        fig1, ax1 = plt.subplots(figsize=(10, 3.8))
        ax1.plot(monthly_trend['Month'], monthly_trend['Total_Sales'],
                 color=PALETTE[0], linewidth=2.2, marker='o',
                 markersize=6, markerfacecolor='white', markeredgewidth=2.2)
        ax1.fill_between(monthly_trend['Month'], monthly_trend['Total_Sales'],
                         alpha=0.07, color=PALETTE[0])
        ax1.set_title("Monthly Sales Trend", loc='left')
        ax1.set_ylabel("Sales (Baht)", labelpad=10)
        ax1.set_xlabel("")
        ax1.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        plt.tight_layout()
        st.pyplot(fig1, use_container_width=True)

        st.divider()

        # ── Bar chart ─────────────────────────────────────────────────────────
        st.markdown("**ยอดขายตามภูมิภาค**")
        region_comp = data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).reset_index()

        fig2, ax2 = plt.subplots(figsize=(8, 3.8))
        bars = ax2.bar(region_comp['Region'], region_comp['Total_Sales'],
                       color=PALETTE[0], width=0.5, zorder=3)
        # Highlight top bar
        bars[0].set_color(PALETTE[1])
        ax2.set_title("Sales by Region", loc='left')
        ax2.set_ylabel("Total Sales (Baht)", labelpad=10)
        ax2.set_xlabel("")
        ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
        for bar in bars:
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
                     f"{bar.get_height():,.0f}", ha='center', va='bottom',
                     fontsize=8.5, color='#6B6B65')
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)

        st.divider()

        best_region  = region_comp.loc[0, 'Region']
        best_product = data.groupby('Product Name')['Quantity'].sum().idxmax()
        st.success(f"""**Executive Summary**  
- แนวโน้มรายเดือน: วิเคราะห์จากกราฟเส้นด้านบน  
- ภูมิภาคหลัก: **{best_region}** มียอดขายสูงสุด (แท่งสีเขียว)  
- แผนงานถัดไป: จัดโปรโมชั่น **{best_product}** ในช่วง Peak Month""")
    else:
        st.warning("กรุณาดำเนินการ 'ทำความสะอาดข้อมูล' ในขั้นตอนที่ 2 ก่อน")