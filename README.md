# AI Study Assistant 

An AI-powered study assistant built with **Python and FastAPI** that helps students learn through AI-generated explanations, summaries, multiple-choice questions, and flashcards.

The application exposes REST APIs for generating study content and stores study history using a SQL database.

## Features

*  **AI Question Answering** — Get simple, context-aware explanations for study questions.
*  **Text Summarization** — Convert lengthy study material into concise summaries.
*  **MCQ Generator** — Generate multiple-choice questions from study material.
*  **Flashcard Generator** — Create flashcards for quick revision.
*  **Study History** — Store and retrieve previous study activities.
*  **RESTful APIs** — FastAPI-based endpoints with JSON request/response handling.
*  **Automated Testing** — API functionality tested using Pytest.
*  **Environment-based Configuration** — API keys and configuration values are managed through environment variables.

##  Tech Stack

| Technology           | Purpose                     |
| -------------------- | --------------------------- |
| Python               | Application development     |
| FastAPI              | REST API framework          |
| Pydantic             | Request/response validation |
| SQLAlchemy           | Database interaction        |
| SQLite               | Local database              |
| Gemini API           | AI/LLM integration          |
| OpenAI Python Client | LLM API interface           |
| Pytest               | Automated testing           |
| Postman              | API testing                 |
| Git & GitHub         | Version control             |

##  Project Architecture

```text
ai-study-assistant/
│
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Environment configuration
│   ├── database.py             # Database configuration
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   │
│   ├── routers/
│   │   ├── ask.py              # Question answering API
│   │   ├── summary.py          # Summary API
│   │   ├── mcqs.py             # MCQ generation API
│   │   ├── flashcards.py       # Flashcard generation API
│   │   └── history.py          # Study history API
│   │
│   └── services/
│       ├── llm_service.py      # LLM integration
│       └── history_service.py  # History/database operations
│
├── tests/                      # Automated API tests
│
├── postman/                    # Postman collection and environment
│
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore configuration
├── requirements.txt            # Application dependencies
├── requirements-dev.txt        # Development/testing dependencies
├── pytest.ini                  # Pytest configuration
└── README.md
```

##  API Endpoints

| Method | Endpoint             | Description                        |
| ------ | -------------------- | ---------------------------------- |
| GET    | `/health`            | Check application health           |
| POST   | `/api/v1/ask`        | Ask an AI-powered study question   |
| POST   | `/api/v1/summary`    | Generate a summary                 |
| POST   | `/api/v1/mcqs`       | Generate multiple-choice questions |
| POST   | `/api/v1/flashcards` | Generate flashcards                |
| GET    | `/api/v1/history`    | Retrieve study history             |

Interactive API documentation is available through FastAPI's Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ashirjoseph/ai-study-assistant.git
cd ai-study-assistant
```

### 2. Create a virtual environment

On Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```env
APP_ENV=development
DATABASE_URL=sqlite:///./study_assistant.db
LLM_API_KEY=your_api_key_here
LLM_MODEL=gemini-3.8-flash
LLM_MAX_TOKENS=400
LLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

**Never commit your `.env` file or API keys to GitHub.**

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

##  Running Tests

Run the automated test suite using:

```bash
pytest -v
```

The current project test suite contains **18 automated tests**, covering the main API functionality.

##  API Testing with Postman

A Postman collection is included in the repository:

```text
postman/AI_Study_Assistant.postman_collection.json
```

The collection can be imported into Postman to test the API endpoints.

##  Example

### Ask a Question

**Request**

```json
{
  "question": "Explain photosynthesis in simple terms."
}
```

**Response**

```json
{
  "id": 1,
  "question": "Explain photosynthesis in simple terms.",
  "answer": "Photosynthesis is the process plants use to make their own food using sunlight.",
  "tokens_used": 428
}
```

##  Security

Sensitive configuration values are stored using environment variables.

The repository intentionally excludes:

```text
.env
.venv/
*.db
__pycache__/
.pytest_cache/
```

API keys should never be committed to source control.

##  Learning Goals

This project was developed to gain practical experience with:

* Python backend development
* REST API development
* FastAPI
* LLM API integration
* Prompt engineering
* SQL/database integration
* API testing
* Pytest
* Postman
* Error handling
* Git and GitHub

##  Future Improvements

* Add user authentication and authorization
* Add persistent user accounts
* Improve LLM response validation
* Add richer study analytics
* Add frontend interface
* Add rate-limit handling and retry mechanisms
* Add deployment using a cloud platform
* Expand automated test coverage

##  Author

**Ashir Joseph**

GitHub:
https://github.com/Ashirjoseph

---

 If you find this project useful, consider giving it a star.
