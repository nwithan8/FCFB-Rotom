FROM python:3.10

# Create directories and copy over
WORKDIR /project
COPY ./requirements.txt ./
COPY /fcfb ./fcfb

# Install everything
RUN apt-get install libmariadb3 libmariadb-dev
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y libmariadb-dev-compat
RUN apt-get install -y libmariadb-dev

# Install python dependencies
RUN pip install -r requirements.txt

# Define python path

ENV PYTHONPATH=.

# Run
CMD [ "python", "fcfb/main/rotom.py" ]
