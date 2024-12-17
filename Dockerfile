FROM python:3.9-slim as base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

ARG UID=1000
ARG GID=1000

FROM base as build

RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential

RUN groupadd -g ${GID} reddrop-group && \
    useradd -u ${UID} -g reddrop-group -m -s /bin/bash reddrop-user

RUN pip install pipenv
WORKDIR /app
COPY Pipfile ./
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM build as runtime
COPY --from=build /app/.venv /.venv
ENV PATH="/.venv/bin:$PATH"
WORKDIR /reddrop
COPY --chown=reddrop-user:reddrop-group ./ ./

RUN mkdir -p uploads logs
RUN chown -R reddrop-user:reddrop-group ./
USER reddrop-user

VOLUME [ "/reddrop/uploads", "/reddrop/logs" ]

ENTRYPOINT [ "python", "reddrop-server.py" ]
