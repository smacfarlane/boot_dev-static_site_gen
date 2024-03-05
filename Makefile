default: test

serve:
	@python src/main.py

test:
	@python -m unittest discover -s src
