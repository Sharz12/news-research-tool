import streamlit as st

from src.pipeline.research import ResearchPipeline

st.set_page_config(
    page_title= "News Research Tool",
    page_icon= "📰",
    layout= "wide",
)


st.title("📰 News Research Tool")

st.write(
    "Enter a company, market, or business topic to retrieve"
    "recent news and generate an  AI-powered research summary"
)


query= st.text_input(
    "Research Query",
    placeholder= "e.g., Nvidia AI, Tesla earnings, Indian banking sector.",
)


col1, col2 = st.columns(2)

with col1:
    page_size = st.slider(
        "Number of articles",
        min_value= 1,
        max_value= 20,
        value= 10,
    )

with col2:
    days_back = st.slider(
        "News from the last(days)",
        min_value= 1,
        max_value= 30,
        value= 7,
    )

if st.button("🔍 Research News", type="primary"):
    if not query.strip():
        st.warning("Please enter research query.")
    else:
        with st.spinner("Searching News and generating recent summary..."):
            try:
                pipeline = ResearchPipeline()

                result = pipeline.research(
                    query= query,
                    page_size= page_size,
                    days_back=days_back,
                )

                st.subheader("📊 Research Summary")
                st.write(result.summary)

                st.subheader("📰 Sources")

                if result.articles:
                    for index, article in enumerate(
                        result.articles,
                        start=1,
                    ):
                        with st.expander(
                            f"{index}.{article.title}"
                        ):
                            st.write(
                                f"**Source:** {article.source_name}"
                            )

                            st.write(
                                f"**Published:** "
                                f"{article.published_at}"
                            )

                            if article.description:
                                st.write(
                                    f"**Description:** "
                                    f"{article.description}"
                                )

                            st.write(
                                f"**URL:** {article.url}"
                            )

                    else:
                        st.info("No relevant news articles were found.")

            except Exception as exc:
                st.error(
                    "Something went wrong while researching the news."
                    "Please try again or use a different research query."
                )