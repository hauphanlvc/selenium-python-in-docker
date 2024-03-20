## ✨ Set up an environment for crawling a website using Selenium with Python in Docker

This repository is a guide to setting up an environment for crawling a website using Selenium with Python in Docker.

## ⚡️ Requirements

- Docker lastest Version
- Python 3.10.12 (Optional)

## 🚀 Getting Started

- Firstly, we need to build the image which was used to become the executed environment.

```bash
docker build -t selenium-python-in-docker-demo-app .
```

- To build the servers for Selenium:

```bash
docker compose up --scale chrome-node=3 # with 3 is chrome containters which wanna to create
or
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
```

- To run the demo script python:

```bash
docker run --rm -it -v .:/code/ --network "host" selenium-python-in-docker-demo-app bash
root@hau:/code# python scraping_data.py
```

## Note: If you got the error when running scraping_data.py OpenSSL.crypto.Error: [('PEM routines', '', 'no start line'), then just re-run again and that wil be fine.

## Optional

- To run demo script python in locally, just need to build the server for Selenium and Python 3.10.12 ( virtual environment package must be installed) above:

```bash
python3 -m venv env
source env/bin/activate
python3 scraping_data.py
```

- The repository could be improved for your project, feel free to use it. :)

## Authors

Hau Phan Trong
hauphanlvc@gmail.com
