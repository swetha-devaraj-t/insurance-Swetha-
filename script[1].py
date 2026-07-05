# Create a proper Python file content for the user to download manually.
from pathlib import Path
out = Path('output')
out.mkdir(exist_ok=True)
code = '''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")

st.markdown("""
<style>
.main {background-color: #0b1220;}
.block-container {padding-top: 1rem; padding-bottom: 1rem;}
.card {
    background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
    padding: 18px 16px;
    border-radius: 16px;
    border: 1px solid #233044;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.card h4 {
    margin: 0;
    color: #94a3b8;
    font-size: 0.82rem;
    font-weight: 600;
}
.card h2 {
    margin: 6px 0 2px 0;
    color: #e2e8f0;
    font-size: 1.8rem;
    font-weight: 800;
}
.card p {
    margin: 0;
    color: #38bdf8;
    font-size: 0.8rem;
}
.section-title {
    color: #e2e8f0;
    font-weight: 700;
    margin-top: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

st.title("E-Commerce Customer Analytics Dashboard")
st.caption("A Streamlit dashboard built from the capstone presentation metrics.")

# Core metrics from the presentation
sessions = 25000
unique_customers = 8442
revenue_m = 10.12
conversion_rate = 22.5
cart_abandonment = 42.0
orders = 5616
aov = 1801
best_accuracy = 92.2
best_f1 = 79.0

# Data tables
weekly_revenue = pd.DataFrame({
    "Week": ["W1", "W2", "W3", "W4", "W5", "W6"],
    "Revenue": [1.3, 1.5, 1.4, 1.7, 1.9, 1.8]
})

category_revenue = pd.DataFrame({
    "Category": ["C2", "C6", "C5", "C3", "C7", "C0", "C1", "C4"],
    "Revenue": [2.037577, 1.930885, 1.729167, 1.293650, 1.089618, 0.880077, 0.702789, 0.452407]
})

device_data = pd.DataFrame({
    "Device": ["Mobile", "Desktop", "Tablet"],
    "Sessions": [12600, 9887, 2513]
})

channel_data = pd.DataFrame({
    "Channel": ["Direct", "Organic", "Paid Ads", "Email", "Social", "Referral"],
    "Purchase Rate": [23.6, 22.7, 22.6, 22.1, 22.0, 21.7]
})

payment_data = pd.DataFrame({
    "Method": ["A", "B", "C", "D", "E", "F"],
    "Share": [980, 949, 940, 939, 913, 895]
})

segment_data = pd.DataFrame({
    "Segment": ["High Value", "Frequent", "Discount", "Window"],
    "Customers": [35, 28, 22, 15]
})

model_data = pd.DataFrame({
    "Model": ["KNN", "Decision Tree", "Random Forest", "Gradient Boosting"],
    "Accuracy": [85.4, 91.8, 92.2, 92.1]
})

# Sidebar filters
st.sidebar.header("Filters")
st.sidebar.date_input("Date range", value=None)
st.sidebar.multiselect("Device", device_data["Device"].tolist(), default=device_data["Device"].tolist())
st.sidebar.multiselect("Channel", channel_data["Channel"].tolist(), default=channel_data["Channel"].tolist())
st.sidebar.multiselect("Category", category_revenue["Category"].tolist(), default=category_revenue["Category"].tolist())

# KPI cards
kpi_cols = st.columns(6)
kpis = [
    ("Revenue", f"{revenue_m:.2f}M", "Total revenue"),
    ("Conversion", f"{conversion_rate:.1f}%", "Purchase rate"),
    ("Orders", f"{orders:,}", "Purchased sessions"),
    ("AOV", f"{aov:,}", "Avg order value"),
    ("Abandonment", f"{cart_abandonment:.1f}%", "Lost carts"),
    ("Customers", f"{unique_customers:,}", "Unique customers"),
]
for col, (title, value, note) in zip(kpi_cols, kpis):
    col.markdown(f"""
    <div class="card">
        <h4>{title}</h4>
        <h2>{value}</h2>
        <p>{note}</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Charts row 1
row1_left, row1_right = st.columns([1.2, 1])
with row1_left:
    fig = px.line(weekly_revenue, x="Week", y="Revenue", markers=True, title="Revenue Trend")
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with row1_right:
    funnel = go.Figure(go.Funnel(y=["Sessions", "Added to Cart", "Purchased"], x=[25000, 16117, 5616]))
    funnel.update_layout(title="Purchase Funnel", height=360, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(funnel, use_container_width=True)

# Charts row 2
row2_left, row2_middle, row2_right = st.columns(3)
with row2_left:
    fig = px.bar(category_revenue, x="Category", y="Revenue", title="Revenue by Category", color="Revenue", color_continuous_scale="Blues")
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=50, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with row2_middle:
    fig = px.pie(device_data, names="Device", values="Sessions", title="Device Mix")
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with row2_right:
    fig = px.bar(channel_data, x="Channel", y="Purchase Rate", title="Channel Purchase Rate", color="Purchase Rate", color_continuous_scale="Viridis")
    fig.update_layout(height=340, margin=dict(l=10, r=10, t=50, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# Charts row 3
row3_left, row3_right = st.columns(2)
with row3_left:
    fig = px.bar(payment_data, x="Method", y="Share", title="Payment Methods")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

with row3_right:
    fig = px.bar(segment_data, x="Segment", y="Customers", title="Customer Segments", color="Customers", color_continuous_scale="Tealgrn")
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=50, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# Predictive section
st.subheader("Predictive Model Benchmark")
st.dataframe(model_data, use_container_width=True, hide_index=True)

# Prescriptive section
st.subheader("Prescriptive Actions")
actions = [
    "Personalized discounts for cart-risk sessions.",
    "Dynamic pricing using engagement rating.",
    "Cross-sell categories 2, 5, and 6.",
    "Align inventory to revenue patterns.",
    "Shift budget toward Direct and Organic channels."
]
for action in actions:
    st.write(f"- {action}")

st.caption(f"Source metrics: {sessions:,} sessions, {unique_customers:,} customers, {revenue_m:.2f}M revenue, {conversion_rate:.1f}% conversion, {cart_abandonment:.1f}% cart abandonment, best model accuracy {best_accuracy:.1f}%.")
'''
path = out / 'ecommerce_dashboard.py'
path.write_text(code)
print(path)
