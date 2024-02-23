FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
  git \
  gcc \
  g++ \
  libgdal-dev \
  pdal \
  && rm -rf /var/lib/apt/lists/*

RUN pip install pdal

COPY . /usr/src/app

RUN pip install poetry

COPY project.toml poetry.lock* /usr/src/app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-dev

CMD ["poetry", "run", "ahn_cli", "$(ARGS)"]
