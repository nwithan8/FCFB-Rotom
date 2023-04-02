FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD fcfb_pong.py /
CMD [ "python", "./pong/fcfb_pong.py" ]