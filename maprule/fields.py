class Field:
	def __init__(self, nullable:bool=False, validate=None, validation_error:str=None, name:str="value"):
		self.name = name
		self.error = None
		self.type = object
		self.nullable = nullable
		self.validation_error = validation_error
		self.validate = validate or (lambda x:True)
		self.parent = None

	def compare(self, other) -> bool:
		if other is None and self.nullable:
			return True

		if other is None and (not self.nullable):
			# null specific validaion
			self.error = f"{self.name} should not be null"
			return False

		res = True
		
		# check 1
		res &= type(other) == self.type
		if not res:
			self.error = f"{self.name} has invalid type"
			return res

		# check 2
		res &= self.validate(other)
		if not res: self.error = self.validation_error
		return res


class Boolean(Field):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.type = bool


class Integer(Field):
	def __init__(self, minimum:int=None, maximum:int=None, **kwargs):
		super().__init__(**kwargs)
		self.type = int
		self.minimum = -100_00_000 if minimum == None else minimum
		self.maximum = 100_00_000 if maximum == None else maximum

	def compare(self, other) -> bool:
		res = super().compare(other)
		if not res: return False
		if res and other is None: return True

		# check 1
		res &= other >= self.minimum
		if not res: self.error = f"{self.name} should be greater than {self.minimum}"

		# check 2
		res &= other <= self.maximum
		if not res: self.error = f"{self.name} should be less than {self.maximum}"

		return res


class String(Field):
	def __init__(self, min_length:int=None, max_length:int=None, **kwargs):
		super().__init__(**kwargs)
		self.type = str
		self.min_length = min_length
		self.max_length = max_length

	def compare(self, other) -> bool:
		res = super().compare(other)
		if not res: return False
		if res and other is None: return True

		# check 1
		res &= len(other) >= (self.min_length or 0)
		if not res: self.error = f"{self.name} should have greater than or {self.min_length} characters"

		# check 2
		res &= len(other) <= (self.max_length or 100_000_000)
		if not res: self.error = f"{self.name} should have less than or {self.max_length} characters"

		return res


class Dictionary(Field):
	def __init__(self, value: dict, **kwargs):
		super().__init__(**kwargs)
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
			# check 1
			# check for extra keys
			extra = set(other.keys()) - set(self.dictionary.keys())
			for i in extra:
				self.error = f"{self.name} has an unnecessary key \"{i}\""
				break

			return False

		# currently looping through the validation mapping
		for key, value in self.dictionary.items():
			value: Field

			# compare current value to value on the otherside
			value.name = key
			value.parent = other
			res &= value.compare(other.get(key))

			# save loop time by breaking when necessary
			if not res:
				self.error = value.error
				break

		return res


class Array(Field):
	def __init__(self, itemtype: Field, **kwargs):
		super().__init__(**kwargs)
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
	"""ignores validation. if types are provided, data is to match any of the types"""
	def __init__(self, types=[]):
		super().__init__()
		self.types = types

	def compare(self, other) -> bool:
		if len(self.types) > 0:
			res = True
			for t_ in self.types:
				res |= type(other) == t_
			return res
		return True
