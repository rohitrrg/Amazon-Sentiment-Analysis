FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the entire application code to the container
# This includes app.py, fine_tuned_sentiment_model, etc.
COPY . /app

# Copy requirements.txt and install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]