from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os

# Import local modules
from models import User, SubmissionResponse, LeaderboardEntry
from auth import authenticate_user
from database import init_db, save_submission, get_leaderboard, get_top_three
from test_evaluate import test_evaluate
from utils import generate_test_questions, ensure_data_dir
from evaluate import load_questions
import sqlite3

# Initialize the FastAPI app
app = FastAPI(title="Leaderboard API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Setup function to run on startup
@app.on_event("startup")
async def startup_event():
    """Initialize everything needed on startup"""
    # Initialize database
    init_db()

    # Ensure data directory exists
    ensure_data_dir()

    # Check if check_questions.csv exists, create if not
    if not os.path.exists("data/check_questions.csv"):
        default_questions = [
            [
                "Hvor mange dager må det gå før purregebyr og renter kan beregnes",
                "SupportAI",
            ],
            ["Legge inn kontaktperson hos kunde", "Sticos"],
            ["Hvordan trekke en ansatt et beløp i lønn?", "SupportAI"],
            ["HVORDAN FINNER MAN LISTE FOR RF-1321 I TRIPLETEX", "Sticos"],
            ["Mva på konto uten avdeling", "SupportAI"],
        ]

        os.makedirs("data", exist_ok=True)

        import csv

        with open("data/check_questions.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["question", "classification"])
            writer.writerows(default_questions)

    # Generate test questions if they don't exist
    if not os.path.exists("data/test_questions.csv"):
        generate_test_questions()


# API Routes
@app.post("/login")
async def login(user: User):
    """Login endpoint"""
    # Check authentication
    name = authenticate_user(user.name, user.password)

    # If authentication fails, return 401
    if name is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"name": name}


@app.post("/submit", response_model=SubmissionResponse)
async def submit_response(user: User):
    """Submit a solution and get evaluation results"""
    # Authenticate the user
    name = authenticate_user(user.name, user.password)

    # If authentication fails, return 401
    if name is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Evaluate the solution
    evaluation = test_evaluate(user.solution or "")

    # Save submission to database with both scores
    save_submission(
        name=name,
        score=evaluation["score"],
        solution=user.solution,
        tmp_score=evaluation["tmp_score"],
    )

    # Return the evaluation results
    response = SubmissionResponse(
        score=evaluation["score"], results=evaluation["results"]
    )
    print(response)
    return response


@app.post("/winner")
def calculate_winner():
    # for each unuque user in the database, take the most recent database entry and run the test data on it
    # then return the user with the highest score, as well as writing it to a new table in the database
    # this table should contain the name of the user and their score, as well as their textstring

    # get all unique users
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM scores")
    users = cursor.fetchall()
    conn.close()

    # get the most recent submission for each user
    user_scores = []
    for user in users:
        conn = sqlite3.connect("leaderboard.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM scores WHERE name = ? ORDER BY timestamp DESC LIMIT 1",
            (user[0],),
        )
        user_scores.append(cursor.fetchall())
        conn.close()

    # evaluate the most recent submission for each user
    user_scores_evaluated = []
    for user in user_scores:
        evaluation = test_evaluate(user[0][4])
        user_scores_evaluated.append(evaluation["score"])

    # get the user with the highest score
    print(user_scores_evaluated)


@app.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard_route():
    """Get the leaderboard data"""
    leaderboard_data = get_leaderboard()
    return [
        LeaderboardEntry(
            name=entry["name"], score=entry["score"], timestamp=entry["timestamp"]
        )
        for entry in leaderboard_data
    ]


@app.get("/top3", response_model=list[LeaderboardEntry])
async def get_top_three_route():
    """Get the top three users"""
    top_three_data = get_top_three()
    return [
        LeaderboardEntry(
            name=entry["name"], score=entry["score"], timestamp=entry["timestamp"]
        )
        for entry in top_three_data
    ]


# For running the app directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
