
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
    docker-compose run up -d
    ```
