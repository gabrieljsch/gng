from maps import Maps
import ai

from bestiary import Monsters
from bestiary import Bands


from codex import Weapons
from codex import Brands
from codex import Armors
from codex import Shields
from codex import CharacterRaces

from random import randint
from copy import deepcopy

import sys, os
import termios, fcntl
import select





class Player():

	def __init__(self, statsheet, innate_equipment, game):


		# Initialize Location, Time
		self.loc, self.time = (2,5), 0

		# Initialize Representation
		self.rep, self.name, self.passives  = '@', "you", []

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.reg = statsheet

		self.hp = 5 + self.con * 5 + self.str
		self.maxhp = 5 + self.con * 5 + self.str

		self.mana = 3 * self.int
		self.maxmana = 3 * self.int


		# Initialze Equipment
		self.wielding, self.hands = [], 2

		for equipment in innate_equipment:
			if equipment in Weapons.array:
				self.give_weapon(equipment)

		# Initialize Armor
		self.equipped_armor = Armor('bear hide','}',3,1, 0, None)

		# Inventory
		self.inventory = []

		# Initialize Level, XP
		self.level = 1
		self.xp = 0
		self.xp_levels = 10

		# Racial Bonuses
		self.innate_ac = 0

		# Apply Racial Passives
		self.racial_passives(game)


	def racial_passives(self, game):

		# Innate passives
		if game.race == 'Elf':
			self.innate_ac += 3

	def fire(self):

		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		for item in self.wielding:


			if type(item) == Weapon:
				if item.wclass in Weapons.ranged_wclasses:

					units_in_range = []
					for unit in game.units[1:]:
						los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
						if los is not None and (len(los) <= (2 * item.damage  + item.to_hit)):
							units_in_range.append(unit)

							# Ranged range
					if len(units_in_range) != 0:
						print("=======================================================================================")
						print("                                                                     ")
						for i in range(len(units_in_range)):

							unit = units_in_range[i]

							print(str(item_order[i]) + " - " + unit.name)

						print("                                                                     ")
						print("=======================================================================================")

						# valid = False

						# while not valid:


						fd = sys.stdin.fileno()
						newattr = termios.tcgetattr(fd)
						newattr[3] = newattr[3] & ~termios.ICANON
						newattr[3] = newattr[3] & ~termios.ECHO
						termios.tcsetattr(fd, termios.TCSANOW, newattr)

						oldterm = termios.tcgetattr(fd)
						oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
						fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

						print("")
						print("Aim at which target?")
						inp, outp, err = select.select([sys.stdin], [], [])
						decision = sys.stdin.read()

							# decision = input("Aim at which target? (enter '9' to cancel)")

						if decision == '9':
							valid = True

						elif len(decision) == 1:
							if decision in item_order:
								if item_order.index(decision) < len(units_in_range):

									# Choose Legal Enemy
									unit = units_in_range[item_order.index(decision)]
									self.time += item.speed
									self.attack(unit, item)
									valid = True

									# Enemy Well-being Statement

									# Enemy over 90%
									if unit.hp / unit.maxhp > 0.9:
										game.game_log.append("The "  + str(unit.name) + " seems uninjured.")

									# Enemy over 70%	
									elif unit.hp / unit.maxhp > 0.7:
										game.game_log.append("The "  + str(unit.name) + " seems only lightly wounded.")

									# Enemy over 30%
									elif unit.hp / unit.maxhp > 0.3:
										game.game_log.append("The "  + str(unit.name) + " seems moderately wounded.")

									# Enemy under 30%
									elif unit.hp > 0:
										game.game_log.append("The "  + str(unit.name) + " seems nearly dead!")

									return
								else:
									print("That is not a valid input")
						else:
							print("That is not a valid input")


						# Reset the terminal:
						termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
						fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

					else:
						game.temp_log.append("There are no targets in range!")
						return

		game.temp_log.append("You are not wielding a ranged weapon!")





	def check_level_up(self):

		# See if enough xp for a level up
		if self.xp >= self.xp_levels:

			self.level += 1

			bonushp = d(self.cha)
			self.hp += 2 + bonushp
			self.maxhp += 2 + bonushp
			self.mana += 2
			self.maxmana += 2

			game.game_log.append("You've leveled up!")
			print("You've leveled up!")
			self.xp -= self.xp_levels
			self.xp_levels = 2 * self.xp_levels

			fd = sys.stdin.fileno()
			newattr = termios.tcgetattr(fd)
			newattr[3] = newattr[3] & ~termios.ICANON
			newattr[3] = newattr[3] & ~termios.ECHO
			termios.tcsetattr(fd, termios.TCSANOW, newattr)

			oldterm = termios.tcgetattr(fd)
			oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
			valid = False

			while not valid:
				print("")
				print("Increase your (C)onsititution, (S)trength, (D)exterity, (I)ntelligence, or (CH)arisma?")
				inp, outp, err = select.select([sys.stdin], [], [])
				stat = sys.stdin.read()

			# valid = False
			# while not valid:
				# stat = input("Increase your (C)onsititution, (S)trength, (D)exterity, (I)ntelligence, or (CH)arisma?")
				if stat.lower() == "c"or stat.lower() == "s"or stat.lower() == "d"or stat.lower() == "i"or stat.lower() == "ch":
					if stat.lower() == "c":
						stat = "Constitution"
						self.con += 1
						self.hp += 5
						self.maxhp += 5
					elif stat.lower() == "s":
						stat = "Strength"
						self.str += 1
						self.hp +=  1
						self.maxhp += 1
					elif stat.lower() == "d":
						stat = "Dexterity"
						self.dex += 1
					elif stat.lower() == "i":
						stat = "Intelligence"
						self.int += 1
						self.mana += 3
						self.maxmana += 3
					elif stat.lower() == "ch":
						stat = "Charisma"
						self.cha += 1
					print("You increase your " + stat + "!")

					valid = True

				else:
					print("Pick a stat!")
			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

	def equip(self, item):

		# Equip Weapon
		if type(item) == Weapon or type(item) == Shield:
			if self.hands < item.hands:
				while self.hands < item.hands:
					other_weap = self.wielding[-1]
					if other_weap.hands != 0:
						self.wielding.remove(other_weap)
						self.inventory.append(other_weap)
						self.hands += other_weap.hands
			self.wielding.append(item)
			self.inventory.remove(item)
			self.hands -= item.hands
			game.game_log.append("You draw your " + item.name + "!")

		# Equip Armor
		elif type(item) == Armor:
			self.inventory.append(self.equipped_armor)
			self.equipped_armor = item
			self.inventory.remove(item)
			game.game_log.append("You put on your " + item.name + "!")

		# Take a turn
		self.time += 1.0

	def unequip(self, weapon):
		if type(item) == Weapon:
			self.wielding.remove(weapon)
			self.inventory.append(weapon)
			self.hands += item.hands
			game.game_log.append("You unequip " + item.name + ".")
			self.time += 1.0

	def pick_up(self, item):
		item.loc = None
		game.items.remove(item)
		self.inventory.append(item)
		game.game_log.append("You pick up the " + item.name + ".")
		self.time += 1.0

	def drop(self,item):
		item.loc = self.loc
		del self.inventory[self.inventory.indexOf(item)]
		game.items.append(item)
		game.game_log.append("You drop the item named" + item.name)
		self.time += 1.0

	def give_weapon(self, weapon):
		data = Weapons.array[weapon]

		# Create Weapon Object
		if len(data) == 9:
			w = Weapon(weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, data[7], data[8])
			self.wielding.append(w)
		elif len(data) == 7:
			w = Weapon(weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], None)
			self.wielding.append(w)
		else:
			w = Weapon(weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, data[7])
			self.wielding.append(w)
		return w

	def calc_AC(self):
		return self.equipped_armor.armor_rating + self.equipped_armor.enchantment + self.innate_ac


	def atk_mv(self, map, coords):

		if map.square_identity(coords) in set(['|', '-', ' ', '#']):
			return

		if map.square_identity(coords) == '+':
			ret = '+'

			if map.adjacent[coords] is None:
				game.map.new_room(coords)
				return ret
			else:
				game.map.change_room(map.adjacent[coords])
				return ret

		# Self-Explanatory
		ground_booty = ""

		# Check if square is occupied for ATTACK
		for unit in game.units:

			# Make sure it's a monster and adjacent to it
			if coords == unit.loc and type(unit) == Monster:


				# Unarmed attacks
				unarmed = []
				if self.hands > 0:
					for i in range(self.hands):
						unarmed.append(self.give_weapon('fist'))

				# Find melee weapons
				weaps = []
				for item in self.wielding[::-1]:
					if type(item) == Weapon:
						if item.wclass not in Weapons.ranged_wclasses:
							weaps.append(item)

				# Attack with each weapon
				for item in weaps:
					if unit.hp > 0:
						self.attack(unit, item)

				# Unequip fists
				for fist in unarmed:
					self.wielding.remove(fist)


				# Enemy Well-being Statement

				# Enemy over 90%
				if unit.hp / unit.maxhp > 0.9:
					game.game_log.append("The "  + str(unit.name) + " seems uninjured.")

				# Enemy over 70%	
				elif unit.hp / unit.maxhp > 0.7:
					game.game_log.append("The "  + str(unit.name) + " seems only lightly wounded.")

				# Enemy over 30%
				elif unit.hp / unit.maxhp > 0.3:
					game.game_log.append("The "  + str(unit.name) + " seems moderately wounded.")

				# Enemy under 30%
				elif unit.hp > 0:
					game.game_log.append("The "  + str(unit.name) + " seems nearly dead!")


				# Unarmed wspeed
				maxas = 0.9 - (0.05 * self.dex)


				# Calc Attack Speed
				if len(weaps) != 0:
					maxas = 0
					for weapon in weaps:
						 if weapon.speed > maxas and weapon.wclass not in Weapons.ranged_wclasses:
						 	maxas = weapon.speed

				# Attack time
				self.time += maxas

				# Don't Move
				return






		# Check whats on the ground
		for item in game.items:

			if coords == item.loc and type(item) == Chest:
				if item.opened:
					game.game_log.append("You see here an opened chest")
				else:
					game.game_log.append("You see here a chest")

			# Look for loot on the ground in case of a move
			elif coords == item.loc:

				# Enchantment String
				ench = item.enchantment
				if ench >= 0:
					ench = '+' + str(ench)

				if item.brand is not None and item.brand != "plate":

					# Brand case
					if len(ground_booty) == 0:
						ground_booty += str(item.brand) + ' ' + str(ench) + ' ' + item.name
					else:
						ground_booty += ', ' + str(item.brand) + ' ' + str(ench) +  ' ' + item.name
				else:
					# No Brand Case
					if len(ground_booty) == 0:
						ground_booty += str(ench) + ' ' + item.name
					else:
						ground_booty += ', ' + str(ench) +  ' ' + item.name

		# Add ground loot to the log
		if len(ground_booty) != 0:
			game.game_log.append("You see here: " + ground_booty)

		# Move unit
		self.loc = coords
		self.time += self.mspeed


	def attack(self, enemy, weapon):

		if self.name in Weapons.spells:
			# weapon.zap(self,enemy)
			pass
		else:
			# Hit the enemy
			weapon.strike(self,enemy)


		# If enemy is defeated
		if enemy.hp <= 0:

			# Remove from units
			game.game_log.append("You slay the "  + str(enemy.name) + " with the " + str(weapon.name) + "!")
			game.units.remove(enemy)

			# Drop Loot
			enemy.drop_booty()

			# XP Gain
			self.xp += enemy.xp + int(d(self.cha) / 2)

			# End
			return

	


