FROM registry.redhat.io/openshift4/ose-cli:latest
USER 0

RUN yum install -y python3-pip && yum clean all

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "/app/consumer.py"]

