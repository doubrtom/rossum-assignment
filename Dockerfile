FROM python:3.8

# Install poppler-utils for pdf2image
RUN apt -y update && apt -y install poppler-utils

# set the working directory in the container
WORKDIR /code

# upgrade pip + install pipenv
RUN pip install --upgrade pip wheel
RUN pip install pipenv

# copy requirements and code
COPY Pipfile Pipfile.lock setup.py ./
COPY pdf_renderer/ ./pdf_renderer/

# Install dependencies
RUN pipenv install --dev

EXPOSE 5000
