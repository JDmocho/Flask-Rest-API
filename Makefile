deps:
		pip install -r requirements.txt

postman:
		postman

run:
		flask run

tests:
		python -m pytest -vv