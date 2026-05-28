## hardpycover

Simplified API Wrapper for Hardcover, written in Python.

> [!WARNING] 
> This package is currently in Alpha development, so download at your own risk.

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
> Using `hardpycover` requires having an API Key from Hardcover. To avail of an API Key, go to https://hardcover.app/account/api.

```python3
import os
from hardpycover import Hardcover

# Store your API_KEY in an .env file
api_key = os.environ["API_KEY"]

# create hardcover instance
hc = Hardcover(api_key=api_key)
```

**Getting User Information**
```python3
hc.user_profile(['id', 'bio', 'created_at', 'username'])
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