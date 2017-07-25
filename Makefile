BASEDIR=$(CURDIR)

help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make publish                       Push to master branch               '
	@echo '   make push                          Push to dev branch					 '
	@echo '                                                                          '

publish:
	git add --update
	git commit -m 'Automaitc update.' 
	git push origin master

push:
	git add --update 
	git commit -m 'Automatic update.' 
	git push origin dev

dependencies:
	pip install -r requirements.txt

travis:
	travis restart
	travis logs
