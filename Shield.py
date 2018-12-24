from codex import Weapons, Brands
from Descriptions import Descriptions
from Colors import Colors

class Shield:

	def __init__(self, game, name, rep, color_tone, hands, armor_rating, encumbrance, enchantment, loc, brand=None):
		self.rep, self.color, self.hands, self.armor_rating, self.encumbrance, self.enchantment, self.loc, self.brand = rep, color_tone, hands, armor_rating, encumbrance, enchantment, loc, brand
		self.wclass = "shield"

		self.name, self.base_string = Colors.color(name, self.color), name

		# Legendary
		if self.base_string in Weapons.legendaries:
			self.legendary = True
			try: game.legendaries_to_spawn.remove(self.base_string)
			except: pass
		else:
			self.legendary = False

		# Magic Damage
		self.mdamage = 0

	def details(self):

		if self.encumbrance >= 0: encum = '-' + str(self.encumbrance)
		else: encum = '+' + str(abs(self.encumbrance))

		print(self)
		print("")
		print("This shield is " + str(self.hands) + "-handed.")
		print("Base armor rating:", str(self.armor_rating) + ',', "Base encumbrance:", encum)

		if self.legendary:
			print("")
			print(Descriptions.legendary[self.base_string])

		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def __str__(self):

		enchant_string = "+" + str(self.enchantment) if self.enchantment >= 0 else str(self.enchantment)

		if self.brand is not None:
			if self.base_string[:4].lower() == 'the ': return Colors.color(self.base_string[:4], self.color) + Colors.color(self.brand, Brands.colors[self.brand]) + " " + enchant_string + ' ' + Colors.color(self.base_string[4:], self.color)
			else: return Colors.color(self.brand, Brands.colors[self.brand]) + " " + enchant_string + ' ' + self.name
		else:
			if self.base_string[:4].lower() == 'the ': return Colors.color(self.base_string[:4], self.color) + enchant_string + ' ' + Colors.color(self.base_string[4:], self.color)
			else: return enchant_string + ' ' + self.name