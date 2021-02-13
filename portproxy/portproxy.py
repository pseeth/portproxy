from flask import Flask, redirect
import dominate
from dominate.util import raw
from dominate.tags import *
import marko
import portpicker
from pathlib import Path
import sshtunnel
import signal
import sys
import argbind

app = Flask(__name__)
ports = {}
#
# ports is a dict that looks like this
# {
#   'machine_name:port': {
#       'machine_name': machine_name,
#       'remote_port': port,
#       'tunnel': tunnel, 
#       'local_port': picked_port, 
#       'link': local_link
#    }
# }
#
app_file_path = Path(__file__).parent

def _read_file(path):
    with open(str(path), 'r') as f:
        data = f.read()
    return data

HEADERS = [
    "Status",
    "Machine", 
    "Port", 
    "Proxy url", 
    "Actual url",
    "Stop",
    "Reconnect",
    "Delete",
]

@app.route('/')
def home():
    readme = _read_file(app_file_path / "static/home.md")
    css = _read_file(app_file_path / "static/style.css")
    doc = dominate.document(title='PortProxy')

    with doc.head:
        style(css)

    with doc: 
        h1("PortProxy")
        h2("Status")
        h3(a("Reconnect all", href="/reconnect"), " |", a("Stop all", href="/stop"))

        _table = table()
        with _table.add(tbody()):
            with tr():
                for _header in HEADERS:
                    td(b(_header))

        for k, v in ports.items():
            link_to_proxy = f"/{v['machine_name']}/{v['remote_port']}"
            is_active = v['tunnel'].is_active
            status = "Active" if is_active else "Stopped"

            stop_link = "/stop" + link_to_proxy
            delete_link = "/delete" + link_to_proxy
            reconnect_link = "/reconnect" + link_to_proxy
            local_link = v['link']

            with _table.add(tbody()):
                _status = td(b(status))
                _status.set_attribute('class', status.lower())

                td(v['machine_name'])
                td(v['remote_port'])
                
                td(a(link_to_proxy, href=link_to_proxy))
                td(a(local_link, href=local_link))

                td(a(b("stop"), href=stop_link))
                td(a(b("reconnect"), href=reconnect_link))
                td(a(b("delete"), href=delete_link))
        
        h2("What is PortProxy?")
        raw(marko.convert(readme))
    
    return str(doc)

@argbind.bind(without_prefix=True)
def make_tunnel(
    machine_name, 
    port,
    ssh_config_file : str = "~/.ssh/config"
):
    """Makes the tunnel.

    Parameters
    ----------
    ssh_config_file : str, optional
        Path to SSH config file, by default "~/.ssh/config"
    """
    key = f"{machine_name}:{port}"
    if key in ports:
        picked_port = ports[key]['local_port']
        tunnel = ports[key]['tunnel']
        if not tunnel.is_active:
            tunnel.stop()
            tunnel = sshtunnel.SSHTunnelForwarder(
                ssh_address_or_host=machine_name,
                remote_bind_address=('localhost', port),
                local_bind_address=('localhost', picked_port),
                ssh_config_file=ssh_config_file
            )
    else:
        picked_port = portpicker.pick_unused_port()
        tunnel = sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host=machine_name,
            remote_bind_address=('localhost', port),
            local_bind_address=('localhost', picked_port),
            ssh_config_file=ssh_config_file
        )
    
    tunnel.start()
    for k, v in tunnel.tunnel_bindings.items():
        debug_str = f"{k} -> {v}"
    app.logger.debug(f"Binding for machine {machine_name}:{port} " + debug_str)
    local_link = f'http://localhost:{picked_port}'
    return {
        'machine_name': machine_name,
        'remote_port': port,
        'tunnel': tunnel, 
        'local_port': picked_port, 
        'link': local_link
    }

@app.route('/<machine_name>/<port>')
def redirect_to_machine(machine_name, port):
    port = int(port)
    key = f"{machine_name}:{port}"    
    ports[key] = make_tunnel(machine_name, port)
    return redirect(ports[key]['link'])

@app.route('/stop')
def stop():
    for key in ports:
        ports[key]['tunnel'].stop()
    return redirect("/")

@app.route('/stop/<machine_name>/<port>')
def stop_one(machine_name, port):
    key = f"{machine_name}:{port}"
    if key in ports:
        ports[key]['tunnel'].stop()
    return redirect("/")

@app.route('/delete/<machine_name>/<port>')
def delete(machine_name, port):
    key = f"{machine_name}:{port}"
    if key in ports:
        ports[key]['tunnel'].stop()
        ports.pop(key)
    return redirect("/")

@app.route('/reconnect')
def reconnect():
    for key in ports:
        ports[key] = make_tunnel(
            ports[key]['machine_name'], 
            ports[key]['remote_port'], 
        )
    return redirect("/")

@app.route('/reconnect/<machine_name>/<port>')
def reconnect_one(machine_name, port):
    port = int(port)
    key = f"{machine_name}:{port}"    
    if key in ports:
        ports[key] = make_tunnel(machine_name, port)
    return redirect('/')

def clean_up(signal, frame):
    app.logger.info("Cleaning up")
    for k, v in ports.items():
        app.logger.debug(f"Stopped {v['tunnel']}")
        v['tunnel'].stop()
    sys.exit(0)

@argbind.bind(without_prefix=True)
def launch(
    host : str = 'localhost',
    port : int = 5000,
):
    """Launch the Flask server for PortProxy.

    Parameters
    ----------
    host : str, optional
        Host for Flask server, by default 'localhost'
    port : int, optional
        Port to run Flask server on, by default 5000
    """
    signal.signal(signal.SIGINT, clean_up)
    app.run(debug=True, host=host, port=port)    

def main():
    args = argbind.parse_args()
    with argbind.scope(args):
        launch()
