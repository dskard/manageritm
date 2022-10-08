# manageritm

Manage a mitmproxy service on another system over a RESTful API

## Getting Started

1. Install manageritm.
   ```python
   pip install manageritm gunicorn
   ```
2. Start manageritm server on port 8000.
   ```python
   gunicorn --bind 0.0.0.0:8000 --workers 1 --log-level debug "manageritm.app:main()"
   ```
3. In Python, create a client, start the mitmproxy service, stop the mitmproxy service
   ```python

   import manageritm

   manageritm_addr = "localhost"
   manageritm_port = "8000"

   # create a manageritm client
   mc = manageritm.client.ManagerITMClient(f'http://{manageritm_addr}:{manageritm_port}')
   proxy_details = mc.client()

   print(f"proxy port: {proxy_details['port']}")
   print(f"proxy webport: {proxy_details['webport']}")

   # start a proxy server
   mc.proxy_start()

   # set your application to use the proxy
   #  host: "localhost"
   #  port: f"{proxy_details['port']}"

   # do some work...

   # stop the proxy server
   mc.proxy_stop()
   ```

## Local Development

1. Check out this repository
2. Create a virtual environment
   ```bash
   make pyenv
   ```
3. Install Python dependencies
   ```bash
   make install
   ```
4. Start the server
   ```bash
   make server
   ```
5. Start a client, in a Python interpreter:
   ```python

   import manageritm

   manageritm_addr = "localhost"
   manageritm_port = "8000"

   # create a manageritm client
   mc = manageritm.client.ManagerITMClient(f'http://{manageritm_addr}:{manageritm_port}')
   proxy_details = mc.client()

   print(f"proxy port: {proxy_details['port']}")
   print(f"proxy webport: {proxy_details['webport']}")

   # start a proxy server
   mc.proxy_start()
   ```
6. Navigate a web browser to `http://localhost:<proxy webport>` to watch the traffic
7. Configure a web browser to use the proxy port.
8. Stop the client
   ```python
   # stop the proxy server
   mc.proxy_stop()
   ```


### Helpful Commands

To build a package for the development version:
```python
make all
```

To install a copy into your local python virtualenv
```python
make install
```

To run the test cases:
```python
make test
```

To run the development version of the service:
```python
make run
```
