import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Global Job Market Dashboard",
    layout="wide"
)

sns.set_theme(style="whitegrid")

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df1 = pd.read_csv("ai_job_dataset.csv")
    df2 = pd.read_csv("ai_job_dataset1.csv")
    df = pd.concat([df1, df2], ignore_index=True, sort=False)
    df = df.drop_duplicates(subset="job_id")

    df["salary_usd"] = pd.to_numeric(df["salary_usd"], errors="coerce")
    df["required_skills"] = df["required_skills"].fillna("Unknown")

    return df

df = load_data()

# ----------------------------
# Title
# ----------------------------
st.title("📊 Global Job Market & Skills Demand Dashboard")
st.markdown("Interactive analysis of AI jobs, salaries, skills, and trends (2025)")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("🔍 Filters")

experience_filter = st.sidebar.multiselect(
    "Select Experience Level",
    options=df["experience_level"].unique(),
    default=df["experience_level"].unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df["company_location"].unique(),
    default=df["company_location"].unique()
)

filtered_df = df[
    (df["experience_level"].isin(experience_filter)) &
    (df["company_location"].isin(country_filter))
]

# ----------------------------
# ROW 1
# ----------------------------
col1, col2 = st.columns(2)

# 1️⃣ Top 10 Skills
with col1:
    st.subheader("Top 10 In-Demand Skills")
    skills = filtered_df["required_skills"].str.split(",").explode()
    top_skills = skills.value_counts().head(10)

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(
        x=top_skills.values,
        y=top_skills.index,
        hue=top_skills.index,
        palette="viridis",
        legend=False,
        ax=ax
    )
    ax.set_xlabel("Job Count")
    ax.set_ylabel("Skill")
    st.pyplot(fig)

# 2️⃣ Experience Distribution
with col2:
    st.subheader("Job Distribution by Experience Level")
    fig, ax = plt.subplots(figsize=(6,4))
    sns.countplot(
        x="experience_level",
        data=filtered_df,
        hue="experience_level",
        palette="pastel",
        legend=False,
        ax=ax
    )
    ax.set_xlabel("Experience Level")
    ax.set_ylabel("Job Count")
    st.pyplot(fig)

# ----------------------------
# ROW 2
# ----------------------------
col3, col4 = st.columns(2)

# 3️⃣ Avg Salary by Experience
with col3:
    st.subheader("Average Salary by Experience Level")
    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(
        x="experience_level",
        y="salary_usd",
        data=filtered_df,
        hue="experience_level",
        palette="coolwarm",
        legend=False,
        ax=ax
    )
    ax.set_ylabel("Salary (USD)")
    st.pyplot(fig)

# 4️⃣ Salary Distribution
with col4:
    st.subheader("Salary Distribution")
    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(
        filtered_df["salary_usd"],
        bins=30,
        kde=True,
        color="purple",
        ax=ax
    )
    ax.set_xlabel("Salary (USD)")
    st.pyplot(fig)

# ----------------------------
# ROW 3
# ----------------------------
col5, col6 = st.columns(2)

# 5️⃣ Top Countries Hiring
with col5:
    st.subheader("Top 10 Countries Hiring AI Professionals")
    top_countries = filtered_df["company_location"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(
        x=top_countries.index,
        y=top_countries.values,
        hue=top_countries.index,
        palette="tab10",
        legend=False,
        ax=ax
    )
    ax.set_xlabel("Country")
    ax.set_ylabel("Job Count")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 6️⃣ Avg Salary by Country
with col6:
    st.subheader("Average Salary by Country")
    country_salary = filtered_df[
        filtered_df["company_location"].isin(top_countries.index)
    ]

    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(
        x="company_location",
        y="salary_usd",
        data=country_salary,
        hue="company_location",
        palette="rocket",
        legend=False,
        ax=ax
    )
    plt.xticks(rotation=45)
    ax.set_ylabel("Salary (USD)")
    st.pyplot(fig)

# ----------------------------
# ROW 4
# ----------------------------
col7, col8 = st.columns(2)

# 7️⃣ Industry Distribution
with col7:
    st.subheader("Job Distribution by Industry")
    fig, ax = plt.subplots(figsize=(6,5))
    sns.countplot(
        y="industry",
        data=filtered_df,
        order=filtered_df["industry"].value_counts().index,
        hue="industry",
        palette="cubehelix",
        legend=False,
        ax=ax
    )
    ax.set_xlabel("Job Count")
    st.pyplot(fig)

# 8️⃣ Salary vs Experience (Boxplot)
with col8:
    st.subheader("Salary Distribution by Experience Level")
    fig, ax = plt.subplots(figsize=(6,5))
    sns.boxplot(
        x="experience_level",
        y="salary_usd",
        data=filtered_df,
        hue="experience_level",
        palette="Set1",
        legend=False,
        ax=ax
    )
    ax.set_ylabel("Salary (USD)")
    st.pyplot(fig)

# ----------------------------
# ROW 5
# ----------------------------
st.subheader("Average Salary by Company Size")
fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(
    x="company_size",
    y="salary_usd",
    data=filtered_df,
    hue="company_size",
    palette="Spectral",
    legend=False,
    ax=ax
)
ax.set_ylabel("Salary (USD)")
st.pyplot(fig)

# ----------------------------
# Footer
# ----------------------------


