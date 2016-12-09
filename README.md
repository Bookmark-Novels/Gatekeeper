# Gatekeeper

Gatekeeper is Bookmark's SSO authentication service. All session requests are authenticated via an encrypted nounce + origin application instance ID combo.

## To Contributors

Note that we use [EditorConfig](http://editorconfig.org/) for all our style needs.

Please note that `master` is only for stable releases. All development work should be done on `dev`. If you are working on your own thing, please append your GitHub username when you branch so we know what branch belongs to who. For example: `dev-wildandrewlee`. Feature branches should look something like `dev-new-ui`. In most cases, it is prefered to use the feature branch naming style vs the username style.

Merged branches will be deleted every 2-3 days after merging.

## Getting Started

Dependencies: Python 3.4+, everything in `requirements.txt`

```
pyvenv venv
source venv/bin/activate
pip install -r requirements.txt
# Exit via ctrl+D
```
