# Base image
FROM python:3.11-slim

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Gurobi license file
COPY gurobi.lic .

# Copy source code
COPY . .

# Expose backend port
EXPOSE 5000

# Set environment variables (can also be done via docker-compose)
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Start the Flask development server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
