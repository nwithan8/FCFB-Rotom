FROM python:3.10

# Create directories and copy over
RUN mkdir /project
WORKDIR /project
COPY ./requirements.txt ./
COPY ./pong/. /pong/

# Install everything
RUN apt-get install libmariadb3 libmariadb-dev
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y libmariadb-dev-compat
RUN apt-get install -y libmariadb-dev
RUN pip install -r requirements.txt
ADD pong/fcfb_pong.py /

# Run
CMD [ "python", "/pong/fcfb_pong.py" ]