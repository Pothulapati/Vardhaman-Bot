FROM utorai/botbase
ADD . /xbot
EXPOSE 8080
CMD ["pipenv", "run", "python", "./bot/main.py"]