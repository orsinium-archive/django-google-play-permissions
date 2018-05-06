
## Installation

```bash
pip install -e git+https://github.com/orsinium/django-google-play-permissions.git#egg=djgpp
```

## Usage

1. Add `djgpp` to `INSTALLED_APPS`.
1. Make your own view like into package's [views.py](djgpp/views.py).

## Run example

1. Build:
  ```bash
  ./build.sh
  ```
1. Run:
  ```bash
  ./run.sh
  ```
1. Serve to [localhost:8000](http://localhost:8000/)
1. Drop containers after all:
  ```bash
  ./clear.sh
  ```

## Run tests

1. Install tox:
  ```bash
  pip install tox
  ```
1. Run tox:
  ```bash
  tox
  ```
