# Multi-stage build - Frontend first
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Backend stage
FROM python:3.13-slim
WORKDIR /app

# Copy backend requirements and install dependencies
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend to be served by backend
COPY --from=frontend-build /app/frontend/build ./static

# Expose port
EXPOSE 8000

# Run the backend server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]