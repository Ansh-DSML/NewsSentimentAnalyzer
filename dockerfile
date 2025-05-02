# Use Python 3.12 as base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the application files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r deployment/requirements.txt

# Expose required ports (FastAPI 7860, Streamlit 7861)
EXPOSE 7860 7861

# Start FastAPI in the background and Streamlit in the foreground
CMD ["bash", "deployment/setup.sh"]
