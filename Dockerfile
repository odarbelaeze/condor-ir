FROM python:3.6

WORKDIR /src/app

ADD . /src/app
RUN pip install -r requirements.txt
RUN pip install .
RUN python -m nltk.downloader snowball_data
RUN python -m nltk.downloader stopwords
RUN condor utils preparedb -y

