# Hedge

Hedge is a provision automation library based on Python language.

## Requirements

1. python v2 or higher    

2. python paramiko library
    ```
    sudo apt install python3-paramiko
    ```

3. python scp library
    ```
    sudo apt install python3-scp
    ```

## Executing 

1. clone hedge to machine where you want to run it

    git clone https://github.com/hedge

2. go to source folder

    cd ./hedge/src

3. run target from repository

    TODO

## How to run tests

1. start container
    ```
    docker-compose up --build -d
    ```
2. get into container
    ```
    docker-exec -it c-hedge-master /bin/bash
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
