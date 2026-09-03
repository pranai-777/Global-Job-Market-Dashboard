import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Global AI Job Market Intelligence",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# COLORS
# ============================================================

GOLD = "#C9A45A"
AMBER = "#E0A83E"
CYAN = "#22B8CF"
BLUE = "#4D96FF"
VIOLET = "#9B5DE5"
GREEN = "#7CB342"
ROSE = "#D16BA5"
CORAL = "#E76F51"

DARK = "#07111F"
CARD = "#101B2A"
TEXT = "#F5F1E8"
MUTED = "#9AA6B5"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* MAIN BACKGROUND */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(201,164,90,0.08),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(34,184,207,0.05),
                transparent 25%
            ),
            #07111F;
        color: #F5F1E8;
    }

    /* MAIN CONTENT */
    .block-container {
        max-width: 1500px;
        padding-top: 30px;
        padding-bottom: 40px;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #091522;
        border-right: 1px solid rgba(201,164,90,0.20);
    }

    section[data-testid="stSidebar"] * {
        color: #F5F1E8;
    }

    /* HERO */
    .hero {
        background:
            linear-gradient(
                135deg,
                rgba(201,164,90,0.13),
                rgba(16,27,42,0.96)
            );

        border: 1px solid rgba(201,164,90,0.28);

        border-radius: 22px;

        padding: 35px 40px;

        margin-bottom: 25px;

        box-shadow:
            0 20px 60px rgba(0,0,0,0.30);
    }

    .hero-label {
        color: #C9A45A;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #F5F1E8;
        font-size: 45px;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 12px;
    }

    .hero-title span {
        color: #C9A45A;
    }

    .hero-text {
        color: #AEB7C3;
        font-size: 15px;
        line-height: 1.6;
        max-width: 750px;
    }

    /* SECTION TITLE */
    .section-title {
        color: #F5F1E8;
        font-size: 21px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 12px;
        border-left: 3px solid #C9A45A;
        padding-left: 10px;
    }

    /* KPI CARD */
    .kpi {
        background: #101B2A;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        min-height: 110px;
    }

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

    .kpi-label {
        color: #8994A3;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .kpi-value {
        color: #F5F1E8;
        font-size: 29px;
        font-weight: 700;
        margin-top: 8px;
    }

    /* FOOTER */
    .footer {
        text-align: center;
        color: #8994A3;
        font-size: 12px;
        padding: 25px;
    }

    .footer-title {
        color: #C9A45A;
        font-weight: 600;
        letter-spacing: 1px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df1 = pd.read_csv("ai_job_dataset.csv")

    df2 = pd.read_csv("ai_job_dataset1.csv")

    df = pd.concat(
        [df1, df2],
        ignore_index=True
    )

    # Remove duplicate jobs
    if "job_id" in df.columns:
        df = df.drop_duplicates(
            subset="job_id"
        )

    # Salary
    if "salary_usd" in df.columns:
        df["salary_usd"] = pd.to_numeric(
            df["salary_usd"],
            errors="coerce"
        )

    # Skills
    if "required_skills" in df.columns:
        df["required_skills"] = (
            df["required_skills"]
            .fillna("Unknown")
            .astype(str)
        )

    return df


# ============================================================
# RUN DATA LOADING
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        "Unable to load the CSV files."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "salary_usd",
    "experience_level",
    "company_location",
    "required_skills",
    "industry",
    "company_size"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "The following required columns are missing:"
    )

    st.write(missing_columns)

    st.stop()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """<div class="hero">
<div class="hero-label">DATA SCIENCE • AI • LABOR MARKET ANALYTICS</div>
<div class="hero-title">Global AI Job Market<br><span>Intelligence</span></div>
<div class="hero-text">Interactive analysis of global AI employment, salary trends, hiring demand, industries, and technical skills across the 2025 job market.</div>
</div>""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙ Dashboard Controls")

st.sidebar.write(
    "Filter the global AI job market."
)

st.sidebar.divider()


# EXPERIENCE

experience_options = sorted(
    df["experience_level"]
    .dropna()
    .unique()
    .tolist()
)

selected_experience = st.sidebar.multiselect(
    "Experience Level",
    experience_options,
    default=experience_options
)


# COUNTRY

country_options = sorted(
    df["company_location"]
    .dropna()
    .unique()
    .tolist()
)

selected_countries = st.sidebar.multiselect(
    "Country",
    country_options,
    default=country_options
)


# INDUSTRY

industry_options = sorted(
    df["industry"]
    .dropna()
    .unique()
    .tolist()
)

selected_industries = st.sidebar.multiselect(
    "Industry",
    industry_options,
    default=industry_options
)


# SALARY

salary_min = int(
    df["salary_usd"].min()
)

salary_max = int(
    df["salary_usd"].max()
)

selected_salary = st.sidebar.slider(
    "Salary Range (USD)",
    min_value=salary_min,
    max_value=salary_max,
    value=(salary_min, salary_max),
    step=5000
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df["experience_level"].isin(
        selected_experience
    )
    &
    df["company_location"].isin(
        selected_countries
    )
    &
    df["industry"].isin(
        selected_industries
    )
    &
    df["salary_usd"].between(
        selected_salary[0],
        selected_salary[1]
    )
].copy()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No jobs match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_jobs = len(filtered_df)

average_salary = filtered_df[
    "salary_usd"
].mean()

total_countries = filtered_df[
    "company_location"
].nunique()

total_industries = filtered_df[
    "industry"
].nunique()


# ============================================================
# MARKET SNAPSHOT
# ============================================================

st.markdown(
    '<div class="section-title">Market Snapshot</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(4)


with k1:
    st.markdown(
        f"""<div class="kpi kpi-gold">
