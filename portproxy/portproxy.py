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

app = Flask(__name__)
ports = {}
app_file_path = Path(__file__).parent

def _read_file(path):
    with open(str(path), 'r') as f:
        data = f.read()
    return data

HEADERS = [
    "Machine name", 
    "Port", 
    "Link via PortProxy", 
    "Link via localhost",
    "Stop forwarded port",
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

        _table = table()
        with _table.add(tbody()):
            with tr():
                for _header in HEADERS:
                    td(b(_header))

        for k, v in ports.items():
            machine_name, port_number = k.split(':')
            link_to_proxy = f"/{machine_name}/{port_number}"
            stop_link = "/stop" + link_to_proxy
            local_link = v['link']

            with _table.add(tbody()):
                td(k.split(':')[0])
                td(k.split(':')[1])
                
                td(a(link_to_proxy, href=link_to_proxy))
                td(a(local_link, href=local_link))
                td(a(b("stop"), href=stop_link))
        
        h2("What is PortProxy?")
        raw(marko.convert(readme))
    
    return str(doc)

@app.route('/<machine_name>/<port>')
def redirect_to_machine(machine_name, port):
    port = int(port)
    key = f"{machine_name}:{port}"
    if key in ports:
        return redirect(ports[key]['link'])
    
    picked_port = portpicker.pick_unused_port()
    ports[key] = {
        'link': f'http://localhost:{picked_port}',
        'tunnel': sshtunnel.SSHTunnelForwarder(
            ssh_address_or_host=machine_name,
            remote_bind_address=('localhost', port),
            local_bind_address=('localhost', picked_port)
        )
    }
    ports[key]['tunnel'].start()

    return redirect(ports[key]['link'])

@app.route('/stop/<machine_name>/<port>')
def stop(machine_name, port):
    key = f"{machine_name}:{port}"
    if key in ports:
        ports[key]['tunnel'].stop()
        ports.pop(key)
    return redirect("/")

def clean_up(signal, frame):
    app.logger.error("Cleaning up")
    for k, v in ports.items():
        v['tunnel'].stop()
    sys.exit(0)

def launch():
    signal.signal(signal.SIGINT, clean_up)
    app.run(debug=True)    
