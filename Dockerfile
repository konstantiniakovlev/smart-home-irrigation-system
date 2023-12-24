FROM --platform=linux/arm/v8 python:3.9 as build
LABEL authors="Konstantin"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src/. src/.


CMD ["python", "src/main.py"]
