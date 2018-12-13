import sys, os
import termios, fcntl
import select
from codex import Weapons, Ammos, Brands, Armors, Shields, Tomes, Potions
from Descriptions import Descriptions
from Colors import Colors


class Ammo:

	def __init__(self, name, rep, color_tone, wclass, number, damage, loc, brand=None):
		self.rep, self.color, self.wclass, self.damage, self.number, self.loc, self.brand = rep, color_tone, wclass, damage, number, loc, brand

		self.name, self.base_string = Colors.color(name, self.color), name

	def details(self):
		brand = '' if self.brand is None else self.brand + ' '

		print(self,' (' + self.wclass + ')')
		print("")
		if self.wclass in Ammos.thrown_amclasses:
			data = Weapons.array[self.base_string]
			weapon = Weapon(self.name, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], None, None, None)
			print("Base damage:",self.damage + weapon.damage)
			print("Range:",weapon.range)
		else:
			print("Base damage:",self.damage)
		print("You are carrying " + str(self.number) + ".")
		print("")
		print(Descriptions.wclass[self.wclass])
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def __str__(self):

		if self.brand is not None:
			return Colors.color(self.brand, Brands.colors[self.brand]) + ' ' + self.name + ' (' + str(self.number) + ')'
		else: return self.name + ' (' + str(self.number) + ')'