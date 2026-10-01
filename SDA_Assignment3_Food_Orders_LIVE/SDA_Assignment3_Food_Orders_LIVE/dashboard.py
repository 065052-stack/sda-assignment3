"""Live food-orders Streamlit dashboard."""
import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_autorefresh import st_autorefresh

DATA_FILE = Path("live_orders.json")

st.set_page_config(page_title="Live Food Orders Dashboard", page_icon="🍔", layout="wide")
st_autorefresh(interval=2000, key="live_refresh")

st.title("🍔 Live Food Orders Dashboard")
st.caption("Simulated streaming demo • A new order is generated every 2 seconds")

if not DATA_FILE.exists():
    st.warning("Start live_producer.py first.")
    st.stop()

try:
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))
except (json.JSONDecodeError, OSError):
    st.warning("Live data is being updated. Please wait for the next refresh.")
    st.stop()

df = pd.DataFrame(records)
if df.empty:
    st.warning("No orders available yet.")
    st.stop()

df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["event_timestamp"] = pd.to_datetime(
    df.get("event_timestamp", pd.Series([None] * len(df))),
    errors="coerce", utc=True
)

st.sidebar.header("Filters")
status_values = sorted(df["order_status"].dropna().unique())
payment_values = sorted(df["payment_method"].dropna().unique())
restaurant_values = sorted(df["restaurant_id"].dropna().unique())

selected_status = st.sidebar.multiselect("Order Status", status_values, default=status_values)
selected_payment = st.sidebar.multiselect("Payment Method", payment_values, default=payment_values)
selected_restaurant = st.sidebar.multiselect("Restaurant", restaurant_values, default=restaurant_values)

filtered = df[
    df["order_status"].isin(selected_status)
    & df["payment_method"].isin(selected_payment)
    & df["restaurant_id"].isin(selected_restaurant)
].copy()

if filtered.empty:
    st.info("No orders match the selected filters.")
    st.stop()

orders = filtered["order_id"].nunique()
revenue = float(filtered["amount"].sum())
items = int(filtered["quantity"].sum())
aov = revenue / orders if orders else 0.0
unique_customers = filtered["customer_id"].nunique()
active_orders = filtered.loc[filtered["order_status"] != "delivered", "order_id"].nunique()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Live Orders", f"{orders:,}")
k2.metric("Revenue", f"₹{revenue:,.0f}")
k3.metric("Items Sold", f"{items:,}")
k4.metric("Average Order Value", f"₹{aov:,.0f}")

k5, k6 = st.columns(2)
k5.metric("Unique Customers", f"{unique_customers:,}")
k6.metric("Active Orders", f"{active_orders:,}")

st.divider()

c1, c2 = st.columns(2)

status_df = (
    filtered.groupby("order_status", as_index=False)
    .agg(orders=("order_id", "nunique"))
    .sort_values("orders", ascending=False)
)
c1.plotly_chart(
    px.bar(status_df, x="order_status", y="orders", text="orders", title="Orders by Status"),
    width="stretch",
)

restaurant_df = (
    filtered.groupby("restaurant_id", as_index=False)
    .agg(revenue=("amount", "sum"))
    .sort_values("revenue", ascending=False)
)
c2.plotly_chart(
    px.bar(restaurant_df, x="restaurant_id", y="revenue", text_auto=True, title="Revenue by Restaurant"),
    width="stretch",
)

c3, c4 = st.columns(2)

payment_df = (
    filtered.groupby("payment_method", as_index=False)
    .agg(orders=("order_id", "nunique"))
    .sort_values("orders", ascending=False)
)
c3.plotly_chart(
    px.pie(payment_df, names="payment_method", values="orders", hole=0.45, title="Payment Method Mix"),
    width="stretch",
)

timeline = filtered.dropna(subset=["event_timestamp"]).copy()
if not timeline.empty:
    timeline = (
        timeline.groupby("event_timestamp", as_index=False)
        .agg(revenue=("amount", "sum"))
        .sort_values("event_timestamp")
    )
    c4.plotly_chart(
        px.line(timeline, x="event_timestamp", y="revenue", markers=True, title="Revenue Over Time"),
        width="stretch",
    )

c5, c6 = st.columns(2)

source_df = (
    filtered.groupby("source", as_index=False)
    .agg(orders=("order_id", "nunique"))
    .sort_values("orders", ascending=False)
)
c5.plotly_chart(
    px.bar(source_df, x="source", y="orders", text="orders", title="Orders by Source"),
    width="stretch",
)

items_restaurant_df = (
    filtered.groupby("restaurant_id", as_index=False)
    .agg(items=("quantity", "sum"))
    .sort_values("items", ascending=False)
)
c6.plotly_chart(
    px.bar(items_restaurant_df, x="restaurant_id", y="items", text="items", title="Items Sold by Restaurant"),
    width="stretch",
)

st.subheader("Latest Live Events")
latest_columns = [
    "order_id", "restaurant_id", "quantity", "amount",
    "payment_method", "order_status", "source", "event_timestamp"
]
st.dataframe(
    filtered.sort_values("event_timestamp", ascending=False)[latest_columns].head(20),
    width="stretch", hide_index=True,
)
st.success("Live refresh is active. Keep live_producer.py running.")
