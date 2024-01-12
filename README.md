# py_june

Python help forum - a place where you can ask questions about python and get answers 
from other users.

![Tests](https://github.com/acman/py_june/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/acman/py_june/branch/main/graph/badge.svg)](https://codecov.io/gh/acman/py_june)


## Technologies
* Python
* Django
* Materialize
* PostgreSQL
* AWS
* Terraform
* Github Actions

## Setup
1. Install `pyenv` for managing python versions https://github.com/pyenv/pyenv?tab=readme-ov-file#installation
2. Install python version used in project  
    `pyenv install $(cat .python-version)`
3. Create virtual environment  
    `python -m venv venv`
4. Activate virtual environment  
    `source venv/bin/activate`
5. Install dependencies  
    `pip install -r requirements.txt`
6. Run migrations  
    `python manage.py migrate`
7. Load test data  
    `python manage.py loaddata categories.json`
8. Run server  
    `python manage.py runserver`
9. Open in browser http://localhost:8000
10. Create superuser for access to admin panel http://localhost:8000/admin  
    `python manage.py createsuperuser`

## Before commit
Autoformat code  
`make autofmt`  
Check code  
`make lint`   
Run tests  
`make test`

## Internalization
1. Install gettext  
    `brew install gettext`
2. Compile messages  
    `python manage.py compilemessages -l uk`

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contact
lambda.py.inc@gmail.com
