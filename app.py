import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Global AI Job Market Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PREMIUM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(201,164,90,0.08), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(201,164,90,0.05), transparent 25%),
        #07111f;
    color: #f5f1e8;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* Main container */

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1450px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #091522;
    border-right: 1px solid rgba(201,164,90,0.18);
}

section[data-testid="stSidebar"] * {
    color: #f5f1e8 !important;
}

/* Hero */

.hero {
    padding: 35px 40px;
    border-radius: 22px;
    margin-bottom: 28px;

    background:
        linear-gradient(
            135deg,
            rgba(201,164,90,0.14),
            rgba(7,17,31,0.95)
        );

    border: 1px solid rgba(201,164,90,0.25);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.30);
}

.hero-label {
    color: #c9a45a;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 48px;
    line-height: 1.1;
    margin: 8px 0;
    color: #f8f4eb;
}

.hero-description {
    color: #aeb7c3;
    font-size: 16px;
    max-width: 760px;
}

/* KPI cards */

.kpi {
    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.055),
        rgba(255,255,255,0.015)
    );

    border: 1px solid rgba(201,164,90,0.18);

    border-radius: 18px;

    padding: 22px;

    min-height: 125px;

    box-shadow:
        0 12px 40px rgba(0,0,0,0.20);

    transition: 0.3s ease;
}

.kpi:hover {
    transform: translateY(-4px);
    border-color: rgba(201,164,90,0.55);
}

.kpi-label {
    color: #929dab;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.kpi-value {
    color: #f5f1e8;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

.kpi-accent {
    color: #c9a45a;
}

/* Section titles */

.section-title {
    color: #f5f1e8;
    font-size: 22px;
    font-weight: 600;
    margin-top: 32px;
    margin-bottom: 15px;
}

.section-subtitle {
    color: #8994a3;
    font-size: 13px;
    margin-bottom: 18px;
}

/* Chart containers */

.chart-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 8px;
}

/* Tabs */

button[data-baseweb="tab"] {
    color: #aeb7c3;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #c9a45a;
}

/* Buttons */

