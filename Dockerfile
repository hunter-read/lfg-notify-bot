FROM python:3.9 AS builder
WORKDIR /code
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt
RUN pip install pytest flake8

# Run tests
COPY src/ .
COPY ./dev/praw.ini .
COPY ./dev/database/lfg_tables.db .
ENV DATABASE=/code/lfg_tables.db
ENV PROFILE=development
RUN python3 -m pytest
RUN python3 -m flake8 . --count --exit-zero --max-complexity=10  --statistics --ignore=E501

# second unnamed stage
FROM python:3.9-slim
WORKDIR /code

COPY src/ .

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
