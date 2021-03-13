from maprule import fields

def test_booleanRule():
	assert fields.Boolean().compare(True)
	assert fields.Boolean().compare(False)
	assert fields.Boolean(nullable=True).compare(None)

def test_integerRule():
	assert fields.Integer().compare(0)
	assert not fields.Integer(maximum=0).compare(1)
	assert not fields.Integer(minimum=0).compare(-1)
	assert fields.Integer(nullable=True).compare(None)

def test_stringRule():
	assert not fields.String(min_length=3).compare("he")
	assert not fields.String().compare(9)
	assert fields.String(nullable=True).compare(None)

def test_dictionaryRule():
	assert fields.Dictionary(dict(
		name=fields.String(min_length=3),
		age=fields.Integer(minimum=0)
	)).compare(dict(name="rubbie", age=19))

	assert not fields.Dictionary(dict(
		name=fields.String(min_length=3),
		age=fields.Integer(minimum=0)
	)).compare(dict(name="ay", age=-1))
	
def test_listRule():
	assert fields.Array(fields.String(min_length=3)).compare(["rubbie", "kelvin"])
	assert not fields.Array(fields.String(min_length=3)).compare(["rubbie", "in"])
	assert not fields.Array(fields.String(min_length=3)).compare(["rubbie", 5])
