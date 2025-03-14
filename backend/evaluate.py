import csv
import random
import os
import json
from typing import Dict, List, Tuple, Any, Optional
import pydantic
from typing import Literal, List, Tuple, Optional, Dict, Any
from pydantic import BaseModel
from models import OpenAIResponse
import os
from openai import OpenAI


client = OpenAI()
OpenAI.api_key = os.getenv(
    "OPENAI_API_KEY",
)


def load_questions(filename: str) -> dict[str, str]:
    """Load questions and classifications from CSV file"""
    questions = {}

    if not os.path.exists(filename):
        return questions

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                questions[row[0]] = row[1]

    return questions


def call_openai_api(
    user_input: str, questions: List[Tuple[str, str]]
) -> Dict[str, Dict[str, str]]:
    """
    Call the OpenAI API with the user's input and questions

    Args:
        user_input: The user's input text
        questions: List of (question, classification) tuples

    Returns:
        The OpenAI API response as a dictionary, or None if the call fails
    """
    try:
        # Prepare messages for the API
        results = {}
        # Add each question as a user message
        for i, (question, _) in enumerate(questions.items()):
            system_message = [
                {
                    "role": "system",
                    "content": f"{user_input}",
                },
                {
                    "role": "user",
                    "content": f"{question}",
                },
            ]

            # Make the API call using the openai package
            response = client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=system_message,
                response_format=OpenAIResponse,
            )
            classification = json.loads(response.choices[0].message.content)["response"]
            # switch the word response to the question

            results[str(i)] = {
                "classification": classification,
                "question": question,
            }

        return results

    except Exception as e:
        print(f"Exception when calling OpenAI API: {str(e)}")
        return None


def parse_openai_response(
    response: dict[str, dict[str, str]], questions: dict[str, str]
) -> Dict[str, Dict[str, Any]]:
    """
    Parse the OpenAI API response to extract classifications and correctness

    Args:
        response: The OpenAI API response
        questions: List of (question, classification) tuples

    Returns:
        A dictionary with results for each question
    """
    results = {}
    try:
        for key, value in response.items():
            classification = value["classification"]
            question = value["question"]
            correct = classification == questions[question].strip()
            results[key] = {
                "question": question,
                "classification": classification,
                "correct": correct,
            }
    except Exception as e:
        print(f"Exception when parsing OpenAI API response: {str(e)}")
        results = {}

    return results


def evaluate(system_prompt: str) -> Dict[str, Dict[str, Any]]:
    """
    Evaluate free text against known questions using OpenAI API.
    If API call fails, falls back to random classifications.

    Args:
        system_prompt: The free text input from the user

    Returns:
        A dictionary mapping question keys to evaluation results
    """
    check_questions = load_questions("data/check_questions.csv")

    response: dict[str, dict[str, str]] = call_openai_api(
        system_prompt, check_questions
    )

    # Parse the response
    if response:
        parsed_data = parse_openai_response(response, check_questions)
        return parsed_data

    # Fallback to random results if API call is not possible or fails
    results = {}
    for key, value in check_questions.items():
        results[key] = {
            "question": key,
            "classification": "?",
            "correct": False,
        }

    return results