<div class="kpi-label">TOTAL JOBS</div>
<div class="kpi-value">{total_jobs:,}</div>
</div>""",
        unsafe_allow_html=True
    )


with k2:
    st.markdown(
        f"""<div class="kpi kpi-cyan">
<div class="kpi-label">AVERAGE SALARY</div>
<div class="kpi-value">${average_salary:,.0f}</div>
</div>""",
        unsafe_allow_html=True
    )


with k3:
    st.markdown(
        f"""<div class="kpi kpi-violet">
<div class="kpi-label">COUNTRIES</div>
<div class="kpi-value">{total_countries}</div>
</div>""",
        unsafe_allow_html=True
    )


with k4:
    st.markdown(
        f"""<div class="kpi kpi-green">
<div class="kpi-label">INDUSTRIES</div>
<div class="kpi-value">{total_industries}</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# PLOTLY COMMON SETTINGS
# ============================================================

common_layout = dict(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color=TEXT
    ),

    margin=dict(
        l=40,
        r=30,
        t=55,
        b=45
    ),

    xaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.06)"
    ),

    yaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.06)"
    )
)


# ============================================================
# SKILLS
# ============================================================

st.markdown(
    '<div class="section-title">Skills Intelligence</div>',
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
    .head(10)
    .sort_values()
)


skills_df = pd.DataFrame({
    "Skill": top_skills.index,
    "Jobs": top_skills.values
})


fig_skills = px.bar(
    skills_df,
    x="Jobs",
    y="Skill",
    orientation="h",
    title="Top 10 In-Demand Skills"
)


fig_skills.update_traces(
    marker_color=GOLD
)


fig_skills.update_layout(
    **common_layout,
    title_font_color=TEXT,
    xaxis_title="Job Count",
    yaxis_title=""
)


st.plotly_chart(
    fig_skills,
    use_container_width=True
)


# ============================================================
# EXPERIENCE SECTION
# ============================================================

st.markdown(
    '<div class="section-title">Experience & Salary</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# EXPERIENCE DISTRIBUTION
# ============================================================

with col1:

    experience_df = (
        filtered_df[
            "experience_level"
        ]
        .value_counts()
        .reset_index()
    )

    experience_df.columns = [
        "Experience",
        "Jobs"
    ]


    fig_experience = px.bar(

        experience_df,

        x="Experience",

        y="Jobs",

        color="Experience",

        title="Job Distribution by Experience",

        color_discrete_sequence=[
            CYAN,
            GOLD,
            VIOLET,
            GREEN
        ]
    )


    fig_experience.update_layout(
        **common_layout,
        showlegend=False
    )


    st.plotly_chart(
        fig_experience,
        use_container_width=True
    )


# ============================================================
# SALARY BY EXPERIENCE
# ============================================================

with col2:

    salary_experience = (
        filtered_df
        .groupby(
            "experience_level"
        )["salary_usd"]
        .mean()
        .reset_index()
    )


    fig_salary_experience = px.bar(

        salary_experience,

        x="experience_level",

        y="salary_usd",

        color="experience_level",

        title="Average Salary by Experience",

        text_auto=".2s",

        color_discrete_sequence=[
            CYAN,
            GOLD,
            VIOLET,
            GREEN
        ]
    )


    fig_salary_experience.update_layout(
        **common_layout,
        showlegend=False,
        xaxis_title="Experience",
        yaxis_title="Salary (USD)"
    )


    st.plotly_chart(
        fig_salary_experience,
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


# ============================================================
# TOP COUNTRIES
# ============================================================

# ============================================================
# TOP COUNTRIES
# ============================================================

with col3:

    country_jobs = (
        filtered_df["company_location"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    country_jobs.columns = [
        "Country",
        "Jobs"
    ]

    fig_countries = px.bar(
        country_jobs,
        x="Jobs",
        y="Country",
        orientation="h",
        title="Top Hiring Countries"
    )

    fig_countries.update_traces(
        marker_color=CYAN
    )

    fig_countries.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
        margin=dict(
            l=40,
            r=30,
            t=55,
            b=45
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.06)"
        ),
        yaxis=dict(
            categoryorder="total ascending",
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.06)"
        )
    )

    st.plotly_chart(
        fig_countries,
        use_container_width=True
    )



# ============================================================
# SALARY BY COUNTRY
# ============================================================

with col4:

    country_salary = (
        filtered_df
        .groupby("company_location")["salary_usd"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_country_salary = px.bar(
        country_salary,
        x="salary_usd",
        y="company_location",
        orientation="h",
        title="Average Salary by Country",
        text_auto=".2s"
    )

    fig_country_salary.update_traces(
        marker_color=BLUE
    )

    fig_country_salary.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT),
        margin=dict(
            l=40,
            r=30,
            t=55,
            b=45
        ),
        xaxis=dict(
            title="Salary (USD)",
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.06)"
        ),
        yaxis=dict(
            categoryorder="total ascending",
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.06)"
        )
    )

    st.plotly_chart(
        fig_country_salary,
        use_container_width=True
    )


