FROM python:3.10

# Create directories and copy over
WORKDIR /fcfb
COPY ./requirements.txt ./
COPY . .

# Install everything
RUN apt-get install libmariadb3 libmariadb-dev
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y libmariadb-dev-compat
RUN apt-get install -y libmariadb-dev

# Copy config.json into the image
COPY config.json /project/fcfb/configuration/

# Install python dependencies
RUN pip install -r requirements.txt

RUN ls -R /

# Run
CMD [ "python", "main/rotom.py" ]