.stButton > button {
    background: #c9a45a;
    color: #07111f;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

/* Dataframe */

[data-testid="stDataFrame"] {
    border: 1px solid rgba(201,164,90,0.15);
    border-radius: 14px;
}

/* Divider */

hr {
    border-color: rgba(201,164,90,0.15);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df1 = pd.read_csv("ai_job_dataset.csv")
    df2 = pd.read_csv("ai_job_dataset1.csv")

    df = pd.concat(
        [df1, df2],
        ignore_index=True,
        sort=False
    )

    if "job_id" in df.columns:
        df = df.drop_duplicates(subset="job_id")

    df["salary_usd"] = pd.to_numeric(
        df["salary_usd"],
        errors="coerce"
    )

    df["required_skills"] = (
        df["required_skills"]
        .fillna("Unknown")
        .astype(str)
    )

    # Clean skill names

    df["required_skills"] = df["required_skills"].apply(
        lambda x: ", ".join(
            skill.strip().title()
            for skill in x.split(",")
            if skill.strip()
        )
    )

    return df


df = load_data()


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-label">
DATA SCIENCE • AI • LABOR MARKET ANALYTICS
</div>

<div class="hero-title">
Global AI Job Market<br>
Intelligence
</div>

<div class="hero-description">
An interactive analysis of global AI employment,
salary trends, hiring demand, industries and
technical skills across the 2025 job market.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## Dashboard Controls")

st.sidebar.markdown(
    "Filter the global job market dataset."
)

st.sidebar.divider()


experience_options = sorted(
    df["experience_level"]
    .dropna()
    .unique()
)

country_options = sorted(
    df["company_location"]
    .dropna()
    .unique()
)

industry_options = sorted(
    df["industry"]
    .dropna()
    .unique()
)


experience_filter = st.sidebar.multiselect(
    "Experience Level",
    experience_options,
    default=experience_options
)


country_filter = st.sidebar.multiselect(
    "Country",
    country_options,
    default=country_options
)


industry_filter = st.sidebar.multiselect(
    "Industry",
    industry_options,
    default=industry_options
)


salary_range = st.sidebar.slider(
    "Salary Range (USD)",
    int(df["salary_usd"].min()),
    int(df["salary_usd"].max()),
    (
        int(df["salary_usd"].min()),
        int(df["salary_usd"].max())
    ),
    step=5000
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["experience_level"].isin(experience_filter)) &
    (df["company_location"].isin(country_filter)) &
    (df["industry"].isin(industry_filter)) &
    (df["salary_usd"].between(
        salary_range[0],
        salary_range[1]
    ))
].copy()


# ============================================================
# KPI SECTION
# ============================================================

total_jobs = len(filtered_df)

avg_salary = filtered_df["salary_usd"].mean()

countries = filtered_df["company_location"].nunique()

unique_skills = (
    filtered_df["required_skills"]
    .str.split(",")
    .explode()
    .str.strip()
    .nunique()
)


st.markdown(
    '<div class="section-title">Market Snapshot</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(4)


with k1:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">Total Jobs</div>
        <div class="kpi-value">{total_jobs:,}</div>
    </div>
    """, unsafe_allow_html=True)


with k2:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">Average Salary</div>
        <div class="kpi-value">
            ${avg_salary:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)


with k3:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">Countries</div>
        <div class="kpi-value">{countries}</div>
    </div>
    """, unsafe_allow_html=True)


with k4:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">Skills Identified</div>
        <div class="kpi-value">{unique_skills}</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PLOTLY THEME
# ============================================================

plot_bg = "rgba(0,0,0,0)"

plot_layout = dict(
    template="plotly_dark",
    paper_bgcolor=plot_bg,
    plot_bgcolor=plot_bg,
    font=dict(
        color="#dce2e8"
    ),
    margin=dict(
        l=30,
        r=30,
        t=45,
        b=40
    ),
)


# ============================================================
# SKILLS ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Skills Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Most frequently requested technical skills across filtered job postings.'
    '</div>',
    unsafe_allow_html=True
)


skills = (
    filtered_df["required_skills"]
    .str.split(",")
    .explode()
    .str.strip()
)

top_skills = (
    skills
    .value_counts()
    .head(12)
    .sort_values()
)


fig_skills = go.Figure(
    go.Bar(
        x=top_skills.values,
        y=top_skills.index,
        orientation="h",
        text=top_skills.values,
        textposition="outside"
    )
)

fig_skills.update_layout(
    **plot_layout,
    title="Top In-Demand Skills",
    xaxis_title="Job Count",
    yaxis_title=""
)

st.plotly_chart(
    fig_skills,
    use_container_width=True
)


# ============================================================
# EXPERIENCE + SALARY
# ============================================================

col1, col2 = st.columns(2)


with col1:

    experience_counts = (
        filtered_df["experience_level"]
        .value_counts()
        .reset_index()
    )

    experience_counts.columns = [
        "Experience",
        "Jobs"
    ]

    fig_exp = px.bar(
        experience_counts,
        x="Experience",
        y="Jobs",
        title="Job Distribution by Experience"
    )

    fig_exp.update_layout(**plot_layout)

    st.plotly_chart(
        fig_exp,
        use_container_width=True
    )


with col2:

    salary_exp = (
        filtered_df
        .groupby("experience_level")["salary_usd"]
        .mean()
        .reset_index()
    )

    fig_salary = px.bar(
        salary_exp,
        x="experience_level",
        y="salary_usd",
        title="Average Salary by Experience",
        text_auto=".2s"
    )

    fig_salary.update_layout(
        **plot_layout,
        yaxis_title="Salary (USD)",
        xaxis_title="Experience"
    )

    st.plotly_chart(
        fig_salary,
        use_container_width=True
    )


# ============================================================
# GLOBAL HIRING
# ============================================================

st.markdown(
    '<div class="section-title">Global Hiring Intelligence</div>',
    unsafe_allow_html=True
)