class Monster():

	def __init__(self,      name, char, tier,    con, st, dex, int, cha, mspeed, xp,   pot_weapons, pot_armor,  loc, other_items = None):

		# Initialize Representation
		self.rep, self.name, self.tier = char, name, tier

		# Initialize Health
		bonushp = multiple_d(6,self.tier)
		self.maxhp = 5 * con + bonushp
		self.hp = 5 * con + bonushp

		# Initialize Mana
		self.mana = 3 * int
		self.maxmana = 3 * int

		# Coordinates
		self.loc, self.time = loc, 1
		self.passives, self.spells = [], []

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.xp = con, st, dex, int, cha, mspeed, xp

		# Monster's Equipment
		self.wielding , self.other_items = [], other_items

		# Give innate weapons / shields
		if other_items is not None:
			for item in other_items:
				if item in Weapons.array:
					self.give_weapon(item)
				if item in Shields.array:
					self.give_shield(item)
				if item in Weapons.spells:
					self.spells.append(Weapons.spells[item])

		self.give_weapon(pot_weapons[d(len(pot_weapons)) - 1])
		self.give_armor( pot_armor[  d(len(pot_armor)) - 1])

	def calc_AC(self):
		return self.equipped_armor.armor_rating + self.equipped_armor.enchantment

	def drop_booty(self):
		for weapon in self.wielding:
			if weapon.hands > 0:
				weapon.loc = self.loc
				game.items.append(weapon)
		self.equipped_armor.loc = self.loc
		game.items.append(self.equipped_armor)

	def give_weapon(self, weapon):
		data = Weapons.array[weapon]

		
		# Manage Enchantment
		spawned_enchantment = data[3]
		if d(10) + (1.5 * self.tier) > 13:
			spawned_enchantment += d(self.tier - 1)

		# Create Weapon Object
		if len(data) == 9:
			self.wielding.append(Weapon(weapon, data[0], data[1], data[2], spawned_enchantment, data[4], data[5], data[6], None, data[7], data[8]))
		elif len(data) == 7:
			self.wielding.append(Weapon(weapon, data[0], data[1], data[2], spawned_enchantment, data[4], data[5], data[6], None))
		else:
			self.wielding.append(Weapon(weapon, data[0], data[1], data[2], spawned_enchantment, data[4], data[5], data[6], None, data[7]))

	def give_armor(self, armor):
		data = Armors.array[armor]

		# Manage Enchantment
		spawned_enchantment = data[3]

		if d(10) + (1.5 * self.tier) > 13:
			spawned_enchantment += d(self.tier - 1)

		# Create Armor Object
		if len(data) == 4:
			self.equipped_armor = Armor(armor, data[0], data[1], data[2], spawned_enchantment, None)
		else:
			self.equipped_armor = Armor(armor, data[0], data[1], data[2], spawned_enchantment, None, data[4])

	def give_shield(self, shield):
		data = Shields.array[shield]

		# Manage Enchantment
		spawned_enchantment = data[3]

		if d(10) + (1.5 * self.tier) > 10:
			spawned_enchantment += d(self.tier)

		# Create Shield Object
		if len(data) == 4:
			self.wielding.append(Shield(shield, data[0], data[1], data[2], spawned_enchantment, None))
		else:
			self.wielding.append(Shield(shield, data[0], data[1], data[2], spawned_enchantment, None, data[4]))

	def zap(self, spell, attacker, enemy):
		spell(attacker, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler)

	def turn(self):

		# MAGIC!!
		if len(self.spells) > 0:
			# Chance to use spells
			if d(10) + self.int >= 11:

				# Zap with spells
				for spell in self.spells:

					in_range = spell(self, game.player, game, Maps.rooms[game.map.map][0], game.map.room_filler)

					if in_range:
						return


		# Melee Attack
		if adjacent_to(self,game.player):

			# Find weapons
			weaps = []
			for item in self.wielding[::-1]:
				if type(item) == Weapon:
					weaps.append(item)

			# Calc Attack Speed
			if len(weaps) != 0:
				maxas = 0
				for weapon in weaps:
					 if weapon.speed > maxas and weapon.wclass not in Weapons.ranged_wclasses:
					 	maxas = weapon.speed

			# Hit with melee
			for item in weaps:
				if item.wclass not in Weapons.ranged_wclasses:
					item.strike(self,game.player)

			self.time += maxas

			return 

		# Make Ranged attacks
		for item in self.wielding:
			if type(item) == Weapon:
				if item.wclass in Weapons.ranged_wclasses:
					los = ai.los(self.loc, game.player.loc, Maps.rooms[game.map.map][0], game )
					if los is not None:

						# Ranged range
						if len(los) <= (2 * item.damage  + item.to_hit):
							item.strike(self, game.player)
							self.time += item.speed
							return

		# If can't, move
		ai.smart_move_towards(self, game.player, game)
		self.time += self.mspeed




