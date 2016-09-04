FROM python:3.5.1

WORKDIR /src/app

RUN apt-get update -y -q
RUN apt-get install -y -q postgresql postgresql-contrib
RUN apt-get install -y -q enchant aspell-es aspell-en aspell-fr aspell-it aspell-pt aspell-de
RUN echo "host  all  all 0.0.0.0/0 md5" >> /etc/postgresql/9.4/main/pg_hba.conf

COPY . /src/app
RUN pip install --quiet -r piprequirements.txt
RUN pip install .
RUN python -m nltk.downloader snowball_data
RUN python -m nltk.downloader porter_test
RUN python -m nltk.downloader stopwords


