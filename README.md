# Hedge

Hedge is a provision automation library based on Python language.

## How to run tests

1. start container
    ```
    docker-compose up --build -d
    ```
2. get into container
    ```
    docker-exec -it c-hedge /bin/bash
    ```
3. go to test folder
    ```
    cd /tmp/hedge/test
    ```
4. run all tests
    ```
    python test.py
    ```

5. run specific test
    ```
    python test.py <testClass>.<testMethod>
    ```
