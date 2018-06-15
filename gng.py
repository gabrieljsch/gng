from maps import Maps
import ai

from bestiary import Monsters, Bands
from codex import Weapons, Ammos, Brands, Armors, Shields
from character import CharacterInfo
from descriptions import Descriptions

from random import randint, shuffle
from copy import deepcopy

import sys, os
import termios, fcntl
import select



class Player():

	def __init__(self, statsheet, innate_equipment, game):

		# Initialize Location, Time
		self.loc, self.time = (2,5), 0

		# Initialize Representation
		self.rep, self.name, self.info, self.passives, self.race, self.pclass  = '@', "you", ('you','your'), [], game.race, game.pclass

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.reg = statsheet[:7]

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = statsheet[7]

		# Class bonus
		if CharacterInfo.class_progression[self.pclass][0] == 'con': self.con += 1
		elif CharacterInfo.class_progression[self.pclass][0] == 'str': self.str += 1
		elif CharacterInfo.class_progression[self.pclass][0] == 'dex': self.dex += 1
		elif CharacterInfo.class_progression[self.pclass][0] == 'int': self.int += 1
		elif CharacterInfo.class_progression[self.pclass][0] == 'cha': self.cha += 1

		self.hp = 5 + self.con * 5 + self.str
		self.maxhp = 5 + self.con * 5 + self.str

		self.mana = 4 + 4 * self.int
		self.maxmana = 4 + 4 * self.int

		# Inventory, Spells
		self.inventory, self.spells, self.abilities, self.cooldowns = [], [], [], []

		# Initialze Equipment
		self.wielding, self.hands, self.quivered = [], 2, None

		# Innate Equipment
		for equipment in innate_equipment:
			if equipment in Weapons.array: weap = self.give_weapon(equipment)
			elif equipment[0] in Weapons.spells and equipment[1]: self.abilities.append(equipment[0])
			elif equipment[0] in Weapons.spells and not equipment[1]: self.spells.append(equipment[0])

		# Class Equipment
		for item in CharacterInfo.race_starting_equipment[game.race][CharacterInfo.class_list.index(game.pclass)]:
			if item in Ammos.array:
				data = Ammos.array[item]
				if data[1] in Ammos.thrown_amclasses: number = 6
				else: number = 20
				self.inventory.append(Ammo(item,data[0],data[1],number,data[2],None))
				self.quivered = self.inventory[-1]
			elif item in Weapons.array: self.give_weapon(item)
			elif item in Shields.array:
				data = Shields.array[item]
				try: brand = data[5]
				except: brand = None
				self.wielding.append(Shield(item,data[0],data[1],data[2],data[3],data[4],None,brand))
				self.hands -= data[1]
			elif item in Armors.array:
				data = Armors.array[item]
				try: brand = data[5]
				except: brand = None
				self.equipped_armor = Armor(item,data[0],data[1],data[2],data[3],data[4],None,brand)
			elif type(item) == tuple:
				if item[1]: self.abilities.append(item[0])
				else: self.spells.append(item[0])

		# Initialize Level, XP
		self.level, self.xp, self.xp_levels = 1, 0, 12

		# Racial Bonuses
		self.innate_ac = 0

		# Apply Racial Passives
		self.racial_bonuses(game)

	def calc_resistances(self):
		return [self.frostr + self.equipped_armor.frostr, self.firer + self.equipped_armor.firer, self.poisonr + self.equipped_armor.poisonr, self.acidr + self.equipped_armor.acidr, self.shockr + self.equipped_armor.shockr, self.expr + self.equipped_armor.expr]

	def calc_mdamage(self):
		sd = 0
		for weapon in self.wielding: sd += weapon.mdamage
		return sd

	def quiver_string(self):
		if self.quivered.brand is None:
			if self.quivered.number > 1: game.game_log.append("You quiver " + str(self.quivered.number) + " " + self.quivered.name + "s!")
			else: game.game_log.append("You quiver 1 " + self.quivered.name + "!")
		else:
			if self.quivered.number > 1: game.game_log.append("You quiver " + str(self.quivered.number) + " " + self.quivered.brand + ' ' + self.quivered.name + "s!")
			else: game.game_log.append("You quiver 1 " + self.quivered.brand + ' ' + self.quivered.name + "!")


	def racial_bonuses(self, game):

		# Innate bonuses
		if self.race == 'Dragonborn':
			self.innate_ac += 2
		if self.race == 'Hill Troll':
			self.innate_ac += 1
			self.hands = 4


	def quiver(self, bypass = None):

		if bypass is None:

			ammo = [thing for thing in self.inventory if type(thing) == Ammo and thing != self.quivered]

			if len(ammo) != 0:
				print("=======================================================================================")
				print("                                                                     ")
				for i in range(len(ammo)): print(str(game.item_order[i]) + " - " + ammo[i].string())
				print("                                                                     ")
				print("=======================================================================================")

				decision = rinput("Quiver What?")

				if decision in game.item_order and game.item_order.index(decision) < len(ammo):

					# Quiver Item
					self.quivered = ammo[game.item_order.index(decision)]
					self.time += self.mspeed

					# Quiver Statement
					self.quiver_string()

				else: game.temp_log.append("That is not a valid option")

			else: game.temp_log.append("You have nothing to quiver.")

		else:
			self.quivered = bypass
			self.time += self.mspeed

			# Quiver Statement
			self.quiver_string()





	def fire(self):

		# Throwing weapon
		thrown = False
		if self.quivered is not None:
			if self.quivered.wclass in Ammos.thrown_amclasses:
				thrown = True
				# Create Throwing platform
				item = self.give_weapon(self.quivered.name)



		for item in self.wielding:

			# Ranged Projectile Thrower
			if item.wclass in Weapons.ranged_wclasses or item.wclass in Ammos.thrown_amclasses:

				# Check for quiver
				if self.quivered is None:
					game.temp_log.append("You do not have the correct ammo type quivered.")
					return
				# Wrong ammo type
				if item.wclass in Weapons.ranged_wclasses and self.quivered.wclass not in Ammos.projectile[item.wclass]:
					game.temp_log.append("You do not have the correct ammo type quivered.")
					if thrown: self.wielding.pop()
					return

				units_in_range = []
				for unit in game.units[1:]:
					los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
					if los is not None and (len(los) - 1 <= (item.range)):
						# if len(units_in_range) == 1:
						# 	for unit in units.in_range:
						# 		if len(los) <= unit[0]: unit.

						units_in_range.append(unit)
				# units_in_range = [units_in_range[0] for unit in unit.range]

				# Ranged range
				if len(units_in_range) != 0:
					print("=======================================================================================")
					print("                                                                     ")
					for i in range(len(units_in_range)): print(str(game.item_order[i]) + " - " + units_in_range[i].name)
					print("                                                                     ")
					print("=======================================================================================")


					decision = rinput("Aim at which enemy?")

					if decision in game.item_order and game.item_order.index(decision) < len(units_in_range):

						# Choose Legal Enemy
						unit = units_in_range[game.item_order.index(decision)]
						self.time += item.speed

						# ATTACK
						item.strike(self, unit)
						self.well_being_statement(unit, self, item.name, game)

						# Remove throwing weapon
						if thrown:
							self.wielding.pop()

						# Remove Ammo
						self.quivered.number -= 1
						if self.quivered.number == 0:
							self.inventory.remove(self.quivered)
							self.quivered = None
						return

					else:
						game.temp_log.append("That is not a valid input")
						# Remove throwing weapon
						
						if thrown:
							self.wielding.pop()
						return

				else:
					game.temp_log.append("There are no targets in range!")

					# Remove throwing weapon
					if thrown:
						self.wielding.pop()
					return

		game.temp_log.append("You are not wielding a ranged weapon!")
		# Remove throwing weapon
		if thrown:
			self.wielding.pop()


	def well_being_statement(self, enemy, attacker, means, game):

		# If enemy is defeated
		if enemy.hp <= 0:

			# Check for Indomibable
			for name, count in enemy.passives:
				if name == 'indominable':
					enemy.hp = 1
					game.game_log.append("The "  + str(enemy.name) + " refuses to die!")
					return

			# Remove from units
			verb = 'slay' if attacker.name == 'you' else 'slays'
			game.game_log.append( attacker.info[0][0].upper() + attacker.info[0][1:] + " " + verb + " the "  + str(enemy.name) + " with " + attacker.info[1] + " " + means + "!")
			game.units.remove(enemy)
			if enemy in game.allies: game.allies.remove(enemy)

			# Ooze Passive
			if 'split' in enemy.spells: Weapons.spells["split"][0]("split", enemy, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler)


			# Drop Loot
			enemy.drop_booty()

			# XP Gain
			self.xp += enemy.xp + int(d(self.cha) / 2)
			return

		if enemy.hp / enemy.maxhp > 0.95: game.game_log.append("The "  + str(enemy.name) + " seems uninjured.")

		# Enemy over 70%	
		elif enemy.hp / enemy.maxhp > 0.7: game.game_log.append("The "  + str(enemy.name) + " seems only lightly wounded.")

		# Enemy over 30%
		elif enemy.hp / enemy.maxhp > 0.3: game.game_log.append("The "  + str(enemy.name) + " seems moderately wounded.")

		# Enemy under 30%
		elif enemy.hp > 0: game.game_log.append("The "  + str(enemy.name) + " seems nearly dead!")





	def cast(self, type, array):
		
		print("=======================================================================================")
		print("                                                                     ")
		for i in range(len(array)):

			if type == "spell": print(str(game.item_order[i]) + " - " + array[i] + " (" + str(Weapons.spells[array[i]][1]) + " mana)")
			else: print(str(game.item_order[i]) + " - " + array[i]+ " (" + str(Weapons.spells[array[i]][1] * 3) + " turns)")

		print("                                                                     ")
		print("=======================================================================================")

		# Controller
		print("")
		if type == "spell": decision = rinput("Use which spell?")
		else: decision = rinput("Use which ability?")

		# Valid Spell
		if decision in game.item_order and game.item_order.index(decision) < len(array):
			spell, spell_name = Weapons.spells[array[game.item_order.index(decision)]][0], array[game.item_order.index(decision)]
		else:
			game.temp_log.append("That is not a valid input")
			return

		if type == "spell":
			# Check Mana
			if self.mana < Weapons.spells[spell_name][1]:
				game.temp_log.append("You don't have enough mana to cast that.")
				return

		# Self-cast
		if not Weapons.spells[spell_name][3]:
			print(spell_name)
			if type == "spell":
				if spell(spell_name, self, self, game, Maps.rooms[game.map.map][0], game.map.room_filler):
					self.time += Weapons.spells[spell_name][2]
					self.mana -= Weapons.spells[spell_name][1]
			else:
				if spell(spell_name, self, self, game, Maps.rooms[game.map.map][0], game.map.room_filler, True):
					self.time += Weapons.spells[spell_name][2]
					self.cooldowns.append( [spell_name, Weapons.spells[spell_name][1] * 3] )
					self.abilities.remove(spell_name)
			return



		# Get units in range
		units_in_range = []
		for unit in game.units[1:]:
			los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
			if los is None: continue
			if Weapons.spells[spell_name][4]:
				if len(los) - 1 <= Weapons.spells[spell_name][5]: units_in_range.append(unit)
			else: units_in_range.append(unit)
		units_in_range = units_in_range[::-1]

		# Ranged range
		if len(units_in_range) != 0:
			print("                                                                     ")
			print("---------------------------------------------------------------------------------------")
			print(spell_name)
			print("                                                                     ")
			print("=======================================================================================")
			print("                                                                     ")
			for i in range(len(units_in_range)):

				unit = units_in_range[i]

				print(str(game.item_order[i]) + " - " + unit.name)
			print("                                                                     ")
			print("=======================================================================================")



			decision = rinput("Cast " + spell_name + " at which target?")


			if decision in game.item_order and game.item_order.index(decision) < len(units_in_range):

				# Choose Legal Enemy
				unit = units_in_range[game.item_order.index(decision)]

				if type == "spell": 
					# Enemy Resist spell
					if d(100) / 100 <= max(0.05, min(0.7, (unit.cha / 2) / self.int)):
						self.time += Weapons.spells[spell_name][2]
						self.mana -= Weapons.spells[spell_name][1]
						game.game_log.append("The " + unit.name + " resists your " + spell_name + "!")
						return

					if spell(spell_name, self, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler):
						self.mana -= Weapons.spells[spell_name][1]
						self.time += Weapons.spells[spell_name][2]
				else:
					if spell(spell_name, self, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler, True):
						self.time += Weapons.spells[spell_name][2]
						self.cooldowns.append( [spell_name, Weapons.spells[spell_name][1] * 3] )
						self.abilities.remove(spell_name)
				return

			else:
				game.temp_log.append("That is not a valid input")
				return
		else:
			game.temp_log.append("There are no targets in range!")
			return


	def racial_level_bonuses(self):
		# Racial level-ups
		if self.race == "Elf" and self.level % 4 == 0:
			if d(10) >= 4: self.inc_dex()
			else: self.inc_int()

		if self.race == "Cytherean" and self.level % 4 == 0:
			if d(10) >= 3: self.inc_int()
			else: self.inc_dex()

		if self.race == "Dragonborn" and self.level % 5 == 0:
			if d(10) <= 5: self.inc_str()
			else: self.inc_con()

		if self.race == "Gnome" and self.level % 4 == 0:
			if d(10) >= 4: self.inc_int()
			else: self.inc_dex()

		if self.race == "Hobbit" and self.level % 4 == 0:
			if d(10) >= 5: self.inc_cha()
			else: self.inc_dex()

		if self.race == "Terran" and self.level % 4 == 0:
			roll = d(10)
			if roll > 8: self.inc_str()
			elif roll > 6: self.inc_dex()
			elif roll > 4: self.inc_cha()
			elif roll > 2: self.inc_int()
			else: self.inc_con()

		if self.race == "Naga" and self.level % 4 == 0:
			if d(10) <= 4: self.inc_con()
			else: self.inc_dex()

		if self.race == "Hill Troll" and self.level % 5 == 0:
			if d(10) <= 5: self.inc_str()
			else: self.inc_con()

		if self.race == "Ghoul" and self.level % 5 == 0:
			if d(10) <= 5: self.inc_str()
			else: self.inc_dex()

		if self.race == "Black Orc" and self.level % 5 == 0:
			if d(10) <= 4: self.inc_str()
			elif d(10) <= 6: self.inc_con()
			else: self.inc_cha()

		if self.race == "Dwarf" and self.level % 4 == 0:
			if d(10) <= 3: self.inc_cha()
			else: self.inc_con()


	def inc_con(self):
		self.con += 1
		self.hp += 5
		self.maxhp += 5
		game.game_log.append("You feel hardier...")

	def inc_str(self):
		self.str += 1
		self.hp +=  1
		self.maxhp += 1
		game.game_log.append("You feel stronger...")

	def inc_dex(self):
		self.dex += 1
		game.game_log.append("You feel more agile...")

	def inc_int(self):
		self.int += 1
		self.mana += 4
		self.maxmana += 4
		game.game_log.append("You feel smarter...")

	def inc_cha(self):
		self.cha += 1
		game.game_log.append("You feel more charismatic...")







	def check_level_up(self):

		# See if enough xp for a level up
		if self.xp >= self.xp_levels:

			game.game_log.append("You've leveled up!")

			# Increment Level
			self.level += 1

			# Gain HP/mana
			bonushp = d(self.con)
			self.hp += 2 + bonushp
			self.maxhp += 2 + bonushp
			self.mana += 2
			self.maxmana += 2

			# Racial level-ups
			self.racial_level_bonuses()


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
				print("Increase your (C)onsititution, (S)trength, (D)exterity, (I)ntelligence, or ch(A)risma?")
				inp, outp, err = select.select([sys.stdin], [], [])
				stat = sys.stdin.read()

				if stat.lower() == "c"or stat.lower() == "s"or stat.lower() == "d"or stat.lower() == "i"or stat.lower() == "a":
					if stat.lower() == "c": self.inc_con()
					elif stat.lower() == "s": self.inc_str()
					elif stat.lower() == "d": self.inc_dex()
					elif stat.lower() == "i": self.inc_int()
					elif stat.lower() == "a": self.inc_cha()
					valid = True

				else: print("Pick a stat!")

			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

	def wield(self, item_type, bypass = None):

		if bypass is None:

			item_array = [item for item in self.inventory if type(item) == item_type or item_type == Weapon and type(item) == Shield]

			# Empty Case
			if len(item_array) == 0:
				if item_type == Weapon: game.temp_log.append("You're not carrying any other weapons!")
				elif item_type == Armor: game.temp_log.append("You're not carrying any other armor!")
				return

			else:
				print("=======================================================================================")
				print("                                                                     ")
				for i in range(len(item_array)): print(game.item_order[i] + " - " + item_array[i].string())
				print("                                                                     ")
				print("=======================================================================================")


				decision = rinput("Equip which item?")
				
				if decision in game.item_order and game.item_order.index(decision) < len(item_array):
					item = item_array[game.item_order.index(decision)]
				else:
					print("That is not a valid input")
					return

		# Inventory Bypass
		else: item = bypass

		# Equip Weapon
		if type(item) == Weapon or type(item) == Shield:

			# Carrying
			total_hands = self.hands
			carrying = []
			for thing in self.wielding:
				total_hands += thing.hands
				if thing.hands > 0: carrying.append(thing)

			# Ranged weapons require all hands
			if item.wclass in Weapons.ranged_wclasses:
				# Remove current weapons
				for weap in carrying:
						self.wielding.remove(weap)
						self.inventory.append(weap)

				# Wield Weapon
				self.hands = 0
				self.wielding.append(item)
				self.inventory.remove(item)
				game.game_log.append("You draw your " + item.name + "!")
				self.time += self.mspeed
				return

			# Not enough total hands
			if item.hands > total_hands or item.hands > 1 and item.wclass != 'bastard sword' and self.race in ['Gnome','Hobbit']:
				game.temp_log.append("You cannot wield that weapon!")
				return

			# Not enough FREE Hands
			if self.hands < item.hands or len(carrying) == 2:

				# Already carrying something
				if len(carrying) == 2 and item.hands < total_hands:

					# Equipped string UI
					equipped = ""
					for i in range(len(carrying)):
						if len(equipped) != 0: equipped += ', ' + '(' + str(game.item_order[i]) + ") " +  carrying[i].string()
						else: equipped += '(' + str(game.item_order[i]) + ") " + carrying[i].string()

					print("")
					decision = rinput("Swap for " + equipped + "?")

					if decision in game.item_order and game.item_order.index(decision) < len(carrying):
						ditem = carrying[game.item_order.index(decision)]

						# Remove chosen item
						game.game_log.append("You put away the " + ditem.name + '.')
						self.wielding.remove(ditem)
						self.inventory.append(ditem)
						self.hands += ditem.hands
					else:
						game.temp_log.append("That is not a valid option.")
						return

				# Remove all items in order to equip
				else:
					for weap in carrying:
						self.wielding.remove(weap)
						self.inventory.append(weap)
						self.hands += weap.hands
			# Wield item
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
		self.time += self.mspeed

	def stash(self, bypass = None):

		if bypass is None:

			# Carrying
			carrying = [thing for thing in self.wielding if thing.hands > 0]

			if len(carrying) > 0:

				# Equipped string UI
				equipped = ""
				for i in range(len(carrying)):
					if len(equipped) != 0: equipped += ', ' + '(' + str(game.item_order[i]) + ") " +  carrying[i].string()
					else: equipped += '(' + str(game.item_order[i]) + ") " + carrying[i].string()

				print("")
				print("Put what into your inventory?")
				decision = rinput(equipped)

				if decision in game.item_order and game.item_order.index(decision) < len(carrying):
					ditem = carrying[game.item_order.index(decision)]

					
				else:
					game.temp_log.append("That is not a valid option.")
					return

			else:
				game.temp_log.append("You are not carrying anything.")
				return
		elif type(bypass) == Ammo:
			if self.quivered.number == 1: game.game_log.append("You put away the " + self.quivered.name + '.')
			else: game.game_log.append("You put away the " + self.quivered.name + 's.')
			self.quivered = None
			self.time += self.mspeed
			return
		else: ditem = bypass

		# Remove chosen item
		game.game_log.append("You put away the " + ditem.name + '.')
		self.wielding.remove(ditem)
		self.inventory.append(ditem)
		self.hands += ditem.hands
		self.time += self.mspeed

	def inventoryize(self):

		# Carrying
		carrying = [thing for thing in self.wielding if thing.hands > 0]
		items = carrying + self.inventory
		items.append(self.equipped_armor)

		if len(self.inventory + carrying) > 0:

			go_back = True
			while go_back: 
				go_back = False

				# Formulate items
				weaps,shields,armors,ammos = [],[],[],[]
				for item in items:
					if type(item) == Ammo: ammos.append(item)
					elif type(item) == Weapon: weaps.append(item)
					elif type(item) == Shield: shields.append(item)
					elif type(item) == Armor: armors.append(item)
				combined = weaps + shields + armors + ammos
				j = 0

				print("=======================================================================================")
				print("                                                                     ")
				if len(weaps) != 0: print("Weapons")
				for i in range(len(weaps)):
					print(game.item_order[j] + " - " + weaps[i].string())
					j += 1
				if len(shields) != 0: print("Shields")
				for i in range(len(shields)):
					print(game.item_order[j] + " - " + shields[i].string())
					j += 1
				if len(armors) != 0: print("Armor")
				for i in range(len(armors)):
					print(game.item_order[j] + " - " + armors[i].string())
					j += 1
				if len(ammos) != 0: print("Ammo")
				for i in range(len(ammos)):
					print(game.item_order[j] + " - " + ammos[i].string())
					j += 1
				print("                                                                     ")
				print("=======================================================================================")

				decision = rinput("Inspect an item?")


				if decision in game.item_order and game.item_order.index(decision) < len(combined):
					ditem = combined[game.item_order.index(decision)]


					print("")
					print("=======================================================================================")

					# Details
					ditem.details()

				else:
					game.temp_log.append("That is not a valid option.")
					return

				# Inventory Options

				# Ammo
				if type(ditem) == Ammo:
					if ditem == self.quivered:
						decision = rinput("(S)tow, (D)rop, or (G)o back?")
						if decision.lower() == 's': self.stash(ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						else: game.temp_log.append("That is not a valid option.")
					else:
						decision = rinput("(Q)uiver, (D)rop, or (G)o back?")
						if decision.lower() == 'q': self.quiver(ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						else: game.temp_log.append("That is not a valid option.")
				# Weapon / Shield
				elif type(ditem) == Weapon or type(ditem) == Shield:
					if ditem in self.wielding:
						decision = rinput("(S)tow, (D)rop, or (G)o back?")
						if decision.lower() == 's': self.stash(ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						else: game.temp_log.append("That is not a valid option.")
					else:
						decision = rinput("(W)ield, (D)rop, or (G)o back?")
						if decision.lower() == 'w': self.wield(Weapon,ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						else: game.temp_log.append("That is not a valid option.")
				# Armor
				elif type(ditem) == Armor:
					if ditem == self.equipped_armor:
						decision = rinput("(D)rop, or (G)o back?")
						if decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
					else:
						decision = rinput("(W)ear, (D)rop, or (G)o back?")
						if decision.lower() == 'w': self.wield(Armor,ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True


		else: game.temp_log.append("You have nothing in your inventory!")


	def pick_up(self, item):
		item.loc = None
		already_in = False
		if type(item) == Ammo:
			for thing in self.inventory:
				if type(thing) == Ammo and thing.name == item.name and thing.brand == item.brand:
					thing.number += item.number
					already_in = True
					break

		game.items.remove(item)
		if not already_in: self.inventory.append(item)
		if type(item) == Ammo:
			if item.number > 1: game.game_log.append("You pick up " + str(item.number) + ' ' + item.name + "s.")
			else: game.game_log.append("You pick up the " + item.name + ".")
		else:
			game.game_log.append("You pick up the " + item.name + ".")
		self.time += self.mspeed

	def drop(self,item):
		item.loc = self.loc
		try:
			if item == self.quivered: self.quivered = None
		except:
			try: self.hands += item.hands
			except: pass

		try: self.wielding.remove(item)
		except: del self.inventory[self.inventory.index(item)]


		game.items.append(item)
		try: game.game_log.append("You drop the " + str(item.number) + ' ' + item.name + "s")	
		except: game.game_log.append("You drop the " + item.name)
		self.time += self.mspeed

	def give_weapon(self, weapon):
		data = Weapons.array[weapon]

		# Manage Brand + Probability
		try: brand = data[7]
		except: brand = None
		try: prob = data[8]
		except: prob = None

		self.hands -= data[2]

		# Create Weapon Object
		if data[1] in Weapons.ranged_wclasses and data[2] > 0:
			self.inventory.append(Weapon(weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, brand, prob))
			return self.inventory[-1]
		else:
 			self.wielding.append(Weapon(weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, brand, prob))
 			return self.wielding[-1]

	def calc_AC(self):
		return self.equipped_armor.armor_rating + self.equipped_armor.enchantment + self.innate_ac

	def atk_mv(self, map, coords):

		# Find melee weapons
		weaps = [item for item in self.wielding[::-1] if type(item) == Weapon and item.wclass not in Weapons.ranged_wclasses]
		carrying = [item for item in self.wielding[::-1] if type(item) in [Weapon,Shield] and item.hands > 0]

		# Initial Weaps
		initial_weaps = len(weaps)

		if map.square_identity(coords) in ['|', '-', ' ', '#','_']: return

		if map.square_identity(coords) == '+':
			if map.adjacent[coords] is None:
				game.map.new_room(coords)
				return '+'
			else:
				game.map.change_room(map.adjacent[coords])
				return '+'

		# Check if square is occupied for ATTACK
		for unit in game.units:

			# Make sure it's a monster and adjacent to it
			if coords == unit.loc and type(unit) == Monster:

				# Equip fists
				if len(carrying) == 0 or (len(carrying) == 1 and self.race == "Hill Troll" or type(carrying[-1]) == Shield and len(carrying) == 1):
					if len(carrying) == 0 and self.race == "Hill Troll":
						fists = self.give_weapon('fist smash')
						weaps.append(fists)
					else:
						fists = self.give_weapon('fists')
						weaps.append(fists)

				# Attack with each weapon
				ranged = True
				for item in weaps:
					ranged = False
					item.strike(self, unit)
					if unit.hp <= 0: break

				if ranged:
					game.temp_log.append("You are not wielding any melee weapons.")
					return

				# Enemy Well-being Statement
				self.well_being_statement(unit, self, item.name, game)

				# Unequip fists
				while len(weaps) > initial_weaps:
					self.wielding.pop()
					weaps.pop()
				# Unarmed wspeed
				maxas = 0.9 - (0.05 * self.dex)

				# Calc Attack Speed
				if len(weaps) != 0:
					maxas = 0
					for weapon in weaps:
						 if weapon.speed > maxas and weapon.wclass not in Weapons.ranged_wclasses: maxas = weapon.speed

				# Attack time
				self.time += maxas

				# Don't Move
				return

		# Check for Traps
		for item in game.items:
			if type(item) == Trap and item.loc == coords:
				item.trip()



		# Check whats on the ground
		ground_booty = ""

		for item in game.items:

			if coords == item.loc and type(item) == Chest:
				if item.opened: game.game_log.append("You see here an opened chest")
				else:
					article = "an" if item.type[0] in ['a','e','i','o','u'] else 'a'
					game.game_log.append("You see here " + article + " " + item.type + " chest")

			# Look for loot on the ground in case of a move
			elif coords == item.loc:
				if len(ground_booty) == 0:
					ground_booty += item.string()
				else: ground_booty += ', ' + item.string()


		# Add ground loot to the log
		if len(ground_booty) != 0: game.game_log.append("You see here: " + ground_booty)

		# Move unit
		self.loc = coords
		self.time += self.mspeed

	


class Monster():

	def __init__(self,      name, char, etype, tier,    con, st, dex, int, cha, mspeed, xp,   resistances,  pot_weapons, pot_armor,  loc, other_items = None):

		# Initialize Representation
		self.rep, self.name, self.info, self.etype, self.tier = char, name, ('the ' + name, 'its'), etype, tier

		# Initialize Health
		bonushp = md(6,self.tier)
		self.maxhp = 5 * con + bonushp
		self.hp = 5 * con + bonushp

		# Initialize Mana
		self.mana, self.maxmana = 5 * int + self.tier, 5 * int + self.tier

		# Coordinates
		self.loc, self.time = loc, 1
		self.passives, self.spells = [], []

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.xp = con, st, dex, int, cha, mspeed, xp

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = resistances

		# Monster's Equipment
		self.wielding , self.other_items, self.quivered, self.inventory = [], other_items, None, []

		# Give innate weapons / shields
		if other_items is not None:
			for item in other_items:
				if item in Ammos.array: self.give_ammo(item)
				elif item in Weapons.array: self.give_weapon(item)
				elif item in Shields.array: self.give_shield(item)
				elif item in Weapons.spells: self.spells.append(item)

		# Give Weapon and Armor
		items = pot_weapons[d(len(pot_weapons)) - 1]
		if type(items) != list: items = [items]
		for item in items:
			if item in Weapons.array: self.give_weapon(item)
			elif item in Shields.array: self.give_shield(item)
		self.give_armor( pot_armor[  d(len(pot_armor)) - 1])

	def calc_resistances(self):
		return [self.frostr + self.equipped_armor.frostr, self.firer + self.equipped_armor.firer, self.poisonr + self.equipped_armor.poisonr, self.acidr + self.equipped_armor.acidr, self.shockr + self.equipped_armor.shockr, self.expr + self.equipped_armor.expr]

	def calc_mdamage(self):
		sd = 0
		for weapon in self.wielding:sd += weapon.mdamage
		return sd

	def calc_AC(self):
		return self.equipped_armor.armor_rating + self.equipped_armor.enchantment

	def drop_booty(self):
		self.equipped_armor.loc = self.loc
		game.items.append(self.equipped_armor)
		for weapon in self.wielding:
			if weapon in Ammos.thrown_amclasses: continue
			if weapon.hands > 0:
				weapon.loc = self.loc
				game.items.append(weapon)
		for item in self.inventory:
			already_in = False
			if type(item) == Ammo:
				for oitem in game.items:
					if oitem.loc == self.loc and type(oitem) == Ammo:
						if oitem.name == item.name and oitem.brand == item.brand:
							oitem.number += item.number
							already_in = True
							break
			if not already_in:
				item.loc = self.loc
				game.items.append(item)
		if self.quivered is not None:

			for item in game.items:
				if item.loc == self.loc and type(item) == Ammo:
					if item.name == self.quivered.name and item.brand == self.quivered.brand:
						item.number += self.quivered.number
						return
			self.quivered.loc = self.loc
			game.items.append(self.quivered)


	def give_weapon(self, weapon):
		data = Weapons.array[weapon]

		# Manage Enchantment
		spawned_enchantment = data[3]
		if d(10) + (1.5 * self.tier) > 13: spawned_enchantment += d(self.tier - 1)

		# Manage Brand + Probability
		try: brand = data[7]
		except:
			if d(100) > 99 - self.tier and data[2] > 0: brand = Brands.weapon_brands[d(len(Brands.weapon_brands)) - 1]
			else: brand = None
		try: prob = data[8]
		except: prob = None

		# Create Weapon Object
		self.wielding.append(Weapon(weapon, data[0], data[1], data[2], spawned_enchantment, data[4], data[5], data[6], None, brand, prob))

	def give_armor(self, armor):
		data = Armors.array[armor]

		# Manage Enchantment
		spawned_enchantment = data[4]
		if d(10) + (1.5 * self.tier) > 13: spawned_enchantment += d(self.tier - 1)
		try: brand = data[5]
		except:
			if d(100) > 99 - self.tier: brand = Brands.armor_brands[d(len(Brands.armor_brands)) - 1]
			else: brand = None

		# Create Armor Object
		self.equipped_armor = Armor(armor, data[0], data[1], data[2], data[3], spawned_enchantment, None, brand)

	def give_shield(self, shield):
		data = Shields.array[shield]

		# Manage Enchantment + brand
		spawned_enchantment = data[4]
		if d(10) + (1.5 * self.tier) > 10: spawned_enchantment += d(self.tier)
		try: brand = data[5]
		except: brand = None

		# Create Shield Object
		self.wielding.append(Shield(shield, data[0], data[1], data[2], data[3], spawned_enchantment, None, brand))

	def give_ammo(self, ammo):
		data = Ammos.array[ammo]

		# Manage Enchantment + Brand
		try: brand = data[3]
		except: brand = None
		if brand is None:
			if d(100) > 99 - self.tier and data[2] > 0: brand = Brands.ammo_brands[d(len(Brands.ammo_brands)) - 1]

		# Manage Number
		if data[1] in Ammos.thrown_amclasses: number = 4 + 2 * self.tier
		else: number = 10 + 5 * self.tier

		# Create Ammo Object
		self.quivered = Ammo(ammo, data[0], data[1], number, data[2], None, brand)


	def turn(self):

		if self in game.allies:
			enemy, mini = None, 100
			for unit in game.units[1:]:
				los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:
					if len(los) < mini:
						enemy, mini = unit, len(los)

			if enemy == None:
				ai.move_towards(self, game.player, game.map)
				self.time += self.mspeed
				return


		else:
			mini, enemy = 100, game.player
			for unit in game.allies:
				los = ai.los(self.loc, game.player.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:
					if len(los) <= mini:
						mini = len(los)
						enemy = unit


		melee_attacked = False

		# MAGIC!!
		if len(self.spells) > 0:

			# Chance to use spells
			if d(10) + min(self.int, 7) >= 12:

				los = ai.los(self.loc, enemy.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:

					# # Shift around spells
					# if len(self.spells) >= 2: shuffle(self.spells)

					# Zap with spells
					for spell in self.spells:

						# Can't cast These 
						if spell == 'split': break

						# Check for mana
						if self.mana >= Weapons.spells[spell][1]:
							spell_fun = Weapons.spells[spell][0]

							# If target
							if Weapons.spells[spell][4]:

								# If in spell range
								if len(los) - 1 <= Weapons.spells[spell][5]:

									# Player Resist spell
									if d(100) / 100 <= max(0.05, min(0.9, (enemy.cha / 2) / self.int)):
										self.time += Weapons.spells[spell][2]
										self.mana -= Weapons.spells[spell][1]
										game.game_log.append("You resist the " + spell + " from the " + self.name + "!")
										return

									if spell_fun(spell, self, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler):
										self.time += Weapons.spells[spell][2]
										self.mana -= Weapons.spells[spell][1]
										return
							# No target
							else:
								if spell_fun(spell, self, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler):
									self.time += Weapons.spells[spell][2]
									self.mana -= Weapons.spells[spell][1]
									return



		# Melee Attack
		if adjacent_to(self, enemy):

			# Find weapons
			weaps = [item for item in self.wielding[::-1] if type(item) == Weapon and item.wclass not in Weapons.ranged_wclasses]

			# Calc Attack Speed
			if len(weaps) != 0:
				maxas = 0
				for weapon in weaps:
					 if weapon.speed > maxas and weapon.wclass not in Weapons.ranged_wclasses: maxas = weapon.speed

			# Hit with melee
			for item in weaps:
				item.strike(self, enemy)
				if self in game.allies: game.player.well_being_statement(enemy, self, item.name, game)

			self.time += maxas
			melee_attacked = True

		# Add thrown weapon platform
		thrown = False
		if self.quivered is not None:
			if self.quivered.wclass in Ammos.thrown_amclasses:
				thrown = True
				item = self.give_weapon(self.quivered.name)

		# Make Ranged attacks
		for item in self.wielding:
			if item.wclass in Weapons.ranged_wclasses or item.wclass in Ammos.thrown_amclasses:

				if self.quivered is not None or item.hands == 0:

					if item.hands > 0 and melee_attacked:
						if thrown: self.wielding.pop()
						return

					los = ai.los(self.loc, enemy.loc, Maps.rooms[game.map.map][0], game )
					if los is not None:

						# Ranged range
						if len(los) <= (2 * item.damage  + item.to_hit):
							item.strike(self, enemy)
							if self in game.allies: game.player.well_being_statement(enemy, self, spell.name, game)

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
		if not melee_attacked:
			ai.smart_move_towards(self, enemy, game)

			# Check for Traps
			for item in game.items:
				if type(item) == Trap and item.loc == self.loc:
					item.trip()
			self.time += self.mspeed




class Weapon():

	def __init__(self,  name, rep, wclass, hands, enchantment, damage, to_hit, speed,   loc, brand = None, probability = None):

		# Initialize Weapon Stats
		self.name, self.rep, self.wclass, self.hands, self.enchantment, self.damage, self.to_hit, self.speed, self.loc, self.brand, self.probability = name, rep, wclass, hands, enchantment, damage, to_hit, speed, loc, brand, probability

		# Spell Damage
		self.mdamage = 1 if wclass in ['staff'] else 0

		# Deal with prob
		if self.probability is None: self.probability = 100

		# Ranged Brands
		if self.wclass in Weapons.ranged_wclasses: 
			self.range = 2 * damage  + to_hit
			self.brand = None
		if self.wclass in Ammos.thrown_amclasses:
			self.range = 2 * damage  + to_hit

	def details(self):

		brand = '' if self.brand is None else self.brand + ' '
		if self.enchantment >= 0: ench = '+' + str(self.enchantment)
		else: ench = str(self.enchantment)
		if self.to_hit >= 0: thit = '+' + str(self.to_hit)
		else: thit = str(self.to_hit)

		print(brand + str(ench),self.name.upper(),' (' + self.wclass + ')')
		print("")
		print("This weapon is " + str(self.hands) + "-handed.")
		print("Base damage:", str(self.damage) + ',', "Base to-hit:", thit)
		if self.wclass in Weapons.ranged_wclasses: print("Range:",self.range)
		print("Swing speed:", self.speed)
		print("")
		print(Descriptions.wclass[self.wclass][0])
		if self.wclass not in ["fists","fist"]: print("Being a " + self.wclass + ', ' + Descriptions.wclass[self.wclass][1].lower())
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def string(self):
		if self.brand is not None:
			if self.enchantment >= 0: return (self.brand + " +" + str(self.enchantment) + ' ' + self.name)
			else: return (self.brand + ' ' + str(self.enchantment) + ' ' + self.name)
		else:
			# Positive Encahntment
			if self.enchantment >= 0: return ("+" + str(self.enchantment) + ' ' + self.name)
			else: return (str(self.enchantment) + ' ' + self.name)

	def strike(self, attacker, enemy, wtypeeff = True):

		brand, wclass, to_hit = self.brand, self.wclass, self.to_hit
		ename = enemy.name if enemy.name == 'you' else "the " + enemy.name
		eposs = 'your' if enemy.name == 'you' else "the " + enemy.name + "'s"

		# Check for enemy statuses
		frozen, marked = False, False
		for passive in enemy.passives:
			if passive[0] == "frozen": frozen = True
			if passive[0] == "marked" and wclass not in ['fist','fists']: marked = True

		# Swing Probability
		if d(100) > (100 - self.probability):

			# Calc Encumberance
			self_encumb, enemy_encumb = attacker.equipped_armor.encumberance - attacker.equipped_armor.enchantment, enemy.equipped_armor.encumberance - enemy.equipped_armor.enchantment

			for item in attacker.wielding:
				if type(item) == Shield: self_encumb += item.encumberance
			for item in enemy.wielding:
				if type(item) == Shield: enemy_encumb += item.encumberance

			# Blessed Iron Passive
			for passive in attacker.passives:
				if passive[0] == "blessed iron":
					if self_encumb > 0: self_encumb = 0
					if to_hit < 0: to_hit = 0
			for passive in enemy.passives:
				if passive[0] == "blessed iron":
					if enemy_encumb > 0: enemy_encumb = 0


			# TO HIT formula
			if (d(100) + (4 * (attacker.dex - enemy.dex) ) + (2 * to_hit) + self.enchantment > 40 + 1.5 * (self_encumb - enemy_encumb)) or frozen:

				# Keep projectiles
				if self.hands > 0 and self.wclass in Weapons.ranged_wclasses or self.wclass in Ammos.thrown_amclasses:
					already_in = False
					for item in enemy.inventory:
						if type(item) == Ammo and attacker.quivered.name == item.name and attacker.quivered.brand == item.brand:
							item.number += 1
							already_in = True
							break
					# Quivereds are same lol
					if enemy.quivered is not None:
						if attacker.quivered.name == enemy.quivered.name and attacker.quivered.brand == enemy.quivered.brand:
							enemy.quivered.number += 1
							already_in = True
					if not already_in: enemy.inventory.append(Ammo(attacker.quivered.name,attacker.quivered.rep,attacker.quivered.wclass,1,attacker.quivered.damage,None,attacker.quivered.brand))

				# Shield Block

				# Dagger passive
				if wclass != 'dagger' and wclass != 'knife':
					for weapon in enemy.wielding:
						if type(weapon) == Shield:
							if d(100) > max(33, 90 - (3 * weapon.armor_rating)):

								# Block Statement
								if type(attacker) == Monster: game.game_log.append("You block the "   + str(attacker.name) + "'s " + self.name + " with your " + weapon.name + "!")
								else: game.game_log.append("The "   + str(enemy.name) +  " blocks " + attacker.info[1] + " " + self.name + " with its " + weapon.name + "!")
								return


				# DAMAGE forumla

				# Marked passive
				if marked:
					damage = int (self.damage + attacker.str + self.enchantment - ( 0.5 * enemy.calc_AC() ) )
					for passive in enemy.passives:
						if passive[0] == 'marked': enemy.passives.remove(passive)
						break

				# Projectile weapon
				elif self.wclass in Weapons.ranged_wclasses and self.hands > 0:
					damage = int (d(self.damage) + d(attacker.quivered.damage) + attacker.dex / 2 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
					brand, wclass = attacker.quivered.brand, attacker.quivered.wclass
				# Thrown Weapon
				elif self.wclass in Ammos.thrown_amclasses and self.hands > 0:
					damage = int (d(self.damage) + d(attacker.quivered.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
					brand, wclass = attacker.quivered.brand, attacker.quivered.wclass
				# Manage demon sword
				elif self.wclass in ['demon sword']:
					damage = int (d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.60 * enemy.calc_AC() ) )
				# Melee weapon
				else:
					damage = int (d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
					if enemy.equipped_armor.brand == 'spiked' and damage > 0 and d(10) > 3: barb_damage = d(int(1/2 + damage * 3/4))


				# Calc Resistances
				frostr, firer, poisonr, acidr, shockr, expr = enemy.calc_resistances()


				# Apply Brands and resistances
				if brand == "envenomed": brandhit = d(100) > 50 and d(4) > poisonr
				elif brand == "flaming": brandhit = d(100) > 60 and d(4) > firer
				elif brand == "infernal": brandhit = d(100) > 65
				elif brand == "frozen": brandhit = d(100) > 80 and d(4) > frostr
				elif brand == "antimagic": brandhit = True if len(enemy.spells) > 0 else False
				elif brand == "silvered":
					if enemy.name != 'you': brandhit = True if enemy.etype in ["undead","demon","skeleton"] else False
					else: brandhit = True if enemy.race in ["ghoul"] else False
				elif brand is not None: brandhit = True
				elif brand is None: brandhit = False

				# Apply Brands
				if not marked and damage > 0: damage = self.apply_brands(attacker, enemy, damage, brand, brandhit)

				# Weapon class effects
				if wtypeeff: damage = self.weapon_type_effect(attacker, enemy, damage)

				# Marked
				if marked:
					verb, preposition = Weapons.weapon_classes[wclass]
					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " ignites " + eposs +  " mark with its " + wclass + ", tearing " + eposs +  " body apart for " + str(damage) + " damage!")
					else: game.game_log.append("You ignite the " + enemy.name + "'s mark with your " + wclass + ", tearing its body apart for "  + str(damage) + " damage!")

				# No damage case
				elif damage <= 0:
					damage = 0

					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " hits " + ename +  " with its " + wclass + " but does no damage!")
					else: game.game_log.append("You " + Weapons.weapon_classes[wclass][0] + " your "+ str(wclass) + " " + Weapons.weapon_classes[wclass][1] + " the " + enemy.name + " but deal no damage!")

				# Damage Case - Statement
				else: self.damage_statement(attacker, enemy, damage, brand, brandhit, ename, eposs)
						
				# Resolve Damage
				enemy.hp -= damage

				# Manage Spiked
				try:
					attacker.hp -= barb_damage
					game.game_log.append(enemy.info[1][0].upper() + enemy.info[1][1:] + ' spikes deal ' + str(barb_damage) + ' damage back to ' + attacker.info[0] + '!')

					# Check if unit is still alive
					if attacker.hp <= 0 and type(attacker) != Player:
						game.game_log.append("The " + attacker.name + " dies from the spikes!")
						game.units.remove(attacker)
						if attacker in game.allies: game.allies.remove(attacker)

						# Ooze Passive
						if 'split' in enemy.spells: Weapons.spells["split"][0]("split", enemy, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler)

						# Drop Loot
						attacker.drop_booty()

						# XP Gain
						game.player.xp += attacker.xp + int(d(game.player.cha) / 2)
				except: pass

			# Miss Case
			else:

				# Manage blades
				counter = None
				for weapon in enemy.wielding:
					if type(weapon) == Weapon:
						if weapon.wclass in ["sword","bastard sword","demon sword","god sword"] and self.wclass not in Weapons.ranged_wclasses: 

							# Counter chance
							if d(100) + 3 * enemy.dex > 75: counter = weapon

				# Miss statement
				if self.wclass in Weapons.ranged_wclasses:
					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " shoots at " + ename +  " with its " + self.wclass + " but misses.")
					else: game.game_log.append("You closely miss the " + str(enemy.name) + " with your " + self.wclass + "!")
				elif self.wclass in Ammos.thrown_amclasses:
					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " hurls a " + self.wclass + " at " + ename +  " but misses.")
					else: game.game_log.append("You closely miss the " + str(enemy.name) + " with your " + self.wclass + "!")
				else:
					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " swings at " + ename +  " with its " + self.wclass + " but misses.")
					else: game.game_log.append("You closely miss the " + str(enemy.name) + " with your " + self.wclass + "!")

				# Riposte with blade
				if counter is not None:
					damage = int (d(int(counter.damage * 0.75)) + attacker.str / 1.5 + counter.enchantment - ( 0.75 * attacker.calc_AC() ) )
					if damage > 0:
						aname = 'you' if type(attacker) == Player else ('the ' + attacker.name)
						if type(enemy) == Player: game.game_log.append("You counter the " + str(attacker.name) + " with your blade for " + str(damage) + " damage!")
						else: game.game_log.append("The "  + str(enemy.name) + " counters " + aname +  " with its blade for " + str(damage) + " damage!")

						attacker.hp -= damage
						if enemy.name == 'you': game.player.well_being_statement(attacker, game.player, counter.name, game)


	def weapon_type_effect(self, attacker, enemy, damage):


		# Blunt weapons
		if self.wclass in ["hammer","club" ,"mace","flail"]:
			if enemy.equipped_armor.aclass == 'plate': damage *= 1.4

		if self.wclass in ["warhammer","greatclub","god hammer","fists"]:
			if enemy.equipped_armor.aclass == 'plate': damage *= 1.4

			# Stun
			if d(100) >= 65:
				for passive in enemy.passives:

					if passive[0] == "stunned":
						passive[1] = 1
						return damage

				enemy.passives.append(["stunned", 1])

		if self.wclass in ["greatsword","god sword","bastard sword"]:

			# CLEAVE Attack
			# --START--------------------------------
			y = attacker.loc[0] - enemy.loc[0]
			x = attacker.loc[1] - enemy.loc[1]

			for unit in game.units:
				cleave = False

				# Horizontal Case
				if x == 0:
					if unit.loc == (enemy.loc[0], enemy.loc[1] + 1):
						self.strike(attacker, unit, False)
						cleave = True
					if unit.loc == (enemy.loc[0], enemy.loc[1] - 1):
						self.strike(attacker, unit, False)
						cleave = True

				# Vertical Case
				elif y == 0:
					if unit.loc == (enemy.loc[0] + 1, enemy.loc[1]):
						self.strike(attacker, unit, False)
						cleave = True
					if unit.loc == (enemy.loc[0] - 1, enemy.loc[1]):
						self.strike(attacker, unit, False)
						cleave = True

				# Corner case
				else:
					if unit.loc == (enemy.loc[0] + y, enemy.loc[1]):
						self.strike(attacker, unit, False)
						cleave = True
					if unit.loc == (enemy.loc[0], enemy.loc[1] + x):
						self.strike(attacker, unit, False)
						cleave = True

				if not cleave and self.wclass != 'bastard sword' and unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])): self.strike(attacker, unit, False)
			# --END------------------------------------


		if self.wclass in ["spear","polearm","lance"]:
			for unit in game.units:
				if unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, False)
					break

		if self.wclass in ["pike","god spear"]:
			for unit in game.units:
				if unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, False)
				if unit.loc == (attacker.loc[0] - 3 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 3 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, False)

		if self.wclass in ["axe"]:
			damage *= (1 + max(0, (0.25 - enemy.calc_AC() / 50 )) )

		if self.wclass in ["greataxe","god axe"]:
			damage *= (1 + max(0, (0.25 - enemy.calc_AC() / 50 )) )

 			# CLEAVE Attack
			# --START--------------------------------
			y = attacker.loc[0] - enemy.loc[0]
			x = attacker.loc[1] - enemy.loc[1]

			for unit in game.units:

				# Horizontal Case
				if x == 0:
					if unit.loc == (enemy.loc[0], enemy.loc[1] + 1): self.strike(attacker, unit, False)
					if unit.loc == (enemy.loc[0], enemy.loc[1] - 1): self.strike(attacker, unit, False)

				# Vertical Case
				elif y == 0:
					if unit.loc == (enemy.loc[0] + 1, enemy.loc[1]): self.strike(attacker, unit, False)
					if unit.loc == (enemy.loc[0] - 1, enemy.loc[1]): self.strike(attacker, unit, False)

				# Corner case
				else:
					if unit.loc == (enemy.loc[0] + y, enemy.loc[1]): self.strike(attacker, unit, False)
					if unit.loc == (enemy.loc[0], enemy.loc[1] + x): self.strike(attacker, unit, False)
			# --END------------------------------------


		return int(damage)


	def apply_brands(self, attacker, enemy, damage, brand, brandhit):


		# APPLY BRANDS
		if brandhit:

			# Manage Flaming
			if brand == "flaming":

				for passive in enemy.passives:
					
					if passive[0] == "aflame": return damage

				enemy.passives.append(["aflame", Brands.dict["flaming"]["count"]])

			# Manage Infernal
			if brand == "infernal":

				for passive in enemy.passives:
					
					if passive[0] == "drained":
						passive[1] = Brands.dict["drained"]["count"]
						return damage

				enemy.passives.append(["drained", Brands.dict["drained"]["count"]])
				enemy.dex -= Brands.dict["drained"]["dex_loss"]

			# Manage Vampiric
			if brand == "vampiric":

				# heal
				attacker.hp = min(attacker.maxhp, attacker.hp + int(damage / 3))

			# Manage Hellfire
			if brand == "hellfire":
				damage += int((1 - (enemy.hp / enemy.maxhp) ) * damage * 0.5)

			# Manage Envenomed
			if brand == "envenomed":

				for passive in enemy.passives:

					if passive[0] == "poisoned":
						passive[1] += Brands.dict["envenomed"]["count"]
						return damage

				enemy.passives.append(["poisoned", Brands.dict["envenomed"]["count"]])

			# Manage Silvered
			if brand == "silvered":
				damage *= 1.5

			# Manage Antimagic
			if brand == "antimagic":
				damage *= 1.5

			# Manage Frozen=
			if brand == "frozen":

				for passive in enemy.passives:

					if passive[0] == "frozen":
						passive[1] += Brands.dict["frozen"]["count"]
						return damage

				enemy.passives.append(["frozen", Brands.dict["frozen"]["count"]])

		# Return DAMAGE
		return damage


	def damage_statement(self, attacker, enemy,  damage, brand, brandhit, ename, eposs):
		attacker_var, attackee_var =  str(attacker.name), str(enemy.name)
		name, wclass = self.name, self.wclass

		if self.wclass in Weapons.ranged_wclasses and self.hands > 0:
			name, wclass = attacker.quivered.name, attacker.quivered.wclass

		# Make the sentence awesome
		verb, preposition = Weapons.weapon_classes[wclass]

		# Make the notes dank
		if brand is None or not brandhit:
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its " +  name + "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var + " for " + str(damage) + " damage!")

		elif brand == "silvered":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its "  + name + ", its silver burns " + ename +  "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var+ ", the silver burns for " + str(damage) + " damage!")

		elif brand == "antimagic":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its "  + name + ", your magic burns inside " + ename +  "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var+ ", tearing the mage apart for " + str(damage) + " damage!")

		elif brand == "vampiric":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its "  + name + " and steals " + eposs +  " life!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var+ ", dealing " + str(damage) + " damage and draining its life!")

		elif brand == "flaming":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its " + name + " and sets " + ename +  " aflame!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and setting it aflame!")

		elif brand == "infernal":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its " + name + " and saps " + eposs +  " soul!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and sapping its soul!")

		elif brand == "frozen":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its " + name + " and freezes " + ename +  "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and freezing it!")

		elif brand == "hellfire":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its " + name + " and sets " + eposs +  " soul aflame!")
			else:
				game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and tearing its soul!")

		elif brand == "envenomed":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits " + ename +  " for " + str(damage) + " damage with its " + name + " and poisons " + ename +  "!")
			else:
				game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and poisoning it!")


