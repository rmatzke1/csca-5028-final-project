# Components

## Development

Open a new terminal before running the commands below.

### Setup Virtual Environment

Windows
```
cd components
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux
```
cd components
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

Windows
```
pip install -r ..\requirements.txt
pip install -r requirements.txt
```

Mac/Linux
```
pip install -r ../requirements.txt
pip install -r requirements.txt
```

### Validation

#### Unit Tests

```
coverage run -m unittest discover
coverage report -m      # Print report
coverage html           # Generate HTML report
```
