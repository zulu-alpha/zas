FROM python:3.9

RUN python -m pip install poetry

# Install Python dev packages
COPY pyproject.toml /srv/app/
WORKDIR /srv/app
RUN poetry config virtualenvs.create false &&\
    poetry install --no-interaction --no-ansi

# Copy project in separate layer
COPY . /srv/app/
