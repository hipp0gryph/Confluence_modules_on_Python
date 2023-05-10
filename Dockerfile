FROM alpine:3.17
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["sleep", "infinity"]