# ============================================================
# INDUSTRY
# ============================================================

st.markdown(
    '<div class="section-title">Industry Intelligence</div>',
    unsafe_allow_html=True
)


industry_df = (
    filtered_df[
        "industry"
    ]
    .value_counts()
    .reset_index()
)


industry_df.columns = [
    "Industry",
    "Jobs"
]


fig_industry = px.pie(

    industry_df,

    names="Industry",

    values="Jobs",

    hole=0.55,

    title="Job Distribution by Industry",

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


fig_industry.update_layout(
    **common_layout
)


st.plotly_chart(
    fig_industry,
    use_container_width=True
)


# ============================================================
# SALARY ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Salary Intelligence</div>',
    unsafe_allow_html=True
)


col5, col6 = st.columns(2)


# ============================================================
# SALARY HISTOGRAM
# ============================================================

with col5:

    fig_histogram = px.histogram(

        filtered_df,

        x="salary_usd",

        nbins=30,

        title="Global Salary Distribution"
    )


    fig_histogram.update_traces(
        marker_color=GOLD
    )


    fig_histogram.update_layout(

        **common_layout,

        xaxis_title="Salary (USD)",

        yaxis_title="Job Count"
    )


    st.plotly_chart(
        fig_histogram,
        use_container_width=True
    )


# ============================================================
# SALARY BOXPLOT
# ============================================================

with col6:

    fig_box = px.box(

        filtered_df,

        x="experience_level",

        y="salary_usd",

        color="experience_level",

        title="Salary Distribution by Experience",

        color_discrete_sequence=[
            CYAN,
            GOLD,
            VIOLET,
            GREEN
        ]
    )


    fig_box.update_layout(

        **common_layout,

        showlegend=False,

        xaxis_title="Experience",

        yaxis_title="Salary (USD)"
    )


    st.plotly_chart(
        fig_box,
        use_container_width=True
    )


# ============================================================
# COMPANY SIZE
# ============================================================

st.markdown(
    '<div class="section-title">Company Size Intelligence</div>',
    unsafe_allow_html=True
)


company_size_df = (
    filtered_df
    .groupby(
        "company_size"
    )["salary_usd"]
    .mean()
    .reset_index()
)


fig_company = px.line(

    company_size_df,

    x="company_size",

    y="salary_usd",

    markers=True,

    title="Average Salary by Company Size"
)


fig_company.update_traces(

    line=dict(
        color=GOLD,
        width=3
    ),

    marker=dict(
        color=AMBER,
        size=9
    )
)


fig_company.update_layout(

    **common_layout,

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


search = st.text_input(
    "Search jobs",
    placeholder=
    "Search job title, company, country, skill..."
)


display_df = filtered_df.copy()


if search:

    mask = (
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
        mask
    ]


st.dataframe(
    display_df,
    use_container_width=True,
    height=400
)


# ============================================================
# DOWNLOAD
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

st.markdown(
    """
    <div class="footer">

        <div class="footer-title">
            GLOBAL AI JOB MARKET INTELLIGENCE
        </div>

        <br>

        Built with
        Python • Pandas • Plotly • Streamlit

        <br><br>

        Data Science Portfolio Project

    </div>
    """,
    unsafe_allow_html=True
)
