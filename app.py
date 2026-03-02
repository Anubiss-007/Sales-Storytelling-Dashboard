import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="🏬 Sales Storytelling Dashboard", layout="wide")

conn = st.connection("sql")
@st.cache_data
def load_data_from_sql():
    query = "SELECT * FROM sales_table"
    df = conn.query(query, ttl="10m") #เก็บ Cache ไว้ 10 นาที

    df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', dayfirst=True)
    df['Month'] = df['order_date'].dt.to_period('M').astype('str')

    df['sales'] = df['sales'].astype(str).str.replace(',', '', regex=False).str.replace('$', '', regex=False)
    df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    
    return df

df = load_data_from_sql()

# @st.cache_data
# def load_data():
    
#     df = pd.read_csv("Super_StoreOrders.csv", encoding="utf-8")
#     # df = pd.read_csv("/Users/Anubiss/Superstore/dataset/Super_StoreOrders.csv", encoding="utf-8")

#     df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', dayfirst=True)  #แปลงวันที่
#     df['Month'] = df['order_date'].dt.to_period('M').astype('str')
    

#     df['sales'] = df['sales'].astype(str).str.replace(',', '', regex=False) # ลบลูกน้ำ ,$, 
#     df['sales'] = df['sales'].str.replace('$', '', regex=False)
#     df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
    
#     return df

# df = load_data()

st.sidebar.header("Filter Data")
selected_category = st.sidebar.multiselect("Select Category",
                             options=df['category'].unique(),
                             default=df['category'].unique()) #ค่าเริ่มต้น เลือกทุกหมวดหมู่

filter_df = df[df['category'].isin(selected_category)] #เลือกเฉพาะใน category เท่านั้น

st.title("📊 E-Commerce Performance Dashboard")
st.markdown("A user-centric dashboard designed to highlight key sales metrics and trends.")

# KPI Cards
total_sales = filter_df['sales'].sum()
total_profit = filter_df['profit'].sum()
avg_sales = filter_df['sales'].mean() 

col1, col2, col3 = st.columns(3) # แบ่งเป็นขนาด 3 columns

with col1:
    st.metric(label="Total Sales", value=f"${total_sales/1_000_000:.2f}M")
with col2:
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}") 
with col3:
    st.metric(label="Average Sales", value=f"${avg_sales:,.2f}") 

st.markdown("<br>", unsafe_allow_html=True)


col_chart1, col_chart2 = st.columns(2) # แบ่งเป็นขนาด 2 columns

with col_chart1:
    st.subheader("Monthly Sales Trend")
    monthly_sales = filter_df.groupby('Month')['sales'].sum().reset_index()
    # เปลี่ยนชื่อตัวแปรเป็น fig_line ให้สอดคล้องกับ px.line
    fig_line = px.line(monthly_sales, x='Month', y='sales', markers=True) 
    # แก้ไขคำสั่ง pyplot_chart เป็น plotly_chart
    st.plotly_chart(fig_line, use_container_width=True) 

with col_chart2:
    st.subheader("Sales by Category")
    cat_sales = filter_df.groupby('category')['sales'].sum().reset_index()
    fig_bar = px.bar(cat_sales, x='category', y='sales', color='category')
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.subheader("🗓️Monthly Profit Trend")
    monthly_profit = filter_df.groupby('Month')['profit'].sum().reset_index()
    fig_line_profit = px.line(monthly_profit, x='Month', y='profit', 
                              markers=True,color_discrete_sequence=['#228B22']) 
    st.plotly_chart(fig_line_profit, use_container_width=True)

with col_chart4:
    st.subheader("📊Profit by Category")
    cat_profit = filter_df.groupby('category')['profit'].sum().reset_index()
    fig_bar_profit = px.bar(cat_profit, x='category', y='profit', 
                            color='category',title="Profit Contribution by Category🛍️")
    st.plotly_chart(fig_bar_profit, use_container_width=True)

st.markdown("---")
with st.expander("📥 View Raw Data"):
    st.dataframe(filter_df.sort_values(by='order_date', ascending=False))