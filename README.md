# Maprule
value validating library

## Installation
```bash
python -m pip install -U maprule
```

## Usage
```python
from maprule import fields

fields.Boolean().compare(True)

fields.Integer().compare(0)
fields.Integer(maximum=0).compare(1)

fields.String(min_length=3).compare("he")

fields.Dictionary(dict(
	name=fields.String(min_length=3),
	age=fields.Integer(minimum=0)
)).compare(dict(name="rubbie", age=19))

fields.Array(fields.String(min_length=3)).compare(["rubbie", "kelvin"])
```