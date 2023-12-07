FROM python:3.10

# Create directories and copy over
WORKDIR /fcfb

# Install everything
RUN apt-get install libmariadb3 libmariadb-dev
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y libmariadb-dev-compat
RUN apt-get install -y libmariadb-dev

# Copy config.json into the image
COPY config.json /fcfb/configuration/

# Install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run
CMD [ "python", "fcfb/main/rotom.py" ]
