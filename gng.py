from maps import Maps
import ai

from bestiary import Monsters, Bands
from codex import Weapons, Ammos, Brands, Armors, Shields, CharacterRaces

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
		self.rep, self.name, self.passives, self.race  = '@', "you", [], game.race

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.reg = statsheet

		self.hp = 5 + self.con * 5 + self.str
		self.maxhp = 5 + self.con * 5 + self.str

		self.mana = 3 * self.int
		self.maxmana = 3 * self.int

		# Inventory, Spells
		self.inventory, self.spells, self.abilities, self.cooldowns = [], ["magic missile"], [], []

		# Initialze Equipment
		self.wielding, self.hands, self.quivered = [], 2, None

		for equipment in innate_equipment:
			if equipment in Weapons.array: self.give_weapon(equipment)
			elif equipment[0] in Weapons.spells and equipment[1]: self.abilities.append(equipment[0])
			elif equipment[0] in Weapons.spells and not equipment[1]: self.spells.append(equipment[0])

		# Initialize Armor
		self.equipped_armor = Armor('leather armor','}','hide',5,2, 0, None)

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
		if self.race == 'Dragonborn': self.innate_ac += 2
		if self.race == 'Hill Troll':
			self.innate_ac += 1
			self.hands = 4


	def quiver(self):
		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		ammo = []
		for thing in self.inventory:
			if type(thing) == Ammo and thing != self.quivered: ammo.append(thing)

		if len(ammo) != 0:
			print("=======================================================================================")
			print("                                                                     ")
			for i in range(len(ammo)):

				ammunition = ammo[i]
				if ammunition.brand is None: print(str(item_order[i]) + " - " + ammunition.name + " (" + str(ammunition.number) + ")")
				else: print(str(item_order[i]) + " - " + ammunition.brand + ' ' + ammunition.name + " (" + str(ammunition.number) + ")")

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

			print("")
			print("Quiver what?")
			inp, outp, err = select.select([sys.stdin], [], [])
			decision = sys.stdin.read()


			if len(decision) == 1:
				if decision in item_order:
					if item_order.index(decision) < len(ammo):

						# Quiver Item
						self.quivered = ammo[item_order.index(decision)]
						self.time += self.mspeed

						# Quiver Statement
						if self.quivered.brand is None:
							if self.quivered.number > 1: game.game_log.append("You quiver " + str(self.quivered.number) + " " + self.quivered.name + "s!")
							else: game.game_log.append("You quiver 1 " + self.quivered.name + "!")
						else:
							if self.quivered.number > 1: game.game_log.append("You quiver " + str(self.quivered.number) + " " + self.quivered.brand + ' ' + self.quivered.name + "s!")
							else: game.game_log.append("You quiver 1 " + self.quivered.brand + ' ' + self.quivered.name + "!")

				else: game.temp_log.append("That is not a valid input")
			else: game.temp_log.append("That is not a valid input")


			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)


		else: game.temp_log.append("You have nothing to quiver.")




	def fire(self):

		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


		# Throwing weapon
		thrown = False
		if self.quivered is not None:
			if self.quivered.wclass in Ammos.thrown_amclasses:
				thrown = True
				# Create Throwing platform
				item = self.give_weapon(self.quivered.name)



		for item in self.wielding:

			# Ranged Projectile Thrower

			if type(item) == Weapon:
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
						if los is not None and (len(los) - 1 <= (2 * item.damage  + item.to_hit)): units_in_range.append(unit)

					# Ranged range
					if len(units_in_range) != 0:
						print("=======================================================================================")
						print("                                                                     ")
						for i in range(len(units_in_range)):

							unit = units_in_range[i]

							print(str(item_order[i]) + " - " + unit.name)
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

						print("")
						print("Aim at which target?")
						inp, outp, err = select.select([sys.stdin], [], [])
						decision = sys.stdin.read()

						if len(decision) == 1:
							if decision in item_order:
								if item_order.index(decision) < len(units_in_range):

									# Choose Legal Enemy
									unit = units_in_range[item_order.index(decision)]
									self.time += item.speed

									# ATTACK
									item.strike(self, unit)
									self.well_being_statement(unit, item.name, game)

									# Remove throwing weapon
									if thrown: self.wielding.pop()

									# Remove Ammo
									self.quivered.number -= 1
									if self.quivered.number == 0:
										self.inventory.remove(self.quivered)
										self.quivered = None
									return

								else: game.temp_log.append("That is not a valid input")
						else: game.temp_log.append("That is not a valid input")


						# Reset the terminal:
						termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
						fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

					else:
						game.temp_log.append("There are no targets in range!")
						# Remove throwing weapon
						if thrown: self.wielding.pop()
						return

		game.temp_log.append("You are not wielding a ranged weapon!")
		# Remove throwing weapon
		if thrown: self.wielding.pop()


	def well_being_statement(self, unit, means, game):

		# If enemy is defeated
		if unit.hp <= 0:

			# Remove from units
			game.game_log.append("You slay the "  + str(unit.name) + " with your " + means + "!")
			game.units.remove(unit)

			# Drop Loot
			unit.drop_booty()

			# XP Gain
			self.xp += unit.xp + int(d(self.cha) / 2)
			return

		if unit.hp / unit.maxhp > 0.9: game.game_log.append("The "  + str(unit.name) + " seems uninjured.")

		# Enemy over 70%	
		elif unit.hp / unit.maxhp > 0.7: game.game_log.append("The "  + str(unit.name) + " seems only lightly wounded.")

		# Enemy over 30%
		elif unit.hp / unit.maxhp > 0.3: game.game_log.append("The "  + str(unit.name) + " seems moderately wounded.")

		# Enemy under 30%
		elif unit.hp > 0: game.game_log.append("The "  + str(unit.name) + " seems nearly dead!")





	def spell(self):

		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		if len(self.spells) == 0:
			game.game_log.append("You don't know any spells, dummy!")
			return

		
		print("=======================================================================================")
		print("                                                                     ")
		i = 0
		for spell in self.spells:
			print("(" + str(Weapons.spells[spell][1]) + " mana) " + str(item_order[i]) + " - " + spell)
			i += 1
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

		# Controller
		print("")
		print("Cast which spell?")
		inp, outp, err = select.select([sys.stdin], [], [])
		decision = sys.stdin.read()
		valid = False

		if decision == '9':
			valid = True
			return

		elif len(decision) == 1:
			if decision in item_order:
				if item_order.index(decision) < len(self.spells):

					spell_name = self.spells[item_order.index(decision)]
					spell = Weapons.spells[spell_name][0]

					valid = True

				else:
					game.temp_log.append("That is not a valid input")
					return
		else:
			game.temp_log.append("That is not a valid input")
			return

		if not valid: return

		# Check Mana
		if self.mana < Weapons.spells[spell_name][1]:
			game.temp_log.append("You dont have enough mana to cast that.")
			return

		# Self-cast
		if not Weapons.spells[spell_name][3]:
			print(spell_name)
			if spell(spell_name, self, self, game, Maps.rooms[game.map.map][0], game.map.room_filler):
				self.mana -= Weapons.spells[spell_name][1]
				self.time += Weapons.spells[spell_name][2]
			return



		# Get units in range
		units_in_range = []
		for unit in game.units[1:]:
			los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
			if los is None: continue
			if Weapons.spells[spell_name][4]:
				if len(los) - 1 <= Weapons.spells[spell_name][5]: units_in_range.append(unit)
			else: units_in_range.append(unit)

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

				print(str(item_order[i]) + " - " + unit.name)
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

			# Controller
			print("")
			print("Cast " + spell_name + " at which target?")
			inp, outp, err = select.select([sys.stdin], [], [])
			decision = sys.stdin.read()

			if decision == '9': valid = True

			elif len(decision) == 1:
				if decision in item_order:
					if item_order.index(decision) < len(units_in_range):

						# Choose Legal Enemy
						unit = units_in_range[item_order.index(decision)]

						# Enemy Resist spell
						if d(100) / 100 <= max(0.05, min(0.75, (unit.cha / 2) / self.int)):
							self.time += Weapons.spells[spell_name][2]
							self.mana -= Weapons.spells[spell_name][1]
							game.game_log.append("The " + unit.name + " resists your " + spell_name + "!")
							return

						if spell(spell_name, self, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler):
							self.mana -= Weapons.spells[spell_name][1]
							self.time += Weapons.spells[spell_name][2]
						valid = True
						return

					else: print("That is not a valid input")
			else: print("That is not a valid input")


			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

		else:
			game.temp_log.append("There are no targets in range!")
			return





	def ability(self):

		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		if len(self.spells) == 0:
			game.game_log.append("You don't have any abilities, dummy!")
			return

		
		print("=======================================================================================")
		print("                                                                     ")
		i = 0
		for spell in self.abilities:
			print(str(item_order[i]) + " - " + spell)
			i += 1
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

		# Controller
		print("")
		print("Use which ability?")
		inp, outp, err = select.select([sys.stdin], [], [])
		decision = sys.stdin.read()
		valid = False

		if decision == '9':
			valid = True
			return

		elif len(decision) == 1:
			if decision in item_order:
				if item_order.index(decision) < len(self.abilities):


					spell_name = self.abilities[item_order.index(decision)]
					spell = Weapons.spells[spell_name][0]


					valid = True

				else:
					game.temp_log.append("That is not a valid input")
					return
		else:
			game.temp_log.append("That is not a valid input")
			return

		if not valid: return

		# Self-cast
		if not Weapons.spells[spell_name][3]:
			print(spell_name)
			if spell(spell_name, self, self, game, Maps.rooms[game.map.map][0], game.map.room_filler, True):
				self.time += Weapons.spells[spell_name][2]
				self.cooldowns.append( [spell_name, Weapons.spells[spell_name][1] * 2] )
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

				print(str(item_order[i]) + " - " + unit.name)

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

			# Controller
			print("")
			print("Cast " + spell_name + " at which target?")
			inp, outp, err = select.select([sys.stdin], [], [])
			decision = sys.stdin.read()

			if decision == '9': valid = True

			elif len(decision) == 1:
				if decision in item_order:
					if item_order.index(decision) < len(units_in_range):

						# Choose Legal Enemy
						unit = units_in_range[item_order.index(decision)]

						if spell(spell_name, self, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler, True):
							self.time += Weapons.spells[spell_name][2]
							self.cooldowns.append( [spell_name, Weapons.spells[spell_name][1] * 2] )
							self.abilities.remove(spell_name)
						valid = True

						# # Enemy Well-being Statement
						# self.well_being_statement(unit, game)

						return

					else: print("That is not a valid input")
			else: print("That is not a valid input")


			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

		else:
			game.temp_log.append("There are no targets in range!")
			return


	def racial_level_bonuses(self):
		# Racial level-ups
		if self.race == "Elf" and self.level % 4 == 0:
			if d(10) <= 6:
				self.dex += 1
				game.game_log.append("You feel more agile...")
			else:
				self.int += 1
				game.game_log.append("You feel smarter...")

		if self.race == "Cytherean" and self.level % 4 == 0:
			if d(10) <= 7:
				self.int += 1
				game.game_log.append("You feel smarter...")
			else:
				self.con += 1
				self.hp += 5
				self.maxhp += 5
				game.game_log.append("You feel hardier...")

		if self.race == "Dragonborn" and self.level % 5 == 0:
			if d(10) <= 5:
				self.str += 1
				game.game_log.append("You feel stronger...")
			else:
				self.con += 1
				self.hp += 5
				self.maxhp += 5
				game.game_log.append("You feel hardier...")

		if self.race == "Gnome" and self.level % 4 == 0:
			if d(10) <= 5:
				self.int += 1
				game.game_log.append("You feel smarter...")
			else:
				self.cha += 1
				game.game_log.append("You feel more charismatic...")

		if self.race == "Hobbit" and self.level % 4 == 0:
			if d(10) <= 4:
				self.cha += 1
				game.game_log.append("You feel more charismatic...")
			else:
				self.dex += 1
				game.game_log.append("You feel more agile...")

		if self.race == "Terran" and self.level % 4 == 0:
			roll = d(10)
			if roll > 8:
				self.str += 1
				game.game_log.append("You feel stronger...")
			elif roll > 6:
				self.dex += 1
				game.game_log.append("You feel more agile...")
			elif roll > 4:
				self.cha += 1
				game.game_log.append("You feel more charismatic...")
			elif roll > 2:
				self.int += 1
				game.game_log.append("You feel smarter...")
			else:
				self.con += 1
				self.hp += 5
				self.maxhp += 5
				game.game_log.append("You feel hardier...")

		if self.race == "Naga" and self.level % 4 == 0:
			if d(10) <= 4:
				self.str += 1
				game.game_log.append("You feel stronger...")
			else:
				self.dex += 1
				game.game_log.append("You feel more agile...")

		if self.race == "Hill Troll" and self.level % 5 == 0:
			if d(10) <= 5:
				self.str += 1
				game.game_log.append("You feel stronger...")
			else:
				self.con += 1
				self.hp += 5
				self.maxhp += 5
				game.game_log.append("You feel hardier...")

		if self.race == "Ghoul" and self.level % 5 == 0:
			if d(10) <= 5:
				self.str += 1
				game.game_log.append("You feel stronger...")
			else:
				self.con += 1
				self.hp += 5
				self.maxhp += 5
				game.game_log.append("You feel hardier...")

		if self.race == "Black Orc" and self.level % 5 == 0:
			if d(10) <= 4:
				self.str += 1
				game.game_log.append("You feel stronger...")
			elif d(10) <= 6:
				self.con += 1
				self.hp += 5
				self.maxhp += 5
				game.game_log.append("You feel hardier...")
			else:
				self.cha += 1
				game.game_log.append("You feel more charismatic...")

		if self.race == "Dwarf" and self.level % 4 == 0:
			if d(10) <= 3:
				self.cha += 1
				game.game_log.append("You feel more charismatic...")
			else:
				self.con += 1
				self.hp += 5
				self.maxhp += 5
				game.game_log.append("You feel hardier...")





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
				print("Increase your (C)onsititution, (S)trength, (D)exterity, (I)ntelligence, or c(H)arisma?")
				inp, outp, err = select.select([sys.stdin], [], [])
				stat = sys.stdin.read()

				if stat.lower() == "c"or stat.lower() == "s"or stat.lower() == "d"or stat.lower() == "i"or stat.lower() == "h":
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
					elif stat.lower() == "h":
						stat = "Charisma"
						self.cha += 1
					print("You increase your " + stat + "!")

					valid = True

				else: print("Pick a stat!")

			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

	def equip(self, item):

		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		# Carrying
		total_hands = self.hands
		carrying = []
		for thing in self.wielding:
			total_hands += thing.hands
			if thing.hands > 0: carrying.append(thing)

		# Equip Weapon
		if type(item) == Weapon or type(item) == Shield:

			# Ranged weapons require all hands
			if type(item) == Weapon:
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
					return

			# Not enough total hands
			if item.hands > total_hands:
				game.temp_log.append("You cannot wield that weapon!")
				return

			# Not enough FREE Hands
			if self.hands < item.hands or len(carrying) == 2:

				# Already carrying something
				if len(carrying) == 2 and item.hands < total_hands:

					fd = sys.stdin.fileno()
					newattr = termios.tcgetattr(fd)
					newattr[3] = newattr[3] & ~termios.ICANON
					newattr[3] = newattr[3] & ~termios.ECHO
					termios.tcsetattr(fd, termios.TCSANOW, newattr)

					oldterm = termios.tcgetattr(fd)
					oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
					fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
					valid = False

					# Equipped string UI
					equipped = ""
					for i in range(len(carrying)):
						if len(equipped) != 0: equipped += ', ' + '(' + str(item_order[i]) + ") " + carrying[i].name
						else: equipped += '(' + str(item_order[i]) + ") " + carrying[i].name

					while not valid:
						print("")
						print("Swap for " + equipped + "?")
						inp, outp, err = select.select([sys.stdin], [], [])
						decision = sys.stdin.read()

						if decision == '9':
							valid = True
							# Reset the terminal:
							termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
							fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
							return

						if decision in item_order:
							if item_order.index(decision) < len(carrying):
								ditem = carrying[item_order.index(decision)]
								valid = True

								# Remove chosen item
								game.game_log.append("You put away the " + ditem.name + '.')
								self.wielding.remove(ditem)
								self.inventory.append(ditem)
								self.hands += ditem.hands

						# Reset the terminal:
						termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
						fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

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
		return True

	def unequip(self, weapon):
		if type(item) == Weapon:
			self.wielding.remove(weapon)
			self.inventory.append(weapon)
			self.hands += item.hands
			game.game_log.append("You unequip " + item.name + ".")
			self.time += self.mspeed

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
		del self.inventory[self.inventory.indexOf(item)]
		game.items.append(item)
		game.game_log.append("You drop the item named" + item.name)
		self.time += self.mspeed

	def give_weapon(self, weapon):
		data = Weapons.array[weapon]

		# Manage Brand + Probability
		try: brand = data[7]
		except: brand = None
		try: prob = data[8]
		except: prob = None

		# Create Weapon Object
		self.wielding.append(Weapon(weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], None, brand, prob))
		return self.wielding[-1]

	def calc_AC(self):
		return self.equipped_armor.armor_rating + self.equipped_armor.enchantment + self.innate_ac


	def atk_mv(self, map, coords):

		# Find melee weapons
		weaps = []
		carrying = []
		for item in self.wielding[::-1]:
			if type(item) == Weapon:
				if item.hands > 0: carrying.append(item)
				if item.wclass not in Weapons.ranged_wclasses: weaps.append(item)
			if type(item) == Shield: carrying.append(item)

		if map.square_identity(coords) in set(['|', '-', ' ', '#']): return

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


				# Equip fists
				unarmed = []
				if len(carrying) == 0 or (len(carrying) == 1 and self.race == "Hill Troll"):
					if len(carrying) == 0 and self.race == "Hill Troll": 
						fists = self.give_weapon('fist smash')
						unarmed.append(fists)
						weaps.append(fists)
					else:
						fists = self.give_weapon('fists')
						unarmed.append(fists)
						weaps.append(fists)

				# Attack with each weapon
				for item in weaps:
					item.strike(self, unit)
					if unit.hp <= 0: break

				# Enemy Well-being Statement
				self.well_being_statement(unit, item.name, game)

				# Unequip fists
				for fist in unarmed: self.wielding.remove(fist)

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






		# Check whats on the ground
		for item in game.items:

			if coords == item.loc and type(item) == Chest:
				if item.opened: game.game_log.append("You see here an opened chest")
				else:
					article = "an" if item.type[0] in set(['a','e','i','o','u']) else 'a'
					game.game_log.append("You see here " + article + " " + item.type + " chest")

			# Look for loot on the ground in case of a move
			elif coords == item.loc:

				if type(item) == Ammo:

					# Enchantment String
					if item.brand is not None:

						# Brand case
						if len(ground_booty) == 0: ground_booty += str(item.brand) + ' ' + item.name + " (" + str(item.number) + ")"
						else: ground_booty += ', ' + str(item.brand) + ' ' + item.name + " (" + str(item.number) + ")"
					else:
						# No Brand Case
						if len(ground_booty) == 0: ground_booty +=  item.name + " (" + str(item.number) + ")"
						else: ground_booty += ', ' + item.name + " (" + str(item.number) + ")"

				else:
					# Enchantment String
					ench = item.enchantment
					if ench >= 0: ench = '+' + str(ench)
					if item.brand is not None:

						# Brand case
						if len(ground_booty) == 0: ground_booty += str(item.brand) + ' ' + str(ench) + ' ' + item.name
						else: ground_booty += ', ' + str(item.brand) + ' ' + str(ench) +  ' ' + item.name
					else:
						# No Brand Case
						if len(ground_booty) == 0: ground_booty += str(ench) + ' ' + item.name
						else: ground_booty += ', ' + str(ench) +  ' ' + item.name


		# Add ground loot to the log
		if len(ground_booty) != 0: game.game_log.append("You see here: " + ground_booty)

		# Move unit
		self.loc = coords
		self.time += self.mspeed

	


