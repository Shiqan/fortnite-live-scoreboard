# We name the `base` stage so we can refence it in multiple later
# stages but only need to update it in one place if we change it
FROM python:3.7-slim AS base

WORKDIR /app
RUN pip install pipenv==2018.10.13

COPY Pipfile /app/
COPY Pipfile.lock /app/

RUN pipenv install --system --deploy


# The `app` stage is used as the base for images that don't
# need the development dependencies
FROM base AS app
COPY . /app


# The `test-base` stage is used as the base for images that require
# the development dependencies. The duplication of the COPY instruction
# avoids breaking the cache for that later when the Pipfile changes 
FROM base AS test-base
RUN pipenv install --system --deploy --dev
COPY . /app


# The `Test` stage runs the application unit tests, the build will fail
# if the tests fail. Note this stage name is capitalised, this is purely
# a convetion for stages which result in useful images. Think of it like
# hint that this is a public interface
# FROM test-base AS Test
# RUN pytest --black


# `release` acts as the basis for images which will actually run the application 
FROM app AS Release
EXPOSE 8888
CMD ["python", "server.py"]
