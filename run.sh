#!/bin/bash

docker build -t BragJetLag .
docker run -d -p 5000:5000 --env-file .env BragJetLag
