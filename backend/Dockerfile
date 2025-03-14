# Use the official Python image from the Docker Hub
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and uv.lock files into the container
COPY pyproject.toml uv.lock ./

# Install uv
RUN pip install uv

# Install the dependencies using uv
RUN python -m uv sync

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]