class Monster():

	def __init__(self,      name, char, etype, tier,    con, st, dex, int, cha, mspeed, xp,   pot_weapons, pot_armor,  loc, other_items = None):

		# Initialize Representation
		self.rep, self.name, self.etype, self.tier = char, name, etype, tier

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

		# Monster's Equipment
		self.wielding , self.other_items, self.quivered = [], other_items, None

		# Give innate weapons / shields
		if other_items is not None:
			for item in other_items:
				if item in Ammos.array: self.give_ammo(item)
				elif item in Weapons.array: self.give_weapon(item)
				elif item in Shields.array: self.give_shield(item)
				elif item in Weapons.spells: self.spells.append(item)

		# Give Weapon and Armor
		weapon = pot_weapons[d(len(pot_weapons)) - 1]
		if type(weapon) == list:
			for item in weapon:
				if item in Weapons.array: self.give_weapon(item)
				if item in Shields.array: self.give_shield(item)
		else: self.give_weapon(weapon)
		self.give_armor( pot_armor[  d(len(pot_armor)) - 1])

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
		if self.quivered is not None:
			self.quivered.loc = self.loc
			game.items.append(self.quivered)


	def give_weapon(self, weapon):
		data = Weapons.array[weapon]

		# Manage Enchantment
		spawned_enchantment = data[3]
		if d(10) + (1.5 * self.tier) > 13: spawned_enchantment += d(self.tier - 1)

		# Manage Brand + Probability
		try: brand = data[7]
		except: brand = None
		if brand is None:
			if d(100) > 99 - self.tier and data[2] > 0: brand = Brands.brands[d(len(Brands.brands)) - 1]
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
		except: brand = None

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
			if d(100) > 99 - self.tier and data[2] > 0: brand = Brands.brands[d(len(Brands.brands)) - 1]

		# Manage Number
		if data[1] in Ammos.thrown_amclasses: number = 4 + 2 * self.tier
		else: number = 10 + 5 * self.tier

		# Create Ammo Object
		self.quivered = Ammo(ammo, data[0], data[1], number, data[2], None, brand)


	def turn(self):

		melee_attacked = False

		# MAGIC!!
		if len(self.spells) > 0:

			# Chance to use spells
			if d(10) + min(self.int, 7) >= 11:


				los = ai.los(self.loc, game.player.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:

					# Shift around spells
					if len(self.spells) > 2: shuffle(self.spells)
					# Zap with spells
					for spell in self.spells:
						# Check for mana
						if self.mana >= Weapons.spells[spell][1]:
							spell_fun = Weapons.spells[spell][0]

							# If target
							if Weapons.spells[spell][4]:

								# If in spell range
								if len(los) - 1 <= Weapons.spells[spell][5]:

									# Player Resist spell
									if d(100) / 100 <= max(0.05, min(0.9, (game.player.cha / 2) / self.int)):
										self.time += Weapons.spells[spell][2]
										self.mana -= Weapons.spells[spell][1]
										game.game_log.append("You resist the " + spell + " from the " + self.name + "!")
										return


									if spell_fun(spell, self, game.player, game, Maps.rooms[game.map.map][0], game.map.room_filler):
										self.time += Weapons.spells[spell][2]
										self.mana -= Weapons.spells[spell][1]
										return
							# No target
							else:
								if spell_fun(spell, self, game.player, game, Maps.rooms[game.map.map][0], game.map.room_filler):
									self.time += Weapons.spells[spell][2]
									self.mana -= Weapons.spells[spell][1]
									return



		# Melee Attack
		if adjacent_to(self,game.player):

			# Find weapons
			weaps = []
			for item in self.wielding[::-1]:
				if type(item) == Weapon: weaps.append(item)

			# Calc Attack Speed
			if len(weaps) != 0:
				maxas = 0
				for weapon in weaps:
					 if weapon.speed > maxas and weapon.wclass not in Weapons.ranged_wclasses: maxas = weapon.speed

			# Hit with melee
			for item in weaps:
				if item.wclass not in Weapons.ranged_wclasses: item.strike(self,game.player)

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
			if type(item) == Weapon:
				if item.wclass in Weapons.ranged_wclasses or item.wclass in Ammos.thrown_amclasses:

					if self.quivered is not None or item.hands == 0:

						if item.hands > 0 and melee_attacked:
							if thrown: self.wielding.pop()
							return

						los = ai.los(self.loc, game.player.loc, Maps.rooms[game.map.map][0], game )
						if los is not None:

							# Ranged range
							if len(los) <= (2 * item.damage  + item.to_hit):
								item.strike(self, game.player)

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
			ai.smart_move_towards(self, game.player, game)
			self.time += self.mspeed




class Weapon():

	def __init__(self,  name, rep, wclass, hands, enchantment, damage, to_hit, speed,   loc, brand = None, probability = None):

		# Initialize Weapon Stats
		self.name, self.rep, self.wclass, self.hands, self.enchantment, self.damage, self.to_hit, self.speed, self.loc, self.brand, self.probability = name, rep, wclass, hands, enchantment, damage, to_hit, speed, loc, brand, probability

		# Deal with prob
		if self.probability is None: self.probability = 100

		# Ranged Brands
		if self.wclass in Weapons.ranged_wclasses: self.brand = None

	def strike(self, attacker, enemy, wtypeeff = True):

		brand = self.brand
		wclass = self.wclass
		to_hit = self.to_hit

		# Check for enemy status
		frozen = False
		for passive in enemy.passives:
			if passive[0] == "frozen": frozen = True

		# Swing Probability
		if d(100) > (100 - self.probability):

			# Calc Encumberance
			self_encumb = attacker.equipped_armor.encumberance - attacker.equipped_armor.enchantment
			enemy_encumb = enemy.equipped_armor.encumberance - enemy.equipped_armor.enchantment

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

				# Shield Block
				for weapon in enemy.wielding:
					if type(weapon) == Shield:
						if d(100) > max(33, 90 - (3 * weapon.armor_rating)):

							# Block Statement
							if type(attacker) == Monster: game.game_log.append("You block the "   + str(attacker.name) + "'s " + self.name + " with your " + weapon.name + "!")
							else: game.game_log.append("The "   + str(enemy.name) +  " blocks your " + self.name + " with its " + weapon.name + "!")
							return


				# DAMAGE forumla

				# Projectile weapon
				if self.wclass in Weapons.ranged_wclasses and self.hands > 0:
					damage = int (d(self.damage) + d(attacker.quivered.damage) + attacker.dex / 2 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
					brand = attacker.quivered.brand
					wclass = attacker.quivered.wclass
				# Thrown Weapon
				elif self.wclass in Ammos.thrown_amclasses and self.hands > 0:
					damage = int (d(self.damage) + d(attacker.quivered.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
					brand = attacker.quivered.brand
					wclass = attacker.quivered.wclass
				# Melee weapon
				else: damage = int (d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )


				# Apply Brands
				brandhit = False

				if brand == "envenomed": brandhit = d(100) > 33
				elif brand == "flaming": brandhit = d(100) > 60
				elif brand == "infernal": brandhit = d(100) > 65
				elif brand == "frozen": brandhit = d(100) > 80
				elif brand == "spectral": brandhit = True if len(enemy.spells) > 0 else False
				elif brand == "silvered":
					if enemy.name != 'you': brandhit = True if enemy.etype in set(["undead","demon","skeleton"]) else False
					else: brandhit = True if enemy.race in set(["ghoul"]) else False
				elif brand is not None: brandhit = True

				# Apply Brands
				damage = self.apply_brands(attacker, enemy, damage, brand, brandhit)

				# Weapon class effects
				if wtypeeff: damage = self.weapon_type_effect(attacker, enemy, damage)

				# No damage case
				if damage <= 0:
					damage = 0

					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " hits you with its " + wclass + " but does no damage!")
					else: game.game_log.append("You " + Weapons.weapon_classes[wclass][0] + " your "+ str(wclass) + " " + Weapons.weapon_classes[wclass][1] + " the " + str(enemy.name)+ " but deal no damage!")

				# Damage Case - Statement
				else: self.damage_statement(attacker, enemy, damage, brand, brandhit)
						
				# Resolve Damage
				enemy.hp -= damage

			# Miss Case
			else:

				# Manage blades
				counter = None
				for weapon in enemy.wielding:
					if type(weapon) == Weapon:
						if weapon.wclass in set(["sword","bastard sword","demon sword","god sword"]) and self.wclass not in Weapons.ranged_wclasses: 

							# Counter chance
							if d(100) + 3 * enemy.dex > 75: counter = weapon

				# Miss statement
				if self.wclass in Weapons.ranged_wclasses:
					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " shoots at you with its " + self.wclass + " but misses.")
					else: game.game_log.append("You closely miss the " + str(enemy.name) + " with your " + self.wclass + "!")
				elif self.wclass in Ammos.thrown_amclasses:
					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " hurls a " + self.wclass + " at you but misses.")
					else: game.game_log.append("You closely miss the " + str(enemy.name) + " with your " + self.wclass + "!")
				else:
					if type(attacker) == Monster: game.game_log.append("The "  + str(attacker.name) + " swings at you with its " + self.wclass + " but misses.")
					else: game.game_log.append("You closely miss the " + str(enemy.name) + " with your " + self.wclass + "!")

				# Riposte with blade
				if counter is not None:
					damage = int (d(int(counter.damage * 0.75)) + attacker.str / 1.5 + counter.enchantment - ( 0.75 * enemy.calc_AC() ) )
					if damage > 0:
						if type(attacker) != Monster: game.game_log.append("The "  + str(enemy.name) + " counters you with its blade for " + str(damage) + " damage!")
						else: game.game_log.append("You counter the " + str(attacker.name) + " with your blade for " + str(damage) + " damage!")

						attacker.hp -= damage
						if attacker.name != "you": game.player.well_being_statement(attacker, counter.name, game)


	def weapon_type_effect(self, attacker, enemy, damage):


		# Blunt weapons
		if self.wclass == "hammer" or self.wclass == "club" or self.wclass == "mace" or self.wclass == "flail":
			if enemy.equipped_armor.aclass == 'plate': damage *= 1.4

		if self.wclass == "warhammer" or  self.wclass == "god hammer":
			if enemy.equipped_armor.aclass == 'plate': damage *= 1.4

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



		if self.wclass == "dagger":
			pass

		if self.wclass == "greatsword" or self.wclass == "god sword" or self.wclass == "bastard sword":

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


		if self.wclass == "spear" or self.wclass == "polearm" or self.wclass == "lance":
			for unit in game.units:
				if unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, False)
					break

		if self.wclass == "pike" or self.wclass == "god spear":
			for unit in game.units:
				if unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, False)
				if unit.loc == (attacker.loc[0] - 3 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 3 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, False)

		if self.wclass == "axe":
			damage *= (1 + max(0, (0.25 - enemy.calc_AC() / 50 )) )

		if self.wclass == "greataxe" or self.wclass == "god axe":
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
			if brand == "flaming":
				count = Brands.dict["flaming"]["count"]
				status = "aflame"

				for passive in enemy.passives:
					
					if passive[0] == status: return damage

				enemy.passives.append([status, count])

			if brand == "infernal":
				count = Brands.dict["drained"]["count"]
				status = "drained"

				for passive in enemy.passives:
					
					if passive[0] == status:
						passive[1] = count
						return damage

				enemy.passives.append([status, count])
				enemy.dex -= Brands.dict["drained"]["dex_loss"]

			if brand == "vampiric":
				attacker.hp += int(damage / 3)

				# Heal
				if attacker.hp > attacker.maxhp: attacker.hp = attacker.maxhp

			if brand == "hellfire":
				damage += int((1 - (enemy.hp / enemy.maxhp) ) * damage * 0.5)

			if brand == "envenomed":
				count = Brands.dict["envenomed"]["count"]
				status = "poisoned"

				for passive in enemy.passives:

					if passive[0] == status:
						passive[1] += count
						return damage

				enemy.passives.append([status, count])

			# Manage Silvered
			if brand == "silvered":
				damage *= 1.5

			# Manage Spectral
			if brand == "spectral":
				damage *= 1.5

			if brand == "frozen":
				status, count = "frozen", Brands.dict["frozen"]["count"]
				# Apply effect
				for passive in enemy.passives:

					if passive[0] == status:
						passive[1] += count
						return damage

				enemy.passives.append([status, count])

		# Return DAMAGE
		return damage


	def damage_statement(self, attacker, enemy,  damage, brand, brandhit):
		attacker_var =  str(attacker.name)
		attackee_var = str(enemy.name)
		name = self.name
		wclass = self.wclass

		if self.wclass in Weapons.ranged_wclasses and self.hands > 0:
			name = attacker.quivered.name
			wclass = attacker.quivered.wclass

		# Make the sentence awesome
		verb, preposition = Weapons.weapon_classes[wclass]

		# Make the notes dank
		if brand is None or not brandhit:
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " +  name + "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var + " for " + str(damage) + " damage!")

		elif brand == "silvered":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its "  + name + ", its silver burns you!")
			else:
				game.game_log.append("You " + verb + " your silvered "+ str(wclass) + " " + preposition + " the " + attackee_var+ ", the silver burns for " + str(damage) + " damage!")

		elif brand == "spectral":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its spectral "  + name + ", your magic burns inside you!")
			else:
				game.game_log.append("You " + verb + " your spectral "+ str(wclass) + " " + preposition + " the " + attackee_var+ ", tearing the mage apart for " + str(damage) + " damage!")

		elif brand == "vampiric":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its "  + name + " and steals your life!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " the " + attackee_var+ ", dealing " + str(damage) + " damage and draining its life!")

		elif brand == "flaming":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " + name + " and sets you aflame!")
			else:
				game.game_log.append("You " + verb + " your flaming "+ str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and setting it aflame!")

		elif brand == "infernal":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its infernal " + name + " and saps your soul!")
			else:
				game.game_log.append("You " + verb + " your infernal "+ str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and sapping its soul!")

		elif brand == "frozen":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its frozen " + name + " and freezes you!")
			else:
				game.game_log.append("You " + verb + " your frozen "+ str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and freezing it!")

		elif brand == "hellfire":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " + name + " and sets your soul aflame!")
			else:
				game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and tearing its soul!")

		elif brand == "envenomed":
			if type(attacker) == Monster:
				game.game_log.append("The "  + attacker_var + " hits you for " + str(damage) + " damage with its " + name + " and poisons you!")
			else:
				game.game_log.append("You " + verb + " your envenomed " + str(wclass) + " " + preposition + " the " + attackee_var + ", dealing " + str(damage) + " damage and poisoning it!")


class Armor():

	def __init__(self, name, rep,  aclass, armor_rating, encumberance, enchantment, loc, brand = None):
		self.name, self.rep, self.aclass, self.armor_rating, self.encumberance, self.enchantment, self.loc, self.brand = name, rep, aclass, armor_rating, encumberance, enchantment, loc, brand

class Shield():

	def __init__(self, name, rep, hands, armor_rating, encumberance, enchantment, loc, brand = None):
		self.name, self.rep, self.hands, self.armor_rating, self.encumberance, self.enchantment, self.loc, self.brand = name, rep, hands, armor_rating, encumberance, enchantment, loc, brand

class Ammo():

	def __init__(self, name, rep, wclass, number, damage, loc, brand = None):
		self.name, self.rep, self.wclass, self.damage, self.number, self.loc, self.brand = name, rep, wclass, damage, number, loc, brand

class Chest():

	def __init__(self, type, tier,  loc):
		self.tier, self.type, self.loc = tier, type, loc

		# Initialize Rep
		self.rep = '='
		self.opened = False

		# Chest contents
		if self.type == "orcish":
			self.pot_weapons = [ ["goblin spear","stabba","choppa"],
								 ["bear hide","ogre hide"],
								 ["choppa","slica","smasha"],
								 ["goblin bow","crude shortbow","iron javelin"], 
								 ["big choppa","big slica","skull smasha"], 
								 ["scrap plate armor","berserker mail","troll hide"], 
								 ["toxic slica"],
								 ["ice choppa"],]
		elif self.type == "elven":
			self.pot_weapons = [ ["spear","elven leafblade","iron javelin"],
								 ["spear","elven leafblade"],
								 ["spear","elven leafblade","elven longbow"],
								 ["elven longbow"], ]
		elif self.type == "wooden":
			self.pot_weapons = [    ["steel dagger","iron axe","spear","hammer","mace","iron longsword","club","iron shortsword"], 
									["crude shortbow","iron battleaxe","iron longsword","mace","flail","quarterstaff","iron bastard sword"], 
									["buckler shield", "wooden broadshield","trollhide shield","recurve bow"], 
									["iron battleaxe","iron greatsword","warhammer","spiked club","barbed javelin"],
									["iron plate armor","iron chainmail","ironscale mail","scrap plate armor"],
									["steel axe","steel longsword","halberd","steel bastard sword","steel shortsword"],
									["steel greatsword","steel battleaxe","pike","greatflail","ranger longbow"] ]

	def open(self):

		n = 1

		# Place Weapons/Armor/Shield
		while n <= game.player.level:
			if len(self.pot_weapons) == 0: return

			# Calculate Tier
			tier = self.pot_weapons[min( n - 1, len(self.pot_weapons) - 1 )] # player level / Specifies not to overshoot
			item_name = tier [ d( len(tier)) - 1]

			# Chance to get item
			if d(100) / 100 <= n / game.player.level:

				# If Ammo
				if item_name in Ammos.array:
					game.map.room_filler.place_ammo(item_name, self.loc, 5 + 4 * self.tier)

				# If weapon
				elif item_name in Weapons.array:

					# Chance for brand
					brand = None
					if Weapons.array[item_name][2] > 0:
						if d(100) + 2 * n > 99: brand = Brands.brands[d(len(Brands.brands)) - 1]
					game.map.room_filler.place_weapon(item_name, self.loc, int((d(self.tier) - 1) / 2), brand)

				# If Armor
				elif item_name in Armors.array:
					game.map.room_filler.place_armor(item_name, self.loc, int((d(self.tier) - 1) / 2))

				#If Shield
				elif item_name in Shields.array:
					game.map.room_filler.place_shield(item_name, self.loc, int((d(self.tier) - 1) / 2))

				self.pot_weapons.remove(tier)

			n += 1

		# Place Ammo
		game.map.room_filler.place_ammo("iron arrow", self.loc, 5 + 2 * self.tier)


		self.opened = True





		



			






class Map():

	def __init__(self, player, room):

		self.map = room

		self.player = player

		self.def_map_array = Maps.rooms[self.map][0]
		self.map_array = deepcopy(self.def_map_array)

		self.entry_point, self.exits = Maps.rooms[self.map][2], Maps.rooms[self.map][3]


		self.adjacent = {self.entry_point: None}
		for point in self.exits[1:]:
			self.adjacent[point] = None

		self.objects = []

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
		for line in self.map_array: print(self.parse(line))

	def change_room(self, new_room):

		room = new_room[0]
		newloc = new_room[1]

		# Store units
		for unit in game.units:
			if type(unit) == Monster:
				self.objects.append(unit)

		for item in game.items: self.objects.append(item)

		# Clear units
		game.units, game.items = [game.player], []

		# Add old room's units
		for object in room.objects: game.units.append(object) if type(object) == Monster else game.items.append(object)

		room.objects, game.map = [], room

		# Place boyo on map
		if newloc == Maps.rooms[new_room[0].map][2]:
			self.player.loc = (newloc[0] + 1, newloc[1])
		else:
			self.player.loc = (newloc[0] - 1, newloc[1])



	def new_room(self, coords):

		# Store units
		for unit in game.units:
			if type(unit) == Monster: self.objects.append(unit)

		for item in game.items: self.objects.append(item)

		# Clear units
		game.units, game.items = [game.player], []

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
		return self.map_array[x][y]

	def can_move(self, loc):
		try: self.square_identity(loc)
		except: return False
		if self.square_identity(loc) in set(['|', '-', ' ', '#']): return False
		for unit in game.units:
			if loc == unit.loc: return False
		return True



class RoomFiller():

	def __init__(self, tier, pos, map):
		self.tier, self.pos, self.map = tier, pos, map

	def place(self):

		# Fill if specified by map
		if Maps.rooms[self.map][4]: self.fill()

		# Place Chests
		for loc, chance in Maps.rooms[self.map][1]:

			# Pick Type
			roll = d(100)
			if roll > 95: type = "elven"
			elif roll > 80: type = "orcish"
			else: type = "wooden"

			if d(100) <= chance: self.place_chest(type, game.player.level, loc)

	def fill(self):

		# Tier and Band pick
		tier_group = Bands.dicto[ min(self.tier, len(Bands.dicto)) ]
		band = tier_group[d(len(tier_group)) -1]

		# Bonuses and actual bands
		bonus, groups = Bands.formations[band]

		# Cut off some units
		for group in groups[:self.tier + bonus]:

			# Choose which units to spawn
			if len(group) > 0:

				unit = d(self.tier + 1) - 1
				if unit >= len(group): unit = len(group) - 1

				picked = False
				while not picked:

					# Pick spawn location
					try: spawn_location = (d(int(len(Maps.rooms[self.map][0][0]))) - 1, d(len(Maps.rooms[self.map][0])) - 1)
					except: spawn_location = (d(len(Maps.rooms[self.map][0][0])) - 1, d(len(Maps.rooms[self.map][0])) - 1)

					if game.map.square_identity(spawn_location) not in set(['|', '-', ' ', '#','+']):
						picked = True
						prev_loc = spawn_location


				self.spawn(group[unit] , spawn_location)

	def spawn(self, monster_name, loc):
		data = Monsters.array[monster_name]
		try: other_items = data[12]
		except: other_items = None

		# Spawn Unit
		game.units.append(Monster(monster_name, data[0],data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], loc, other_items))

	def place_weapon(self, weapon, loc, enchantment = 0, brand = None):
		data = Weapons.array[weapon]

		# Manage Enchantment + Brand
		try: spawned_enchantment = data[3] + enchantment
		except: spawned_enchantment = enchantment
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
		spawned_enchantment = data[2] + enchantment
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
		self.race = "Hill Troll"

		self.player = Player(CharacterRaces.races[self.race][0], CharacterRaces.races[self.race][1], self)
		self.map = Map(self.player, 'starting_room')
		self.state = 'ongoing'
		self.room = 0

		# Initiate Regen
		self.hregen, self.mregen = 0, 0

		# Manage Units
		self.units, self.items, self.seen = [self.player], [], set([])

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
				elif unit.time == min_time: indeces.append(i)
				i += 1

			for index in indeces:
				try: tunit = game.units[index]
				except: continue

				self.check_passives(tunit)
				if tunit.time != min_time: continue

				if type(tunit) == Monster:
					if tunit.hp > 0: tunit.turn()
				elif type(tunit) == Player: self.player_turn(self.map)

			for unit in game.units: unit.time -= min_time



	def player_turn(self, map):


		def action(move):
			x, y = self.player.loc[0], self.player.loc[1]



			# Base Case
			if move in set(['h','H','j','J','k','K','l','L','y','Y','u','U','b','B','n','N',',','.','w','W','f','r','s','a','q']):

				# Attack Move (1 turn)
				if move == 'l': self.player.atk_mv(map, (x + 1, y))
				elif move == 'k': self.player.atk_mv(map, (x, y - 1))
				elif move == 'j': self.player.atk_mv(map, (x, y + 1))
				elif move == 'h': self.player.atk_mv(map, (x - 1, y))
				elif move == 'y': self.player.atk_mv(map, (x - 1, y - 1))
				elif move == 'u': self.player.atk_mv(map, (x + 1, y - 1))
				elif move == 'b': self.player.atk_mv(map, (x - 1, y + 1))
				elif move == 'n': self.player.atk_mv(map, (x + 1, y + 1))
				# Run Right
				elif move == 'L':
					if len(game.units) == 1:
						while map.can_move((self.player.loc[0] + 1, self.player.loc[1])):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1])) != '+':
								action('l')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
						return
				# Run Up
				elif move == 'K':
					if len(game.units) == 1:
						while map.can_move((self.player.loc[0], self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0], self.player.loc[1] - 1)) != '+':
								action('k')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
						return
				# Run Down
				elif move == 'J':
					if len(game.units) == 1:
						while map.can_move((self.player.loc[0], self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0], self.player.loc[1] + 1)) != '+':
								action('j')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
						return
				# Run Left
				elif move == 'H':
					if len(game.units) == 1:
						while map.can_move((self.player.loc[0] - 1, self.player.loc[1])):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1])) != '+':
								action('h')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
						return
				# Run UL
				elif move == 'Y':
					if len(game.units) == 1:
						while map.can_move((self.player.loc[0] - 1, self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1] - 1)) != '+':
								action('y')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
						return
				# Run UR
				elif move == 'U':
					if len(game.units) == 1:
						while map.can_move((self.player.loc[0] + 1, self.player.loc[1] - 1)):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1] - 1)) != '+':
								action('u')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
						return
				# Run DL
				elif move == 'B':
					if len(game.units) == 1:
						while map.can_move((self.player.loc[0] - 1, self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0] - 1, self.player.loc[1] + 1)) != '+':
								action('b')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
						return
				# Run DR
				elif move == 'N':
					if len(game.units) == 1:
						while map.can_move((self.player.loc[0] + 1, self.player.loc[1] + 1)):
							if map.square_identity((self.player.loc[0] + 1, self.player.loc[1] + 1)) != '+':
								action('n')
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
						return

				# quiver
				elif move == 'q': self.player.quiver()
				# fire
				elif move == 'f': self.player.fire()
				# spell
				elif move == 's': 
					if len(self.player.spells) > 0: self.player.spell()
					else:
						game.temp_log.append("You do not know any spells.")
						return
				# ability
				elif move == 'a': 
					if len(self.player.abilities) > 0: self.player.ability()
					else:
						game.temp_log.append("All your abilites are on cooldown.")
						return
				# wield
				elif move == 'w':
					if not self.equip(Weapon): return
				# Wear
				elif move == 'W':
					if not self.equip(Armor): return
				# Investigate
				elif move == ',':
					if not self.investigate(): return
				# Wait
				elif move == '.':
					self.player.time += self.player.mspeed
					self.check_passives(self.player)
				# rest
				elif move == 'r':
					if len(game.units) == 1:
						while self.player.hp < self.player.maxhp or self.player.mana < self.player.maxmana: action('.')
						game.temp_log.append("You feel well-rested")
						self.player.time = 0
					else:
						game.temp_log.append("There are enemies nearby!")
						return


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
		carrying = []
		for weap in self.player.wielding:
			if weap.hands != 0: carrying.append(weap)

		for item in self.player.wielding:
			if type(item) != Armor:
				if item.hands != 0:

					# Hand String Formulation
					hands = item.hands
					if self.player.race == "Hill Troll":
						if item.hands >= 3: hands = 2
						elif item.hands == 2: hands = 1			

					if item.brand is None:
						if item.enchantment >= 0:
							weapon_string += " +" + str(item.enchantment) + " " + item.name + " (" + str(hands) + "h)"
						else:
							weapon_string += " " + str(item.enchantment) + " " + item.name + " (" + str(hands) + "h)"
					else:
						if item.enchantment >= 0:
							weapon_string += " " + item.brand + " +" + str(item.enchantment) + " " + item.name + " (" + str(hands) + "h)"
						else:
							weapon_string += " " + item.brand + " " + str(item.enchantment) + " " + item.name + " (" + str(hands) + "h)"

		# Wielding Nothing
		if weapon_string == "": weapon_string = " None"

		# Quiver String
		if self.player.quivered is None: quivered_string = " None"
		else:
			if self.player.quivered.brand is None: quivered_string = " " + self.player.quivered.name + " (" + str(self.player.quivered.number) + ")"
			else: quivered_string = " " + self.player.quivered.brand + ' ' + self.player.quivered.name + " (" + str(self.player.quivered.number) + ")"

		# Enchantment Strings
		a_ench = self.player.equipped_armor.enchantment
		if a_ench >= 0: a_ench = '+' + str(a_ench)

		hpspace =   "                 "
		for i in range(len(str(self.player.hp))):
			hpspace = hpspace[:-2]

		manaspace = "                 "
		for i in range(len(str(self.player.mana))):
			manaspace = manaspace[:-2]

		print("Level " + str(self.player.level) + " " + self.player.race)
		print("HP    " + str(self.player.hp)   + "/" + str(self.player.maxhp)   + hpspace + "Wielding:" + weapon_string + "             Armor: " + str(a_ench) + ' ' + self.player.equipped_armor.name)
		print("MANA  " + str(self.player.mana) + "/" + str(self.player.maxmana) + manaspace + "Quivered:" + quivered_string)

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
					if wielding == "" and item.hands > 0: wielding += item.name
					elif item.hands > 0: wielding += (", a " + item.name)

				if len(wielding) == 0: game.game_log.append("You see a " + unit.name + ", wearing " + unit.equipped_armor.name)
				else: game.game_log.append("You see a " + unit.name + ", wearing " + unit.equipped_armor.name + ", wielding a " + wielding)
				self.seen.add(unit)


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

		# Reset the terminal
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

		if len(drops) == 0:
			self.game_log.append("There is nothing here to interact with.")
			return False

		# One item on the ground
		if len(drops) == 1 and not opened_a_chest:
			self.player.pick_up(drops[0])
			return True

		# Nothing on the ground
		elif len(drops) == 0:
			game.temp_log.append("There is nothing here to interact with.")
			return False

		# Multiple ground items
		else:
			return self.ground_inventory(drops)


	def equip(self, item_type):
		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		item_array = []
		for item in self.player.inventory:
			if type(item) == item_type: item_array.append(item)
			if item_type == Weapon and type(item) == Shield: item_array.append(item)

		# Empty Case
		if len(item_array) == 0:
			game.temp_log.append("Your inventory is empty!")
			return

		else:
			print("=======================================================================================")
			print("                                                                     ")
			for i in range(len(item_array)):

				unit = item_array[i]

				if unit.brand is not None: print( item_order[i] + " - " + unit.brand + " +" + str(unit.enchantment) + ' ' + unit.name)
				else: print( item_order[i] + " - +" + str(unit.enchantment) + ' ' + unit.name)
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
						else: print("That is not a valid input")
				if not valid: return
			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

				

	def ground_inventory(self, drops):
		item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

		print("=======================================================================================")
		print("                                                                     ")
		for i in range(len(drops)):

			unit = drops[i]

			if type(unit) == Ammo:

				if unit.brand is not None: print( item_order[i] + " - " + unit.brand + ' ' + unit.name + ' (' + str(unit.number) + ')')
				else: print( item_order[i] + " - " + unit.name + ' (' + str(unit.number) + ')')

			else:

				if unit.brand is not None:
					print( item_order[i] + " - " + unit.brand + " +" + str(unit.enchantment) + ' ' + unit.name)
				else:
					# Positive Encahntment
					if unit.enchantment >= 0: print( item_order[i] + " - +" + str(unit.enchantment) + ' ' + unit.name)
					else: print( item_order[i] + " - " + str(unit.enchantment) + ' ' + unit.name)
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
		print("Pick up which item?")
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
		

		# Reset the terminal:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

		return True if valid else False





	def check_passives(self, unit):

		for passive in unit.passives:

			name = passive[0]
			count = passive[1]

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

			# Decrement Count
			passive[1] -= 1
			if passive[1] <= 0:

				# Manage drained
				if name == "drained": unit.dex += Brands.dict["drained"]["dex_loss"]

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



		# Check if unit is still alive
		if unit.hp <= 0 and type(unit) != Player:
			game.game_log.append("The " + unit.name + " dies from its wounds!")
			game.units.remove(unit)

			if type(unit) == Monster:

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







game = Game()
# try:
game.run()
# except:
# 	pass








