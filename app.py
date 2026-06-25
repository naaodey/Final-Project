from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import solve_question

app = FastAPI(
    title="Student Study Helper",
    description="AI-powered Math and Statistics Tutor",
    version="1.0.0"
)



class SolveRequest(BaseModel):
    question: str
    session_id: str = "default"


class SolveResponse(BaseModel):
    success: bool
    question: str
    result: dict



@app.get("/")
def home():
    return {
        "application": "Student Study Helper",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/about")
def about():
    return {
        "project": "Student Study Helper",
        "features": [
            "Step-by-step solutions",
            "Structured JSON output",
            "Conversation memory",
            "Educational guardrails",
            "Math and Statistics support"
        ]
    }


@app.post(
    "/solve",
    response_model=SolveResponse
)
def solve(request: SolveRequest):

    try:

        result = solve_question(
            question=request.question,
            session_id=request.session_id
        )

        return SolveResponse(
            success=True,
            question=request.question,
            result=result
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )