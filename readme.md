## Installation
```bash
pip install git+
```

## Quickstart
```python

# the only function this module provides
from mat2py import load
data = load("data.mat")

# obtain the keys 
list_of_keys = data.keys()

# obtain value / go one level down in matlab structure
key="monday"

data.monday # these are ..
data[key] # both identical

values = data.values()

# pprint entire tree-like structure
data.pprint()
```