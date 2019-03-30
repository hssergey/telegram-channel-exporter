Утилита для получения сообщений от телеграм-каналов и складывания их в папки. Используется совместно с софтом для постинга этих событий в другие социалки.

Установка

- установить python3 virtual environment:
sudo apt-get install python3-venv

- установить зависимости:
python3 -m venv venv
source venv/bin activate
pip3 install -r requirements.txt

- переименовать settings.py.template в settings.py и отредактировать (как минимум, прописать api_id и  api_hash)

- для запуска
python3 main.py

При первом запуске надо будет авторизоваться в Телеграме. Программа будет получать сообщения с каналов, на которые подписан данный телеграм аккаунт, и класть их в виде текстовых файлов формата channels/<chat_id>/<timestamp>.txt