class Armor():

	def __init__(self, name, rep,  aclass, armor_rating, encumberance, enchantment, loc, brand = None):
		self.name, self.rep, self.aclass, self.armor_rating, self.encumberance, self.enchantment, self.loc, self.brand = name, rep, aclass, armor_rating, encumberance, enchantment, loc, brand

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = 0, 0, 0, 0, 0, 0

		# Manage Icy, Tempered
		if self.brand == 'tempered':
			self.firer += 3
		if self.brand == 'icy':
			self.frostr += 3

		if aclass == 'garments':
			self.mdefense = 0
		elif aclass == 'robes':
			self.mdefense = 3
		elif aclass == 'hide':
			self.mdefense = 2
		elif aclass == 'scale':
			self.mdefense = 1
		elif aclass == 'chainmail':
			self.mdefense = 1
		elif aclass == 'plate':
			self.mdefense = 1

	def details(self):

		brand = '' if self.brand is None else self.brand + ' '
		if self.enchantment >= 0: ench = '+' + str(self.enchantment)
		else: ench = str(self.enchantment)
		if self.encumberance > 0: encum = '-' + str(self.encumberance)
		else: encum = '+' + str(abs(self.encumberance))

		print(brand + str(ench),self.name.upper(),' (' + self.aclass + ')')
		print("")
		print("Base armor rating:", str(self.armor_rating) + ',', "Base encumberance:", encum)
		print("")
		print(Descriptions.wclass[self.aclass])
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def string(self):
		if self.brand is not None:
			if self.enchantment >= 0: return (self.brand + " +" + str(self.enchantment) + ' ' + self.name)
			else: return (self.brand + ' ' + str(self.enchantment) + ' ' + self.name)
		else:
			# Positive Encahntment
			if self.enchantment >= 0: return ("+" + str(self.enchantment) + ' ' + self.name)
			else: return (str(self.enchantment) + ' ' + self.name)

