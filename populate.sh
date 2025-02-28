#!/bin/bash

set -e

if [ $# -ne 1 ]; then
    echo "Data loading script requires a single argument: the name of the settings file to use 'local' or 'prod'"
    exit 1
fi

FIXTURES=(
    "groups.json"
    "users.json"
    "posts.json"
    "sources.json"
    "comments.json"
    "tags.json"
    "profile.json"
    "answers.json"
    "questions.json"
)

echo "Beginning to load data"

for fixture in "${FIXTURES[@]}"; do
    echo "Loading data from $fixture"
    python manage.py loaddata $fixture --settings="samer.settings.$1"
done

echo "Data loaded successfully"