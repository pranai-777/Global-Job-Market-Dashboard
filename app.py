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
# PREMIUM MULTI-COLOR DARK THEME
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');


/* =========================================================
   GLOBAL
   ========================================================= */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 8% 5%,
            rgba(201,164,90,0.10),
            transparent 22%
        ),

        radial-gradient(
            circle at 92% 10%,
            rgba(34,184,207,0.06),
            transparent 23%
        ),

        radial-gradient(
            circle at 55% 100%,
            rgba(155,93,229,0.05),
            transparent 28%
        ),

        #07111F;

    color: #F5F1E8;
}


/* =========================================================
   STREAMLIT CLEANUP
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1480px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #081321 0%,
            #0B1624 55%,
            #0D1928 100%
        );

    border-right:
        1px solid rgba(201,164,90,0.20);

    box-shadow:
        10px 0 45px rgba(0,0,0,0.25);
}


section[data-testid="stSidebar"] * {
    color: #F5F1E8 !important;
}


section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #C9A45A !important;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {

    position: relative;

    padding: 42px 45px;

    border-radius: 24px;

    margin-bottom: 30px;

    overflow: hidden;

    background:

        radial-gradient(
            circle at 82% 15%,
            rgba(34,184,207,0.08),
            transparent 25%
        ),

        radial-gradient(
            circle at 75% 90%,
            rgba(155,93,229,0.07),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            rgba(201,164,90,0.14),
            rgba(10,20,33,0.96) 55%,
            rgba(7,17,31,0.99)
        );

    border:
        1px solid rgba(201,164,90,0.28);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.38);
}


.hero::after {

    content: "";

    position: absolute;

    width: 280px;
    height: 280px;

    right: -90px;
    top: -120px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(201,164,90,0.15),
            transparent 70%
        );

    pointer-events: none;
}


/* =========================================================
   HERO LABEL
   ========================================================= */

.hero-label {

    color: #C9A45A;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 3px;

    text-transform: uppercase;
}


/* =========================================================
   HERO TITLE
   ========================================================= */

.hero-title {

    font-family:
        'Playfair Display',
        serif;

    font-size: 50px;

    line-height: 1.08;

    margin: 10px 0;

    color: #F8F4EB;

    letter-spacing: -1px;
}


.hero-title .gold {
    color: #C9A45A;
}


/* =========================================================
   HERO DESCRIPTION
   ========================================================= */

.hero-description {

    color: #AEB7C3;

    font-size: 16px;

    line-height: 1.7;

    max-width: 760px;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {

    color: #F5F1E8;

    font-size: 22px;

    font-weight: 600;

    margin-top: 34px;

    margin-bottom: 8px;

    position: relative;

    padding-left: 14px;
}


.section-title::before {

    content: "";

    position: absolute;

    left: 0;

    top: 3px;

    width: 3px;

    height: 22px;

    border-radius: 4px;

    background:
        linear-gradient(
            180deg,
            #C9A45A,
            #E0A83E
        );
}


.section-subtitle {

    color: #8994A3;

    font-size: 13px;

    margin-bottom: 18px;
}


/* =========================================================
   KPI CARDS
   ========================================================= */

.kpi {

    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.065),
            rgba(255,255,255,0.018)
        );

    border:
        1px solid rgba(255,255,255,0.09);

    border-radius: 18px;

    padding: 22px;

    min-height: 125px;

    box-shadow:
        0 15px 45px rgba(0,0,0,0.22);

    transition:
        transform 0.3s ease,
        border-color 0.3s ease;
}


/* Individual KPI accents */

.kpi-gold {
    border-color: rgba(201,164,90,0.35);
}

.kpi-cyan {
    border-color: rgba(34,184,207,0.35);
}

.kpi-violet {
    border-color: rgba(155,93,229,0.35);
}

.kpi-green {
    border-color: rgba(124,179,66,0.35);
}


