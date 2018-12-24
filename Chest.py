from codex import Weapons, Ammos, Brands, Armors, Potions, Shields
from Colors import Colors
from ai import *

from sty import fg, bg, rs

def color(statement, color):
	color = Colors.array[color]
	return fg(color[0], color[1], color[2]) + str(statement) + fg.rs

def bcolor(statement, bcolor):
	bcolor = Colors.array[bcolor]
	return bg(bcolor[0], bcolor[1], bcolor[2]) + str(statement) + bg.rs

def fullcolor(statement, fcolor, bcolor):
	color, bcolor = Colors.array[fcolor], Colors.array[bcolor]
	return fg(color[0], color[1], color[2]) + bg(bcolor[0], bcolor[1], bcolor[2]) + str(statement) + rs.all


class Chest:

	def __init__(self, chest_type, tier,  loc, game):
		self.tier, self.chest_type, self.loc = tier, chest_type, loc
		self.base_string = "chest"
		self.game = game

		# Initialize Rep
		self.rep = '='
		self.opened = False

		# Chest contents
		if self.chest_type == "golden":
			self.pot_weapons = [ ["steel longsword","hooked longsword","skull smasha","bearded axe"],
								 ["gorktooth choppa","ranger longbow","godclaw","gladius"],
								 ["claymore","khopesh","gorkjaw choppa","executioner axe","dwarven waraxe"],
								 ["witchhunter blade","glaive","dwarven crossbow","dwarven broadaxe"],
								 ["godfist","demonfist","demonclaw","glass dagger","bearded greataxe"] 	]
			self.color = "gold"

		elif self.chest_type == "elven":
			self.pot_weapons = [ ["elven wooddagger","elven leafblade"],
								 ["elfrobe"],
								 ["elven leafblade","winged javelin"],
								 ["elven broadspear","elven longbow"],
								 ["elven longstaff"], 	]
			self.color = "gold"
		elif self.chest_type == "dark elven":
			self.pot_weapons = [ ["thornblade","thornknife"],
								 ["thornarrow"],
								 ["blackwood longbow","ironscale mail"],
								 ["sunspear","sunlance"], 	]
			self.color = "purple"
		elif self.chest_type == "wooden":
			self.pot_weapons = [["steel dagger","iron axe","spear","hammer","mace","iron longsword","club","iron shortsword"],
								["crude shortbow","iron battleaxe","iron longsword","mace","flail","quarterstaff","iron bastard sword"],
								["buckler shield", "wooden broadshield","trollhide shield","recurve bow"],
								["iron battleaxe","iron greatsword","warhammer","spiked club","barbed javelin","longbow","falchion","scimitar"],
								["iron plate","iron chainmail","ironscale mail","scrap plate armor"],
								["steel axe","steel longsword","halberd","steel bastard sword","steel shortsword","bearded axe"],
								["steel greatsword","steel battleaxe","pike","greatflail","ranger longbow","steel shortsword"],
								["godfist","godclaw","claymore","gladius"] ]
			self.color = "brown"
		elif self.chest_type == "orcish":
			self.pot_weapons = [ ["goblin spear","stabba","choppa"],
								 ["bear hide","ogre hide","berserker mail","scrap plate armor"],
								 ["choppa","slica","smasha","goblin bow","crude shortbow"],
								 ["big choppa","big slica","skull smasha"],
								 ["toxic slica","krogtooth choppa"],
								 ["ice choppa","boss choppa"],
								 [],
								 ["krogjaw choppa","dethklaw"], 	]
			self.color = "darkgreen"

		self.pot_ammo = ["iron arrow","iron bolt","iron javelin","steel arrow","steel bolt","thornarrow"]

	def open(self):

		# Legendary Chance
		if d(100) + self.tier > 100:
			try:
				legendary = self.game.legendaries_to_spawn[ d(len(self.game.legendaries_to_spawn)) - 1]
				self.game.map.room_filler.place_weapon(legendary, self.loc, int((d(self.tier) - 1) / 2))
			except: pass

		else:

			# Place Weapons/Armor/Shield
			for i in range(1, int(self.game.player.level / 2) + 2):
				if len(self.pot_weapons) == 0: return

				# Calculate Tier
				tier = self.pot_weapons[min( i - 1, len(self.pot_weapons) - 1 )] # player level / Specifies not to overshoot
				item_string = tier [d(len(tier)) - 1]

				# Chance to get item
				if d(100) / 100 <= i / int(self.game.player.level) / 2 + 1:

					# If Ammo
					if item_string in Ammos.array:

						# Chance for brand
						brand = None
						brand = Brands.ammo_brands[d(len(Brands.ammo_brands)) - 1] if d(100) + self.tier > 97 else None
						self.game.map.room_filler.place_ammo(item_string, self.loc, 5 + 4 * self.tier, brand)

					# If weapon
					elif item_string in Weapons.array:

						# Chance for brand
						brand = None
						if Weapons.array[item_string][3] > 0 and item_string not in Weapons.legendaries:
							if d(100) + self.tier > 97: brand = Brands.weapon_brands[d(len(Brands.weapon_brands)) - 1]
						self.game.map.room_filler.place_weapon(item_string, self.loc, int((d(self.tier) - 1) / 2), brand)

					# If Armor
					elif item_string in Armors.array:

						# Chance for brand
						brand = Brands.armor_brands[d(len(Brands.armor_brands)) - 1] if d(100) + self.tier > 97 and item_string not in Weapons.legendaries else None
						self.game.map.room_filler.place_armor(item_string, self.loc, int((d(self.tier) - 1) / 2), brand)

					# If Shield
					elif item_string in Shields.array:
						self.game.map.room_filler.place_shield(item_string, self.loc, int((d(self.tier) - 1) / 2))

					# If Potion
					elif item_string in Potions.array: self.game.map.room_filler.place_potion(item_string, self.loc, self.tier)

					# self.pot_weapons.remove(tier)

		# Place Ammo
		if d(10) + d(self.tier) > 6:

			# Chance for brand
			brand = None
			if d(100) + 2 * self.tier > 96: brand = Brands.ammo_brands[d(len(Brands.ammo_brands)) - 1]

			ammo = self.pot_ammo[min(len(self.pot_ammo) - 1, d(self.tier) - 1)]
			if ammo in Weapons.array: number = 2 * self.tier
			else: number = 5 + self.tier
			self.game.map.room_filler.place_ammo(ammo, self.loc, number, brand)
		self.opened = True

