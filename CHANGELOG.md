# CHANGELOG



## v0.2.0 (2023-08-06)

### Ci

* ci: bump github actions versions ([`c8caf30`](https://github.com/dskard/manageritm/commit/c8caf307623f9666e336e64254bad6fcbc0478a0))

### Feature

* feat: generalizing manageritm to support multiple clients

remove `proxy` from function names, variable names, and routes

adding a general command client and more configuration file options for
defining a custom command to launch.

also adding `&#34;pages&#34;: [{&#34;pageTimings&#34;: {}}],` to har_dump.py so the har
files that are generated can be loaded into firefox for reading.
https://bugzilla.mozilla.org/show_bug.cgi?id=1691240

updating dependency package versions.

convert client/proxy and client/command requests to POST

Convert the client requests from GET to POST so we can send json data to
the requests. This end point is creating something, so POST feels more
appropriate.

Performing parameter validation through jsonschema for /client/... end
points.

Updating test cases to make POST requests to /client/... end points.

Also, adding new test cases to cover i:
1. proxy client
2. command client
3. parameter validation using jsonschema ([`10bb2e9`](https://github.com/dskard/manageritm/commit/10bb2e9d6dcbc0eccfaaf498c38f58f1f159d1e5))

### Unknown

* Merge pull request #4 from dskard/dsk-generalized-manageritm

feat: generalizing manageritm to support multiple clients ([`586ea2b`](https://github.com/dskard/manageritm/commit/586ea2b6b02e8f859a311ae633f5dfa9ca940e9d))

* Merge pull request #3 from dskard/dsk-bump-github-actions-versions

ci: bump github actions versions ([`3a997ff`](https://github.com/dskard/manageritm/commit/3a997ff19dd9b6567092d22afa06d52ff36e17ff))


## v0.1.0 (2022-10-09)

### Ci

* ci: adding actions to make releases ([`4e71097`](https://github.com/dskard/manageritm/commit/4e71097aa1a692d83f490bfbe750ef7f85fb7c77))

### Feature

* feat: allows users to provide port and webport numbers for mitmweb

users can provide a port and webport number when creating a manageritm
client:
```python

mc = ManagerITMClient(base_uri)
proxy_details = mc.client(port=5200, webport=5201)
```

`proxy_details[&#39;port&#39;]` should be 5200
`proxy_details[&#39;webport&#39;]` should be 5201

users can direct their proxied applications to use port 5200
users can watch traffic by directing their web browser to port 5201 ([`26ced42`](https://github.com/dskard/manageritm/commit/26ced428c1e1319304730855f78d3d0d537d1b6f))

### Unknown

* Merge pull request #2 from dskard/dsk-user-provided-ports

feat: allows users to provide port and webport numbers for mitmweb ([`e66455d`](https://github.com/dskard/manageritm/commit/e66455d2b53c4773f515c1f0c5b17dd762e6d4d0))

* Merge pull request #1 from dskard/dsk-releases

ci: adding actions to make releases ([`4b0f097`](https://github.com/dskard/manageritm/commit/4b0f0972d3fdd9174142a82ebf1bcd39f926662b))

* add client destructor, update docs and Makefile

clean up the client when it is deleted.
update test cases to work with new destructor.

add some notes about how to run basic examples in README.md

update pyenv target in Makefile to use a pyenv virtual environment ([`28dc9da`](https://github.com/dskard/manageritm/commit/28dc9da249da82dee56d32a2c8097754ae80524a))

* misc cleanup, write process output to log file

in mitmproxy config file, return a 404 for mozilla and firefox requests
instead of killing the connection.

in Makefile, remove quotes from project name

in process_minder.py, write process stdout and stderr to a single log
file, also perform some cleanup when deleting the ProcessMinder object.

in conftest.py and test_process_minder.py, mock the opening of the
process_minder.py log file so the test cases don&#39;t create tons of log
files on disk every time they run. ([`623d543`](https://github.com/dskard/manageritm/commit/623d5433ded06b44db0b4ab4b7f6318736ebbfb3))

* cleanup tasks

don&#39;t fail when calling `make clean` and a directory doesn&#39;t exist.

send more details about the har file path back to the client. ([`008297c`](https://github.com/dskard/manageritm/commit/008297cf4f5d226c747ee4792f22336ad55321c1))

* adding example of using manageritm

launches:
1. manageritm server in a docker container
2. selenium grid and web browsers docker containers
3. example script in docker container

example script configures a web browser to talk to the manageritm
server, and launches the web browser. while browser is running, user can
interact with it through a vnc viewer. when the user is done, they send
a CTRL-C to the example script. the example script closes the web
browser and tells manageritm to shut down the proxy. ([`8802a38`](https://github.com/dskard/manageritm/commit/8802a38fbfd3326976af988db772b94b49e691fa))

* initial upload ([`da2563b`](https://github.com/dskard/manageritm/commit/da2563bea0e546c463828b9f94d4aa4cea4dc823))

* Initial commit ([`3b9a8cc`](https://github.com/dskard/manageritm/commit/3b9a8ccdfee7121708024859296d3e0631477d11))
