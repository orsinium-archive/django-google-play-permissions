
## Run example

1. Copy config example:
    ```bash
    cp example/settings/local{_example,}.py
    ```
1. Set up `ANDROID_EMAIL` and `ANDROID_PASSWORD` into config:
    ```bash
    nano example/settings/local.py
    ```
1. Run containers:
    ```bash
    docker-compose up -d
    ```

## Run tests

Set up credentials like in [Run example](#run-example) and run Django tests:

```bash
docker-compose run project python manage.py test djgpp
```
