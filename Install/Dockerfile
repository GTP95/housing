FROM ubuntu:22.04
LABEL authors="giacomo"
RUN apt-get update && apt-get -y upgrade && apt-get -y install python3 python3-pip
RUN pip3 install pytest-playwright
RUN playwright install
RUN playwright install-deps
COPY . /housing
RUN pip3 install -r /housing/requirements.txt
ENTRYPOINT ["/bin/python3", "-u", "/housing/main.py"]