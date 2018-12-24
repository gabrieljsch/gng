import ai
from ai import *

from bestiary import Monsters
from codex import Weapons, Ammos, Brands, Armors, Shields, Tomes, Potions
from Spells import Spells
from Colors import Colors
from Weapon import Weapon
from Armor import Armor
from Shield import Shield
from Tome import Tome
from Ammo import Ammo
from Potion import Potion
from Trap import Trap
from Maps import Maps

from random import shuffle

def apply(unit, passive, count, stacking=False):

	for present_passive in unit.passives:

		if present_passive[0] == passive:
			if stacking: present_passive[1] += count
			else: present_passive[1] = count
			return

	unit.passives.append([passive, count])


# noinspection PyBroadException
class Monster:

	def __init__(self, game, name, char, color_tone, etype, behavior_type, tier,    con, st, dex, int, cha, mspeed, reg, xp,   resistances,  loc, other_items=None):

		self.game = game
		self.equipped_armor = None

		# Initialize Representation
		self.rep, self.color, self.etype, self.behavior_type, self.tier = char, color_tone, etype, behavior_type, tier

		# Mount?
		self.mount, self.rider = None, None

		self.name, self.namestring = Colors.color(name, self.color), name
		self.info = ('the ' + self.name, 'the ' + self.name + "'s", 'its', 'The ' + self.name, 'The ' + self.name + "'s") if self.namestring not in Monsters.uniques else (self.name, self.name + "'s", 'its', self.name, self.name + "'s")

		# Initialize Health
		bonushp = md(6,self.tier)
		self.maxhp = 5 * con + bonushp
		self.hp = 5 * con + bonushp

		# Initialize Mana
		self.mana, self.maxmana = 5 * int + self.tier, 5 * int + self.tier

		# Regen
		self.hregen, self.mregen, self.innate_ac = 0, 0, 0

		# Coordinates
		self.loc, self.time = loc, 1
		self.passives, self.spells, self.traits = [], [], []

		# Initialize Range
		self.range_from_player = 100

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.reg, self.xp = con, st, dex, int, cha, mspeed, reg, xp

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = resistances

		# Monster's Equipment
		self.wielding , self.other_items, self.quivered, self.inventory = [], other_items, None, []

		# Manage God-Cleaver Passive
		self.god_cleaver_hits = 0


	def calc_resistances(self):
		return [self.frostr + self.equipped_armor.frostr, self.firer + self.equipped_armor.firer, self.poisonr + self.equipped_armor.poisonr, self.acidr + self.equipped_armor.acidr, self.shockr + self.equipped_armor.shockr, self.expr + self.equipped_armor.expr]

	def calc_mdamage(self):
		sd = 0
		for weapon in self.wielding:sd += weapon.mdamage
		return sd

	def calc_AC(self):
		return d(int(max(1, (self.equipped_armor.armor_rating + self.equipped_armor.enchantment) / 2))) + int((self.equipped_armor.armor_rating + self.equipped_armor.enchantment) / 2) + self.innate_ac

	def drop_booty(self):
		self.equipped_armor.loc = self.loc
		self.game.items.append(self.equipped_armor)
		for weapon in self.wielding:
			if weapon in Ammos.thrown_amclasses: continue
			if weapon.hands > 0:
				weapon.loc = self.loc
				self.game.items.append(weapon)
		for item in self.inventory:
			already_in = False
			if type(item) == Ammo:
				for other_item in self.game.items:
					if other_item.loc == self.loc and type(other_item) == Ammo:
						if other_item.name == item.name and other_item.brand == item.brand:
							other_item.number += item.number
							already_in = True
							break
			if not already_in:
				item.loc = self.loc
				self.game.items.append(item)
		if self.quivered is not None:

			for item in self.game.items:
				if item.loc == self.loc and type(item) == Ammo:
					if item.base_string == self.quivered.base_string and item.brand == self.quivered.brand:
						item.number += self.quivered.number
						return
			self.quivered.loc = self.loc
			self.game.items.append(self.quivered)


	def give_weapon(self, weapon):
		data = Weapons.array[weapon]

		# Manage Enchantment
		spawned_enchantment = data[4]
		if d(10) + (1.5 * self.tier) > 13: spawned_enchantment += d(int(max(1, self.tier / 2))) - 1

		# Manage Brand + Probability
		try: brand = data[8]
		except:
			if d(100) > 99 - self.tier and data[3] > 0 and weapon not in Weapons.legendaries: brand = Brands.weapon_brands[d(len(Brands.weapon_brands)) - 1]
			else: brand = None
		try: prob = data[9]
		except: prob = None

		# Create Weapon Object
		self.wielding.append(Weapon(self.game, weapon, data[0], data[1], data[2], data[3], spawned_enchantment, data[5], data[6], data[7], None, brand, prob))

	def give_armor(self, armor):
		data = Armors.array[armor]

		# Manage Enchantment
		spawned_enchantment = data[5]
		if d(10) + (1.5 * self.tier) > 13: spawned_enchantment += d(int(max(1, self.tier / 2))) - 1
		try: brand = data[6]
		except:
			if d(100) > 99 - self.tier and armor not in Weapons.legendaries: brand = Brands.armor_brands[d(len(Brands.armor_brands)) - 1]
			else: brand = None

		# Create Armor Object
		self.equipped_armor = Armor(armor, data[0], data[1], data[2], data[3], data[4], spawned_enchantment, None, brand)

	def give_shield(self, shield):
		data = Shields.array[shield]

		# Manage Enchantment + brand
		spawned_enchantment = data[5]
		if d(10) + (1.5 * self.tier) > 10 and shield not in Weapons.legendaries: spawned_enchantment += d(int(max(1, self.tier / 2))) - 1
		try: brand = data[6]
		except: brand = None

		# Create Shield Object
		self.wielding.append(Shield(self.game,shield, data[0], data[1], data[2], data[3], data[4],spawned_enchantment, None, brand))

	def give_tome(self, tome):
		data = Tomes.array[tome]
		try: brand = data[3]
		except: brand = None

		# Create Weapon Object
		self.wielding.append(Tome(data[0], tome, '_', data[2], data[1], None, brand))
		return self.wielding[-1]

	def give_ammo(self, ammo):
		data = Ammos.array[ammo]

		# Manage Enchantment + Brand
		try: brand = data[4]
		except: brand = None
		if brand is None:
			if d(100) > 99 - self.tier and data[3] > 0: brand = Brands.ammo_brands[d(len(Brands.ammo_brands)) - 1]

		# Manage Number
		if data[2] in Ammos.thrown_amclasses: number = 4 + 2 * self.tier
		else: number = 10 + 5 * self.tier

		# Create Ammo Object
		self.quivered = Ammo(ammo, data[0], data[1], data[2], number, data[3], None, brand)

	def give_potion(self, pot):
		data = Potions.array[pot]

		# Manage Number
		number = max(1, self.tier / 2)

		# Create Potion Object
		self.inventory.append(Potion(pot, data, None, number))


	def currentPassives(self):
		current = {name for name,count in self.passives}
		for name, count in self.passives:
			current.add(name)
		return current


	def removePassive(self, specified):
		for passive in self.passives:
			if passive[0] == specified:
				self.passives.remove(passive)
				return True
		return False


	def turn(self, game):

		# Manage Terrified
		for passive in self.passives:
			if passive[0] == "terrified":

				# Fear Radius
				spaces = []
				for x in range(-1,2):
					for y in range(-1,2):
						if self.loc[0] + x >= 0 and self.loc[1] + y >= 0: spaces.append((self.loc[0] + x, self.loc[1] + y))
				shuffle(spaces)

				# Move to random square
				for space in spaces:
					if game.map.can_move(space):
						self.loc = space
						break

				# Check for Traps
				for item in game.items:
					if type(item) == Trap and item.loc == self.loc:
						item.trip(game)

				self.time += self.mspeed
				return


		# Ally Unit
		los = None
		if self in game.allies:
			enemy, mini = None, 100
			for unit in game.units:
				if unit in game.allies: continue
				los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:
					if unit.name == "you": self.range_from_player = len(los)
					elif len(los) < mini: enemy, mini, minlos = unit, len(los), los

			# No enemies in room
			if enemy is None:
				move_towards(self, game.player, game.map)
				self.time += self.mspeed
				return

		# Enemy Unit
		else:
			minlos = ai.los(self.loc, game.player.loc, Maps.rooms[game.map.map][0], game )
			try: mini, enemy = len(minlos), game.player
			except: mini, enemy = 100, game.player
			for unit in game.allies:
				los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:
					if unit.name == "you": self.range_from_player = len(los)
					if len(los) <= mini: enemy, mini, minlos = unit, len(los), los


		melee_attacked = False

		# MAGIC!!
		if len(self.spells) > 0:

			# Chance to use spells
			if d(10) + min(self.int, 7) >= 12:

				if minlos is not None:

					# Zap with spells
					for spell in self.spells:

						# Check for mana
						if self.mana >= Spells.spells[spell][1]:
							spell_fun = Spells.spells[spell][0]

							# If target
							if Spells.spells[spell][4]:

								# If in spell range
								if len(minlos) - 1 <= Spells.spells[spell][5]:

									# Player Resist spell
									if d(100) / 100 <= max(0.05, min(0.9, (enemy.cha / 2) / self.int)):
										self.time += Spells.spells[spell][2]
										self.mana -= Spells.spells[spell][1]
										if enemy.name == 'you': game.game_log.append("You resist the " + spell + " from " + self.info[0] + "!")
										else: game.game_log.append(enemy.info[3] + " resists the " + spell + " from " + self.info[0] + "!")

									elif spell_fun(spell, self, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler):
										self.time += Spells.spells[spell][2]
										self.mana -= Spells.spells[spell][1]

										if self.mount is not None: self.mount.unit.loc = self.loc
										if self.rider is not None: self.rider.loc = self.loc
							# No target
							else:
								if spell_fun(spell, self, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler):
									self.time += Spells.spells[spell][2]
									self.mana -= Spells.spells[spell][1]

									if self.mount is not None: self.mount.unit.loc = self.loc
									if self.rider is not None: self.rider.loc = self.loc

							# Manage the Black Cross 2
							for unit in self.game.units:
								for item in unit.wielding:
									if item.base_string == "the Black Cross":
										for school, spells in Spells.spell_schools.items():
											if spell in spells:
												if school in Spells.school_info:
													if Spells.school_info[school][1] is not None:
														self.game.game_log.append("Yet " + item.name + " condemns " + self.info[1] + " use of magic, it " + Colors.color("ignites", "fire") + " " + self.info[2] + " flesh!")
														apply(self, "aflame", 3)

							# Manage Longfang 2
							for weapon in self.wielding:
								if weapon.base_string == "Longfang":
									for school, spells in Spells.spell_schools.items():
										if spell in spells:
											if school in Spells.school_info:
												if Spells.school_info[school][1] is not None:
													weapon.passives = [[Spells.school_info[school][1] , 1]]
													weapon.brand = Spells.school_info[school][1]
													game.game_log.append(weapon.name + " absorbs the power of " + self.info[1] + " spell and becomes " + Colors.color(weapon.brand, Brands.colors[weapon.brand]) + "!")
													break

							# One spell per turn
							return



		# Melee Attack
		if adjacent_to(self, enemy):

			# Find weapons
			weaps = [item for item in self.wielding[::-1] if type(item) == Weapon and item.wclass not in Weapons.ranged_wclasses]


			maxas = 0
			for weapon in weaps:
				 if weapon.speed > maxas and weapon.wclass not in Weapons.ranged_wclasses: maxas = weapon.speed

			# Hit with melee
			for item in weaps:
				item.strike(self, enemy, game)
				if self in game.allies:
					# Enemy Well-being Statement
					try: game.player.well_being_statement(enemy, self, item)
					except: pass

			self.time += maxas
			melee_attacked = True

		# Add thrown weapon platform
		thrown = False
		if self.quivered is not None:
			if self.quivered.wclass in Ammos.thrown_amclasses:
				thrown = True
				self.give_weapon(self.quivered.base_string)

		# Make Ranged attacks
		for item in self.wielding:
			if item.wclass in Weapons.ranged_wclasses or item.wclass in Ammos.thrown_amclasses:

				if self.quivered is not None or item.hands == 0:

					if item.hands > 0 and melee_attacked:
						if thrown: self.wielding.pop()
						return

					# los = los(self.loc, enemy.loc, Maps.rooms[game.map.map][0], game )
					if minlos is not None:

						# Ranged range
						if mini <= (2 * item.damage + item.to_hit):
							item.strike(self, enemy, game)
							if self in game.allies:
								# Enemy Well-being Statement
								try: game.player.well_being_statement(enemy, self, item)
								except: pass


							# Remove Ammo
							if thrown: self.wielding.pop()
							if item.hands > 0:
								self.quivered.number -= 1
								if self.quivered.number == 0: self.quivered = None
								self.time += item.speed
								return
						else:
							if thrown: self.wielding.pop()
					else:
						if thrown: self.wielding.pop()

		# If can't, move
		immobile = False
		for name, count in self.passives:
			if name == 'immobile': immobile = True

		if not melee_attacked and self.behavior_type != 'as':

			if not immobile:
				coordinates = self.loc
				if self.mount is None: smart_move_towards(self, enemy, game)

				# Check for Traps
				for item in game.items:
					if type(item) == Trap and item.loc == self.loc:
						item.trip()

				# Manage Furious Charge (enemies)
				if "furious charge" in self.traits:
					if self in game.allies:
						for unit in game.units:
							if unit in game.allies: continue
							if unit.loc == (coordinates[0] - 2 * (self.loc[0] - unit.loc[0]), self.loc[1] - 2 * (self.loc[1] - unit.loc[1])):
								for weapon in self.wielding: weapon.strike(self, unit, game, False)
								break
					else:
						for unit in game.allies:
							if unit.loc == (coordinates[0] - 2 * (self.loc[0] - unit.loc[0]), coordinates[1] - 2 * (self.loc[1] - unit.loc[1])):
								for weapon in self.wielding: weapon.strike(self, unit, game,  False)
								break

				# Manage Lance (enemies)
				if self.rider is not None:
					for weapon in self.rider.wielding:
						if weapon.wclass == 'lance':
							for unit in game.units:
								if unit.loc == (coordinates[0] - 2 * (self.loc[0] - unit.loc[0]), coordinates[1] - 2 * (self.loc[1] - unit.loc[1])):
									weapon.strike(self.rider, unit, game, False)
									break

			self.time += self.mspeed

			if self.rider is not None:
				self.rider.prev_loc = self.rider.loc
				self.rider.loc = self.loc

