# 📰 News Research Tool

An AI-powered news research application that retrieves news articles for a user-defined topic and generates a structured research summary using a Groq-hosted LLM.

The application combines real-world news retrieval, article validation, text processing, AI-powered research analysis, multilingual output, visual news coverage, related research recommendations, and downloadable research reports in an interactive Streamlit interface.

---

## 🚀 Features

- 🔎 Search news using NewsAPI
- 🧠 Generate structured AI research summaries using Groq
- 🔗 LangChain-based LLM integration
- ✅ Pydantic-based article validation
- 🧹 Article text cleaning and processing
- 📊 Configurable number of articles
- 📅 Configurable research date range
- 🌐 Multilingual research output
  - English
  - Hindi
  - Marathi
- 🖼️ Featured research images from retrieved news articles
- 📰 Images for individual source articles when available
- 🔗 Direct links to original news articles
- 🎯 Within-topic related research recommendations
- 🌍 Broader-context research recommendations
- 🔄 Click recommendations to launch new research
- 📄 Downloadable research reports
- 📊 Downloadable article CSV files
- 🛡️ Environment-based API key configuration
- 🧪 Automated testing with pytest
- 🎨 Interactive Streamlit interface
- 🔒 Secure handling of API credentials

---

## 🏗️ System Architecture