class Shield():

	def __init__(self, name, rep, hands, armor_rating, encumberance, enchantment, loc, brand = None):
		self.name, self.rep, self.hands, self.armor_rating, self.encumberance, self.enchantment, self.loc, self.brand = name, rep, hands, armor_rating, encumberance, enchantment, loc, brand
		self.wclass = "shield"

		# Magic Damage
		self.mdamage = 0

	def details(self):

		brand = '' if self.brand is None else self.brand + ' '
		if self.enchantment >= 0: ench = '+' + str(self.enchantment)
		else: ench = str(self.enchantment)
		if self.encumberance >= 0: encum = '-' + str(self.encumberance)
		else: encum = '+' + str(abs(self.encumberance))

		print(brand + str(ench),self.name.upper())
		print("")
		print("This shield is " + str(self.hands) + "-handed.")
		print("Base armor rating:", str(self.armor_rating) + ',', "Base encumberance:", encum)
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def string(self):
		if self.brand is not None:
			if self.enchantment >= 0: return (self.brand + " +" + str(self.enchantment) + ' ' + self.name)
			else: return (self.brand + ' ' + str(self.enchantment) + ' ' + self.name)
		else:
			# Positive Encahntment
			if self.enchantment >= 0: return ("+" + str(self.enchantment) + ' ' + self.name)
			else: return (str(self.enchantment) + ' ' + self.name)

class Ammo():

	def __init__(self, name, rep, wclass, number, damage, loc, brand = None):
		self.name, self.rep, self.wclass, self.damage, self.number, self.loc, self.brand = name, rep, wclass, damage, number, loc, brand

	def details(self):
		brand = '' if self.brand is None else self.brand + ' '

		print(brand + self.name.upper(),' (' + self.wclass + ')')
		print("")
		if self.wclass in Ammos.thrown_amclasses: 
			data = Weapons.array[self.name]
			weap = Weapon(self.name, data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, None, None)
			print("Base damage:",self.damage + weap.damage)
			print("Range:",weap.range)
		else:
			print("Base damage:",self.damage)
		print("You are carrying " + str(self.number) + ".")
		print("")
		print(Descriptions.wclass[self.wclass])
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def string(self):
		if self.brand is not None: return(self.brand + ' ' + self.name + ' (' + str(self.number) + ')')
		else: return (self.name + ' (' + str(self.number) + ')')

class Trap():

	def __init__(self, damage, type, loc):
		self.damage, self.type, self.loc, self.rep = damage, type, loc,'*'

	def trip(self):
		if self.type == 'mine':
			# Blast Radius
			spaces, affected = set([]), []
			for x in range(-1,2):
				for y in range(-1,2):
					if self.loc[0] + x >= 0 and self.loc[1] + y >= 0: spaces.add((self.loc[0] + x, self.loc[1] + y))
			# Find units affected
			for unit in game.units:
				if unit.loc in spaces:
					if unit.loc == self.loc: triggerer = self.loc
					affected.append(unit)
			# Hit string
			hit = ""
			for unit in affected:

				# Shock Resist
				resist = enemy.calc_resistances()[5]
				if d(4) <= resist:
					if unit.name == 'you':
						game.game_log.append("You shrug off the mine's explosion!")
					else:
						game.game_log.append("The " + unit.name + " shrugs off the mine's explosion!")
					continue

				unit.hp -= self.damage
				if unit.name == 'you':
					if len(hit) == 0: hit += "you"
					else: hit += ", you"
				else:
					if len(hit) == 0: hit += "the " + unit.name
					else: hit += ", the " + unit.name
			try:
				game.game_log.append("The " + triggerer.name + " sets off the mine, dealing " + str(self.damage) + " damage to " + hit + '!')
			except:
				game.game_log.append("The mine explodes, dealing " + str(self.damage) + " damage to " + hit + '!')

		game.items.remove(self)

