FROM mcr.microsoft.com/playwright/python:v1.42.0
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN playwright install --with-deps
CMD ["python", "GoodReadsGiveaway.py"]