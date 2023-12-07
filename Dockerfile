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

# Copy config.json into the image
COPY config.json /project/fcfb/configuration/

# Install python dependencies
RUN pip install -r requirements.txt

# Run
CMD [ "python", "fcfb/main/rotom.py" ]
