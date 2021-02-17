# PortProxy

**TL;DR: Start and manage ssh tunnels just by browsing to easily-remembered URLs.**

`ssh -N -f -L 8888:localhost:8888 you@machine` -> `http://[portproxy]/machine1/8888`.


![Example Image of PortProxy](/images/interface.png)


PortProxy is a simple service for forwarding ports dynamically 
upon request from machine names found in your ssh config file.
Here's how it works. Say you have a config file in your ssh
that looks like this:

```
Host machine1
    HostName machine1.internet.com
    User you

Host machine1
    HostName machine2.internet.com
    User you
```

You might want port `8888` from both `machine1` and `machine2` (e.g.
you have a Jupyter notebook running on both). So, what you would
normally do is something like this:

```
ssh -L 8888:localhost:8888 machine1
ssh -L 8888:localhost:8889 machine2
```

and so on for each machine. If you have a lot of machines, the above
method can get a bit cumbersome. So, PortProxy handles all of this
under the hood. Your mental model of all of the ports on all remote
machines becomes like this:

```
[PortProxy_url]/[machine_name]/[forwarded_port]
```

For example, to get on port `8888` on `machine1`, navigate to 
`localhost:5000/machine1/8888` in your browser, if `PortProxy` 
is running on `localhost:5000`.

And that's it!

# Installation

```
pip install portproxy
```

# Usage

Just run the server, one of two ways:

```
❯ python -m portproxy
 * Serving Flask app "portproxy.portproxy" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 308-152-645
```

or via

```
❯ portproxy
 * Serving Flask app "portproxy.portproxy" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 308-152-645
```

Then navigate to `http://127.0.0.1:5000/ `, and happy forwarding!

# Releasing

Do the following steps:

```
python setup.py sdist
```

Upload it to test PyPI:

```
pip install twine
twine upload --repository testpypi dist/*
pip install -U --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple -U portproxy
```

Make sure you can install it and it works (e.g. run the examples). Now upload
to actual PyPI:

```
twine upload dist/*
```
