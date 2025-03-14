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


@app.on_event("startup")
async def startup_event():
    """Initialize everything needed on startup"""
    init_db()
    ensure_data_dir()
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

    # Check the current number of tries
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT tries FROM scores WHERE name = ? ORDER BY timestamp DESC LIMIT 1",
        (name,),
    )
    row = cursor.fetchone()
    tries = row[0] if row else 0

    if tries >= 5:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Maximum number of tries exceeded",
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
        score=evaluation["score"], results=evaluation["results"], num_uses=tries + 1
    )
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
