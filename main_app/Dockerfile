# Build
FROM ubuntu:24.04

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

RUN mkdir /code/
WORKDIR /code/

COPY uv.lock pyproject.toml app.py .env* /code/

RUN uv sync --locked

# Post-build & run
RUN mkdir -p /code/output/

EXPOSE 8000

CMD ["uv", "run", "nanodjango", "run", "app.py", "--user=admin", "--password=Chocolate777"]