.kpi:hover {

    transform: translateY(-5px);

    box-shadow:
        0 20px 55px rgba(0,0,0,0.30);
}


.kpi-label {

    color: #929DAB;

    font-size: 12px;

    letter-spacing: 1.5px;

    text-transform: uppercase;
}


.kpi-value {

    color: #F5F1E8;

    font-size: 30px;

    font-weight: 700;

    margin-top: 8px;
}


/* =========================================================
   CHART CARD
   ========================================================= */

.chart-card {

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.045),
            rgba(255,255,255,0.012)
        );

    border:
        1px solid rgba(255,255,255,0.075);

    border-radius: 18px;

    padding: 8px;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {

    background:
        linear-gradient(
            135deg,
            #C9A45A,
            #E0A83E
        );

    color: #07111F;

    border: none;

    border-radius: 10px;

    font-weight: 700;

    transition: 0.25s ease;
}


.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 25px rgba(201,164,90,0.30);
}


/* =========================================================
   INPUTS
   ========================================================= */

input,
textarea {

    background-color:
        rgba(255,255,255,0.035) !important;

    color: #F5F1E8 !important;

    border:
        1px solid rgba(255,255,255,0.10) !important;
}


/* =========================================================
   SELECT BOXES
   ========================================================= */

div[data-baseweb="select"] > div {

    background-color:
        rgba(255,255,255,0.035);

    border:
        1px solid rgba(255,255,255,0.10);
}


/* =========================================================
   SLIDER
   ========================================================= */

div[data-testid="stSlider"] div[role="slider"] {

    background-color: #C9A45A !important;
}


/* =========================================================
   CHECKBOXES
   ========================================================= */

div[data-testid="stCheckbox"] label span {

    color: #F5F1E8 !important;
}


/* =========================================================
   TABS
   ========================================================= */

button[data-baseweb="tab"] {

    color: #8994A3;

    font-weight: 500;
}


button[data-baseweb="tab"][aria-selected="true"] {

    color: #C9A45A !important;

    border-bottom:
        2px solid #C9A45A;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {

    border:
        1px solid rgba(201,164,90,0.16);

    border-radius: 14px;

    overflow: hidden;
}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {

    border-color:
        rgba(201,164,90,0.15);
}


/* =========================================================
   SCROLLBAR
   ========================================================= */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #07111F;
}

::-webkit-scrollbar-thumb {

    background: #394554;

    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #C9A45A;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# COLOR SYSTEM
# ============================================================

GOLD = "#C9A45A"
AMBER = "#E0A83E"

CYAN = "#22B8CF"
BLUE = "#4D96FF"

VIOLET = "#9B5DE5"
PURPLE = "#7E57C2"

GREEN = "#7CB342"
EMERALD = "#2FBF71"

ROSE = "#D16BA5"
CORAL = "#E76F51"

IVORY = "#F5F1E8"
SLATE = "#8994A3"

DARK = "#07111F"

CHART_COLORS = [
    GOLD,
    CYAN,
    VIOLET,
    GREEN,
    ROSE,
    AMBER,
    BLUE,
    CORAL
]


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
        df = df.drop_duplicates(
            subset="job_id"
        )

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

    df["required_skills"] = df[
        "required_skills"
    ].apply(
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
        Global AI Job Market
        <br>
        <span class="gold">Intelligence</span>
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

st.sidebar.markdown(
    "## Dashboard Controls"
)

st.sidebar.markdown(
    "Filter the global job market dataset."
)

st.sidebar.divider()


# ============================================================
# FILTER OPTIONS
# ============================================================

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
    options=experience_options,
    default=experience_options
)


country_filter = st.sidebar.multiselect(
    "Country",
    options=country_options,
    default=country_options
)


industry_filter = st.sidebar.multiselect(
    "Industry",
    options=industry_options,
    default=industry_options
)


salary_min = int(
    df["salary_usd"].min()
)

salary_max = int(
    df["salary_usd"].max()
)


salary_range = st.sidebar.slider(
    "Salary Range (USD)",

    min_value=salary_min,

    max_value=salary_max,

    value=(
        salary_min,
        salary_max
    ),

    step=5000
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["experience_level"].isin(
        experience_filter
    ))
    &
    (df["company_location"].isin(
        country_filter
    ))
    &
    (df["industry"].isin(
        industry_filter
    ))
    &
    (
        df["salary_usd"].between(
            salary_range[0],
            salary_range[1]
        )
    )
].copy()


