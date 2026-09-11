import streamlit as st
import pandas as pd

st.title("IPL Data Analysis")

# Load dataset
df = pd.read_csv("IPL_2008_2026_Merged.csv")

# Dataset preview
st.header("Dataset")

st.dataframe(df)

# Dataset information
st.header("Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Rows", df.shape[0])

with col2:
    st.metric("Total Columns", df.shape[1])

# Missing values
st.subheader("Missing Values")

st.dataframe(df.isnull().sum())

# Filters
st.header("Filters")

season = st.selectbox(
    "Select Season",
    ["All"] + sorted(df["season"].dropna().unique().tolist())
)

team = st.selectbox(
    "Select Team",
    ["All"] + sorted(
        set(df["team1"].dropna().unique()) |
        set(df["team2"].dropna().unique())
    )
)

# Apply filters
filtered_df = df.copy()

if season != "All":
    filtered_df = filtered_df[filtered_df["season"] == season]

if team != "All":
    filtered_df = filtered_df[
        (filtered_df["team1"] == team) |
        (filtered_df["team2"] == team)
    ]

st.subheader("Filtered Data")

st.dataframe(filtered_df)

# KPI calculations
total_runs = (
    filtered_df["team1_runs"].fillna(0).sum()
    + filtered_df["team2_runs"].fillna(0).sum()
)

average_runs = (
    total_runs / len(filtered_df)
    if len(filtered_df) > 0 else 0
)

highest_score = (
    filtered_df["team1_runs"].fillna(0)
    + filtered_df["team2_runs"].fillna(0)
).max()

total_wickets = (
    filtered_df["team1_wickets"].fillna(0).sum()
    + filtered_df["team2_wickets"].fillna(0).sum()
)

# KPI Cards
st.header("IPL Statistics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Match Runs", int(total_runs))

with c2:
    st.metric("Average Match Runs", round(average_runs, 2))

with c3:
    st.metric("Highest Combined Score", int(highest_score))

with c4:
    st.metric("Total Wickets", int(total_wickets))