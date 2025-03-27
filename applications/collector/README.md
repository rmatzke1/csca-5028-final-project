# Collector

Data Collection Job

## Development

### Setup Virtual Environment

Windows
```
cd applications\collector
python -m venv .venv
.venv\Scripts\activate
```

Linux:
```
cd applications/collector
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

Windows:
```
pip install -r ..\..\requirements.txt
pip install -r requirements.txt
```

Linux
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
