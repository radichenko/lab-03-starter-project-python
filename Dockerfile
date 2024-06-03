FROM python:3.10-alpine
WORKDIR /app
COPY requirements/backend.freeze.in requirements/backend.freeze.in
RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements/backend.freeze.in
COPY . .
CMD [".venv/bin/python", "-m", "uvicorn", "spaceship.main:app", "--host=0.0.0.0", "--port=8080"]