```text
                              USER
                                │
                                ▼
                         ┌─────────────┐
                         │ Streamlit UI│
                         └──────┬──────┘
                                │
                                ▼
                      ┌──────────────────┐
                      │ Research Pipeline│
                      └────────┬─────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
        ┌──────────────┐             ┌────────────────┐
        │   NewsAPI    │             │ Research Prompt│
        └──────┬───────┘             └───────┬────────┘
               │                             │
               ▼                             ▼
       Raw News Articles                 ┌─────────┐
               │                         │  Groq   │
               ▼                         │   LLM   │
      Pydantic Validation                └────┬────┘
               │                              │
               ▼                              │
      Article Processing                     │
               │                              │
               └──────────────┬───────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Research Result │
                     └────────┬────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
    AI Research          News Images       Source Articles
       Summary
          │
          ▼
 ┌────────────────────────┐
 │ Related Research       │
 │ Recommendation Engine  │
 └───────────┬────────────┘
             │
       ┌─────┴──────┐
       ▼            ▼
 Within Topic   Broader Context
       │            │
       └─────┬──────┘
             │
             ▼
       New Research Query
             │
             ▼
       Research Pipeline

             Research Result
                    │
             ┌──────┴──────┐
             ▼             ▼
       Research Report   Articles CSV
🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
Streamlit	Interactive web application
NewsAPI	News article retrieval
LangChain	LLM application framework
Groq	LLM inference
Pydantic	Data validation and structured models
Pytest	Automated testing
python-dotenv	Environment variable management
📁 Project Structure
news-research-tool/
│
├── newsapp.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│
├── scripts/
│   ├── __init__.py
│   ├── test_news_api.py
│   └── test_grok.py
│
├── src/
│   ├── __init__.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── client.py
│   │
│   ├── news/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── models.py
│   │   └── exceptions.py
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── research.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   └── articles.py
│   │
│   ├── recommendations/
│   │   ├── __init__.py
│   │   └── related.py
│   │
│   └── export/
│       ├── __init__.py
│       └── reports.py
│
└── tests/
    ├── test_config.py
    ├── test_news_client.py
    ├── test_news_exceptions.py
    ├── test_llm_client.py
    ├── test_research_pipeline.py
    ├── test_article_processing.py
    ├── test_reports.py
    └── test_related.py

The .env file is intentionally excluded from version control and should be created locally.

⚙️ Installation
1. Clone the repository
git clone <your-github-repository-url>
cd news-research-tool
2. Create a virtual environment

On Windows PowerShell:

python -m venv .venv
3. Activate the virtual environment
.\.venv\Scripts\Activate.ps1
4. Install dependencies
python -m pip install -r requirements.txt
🔑 API Configuration

The application requires API credentials for:

NewsAPI
Groq

Create a .env file in the project root:

NEWSAPI_KEY=your_newsapi_key
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
Security

Never commit the .env file to Git.

The .gitignore file excludes:

.env

API keys should never be:

Hard-coded in Python source files
Committed to Git
Included in documentation
Shared publicly

A safe configuration template is provided as:

.env.example
▶️ Running the Application

Make sure the virtual environment is activated.

Start the Streamlit application:

python -m streamlit run .\newsapp.py

Streamlit will provide a local URL in the terminal and open the application in the browser.

🔎 Using the Application

Enter a company, market, sector, industry, or general news topic.

Example Queries
Tesla
Nvidia AI
Indian banking sector
Air India
Nepal news on weather

The application allows the user to configure:

Number of articles
Research period
Output language
Supported Languages
English
Hindi
Marathi
Research Process
Enter a research topic.
Select the number of articles.
Select the research period.
Select the output language.
Click Research.
NewsAPI retrieves relevant articles.
Retrieved articles are validated using Pydantic.
Article content is cleaned and formatted.
The processed articles are passed to the research pipeline.
A structured research prompt is created.
The prompt is sent to the Groq LLM through LangChain.
The AI-generated research summary is displayed.
Relevant news imagery is displayed when available.
Source articles are displayed with publication information and images.
Related research recommendations are generated.
Users can click recommendations to launch new research.
Research results can be exported as a report or CSV.
🧠 AI Research Summary

The application uses a structured research prompt designed to assist with business and equity research analysis.

The generated research summary contains six sections:

Executive Summary
Key Developments
Companies / Markets Affected
Business & Market Implications
Risks / Contradictions
Research Takeaway
Research Grounding

The LLM is instructed to:

Use only information supported by the retrieved articles
Avoid inventing facts
Avoid inventing numbers
Avoid inventing events
Avoid unsupported conclusions
Distinguish reported facts from implications
Use cautious language when evidence is uncertain
Identify contradictions or differences between sources
Avoid providing investment advice

The generated response is also sanitized before being displayed in the Streamlit interface.

🌐 Multilingual Research

The application supports AI research output in:

English
Hindi
Marathi

English is the default language.

The selected language is passed into the research prompt so that the generated research summary is returned in the user's selected language.

🖼️ News Images

The application uses image URLs provided by retrieved news articles when available.

Featured Research Image

A relevant image from the retrieved article set is displayed near the AI Research Summary.

Source Article Images

Individual source article cards display their corresponding images when available.

This implementation uses existing article imagery rather than a separate AI image-generation service, reducing additional API dependencies, latency, and cost.

🎯 Related Research Recommendations

After a successful research query, the application uses the LLM to generate additional research paths.

Recommendations are divided into two categories.

🎯 Within This Topic

These recommendations remain closely related to the original topic.

They may include:

Related companies
Products
Locations
Events
Subtopics
Industries
Business developments
🌍 Broader Context

These recommendations expand the research into related:

Countries
Regions
Markets
Competitors
Industries
Global developments
Example

For a query such as:

weather in USA

the application can generate related research such as:

Within this topic:
- California weather
- Texas weather
- Florida weather
- New York weather

Broader context:
- Weather in India
- Weather in the UK
- Weather in Japan
- Weather in Australia

Recommendations are generated dynamically rather than being limited to a hard-coded list.

Clicking a recommendation launches a new research query through the same research pipeline.

📥 Export and Downloads

The application provides two export options.

📄 Research Report

The research report contains:

Research query
Output language
Research period
Number of articles analyzed
Number of sources
AI research summary
Source article information
Article URLs
📊 Articles CSV

The CSV export contains:

Title
Source
Published date
Description
URL

These exports allow users to retain, share, and further analyze their research results.

🔄 End-to-End Research Workflow
User Query
    │
    ▼
Streamlit Interface
    │
    ▼
Research Pipeline
    │
    ▼
NewsAPI Search
    │
    ▼
Raw News Articles
    │
    ▼
Pydantic Validation
    │
    ▼
Article Cleaning & Formatting
    │
    ▼
Research Prompt
    │
    ▼
Groq LLM via LangChain
    │
    ▼
AI Research Summary
    │
    ├──────────────► Featured News Image
    │
    ├──────────────► Source Articles
    │
    ├──────────────► Related Research
    │
    └──────────────► Export / Download
🧩 Core Components
News Client

Location:

src/news/client.py

Responsible for:

Communicating with NewsAPI
Validating search parameters
Retrieving news articles
Supporting configurable date ranges
Supporting article limits
Removing duplicate articles
Handling NewsAPI errors
Converting API responses into validated models
News Article Model

Location:

src/news/models.py

Uses Pydantic to provide structured validation for:

Title
Description
Content
Source
Author
URL
Image URL
Publication date
News Exceptions

Location:

src/news/exceptions.py

Defines application-specific exceptions for:

Authentication failures
Rate limiting
Request failures
Invalid API responses

This keeps NewsAPI error handling explicit and easier to test.

Article Processing

Location:

src/processing/articles.py

Responsible for:

Cleaning whitespace
Truncating long article text
Formatting individual articles
Combining multiple articles into LLM-ready context
Groq Client

Location:

src/llm/client.py

Responsible for:

Initializing the Groq LLM
Validating prompts
Sending requests through LangChain
Returning generated responses
Handling LLM failures
Research Pipeline

Location:

src/pipeline/research.py

Acts as the main orchestration layer between:

NewsAPI
    ↓
Article Validation
    ↓
Article Processing
    ↓
Research Prompt
    ↓
Groq LLM
    ↓
Research Result

The pipeline returns a structured research result containing:

Original query
Retrieved articles
Generated summary

The pipeline also supports:

Configurable article limits
Configurable date ranges
English output
Hindi output
Marathi output
Safe summary rendering
Related Research Generator

Location:

src/recommendations/related.py

Responsible for:

Generating related research queries
Creating within-topic recommendations
Creating broader-context recommendations
Parsing structured LLM output
Removing duplicate recommendations
Limiting recommendation counts
Handling invalid LLM responses safely
Export Module

Location:

src/export/reports.py

Responsible for generating:

Research report exports
Article CSV exports
🧪 Testing

Run the complete automated test suite:

python -m pytest -q
Current Test Status
42 passed
Test Coverage Areas

The automated tests cover:

Configuration handling
NewsAPI client behavior
NewsAPI authentication errors
NewsAPI rate-limit errors
NewsAPI request errors
Invalid NewsAPI responses
LLM client behavior
Empty prompt validation
Research pipeline
Article processing
Input validation
Empty-result handling
Multilingual research output
Research report generation
CSV generation
Related research generation
Recommendation parsing
Duplicate recommendation handling
Recommendation limits
🔍 Validation and Quality Checks

The application has been validated through both automated tests and manual end-to-end testing.

Automated Validation
Pytest Tests: 42 passed
Python Compilation: Passed
Manual Validation

The following workflows have been tested successfully:

Normal News Research
        ↓
AI Research Summary
        ↓
Featured News Image
        ↓
Source Article Images
        ↓
Related Research
        ↓
Recommendation Click
        ↓
Fresh Research Query
        ↓
New AI Summary + Images

Additional manual validation includes:

English research output
Hindi research output
Non-technical/general-audience topics
Empty search validation
Research report download
Articles CSV download
Recommendation-driven research
🛡️ Security

API credentials are loaded from environment variables using python-dotenv.

Sensitive credentials should never be:

Hard-coded in source code
Committed to Git
Included in documentation
Shared publicly

The .env file is excluded from version control through .gitignore.

The project provides:

.env.example

as a safe configuration template.

📊 Project Status

The project currently includes:

✅ NewsAPI integration
✅ Groq LLM integration
✅ LangChain integration
✅ Pydantic article validation
✅ Article text processing
✅ Research pipeline
✅ Streamlit application
✅ Configurable article count
✅ Configurable research period
✅ English research output
✅ Hindi research output
✅ Marathi research output
✅ Featured news images
✅ Source article images
✅ Related research recommendations
✅ Within-topic recommendations
✅ Broader-context recommendations
✅ Recommendation-driven new research
✅ Research report export
✅ Article CSV export
✅ Automated testing
✅ Environment-based configuration
✅ Clean dependency management
✅ Git version control
✅ Input validation
✅ Error handling
Final Validation
Automated Tests: 42 passed
Python Compilation: Passed
Streamlit Application: Working
NewsAPI Integration: Working
Groq LLM Integration: Working
Multilingual Output: Working
Related Research: Working
Recommendation Loop: Working
Exports: Working
News Images: Working
Input Validation: Working
🔮 Future Enhancements

Potential future improvements include:

User authentication
Research result caching
Historical query analysis
Advanced filtering by source
Source credibility scoring
Cloud deployment
Additional LLM providers
More comprehensive integration testing
Persistent user research history