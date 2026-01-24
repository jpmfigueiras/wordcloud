FROM python:3.11-slim

WORKDIR /app

COPY Script/ Script/
COPY InputFiles/ InputFiles/
RUN mkdir -p OutputFile

CMD ["python3", "Script/word_cloud.py"]
