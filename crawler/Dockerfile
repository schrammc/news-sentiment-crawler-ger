# Use an official Python runtime as a parent image
FROM python:3.12.2-slim

# Set the working directory in the container
WORKDIR /app/crawler

# Copy the web crawler application code and requirements file into the container
COPY ./ .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
