FROM python:3.10-alpine3.19

WORKDIR /app

RUN apk upgrade --no-cache

COPY ./backend/pyproject.toml /app/

RUN pip install .

COPY ./backend/ /app/

ENTRYPOINT [ "./entrypoint.sh" ]