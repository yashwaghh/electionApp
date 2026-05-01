# STAGE 1: Build the React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
# Copy dependency files
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
# Copy source code and build
COPY frontend/ ./
RUN chmod -R +x node_modules/.bin && npm run build

# STAGE 2: Build the Python Backend & Serve
FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./

# Create static directory and copy built frontend from Stage 1
RUN mkdir -p /app/static
COPY --from=frontend-builder /app/frontend/dist /app/static

# Expose port (Cloud Run sets the PORT env variable automatically)
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
