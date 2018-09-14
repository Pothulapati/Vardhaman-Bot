.PHONY: help install install-dev train start

help:
	@/bin/echo -e "Commands:\n"
	@/bin/echo -e "\e[1m\e[31m  install     \e[0m Resolves all project dependencies using"
	@/bin/echo -e "               pipenv.\n" 
	@/bin/echo -e "\e[1m\e[32m  install-dev \e[0m Resolves both project dependencies and "
	@/bin/echo -e "               developer dependencies using pipenv.\n"
	@/bin/echo -e "\e[1m\e[33m  env         \e[0m Activates the virtual environment      "
	@/bin/echo -e "               created by pipenv.\n"
	@/bin/echo -e "\e[1m\e[34m  train       \e[0m Trains your NLP models with the desired"
	@/bin/echo -e "               data using the components in the"
	@/bin/echo -e "               Rasa NLU pipeline.\n"
	@/bin/echo -e "\e[1m\e[35m  run         \e[0m Starts your bot server."
	@/bin/echo -e "               (Stop the server with an interrupt)."

install:
	pipenv install --skip-lock

install-dev:
	pipenv install --dev --skip-lock

env:
	pipenv shell

train:
	python -m rasa_nlu.train -c bot/config/rasa.yml --data bot/data/rasa.md -o models --fixed_model_name nlu --project current --verbose

run:
	python bot/main.py