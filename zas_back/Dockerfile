FROM python:3.8

COPY . /srv/zas_back
WORKDIR /srv/zas_back

RUN python -m pip install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT ["/srv/zas_back/runserver.sh"]