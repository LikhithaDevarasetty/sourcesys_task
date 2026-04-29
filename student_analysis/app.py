import streamlit as st
import pandas as pd
import numpy as np


# PAGE CONFIG
st.set_page_config(page_title="Student Analyzer", layout="wide")

st.title("📊 Student Data Analysis Dashboard")
st.write("Interactive analysis of student performance dataset")


# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_student_data.csv")

    # Handle missing values
    df["AGE"].fillna(df["AGE"].mean(), inplace=True)
    df["ATTENDANCE"].fillna(df["ATTENDANCE"].mean(), inplace=True)
    df["EXAM SCORE"].fillna(df["EXAM SCORE"].mean(), inplace=True)

    return df

df = load_data()


# SIDEBAR OPTIONS
st.sidebar.header("🔍 Select Analysis")

option = st.sidebar.selectbox(
    "Choose what you want to see",
    [
        "Dataset Overview",
        "Statistical Summary",
        "Group Analysis",
        "Top / Low Performers",
        "Filter Data",
        "Correlation",
        "Custom Insights"
    ]
)


# 1. DATASET OVERVIEW
if option == "Dataset Overview":
    st.subheader("📌 Dataset Overview")
    st.dataframe(df)

    st.write("Shape of dataset:", df.shape)


# 2. STATISTICS
elif option == "Statistical Summary":
    st.subheader("📈 Statistical Summary")
    st.write(df.describe())


# 3. GROUP ANALYSIS
elif option == "Group Analysis":
    st.subheader("📊 Group Analysis")

    group_option = st.selectbox(
        "Select category",
        ["TUTION", "HEALTH", "STRESS", "DAILY WORK"]
    )

    result = df.groupby(group_option)["EXAM SCORE"].mean()
    st.write(result)

    st.bar_chart(result)


# 4. TOP / LOW PERFORMERS
elif option == "Top / Low Performers":
    st.subheader("🏆 Performance Analysis")

    choice = st.radio("Select", ["Top Students", "Low Students"])

    if choice == "Top Students":
        st.dataframe(df.sort_values(by="EXAM SCORE", ascending=False).head(10))
    else:
        st.dataframe(df.sort_values(by="EXAM SCORE").head(10))


# 5. FILTER DATA
elif option == "Filter Data":
    st.subheader("🔍 Filter Students")

    attendance = st.slider("Minimum Attendance", 0, 100, 75)
    study = st.slider("Minimum Self Study Hours", 0, 6, 2)

    filtered = df[
        (df["ATTENDANCE"] >= attendance) &
        (df["SELF STUDY"] >= study)
    ]

    st.write("Filtered Results:")
    st.dataframe(filtered)


# 6. CORRELATION
elif option == "Correlation":
    st.subheader("🔗 Correlation Matrix")

    corr = df.corr(numeric_only=True)
    st.write(corr)

    st.line_chart(corr)


# 7. CUSTOM INSIGHTS
elif option == "Custom Insights":
    st.subheader("💡 Insights")

    high_study = df[df["SELF STUDY"] > 3]["EXAM SCORE"].mean()
    low_study = df[df["SELF STUDY"] <= 3]["EXAM SCORE"].mean()

    st.write("📚 Avg Score (High Study >3 hrs):", round(high_study, 2))
    st.write("📚 Avg Score (Low Study ≤3 hrs):", round(low_study, 2))

    more_games = df[df["VIDEO GAMES"] > 2]["EXAM SCORE"].mean()
    less_games = df[df["VIDEO GAMES"] <= 2]["EXAM SCORE"].mean()

    st.write("🎮 Avg Score (More Gaming >2 hrs):", round(more_games, 2))
    st.write("🎮 Avg Score (Less Gaming ≤2 hrs):", round(less_games, 2))

