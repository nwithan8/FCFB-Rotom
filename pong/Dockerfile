FROM python:3.10
ADD requirements.txt /
RUN apt-get install libmariadb3 libmariadb-dev
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install -y libmariadb-dev-compat
RUN apt-get install -y libmariadb-dev
RUN pip install -r requirements.txt
ADD fcfb_pong.py /
CMD [ "python", "./fcfb_pong.py" ]