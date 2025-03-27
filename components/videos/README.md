# Videos

Video Components

## Development

### Setup Virtual Environment

Windows
```
cd components\videos
python -m venv .venv
.venv\Scripts\activate
```

Linux:
```
cd components/videos
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
