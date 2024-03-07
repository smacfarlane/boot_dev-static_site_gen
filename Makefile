default: test

generate:
	@python src/main.py
serve:
	@python server.py --dir public
test:
	@python -m unittest discover -s src


