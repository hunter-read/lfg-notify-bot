FROM python:3.11 AS builder

WORKDIR /code
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r requirements.txt

# second unnamed stage
FROM python:3.11-slim
LABEL maintainer="hunter@readpnw.dev"

WORKDIR /code

COPY src/ .

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
