import sys, os
import termios, fcntl
import select
from sty import fg, bg, rs
from codex import Weapons, Ammos, Brands, Armors, Shields, Tomes, Potions
from Descriptions import Descriptions
from Colors import Colors


class Tome:

	def __init__(self, spells, name, rep, color_tone, hands, loc, brand=None):
		self.rep, self.color, self.hands, self.loc, self.brand, self.wclass = rep, color_tone, hands, loc, brand, "tome"

		# Purchasable Skills
		self.spells = spells

		self.name, self.base_string = Colors.color(name, self.color), name

		# Magic Damage
		self.mdamage = 2

		# Legendary
		if self.base_string in Weapons.legendaries:
			self.legendary = True
			try: game.legendaries_to_spawn.remove(self.base_string)
			except: pass
		else:
			self.legendary = False

	def details(self):

		print(self)
		print("")
		print("Basic Class Tome.")
		print("")
		print("Provides 2 bonus magic damage when wielded.")

		if self.legendary:
			print(Descriptions.legendary[self.base_string])
			print("")

		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def __str__(self):

		if self.brand is not None: return Colors.color(self.brand,Brands.colors[self.brand]) + ' ' + self.name
		else: return self.name

