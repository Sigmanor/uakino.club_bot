# uakino.club_bot

A Telegram bot that sends random recommendations for movies, TV series, and cartoons based on data from [uakino](https://uakino.me).

## Table of Contents

- [uakino.club\_bot](#uakinoclub_bot)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Deployment](#deployment)
    - [Clone Repository and Install Dependencies](#clone-repository-and-install-dependencies)
    - [Environment Setup](#environment-setup)
    - [Running](#running)
    - [Docker](#docker)
    - [Docker Compose](#docker-compose)

## Description

This bot is designed for convenient access to random movie, TV series, and cartoon recommendations through Telegram. Using the API source [uakino.me](https://uakino.me), the bot provides a quick and easy way to find something interesting to watch.

## Features

- Random recommendations for movies, TV series, and cartoons.
- Easy setup and deployment.
- Docker integration for simplified deployment.

## Requirements

- Python 3.6 or higher.
- pip3 for installing dependencies.
- Telegram Bot API token.

## Deployment

### Clone Repository and Install Dependencies

```bash
git clone https://github.com/Sigmanor/uakino.club_bot.git
cd uakino.club_bot
pip3 install -r requirements.txt
```

### Environment Setup
Rename the `.env_example` file to `.env` and fill in the required data

### Running
To run the bot locally, use the following command:

```bash
python3 bot.py
```

### Docker

```bash
docker build -t uakino.club_bot .
docker run uakino.club_bot
```

### Docker Compose

```bash
docker compose up -d
```