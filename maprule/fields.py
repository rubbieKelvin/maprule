class Field:
	def __init__(self, nullable:bool=False, validate=None):
		self.type = object
		self.nullable = nullable
		self.validate = validate or (lambda x:True)

	def compare(self, other) -> bool:
		if other is None and self.nullable:
			return True
		return type(other) == self.type and self.validate(other)


class Boolean(Field):
	def __init__(self, nullable: bool=False, validate=None):
		super().__init__(nullable=nullable, validate=validate)
		self.type = bool


class Integer(Field):
	def __init__(self, minimum:int=None, maximum:int=None, nullable: bool=False, validate=None):
		super().__init__(nullable=nullable, validate=validate)
		self.type = int
		self.minimum = -100_00_000 if minimum == None else minimum
		self.maximum = 100_00_000 if maximum == None else maximum

	def compare(self, other) -> bool:
		res = super().compare(other)
		if not res: return False
		if res and other is None: return True

		res &= other >= self.minimum
		res &= other <= self.maximum
		return res


class String(Field):
	def __init__(self, min_length:int=None, max_length:int=None, nullable: bool=False, validate=None):
		super().__init__(validate=validate, nullable=nullable)
		self.type = str
		self.min_length = min_length
		self.max_length = max_length

	def compare(self, other) -> bool:
		res = super().compare(other)
		if not res: return False
		if res and other is None: return True

		res &= len(other) >= (self.min_length or 0)
		res &= len(other) <= (self.max_length or 100_000_000)
		return res


class Dictionary(Field):
	def __init__(self, value: dict, nullable: bool=False, validate=None):
		super().__init__(nullable=nullable, validate=validate)
		self.type = dict
		self.dictionary = value

	def addRules(self, **kwargs):
		self.dictionary.update(kwargs)

	def compare(self, other: dict) -> bool:
		res = super().compare(other)
		if not res: return False
		if res and other is None: return True

		# check if all keys in other are in self.dictionary
		if not set(other.keys()).issubset(self.dictionary.keys()):
			return False

		# currently looping through the validation mapping
		for key, value in self.dictionary.items():
			value: Field

			# compare current value to value on the otherside
			res &= value.compare(other.get(key))
			
			# save loop time by breaking when necessary
			if not res: break
		return res

class Array(Field):
	def __init__(self, itemtype: Field, nullable: bool=False, validate=None):
		super().__init__(nullable=nullable, validate=validate)
		self.type = list
		self.itemtype = itemtype

	def compare(self, other: list) -> bool:
		res = super().compare(other)
		if not res: return False
		if res and other is None: return True

		for item in other:
			res &= self.itemtype.compare(item)

			# cut loop time
			if not res: break
		return res


class Any(Field):
	def __init__(self):
		pass

	def compare(self, other):
		return True