class Chest():

	def __init__(self, type, tier,  loc):
		self.tier, self.type, self.loc = tier, type, loc

		# Initialize Rep
		self.rep = '='
		self.opened = False

		# Chest contents
		if self.type == "golden":
			self.pot_weapons = [ ["steel longsword","hooked longsword","skull smasha","bearded axe"],
								 ["gorktooth choppa","ranger longbow"],
								 ["claymore","khopesh","gorkjaw choppa","executioner axe","dwarven "],
								 ["witchhunter blade","glaive","dwarven crossbow"], 	]
		
		elif self.type == "elven":
			self.pot_weapons = [ ["elven wooddagger","elven leafblade"],
								 ["elfrobe"],
								 ["elven leafblade","winged javelin"],
								 ["elven broadspear","elven longbow"],
								 ["elven longstaff"], 	]
		elif self.type == "dark elven":
			self.pot_weapons = [ ["thornblade","thornknife"],
								 ["thornarrow"],
								 ["blackwood longbow","ironscale mail"],
								 ["sun spear","sunlance"], 	]
		elif self.type == "wooden":
			self.pot_weapons = [["steel dagger","iron axe","spear","hammer","mace","iron longsword","club","iron shortsword"], 
								["crude shortbow","iron battleaxe","iron longsword","mace","flail","quarterstaff","iron bastard sword"], 
								["buckler shield", "wooden broadshield","trollhide shield","recurve bow"], 
								["iron battleaxe","iron greatsword","warhammer","spiked club","barbed javelin","longbow"],
								["iron plate armor","iron chainmail","ironscale mail","scrap plate armor"],
								["steel axe","steel longsword","halberd","steel bastard sword","steel shortsword"],
								["steel greatsword","steel battleaxe","pike","greatflail","ranger longbow"] ]
		elif self.type == "orcish":
			self.pot_weapons = [ ["goblin spear","stabba","choppa"],
								 ["bear hide","ogre hide"],
								 ["choppa","slica","smasha"],
								 ["goblin bow","crude shortbow"], 
								 ["big choppa","big slica","skull smasha"], 
								 ["scrap plate armor","berserker mail","troll hide"], 
								 ["toxic slica"],
								 ["ice choppa","boss choppa"], 	]

		self.pot_ammo = ["iron arrow","iron bolt","iron javelin","steel arrow","steel bolt","thornarrow"]

	def open(self):

		# Legendary Chance
		if d(100) + self.tier > 100:
			try:
				legendary = Weapons.legendary_weapons[ d(len(Weapons.legendary_weapons)) - 1]
				game.map.room_filler.place_weapon(legendary, self.loc, int((d(self.tier) - 1) / 2))
				Weapons.legendary_weapons.remove(legendary)
			except: pass

		else:

			# Place Weapons/Armor/Shield
			for i in range(1, int(game.player.level / 2) + 2):
				if len(self.pot_weapons) == 0: return

				# Calculate Tier
				tier = self.pot_weapons[min( i - 1, len(self.pot_weapons) - 1 )] # player level / Specifies not to overshoot
				item_name = tier [ d( len(tier)) - 1]

				# Chance to get item
				if d(100) / 100 <= i / int(game.player.level) / 2 + 1:

					# If Ammo
					if item_name in Ammos.array:

						# Chance for brand
						brand = None
						brand = Brands.ammo_brands[d(len(Brands.ammo_brands)) - 1] if d(100) + self.tier > 97 else None
						game.map.room_filler.place_ammo(item_name, self.loc, 5 + 4 * self.tier, brand)

					# If weapon
					elif item_name in Weapons.array:

						# Chance for brand
						brand = None
						if Weapons.array[item_name][2] > 0:
							if d(100) + self.tier > 97: brand = Brands.weapon_brands[d(len(Brands.weapon_brands)) - 1]
						game.map.room_filler.place_weapon(item_name, self.loc, int((d(self.tier) - 1) / 2), brand)

					# If Armor
					elif item_name in Armors.array:

						# Chance for brand
						brand = Brands.armor_brands[d(len(Brands.armor_brands)) - 1] if d(100) + self.tier > 97 else None
						game.map.room_filler.place_armor(item_name, self.loc, int((d(self.tier) - 1) / 2), brand)

					#If Shield
					elif item_name in Shields.array:
						game.map.room_filler.place_shield(item_name, self.loc, int((d(self.tier) - 1) / 2))

					# self.pot_weapons.remove(tier)

		# Place Ammo
		if d(10) + d(self.tier) > 6:

			# Chance for brand
			brand = None
			if d(100) + 2 * i > 96: brand = Brands.ammo_brands[d(len(Brands.ammo_brands)) - 1]

			ammo = self.pot_ammo[min(len(self.pot_ammo) - 1, d(self.tier) - 1)]
			if ammo in Weapons.array: number = 2 * self.tier
			else: number = 5 + self.tier
			game.map.room_filler.place_ammo(ammo, self.loc, number, brand)
		self.opened = True





