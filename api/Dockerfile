FROM python:3.12.2-slim
WORKDIR /app/api
COPY ./ .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app"]
