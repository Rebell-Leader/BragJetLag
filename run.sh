#!/bin/bash

docker build -t flight-recommendations-chatbot .
docker run -d --name telegram_bot_container --env-file .env flight-recommendations-chatbot

