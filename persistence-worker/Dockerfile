FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    RUNNING_IN_DOCKER=true

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential openjdk-17-jdk ca-certificates \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN java -version

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Path for Spark dependencies jars
RUN mkdir -p /opt/spark-jars

# Downloading Spark dependencies jars
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar /opt/spark-jars/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar /opt/spark-jars/
ADD https://repo1.maven.org/maven2/software/amazon/awssdk/bundle/2.31.5/bundle-2.31.5.jar /opt/spark-jars/
ADD https://repo1.maven.org/maven2/io/netty/netty-transport-native-epoll/4.1.119.Final/netty-transport-native-epoll-4.1.119.Final.jar /opt/spark-jars/

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

COPY . .

CMD ["python", "src/__main__.py"]