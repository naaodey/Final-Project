# 📐 Student Study Helper

An AI-powered maths and statistics tutor that delivers clear, step-by-step solutions through a clean Streamlit interface. Built with Groq (LLaMA 3.3 70B), it includes conversation memory, input guardrails, and structured JSON output — all running from a single Python file with no backend server required.

---

## Features

- **Step-by-step solutions** — every answer is broken into numbered steps with plain-language explanations
- **Structured JSON output** — responses follow a consistent schema (`topic`, `steps`, `final_answer`, `confidence`), displayed alongside the UI in a live JSON panel
- **Conversation memory** — remembers the last 5 questions per session so follow-up questions have full context
- **Input guardrails** — validates questions against an allowlist of maths/statistics topics and blocks unsafe or off-topic prompts before they reach the model
- **Example chips** — one-click questions to get started instantly
- **Session history** — sidebar shows a running log of questions and answers for the current session

---

## Project Structure

```
student-study-helper/
│
├── streamlit_app.py   # Main UI — run this to launch the app
├── main.py            # Core logic: validates, builds context, calls Groq, parses response
├── memory.py          # In-memory conversation history manager (per session)
├── guardrails.py      # Input validation: topic allowlist, blocked phrases, length checks
├── app.py             # Optional FastAPI wrapper (not required to run the app)
└── .env               # Your Groq API key (see setup below)
```

---

## Subjects Covered

| Area | Topics |
|---|---|
| **Statistics** | Mean, median, mode, variance, standard deviation, z-score, confidence intervals, hypothesis testing, ANOVA, t-test, chi-square, regression, correlation, Bayes' theorem, distributions (normal, binomial, Poisson) |
| **Calculus** | Differentiation, integration, limits, derivatives |
| **Algebra** | Equations, polynomials, quadratics, sequences, series, factorials, permutations, combinations |
| **Linear Algebra** | Matrices, determinants, eigenvalues, vectors |
| **Trigonometry** | Sine, cosine, tangent, identities |
| **General Maths** | Arithmetic, fractions, ratios, logarithms, exponentials, set theory |

---

## JSON Response Schema

Every question returns a structured JSON object:

```json
{
  "topic": "Statistics — Variance",
  "steps": [
    "List the values: 1, 2, 3, 4, 5. There are n = 5 values.",
    "Calculate the mean: (1+2+3+4+5) / 5 = 3.",
    "Find squared deviations from the mean: 4, 1, 0, 1, 4.",
    "Sum the squared deviations: 10.",
    "Divide by n: 10 / 5 = 2."
  ],
  "final_answer": "The variance of {1, 2, 3, 4, 5} is 2.",
  "confidence": "High"
}
```

| Field | Description |
|---|---|
| `topic` | Subject area of the question |
| `steps` | Ordered list of solution steps |
| `final_answer` | Concise final result |
| `confidence` | Model's confidence level: `High`, `Medium`, or `Low` |

---


## How It Works

```
User question
      │
      ▼
 guardrails.py
 ┌─────────────────────────────────┐
 │ 1. Check question length        │
 │ 2. Scan for blocked phrases     │
 │ 3. Match against topic allowlist│
 │    or maths expression patterns │
 └─────────────────────────────────┘
      │ valid
      ▼
  memory.py
  └─ Load last 5 Q&A pairs for session context
      │
      ▼
  main.py → Groq API (LLaMA 3.3 70B)
  └─ System prompt enforces JSON-only output
      │
      ▼
  Parse JSON response
      │
      ▼
  memory.py
  └─ Save question + answer to session history
      │
      ▼
  streamlit_app.py
  └─ Render step tiles, final answer box, JSON panel
```

---

## Guardrails

Questions are validated before reaching the model:

| Check | Rule |
|---|---|
| **Length** | Between 3 and 1000 characters |
| **Blocked content** | Rejects prompts containing phrases like `hack`, `jailbreak`, `ignore previous instructions`, `reveal system prompt`, etc. |
| **Topic** | Must match at least one keyword from the maths/statistics allowlist, or match a recognised maths expression pattern (e.g. `x^2`, `f(x)`, `3 + 4`) |

Rejected questions return a clear message without calling the model.



## Running the FastAPI backend

`app.py` exposes the same `solve_question` logic as a REST API, useful if you want to call the solver from another application.

```bash
pip install fastapi uvicorn
uvicorn app:app --reload
```

The API runs at `http://localhost:8000`.

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | App info |
| `/health` | GET | Health check |
| `/about` | GET | Feature list |
| `/solve` | POST | Submit a question |

**POST `/solve` — request body:**

```json
{
  "question": "Find the mean of 2, 4, 6, 8, 10",
  "session_id": "student_001"
}
```

> Note: the Streamlit app does **not** require this server. It calls `solve_question` directly via Python import.

---

## Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| AI model | LLaMA 3.3 70B via Groq |
| API client | `groq` Python SDK |
| Optional API | FastAPI + Uvicorn |
| Memory | In-process Python dict (session-scoped) |
| Config | `python-dotenv` |
