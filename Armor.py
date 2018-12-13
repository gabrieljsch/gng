import termios, fcntl
import select
from sty import fg, bg, rs
from Descriptions import Descriptions
from Colors import Colors
from codex import Weapons, Ammos, Brands, Armors, Shields, Tomes, Potions

class Armor:

	def __init__(self, name, rep, color_tone,   aclass, armor_rating, encumbrance, enchantment, loc, brand=None):
		self.rep, self.color, self.aclass, self.armor_rating, self.encumbrance, self.enchantment, self.loc, self.brand = rep, color_tone, aclass, armor_rating, encumbrance, enchantment, loc, brand

		self.name, self.base_string = Colors.color(name, self.color), name

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = 0, 0, 0, 0, 0, 0

		# Legendary
		if self.base_string in Weapons.legendaries:
			self.legendary = True
			try:
				game.legendaries_to_spawn.remove(self.base_string)
			except: pass
		else:
			self.legendary = False

		# Armor Types mdefense
		if aclass == 'garments': self.mdefense = 0
		elif aclass == 'robes': self.mdefense = 3
		elif aclass == 'hide': self.mdefense = 2
		elif aclass == 'scale': self.mdefense = 1
		elif aclass == 'chainmail': self.mdefense = 1
		elif aclass == 'plate': self.mdefense = 1


		# Manage Icy, Tempered, Insulated, Voidforged
		if self.brand == 'tempered': self.firer += 2
		if self.brand == 'icy': self.frostr += 2
		if self.brand == 'insulated': self.shockr += 2
		if self.brand == 'voidforged': self.mdefense += 2


	def details(self):

		if self.encumbrance > 0: encum = '-' + str(self.encumbrance)
		else: encum = '+' + str(abs(self.encumbrance))

		print(self,' (' + self.aclass + ')')
		print("")
		print("Base armor rating:", str(self.armor_rating) + ',', "Base encumbrance:", encum)
		print("")

		if self.legendary:
			print(Descriptions.legendary[self.base_string])
			print("")

		print(Descriptions.wclass[self.aclass])
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def __str__(self):

		enchantment_string = "+" + str(self.enchantment) if self.enchantment >= 0 else str(self.enchantment)

		if self.brand is not None:
			if self.base_string[:4].lower() == 'the ': return Colors.color(self.base_string[:4], self.color) + Colors.color(self.brand, Brands.colors[self.brand]) + " " + enchantment_string + ' ' + Colors.color(self.base_string[4:], self.color)
			else: return Colors.color(self.brand, Brands.colors[self.brand]) + " " + enchantment_string + ' ' + self.name
		else:
			if self.base_string[:4].lower() == 'the ': return Colors.color(self.base_string[:4], self.color) + enchantment_string + ' ' + Colors.color(self.base_string[4:], self.color)
			else: return enchantment_string + ' ' + self.name


