# Data Collector

Data Collection Application

## Development

### Setup Virtual Environment

Windows
```
cd applications\data-collector
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux
```
cd applications/data-collector
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

Windows
```
pip install -r ..\..\requirements.txt
pip install -r requirements.txt
```

Mac/Linux
```
pip install -r ../../requirements.txt
pip install -r requirements.txt
```

### Validation

The following commands can help with formatting, linting, tests, etc.

```
# Linting, formatting, etc.
black --check .
flake8 .
isort --check-only .
pyright .

# Unit tests
coverage run -m unittest discover
coverage report -m      # Print report
coverage html           # Generate HTML report
```

### Run

Windows
```
python src\main.py
```

Mac/Linux
```
python src/main.py
```
