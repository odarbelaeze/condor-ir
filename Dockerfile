FROM python:3.6

WORKDIR /src/app

RUN apt-get update -y -q
RUN apt-get install -y -q enchant aspell-es aspell-en aspell-fr aspell-it aspell-pt aspell-de

ADD . /src/app
RUN pip install -r piprequirements.txt
RUN pip install -e .
RUN python -m nltk.downloader snowball_data
RUN python -m nltk.downloader porter_test
RUN python -m nltk.downloader stopwords

