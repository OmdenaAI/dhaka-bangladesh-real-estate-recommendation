FROM python:3.11
COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./app /app

CMD ["streamlit", "run", "/app/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]

