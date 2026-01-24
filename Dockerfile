FROM python:3.11-slim

WORKDIR /app

COPY src/ src/
COPY InputFiles/ InputFiles/
RUN mkdir -p OutputFile

CMD ["python3", "src/wordcloud.py"]