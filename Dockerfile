FROM python:3.9-slim as base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

FROM base as build

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential

RUN pip install pipenv
COPY Pipfile ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM build as runtime
COPY --from=build /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN useradd reddrop-user -m
WORKDIR /reddrop
RUN chown reddrop-user:reddrop-user .
USER reddrop-user

COPY . .

VOLUME [ "/reddrop/uploads", "/reddrop/logs" ]

ENTRYPOINT [ "python", "reddrop-server.py" ]