# Gatekeeper

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b9279b59eae14efb86aa119fa3e96622)](https://www.codacy.com/app/WildAndrewLee/Gatekeeper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Bookmark-Novels/Gatekeeper&amp;utm_campaign=Badge_Grade)

Gatekeeper is Bookmark's SSO authentication service. All session requests are authenticated via an encrypted nounce + origin application instance ID combo.

## Pipelines

| Branch | Status |
|--------|--------|
| master | [![Build Status](https://travis-ci.org/Bookmark-Novels/Gatekeeper.svg?branch=master)](https://travis-ci.org/Bookmark-Novels/Gatekeeper) |
| dev    | [![Build Status](https://travis-ci.org/Bookmark-Novels/Gatekeeper.svg?branch=dev)](https://travis-ci.org/Bookmark-Novels/Gatekeeper) |

## To Contributors

Note that we use [EditorConfig](http://editorconfig.org/) for all our style needs.

We are also using [Standard Style](https://github.com/standard/standard) exclusively for JS.

Please note that `master` is only for stable releases. All development work should be done on `dev`. If you are working on your own thing, please append your GitHub username when you branch so we know what branch belongs to who. For example: `dev-wildandrewlee`. Feature branches should look something like `dev-new-ui`. In most cases, it is prefered to use the feature branch naming style vs the username style.

Merged branches will be deleted every 2-3 days after merging.

## Getting Started

See [this page](https://wiki.dev.bookmark.services/development/gatekeeper/dev-setup-old).
