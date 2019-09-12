# Report bot

## Installation

* Install Docker
* Install docker-compose
* Run `docker-compose build` from top dir
* Wait
* Run `docker-compose up`
* Open `http://localhost:5000`
* Profit

## Developers guide
```bash
# install project dependencies
pip install -r app/dev-requirements.txt

# create database (only first time, in development mode creates sqlite3 file) before go to app directory
cd app
python manage.py db init

# initialize new migrations (the command creates new migrations file)
python manage.py db migrate

# apply migrations to database
python manage.py db upgrade

# set WEBHOOK_HOST env variable in ~/.bashrc
export WEBHOOK_HOST='somelongrandomname.serveo.net'

# run proxy server in another terminal tab (you can use webhooks after that)
ssh -R $WEBHOOK_HOST:443:localhost:5000 serveo.net

# run main app and bot with one command
python manage.py runserver
```

## Further improvements

[Use proper folder structure](https://github.com/hack4impact/flask-base)
Add DB support:
* [check this](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart)
* [or this](https://github.com/mehemken/docker-flask-postgres/blob/master/app/app.py)
