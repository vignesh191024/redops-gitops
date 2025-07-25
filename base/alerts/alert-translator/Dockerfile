FROM registry.access.redhat.com/ubi8/python-311

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY translate.py .

ENTRYPOINT ["python", "-u", "translate.py"]