class Map():

	def __init__(self, player, room):

		self.map, self.player = room, player

		self.def_map_array = Maps.rooms[self.map][0]
		self.map_array = deepcopy(self.def_map_array)

		self.entry_point, self.exits = Maps.rooms[self.map][2], Maps.rooms[self.map][3]


		self.adjacent = {self.entry_point: None}
		for point in self.exits[1:]: self.adjacent[point] = None

		self.objects, self.allies = [], []

		self.filled = False


	def fill(self):
		self.room_filler = RoomFiller(self.player.level, (15,2), self.map)
		self.room_filler.place()

	def parse(self,line):

		# Parse for display
		art = ""
		for char in line: art += char
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
		for line in self.map_array: print("        " + self.parse(line))

	def change_room(self, new_room):

		room, newloc = new_room[0], new_room[1]

		# Store units
		for unit in game.units[1:]:
			if type(unit) == Monster:
				self.objects.append(unit)
			if unit in game.allies: self.allies.append(unit)

		for item in game.items: self.objects.append(item)

		# Clear units
		game.units, game.allies, game.items = [game.player], [], []

		# Add old room's units
		for object in room.objects:
			game.units.append(object) if type(object) == Monster else game.items.append(object)
			if object in room.allies: game.allies.append(object)

		game.map = room

		# Place boyo on map
		if newloc == Maps.rooms[room.map][2]:
			self.player.loc = (newloc[0] + 1, newloc[1])
		else:
			self.player.loc = (newloc[0] - 1, newloc[1])



	def new_room(self, coords):

		# Store units
		for unit in game.units[1:]:
			if type(unit) == Monster: self.objects.append(unit)
			if unit in game.allies: self.allies.append(unit)

		for item in game.items: self.objects.append(item)

		# Clear units
		game.units, game.allies, game.items = [game.player], [], []

		# Make new Map
		pot_maps = Maps.sizes[Maps.rooms[self.map][3][0][d(len(Maps.rooms[self.map][3][0])) - 1]]
		newmap = Map(self.player,pot_maps[ d(len(pot_maps)) - 1])
		game.map = newmap

		# Entry Point
		self.adjacent[coords] = (newmap, newmap.entry_point)
		newmap.adjacent[newmap.entry_point] = (self, coords)
		self.player.loc = (newmap.entry_point[0] + 1, newmap.entry_point[1])

		game.game_log.append("You enter the room...")


	def square_identity(self, coord):
		y,x = coord
		return self.def_map_array[x][y]

	def can_move(self, loc, leap = False):
		unallowed = ['|', '-', ' ', '#','_']
		if leap: unallowed.append('@') 
		units = game.units
		try: self.square_identity(loc)
		except: return False
		if self.square_identity(loc) in unallowed:
			print("False")
			return False
		if leap: units = game.units[1:]
		for unit in units:
			if loc == unit.loc:
				return False
		return True



