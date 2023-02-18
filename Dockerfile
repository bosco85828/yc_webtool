FROM python:3.9.13

WORKDIR /bill_web

COPY . /bill_web

RUN apt-get update \
    && apt-get install -y apt-transport-https vim iproute2 net-tools ca-certificates curl wget software-properties-common  unzip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome*.deb \
    || apt-get -y -f install \ 
    && ln -s /usr/bin/google-chrome-stable /usr/bin/chrome \
    && rm google-chrome*.deb

RUN python -m pip install -r requirements.txt

CMD ["/bin/bash"]