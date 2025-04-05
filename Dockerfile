FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y ffmpeg curl libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . /app/

RUN chmod +x /app/deploy.sh /app/populate.sh

EXPOSE 8000

CMD ["python", "manage.py",  "runserver"]
