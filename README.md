> [!WARNING]
> This package is currently in Alpha development, so download at your own risk.

<h1 align="left">
  hardpycover
</h1>
<p align="left">
  <b>Simplified API Wrapper for Hardcover, written in Python.</b>
</p>

![PyPI - Version](https://img.shields.io/pypi/v/hardpycover)
![Python Versions](https://img.shields.io/pypi/pyversions/hardpycover?style=flat-square)

<hr />

### Introduction

Hardcover is a Goodreads alternative where the focus is on building a better replacement while providing a publicly-accessible API for all users to explore and use in their various other projects.

In this context, `hardpycover` is born out of an interest to develop a Python API Wrapper in the same vein as TMDB's API. Powered by `sgqlc` and `pydantic`, this wrapper intentionally provides an extra layer of abstraction to ensure that the API use is not just effective, but also efficient and safe-to-use.

### Installation

**pip**
```
pip install hardpycover
```

**uv**
```
uv add hardpycover
```

### Usage

> [!NOTE]
> Using `hardpycover` requires having an API Key from Hardcover. To avail of an API Key, create a Hardcover account and then go to https://hardcover.app/account/api.

```python3
import os
from hardpycover import Hardcover

# Store your API_KEY in an .env file
API_KEY=abcdefg12345

# ...

token = os.environ["API_KEY"]

# create hardcover instance
hc = Hardcover(token=token)
```

**Getting User Information**
```python3
hc.query.user_profile(['id', 'bio', 'created_at', 'username'])
# > {
# 'id': 2,
# 'bio' 'Lorem ipsum dolores amit',
# 'created_at': '2025-06-23T10:10:10.32341Z',
# 'username': 'kennyrogers'
# }
```

For more use cases, read the available methods found at [main.py](/hardpycover/main.py).

### Contributors
<a href="https://github.com/jmcruz14/hardpycover/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=jmcruz14/hardpycover" />
</a>

### License
[MIT License](/LICENSE) – Free to use, modify, and share.