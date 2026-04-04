# Build
FROM ubuntu:24.04

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

RUN mkdir /code/
WORKDIR /code/

COPY uv.lock pyproject.toml app.py /code/

# isolated for caching (long bpy, numpy build etc..)
RUN uv add bpy

RUN uv sync --locked

# Post-build & run
COPY generate_cad_part.py chocolate_biscuit_CAD_part.blend ChocolateHeightmap_input.png /code/

RUN mkdir -p /code/output/
RUN mkdir -p /code/uploads/

EXPOSE 8037

CMD ["uv", "run", "app.py"]
