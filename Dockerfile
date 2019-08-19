FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY app/requirements.txt /app/
ADD app/requirements.txt /app/

# Install requirements
RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

EXPOSE 8008

CMD ["bash"]
#CMD ["python", "package.py"]