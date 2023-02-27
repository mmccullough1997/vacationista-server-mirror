#!/bin/bash

# Run chmod +x seed.sh in the terminal.
# run ./seed.sh in the terminal to run the commands

rm -rf vacationistaapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations vacationistaapi
python3 manage.py migrate vacationistaapi
python3 manage.py loaddata users
python3 manage.py loaddata articles
python3 manage.py loaddata recommendations
python3 manage.py loaddata highlights
python3 manage.py loaddata event_types
python3 manage.py loaddata expense_types
python3 manage.py loaddata transportation_types
python3 manage.py loaddata legs
python3 manage.py loaddata trips
python3 manage.py loaddata events
python3 manage.py loaddata expenses
python3 manage.py loaddata transportations
python3 manage.py loaddata trip_legs
