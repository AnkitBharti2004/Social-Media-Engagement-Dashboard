import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Social Media Engagement Dashboard", page_icon="📊", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "sample_engagement_data.csv"

st.title("📊 Social Media Engagement Dashboard")
st.caption("Track content performance, compare platforms, and discover practical posting insights.")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce").fillna(12).astype(int)
    for col in ["likes", "comments", "shares", "impressions", "reach", "clicks", "followers_gained"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["engagements"] = df["likes"] + df["comments"] + df["shares"]
    df["engagement_rate"] = (df["engagements"] / df["impressions"].replace(0, pd.NA) * 100).fillna(0)
    df["ctr"] = (df["clicks"] / df["impressions"].replace(0, pd.NA) * 100).fillna(0)
    return df

df = load_data()
with st.sidebar:
    st.header("Filters")
    platforms = st.multiselect("Platform", sorted(df["platform"].unique()), default=sorted(df["platform"].unique()))
    content_types = st.multiselect("Content type", sorted(df["content_type"].unique()), default=sorted(df["content_type"].unique()))
    date_min, date_max = df["date"].min().date(), df["date"].max().date()
    date_range = st.date_input("Date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range

filtered = df[
    df["platform"].isin(platforms) &
    df["content_type"].isin(content_types) &
    df["date"].dt.date.between(start_date, end_date)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Select another platform, content type, or date range.")
    st.stop()

total_engagements = int(filtered["engagements"].sum())
total_impressions = int(filtered["impressions"].sum())
total_reach = int(filtered["reach"].sum())
avg_rate = (total_engagements / total_impressions * 100) if total_impressions else 0
total_posts = len(filtered)
followers = int(filtered["followers_gained"].sum())

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Posts", f"{total_posts:,}")
c2.metric("Engagements", f"{total_engagements:,}")
c3.metric("Impressions", f"{total_impressions:,}")
c4.metric("Avg. engagement rate", f"{avg_rate:.2f}%")
c5.metric("Followers gained", f"{followers:,}")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Content analysis", "Best posting time", "Data & export"])
with tab1:
    left, right = st.columns(2)
    with left:
        daily = filtered.groupby(filtered["date"].dt.date, as_index=False).agg(
            engagements=("engagements", "sum"), impressions=("impressions", "sum"))
        st.plotly_chart(px.line(daily, x="date", y="engagements", markers=True,
                                title="Engagements over time"), use_container_width=True)
    with right:
        plat = filtered.groupby("platform", as_index=False).agg(
            engagements=("engagements", "sum"), impressions=("impressions", "sum"))
        st.plotly_chart(px.bar(plat, x="platform", y="engagements", color="platform",
                               title="Engagements by platform"), use_container_width=True)
    metrics = filtered.groupby("platform", as_index=False).agg(
        likes=("likes", "sum"), comments=("comments", "sum"), shares=("shares", "sum"))
    melt = metrics.melt(id_vars="platform", var_name="metric", value_name="count")
    st.plotly_chart(px.bar(melt, x="platform", y="count", color="metric", barmode="group",
                           title="Likes, comments and shares by platform"), use_container_width=True)

with tab2:
    by_type = filtered.groupby("content_type", as_index=False).agg(
        posts=("post_id", "count"), engagements=("engagements", "sum"),
        impressions=("impressions", "sum"), clicks=("clicks", "sum"))
    by_type["engagement_rate_pct"] = (by_type["engagements"] / by_type["impressions"].replace(0, pd.NA) * 100).fillna(0)
    by_type["ctr_pct"] = (by_type["clicks"] / by_type["impressions"].replace(0, pd.NA) * 100).fillna(0)
    l, r = st.columns(2)
    with l:
        st.plotly_chart(px.bar(by_type, x="content_type", y="engagement_rate_pct",
                               color="content_type", title="Engagement rate by content type"),
                        use_container_width=True)
    with r:
        st.plotly_chart(px.bar(by_type, x="content_type", y="engagements",
                               color="content_type", title="Total engagements by content type"),
                        use_container_width=True)
    st.dataframe(by_type.round(2), use_container_width=True, hide_index=True)

with tab3:
    hourly = filtered.groupby("hour", as_index=False).agg(
        engagements=("engagements", "sum"), impressions=("impressions", "sum"), posts=("post_id", "count"))
    hourly["engagement_rate_pct"] = (hourly["engagements"] / hourly["impressions"].replace(0, pd.NA) * 100).fillna(0)
    if not hourly.empty:
        best = hourly.sort_values(["engagement_rate_pct", "engagements"], ascending=False).iloc[0]
        st.success(f"Best observed hour in this filtered sample: **{int(best['hour']):02d}:00** "
                   f"({best['engagement_rate_pct']:.2f}% engagement rate).")
    st.plotly_chart(px.line(hourly, x="hour", y="engagement_rate_pct", markers=True,
                            title="Engagement rate by posting hour", labels={"hour": "Hour of day", "engagement_rate_pct": "Engagement rate (%)"}),
                    use_container_width=True)
    st.caption("This is a pattern in the selected dataset, not a guarantee. Test time slots against your audience's timezone and compare results over several weeks.")

with tab4:
    st.markdown("### Export filtered data")
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"),
                       file_name="filtered_engagement_data.csv", mime="text/csv")
    st.dataframe(filtered.sort_values("date", ascending=False), use_container_width=True, hide_index=True)
    st.info("The included CSV is synthetic demo data. Connect authorized platform APIs to replace it with real account data.")

st.divider()
st.subheader("Recommendations")
if 'by_type' in locals() and not by_type.empty:
    best_type = by_type.sort_values("engagement_rate_pct", ascending=False).iloc[0]
    st.write(f"- Prioritize experiments with **{best_type['content_type']}** content, which has the highest engagement rate in the current filter.")
best_platform = filtered.groupby("platform").apply(
    lambda x: (x["engagements"].sum() / x["impressions"].sum() * 100) if x["impressions"].sum() else 0
).sort_values(ascending=False)
if len(best_platform):
    st.write(f"- Review what works on **{best_platform.index[0]}** and adapt the format to other platforms rather than reposting without changes.")
st.write("- Test two or three posting time slots, track results for several weeks, and use engagement rate alongside reach—not raw likes alone.")
st.write("- Use comments and shares as stronger conversation/utility signals; add clear calls to action where appropriate.")
