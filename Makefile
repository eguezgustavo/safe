# A=$(which python3)
PYTHON_3_PATH=$(shell which python3)

install:	
	@echo \#!$(PYTHON_3_PATH) > /usr/local/bin/safe
	@pip install -r requirements.txt
	@cat ./safe.py >> /usr/local/bin/safe
	@chmod +x /usr/local/bin/safe
	echo "Safe is intalled, run safe --help to obtain details"

uninstall:
	rm /usr/local/bin/safe
	pip uninstall -r requirements.txt
	echo "Safe has been uninstalled"
