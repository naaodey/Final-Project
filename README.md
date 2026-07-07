# 🛡️ SafeMath Tutor: A Guardrailed AI Assistant for Mathematics Education

An AI-powered mathematics and statistics tutor designed with **AI safety, reliability, and educational integrity** at its core.

SafeMath Tutor provides clear, step-by-step solutions through an intuitive Streamlit interface while incorporating guardrails that reduce misuse, improve reliability, and encourage trustworthy interactions with Large Language Models (LLMs).

Unlike traditional AI chatbots that prioritize generating answers, SafeMath Tutor emphasizes **safe reasoning, structured outputs, and transparent explanations** to support student learning.

---

## Why This Project?

Large Language Models have enormous potential in education, but they also introduce important challenges:

* Hallucinated mathematical solutions
* Incorrect reasoning presented confidently
* Prompt injection and jailbreak attempts
* Off-topic conversations
* Limited transparency into model outputs

SafeMath Tutor was built to explore how AI systems can become **more trustworthy educational assistants** through structured outputs, input validation, and controlled interactions.

---

# AI Safety Objectives

This project investigates practical approaches to safer educational AI by incorporating:

* Input validation before model execution
* Prompt injection resistance
* Topic restriction to approved mathematics and statistics concepts
* Structured JSON responses
* Conversation memory with controlled context length
* Confidence reporting
* Transparent reasoning through step-by-step explanations

The long-term goal is to study how educational AI systems can become more reliable, interpretable, and safe for classroom use.

---

# Features

## Step-by-step reasoning

Every solution is broken into logical, numbered steps so students learn the reasoning process rather than only receiving the final answer.

---

## Structured JSON Output

Each response follows a predefined schema:

```json
{
  "topic": "...",
  "steps": [...],
  "final_answer": "...",
  "confidence": "High"
}
```

This enables:

* easier validation
* downstream evaluation
* future automated checking
* interoperability with other educational systems

---

## Conversation Memory

Maintains the previous five interactions for each student session, allowing follow-up questions while limiting excessive context accumulation.

---

## Guardrails

Every prompt is validated before reaching the LLM.

Current checks include:

* minimum/maximum length
* blocked phrases
* jailbreak attempts
* prompt injection patterns
* topic allowlist
* mathematics expression detection

Unsafe or unrelated prompts are rejected before any API request is made.

---

## Student-Friendly Interface

Built with Streamlit, featuring:

* one-click example questions
* session history
* structured solution display
* live JSON panel
* clean educational interface

---

# System Architecture

```
Student Question
        │
        ▼
 Input Guardrails
        │
        ▼
 Conversation Memory
        │
        ▼
 Prompt Construction
        │
        ▼
Groq API (LLaMA 3.3 70B)
        │
        ▼
 JSON Parsing
        │
        ▼
 Response Validation
        │
        ▼
 Streamlit Interface
```

---

# Technology Stack

| Component     | Technology             |
| ------------- | ---------------------- |
| Frontend      | Streamlit              |
| LLM           | LLaMA 3.3 70B via Groq |
| API Client    | Groq Python SDK        |
| Optional API  | FastAPI                |
| Memory        | Python Session Storage |
| Configuration | python-dotenv          |

---

# Supported Topics

* Statistics
* Probability
* Hypothesis Testing
* Regression
* Confidence Intervals
* Bayesian Statistics
* Algebra
* Calculus
* Linear Algebra
* Trigonometry
* Arithmetic

---

# Current Safety Features

✅ Topic allowlist

✅ Prompt injection filtering

✅ Jailbreak detection

✅ Structured outputs

✅ Controlled conversation memory

✅ Confidence reporting

✅ Educational reasoning instead of answer-only responses

---

# Planned AI Safety Improvements

The next stage of this project focuses on advancing reliability and trustworthiness.

## Mathematical Verification

Use symbolic mathematics (e.g., SymPy) to independently verify algebraic manipulations, differentiation, integration, and equation solving before presenting results.

---

## Multi-Agent Verification

Generate multiple independent solutions and compare them for consistency before returning a final answer.

---

## Confidence Calibration

Replace qualitative confidence labels ("High", "Medium", "Low") with calibrated confidence scores informed by model behavior and evaluation data.

---

## Hallucination Detection

Automatically identify unsupported or inconsistent mathematical reasoning and flag potentially unreliable responses.

---

## Educational Benchmarking

Evaluate multiple LLMs on standardized mathematics and statistics datasets, including questions aligned with BECE and WAEC curricula, measuring:

* Accuracy
* Reasoning quality
* Hallucination rate
* Explanation clarity
* Safety performance

---

# Research Directions

This project serves as a foundation for research in:

* AI Safety
* Responsible AI
* Educational AI
* LLM Evaluation
* AI Reliability
* Human-AI Interaction
* AI Alignment for Education

---

# Potential Impact

SafeMath Tutor demonstrates how AI systems can support education while incorporating practical safeguards that encourage reliability, transparency, and responsible use.

The project aims to contribute toward trustworthy AI assistants that help students learn mathematics safely and effectively rather than simply producing answers.

---

# Author

**Naa Odey Solomon (MPhil)**

Mathematics & STEM Educator

AI Developer | Statistics Researcher | Responsible AI Enthusiast
