# Steven Manurung
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from function_all import DataAnalyzer
sns.set(style='white')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Databases
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
df_combine = pd.read_csv("../databases/combine_data.csv")
df_combine.sort_values(by="order_approved_at", inplace=True)
df_combine.reset_index(inplace=True)

geolocation = pd.read_csv('../databases/geolocation_dataset.csv')

for col in datetime_cols:
    df_combine[col] = pd.to_datetime(df_combine[col])

min_date = df_combine["order_approved_at"].min()
max_date = df_combine["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("Steven Manurung")

    # Date Range
    start_date, end_date = st.date_input(
        label="Pilih jarak tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = df_combine[(df_combine["order_approved_at"] >= str(start_date)) & 
                 (df_combine["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)

daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

# Title
st.header("E-Commerce Dashboard")

# Order Items
st.subheader("Item Paling banyak diminati")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(45, 25))  # Create a single subplot

colors = ["#068DA9"]

sns.barplot(
    x="product_count",
    y="product_category_name_english",
    data=sum_order_items_df.head(3),
    palette=colors,
    ax=ax,
)
ax.set_ylabel(None)
ax.set_xlabel("Jumlah penjual", fontsize=30)
ax.set_title("Produk paling banyak terjual", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Review Score
st.subheader("Penilian pelanggan kepada pelayanan")
col1,col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Rata-rata skor penialian: **{avg_review_score}**")

with col2:
    most_common_review_score = review_score.value_counts().index[0]

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=review_score.index, 
            y=review_score.values, 
            order=review_score.index,
            palette=["#068DA9" if score == common_score else "#D3D3D3" for score in review_score.index]
            )

plt.title("Penilaian customer tentang pelayanan", fontsize=15)
plt.xlabel("Penilaian")
plt.ylabel("Jumlah")
plt.xticks(fontsize=12)
st.pyplot(fig)

# Customer Demographic
st.subheader("Pelanggan dalam negara")
tab1, tab2 = st.tabs(["State", "Order Status"])

with tab1:
    most_common_state = state.customer_state.value_counts().index[0]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state.customer_state.value_counts().index,
                y=state.customer_count.values, 
                data=state,
                palette=["#068DA9" if score == most_common_state else "#D3D3D3" for score in state.customer_state.value_counts().index]
                    )

    plt.title("Jumlah customer dalam negara", fontsize=15)
    plt.xlabel("Negara")
    plt.ylabel("Jumlah customer")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

with tab2:
    common_status_ = order_status.value_counts().index[0]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=order_status.index,
                y=order_status.values,
                order=order_status.index,
                palette=["#068DA9" if score == common_status else "#D3D3D3" for score in order_status.index]
                )
    
    plt.title("Status Order", fontsize=15)
    plt.xlabel("Status")
    plt.ylabel("Jumlah")
    plt.xticks(fontsize=12)
    st.pyplot(fig)