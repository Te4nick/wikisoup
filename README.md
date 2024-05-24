# WIKISOUP

## Run in Docker Compose

- Clone repository
- Run Docker Compose
  ```shell
  $ docker compose -p "wikisoup" up -d
  ```

## Run locally
- Clone repository
- Create venv (https://docs.python.org/3/tutorial/venv.html)
  ```shell
  $ python3 -m venv .venv
  ```
- Activate venv (https://docs.python.org/3/tutorial/venv.html)
  - Windows
    ```shell
    $ .\.venv\Scripts\activate
    ```
    - Unix or MacOS
    ```shell
    $ source ./.venv/bin/activate
    ```
- Install dependencies
  ```shell
  $ pip install ./backend
  ```
- Make Django migrations
  ```shell
  $ python3 backend/manage.py makemigrations
  ```
  ```shell
  $ python3 backend/manage.py migrate
  ```
- Run Django Development server
  ```shell
  $ python3 backend/manage.py runserver
  ```
- To use with frontend change line below in `frontend/script.js` 
  to desired address (don't forget port) and open `frontend/index.html` in browser
  ```javascript
  const api_addr = "http://127.0.0.1/"
  ```