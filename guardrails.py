import re


ALLOWED_TOPICS = [
    "math",
    "mathematics",
    "statistics",
    "probability",
    "algebra",
    "calculus",
    "regression",
    "variance",
    "mean",
    "median",
    "mode",
    "quantile",
    "bayes",
    "bayesian",
    "theorem",
    "proof",
    "distribution",
    "sampling",
    "hypothesis",
    "correlation",
    "linear algebra",
    "matrix",
    "determinant",
    "eigenvalue",
    "equation",
    "differentiate",
    "differentiation",
    "derivative",
    "integrate",
    "integration",
    "integral",
    "limit",
    "function",
    "normal distribution",
    "binomial",
    "poisson",
    "chi-square",
    "t-test",
    "anova",
    "confidence interval",
    "z-score",
    "standard deviation",
    "solve",
    "calculate",
    "compute",
    "vector",
    "scalar",
    "set theory",
    "graph",
    "formula",
    "permutation",
    "combination",
    "factorial",
    "logarithm",
    "exponential",
    "trigonometry",
    "sine",
    "cosine",
    "tangent",
    "polynomial",
    "quadratic",
    "arithmetic",
    "geometric",
    "sequence",
    "series",
    "sum",
    "product",
    "number",
    "fraction",
    "ratio",
    "proportion"
]


BLOCKED_PHRASES = [
    "hack",
    "hacking",
    "malware",
    "virus",
    "trojan",
    "ransomware",
    "bypass",
    "jailbreak",
    "ignore previous instructions",
    "ignore all instructions",
    "reveal system prompt",
    "show hidden prompt",
    "developer message",
    "system message"
]

MAX_LENGTH = 1000
MIN_LENGTH = 3


def contains_blocked_content(question: str):

    text = question.lower()

    for phrase in BLOCKED_PHRASES:
        if phrase in text:
            return True

    return False


def is_allowed_topic(question: str):

    text = question.lower()

    for topic in ALLOWED_TOPICS:
        if topic in text:
            return True

    return False


def valid_length(question: str):

    question = question.strip()

    if len(question) < MIN_LENGTH:
        return False

    if len(question) > MAX_LENGTH:
        return False

    return True


def looks_like_math_expression(question: str):

    patterns = [
        r"\d+\s*[\+\-\*/]\s*\d+",
        r"x\^",
        r"y=",
        r"f\(x\)",
        r"\(",
        r"\)"
    ]

    for pattern in patterns:
        if re.search(pattern, question):
            return True

    return False



def validate_question(question: str):

    if not valid_length(question):

        return (
            False,
            "Question length is invalid."
        )

    if contains_blocked_content(question):

        return (
            False,
            "Unsafe prompt detected."
        )

    if (
        is_allowed_topic(question)
        or looks_like_math_expression(question)
    ):

        return (
            True,
            "Valid question."
        )

    return (
        False,
        "Only Math and Statistics questions are allowed."
    )