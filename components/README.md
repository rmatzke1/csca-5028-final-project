# Components

## Setup Virtual Environment

```
Windows
------------------------------------
cd components
python -m venv .venv
.venv\Scripts\activate
pip install -r ..\requirements.txt
pip install -r requirements.txt

Mac/Linux
------------------------------------
cd components
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
pip install -r requirements.txt
```

## Unit / Integration Tests

Prepare the environment:
```
Windows
------------------------------------
cd components
.venv\Scripts\activate
set TEST_DATABASE_URI=postgresql+psycopg2://db_user:password@localhost:5432/movie_recaps_test

Mac/Linux
------------------------------------
cd components
source .venv/bin/activate
export TEST_DATABASE_URI=postgresql+psycopg2://db_user:password@localhost:5432/movie_recaps_test
```

You can now run the unit / integration tests:
```
coverage run -m unittest discover
```

After you run the tests, you can use these commands for more details:
```
coverage report -m      # Print report
coverage html           # Generate HTML report
```
