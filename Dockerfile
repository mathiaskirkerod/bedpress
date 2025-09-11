# Multi-stage build - Frontend first
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
ENV REACT_APP_API_URL=https://bedpress-krk4l.ondigitalocean.app
RUN npm run build

# Backend stage
FROM python:3.13-slim
WORKDIR /app

# Copy backend requirements and install dependencies
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

# Copy built frontend first (React build structure)
COPY --from=frontend-build /app/frontend/build ./

# Copy backend code
COPY backend/ ./
ENV REACT_APP_API_URL=https://bedpress-krk4l.ondigitalocean.app
# Expose port
EXPOSE 8000

# Run the backend server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]