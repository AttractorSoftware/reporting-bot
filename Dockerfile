FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/
ADD requirements.txt /code/

# Install requirements
RUN pip install --upgrade pip

RUN pip install -r /code/requirements.txt

EXPOSE 8008

CMD ["bash"]
#CMD ["python", "package.py"]