FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
# This includes app.py, fine_tuned_sentiment_model, etc.
COPY /src /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]