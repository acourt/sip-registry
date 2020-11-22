FROM python:3.9.0-alpine3.12
COPY . /usr/local/sbin/sip-registry-server
WORKDIR /usr/local/sbin/sip-registry-server
# RUN pip install -r requirements.txt
EXPOSE 8888
CMD python src/SipRegistryServer.py
