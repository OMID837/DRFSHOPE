FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /user/src/app
COPY requirements.txt requirements.txt
COPY . /user/src/app
RUN pip install -r requirements.txt



#FROM python:3.10
#ENV PYTHONUNBUFFERED=1
#WORKDIR /app
#COPY requirements.txt requirements.txt
#COPY . /app
#RUN pip install -r requirements.txt

