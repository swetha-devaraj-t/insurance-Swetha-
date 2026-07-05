"""
Noon Ecosystem Insights Dashboard
==================================
Covers 5 business problems with illustrative (simulated) data:
 1. Generic Customer Experience -> Chameleon UI / RFM segmentation
 2. Inefficient Promotional Spend -> LTV & Churn targeting
 3. Cart Abandonment in Noon Minutes -> Surge pricing / funnel drop-off
 4. Ecosystem Silos -> Cross-sell / Market Basket Analysis
 5. Dark Store Inventory -> Demand forecasting by neighborhood

Run with:
    pip install streamlit pandas numpy plotly --break-system-packages
    streamlit run noon_dashboard.py

Replace the `generate_*` functions with real data loaders (CSV/SQL/Snowflake)
when you plug in actual Noon data.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Noon Ecosystem Insights Dashboard",
    page_icon="🛒",
    layout="wide",
)

np.random.seed(42)

# ----------------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------------
st.sidebar.title("🛒 Noon Insights")
page = st.sidebar.radio(
    "Select a problem area",
    [
        "Overview",
        "1. Generic Customer Experience",
        "2. Promotional Spend Efficiency",
        "3. Noon Minutes Cart Abandonment",
        "4. Ecosystem Cross-Selling",
        "5. Dark Store Inventory",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "All figures below use **simulated sample data** for illustration. "
    "Swap in real data sources (transactions, clickstream, inventory feeds) "
    "to make this production-ready."
)

# ----------------------------------------------------------------------------
# Data generators (replace with real data loading later)
# ----------------------------------------------------------------------------

@st.cache_data
def generate_customer_segments(n=2000):
    segments = np.random.choice(
        ["Champions", "Loyal", "At-Risk", "Bargain Hunters", "New"],
        size=n, p=[0.15, 0.25, 0.15, 0.30, 0.15]
    )
    recency = np.random.randint(1, 180, n)
    frequency = np.random.poisson(5, n) + 1
    monetary = np.round(np.random.exponential(400, n) + 50, 2)
    device = np.random.choice(["Mobile App", "Mobile Web", "Desktop"], n, p=[0.6, 0.25, 0.15])
    category = np.random.choice(
        ["Electronics", "Groceries", "Fashion", "Beauty", "Home"], n
    )
    return pd.DataFrame({
        "segment": segments, "recency_days": recency, "frequency": frequency,
        "monetary_aed": monetary, "device": device, "category": category
    })


@st.cache_data
def generate_ltv_churn(n=1500):
    segments = np.random.choice(
        ["Champions", "Loyal", "At-Risk", "Bargain Hunters", "New"],
        size=n, p=[0.15, 0.25, 0.15, 0.30, 0.15]
    )
    base_ltv = {"Champions": 3200, "Loyal": 1800, "At-Risk": 900,
                "Bargain Hunters": 600, "New": 400}
    ltv = [max(50, np.random.normal(base_ltv[s], base_ltv[s]*0.3)) for s in segments]
    base_churn = {"Champions": 0.05, "Loyal": 0.15, "At-Risk": 0.65,
                  "Bargain Hunters": 0.35, "New": 0.45}
    churn_prob = [np.clip(np.random.normal(base_churn[s], 0.08), 0, 1) for s in segments]
    discount_given = np.random.choice([0, 10, 15, 20, 25], n)
    return pd.DataFrame({
        "segment": segments, "predicted_ltv_aed": np.round(ltv, 2),
        "churn_probability": np.round(churn_prob, 2),
        "current_discount_pct": discount_given
    })


@st.cache_data
def generate_funnel():
    hours = list(range(0, 24))
    base_funnel = {"Browse": 10000, "Add to Cart": 6200, "Checkout Start": 4100, "Payment": 3500, "Order Complete": 3050}
    stages = list(base_funnel.keys())
    surge_hours = [12, 13, 19, 20, 21]
    rows = []
    for h in hours:
        surge = 1.4 if h in surge_hours else 1.0
        prev = None
        for i, stage in enumerate(stages):
            drop_extra = surge if stage in ("Checkout Start", "Payment") else 1.0
            val = base_funnel[stage] / drop_extra * np.random.uniform(0.9, 1.1)
            rows.append({"hour": h, "stage": stage, "users": int(val), "surge": surge > 1})
    return pd.DataFrame(rows)


@st.cache_data
def generate_basket_size_sensitivity():
    basket = np.arange(20, 200, 5)
    surge_fee = np.maximum(0, 15 - basket * 0.08)
    conversion = 100 / (1 + np.exp(-(basket - 90) / 20)) * 0.9 + 5
    return pd.DataFrame({"basket_aed": basket, "surge_fee_aed": np.round(surge_fee, 1),
                          "conversion_rate_pct": np.round(conversion, 1)})


@st.cache_data
def generate_cross_sell():
    apps = ["Marketplace", "Noon Food", "Noon Pay", "Noon Minutes"]
    matrix = pd.DataFrame(
        [[1.0, 0.12, 0.35, 0.18],
         [0.12, 1.0, 0.22, 0.55],
         [0.35, 0.22, 1.0, 0.28],
         [0.18, 0.55, 0.28, 1.0]],
        index=apps, columns=apps
    )
    rules = pd.DataFrame({
        "trigger_purchase": ["Gaming Console", "Baby Products", "Home Workout Gear", "Kitchen Appliance", "Travel Bag"],
        "recommended_action": ["Order Food (Noon Food)", "Subscribe & Save (Marketplace)",
                                "Protein Snacks (Noon Minutes)", "Recipe Ingredients (Noon Minutes)",
                                "Travel Insurance (Noon Pay)"],
        "lift": [3.2, 2.1, 2.8, 2.4, 1.9],
        "confidence_pct": [42, 38, 51, 47, 33]
    })
    return matrix, rules


@st.cache_data
def generate_inventory(n_days=30):
    neighborhoods = ["Downtown", "Marina", "Al Barsha", "Deira", "JVC"]
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days)
    rows = []
    for nb in neighborhoods:
        base = np.random.randint(80, 200)
        for d in dates:
            weekend_boost = 1.3 if d.dayofweek >= 5 else 1.0
            demand = int(base * weekend_boost * np.random.uniform(0.8, 1.3))
            stock = int(base * 1.1 * np.random.uniform(0.7, 1.05))
            rows.append({"date": d, "neighborhood": nb, "demand_units": demand,
                         "stock_units": stock, "stockout": stock < demand})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------

if page == "Overview":
    st.title("🛒 Noon Ecosystem Insights Dashboard")
    st.markdown(
        """
        This dashboard summarizes **5 key business problems** across the Noon ecosystem,
        each with a proposed data-driven solution. Use the sidebar to explore each area.
        """
    )
    cols = st.columns(5)
    problems = [
        ("Generic UX", "Chameleon UI via RFM segmentation"),
        ("Promo Spend", "LTV & churn-based targeting"),
        ("Cart Abandonment", "Transparent surge pricing"),
        ("Ecosystem Silos", "Cross-sell recommendation engine"),
        ("Dark Store Stockouts", "Hyper-local demand forecasting"),
    ]
    for c, (title, desc) in zip(cols, problems):
        with c:
            st.metric(title, "▶")
            st.caption(desc)

    st.markdown("---")
    st.subheader("Suggested Analytics Stack")
    st.table(pd.DataFrame({
        "Problem": [p[0] for p in problems],
        "Core Method": [
            "RFM clustering + Collaborative Filtering",
            "BTYD/Lifetimes LTV + XGBoost churn",
            "Funnel analysis + Price elasticity",
            "Apriori / Market Basket Analysis",
            "ARIMA / Prophet + GeoPandas",
        ],
        "Tools": [
            "Python (Scikit-learn, Pandas), A/B testing",
            "Python (lifetimes), Cohort analysis",
            "Mixpanel/Amplitude, Kafka streaming",
            "Graph DB, Snowflake/BigQuery",
            "Prophet, GeoPandas, replenishment bots",
        ],
    }))

# ----------------------------------------------------------------------------
elif page == "1. Generic Customer Experience":
    st.title("1️⃣ Generic Customer Experience → Chameleon UI")
    df = generate_customer_segments()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, names="segment", title="Customer Segment Mix (RFM-based)", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.box(df, x="segment", y="monetary_aed", color="segment",
                     title="Monetary Value (AOV proxy) by Segment")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = px.scatter(df, x="recency_days", y="frequency", color="segment",
                          size="monetary_aed", opacity=0.6,
                          title="RFM Scatter: Recency vs Frequency")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        pivot = df.groupby(["segment", "category"]).size().reset_index(name="count")
        fig = px.bar(pivot, x="segment", y="count", color="category",
                     title="Category Affinity by Segment", barmode="stack")
        st.plotly_chart(fig, use_container_width=True)

    st.info("💡 **Chameleon UI concept:** homepage layout, banners, and recommended "
            "SKUs would be dynamically selected per segment above, using a "
            "Collaborative Filtering model refreshed via A/B tested variants.")

# ----------------------------------------------------------------------------
elif page == "2. Promotional Spend Efficiency":
    st.title("2️⃣ Inefficient Promotional Spend → LTV-Based Targeting")
    df = generate_ltv_churn()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(df, x="predicted_ltv_aed", y="churn_probability", color="segment",
                          size="current_discount_pct", opacity=0.6,
                          title="LTV vs Churn Probability (bubble = current discount %)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        summary = df.groupby("segment").agg(
            avg_ltv=("predicted_ltv_aed", "mean"),
            avg_churn=("churn_probability", "mean"),
            avg_discount=("current_discount_pct", "mean")
        ).reset_index()
        fig = px.bar(summary, x="segment", y="avg_discount", color="segment",
                     title="Current Avg Discount % by Segment (should target At-Risk more)")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Misallocation Check")
    misallocated = df[(df["segment"] == "Champions") & (df["current_discount_pct"] >= 15)]
    underserved = df[(df["segment"] == "At-Risk") & (df["current_discount_pct"] < 15)]
    m1, m2 = st.columns(2)
    m1.metric("Champions over-discounted", f"{len(misallocated)} customers",
               help="High-value loyal customers getting 15%+ off who likely would've bought anyway")
    m2.metric("At-Risk under-incentivized", f"{len(underserved)} customers",
               help="High-churn-risk customers getting less than 15% off")

    st.dataframe(summary.style.format({"avg_ltv": "{:.0f} AED", "avg_churn": "{:.0%}", "avg_discount": "{:.1f}%"}))

# ----------------------------------------------------------------------------
elif page == "3. Noon Minutes Cart Abandonment":
    st.title("3️⃣ Cart Abandonment in Noon Minutes → Transparent Surge Pricing")
    funnel_df = generate_funnel()
    basket_df = generate_basket_size_sensitivity()

    st.subheader("Funnel Drop-off by Hour (Surge vs Non-Surge)")
    agg = funnel_df.groupby(["stage", "surge"])["users"].mean().reset_index()
    fig = px.bar(agg, x="stage", y="users", color="surge", barmode="group",
                 title="Avg Users per Stage: Surge Hours vs Normal Hours",
                 labels={"surge": "Surge Hour"})
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=basket_df["basket_aed"], y=basket_df["surge_fee_aed"],
                                  name="Surge Fee (AED)", line=dict(color="crimson")))
        fig.update_layout(title="Surge Fee vs Basket Size (waived above ~AED 190)",
                           xaxis_title="Basket Value (AED)", yaxis_title="Surge Fee (AED)")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.line(basket_df, x="basket_aed", y="conversion_rate_pct",
                       title="Estimated Checkout Conversion vs Basket Size")
        st.plotly_chart(fig, use_container_width=True)

    st.success("💡 **Nudge idea:** show a live progress bar — "
               "\"Add X AED more to waive your surge fee\" — computed from the curve above.")

# ----------------------------------------------------------------------------
elif page == "4. Ecosystem Cross-Selling":
    st.title("4️⃣ Ecosystem Silos → Next Best Action Engine")
    matrix, rules = generate_cross_sell()

    st.subheader("Cross-App Usage Overlap")
    fig = px.imshow(matrix, text_auto=True, color_continuous_scale="Blues",
                     title="Share of Users Overlapping Across Noon Apps")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Market Basket / Next-Best-Action Rules")
    fig = px.bar(rules, x="trigger_purchase", y="lift", color="confidence_pct",
                 title="Association Rule Lift by Trigger Purchase",
                 hover_data=["recommended_action"], color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(rules)

    st.info("💡 Example: a customer buying a **Gaming Console** on Marketplace shows "
            "3.2x lift for ordering food within 2 hours → trigger a Noon Food push notification.")

# ----------------------------------------------------------------------------
elif page == "5. Dark Store Inventory":
    st.title("5️⃣ Dark Store Inventory → Hyper-Local Demand Forecasting")
    df = generate_inventory()

    neighborhoods = df["neighborhood"].unique().tolist()
    selected = st.multiselect("Filter neighborhoods", neighborhoods, default=neighborhoods)
    filtered = df[df["neighborhood"].isin(selected)]

    fig = px.line(filtered, x="date", y="demand_units", color="neighborhood",
                  title="Demand Trend by Neighborhood (last 30 days)")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.area(filtered.groupby(["date", "neighborhood"])["stock_units"].sum().reset_index(),
                    x="date", y="stock_units", color="neighborhood",
                    title="Stock Levels Over Time")
    st.plotly_chart(fig2, use_container_width=True)

    stockout_rate = filtered.groupby("neighborhood")["stockout"].mean().reset_index()
    stockout_rate["stockout_rate_pct"] = (stockout_rate["stockout"] * 100).round(1)
    fig3 = px.bar(stockout_rate, x="neighborhood", y="stockout_rate_pct", color="neighborhood",
                  title="Stockout Rate % by Neighborhood (last 30 days)")
    st.plotly_chart(fig3, use_container_width=True)

    st.warning("💡 Neighborhoods with high stockout rate above should get **priority "
               "replenishment** using Prophet/ARIMA forecasts + weather/event triggers.")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit + Plotly · Replace simulated data with live sources when ready.")
