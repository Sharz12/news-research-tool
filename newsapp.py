import html

import streamlit as st

from src.pipeline.research import ResearchPipeline


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="News Research Tool",
    page_icon="📰",
    layout="wide",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

    /* =====================================================
       GLOBAL APP
       ===================================================== */

    .stApp {
        background: #07111f;
        color: #e8eef7;
    }

    [data-testid="stAppViewContainer"] {
        background: #07111f;
    }

    [data-testid="stHeader"] {
        background: #07111f;
    }

    [data-testid="stToolbar"] {
        background: transparent;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       GENERAL TEXT
       ===================================================== */

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #cbd7e6;
    }

    [data-testid="stMarkdownContainer"] strong {
        color: #f8fafc;
    }

    h1,
    h2,
    h3,
    h4 {
        color: #f8fafc !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #8fa3bb !important;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero-box {
        background: #0d1b2e;
        border: 1px solid #1d3654;
        border-radius: 24px;
        padding: 42px 46px;
        margin-bottom: 30px;
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.25);
    }

    .hero-badge {
        display: inline-block;
        background: #122b46;
        color: #6ed6ff;
        border: 1px solid #24547a;
        border-radius: 999px;
        padding: 7px 14px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 18px;
    }

    .hero-title {
        color: #f8fafc;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 14px;
    }

    .hero-subtitle {
        color: #9fb1c7;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 850px;
    }


    /* =====================================================
       SECTION LABEL
       ===================================================== */

    .section-label {
        color: #6ed6ff;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 12px;
        margin-bottom: 12px;
    }


    /* =====================================================
       SEARCH INPUT
       ===================================================== */

    div[data-testid="stTextInput"] input {
        background: #0d1b2e;
        color: #f8fafc;
        border: 1px solid #29435f;
        border-radius: 12px;
        min-height: 48px;
        font-size: 1rem;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #4fc3f7;
        box-shadow: 0 0 0 1px #4fc3f7;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #70859e;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        background: #10243a;
        color: #dcecff;
        border: 1px solid #294b6b;
        border-radius: 10px;
        font-weight: 650;
        min-height: 44px;
    }

    .stButton > button:hover {
        background: #16324e;
        color: #ffffff;
        border-color: #4fc3f7;
    }

    .stButton > button[kind="primary"] {
        background: #1b8ac4;
        color: #ffffff;
        border: 1px solid #35a9e8;
        font-weight: 750;
    }

    .stButton > button[kind="primary"]:hover {
        background: #229bd8;
        border-color: #6ed6ff;
    }


    /* =====================================================
       SELECTBOX
       ===================================================== */

    div[data-baseweb="select"] > div {
        background: #0d1b2e;
        border-color: #29435f;
        color: #f8fafc;
        border-radius: 10px;
    }

    div[data-baseweb="select"] span {
        color: #e8eef7;
    }


    /* =====================================================
       SLIDER
       ===================================================== */

    [data-testid="stSlider"] {
        color: #6ed6ff;
    }


    /* =====================================================
       EXPANDER
       ===================================================== */

    [data-testid="stExpander"] {
        background: #0b1727;
        border: 1px solid #1e344d;
        border-radius: 14px;
    }

    [data-testid="stExpander"] summary {
        color: #dce7f4;
    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    .metric-card {
        background: #0d1b2e;
        border: 1px solid #1d3654;
        border-radius: 16px;
        padding: 20px;
        min-height: 105px;
    }

    .metric-label {
        color: #8298b0;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 800;
        line-height: 1.25;
    }


    /* =====================================================
       SUMMARY HEADER
       ===================================================== */

    .summary-card {
        background: #0d1b2e;
        border: 1px solid #24547a;
        border-left: 4px solid #4fc3f7;
        border-radius: 16px;
        padding: 24px 26px;
        margin-top: 24px;
        margin-bottom: 18px;
    }

    .summary-label {
        color: #6ed6ff;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }

    .summary-title {
        color: #f8fafc;
        font-size: 1.35rem;
        font-weight: 800;
    }


    /* =====================================================
       AI RESEARCH OUTPUT
       ===================================================== */

    .research-output {
        color: #cbd7e6;
        font-size: 0.95rem;
        line-height: 1.75;
        margin-top: 8px;
        overflow-wrap: anywhere;
        word-break: normal;
    }

    .research-section-title {
        color: #f8fafc;
        font-size: 1.05rem;
        font-weight: 800;
        margin-top: 24px;
        margin-bottom: 8px;
    }

    .research-body {
        color: #cbd7e6;
        margin-bottom: 12px;
    }

    .research-list-item {
        color: #cbd7e6;
        margin-bottom: 10px;
        padding-left: 4px;
    }

    .research-label {
        color: #f8fafc;
        font-weight: 750;
    }


    /* =====================================================
       NEWS CARDS
       ===================================================== */

    .news-card {
        background: #0c1929;
        border: 1px solid #1d344d;
        border-radius: 14px;
        padding: 20px 22px;
        margin-top: 16px;
        margin-bottom: 6px;
    }

    .news-meta {
        color: #8196ad;
        font-size: 0.78rem;
        margin-bottom: 10px;
    }

    .source-badge {
        display: inline-block;
        background: #122b46;
        color: #70d7ff;
        border: 1px solid #24547a;
        border-radius: 999px;
        padding: 4px 9px;
        font-weight: 700;
    }

    .news-title {
        color: #f4f8fc;
        font-size: 1.05rem;
        font-weight: 750;
        line-height: 1.45;
        margin-bottom: 9px;
    }

    .news-description {
        color: #9eb0c4;
        font-size: 0.92rem;
        line-height: 1.6;
    }


    /* =====================================================
       EMPTY STATE
       ===================================================== */

    .empty-state {
        background: #0d1b2e;
        border: 1px solid #1d3654;
        border-radius: 18px;
        padding: 42px;
        text-align: center;
        margin-top: 25px;
    }

    .empty-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }

    .empty-title {
        color: #f8fafc;
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .empty-text {
        color: #94a8be;
        line-height: 1.7;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    .soft-divider {
        height: 1px;
        background: #1b3047;
        margin: 32px 0 26px 0;
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        color: #60758c;
        text-align: center;
        font-size: 0.78rem;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #172a40;
    }

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HERO SECTION
# =========================================================

st.html(
    """
<div class="hero-box">

    <div class="hero-badge">
        ✨ AI-POWERED RESEARCH
    </div>

    <div class="hero-title">
        📰 News Research Tool
    </div>

    <div class="hero-subtitle">
        Turn news into focused research intelligence.
        Search companies, markets, sectors, and business topics,
        then let AI identify the most important developments
        and potential implications.
    </div>

</div>
"""
)


# =========================================================
# SEARCH SECTION
# =========================================================

st.html(
    """
<div class="section-label">
    Start your research
</div>
"""
)


search_col, button_col = st.columns(
    [5, 1],
    vertical_alignment="bottom",
)


with search_col:

    query = st.text_input(
        "Research Query",
        placeholder=(
            "Search a company, market, sector, "
            "or business topic..."
        ),
        label_visibility="collapsed",
    )


with button_col:

    research_clicked = st.button(
        "🔎 Research",
        type="primary",
        use_container_width=True,
    )


# =========================================================
# SUGGESTED SEARCHES
# =========================================================

st.caption(
    "Popular research topics"
)


suggestion_cols = st.columns(4)


suggestions = [
    "Tesla",
    "Nvidia AI",
    "Apple",
    "Indian banking",
]


for column, suggestion in zip(
    suggestion_cols,
    suggestions,
):

    with column:

        if st.button(
            suggestion,
            use_container_width=True,
            key=f"suggestion_{suggestion}",
        ):

            query = suggestion
            research_clicked = True


# =========================================================
# RESEARCH SETTINGS
# =========================================================

with st.expander(
    "⚙️ Research Settings",
    expanded=False,
):

    settings_col1, settings_col2 = st.columns(2)


    with settings_col1:

        max_articles = st.slider(
            "Articles to analyze",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
        )

        page_size = 20


    with settings_col2:

        research_period = st.selectbox(
            "Research period",
            options=[
                "All available history",
                "Last 24 hours",
                "Last 7 days",
                "Last 30 days",
            ],
            index=0,
        )


    if research_period == "All available history":

        days_back = None
        period_label = "All available history"


    elif research_period == "Last 24 hours":

        days_back = 1
        period_label = "Last 24 hours"


    elif research_period == "Last 7 days":

        days_back = 7
        period_label = "Last 7 days"


    else:

        days_back = 30
        period_label = "Last 30 days"


    if days_back is None:

        st.caption(
            "No application-level date filter is applied. "
            "NewsAPI will search the historical range "
            "available under your API plan."
        )


    else:

        st.caption(
            f"Search for relevant news from the "
            f"{period_label.lower()}."
        )


# =========================================================
# RESEARCH EXECUTION
# =========================================================

if research_clicked:

    if not query or not query.strip():

        st.warning(
            "Please enter a company, market, or topic "
            "to begin your research."
        )


    else:

        with st.spinner(
            "🔎 Searching news → "
            "🧠 analyzing articles → "
            "✨ generating insights..."
        ):

            try:

                pipeline = ResearchPipeline()


                result = pipeline.research(
                    query=query,
                    page_size=page_size,
                    days_back=days_back,
                    max_articles=max_articles,
                )


                # =================================================
                # NO RESULTS
                # =================================================

                if not result.articles:

                    escaped_query = html.escape(
                        result.query
                    )

                    escaped_period = html.escape(
                        period_label
                    )

                    st.html(
                        f"""
<div class="empty-state">

    <div class="empty-icon">
        🔎
    </div>

    <div class="empty-title">
        No relevant news found
    </div>

    <div class="empty-text">
        We couldn't find relevant coverage for
        <strong>{escaped_query}</strong>
        under the selected research period:

        <strong>{escaped_period}</strong>.

        <br><br>

        Try a broader search term, another company,
        or a different research period.
    </div>

</div>
"""
                    )


                # =================================================
                # RESULTS
                # =================================================

                else:

                    st.html(
                        """
<div class="soft-divider"></div>

<div class="section-label">
    Research results
</div>
"""
                    )


                    escaped_query = html.escape(
                        result.query
                    )


                    st.markdown(
                        f'## Insights for "{escaped_query}"'
                    )


                    unique_sources = len(
                        {
                            article.source_name
                            for article in result.articles
                        }
                    )


                    # =================================================
                    # METRICS
                    # =================================================

                    (
                        metric_col1,
                        metric_col2,
                        metric_col3,
                    ) = st.columns(3)


                    with metric_col1:

                        st.html(
                            f"""
<div class="metric-card">

    <div class="metric-label">
        Articles analyzed
    </div>

    <div class="metric-value">
        {len(result.articles)}
    </div>

</div>
"""
                        )


                    with metric_col2:

                        st.html(
                            f"""
<div class="metric-card">

    <div class="metric-label">
        Sources
    </div>

    <div class="metric-value">
        {unique_sources}
    </div>

</div>
"""
                        )


                    with metric_col3:

                        st.html(
                            f"""
<div class="metric-card">

    <div class="metric-label">
        Research period
    </div>

    <div class="metric-value">
        {html.escape(period_label)}
    </div>

</div>
"""
                        )


                    # =================================================
                    # AI SUMMARY HEADER
                    # =================================================

                    st.html(
                        """
<div class="summary-card">

    <div class="summary-label">
        AI Research Summary
    </div>

    <div class="summary-title">
        🧠 Key Intelligence
    </div>

</div>
"""
                    )


                    # =================================================
                    # AI SUMMARY
                    #
                    # IMPORTANT:
                    # We use st.html + html.escape here.
                    # The LLM output is therefore treated as
                    # plain text and cannot be interpreted as
                    # Markdown by Streamlit.
                    # =================================================

                    safe_summary = html.escape(
                        result.summary
                    )

                    safe_summary = safe_summary.replace(
                        "\r\n",
                        "\n",
                    )

                    safe_summary = safe_summary.replace(
                        "\r",
                        "\n",
                    )

                    safe_summary = safe_summary.replace(
                        "\n\n",
                        "<br><br>",
                    )

                    safe_summary = safe_summary.replace(
                        "\n",
                        "<br>",
                    )

                    st.html(
                        f"""
<div class="research-output">
    {safe_summary}
</div>
"""
                    )


                    # =================================================
                    # NEWS COVERAGE
                    # =================================================

                    st.html(
                        """
<div class="soft-divider"></div>

<div class="section-label">
    News coverage
</div>
"""
                    )


                    st.markdown(
                        "## 🗞️ Sources"
                    )


                    for index, article in enumerate(
                        result.articles,
                        start=1,
                    ):

                        title = html.escape(
                            article.title
                        )


                        source = html.escape(
                            article.source_name
                        )


                        description = html.escape(
                            article.description
                            or "No description available."
                        )


                        published = (
                            article.published_at.strftime(
                                "%d %b %Y, %H:%M"
                            )
                        )


                        st.html(
                            f"""
<div class="news-card">

    <div class="news-meta">

        <span class="source-badge">
            {source}
        </span>

        &nbsp; • &nbsp;

        {published}

    </div>

    <div class="news-title">
        {index}. {title}
    </div>

    <div class="news-description">
        {description}
    </div>

</div>
"""
                        )


                        st.link_button(
                            "Read full article →",
                            str(article.url),
                        )


            except Exception as exc:

                st.error(
                    "Something went wrong while researching "
                    "the news."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.exception(exc)


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
<div class="footer">

    News Research Tool
    · NewsAPI
    · LangChain
    · Groq

</div>
"""
)