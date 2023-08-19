FROM python:3.11.3-slim-bullseye
RUN adduser --disabled-password --gecos "" anna && \
    chown -R anna /home/anna && \
    pip install poetry
USER anna
WORKDIR /home/anna
COPY pyproject.toml .
RUN poetry install --no-root
COPY . .
CMD ["poetry", "run", "python", "run.py"]
