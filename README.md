# 📰 News Research Tool

An AI-powered news research application that retrieves recent news articles for a user-defined topic and generates a concise research summary using a Groq-hosted LLM.

The application is designed to support equity research and business analysis by combining real-time news retrieval, article validation, text processing, and LLM-based summarization.

---

## 🚀 Features

- Search recent news using NewsAPI
- Validate retrieved articles using Pydantic models
- Clean and format article content for LLM processing
- Generate research summaries using Groq
- Use LangChain for LLM integration
- Streamlit-based interactive user interface
- Configurable number of articles
- Configurable news date range
- Display article sources and publication dates
- Automated unit testing with pytest
- Environment-based API key configuration

---

## 🏗️ Architecture

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
Research Pipeline
  │
  ├──────────────► NewsAPI
  │                    │
  │                    ▼
  │              News Articles
  │                    │
  │                    ▼
  │              Pydantic Validation
  │                    │
  │                    ▼
  │              Article Processing
  │
  ▼
Research Prompt
  │
  ▼
Groq LLM
  │
  ▼
Research Summary
  │
  ▼
Streamlit UI
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| NewsAPI | News article retrieval |
| LangChain | LLM application framework |
| Groq | LLM inference |
| Pydantic | Data validation |
| Pytest | Automated testing |
| python-dotenv | Environment variable management |

---

## 📁 Project Structure

```text
news-research-tool/
│
├── newsapp.py
├── README.md
├── requirements.txt
├── .env
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
│   └── processing/
│       ├── __init__.py
│       └── articles.py
│
└── tests/
    ├── test_config.py
    ├── test_news_client.py
    ├── test_news_exceptions.py
    ├── test_llm_client.py
    ├── test_research_pipeline.py
    └── test_article_processing.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd news-research-tool
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## 🔑 API Configuration

The application requires API credentials for:

- NewsAPI
- Groq

Create a `.env` file in the project root:

```text
NEWSAPI_KEY=your_newsapi_key
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

### Security

Never commit your `.env` file to Git.

The project `.gitignore` is configured to exclude:

```text
.env
```

Never hard-code API keys directly into Python source files.

---

## ▶️ Running the Application

Make sure the virtual environment is activated.

Start the Streamlit application:

```powershell
python -m streamlit run .\newsapp.py
```

Streamlit will provide a local URL in the terminal and open the application in your browser.

### Example Queries

You can search for topics such as:

```text
Tesla
```

```text
Nvidia AI
```

```text
Indian banking sector
```

```text
Microsoft earnings
```

After entering a query:

1. Select the number of articles.
2. Select the news date range.
3. Click **Research News**.
4. The application retrieves relevant news articles.
5. The articles are processed and sent to the Groq LLM.
6. The generated research summary is displayed.
7. Article sources and publication information are displayed below the summary.

---

## 🧪 Running Tests

Run the complete automated test suite:

```powershell
python -m pytest
```

The test suite covers:

- Configuration handling
- NewsAPI client behavior
- NewsAPI error handling
- LLM client behavior
- Research pipeline
- Article processing
- Input validation
- Empty-result handling

### Current Test Status

```text
24 passed
```

---

## 🔄 Research Workflow

The application follows this workflow:

```text
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
AI-Generated Summary
    │
    ▼
Streamlit Results
```

### Detailed Process

1. The user enters a research query.
2. The Streamlit application passes the query to `ResearchPipeline`.
3. `NewsClient` sends the query to NewsAPI.
4. Retrieved articles are converted into validated `NewsArticle` objects.
5. Invalid articles are safely skipped.
6. Article descriptions and content are cleaned and normalized.
7. Article information is formatted into LLM-ready text.
8. A research prompt is constructed using the user query and retrieved articles.
9. The prompt is sent to the Groq LLM through `GroqClient`.
10. The generated summary is returned to the research pipeline.
11. Streamlit displays the summary and article sources.

---

## 🧠 Research Prompt

The application instructs the LLM to act as an AI assistant helping an equity research analyst.

The generated summary focuses on:

- Important developments
- Companies, organizations, or markets affected
- Potential business or market implications
- Differences or conflicting information between articles

The prompt also instructs the model to:

- Use only information supported by the provided articles
- Avoid inventing facts
- Avoid inventing numbers
- Avoid inventing events
- Avoid unsupported conclusions

This helps keep the generated research summary grounded in the retrieved news content.

---

## 🧩 Core Components

### News Client

Located at:

```text
src/news/client.py
```

Responsible for:

- Communicating with NewsAPI
- Validating search parameters
- Retrieving recent articles
- Handling API errors
- Converting API responses into validated models

### News Article Model

Located at:

```text
src/news/models.py
```

Uses Pydantic to provide structured validation for:

- Title
- Description
- Content
- Source
- Author
- URL
- Image URL
- Publication date

### Article Processing

Located at:

```text
src/processing/articles.py
```

Responsible for:

- Cleaning whitespace
- Truncating long article text
- Formatting individual articles
- Combining multiple articles into LLM-ready context

### Groq Client

Located at:

```text
src/llm/client.py
```

Responsible for:

- Initializing the Groq LLM
- Validating prompts
- Sending requests through LangChain
- Returning generated responses
- Handling LLM failures

### Research Pipeline

Located at:

```text
src/pipeline/research.py
```

Acts as the orchestration layer between:

```text
NewsAPI → Article Processing → Groq LLM
```

It returns a structured research result containing:

- Original query
- Retrieved articles
- Generated summary

---

## 🔐 Security

API credentials are loaded from environment variables using `python-dotenv`.

Sensitive credentials should never be:

- Hard-coded in source code
- Committed to Git
- Included in documentation
- Shared publicly

The `.env` file is excluded from version control through `.gitignore`.

---

## 📊 Current Project Status

The project currently includes:

- ✅ NewsAPI integration
- ✅ Groq LLM integration
- ✅ LangChain integration
- ✅ Pydantic article validation
- ✅ Article text processing
- ✅ Research pipeline
- ✅ Streamlit application
- ✅ Automated testing
- ✅ Environment-based configuration
- ✅ Clean dependency management
- ✅ Git version control

### Validation

```text
Automated Tests: 24 passed
Streamlit Application: Working
NewsAPI Integration: Working
Groq LLM Integration: Working
```

---

## 🔮 Future Enhancements

Potential future improvements include:

- User authentication
- Improved Streamlit UI/UX
- Article deduplication
- Research result caching
- Save and export research results
- Historical query analysis
- Improved source presentation
- Advanced filtering by source or category
- Cloud deployment
- Additional LLM providers
- More comprehensive integration testing

---

## 📄 License

This project is intended for educational and portfolio purposes.