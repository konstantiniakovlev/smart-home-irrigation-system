FROM python:3.9
LABEL authors="Konstantin"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY src/. src/.


CMD ["python", "src/main.py"]
