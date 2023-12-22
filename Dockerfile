FROM python:3.11-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install -y gcc python3-dev
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY prod.env /code/prod.env
ENV ENV_FILE="prod.env"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
