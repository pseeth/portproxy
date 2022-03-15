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

And that's it! The status of all the ports is at the top of this
page. You can reconnect all tunnels (say after closing your laptop
and opening it back up) by hitting [Reconnect all](/reconnect).

### Have a link to forward?

If you have a full link to forward, you can use this utility to automatically open the forwarded, local version:

```
python -m portproxy.forward [machine_name] [link]
```

The link will be opened in your browser if possible via the `open` command on MacOS. Otherwise the link will be displayed in your terminal to open up.