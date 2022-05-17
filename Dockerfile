FROM python:3.8

# set the working directory in the container
WORKDIR /code

# upgrade pip + install pipenv
RUN pip install --upgrade pip wheel
RUN pip install pipenv

# copy requirements
COPY Pipfile Pipfile.lock ./

RUN pipenv install

EXPOSE 5000
