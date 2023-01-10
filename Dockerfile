FROM python:3.9


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    make \
    wget \
    ffmpeg \
    libsm6 \
    libxext6


WORKDIR /planet_service

COPY . /planet_service/

RUN pip install poetry && poetry --version && poetry config virtualenvs.in-project true && poetry install -vv --no-root && rm -rf ~/.cache/pypoetry/{cache,artifacts}

CMD make run