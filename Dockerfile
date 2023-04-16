FROM python:3.10
WORKDIR /core
COPY requriemnts.txt /core/
RUN pip install -r requirements.txt
COPY . /core
CMD python -OO core.py