class Weapon():

	def __init__(self,  name, rep, wclass, hands, enchantment, damage, to_hit, speed,   loc, brand = None, probability = None):

		# Initialize Weapon Stats
		self.name, self.rep, self.wclass, self.hands, self.enchantment, self.damage, self.to_hit, self.speed, self.loc, self.brand, self.probability = name, rep, wclass, hands, enchantment, damage, to_hit, speed, loc, brand, probability

		# Deal with prob
		if self.probability is None:
			self.probability = 100

	def strike(self, attacker, enemy):

		if d(100) > (100 - self.probability):

			# Calc Encumberance
			self_encumb = attacker.equipped_armor.encumberance - attacker.equipped_armor.enchantment
			enemy_encumb = enemy.equipped_armor.encumberance - enemy.equipped_armor.enchantment

			for item in attacker.wielding:
				if type(item) == Shield:
					self_encumb += item.encumberance
			for item in enemy.wielding:
				if type(item) == Shield:
					enemy_encumb += item.encumberance

			# TO HIT formula
			if d(100) + (4 * (attacker.dex - enemy.dex) ) + (2 * self.to_hit) + self.enchantment > 40 + 1.5 * self_encumb - 1.5 * enemy_encumb:

				# Shield Block
				for weapon in enemy.wielding:
					if type(weapon) == Shield:
						if d(100) > (90 - (2 * weapon.armor_rating) ):

							# Block Statement
							if type(attacker) == Monster:
								game.game_log.append("You block the "   + str(attacker.name) + "'s " + self.name + " with your " + weapon.name + "!")
							else:
								game.game_log.append("The "   + str(enemy.name) +  " blocks your " + self.name + " with its " + weapon.name + "!")
							return


				# DAMAGE forumla

				# Ranged weapon
				if self.wclass in Weapons.ranged_wclasses:
					damage = int (d(self.damage) + attacker.dex / 2 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
				# Melee weapon
				else:
					damage = int (d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )


				# Apply Brands
				brandhit = False

				if self.brand == "envenomed":
					brandhit = d(100) > 20
				elif self.brand == "flaming":
					brandhit = d(100) > 60
				elif self.brand == "frozen":
					brandhit = d(100) > 65
				elif self.brand is not None:
					brandhit = True

				# Apply Brands
				damage = self.apply_brands(attacker, enemy, damage, brandhit)

				# Weapon class effects
				damage = self.weapon_type_effect(attacker, enemy, damage)

				# No damage case
				if damage <= 0:
					damage = 0

					if type(attacker) == Monster:
						game.game_log.append("The "  + str(attacker.name) + " hits you with its " + self.wclass + " but does no damage!")
					else:
						game.game_log.append("You " + Weapons.weapon_classes[self.wclass][0] + " your "+ str(self.wclass) + " " + Weapons.weapon_classes[self.wclass][1] + " the " + str(enemy.name)+ " but deal no damage!")

				# Damage case
				else:
					# Damage statement, MF's
					self.damage_statement(attacker, enemy, damage, brandhit)
						
				# Resolve Damage
				enemy.hp -= damage

			# Miss Case
			else:
				if self.wclass in Weapons.ranged_wclasses:
					if type(attacker) == Monster:
						game.game_log.append("The "  + str(attacker.name) + " fires at you with its " + self.wclass + " but misses.")
					else:
						game.game_log.append("You closely miss the " + str(enemy.name) + " with your " + self.wclass + "!")
				else:
					if type(attacker) == Monster:
						game.game_log.append("The "  + str(attacker.name) + " swings at you with its " + self.wclass + " but misses.")
					else:
						game.game_log.append("You closely miss the " + str(enemy.name) + " with your " + self.wclass + "!")


	def weapon_type_effect(self, attacker, enemy, damage):
		if self.wclass == "hammer" or self.wclass == "club" or self.wclass == "god hammer":
			if enemy.equipped_armor.brand == 'plate':
				damage *= 1.5
		return int(damage)


	def apply_brands(self, attacker, enemy, damage, brandhit):
		# APPLY BRANDS
		if brandhit:
			if self.brand == "flaming":
				count = Brands.dict["flaming"]["count"]
				status = "aflame"

				for passive in enemy.passives:
					
					if passive[0] == status:
						return damage

				enemy.passives.append([status, count])

			if self.brand == "frozen":
				count = Brands.dict["frozen"]["count"]
				status = "frozen"

				for passive in enemy.passives:
					
					if passive[0] == status:
						return damage

				enemy.passives.append([status, count])
				enemy.dex -= Brands.dict["frozen"]["dex_loss"]

			if self.brand == "vampiric":
				attacker.hp += int(damage / 3)

				# Heal
				if attacker.hp > attacker.maxhp:
					attacker.hp = attacker.maxhp

			if self.brand == "hellfire":
				damage += int((1 - (enemy.hp / enemy.maxhp) ) * damage * 0.5)

			if self.brand == "envenomed":
				count = Brands.dict["envenomed"]["count"]
				status = "poisoned"

				for passive in enemy.passives:

					if passive[0] == status:
						passive[1] += count
						return damage

				enemy.passives.append([status, count])

		# Return DAMAGE
		return damage


	def damage_statement(self, attacker, enemy,  damage, brandhit):
		attacker_var =  str(attacker.name)
		attackee_var = str(enemy.name)

		# Make the sentence awesome
		verb, preposition = Weapons.weapon_classes[self.wclass]

		# Make the notes dank
		if self.brand is None or not brandhit:
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " +  self.name + "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(self.wclass) + " " + preposition + " the " + attackee_var + " for " + str(damage) + " damage!")

		elif self.brand == "vampiric":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its "  + self.name + " and steals your life!")
			else:
				game.game_log.append("You " + verb + " your vampiric "+ str(self.wclass) + " " + preposition + " the " + attackee_var+ ", dealing " + str(damage) + " damage and draining its life!")

		elif self.brand == "flaming":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " + self.name + " and sets you aflame!")
			else:
				game.game_log.append("You " + verb + " your flaming "+ str(self.wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and setting it aflame!")

		elif self.brand == "frozen":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " + self.name + " and freezes you!")
			else:
				game.game_log.append("You " + verb + " your frozen "+ str(self.wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and freezing it!")

		elif self.brand == "hellfire":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " + self.name + " and sets your soul aflame!")
			else:
				game.game_log.append("You " + verb + " your hellfire " + str(self.wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and tearing its soul!")

		elif self.brand == "envenomed":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " + self.name + " and poisons you!")
			else:
				game.game_log.append("You " + verb + " your envenomed " + str(self.wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and poisoning it!")


class Armor():

	def __init__(self, name, rep,  armor_rating, encumberance, enchantment, loc, brand = None):
		self.name, self.rep, self.armor_rating, self.encumberance, self.enchantment, self.loc, self.brand = name, rep, armor_rating, encumberance, enchantment, loc, brand

class Shield():

	def __init__(self, name, rep,  armor_rating, encumberance, enchantment, loc, brand = None):
		self.name, self.rep, self.armor_rating, self.encumberance, self.enchantment, self.loc, self.brand = name, rep, armor_rating, encumberance, enchantment, loc, brand

		# Hands
		self.hands = 1

class Chest():

	def __init__(self, type, tier,  loc):
		self.tier, self.type, self.loc = tier, type, loc

		# Initialize Rep
		self.rep = '='
		self.opened = False

		if self.type == "orc":
			self.pot_weapons = [["troll hide","drake scale armor"], ["choppa"], ["slica"], ["bear hide"], ["toxic slica"]]
		elif self.type == "elf":
			self.pot_weapons = [["spear","elven leafblade"], ["Singing Spear of Dorn","ranger longbow"]]
		else:
			self.pot_weapons = [["crude shortbow","iron dagger","iron axe"], ["iron battleaxe","iron longsword"], ["iron battleaxe"], ["steel plate armor"]]

	def open(self):

		n = game.player.level
		while n > 0:
			if len(self.pot_weapons) == 0:
				return

			tier = self.pot_weapons[game.player.level - 1]
			item_name = tier [ d( len(tier)) - 1]
			if item_name in Weapons.array:
				game.map.room_filler.place_weapon(item_name, self.loc, d(self.tier))
			elif item_name in Armors.array:
				game.map.room_filler.place_armor(item_name, self.loc, d(self.tier))
			elif item_name in Shields.array:
				game.map.room_filler.place_shield(item_name, self.loc, d(self.tier))
			self.pot_weapons.remove(tier)
			n -= 1
		self.opened = True





		














			






class Map():

	def __init__(self, player, room):

		self.map = room

		self.player = player
		self.def_map_array = Maps.rooms[self.map][0]

		self.entry_point, self.exits = Maps.rooms[self.map][2], Maps.rooms[self.map][3]


		self.adjacent = {self.entry_point: None}
		for point in self.exits:
			self.adjacent[point] = None

		self.objects = []

		self.filled = False


	def fill(self):
		self.room_filler = RoomFiller(self.player.level, (15,2), self.map)
		self.room_filler.place()


	def extend_map(self):
		pass

	def parse(self,line):

		# Parse for display
		art = ""
		for char in line:
			art += char
		return art


	def display(self, game):

		# Reset Map
		self.map_array = deepcopy(self.def_map_array)

		# Place items
		for item in game.items:
			y, x = item.loc[0], item.loc[1]
			self.map_array[x][y] = item.rep

		# Place each unit on the map
		for unit in game.units[::-1]:
			y, x = unit.loc[0], unit.loc[1]
			self.map_array[x][y] = unit.rep

		# Display the map
		for line in self.map_array:
			print(self.parse(line))

	def change_room(self, new_room):

		room = new_room[0]
		newloc = new_room[1]

		# Store units
		for unit in game.units:
			if type(unit) == Monster:
				self.objects.append(unit)

		for item in game.items:
			self.objects.append(item)

		# Clear units
		game.units, game.items = [game.player], []

		# Add old room's units
		for object in room.objects:
			if type(object) == Monster:
				game.units.append(object)
			else:
				game.items.append(object)

		room.objects = []

		game.map = room


		if newloc == Maps.rooms[new_room[0].map][2]:
			self.player.loc = (newloc[0] + 1, newloc[1])
		else:
			self.player.loc = (newloc[0] - 1, newloc[1])



	def new_room(self, coords):

		# Store units
		for unit in game.units:
			if type(unit) == Monster:
				self.objects.append(unit)

		for item in game.items:
			self.objects.append(item)


		# Clear units
		game.units, game.items = [game.player], []

		# Make new Map
		newmap = Map(self.player, "bridge_crossing")
		game.map = newmap

		# Entry Point
		self.adjacent[coords] = (newmap, newmap.entry_point)
		newmap.adjacent[newmap.entry_point] = (self, coords)
		self.player.loc = (newmap.entry_point[0] + 1, newmap.entry_point[1])


		game.game_log.append("You enter the room...")


	def square_identity(self, coord):
		y,x = coord
		return self.map_array[x][y]

	def can_move(self, unit, loc):
		if self.square_identity(loc) in set(['|', '-', ' ', '#']):
			return False
		for unit in game.units:
			if loc == unit.loc:
				return False
		return True




class RoomFiller():

	def __init__(self, tier, pos, map):
		self.tier = tier
		self.pos = pos
		self.map = map

	def place(self):

		if Maps.rooms[self.map][4]:
			self.fill()

		# QUICKTRAVEL

		# self.place_weapon("uruk crossbow", (1,1))
		# self.place_weapon("toxic slica", (2,1))
		# self.place_armor("wyvern scale mail", (1,2))
		# self.place_shield("tower shield", (2,2))

		# Place Chests
		for type,  loc in Maps.rooms[self.map][1]:
			self.place_chest(type, game.player.level, loc)

	def fill(self):

		band = Bands.dicto[ self.tier ][d(len(Bands.dicto[d(self.tier)])) -1]

		bonus = Bands.formations[band][0]
		groups = Bands.formations[band][1]

		# Cut off some units
		i = 0
		for group in groups[:self.tier + bonus]:

			# Choose which units to spawn
			if len(group) > 0:

				unit =  d(self.tier + 1) - 1
				if unit >= len(group):
					unit = len(group) - 1

				self.spawn(group[unit] , self.pos[::])

				
				if i == 2:
					i = 0
					self.pos = (self.pos[0] + 1, self.pos[1] - 2)
				else:
					self.pos = (self.pos[0], self.pos[1] + 1)

				i += 1


	def spawn(self, monster_name, loc):
		data = Monsters.array[monster_name]

		if len(data) == 11:
			game.units.append(Monster(monster_name, data[0],data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data [10], loc))
		else:
			game.units.append(Monster(monster_name, data[0],data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], loc, data[11]))

	def place_weapon(self, weapon, loc, enchantment = 0, brand = None):
		data = Weapons.array[weapon]

		# Manage Enchantment
		spawned_enchantment = data[3] + enchantment

		# Create Weapon Object
		if len(data) == 7 and brand is None:
			game.items.append(Weapon(weapon, data[0], data[1], data[2], spawned_enchantment, data[4], data[5], data[6], loc))
		else:
			if brand is None:
				brand = data[7]
			game.items.append(Weapon(weapon, data[0], data[1], data[2], spawned_enchantment, data[4], data[5], data[6], loc, brand))

	def place_armor(self, armor, loc, enchantment = 0, brand = None):
		data = Armors.array[armor]

		# Manage Enchantment
		spawned_enchantment = data[2] + enchantment

		# Create Armor Object
		if len(data) == 4 and brand is None:
			game.items.append(Armor(armor, data[0], data[1], data[2], data[3], loc))
		else:
			if brand is None:
				brand = data[4]
			game.items.append(Armor(armor, data[0], data[1], data[2], data[3], loc, brand))

	def place_shield(self, armor, loc, enchantment = 0):
		data = Shields.array[armor]

		# Manage Enchantment
		spawned_enchantment = data[2] + enchantment

		#Create Shield Object
		if len(data) == 4:
			game.items.append(Shield(armor, data[0], data[1], data[2], data[3], loc))

		else:
			if brand is None:
				brand = data[4]
			game.items.append(Shield(armor, data[0], data[1], data[2], data[3], loc, brand))

	def place_chest(self, type, tier, loc):
		game.items.append(Chest(type, tier, loc))














class Game():

	def __init__(self):
		# Manage Constants
		self.race = "Dragonborn"

		self.player = Player(CharacterRaces.races[self.race][0], CharacterRaces.races[self.race][1], self)
		self.map = Map(self.player, 'starting_room')
		self.state = 'ongoing'
		self.room = 0

		# Initiate Regen
		self.regen = 0

		# Manage Units
		self.units, self.items, self.seen = [self.player], [], []

		# Manage Game Log
		self.game_log, self.temp_log = [], []


	def run(self):
		while self.state == 'ongoing':

			

			if not self.map.filled:
				self.map.fill()
				self.map.filled = True



			#  Turn Finder
			min_time = self.player.time
			i = 0
			indeces = []
			for unit in game.units:
				if unit.time < min_time:
					indeces = [i]
					min_time = unit.time
				elif unit.time == min_time:
					indeces.append(i)
				i += 1

			for index in indeces:
				try:
					tunit = game.units[index]
				except:
					continue

				self.check_passives(tunit)
				if type(tunit) == Monster:
					if tunit.hp > 0:
						tunit.turn()
				elif type(tunit) == Player:
					self.player_turn(self.map)

			for unit in game.units:
				# print("Unit: ", unit.time)
				unit.time -= min_time



	def player_turn(self, map):


		def action(move):
			x, y = self.player.loc[0], self.player.loc[1]

			# Regen Health
			if self.player.hp < self.player.maxhp:

				# Increment Counter
				self.regen += 1

				# Regen one health
				if self.regen >= (self.player.reg  -  1/3  * self.player.con):

					self.player.hp += 1
					self.regen = 0


			# Base Case
			if move in set(['h','H','j','J','k','K','l','L','y','Y','u','U','b','B','n','N',',','.','w','W','f','r']):

				# Attack Move (1 turn)
				if move == 'l':
					return self.player.atk_mv(map, (x + 1, y))
				elif move == 'k':
					return self.player.atk_mv(map, (x, y - 1))
				elif move == 'j':
					return self.player.atk_mv(map, (x, y + 1))
				elif move == 'h':
					return self.player.atk_mv(map, (x - 1, y))
				elif move == 'y':
					return self.player.atk_mv(map, (x - 1, y - 1))
				elif move == 'u':
					return self.player.atk_mv(map, (x + 1, y - 1))
				elif move == 'b':
					return self.player.atk_mv(map, (x - 1, y + 1))
				elif move == 'n':
					return self.player.atk_mv(map, (x + 1, y + 1))
				# Run Right
				elif move == 'L':
					if len(game.units) == 1:
						while map.can_move(self.player, (self.player.loc[0] + 1, self.player.loc[1])):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1])) != '+':
								action('l')
								self.player.time = 0
							else:
								break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Up
				elif move == 'K':
					if len(game.units) == 1:
						while map.can_move(self.player, (self.player.loc[0], self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0], self.player.loc[1] - 1)) != '+':
								action('k')
								self.player.time = 0
							else:
								break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Down
				elif move == 'J':
					if len(game.units) == 1:
						while map.can_move(self.player, (self.player.loc[0], self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0], self.player.loc[1] + 1)) != '+':
								action('j')
								self.player.time = 0
							else:
								break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Left
				elif move == 'H':
					if len(game.units) == 1:
						while map.can_move(self.player, (self.player.loc[0] - 1, self.player.loc[1])):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1])) != '+':
								action('h')
								self.player.time = 0
							else:
								break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run UL
				elif move == 'Y':
					if len(game.units) == 1:
						while map.can_move(self.player, (self.player.loc[0] - 1, self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1] - 1)) != '+':
								action('y')
								self.player.time = 0
							else:
								break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run UR
				elif move == 'U':
					if len(game.units) == 1:
						while map.can_move(self.player, (self.player.loc[0] + 1, self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1] - 1)) != '+':
								action('u')
								self.player.time = 0
							else:
								break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run DL
				elif move == 'B':
					if len(game.units) == 1:
						while map.can_move(self.player, (self.player.loc[0] - 1, self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1] + 1)) != '+':
								action('b')
								self.player.time = 0
							else:
								break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run DR
				elif move == 'N':
					if len(game.units) == 1:
						while map.can_move(self.player, (self.player.loc[0] + 1, self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1] + 1)) != '+':
								action('n')
								self.player.time = 0
							else:
								break
					else:
						game.temp_log.append("There are enemies nearby!")

				# fire
				elif move == 'f':
					valid = self.player.fire()
				# wield
				elif move == 'w':
					self.equip(Weapon)
				# Wear
				elif move == 'W':
					self.equip(Armor)
				# Pick up form ground (1 turn)
				elif move == ',':
					# Find items on square
					self.investigate()
				# Wait
				elif move == '.':
					self.player.time += 1
				# rest
				elif move == 'r':
					if len(game.units) == 1:
						while self.player.hp < self.player.maxhp:
							action('.')
						game.temp_log.append("You feel well-rested")
						self.player.time = 0
					else:
						game.temp_log.append("There are enemies nearby!")
			else:
				game.temp_log.append("Invalid Move")









		# Manage Game Log
		self.game_log.append("                                                                     ")


		ex = len(self.temp_log)

		log_select = self.game_log[((len(Maps.rooms[game.map.map][0]) - 26) + ex):]
		print("=======================================================================================")
		print("                                                                     ")


		# Display Game Log
		for line in log_select:
			print(line)
		for line in self.temp_log:
			print(line)

		# Reset Temp Log
		self.temp_log = []



		# Check levelup
		self.player.check_level_up()





		print("=======================================================================================")
		print("                                                                     ")

		# Display map
		self.map.display(self)
		print("                                                                     ")



		# Print HP / Mana / Wielding / Wearing
		weapon_string = ""
		for item in self.player.wielding:
			if type(item) != Armor:
				if item.hands != 0:
					if item.enchantment >= 0:
						weapon_string += " +" + str(item.enchantment) + " " + item.name + " (" + str(item.hands) + "h)"
					else:
						weapon_string += " " + str(item.enchantment) + " " + item.name + " (" + str(item.hands) + "h)"

		# Wielding Nothing
		if weapon_string == "":
			weapon_string = " None"

		# Enchantment Strings
		a_ench = self.player.equipped_armor.enchantment
		if a_ench >= 0:
			a_ench = '+' + str(a_ench)

		print("Level " + str(self.player.level) + " " + self.race)
		print("HP    " + str(self.player.hp)   + "/" + str(self.player.maxhp)   + "               Wielding:" + weapon_string + "             Armor: " + str(a_ench) + ' ' + self.player.equipped_armor.name)
		print("MANA  " + str(self.player.mana) + "/" + str(self.player.maxmana))

		# YOU DIE!!
		if self.player.hp <= 0:
			print("You have been slain!")
			print("You suck at this game bruh")
			self.state = "defeat"
			return


		# See Monster
		for unit in self.units:
			if unit not in self.seen and type(unit) == Monster:

				wielding = ""
				for item in unit.wielding[::-1]:
					if wielding == "" and item.hands > 0:
						wielding += item.name
					elif item.hands > 0:
						wielding += (", a " + item.name)

				if len(wielding) == 0:
					game.game_log.append("You see a " + unit.name + ", wearing " + unit.equipped_armor.name)
				else:
					game.game_log.append("You see a " + unit.name + ", wearing " + unit.equipped_armor.name + " and wielding a " + wielding)
				self.seen.append(unit)





		# --- Old Enter code 1/2-----

		# Valid Input
		# move = input("Your move: ")

		# # Perform
		# for act in move:
		# 	if len(move) == 1:
		# 		action(act)

		# --- New Sytem Halt Code 1/1-----

		fd = sys.stdin.fileno()
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON
		newattr[3] = newattr[3] & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		oldterm = termios.tcgetattr(fd)
		oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

		print("")
		print("Your Move:")
		inp, outp, err = select.select([sys.stdin], [], [])
		move = sys.stdin.read()

		# move = input("Your move: ")

		action(move)
		print(move)
		# print("hello")

		# Reset the terminal:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



		return

			# --- Old Enter code 2/2-----


			# elif len(game.units) == 1:
			# 	self.player.time = 0
			# 	if action(act) == '+':
			# 		break
			# 	else:
			# 		pass
			# else:
			# 	game.temp_log.append("Slow down bro, there are enemies in range!")
			# 	return

		



	def investigate(self):
		drops = []
		opened_a_chest = False
		for item in self.items:
			if self.player.loc == item.loc:
				if type(item) != Chest:
					drops.append(item)
				else:
					if not item.opened:
						game.game_log.append("You bust open the chest!")
						print("You bust open the chest!")
						item.open()
						opened_a_chest = True
						# self.investigate()
						# return

		# One item on the ground
		if len(drops) == 1 and not opened_a_chest:
			self.player.pick_up(drops[0])

		# Nothing on the ground
		elif len(drops) == 0:
			game.temp_log.append("There is nothing here to interact with.")
			return

		# Multiple ground items
		else:
			self.ground_inventory(drops)


	def equip(self, item_type):
		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		item_array = []
		for item in self.player.inventory:
			if type(item) == item_type:
				item_array.append(item)
			if item_type == Weapon and type(item) == Shield:
				item_array.append(item)

		# Empty Case
		if len(item_array) == 0:
			game.temp_log.append("Your inventory is empty!")
			return

		else:
			print("=======================================================================================")
			print("                                                                     ")

			for i in range(len(item_array)):

				unit = item_array[i]

				if unit.brand is not None and unit.brand != "plate":

					print( item_order[i] + " - " + unit.brand + " +" + str(unit.enchantment) + ' ' + unit.name)
				else:
					print( item_order[i] + " - +" + str(unit.enchantment) + ' ' + unit.name)

			print("                                                                     ")
			print("=======================================================================================")

			# valid = False

			# while not valid:

			fd = sys.stdin.fileno()
			newattr = termios.tcgetattr(fd)
			newattr[3] = newattr[3] & ~termios.ICANON
			newattr[3] = newattr[3] & ~termios.ECHO
			termios.tcsetattr(fd, termios.TCSANOW, newattr)
			valid = False

			oldterm = termios.tcgetattr(fd)
			oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

			while not valid:

				print("")
				print("Equip which item? (enter '9' to cancel)")
				inp, outp, err = select.select([sys.stdin], [], [])
				decision = sys.stdin.read()

				if decision == '9':
					valid = True
					return
				elif len(decision) == 1:
					if decision in item_order:
						if item_order.index(decision) < len(item_array):
							self.player.equip(item_array[item_order.index(decision)])
							valid = True
						else:
							print("That is not a valid input")
				else:
					print("That is not a valid input")
			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

				

	def ground_inventory(self, drops):
		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		print("=======================================================================================")
		print("                                                                     ")

		for i in range(len(drops)):

			unit = drops[i]

			if unit.brand is not None and unit.brand != "plate":

				print( item_order[i] + " - " + unit.brand + " +" + str(unit.enchantment) + ' ' + unit.name)
			else:
				# Positive Encahntment
				if unit.enchantment >= 0:
					print( item_order[i] + " - +" + str(unit.enchantment) + ' ' + unit.name)
				else:
					print( item_order[i] + " - " + str(unit.enchantment) + ' ' + unit.name)

		print("                                                                     ")
		print("=======================================================================================")


		fd = sys.stdin.fileno()
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON
		newattr[3] = newattr[3] & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		oldterm = termios.tcgetattr(fd)
		oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
		valid = False

		while not valid:

			print("")
			print("Pick up which items? (enter '9' to cancel)")
			inp, outp, err = select.select([sys.stdin], [], [])
			decision = sys.stdin.read()

			# decision = input("Pick up which items? (enter '9' to cancel)")
			if decision == '9':
				valid = True
				return
			decision = set([char for char in decision])
			for char in decision:
				if char in item_order:
					if item_order.index(char) < len(drops):
						self.player.pick_up(drops[item_order.index(char)])
						valid = True
					else:
						print("That is not a valid input")
		# Reset the terminal:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



	def check_passives(self, unit):



		for passive in unit.passives:

			name = passive[0]
			count = passive[1]

			# Manage poisoned
			if name == "poisoned":

				damage = Brands.dict["envenomed"]["damage"]
				unit.hp -= damage

				if type(unit) == Player:
					game.game_log.append("The venom stings you for " + str(damage) + " damage!")
				else:
					game.game_log.append("The venom stings the " + str(unit.name) + " for " + str(damage) + " damage!")

			# Manage aflame
			if name == "aflame":

				damage = Brands.dict["flaming"]["damage"]
				unit.hp -= damage

				if type(unit) == Player:
					game.game_log.append("The fire burns you for " + str(damage) + " damage!")
				else:
					game.game_log.append("The fire burns the " + str(unit.name) + " for " + str(damage) + " damage!")

			# Decrement Count
			passive[1] -= 1
			if passive[1] <= 0:

				# Manage frozen
				if name == "frozen":
					unit.dex += Brands.dict["frozen"]["dex_loss"]

				unit.passives.remove([passive[0], passive[1]])



		# Check if unit is still alive
		if unit.hp <= 0 and type(unit) != Player:
			game.game_log.append("The " + unit.name + " dies from its wounds!")
			game.units.remove(unit)

			
			if type(unit) == Monster:
				# Drop Loot
				unit.drop_booty()

				# XP Gain
				game.player.xp += unit.xp + int(d(game.player.cha) / 2)














def d(range):
	return randint(1,range)

def multiple_d(range, number):
	sum = 0
	while number > 0:
		sum += d(range)
		number -= 1
	return sum

def adjacent_to(one, two):
	return True if (abs(one.loc[0] - two.loc[0]) <= 1) and (abs(one.loc[1] - two.loc[1]) <= 1) else False






game = Game()
game.run()