class RoomFiller():

	def __init__(self, tier, pos, map):
		self.tier, self.pos, self.map = tier, pos, map

	def place_trap(self, damage, type, loc):
		game.items.append(Trap(damage,type,loc))

	def place(self):

		# Fill if specified by map
		if Maps.rooms[self.map][4]: self.fill()

		# Place Chests
		for loc, chance in Maps.rooms[self.map][1]:

			# Pick Chest Type
			roll = d(100)
			if roll + 2*self.tier > 106: type = "golden"
			elif roll + 2*self.tier > 103: type = "elven"
			elif roll + 2*self.tier > 97: type = "dark elven"
			elif roll + 2*self.tier > 20: type = "wooden"
			else: type = "orcish"

			if d(100) <= chance: self.place_chest(type, game.player.level, loc)

	def fill(self):

		# Tier and Band pick
		etier = min(self.tier, len(Bands.dicto))
		tier_group = Bands.dicto[ etier ]
		band = tier_group[d(len(tier_group)) -1]

		# Bonuses and actual bands
		bonus, groups = Bands.formations[band]

		# Cut off some units
		squad = groups[:self.tier + bonus]
		spawned = set([])
		for i in range( len(squad)):

			group = groups[i]

			# Choose which units to spawn
			if len(group) > 0:

				unit = min(len(group) - 1, max( 0, d(etier) - i - bonus))
				# unit = min(len(group) - 1, d(self.tier)  - min(groups.index(group), bonus + etier) - 1)

				picked = False
				while not picked:

					# Pick spawn location
					try: spawn_location = (d(int(len(Maps.rooms[self.map][0][0]))) - 1, d(len(Maps.rooms[self.map][0])) - 1)
					except: spawn_location = (d(len(Maps.rooms[self.map][0][0])) - 1, d(len(Maps.rooms[self.map][0])) - 1)

					try:
						forbidden, fsquares = Maps.rooms[self.map][5], set([])
						for i in range(-forbidden[1], forbidden[1] + 1):
							for j in range(-forbidden[1], forbidden[1] + 1): fsquares.add((i + forbidden[0][0],j + forbidden[0][1]))
						if spawn_location in fsquares: continue
					except: pass

					if game.map.square_identity(spawn_location) not in ['|', '-', ' ', '#','+','@','_'] and spawn_location != game.player.loc and spawn_location not in spawned:
						picked = True
						prev_loc = spawn_location
						spawned.add(prev_loc)


				self.spawn(group[unit] , spawn_location)

	def spawn(self, monster_name, loc, ally = False):
		data = Monsters.array[monster_name]
		try: other_items = data[13]
		except: other_items = None

		# Spawn Unit
		unit = Monster(monster_name, data[0],data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], loc, other_items)
		game.units.append(unit)
		if ally: game.allies.append(unit)

	def place_weapon(self, weapon, loc, enchantment = 0, brand = None):
		data = Weapons.array[weapon]

		# Manage Enchantment + Brand
		spawned_enchantment = data[3] + enchantment
		try: brand = data[7]
		except: pass

		# Create Weapon Object
		game.items.append(Weapon(weapon, data[0], data[1], data[2], spawned_enchantment, data[4], data[5], data[6], loc, brand))

	def place_armor(self, armor, loc, enchantment = 0, brand = None):
		data = Armors.array[armor]

		# Manage Enchantment + Brand
		spawned_enchantment = data[4] + enchantment
		try: brand = data[5]
		except: pass

		# Create Armor Object
		game.items.append(Armor(armor, data[0], data[1], data[2], data[3], data[4], loc, brand))

	def place_shield(self, armor, loc, enchantment = 0, brand = None):
		data = Shields.array[armor]

		# Manage Enchantment
		spawned_enchantment = data[4] + enchantment
		try: brand = data[5]
		except: pass

		#Create Shield Object
		game.items.append(Shield(armor, data[0], data[1], data[2], data[3], data[4], loc, brand))

	def place_ammo(self, ammo, loc, number, brand = None):
		data = Ammos.array[ammo]

		# Manage Enchantment
		try: brand = data[3]
		except: pass

		#Create Shield Object
		game.items.append(Ammo(ammo, data[0], data[1], number, data[2], loc, brand))

	def place_chest(self, type, tier, loc):
		game.items.append(Chest(type, tier, loc))










