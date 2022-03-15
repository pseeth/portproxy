# Changelog
## v0.6.2
- Fixing issue with trailing slash.

## v0.6.1
- Bugfix

## v0.6.0
- Allow all the extra stuff after a link to get forwarded as well. `localhost/machine_name/port/blah -> localhost/redirected_port/blah`.
- Added a utility for copy/pasting a link and having it be automatically portproxified. Usage: `python -m portproxy.forward [machine_name] [link]`.

## v0.5.0
- Adding a button for reconnecting one SSH tunnel after stopping it.
- Refactoring and simplifying code
- Adding arguments to the launcher for better configurability.

## v0.4.0
- If SSH tunnel is stopped, or goes down, an attempt is made to restart it at the same port as before. 
- Improved interface for handling connections.

## v0.3.0
- First official release

## v0.2.0 -> v0.2.1
- Bugs with uploading to PyPi.

## v0.1.0
- Initial release.

