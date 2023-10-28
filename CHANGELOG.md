# CHANGELOG



## v0.4.0 (2023-10-28)

### Ci

* ci: stop testing against windows

until we figure out why installing pyrepl fails with:
```
  � Installing werkzeug (3.0.1)

  ChefBuildError

  Backend &#39;setuptools.build_meta:__legacy__&#39; is not available.

  at ~\AppData\Roaming\pypoetry\venv\lib\site-packages\poetry\installation\chef.py:147 in _prepare
      143|
      144|                 error = ChefBuildError(&#34;\n\n&#34;.join(message_parts))
      145|
      146|             if error is not None:
    &gt; 147|                 raise error from None
      148|
      149|             return path
      150|
      151|     def _prepare_sdist(self, archive: Path, destination: Path | None = None) -&gt; Path:

Note: This error originates from the build backend, and is likely not a problem with poetry but with pyrepl (0.9.0) not supporting PEP 517 builds. You can verify this by running &#39;pip wheel --use-pep517 &#34;pyrepl (==0.9.0)&#34;&#39;.

Error: Process completed with exit code 1.
``` ([`1d70cc8`](https://github.com/dskard/manageritm/commit/1d70cc8ce8cd52d9f81834429bbbf52fac17b31d))

### Feature

* feat: user can specify flags to proxy, and specify command

When using the /client/proxy endpoint, users can send additional command
line options to the proxy command. In the data sent with the request,
provide a key named `additional_flags` and a value that is a list of
flags to be appended to the default command.

Example:

```
{
   ...
   &#39;additional_flags&#39;: [&#39;--opt1&#39;,&#39;value1&#39;,&#39;--opt2&#39;,&#39;value2&#39;]
}
```

When using the /client/command endpoint, users can set the command to
run. In the data sent with the request, provide a key named `command`
and a value that that is a list version of the command to run.

Example:

```
{
   ...
   &#39;command&#39;: [&#39;sleep&#39;,&#39;200000000000&#39;]
}
```

Added test cases for the new features.

Updating Makefile to use `pyenv virtualenv-delete` to delete the virtual
environment instead of `pyenv uninstall`. Also, I think the hooks are
properly being created in pyenv now, so we don&#39;t need to install black,
pytest, and pdbpp outside of poetry. We can run `poetry install` to get
all of the pieces installed. ([`0aea355`](https://github.com/dskard/manageritm/commit/0aea3551e20b7f41ac178e59d602faff7ecc632b))

### Fix

* fix: update dependency versions ([`952cc54`](https://github.com/dskard/manageritm/commit/952cc541379e174cebc2eaa817e698541e5661e1))

### Unknown

* Merge pull request #6 from dskard/dsk-update-client-proxy-and-command-route-parameters

update client proxy and command route parameters ([`f3675bb`](https://github.com/dskard/manageritm/commit/f3675bbad81b2d30b865aa2400c90c78c0eecb42))


## v0.3.0 (2023-08-06)

### Ci

* ci: upgrade python-semantic-release, fix pypi publishing ([`bd677db`](https://github.com/dskard/manageritm/commit/bd677db335c71ae991647899e87482216d0e4619))

### Feature

* feat: remove manageritm client library

the client library is in a separate library, manageritm-client.
this allows people to install the client without needing the
dependencies of the server. ([`f967eff`](https://github.com/dskard/manageritm/commit/f967eff12fcef4cbd62f3088156e6cef01bbec23))

### Unknown

* Merge pull request #5 from dskard/dsk-remove-client

feat: remove manageritm client library ([`a14ba0d`](https://github.com/dskard/manageritm/commit/a14ba0db976b30eddb08569edc824c49370b0ec5))


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
