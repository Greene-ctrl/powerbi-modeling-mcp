# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 user

# Set up working directory
WORKDIR /home/user/app

# Change ownership of the app directory
RUN chown user:user /home/user/app

# Switch to non-root user
USER user

# Set environment variables
ENV PATH="/home/user/.local/bin:/home/user/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy the application code
COPY --chown=user . .

# Remove existing venv if any and install dependencies
RUN rm -rf .venv && uv venv && uv pip install .

# Expose the port Hugging Face expects
EXPOSE 7860

# Command to run the application
CMD ["python", "-m", "app.main"]
