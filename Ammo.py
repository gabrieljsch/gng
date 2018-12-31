from codex import Ammos, Brands
from Descriptions import Descriptions
from Colors import Colors
from Weapon import Weapon


class Ammo:

	def __init__(self, game, name, rep, color_tone, wclass, number, damage, loc, brand=None):
		self.rep, self.color, self.wclass, self.damage, self.number, self.loc, self.brand = rep, color_tone, wclass, damage, number, loc, brand
		self.name, self.base_string = Colors.color(name, self.color), name
		self.game = game

	@staticmethod
	def give_ammo(unit, ammo, number=(20,6), brand=None):
		data = Ammos.array[ammo]
		number = number[1] if data[2] in Ammos.thrown_amclasses else number[0]
		unit.inventory.append(Ammo(unit.game, ammo, data[0], data[1], data[2], number, data[3], None, brand))
		return unit.inventory[-1]


	def details(self):
		print(self,' (' + self.wclass + ')')
		print("")
		if self.wclass in Ammos.thrown_amclasses:
			weapon = Weapon.make_weapon(self.base_string, self.game)
			print("Base damage:",self.damage + weapon.damage)
			print("Range:",weapon.range)
		else:
			print("Base damage:", self.damage)
		print("You are carrying " + str(self.number) + ".")
		print("")
		print(Descriptions.wclass[self.wclass])
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def one_ammo(self):
		return Ammo(self.game, self.base_string, self.rep, self.color, self.wclass, self.damage, 1, self.loc, self.brand)

	def same_value(self, other):
		if type(other) != Ammo: return False
		return self.base_string == other.base_string and self.brand == other.brand

	def __str__(self):
		if self.brand is not None:
			return Colors.color(self.brand, Brands.colors[self.brand]) + ' ' + self.name + ' (' + str(self.number) + ')'
		else: return self.name + ' (' + str(self.number) + ')'