# ============================================================
# EMPTY FILTER PROTECTION
# ============================================================

if filtered_df.empty:

    st.warning(
        "No jobs match the selected filters. "
        "Please expand your filters."
    )

    st.stop()


# ============================================================
# MARKET SNAPSHOT
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Market Snapshot'
    '</div>',
    unsafe_allow_html=True
)


total_jobs = len(filtered_df)

avg_salary = (
    filtered_df["salary_usd"].mean()
)

countries = (
    filtered_df["company_location"]
    .nunique()
)

unique_skills = (
    filtered_df["required_skills"]
    .str.split(",")
    .explode()
    .str.strip()
    .nunique()
)


k1, k2, k3, k4 = st.columns(4)


with k1:

    st.markdown(
        f"""
        <div class="kpi kpi-gold">

            <div class="kpi-label">
                Total Jobs
            </div>

            <div class="kpi-value">
                {total_jobs:,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
        <div class="kpi kpi-cyan">

            <div class="kpi-label">
                Average Salary
            </div>

            <div class="kpi-value">
                ${avg_salary:,.0f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
        <div class="kpi kpi-violet">

            <div class="kpi-label">
                Countries
            </div>

            <div class="kpi-value">
                {countries}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
        <div class="kpi kpi-green">

            <div class="kpi-label">
                Skills Identified
            </div>

            <div class="kpi-value">
                {unique_skills}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PLOTLY GLOBAL THEME
# ============================================================

plot_layout = dict(

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        family="Inter, sans-serif",
        color=IVORY
    ),

    title=dict(
        font=dict(
            color=IVORY,
            size=16
        ),

        x=0.02
    ),

    margin=dict(
        l=35,
        r=30,
        t=55,
        b=45
    ),

    hoverlabel=dict(
        bgcolor="#101B2A",

        bordercolor=GOLD,

        font=dict(
            color=IVORY
        )
    ),

    xaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",

        zerolinecolor=
            "rgba(255,255,255,0.08)",

        tickfont=dict(
            color=SLATE
        ),

        title_font=dict(
            color=SLATE
        )
    ),

    yaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",

        zerolinecolor=
            "rgba(255,255,255,0.08)",

        tickfont=dict(
            color=SLATE
        ),

        title_font=dict(
            color=SLATE
        )
    )
)


# ============================================================
# SKILLS INTELLIGENCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Skills Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Most frequently requested technical skills '
    'across filtered job postings.'
    '</div>',
    unsafe_allow_html=True
)


skills = (
    filtered_df[
        "required_skills"
    ]
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

        textposition="outside",

        marker=dict(

            color=GOLD,

            line=dict(
                color="#E8C878",
                width=1
            )
        ),

        hovertemplate=
            "<b>%{y}</b><br>"
            "Job Count: %{x:,}"
            "<extra></extra>"
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
# EXPERIENCE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Experience & Salary'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# JOB DISTRIBUTION BY EXPERIENCE
# ============================================================

with col1:

    experience_counts = (
        filtered_df[
            "experience_level"
        ]
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

        title=
            "Job Distribution by Experience",

        color="Experience",

        color_discrete_sequence=[
            CYAN,
            GOLD,
            VIOLET,
            GREEN,
            ROSE
        ]
    )


    fig_exp.update_layout(
        **plot_layout,
        showlegend=False
    )


    st.plotly_chart(
        fig_exp,
        use_container_width=True
    )


# ============================================================
# AVERAGE SALARY BY EXPERIENCE
# ============================================================

with col2:

    salary_exp = (
        filtered_df
        .groupby(
            "experience_level"
        )["salary_usd"]
        .mean()
        .reset_index()
    )


    fig_salary = px.bar(

        salary_exp,

        x="experience_level",

        y="salary_usd",

        title=
            "Average Salary by Experience",

        text_auto=".2s",

        color=
            "experience_level",

        color_discrete_sequence=[
            CYAN,
            GOLD,
            VIOLET,
            GREEN,
            ROSE
        ]
    )


    fig_salary.update_layout(

        **plot_layout,

        showlegend=False,

        yaxis_title=
            "Salary (USD)",

        xaxis_title=
            "Experience"
    )


    st.plotly_chart(
        fig_salary,
        use_container_width=True
    )


# ============================================================
# GLOBAL HIRING INTELLIGENCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Global Hiring Intelligence'
    '</div>',
    unsafe_allow_html=True
)


col3, col4 = st.columns(2)


# ============================================================
# TOP COUNTRIES
# ============================================================

with col3:

    top_countries = (
        filtered_df[
            "company_location"
        ]
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

        title=
            "Top Hiring Countries"
    )


    fig_country.update_traces(

        marker=dict(
            color=CYAN,

            line=dict(
                color="#5AD9E8",
                width=1
            )
        )
    )


    fig_country.update_layout(

        **plot_layout,

        yaxis=dict(
            categoryorder=
                "total ascending"
        )
    )


    st.plotly_chart(
        fig_country,
        use_container_width=True
    )


# ============================================================
# SALARY BY COUNTRY
# ============================================================

with col4:

    country_salary = (
        filtered_df
        .groupby(
            "company_location"
        )["salary_usd"]
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

        title=
            "Highest Average Salaries by Country",

        text_auto=".2s"
    )


    fig_country_salary.update_traces(

        marker=dict(

            color=BLUE,

            line=dict(
                color="#75AEFF",
                width=1
            )
        )
    )


    fig_country_salary.update_layout(

        **plot_layout,

        yaxis=dict(
            categoryorder=
                "total ascending"
        ),

        xaxis_title=
            "Salary (USD)"
    )


    st.plotly_chart(
        fig_country_salary,
        use_container_width=True
    )


# ============================================================
# INDUSTRY INTELLIGENCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Industry Intelligence'
    '</div>',
    unsafe_allow_html=True
)


industry_counts = (
    filtered_df[
        "industry"
    ]
    .value_counts()
    .reset_index()
)


industry_counts.columns = [
    "Industry",
    "Jobs"
]


fig_industry = px.pie(

    industry_counts,

    names="Industry",

    values="Jobs",

    hole=0.58,

    title=
        "Job Distribution by Industry",

    color_discrete_sequence=[
        CYAN,
        GOLD,
        VIOLET,
        GREEN,
        ROSE,
        AMBER,
        BLUE,
        CORAL
    ]
)


fig_industry.update_traces(

    textposition="inside",

    textinfo=
        "percent+label",

    marker=dict(

        line=dict(
            color=DARK,
            width=2
        )
    )
)


fig_industry.update_layout(

    **plot_layout,

    legend=dict(

        font=dict(
            color=IVORY
        )
    )
)


st.plotly_chart(
    fig_industry,
    use_container_width=True
)


# ============================================================
# SALARY INTELLIGENCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Salary Intelligence'
    '</div>',
    unsafe_allow_html=True
)


col5, col6 = st.columns(2)


# ============================================================
# SALARY DISTRIBUTION
# ============================================================

with col5:

    fig_hist = px.histogram(

        filtered_df,

        x="salary_usd",

        nbins=30,

        title=
            "Global Salary Distribution"
    )


    fig_hist.update_traces(

        marker=dict(

            color=GOLD,

            line=dict(
                color=AMBER,
                width=1
            )
        )
    )


    fig_hist.update_layout(

        **plot_layout,

        xaxis_title=
            "Salary (USD)",

        yaxis_title=
            "Number of Jobs"
    )


    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )


# ============================================================
# SALARY BY EXPERIENCE BOX PLOT
# ============================================================

with col6:

    fig_box = px.box(

        filtered_df,

        x="experience_level",

        y="salary_usd",

        title=
            "Salary Distribution by Experience"
    )


    fig_box.update_traces(

        marker=dict(
            color=ROSE,

            line=dict(
                color=ROSE
            )
        ),

        line=dict(
            color=ROSE
        )
    )


    fig_box.update_layout(

        **plot_layout,

        yaxis_title=
            "Salary (USD)",

        xaxis_title=
            "Experience"
    )


    st.plotly_chart(
        fig_box,
        use_container_width=True
    )


# ============================================================
# COMPANY SIZE INTELLIGENCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Company Size Intelligence'
    '</div>',
    unsafe_allow_html=True
)


company_salary = (
    filtered_df
    .groupby(
        "company_size"
    )["salary_usd"]
    .mean()
    .reset_index()
)


fig_company = go.Figure()


fig_company.add_trace(

    go.Scatter(

        x=company_salary[
            "company_size"
        ],

        y=company_salary[
            "salary_usd"
        ],

        mode=
            "lines+markers+text",

        text=[
            f"${v/1000:.0f}K"
            for v in company_salary[
                "salary_usd"
            ]
        ],

        textposition=
            "top center",

        line=dict(

            color=GOLD,

            width=3
        ),

        marker=dict(

            color=AMBER,

            size=9,

            line=dict(

                color=IVORY,

                width=1
            )
        ),

        fill="tozeroy",

        fillcolor=
            "rgba(201,164,90,0.10)",

        hovertemplate=
            "<b>%{x}</b><br>"
            "Average Salary: "
            "$%{y:,.0f}"
            "<extra></extra>"
    )
)


fig_company.update_layout(

    **plot_layout,

    title=
        "Average Salary by Company Size",

    xaxis_title=
        "Company Size",

    yaxis_title=
        "Salary (USD)"
)


st.plotly_chart(
    fig_company,
    use_container_width=True
)


# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">'
    'Data Explorer'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-subtitle">'
    'Search and explore the filtered job-market dataset.'
    '</div>',
    unsafe_allow_html=True
)


search = st.text_input(

    "Search job records",

    placeholder=
        "Search by job title, company, country, skill..."
)


display_df = filtered_df.copy()


# ============================================================
# SEARCH
# ============================================================

if search:

    search_mask = (
        display_df
        .astype(str)
        .apply(

            lambda row:
                row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),

            axis=1
        )
    )

    display_df = display_df[
        search_mask
    ]


# ============================================================
# DATA TABLE
# ============================================================

st.dataframe(

    display_df,

    use_container_width=True,

    height=450
)


# ============================================================
# DOWNLOAD DATA
# ============================================================

csv_data = display_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(

    label="⬇ Download Filtered Data",

    data=csv_data,

    file_name=
        "global_ai_job_market_filtered.csv",

    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


st.markdown(
    """
    <div style="
        text-align:center;
        color:#778291;
        font-size:12px;
        padding:25px;
    ">

        <div style="
            color:#C9A45A;
            font-weight:600;
            letter-spacing:1px;
        ">
            GLOBAL AI JOB MARKET INTELLIGENCE
        </div>

        <br>

        Built with
        <span style="color:#22B8CF;">Python</span>
        •
        <span style="color:#7CB342;">Pandas</span>
        •
        <span style="color:#9B5DE5;">Plotly</span>
        •
        <span style="color:#D16BA5;">Streamlit</span>

        <br><br>

        Data Science Portfolio Project

    </div>
    """,
    unsafe_allow_html=True
)
