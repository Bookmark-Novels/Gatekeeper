# Gatekeeper

Gatekeeper is Bookmark's SSO authentication service. All session requests are authenticated via an encrypted nounce + origin application instance ID combo.

## To Contributors

Note that we use [EditorConfig](http://editorconfig.org/) for all our style needs.

## Getting Started

Dependencies: Python 3.4+, everything in `requirements.txt`

```
pyvenv venv
source venv/bin/activate
pip install -r requirements.txt
# Exit via ctrl+D
```