class Game():

	def __init__(self):
		# Manage Constants

		# CHANGE RACE
		self.race = "Dragonborn"
		self.pclass = "Warrior"

		self.player = Player(CharacterInfo.races[self.race][0], CharacterInfo.races[self.race][1], self)
		self.map = Map(self.player, 'starting_room')
		self.state = 'ongoing'
		self.room = 0

		# Initiate Regen
		self.hregen, self.mregen, self.prev_valid_turn = 0, 0, True

		# Manage Units
		self.units, self.allies, self.items, self.seen = [self.player], [], [], set([])

		# Manage Game Log
		self.game_log, self.temp_log = [], []

		# item order
		self.item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


	def run(self):
		while self.state == 'ongoing':

			if not self.map.filled:
				self.map.fill()
				self.map.filled = True

			#  Turn Finder
			min_time = self.player.time
			indeces = []
			for i in range(len(game.units)):
				unit = game.units[i]
				if unit.time < min_time:
					indeces = [i]
					min_time = unit.time
				elif unit.time == min_time: indeces.append(i)

			if self.player.time == 0 and min_time == 0: self.prev_valid_turn = False
			else: self.prev_valid_turn = True

			for index in indeces:
				try: tunit = game.units[index]
				except: continue

				if self.prev_valid_turn: self.check_passives(tunit)
				if tunit.time != min_time: continue

				if type(tunit) == Monster:
					if tunit.hp > 0: tunit.turn()
				elif type(tunit) == Player: self.player_turn(self.map)

			for unit in game.units: unit.time -= min_time



	def player_turn(self, map):


		def action(move):
			x, y = self.player.loc[0], self.player.loc[1]



			# Base Case
			if move in ['h','H','j','J','k','K','l','L','y','Y','u','U','b','B','n','N',',','.','w','W','f','r','s','S','a','q','i','+']:

				# Attack Move (1 turn)
				if move == 'l': self.player.atk_mv(map, (x + 1, y))
				elif move == 'k': self.player.atk_mv(map, (x, y - 1))
				elif move == 'j': self.player.atk_mv(map, (x, y + 1))
				elif move == 'h': self.player.atk_mv(map, (x - 1, y))
				elif move == 'y': self.player.atk_mv(map, (x - 1, y - 1))
				elif move == 'u': self.player.atk_mv(map, (x + 1, y - 1))
				elif move == 'b': self.player.atk_mv(map, (x - 1, y + 1))
				elif move == 'n': self.player.atk_mv(map, (x + 1, y + 1))

				# GOD MODE
				elif move == '+':
					self.player.innate_ac += 200
					game.game_log.append("You're no fun")
					self.player.equipped_armor.mdefense += 200



				# Run Right
				elif move == 'L':
					if len(game.units) == len(game.allies) + 1:
						while map.can_move((self.player.loc[0] + 1, self.player.loc[1])):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1])) != '+':
								action('l')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Up
				elif move == 'K':
					if len(game.units) == len(game.allies) + 1:
						while map.can_move((self.player.loc[0], self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0], self.player.loc[1] - 1)) != '+':
								action('k')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Down
				elif move == 'J':
					if len(game.units) == len(game.allies) + 1:
						while map.can_move((self.player.loc[0], self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0], self.player.loc[1] + 1)) != '+':
								action('j')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Left
				elif move == 'H':
					if len(game.units) == len(game.allies) + 1:
						while map.can_move((self.player.loc[0] - 1, self.player.loc[1])):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1])) != '+':
								action('h')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run UL
				elif move == 'Y':
					if len(game.units) == len(game.allies) + 1:
						while map.can_move((self.player.loc[0] - 1, self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1] - 1)) != '+':
								action('y')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run UR
				elif move == 'U':
					if len(game.units) == len(game.allies) + 1:
						while map.can_move((self.player.loc[0] + 1, self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1] - 1)) != '+':
								action('u')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run DL
				elif move == 'B':
					if len(game.units) == len(game.allies) + 1:
						while map.can_move((self.player.loc[0] - 1, self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1] + 1)) != '+':
								action('b')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run DR
				elif move == 'N':
					if len(game.units) == len(game.allies) + 1:
						while map.can_move((self.player.loc[0] + 1, self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1] + 1)) != '+':
								action('n')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")

				# quiver
				elif move == 'q': self.player.quiver()
				# fire
				elif move == 'f': self.player.fire()
				# spell
				elif move == 's': 
					if len(self.player.spells) > 0: self.player.cast("spell",self.player.spells)
					else:
						game.temp_log.append("You do not know any spells.")
				# ability
				elif move == 'a': 
					if len(self.player.abilities) > 0: self.player.cast("ability",self.player.abilities)
					else:
						if len(self.player.cooldowns) > 0: game.temp_log.append("All your abilites are on cooldown.")
						else: game.temp_log.append("You don't have any abilities.")
				# wield
				elif move == 'w':
					self.player.wield(Weapon)
				# Wear
				elif move == 'W':
					self.player.wield(Armor)
				# Stash
				elif move == "S":
					self.player.stash()
				# inventory
				elif move == "i":
					self.player.inventoryize()
				# Investigate
				elif move == ',':
					self.investigate()
				# Wait
				elif move == '.':
					self.player.time += self.player.mspeed
					self.check_passives(self.player)
				# rest
				elif move == 'r':
					if len(game.units) == len(game.allies) + 1:
						while self.player.hp < self.player.maxhp or self.player.mana < self.player.maxmana: action('.')
						game.temp_log.append("You feel well-rested")
						self.player.time = 0
					else:
						game.temp_log.append("There are enemies nearby!")

			else: game.temp_log.append("Invalid Move")









		# Manage Game Log
		self.game_log.append("                                                                     ")

		log_select = self.game_log[((len(Maps.rooms[game.map.map][0]) - 26) + len(self.temp_log)):]
		print("=======================================================================================")
		print("                                                                     ")

		# Display Game Log
		for line in log_select: print(line)
		for line in self.temp_log: print(line)

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

		# Carrying
		carrying = [weap for weap in self.player.wielding if weap.hands != 0]

		for item in self.player.wielding:
			if item.hands != 0:

				# Hand String Formulation
				hands = item.hands

				# Hill Troll Passive
				if self.player.race == "Hill Troll":
					if item.hands >= 3: hands = 2
					elif item.hands == 2: hands = 1

				weapon_string += ' ' + item.string() + " (" + str(hands) + "h)"

		# Wielding Nothing
		if weapon_string == "": weapon_string = " None"

		# Quiver String
		if self.player.quivered is None: quivered_string = " None"
		else:
			if self.player.quivered.brand is None: quivered_string = " " + self.player.quivered.name + " (" + str(self.player.quivered.number) + ")"
			else: quivered_string = " " + self.player.quivered.brand + ' ' + self.player.quivered.name + " (" + str(self.player.quivered.number) + ")"

		hpspace =   "              "
		for i in range(len(str(self.player.hp)) + len(str(self.player.maxhp))): hpspace = hpspace[:-1]

		manaspace = "              "
		for i in range(len(str(self.player.mana)) + len(str(self.player.maxmana))): manaspace = manaspace[:-1]




		# Check for indominable!
		if self.player.hp <= 0:
			for name, count in self.player.passives:
				if name == 'indominable':
					game.game_log.append("You refuse to die!")
					self.player.hp = 1


		print("Level " + str(self.player.level) + " " + self.player.race + " " + self.player.pclass)
		print("HP    " + str(self.player.hp)   + "/" + str(self.player.maxhp)   + hpspace + "Wielding:" + weapon_string + "         Armor: " + self.player.equipped_armor.string())
		print("MANA  " + str(self.player.mana) + "/" + str(self.player.maxmana) + manaspace + "Quivered:" + quivered_string)

		# YOU DIE!!
		if self.player.hp <= 0:
			print("You have been slain!")
			print("You suck at this game bruh")
			self.state = "defeat"
			return


		# See Monster
		for unit in self.units[1:]:
			if unit not in self.seen:

				wielding = ""
				for item in unit.wielding[::-1]:
					if wielding == "" and item.hands > 0: wielding += item.name
					elif item.hands > 0: wielding += (", a " + item.name)

				if len(wielding) == 0: game.game_log.append("You see a " + unit.name + ", wearing " + unit.equipped_armor.name)
				else: game.game_log.append("You see a " + unit.name + ", wearing " + unit.equipped_armor.name + ", wielding a " + wielding)
				self.seen.add(unit)

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

		action(move)
		print(move)

		# Reset the terminal
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
		return
	

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

		# Nothing to interact with
		if len(drops) == 0:
			self.temp_log.append("There is nothing here to interact with.")

		# One item on the ground
		elif len(drops) == 1 and not opened_a_chest:
			self.player.pick_up(drops[0])

		# Multiple ground items
		else:
			self.ground_inventory(drops, opened_a_chest)

				

	def ground_inventory(self, drops, chest):

		spaces = [i for i in range(27 - (len(drops)))]

		pickups = set([])


		leave = False
		while not leave:

			print("=======================================================================================")
			for space in spaces: print('')

			if chest: print("You find in the chest:")
			else: print("You find on the floor:")
			print("")
			print("=======================================================================================")
			print("                                                                     ")
			for i in range(len(drops)):
				sign = " - " if drops[i] not in pickups else " + "
				print(game.item_order[i] + sign + drops[i].string())
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


			print("")
			print("Pick up which items? (enter spacebar to accept, a number to cancel)")
			inp, outp, err = select.select([sys.stdin], [], [])
			decision = sys.stdin.read()

			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

			if decision in ['1','2','3','4','5','6','7','8','9']:
				leave = True
				return
			elif decision in game.item_order:
				if game.item_order.index(decision) < len(drops):

					if drops[game.item_order.index(decision)] in pickups:
						# Legal item drop
						pickups.remove(drops[game.item_order.index(decision)])
					else:
						# Legal item pickup
						pickups.add(drops[game.item_order.index(decision)])
					
			elif decision == ' ':
				for item in pickups:
					self.player.pick_up(item)
				leave = True
				return




	def check_passives(self, unit, purge = False):

		if type(unit) == Player and not purge:
			# Reduce Cooldowns
			#------------------

			# Reduce
			for tuplee in self.player.cooldowns:
				tuplee[1] -= 1

				# Add back
				if tuplee[1] == 0:
					self.player.abilities.append(tuplee[0])
					self.game_log.append("You can use your " + str(tuplee[0] + " again!"))
					self.player.cooldowns.remove(tuplee)

			# Regen Health
			if self.player.hp < self.player.maxhp:

				# Increment Counter
				self.hregen += 1

				# Regen one health
				if self.hregen >= (self.player.reg  -  1/3  * self.player.con):

					self.player.hp += 1
					self.hregen = 0

			# Regen Mana
			if self.player.mana < self.player.maxmana:

				# Increment Counter
				self.mregen += 1

				# Regen one health
				if self.mregen >= (14 - self.player.int):

					self.player.mana += 1
					self.mregen = 0


		for passive in unit.passives:

			name = passive[0]
			count = passive[1]



			# Decrement Count
			passive[1] -= 1
			if passive[1] <= 0 or purge:

				# Manage drained
				if name == "drained": unit.dex += Brands.dict["drained"]["dex_loss"]

				# Manage Indominable
				if name == "indominable":
					if unit.name == 'you': game.game_log.append("You can now enter Valhalla in peace.")
					else: game.game_log.append("The " + unit.name + " can now enter Valhalla in peace.")

				# Manage Iron Blessing
				if name == "blessed iron":
					if unit.name == 'you': game.game_log.append("Your iron blessing wears off.")
					else: game.game_log.append("The " + unit.name + "'s iron blessing wears off.")

				# Manage grotesque
				if name == "grotesque":
					unit.hp -= Brands.dict['grotesque']['bonushp']
					unit.maxhp -= Brands.dict['grotesque']['bonushp']
					unit.str -= Brands.dict['grotesque']['bonusstr']
					if unit.name == 'you': game.game_log.append("Your body returns to its normal shape.")
					else: game.game_log.append("The " + unit.name + "'s body returns to its normal shape.")

				unit.passives.remove([passive[0], passive[1]])

			if not purge: 

				# Manage poisoned
				if name == "poisoned":

					damage = count
					unit.hp -= damage

					if type(unit) == Player:
						game.game_log.append("Venom stings you for " + str(damage) + " damage!")
					else:
						game.game_log.append("Venom stings the " + str(unit.name) + " for " + str(damage) + " damage!")

				# Manage aflame
				if name == "aflame":

					damage = max(1, int(unit.con / 2))
					unit.hp -= damage

					if type(unit) == Player:
						game.game_log.append("Fire burns you for " + str(damage) + " damage!")
					else:
						game.game_log.append("Fire burns the " + str(unit.name) + " for " + str(damage) + " damage!")

				# Manage Frozen
				if name == "frozen":
					unit.time += unit.mspeed
					if type(unit) == Player:
						game.game_log.append("You are frozen!")
					else:
						game.game_log.append("The " + str(unit.name) + " is frozen and cannot move!")


				# Stunned
				if name == "stunned":
					unit.time += unit.mspeed
					if type(unit) == Player:
						game.game_log.append("You are stunned!")
					else:
						game.game_log.append("The " + str(unit.name) + " is stunned!")



		# Check if unit is still alive
		if unit.hp <= 0 and type(unit) != Player:
			game.game_log.append("The " + unit.name + " dies from its wounds!")
			game.units.remove(unit)
			if unit in game.allies: game.allies.remove(unit)

			# Ooze Passive
			if 'split' in enemy.spells: Weapons.spells["split"][0]("split", enemy, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler)

			# Drop Loot
			unit.drop_booty()

			# XP Gain
			game.player.xp += unit.xp + int(d(game.player.cha) / 2)











# GLOBAL FUNCTIONS


def d(range):
	return randint(1,range)

def md(range, number):
	sum = 0
	while number > 0:
		sum += d(range)
		number -= 1
	return sum

def adjacent_to(one, two):
	return True if (abs(one.loc[0] - two.loc[0]) <= 1) and (abs(one.loc[1] - two.loc[1]) <= 1) else False


def rinput(question):
	fd = sys.stdin.fileno()
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON
	newattr[3] = newattr[3] & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldterm = termios.tcgetattr(fd)
	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	print("")
	print(question)
	inp, outp, err = select.select([sys.stdin], [], [])
	decision = sys.stdin.read()

	# Reset the terminal:
	termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	return decision







game = Game()
# try:
game.run()
# except:
# 	pass








