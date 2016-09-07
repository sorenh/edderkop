#!/bin/sh

if [ "$1" == "web" ]
then
    FLASK_APP=edderkop.web exec flask run -h 0.0.0.0
fi

exec edderkop "$@"
