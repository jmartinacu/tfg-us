FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg curl libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . /app/

RUN chmod +x /app/launch.sh /app/populate.sh

EXPOSE 8000

CMD ["python", "manage.py",  "runserver"]