col3, col4 = st.columns(2)


with col3:

    top_countries = (
        filtered_df["company_location"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    top_countries.columns = [
        "Country",
        "Jobs"
    ]

    fig_country = px.bar(
        top_countries,
        x="Jobs",
        y="Country",
        orientation="h",
        title="Top Hiring Countries"
    )

    fig_country.update_layout(
        **plot_layout,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )


with col4:

    country_salary = (
        filtered_df
        .groupby("company_location")["salary_usd"]
        .mean()
        .sort_values(
            ascending=False
        )
        .head(15)
        .reset_index()
    )

    fig_country_salary = px.bar(
        country_salary,
        x="salary_usd",
        y="company_location",
        orientation="h",
        title="Highest Average Salaries by Country",
        text_auto=".2s"
    )

    fig_country_salary.update_layout(
        **plot_layout,
        yaxis=dict(
            categoryorder="total ascending"
        ),
        xaxis_title="Salary (USD)"
    )

    st.plotly_chart(
        fig_country_salary,
        use_container_width=True
    )


# ============================================================
# INDUSTRY ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Industry Intelligence</div>',
    unsafe_allow_html=True
)


industry_counts = (
    filtered_df["industry"]
    .value_counts()
    .reset_index()
)

industry_counts.columns = [
    "Industry",
    "Jobs"
]


fig_industry = px.bar(
    industry_counts,
    x="Jobs",
    y="Industry",
    orientation="h",
    title="AI Job Distribution by Industry"
)

fig_industry.update_layout(
    **plot_layout,
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig_industry,
    use_container_width=True
)


# ============================================================
# SALARY DISTRIBUTION
# ============================================================

st.markdown(
    '<div class="section-title">Salary Intelligence</div>',
    unsafe_allow_html=True
)


col5, col6 = st.columns(2)


with col5:

    fig_hist = px.histogram(
        filtered_df,
        x="salary_usd",
        nbins=30,
        title="Global Salary Distribution"
    )

    fig_hist.update_layout(
        **plot_layout,
        xaxis_title="Salary (USD)",
        yaxis_title="Number of Jobs"
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )


with col6:

    fig_box = px.box(
        filtered_df,
        x="experience_level",
        y="salary_usd",
        title="Salary Distribution by Experience"
    )

    fig_box.update_layout(
        **plot_layout,
        yaxis_title="Salary (USD)",
        xaxis_title="Experience"
    )

    st.plotly_chart(
        fig_box,
        use_container_width=True
    )


# ============================================================
# COMPANY SIZE
# ============================================================

company_salary = (
    filtered_df
    .groupby("company_size")["salary_usd"]
    .mean()
    .reset_index()
)


fig_company = px.bar(
    company_salary,
    x="company_size",
    y="salary_usd",
    title="Average Salary by Company Size",
    text_auto=".2s"
)

fig_company.update_layout(
    **plot_layout,
    xaxis_title="Company Size",
    yaxis_title="Salary (USD)"
)

st.plotly_chart(
    fig_company,
    use_container_width=True
)


# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">Data Explorer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Explore the underlying job-market dataset.'
    '</div>',
    unsafe_allow_html=True
)


search = st.text_input(
    "Search job records",
    placeholder="Search by job title, company, country, skill..."
)


display_df = filtered_df.copy()


if search:

    search_mask = display_df.astype(str).apply(
        lambda row:
        row.str.contains(
            search,
            case=False,
            na=False
        ).any(),
        axis=1
    )

    display_df = display_df[
        search_mask
    ]


st.dataframe(
    display_df,
    use_container_width=True,
    height=450
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown("""
<div style="
text-align:center;
color:#778291;
font-size:12px;
padding:20px;
">

GLOBAL AI JOB MARKET INTELLIGENCE

<br><br>

Built with Python • Pandas • Plotly • Streamlit

<br>

Data Science Portfolio Project

</div>
""", unsafe_allow_html=True)
