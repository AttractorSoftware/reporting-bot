FROM python:3

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

COPY app/requirements.txt /app/
COPY app/dev-requirements.txt /app/
RUN pip install -r /app/dev-requirements.txt

EXPOSE 5000

CMD ["bash"]