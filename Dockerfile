# Multi-stage build for React + FastAPI on Hugging Face Spaces
# 用于在 Hugging Face Spaces 中同时运行 React 前端和 FastAPI 后端

# Stage 1: Build React frontend
FROM node:18-alpine AS react-builder

WORKDIR /frontend

# Copy frontend files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source
COPY frontend/public ./public
COPY frontend/src ./src

# Build React app for production
RUN npm run build

# Stage 2: Final image with Python FastAPI backend and static React frontend
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements
COPY requirements.txt .

# Install Python dependencies
# Install CPU-only torch first to reduce image size for Hugging Face Spaces
RUN pip install --no-cache-dir torch==2.1.2 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python application
COPY . ./

# Copy built React frontend from builder stage
COPY --from=react-builder /frontend/build ./frontend/build

# Create required directories
RUN mkdir -p data logs config

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Hugging Face Spaces uses port 7860
EXPOSE 7860

# Start FastAPI server (which also serves the React frontend)
CMD ["python", "api.py"]
