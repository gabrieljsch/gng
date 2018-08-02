from maps import Maps
import ai

from bestiary import Monsters, Bands
from codex import Weapons, Ammos, Brands, Armors, Shields, Tomes
from spells import Spells
from character import CharacterInfo
from descriptions import Descriptions, Colors

from random import randint, shuffle
from copy import deepcopy

import sys, os
import termios, fcntl
import select
from sty import fg, bg, ef, rs



'''
TODO:

- Legendary that chops arrows from air
- Legendary returning throwing axe
- Nerf dual-wielding
- Lances
- finish unique enemies in strike
- enemies casting buffs on already-buffed bois
- enemy behavior types
- Finish class tomes, leech life
- Felltron ability
- Buff ability template
'''



def color(statement, color):
	fg.color = color
	print(fg.color + str(statement) + fg.rs)



class Player():

	def __init__(self, statsheet, innate_equipment, game):

		# Initialize Location, Time
		self.loc, self.range_from_player, self.time = (2,5), 0, 0

		# Initialize Representation
		self.rep, self.name, self.info, self.passives, self.race, self.pclass  = '@', "you", ('you','your'), [], None, game.pclass

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.reg = statsheet[:7]

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = statsheet[7]

		# Initiaize Color
		self.color = statsheet[8]

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

		# Mount
		self.rider, self.mount = None, None

		# Inventory, Spells
		self.inventory, self.spells, self.abilities, self.cooldowns = [], [], [], []

		# Initialze Equipment
		self.wielding, self.hands, self.total_hands, self.quivered = [], 2, 2, None

		# Manage God-Cleaver Passive
		self.god_cleaver_hits = 0

		# Apply Racial Passives
		self.skill_points = 0
		self.innate_ac = 0
		self.traits = []
		self.racial_bonuses(game)

		# Innate Equipment
		for equipment in innate_equipment:
			if equipment in Weapons.array: weap = self.give_weapon(equipment)
			elif equipment[0] in Spells.spells and equipment[1]: self.abilities.append(equipment[0])
			elif equipment[0] in Spells.spells and not equipment[1]: self.spells.append(equipment[0])

		# Class Equipment
		for item in CharacterInfo.race_starting_equipment[game.race][CharacterInfo.class_list.index(game.pclass)]:
			if item in Ammos.array:
				data = Ammos.array[item]
				if data[2] in Ammos.thrown_amclasses: number = 6
				else: number = 20
				self.inventory.append(Ammo(item,data[0],data[1],data[2], number,data[3],None))
				self.quivered = self.inventory[-1]
			elif item in Weapons.array: self.give_weapon(item)
			elif item in Shields.array:
				data = Shields.array[item]
				try: brand = data[6]
				except: brand = None
				self.wielding.append(Shield(item,data[0],data[1],data[2],data[3],data[4],data[5],None,brand))
				self.hands -= data[2]
			elif item in Armors.array:
				data = Armors.array[item]
				try: brand = data[6]
				except: brand = None
				self.equipped_armor = Armor(item,data[0],data[1],data[2],data[3],data[4],data[5],None,brand)
			elif type(item) == tuple:
				if item[1]: self.abilities.append(item[0])
				else: self.spells.append(item[0])


		# Give Class Tome
		if game.pclass == "Warrior":
			tome = 'Tome of the Warrior'
		elif game.pclass == "Paladin":
			tome = 'Tome of the Paladin'
		elif game.pclass == "Ranger":
			tome = 'Tome of the Ranger'
		elif game.pclass == "Rogue":
			tome = 'Tome of the Rogue'
		elif game.pclass == "Mage":
			tome = 'Tome of the Mage'
		elif game.pclass == "Warlock":
			tome = 'Tome of the Warlock'
		data = Tomes.array[tome]
		self.inventory.append(Tome(data[0],tome,'_',data[2], data[1], None))

		# Initialize Level, XP
		self.level, self.xp, self.xp_levels = 1, 0, 12
		

		

	def read(self,tome):
		skillnums = '123456789'

		spaces = [i for i in range(24 - (len(tome.spells)))]

		repeat = True
		while repeat:
			print("=======================================================================================")
			for space in spaces: print("")
			print("")
			print("")
			print("")
			print("Available Skills")
			print("=======================================================================================")
			print("")
			repeat = False
			for spell in tome.spells:
				print(skillnums[tome.spells.index(spell)] + ') '+ spell[0])
				print("")

			decision = rinput("Which skill will you investigate?")

			if decision in skillnums and skillnums.index(decision) < len(tome.spells):
				skill = tome.spells[skillnums.index(decision)][0]
				cost = tome.spells[skillnums.index(decision)][1]
				stype = tome.spells[skillnums.index(decision)][2]
				print("=======================================================================================")
				print("")
				print("")
				print("")
				print(skill.upper() + "  ("+stype+") : " + str(cost) + " points")
				print("")
				print(Descriptions.skill[skill][0])
				print("")

				if skill in self.traits or skill in self.abilities or skill in self.spells:
					print("You already know this skill.")

					decision = rinput("(G)o back")

					if decision.lower() == 'g':
						repeat = True
				else:
					decision = rinput("You have " + str(self.skill_points) + " skill points. (B)uy or (G)o back?")

					if decision.lower() == 'g':
						repeat = True
					elif decision.lower() == 'b':
						if self.skill_points < cost:
							print("You do not have enough points for that.")
							spaces.pop()
							repeat = True
						else:
							if stype == 'trait':
								self.traits.append(skill)
							elif stype == 'spell':
								self.spells.append(skill)
							elif stype == 'ability':
								self.abilities.append(skill)
							self.skill_points -= cost

							game.game_log.append("You learn " + skill + "!")




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
		if game.race == 'Black Orc':
			self.innate_ac += 1
		if game.race == 'Dragonborn':
			self.innate_ac += 2
		if game.race == 'Felltron':
			self.innate_ac += 2
		if game.race == 'Hill Troll':
			self.innate_ac += 1
			self.hands, self.total_hands = 4, 4
		if game.race == "Terran":
			self.skill_points += 2


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

					try: 
						if Weapons.array[ammo[game.item_order.index(decision)].sname][3] > self.total_hands:
							game.temp_log.append("That item is too heavy for you to quiver.")
							return
					except: pass

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
		kraken = True if [weap for weap in self.wielding if weap.sname == 'Kraken'] else False

		# Manage Kraken 1
		if kraken: thrown = True


		if self.quivered is not None:

			# Manage throwing Weapons
			if self.quivered.wclass in Ammos.thrown_amclasses:
				thrown = True
				# Create Throwing platform
				item = self.give_weapon(self.quivered.sname)



		for item in self.wielding:

			# Ranged Projectile Thrower
			if item.wclass in Weapons.ranged_wclasses or item.wclass in Ammos.thrown_amclasses or item.sname == 'Kraken':


				if item.sname == 'Kraken': item.range = 8

				# Check for quiver
				elif self.quivered is None:
					game.temp_log.append("You do not have the correct ammo type quivered.")
					return
				# Wrong ammo type
				elif item.wclass in Weapons.ranged_wclasses and self.quivered.wclass not in Ammos.projectile[item.wclass]:
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

						# Attack
						if item.sname == 'Kraken': item.thrown = True
						item.strike(self, unit)

						# Manage Tempest
						if item.sname == "Tempest":
							units_in_range.remove(unit)
							others = 2
							while len(units_in_range) != 0 and others > 0:
								ounit = units_in_range[d(len(units_in_range)) - 1]
								item.strike(self, ounit)
								units_in_range.remove(ounit)
								others -= 1

						# Well-being
						try: self.well_being_statement(unit, self, item, game)
						except: pass

						# Remove throwing weapon
						if thrown and not kraken: self.wielding.pop()

						# Remove Ammo
						if not kraken:
							self.quivered.number -= 1
							if self.quivered.number == 0:
								self.inventory.remove(self.quivered)
								self.quivered = None
						return

					else:
						game.temp_log.append("That is not a valid input")
						# Remove throwing weapon
						
						if thrown and not kraken: self.wielding.pop()
						return

				else:
					game.temp_log.append("There are no targets in range!")

					# Remove throwing weapon
					if thrown and not kraken: self.wielding.pop()
					return

		game.temp_log.append("You are not wielding a ranged weapon!")
		# Remove throwing weapon
		if thrown and not kraken: self.wielding.pop()


	def well_being_statement(self, enemy, attacker, means, game, estatus = True):

		# If enemy is defeated
		if enemy.hp <= 0:

			# Remove enemy
			game.units.remove(enemy)
			if enemy in game.allies: game.allies.remove(enemy)

			# Check for Indomibable
			for name, count in enemy.passives:
				if name == 'indominable':
					enemy.hp = 1
					game.game_log.append("The "  + str(enemy.name) + " refuses to die!")
					return

			# If kill with weapon
			legendary = False
			if type(means) == Weapon:

				kill_weapon = means

				legendary = True if kill_weapon.legendary else False
				means = means.name

			# Flavor Text
			verb = 'slay' if attacker.name == 'you' else 'slays'
			poss = " " + attacker.info[1] if not legendary else ""
			game.game_log.append( attacker.info[0][0].upper() + attacker.info[0][1:] + " " + verb + " the "  + str(enemy.name) + " with" + poss + " " + means + "!")


			# Mounts
			if enemy.rider is not None: enemy.rider.mount = None
			elif enemy.mount is not None: enemy.mount.unit.rider = None


			# Add to weapon kill count
			try: 
				kill_weapon.kills += 1

				# Manage Worldshaper
				if kill_weapon.sname == "Worldshaper":
					attacker.mana = min(attacker.maxmana, int(attacker.mana + attacker.mana / 4))
					game.game_log.append(kill_weapon.name + " saps mana from the falling corpse.")

				# Manage Swiftspike
				if kill_weapon.sname == "Swiftspike":
					attacker.mspeed = attacker.mspeed / 4
					# Speed
					# ------------------------
					applied = False
					for passive in attacker.passives:

						if passive[0] == "hastened":
							passive[1] = 5
							applied = True
							break

					if not applied: attacker.passives.append(["hastened", 5])
					# ------------------------
					game.game_log.append(kill_weapon.name + " grants you a burst of movement speed!")

				# Manage Soulreaper
				if kill_weapon.sname == "Soulreaper":

					kill_prog = [20,50,90,140,200,300]
					if kill_weapon.kills in kill_prog:
						kill_weapon.damage += 1
						if kill_weapon.kills == kill_prog[-1]:
							game.game_log.append(kill_weapon.name + " is sated.")
							kill_weapon.brand = 'possessed'
						else: game.game_log.append(kill_weapon.name + " demands more blood.")

				# Manage the Talons of Belial
				if kill_weapon.sname == "the Talons of Belial":

					# Fear Radius
					spaces, affected = set([]), []
					for x in range(-3,4):
						for y in range(-3,4):
							if enemy.loc[0] + x >= 0 and enemy.loc[1] + y >= 0: spaces.add((enemy.loc[0] + x, enemy.loc[1] + y))
					# Find units affected
					for unit in game.units[1:]:
						if unit.loc in spaces and unit != attacker and unit.tier < enemy.tier:
							affected.append(unit)

					if len(affected) != 0:
						for unit in affected:
							# ------------------------
							applied = False
							for passive in unit.passives:

								if passive[0] == "terrified":
									passive[1] = 5
									applied = True
									break

							if not applied: unit.passives.append(["terrified", 5])
							# ------------------------
						ename = enemy.name if enemy.namestring in Monsters.uniques else "the " + enemy.name
						game.game_log.append("The shredded remains of " + ename +  " left by " + kill_weapon.name + " make its underlings flee in terror!")
			except: pass

			# Ooze Passive
			if 'split' in enemy.spells: Spells.spells["split"][0]("split", enemy, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler)


			# Drop Loot
			enemy.drop_booty()

			# XP Gain
			self.xp += enemy.xp + int(d(self.cha) / 2)
			return

		if estatus:

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

			if type == "spell": print(str(game.item_order[i]) + " - " + array[i] + " (" + str(Spells.spells[array[i]][1]) + " mana)")
			else: print(str(game.item_order[i]) + " - " + array[i]+ " (" + str(Spells.spells[array[i]][1] * 3) + " turns)")

		print("                                                                     ")
		print("=======================================================================================")

		# Controller
		print("")
		if type == "spell": decision = rinput("Use which spell?")
		else: decision = rinput("Use which ability?")

		# Valid Spell
		if decision in game.item_order and game.item_order.index(decision) < len(array):
			spell, spell_name = Spells.spells[array[game.item_order.index(decision)]][0], array[game.item_order.index(decision)]
		else:
			game.temp_log.append("That is not a valid input")
			return

		if type == "spell":

			# Check Mana
			kainspact = False
			if self.mana < Spells.spells[spell_name][1]:

				# Manage Kain's Pact
				if self.equipped_armor.sname != "Kain's Pact": 
					game.temp_log.append("You don't have enough mana to cast that.")
					return
				else:
					print(self.equipped_armor.name + " draws power from your health.")
					kainspact = True

		# Self-cast
		if not Spells.spells[spell_name][3]:
			print(spell_name)
			if type == "spell":
				if spell(spell_name, self, self, game, Maps.rooms[game.map.map][0], game.map.room_filler):
					self.time += Spells.spells[spell_name][2]
					if kainspact:self.hp -= Spells.spells[spell_name][1]
					else: self.mana -= Spells.spells[spell_name][1]
			else:
				if spell(spell_name, self, self, game, Maps.rooms[game.map.map][0], game.map.room_filler, True):
					self.time += Spells.spells[spell_name][2]
					self.cooldowns.append( [spell_name, Spells.spells[spell_name][1] * 3] )
					self.abilities.remove(spell_name)
		

		# There is a target
		else:
			# Get units in range
			units_in_range = []
			for unit in game.units[1:]:
				los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
				if los is None: continue
				if Spells.spells[spell_name][4]:
					if len(los) - 1 <= Spells.spells[spell_name][5]: units_in_range.append(unit)
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
							self.time += Spells.spells[spell_name][2]
							if kainspact:self.hp -= Spells.spells[spell_name][1]
							else: self.mana -= Spells.spells[spell_name][1]
							game.game_log.append("The " + unit.name + " resists your " + spell_name + "!")

						elif spell(spell_name, self, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler):
							if kainspact:self.hp -= Spells.spells[spell_name][1]
							else: self.mana -= Spells.spells[spell_name][1]
							self.time += Spells.spells[spell_name][2]
					else:
						if spell(spell_name, self, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler, True):
							self.time += Spells.spells[spell_name][2]
							self.cooldowns.append( [spell_name, Spells.spells[spell_name][1] * 3] )
							self.abilities.remove(spell_name)

				else:
					game.temp_log.append("That is not a valid input")
					return
			else:
				game.temp_log.append("There are no targets in range!")
				return

		# Manage Longfang
		if type == "spell":
			for weapon in self.wielding:
				if weapon.sname == "Longfang":
					for school, spells in Spells.spell_schools.items():
						if spell_name in spells:
							if school in Spells.school_brands:
								weapon.passives = [[Spells.school_brands[school] , 1]]
								weapon.brand = Spells.school_brands[school]
								fg.bcolor = Colors.array[Brands.colors[weapon.brand]]
								game.game_log.append(weapon.name + " absorbs the power of your spell and becomes " + fg.bcolor + weapon.brand + fg.rs + "!")
								break

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
		while self.xp >= self.xp_levels:

			# Increment Level
			self.level += 1
			self.skill_points += 1
			try:
				for band in Bands.dicto[self.level]:
					try: game.bands.remove(band)
					except: game.bands.append(band)
			except: pass

			# Gain HP/mana
			bonushp = d(self.con)
			self.hp += 2 + bonushp
			self.maxhp += 2 + bonushp
			self.mana += 2
			self.maxmana += 2

			# Racial level-ups
			self.racial_level_bonuses()


			print("You've leveled up to level " + str(self.level) + "!")
			game.game_log.append("You've leveled up to level " + str(self.level) + "!")
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
		if type(item) == Weapon or type(item) == Shield or type(item) == Tome:

			# Carrying
			carrying = [thing  for thing in self.wielding if thing.hands > 0]

			# Ranged weapons / Gauntlets / Claw Gauntlet  require all hands
			if item.wclass in Weapons.ranged_wclasses or item.wclass in ['gauntlets','claw gauntlets']:
				# Remove current weapons
				for weap in carrying:
					self.wielding.remove(weap)
					self.inventory.append(weap)

				# Wield Weapon
				self.hands = 0
				self.wielding.append(item)
				self.inventory.remove(item)
				if item.legendary: game.game_log.append("You draw " + item.name + "!")
				else: game.game_log.append("You draw your " + item.name + ".")

				self.time += self.mspeed

			# Not enough total hands
			elif item.hands > self.total_hands or item.hands > 1 and item.wclass != 'bastard sword' and self.race in ['Gnome','Hobbit']:
				game.temp_log.append("You cannot wield that weapon!")

			# Not enough FREE Hands
			elif self.hands < item.hands or len(carrying) == 2:

				# Already carrying something
				if len(carrying) == 2 and item.hands < self.total_hands:

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
						if ditem.legendary: game.game_log.append("You put away " + ditem.name + '.')
						else: game.game_log.append("You put away the " + ditem.name + '.')
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
				if item.legendary: game.game_log.append("You draw " + item.name + "!")
				else: game.game_log.append("You draw your " + item.name + ".")

			# Enough free hands
			else:
				# Wield item
				self.wielding.append(item)
				self.inventory.remove(item)
				self.hands -= item.hands
				if item.legendary: game.game_log.append("You draw " + item.name + "!")
				else: game.game_log.append("You draw your " + item.name + ".")


			# Manage Martial Draw
			if 'martial draw' in self.traits and type(item) == Weapon:
				x, y = self.loc
				squares = []
				for i in range(3):
					for j in range(3):
						squares.append([x - 1 + i, y - 1 + j])
				targets = []
				for unit in game.units[1:]:
					if unit in game.allies: continue
					if [unit.loc[0], unit.loc[1]] in squares:
						targets.append(unit)

				if len(targets) != 0:
					target = targets[d(len(targets)) - 1]
					self.wielding[-1].strike(self, target)



		# Equip Armor
		elif type(item) == Armor:
			self.inventory.append(self.equipped_armor)
			self.equipped_armor = item
			self.inventory.remove(item)
			if item.legendary: game.game_log.append("You put on " + item.name + "!")
			else: game.game_log.append("You put on your " + item.name + "!")

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
		if ditem.legendary: game.game_log.append("You put away " + ditem.name + '.')
		else: game.game_log.append("You put away the " + ditem.name + '.')
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
				weaps,shields,armors,ammos, tomes = [],[],[],[], []
				for item in items:
					if type(item) == Ammo: ammos.append(item)
					elif type(item) == Weapon: weaps.append(item)
					elif type(item) == Shield: shields.append(item)
					elif type(item) == Armor: armors.append(item)
					elif type(item) == Tome: tomes.append(item)
				combined = weaps + shields + armors + ammos + tomes
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
				if len(tomes) != 0: print("Tomes")
				for i in range(len(tomes)):
					print(game.item_order[j] + " - " + tomes[i].string())
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
				# Tome
				elif type(ditem) == Tome:
					if ditem in self.wielding:
						decision = rinput("(S)tow, (R)ead, (D)rop, or (G)o back?")
						if decision.lower() == 's': self.stash(ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						elif decision.lower() == 'r': self.read(ditem)
						else: game.temp_log.append("That is not a valid option.")
					else:
						decision = rinput("(W)ield, (R)ead, (D)rop, or (G)o back?")
						if decision.lower() == 'w': self.wield(Weapon,ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						elif decision.lower() == 'r': self.read(ditem)
						else: game.temp_log.append("That is not a valid option.")
				# Armor
				elif type(ditem) == Armor:
					if ditem == self.equipped_armor:
						print("You are currently wearing this armor.")
						decision = rinput("(G)o back?")
						if decision.lower() == 'g': go_back = True
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
				if type(thing) == Ammo and thing.sname == item.sname and thing.brand == item.brand:
					thing.number += item.number
					already_in = True
					break

		game.items.remove(item)
		if not already_in: self.inventory.append(item)
		if type(item) == Ammo:
			if item.number > 1: game.game_log.append("You pick up " + str(item.number) + ' ' + item.name + "s.")
			else: game.game_log.append("You pick up the " + item.name + ".")
		elif item.legendary:
			game.game_log.append("You pick up " + item.name + "!")
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
		try:
			article = "" if item.legendary else "the "
		except: article = "the "
		try: game.game_log.append("You drop " + article + str(item.number) + ' ' + item.name + "s")	
		except: game.game_log.append("You drop " + article + item.name)
		self.time += self.mspeed


	def give_weapon(self, weapon):
		data = Weapons.array[weapon]

		# Manage Brand + Probability
		try: brand = data[8]
		except: brand = None
		try: prob = data[9]
		except: prob = None

		self.hands -= data[3]

		# Create Weapon Object
		if data[2] in Weapons.ranged_wclasses and data[3] > 0:
			self.inventory.append(Weapon(weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],None, brand, prob))
			return self.inventory[-1]
		else:
 			self.wielding.append(Weapon(weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], None, brand, prob))
 			return self.wielding[-1]


	def calc_AC(self):
		return d(int(max(1, (self.equipped_armor.armor_rating + self.equipped_armor.enchantment) / 2))) + int((self.equipped_armor.armor_rating + self.equipped_armor.enchantment) / 2)  + self.innate_ac


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
				self.time += 1
				return '+'
			else:
				game.map.change_room(map.adjacent[coords])
				self.time += 1
				return '+'

		# Check if square is occupied for ATTACK
		for unit in game.units:

			# Make sure it's a monster and adjacent to it
			if coords == unit.loc and type(unit) == Monster:

				# Equip fists
				if len(carrying) == 0 or (len(carrying) == 1 and self.race == "Hill Troll" and weaps[-1].wclass not in ["gauntlets","claw gauntlets"] or type(carrying[-1]) == Shield and len(carrying) == 1):
					if len(carrying) == 0 and self.race == "Hill Troll":
						fists = self.give_weapon('fist smash')
						weaps.append(fists)
					else:
						fists = self.give_weapon('fist')
						weaps.append(fists)

				# Attack with each weapon
				ranged = True
				for item in weaps:
					ranged = False
					item.strike(self, unit)
					if unit.hp <= 0: break

				# Manage Wraithform
				for passive in self.passives:
					if passive[0] == 'wraithform':
						self.passives.remove(passive)
						game.game_log.append("You break from the material plane!")

				# Not wielding melee weapon
				if ranged:
					game.temp_log.append("You are not wielding any melee weapons.")
					return

				# Enemy Well-being Statement
				try: self.well_being_statement(unit, self, item, game)
				except: pass
				

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

		# Manage Immobile
		for name, count in self.passives:
			if name == 'immobile':
				game.temp_log.append("You can't move!")
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


		# Manage Furious Charge
		if "furious charge" in self.traits:
			for unit in game.units[1:]:
				if unit.loc == (self.loc[0] - 2 * (self.loc[0] - coords[0]), self.loc[1] - 2 * (self.loc[1] - coords[1])):
					for weapon in weaps: weapon.strike(self, unit)
					break

		# move unit
		self.loc = coords
		self.time += self.mspeed

	


class Monster():

	def __init__(self,      name, char, color, etype, tier,    con, st, dex, int, cha, mspeed, xp,   resistances,  pot_weapons, pot_armor,  loc, other_items = None):

		# Initialize Representation
		self.rep, self.color, self.etype, self.tier = char, color, etype, tier

		# Mount?
		self.mount, self.rider = None, None

		fg.color = Colors.array[self.color]
		self.name, self.namestring = fg.color + name + fg.rs, name
		self.info = ('the ' + self.name, 'its')

		# Initialize Health
		bonushp = md(6,self.tier)
		self.maxhp = 5 * con + bonushp
		self.hp = 5 * con + bonushp

		# Initialize Mana
		self.mana, self.maxmana = 5 * int + self.tier, 5 * int + self.tier

		# Coordinates
		self.loc, self.time = loc, 1
		self.passives, self.spells, self.traits = [], [], []

		# Initialize Range
		self.range_from_player = 100

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.xp = con, st, dex, int, cha, mspeed, xp

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = resistances

		# Monster's Equipment
		self.wielding , self.other_items, self.quivered, self.inventory = [], other_items, None, []

		# Manage God-Cleaver Passive
		self.god_cleaver_hits = 0

		# Give innate weapons / shields
		if other_items is not None:
			for item in other_items:
				if item in Ammos.array: self.give_ammo(item)
				elif item in Weapons.array: self.give_weapon(item)
				elif item in Shields.array: self.give_shield(item)
				elif item in Spells.spells: self.spells.append(item)
				elif item in Tomes.array: self.give_tome(item)
				elif item in Monsters.array:
					ally = True if self in game.allies else False
					self.mount = Mount(game.map.room_filler,self,item,ally)
					self.mount.unit.rider = self
				else: self.traits.append(item)

		# Give Weapon and Armor
		items = pot_weapons[d(len(pot_weapons)) - 1]
		if type(items) != list: items = [items]
		for item in items:
			if item in Weapons.array: self.give_weapon(item)
			elif item in Shields.array: self.give_shield(item)
			elif item in Tomes.array: self.give_tome(item)
		self.give_armor( pot_armor[  d(len(pot_armor)) - 1])

	def calc_resistances(self):
		return [self.frostr + self.equipped_armor.frostr, self.firer + self.equipped_armor.firer, self.poisonr + self.equipped_armor.poisonr, self.acidr + self.equipped_armor.acidr, self.shockr + self.equipped_armor.shockr, self.expr + self.equipped_armor.expr]

	def calc_mdamage(self):
		sd = 0
		for weapon in self.wielding:sd += weapon.mdamage
		return sd

	def calc_AC(self):
		return d(int(max(1, (self.equipped_armor.armor_rating + self.equipped_armor.enchantment) / 2))) + int((self.equipped_armor.armor_rating + self.equipped_armor.enchantment) / 2)

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
					if item.sname == self.quivered.sname and item.brand == self.quivered.brand:
						item.number += self.quivered.number
						return
			self.quivered.loc = self.loc
			game.items.append(self.quivered)


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
		self.wielding.append(Weapon(weapon, data[0], data[1], data[2], data[3], spawned_enchantment, data[5], data[6], data[7], None, brand, prob))

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
		self.wielding.append(Shield(shield, data[0], data[1], data[2], data[3], data[4],spawned_enchantment, None, brand))

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


	def turn(self):

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
						item.trip()

				self.time += self.mspeed
				return


		# Ally Unit
		if self in game.allies:
			enemy, mini = None, 100
			for unit in game.units:
				if unit in game.allies: continue
				los = ai.los(self.loc, unit.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:
					if type(unit) == Player: self.range_from_player = len(los)
					elif len(los) < mini:
						enemy, mini, minlos = unit, len(los), los

			# No enemies in room
			if enemy == None:
				ai.move_towards(self, game.player, game.map)
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
					if type(unit) == Player: self.range_from_player = len(los)
					if len(los) <= mini:
						enemy, mini, minlos = unit, len(los), los


		melee_attacked = False

		# MAGIC!!
		if len(self.spells) > 0:

			# Chance to use spells
			if d(10) + min(self.int, 7) >= 12:

				# los = ai.los(self.loc, enemy.loc, Maps.rooms[game.map.map][0], game )
				if minlos is not None:

					# # Shift around spells
					# if len(self.spells) >= 2: shuffle(self.spells)

					# Zap with spells
					for spell in self.spells:

						# Can't cast These 
						if spell == 'split': break

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
										if enemy.name == 'you': game.game_log.append("You resist the " + spell + " from the " + self.name + "!")
										else: game.game_log.append(enemy.name + " resists the " + spell + " from the " + self.name + "!")
										return

									elif spell_fun(spell, self, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler):
										self.time += Spells.spells[spell][2]
										self.mana -= Spells.spells[spell][1]

										if self.mount is not None:
											self.mount.unit.loc = self.loc
										if self.rider is not None:
											self.rider.loc = self.loc
							# No target
							else:
								if spell_fun(spell, self, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler):
									self.time += Spells.spells[spell][2]
									self.mana -= Spells.spells[spell][1]

									if self.mount is not None:
										self.mount.unit.loc = self.loc
									if self.rider is not None:
										self.rider.loc = self.loc

							# Manage Longfang 2
							if type == "spell":
								for weapon in self.wielding:
									if weapon.sname == "Longfang":
										for school, spells in Spells.spell_schools.items():
											if spell_name in spells:
												if school in Spells.school_brands:
													weapon.passives = [[Spells.school_brands[school] , 1]]
													weapon.brand = Spells.school_brands[school]
													fg.bcolor = Colors.array[Brands.colors[weapon.brand]]
													game.game_log.append(weapon.name + " absorbs the power of " + self.info[0] + " spell and becomes " + fg.bcolor + weapon.brand + fg.rs + "!")
													break



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
				if self in game.allies:
					# Enemy Well-being Statement
					try: game.player.well_being_statement(enemy, self, item, game)
					except: pass

			self.time += maxas
			melee_attacked = True

		# Add thrown weapon platform
		thrown = False
		if self.quivered is not None:
			if self.quivered.wclass in Ammos.thrown_amclasses:
				thrown = True
				item = self.give_weapon(self.quivered.sname)

		# Make Ranged attacks
		for item in self.wielding:
			if item.wclass in Weapons.ranged_wclasses or item.wclass in Ammos.thrown_amclasses:

				if self.quivered is not None or item.hands == 0:

					if item.hands > 0 and melee_attacked:
						if thrown: self.wielding.pop()
						return

					# los = ai.los(self.loc, enemy.loc, Maps.rooms[game.map.map][0], game )
					if minlos is not None:

						# Ranged range
						if mini <= (2 * item.damage  + item.to_hit):
							item.strike(self, enemy)
							if self in game.allies:
								# Enemy Well-being Statement
								try: game.player.well_being_statement(enemy, self, item, game)
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


		if not melee_attacked:

			if not immobile:

				ai.smart_move_towards(self, enemy, game)

				# Check for Traps
				for item in game.items:
					if type(item) == Trap and item.loc == self.loc:
						item.trip()

				# Manage Furious Charge (enemies)
				if "furious charge" in self.traits:
					if self in game.allies:
						for unit in game.units:
							if unit in game.allies: continue
							if unit.loc == (self.loc[0] - 2 * (self.loc[0] - coords[0]), self.loc[1] - 2 * (self.loc[1] - coords[1])):
								for weapon in weaps: weapon.strike(self, unit, False)
								break
					else:
						for unit in game.allies:
							if unit.loc == (self.loc[0] - 2 * (self.loc[0] - unit.loc[0]), self.loc[1] - 2 * (self.loc[1] - unit.loc[1])):
								for weapon in weaps: weapon.strike(self, unit, False)
								break

			self.time += self.mspeed

			if self.mount is not None:
				self.mount.unit.loc = self.loc
			if self.rider is not None:
				self.rider.loc = self.loc



class Weapon():

	def __init__(self,  name, rep, color, wclass, hands, enchantment, damage, to_hit, speed,   loc, brand = None, probability = None):

		# Initialize Weapon Stats
		self.rep, self.color, self.wclass, self.hands, self.enchantment, self.damage, self.to_hit, self.speed, self.loc, self.brand, self.origbrand, self.probability = rep, color, wclass, hands, enchantment, damage, to_hit, speed, loc, brand, brand, probability

		# Initialize Passives, kills
		self.passives, self.kills = [], 0

		fg.color = Colors.array[self.color]
		self.name, self.sname= fg.color + name + fg.rs, name

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

		# Legendary
		if self.sname in Weapons.legendaries:
			self.legendary = True
			try: game.legendaries_to_spawn.remove(self.sname)
			except: pass
		else:
			self.legendary = False

		# Manage Kraken 5
		self.thrown = False


	def details(self):

		if self.to_hit >= 0: thit = '+' + str(self.to_hit)
		else: thit = str(self.to_hit)

		print(self.string(),' (' + self.wclass + ')')
		print("")
		print("This weapon is " + str(self.hands) + "-handed.")
		print("Base damage:", str(self.damage) + ',', "Base to-hit:", thit)
		if self.wclass in Weapons.ranged_wclasses: print("Range:",self.range)
		print("Swing speed:", self.speed)
		print("")

		if self.legendary:
			print(Descriptions.legendary[self.sname])
			print("")

		print(Descriptions.wclass[self.wclass][0])
		if self.wclass[-1] != 's': print("Being a " + self.wclass + ', ' + Descriptions.wclass[self.wclass][1].lower())
		else: print("Being " + self.wclass + ', ' + Descriptions.wclass[self.wclass][1].lower())
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])
		if self.kills != 1: print("You have slain",str(self.kills),"enemies with this weapon.")
		else: print("You have slain",str(self.kills),"enemy with this weapon.")

	def string(self):

		enchstr = "+" + str(self.enchantment) if self.enchantment >= 0 else str(self.enchantment)
		fg.color = Colors.array[self.color]

		if self.brand is not None:
			fg.bcolor = Colors.array[Brands.colors[self.brand]]
			if self.sname[:4].lower() == 'the ': return (fg.color + self.sname[:4] + fg.rs + fg.bcolor + self.brand + fg.rs + " " + enchstr + ' ' + fg.color + self.sname[4:] + fg.rs)
			else: return (fg.bcolor + self.brand + fg.rs + " " + enchstr + ' ' + self.name)
		else:
			if self.sname[:4].lower() == 'the ': return (fg.color + self.sname[:4] + fg.rs + enchstr + ' ' + fg.color + self.sname[4:] + fg.rs)
			else: return (enchstr + ' ' + self.name)

	def strike(self, attacker, enemy, firstswing = True):

			
		if enemy.rider is not None:
			if d(10) >= 7 or self.wclass in ["spear","god spear","pike","lance","polearm","glaive"]:
				self.strike(attacker, enemy.rider, firstswing)
				return


		brand, wclass, to_hit = self.brand, self.wclass, self.to_hit
		if enemy.name == 'you':
			ename = enemy.name
		else:
			ename = "the " + enemy.name
		eposs = 'your' if enemy.name == 'you' else "the " + enemy.name + "'s"

		# Check for enemy statuses
		frozen, marked = False, False
		for passive in enemy.passives:
			if passive[0] == "frozen": frozen = True
			if passive[0] == "marked" and wclass not in ['fist','fists']: marked = True

		# Swing Probability
		if d(100) > (100 - self.probability):

			# Weapon Swing
			if firstswing: self.weapon_type_swing(attacker, enemy)

			# Calc Encumbrance
			self_encumb, enemy_encumb = attacker.equipped_armor.encumbrance, enemy.equipped_armor.encumbrance

			for item in attacker.wielding:
				if type(item) == Shield: self_encumb += item.encumbrance
			for item in enemy.wielding:
				if type(item) == Shield: enemy_encumb += item.encumbrance

			# Blessed Iron Passive
			for passive in attacker.passives:
				if passive[0] == "blessed iron":
					if self_encumb > 0: self_encumb = 0
					if to_hit < 0: to_hit = 0
			for passive in enemy.passives:
				if passive[0] == "blessed iron":
					if enemy_encumb > 0: enemy_encumb = 0


			# TO HIT formula / Manage Godfinger
			if (d(100) + (4 * (attacker.dex - enemy.dex) ) + (2 * to_hit) + self.enchantment > 40 + 1.5 * (self_encumb - enemy_encumb)) or frozen or self.sname == "Godfinger":

				# Keep projectiles
				if self.hands > 0 and self.wclass in Weapons.ranged_wclasses or self.wclass in Ammos.thrown_amclasses:
					already_in = False
					for item in enemy.inventory:
						if type(item) == Ammo and attacker.quivered.sname == item.sname and attacker.quivered.brand == item.brand:
							item.number += 1
							already_in = True
							break
					# Quivereds are same lol
					if enemy.quivered is not None:
						if attacker.quivered.sname == enemy.quivered.sname and attacker.quivered.brand == enemy.quivered.brand:
							enemy.quivered.number += 1
							already_in = True
					if not already_in: enemy.inventory.append(Ammo(attacker.quivered.sname,attacker.quivered.rep,attacker.quivered.color,attacker.quivered.wclass,1,attacker.quivered.damage,None,attacker.quivered.brand))

				# Shield Block

				# Dagger passive
				if wclass not in ['dagger','knife','scream']:
					for weapon in enemy.wielding:
						if type(weapon) == Shield:
							if d(100) > max(33, 90 - (3 * weapon.armor_rating)):

								# Manage the Gauntlets of Mars
								if self.sname == "the Gauntlets of Mars":
									damage = int(d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )

									# Stun
									# ------------------------
									applied = False
									for passive in enemy.passives:

										if passive[0] == "stunned":
											passive[1] = 1
											applied = True
											break

									if not applied: enemy.passives.append(["stunned", 1])
									# ------------------------

									# Manage runic Armor
									if enemy.equipped_armor.brand == 'runic' and enemy.mana > 0:
										manadam = min(enemy.mana, damage)
										enemy.mana -= manadam
										enemy.hp -= damage - manadam
									else:
										# Resolve Damage
										enemy.hp -= damage

									# Flavor Text
									if type(attacker) == Player: game.game_log.append("You smash through the " + enemy.name + "'s shield with " + self.name + ", dealing " + str(damage) + " damage and " + fg.magenta + "stunning" + fg.rs + " it!")
									else: game.game_log.append("The "   + str(attacker.name) +  " smashes through " + enemy.info[1] + " shield with " + self.name + ", dealing " + str(damage) + " damage and " + fg.magenta + "stunning" + fg.rs + " " + str(enemy.name) + "!")
									return

								# Manage Kraken 3
								if self.sname == "Kraken" and self.thrown:
									self.loc = enemy.loc
									game.items.append(self)
									attacker.wielding.remove(self)
									if attacker.name == 'you': attacker.hands += 1


								# Block Statement
								if type(attacker) == Monster: game.game_log.append("You block the "   + str(attacker.name) + "'s " + self.name + " with your " + weapon.name + "!")
								else:
									if self.legendary: game.game_log.append("The "   + str(enemy.name) +  " blocks " + self.name + " with its " + weapon.name + "!")
									else: game.game_log.append("The "   + str(enemy.name) +  " blocks " + attacker.info[1] + " " + self.name + " with its " + weapon.name + "!")
								return


				# DAMAGE forumla


				# Projectile weapon
				if self.wclass in Weapons.ranged_wclasses and self.hands > 0:
					damage = int(d(self.damage) + d(attacker.quivered.damage) + attacker.dex / 2 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
					brand, wclass = attacker.quivered.brand, attacker.quivered.wclass
				# Thrown Weapon
				elif self.wclass in Ammos.thrown_amclasses and self.hands > 0:
					damage = int(d(self.damage) + d(attacker.quivered.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
					brand, wclass = attacker.quivered.brand, attacker.quivered.wclass
				# Manage Kraken 7
				elif self.sname == 'Kraken' and self.thrown:
					damage = int(d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )
				# Melee weapon
				elif self.sname in Weapons.array:
					# Manage Runic weapon
					if brand == 'runic':damage = int(d(self.damage) + attacker.str / 1.5 + self.enchantment)
					# Manage demon sword
					elif self.wclass in ['demon sword']: damage = int(d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.50 * enemy.calc_AC() ) )
					# Manage scream
					elif self.wclass in ['scream']: damage = int(d(self.damage) + attacker.cha / 1.5 + self.enchantment )
					# REGULAR MELEE HIT
					else: damage = int(d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )

					# Managed Spiked Armor
					if enemy.equipped_armor.brand == 'spiked' and damage > 0 and d(10) > 3: barb_damage = d(max(1, int(1/2 * damage)))

				# Marked passive
				if marked:
					damage = int (self.damage + attacker.str + self.enchantment - ( 0.5 * enemy.calc_AC() ) )
					for passive in enemy.passives:
						if passive[0] == 'marked': enemy.passives.remove(passive)
						break


				# Calc Resistances
				frostr, firer, poisonr, acidr, shockr, expr = enemy.calc_resistances()

				# Manage God-Cleaver 1
				if self.sname == 'God-Cleaver': enemy.god_cleaver_hits += 1

				# Apply Brands and resistances
				if brand == "envenomed": brandhit = d(100) > 50 and d(4) > poisonr
				elif brand == "flaming":
					# Manage Dawn
					if self.sname == 'Dawn': brandhit = d(6) > firer
					else: brandhit = d(100) > 60 and d(4) > firer
				elif brand == "electrified":
					# Manage Mjölnir 1
					if self.sname == "Mjölnir": brandhit = d(100) > 40 and d(5) > shockr
					else: brandhit = d(100) > 40 and d(4) > shockr
				elif brand == "soulflame": brandhit = True if d(100) > 65 and "evening rites" not in enemy.traits else False
				elif brand == "frozen": brandhit = d(100) > 80 and d(4) > frostr
				elif brand == "antimagic": brandhit = True if len(enemy.spells) > 0 else False
				elif brand == "possessed": brandhit =  d(100) > 80
				elif brand == "vorpal": brandhit =  True if len(enemy.passives) != 0 else False
				elif brand == "holy":
					if enemy.name != 'you': brandhit = True if enemy.etype in Monsters.holy_vulnerable else False
					else: brandhit = True if enemy.race in ["Demonkin"] else False
				elif brand == "silvered":
					if enemy.name != 'you': brandhit = True if enemy.etype in Monsters.silver_vulnerable else False
					else: brandhit = True if enemy.race in ["Ghoul"] else False
				elif brand == "vampiric":
					if enemy.name != 'you': brandhit = False if enemy.etype in Monsters.dont_bleed or "evening rites" in enemy.traits else True
					else: brandhit = False if enemy.race in ["Felltron"] or "evening rites" in enemy.traits else True
				elif brand == "runic":
					brandhit = False
					if attacker.mana >= self.damage / 2:
						attacker.mana -= int(self.damage / 2)
						brandhit = True
				elif brand == "hellfire":
					brandhit = True if "evening rites" not in enemy.traits else False
				elif brand is not None: brandhit = True
				elif brand is None: brandhit = False

				# Apply Brands
				if not marked and damage > 0: damage = self.apply_brands(attacker, enemy, damage, brand, brandhit)


				# Weapon class effects
				damage = self.weapon_type_effect(attacker, enemy, damage)

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

				# Check passives
				if brandhit:
					for passive in self.passives:
						passive[1] -= 1

						if passive[1] == 0:
							self.passives.remove(passive)
							self.brand = self.origbrand
						
				# Manage runic Armor
				if enemy.equipped_armor.brand == 'runic' and enemy.mana > 0:
					manadam = min(enemy.mana, damage)
					enemy.mana -= manadam
					enemy.hp -= damage - manadam
				else:
					# Resolve Damage
					enemy.hp -= damage

				# Manage Spiked
				try:
					game.game_log.append(enemy.info[1][0].upper() + enemy.info[1][1:] + ' spikes deal ' + str(barb_damage) + ' damage back to ' + attacker.info[0] + '!')

					# Manage runic Armor
					if attacker.equipped_armor.brand == 'runic' and attacker.mana > 0:
						manadam = min(attacker.mana, barb_damage)
						attacker.mana -= manadam
						attacker.hp -= barb_damage - manadam
					else:
						# Resolve Damage
						attacker.hp -= barb_damage

						# Manage Bloodshell
						if enemy.equipped_armor.sname == "Bloodshell":
							healthback = d(barb_damage)
							enemy.hp = min(enemy.maxhp, enemy.hp + healthback)
							game.game_log.append(enemy.equipped_armor.name + " collects the blood and heals " + enemy.info[0] + " for " + str(healthback) + " health!")

					# Check if unit is still alive
					if type(attacker) != Player: 
						game.player.well_being_statement(attacker, enemy, "spikes", game, False)

				except: pass

				# Manage Possessed
				if brand == "possessed" and brandhit: self.strike(attacker, enemy)

				# Manage the Phasic Robes
				if enemy.equipped_armor.sname == "the Phasic Robes" and self.wclass not in Weapons.ranged_wclasses:
					Spells.blink("blink",enemy, enemy, game, Maps.rooms[game.map.map][0], game.map.room_filler)

				# Manage God-Frame
				if enemy.equipped_armor.sname == "God-Frame" and self.wclass not in Weapons.ranged_wclasses:
					if d(100) >= 90:
						# Stun
						# ------------------------
						applied = False
						for passive in attacker.passives:

							if passive[0] == "stunned":
								passive[1] = 1
								applied = True
								break

						if not applied: attacker.passives.append(["stunned", 1])
						# ------------------------
						game.game_log.append(enemy.equipped_armor.name + " unleashes a shockframe of energy that " + fg.magenta + "stuns" + fg.rs + " " + attacker.info[0] + "!")



				# Manage the Singing Spear
				if self.sname == "the Singing Spear" and d(100) >= 75:

					brands = ["flaming","frozen","envenomed","hellfire","soulflame","vampiric","electrified","vorpal","holy","runic","possessed"]
					verbs = ["whistles","sings","shouts","whispers","belts","hums"]
					types = ["sweet","brisk","harsh","soft","crashing","melodic"]

					self.brand = brands[d(len(brands)) - 1]
					fg.color, self.color = Colors.array[Brands.colors[self.brand]], Brands.colors[self.brand]
					self.name = fg.color + self.sname + fg.rs
					verb = verbs[d(len(verbs)) - 1]
					atype = types[d(len(verbs)) - 1]
					game.game_log.append(self.name + " " + verb + " a " + atype + " melody.")

				# Manage Kraken 2
				if self.sname == 'Kraken' and self.thrown:
					enemy.inventory.append(self)
					attacker.wielding.remove(self)
					if attacker.name == 'you': attacker.hands += 1



				# Check to see who weapon killed
				for unit in game.units[1:]:
					if unit == attacker: continue
					game.player.well_being_statement(unit,attacker,self,game,False)

			# Miss Case
			else:

				# Manage Kraken 4
				if self.sname == "Kraken" and self.thrown:
					self.loc = enemy.loc
					game.items.append(self)
					attacker.wielding.remove(self)
					if attacker.name == 'you': attacker.hands += 1

				# Manage blades
				counter = None
				for weapon in enemy.wielding:
					if type(weapon) == Weapon:
						if weapon.wclass in ["sword","bastard sword","demon sword","god sword"] and self.wclass not in Weapons.ranged_wclasses: 

							# Manage Nightsbane
							if weapon.sname == "Nightsbane":
								if attacker.name != 'you':
									if attacker.etype in Monsters.silver_vulnerable: counter = weapon 
								else:
									if attacker.race in ["Ghoul"]: counter = weapon 
							else:
								# Normal Counter chance
								if d(100) + 3 * enemy.dex > 75: counter = weapon

				if firstswing:

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

						# Manage Bloodreaver
						if counter.sname == "Bloodreaver":
							# Apply Effect
							# ---------------------------
							status, count = 'marked', 10
							applied = False
							for passive in attacker.passives:

								if passive[0] == status:
									passive[1] = count
									applied = True
									break
							if not applied: attacker.passives.append([status, count])
							# ---------------------------
							fg.color = Colors.array["darkred"]
							if type(enemy) == Player: game.game_log.append("You counter the " + str(attacker.name) + " with " + counter.name + " for " + str(damage) + " damage and mark it with a " + fg.color +  "black mark" + fg.rs + "!")
							else: game.game_log.append("The "  + str(enemy.name) + " counters " + aname +  " with " + counter.name + " for " + str(damage) + " damage and marks you with a " + fg.color +  "black mark" + fg.rs + "!")
						else:
							if type(enemy) == Player: game.game_log.append("You counter the " + str(attacker.name) + " with your blade for " + str(damage) + " damage!")
							else: game.game_log.append("The "  + str(enemy.name) + " counters " + aname +  " with its blade for " + str(damage) + " damage!")

						# Manage runic Armor
						if attacker.equipped_armor.brand == 'runic' and attacker.mana > 0:
							manadam = min(attacker.mana, damage)
							attacker.mana -= manadam
							attacker.hp -= damage - manadam
						else:
							# Resolve Damage
							attacker.hp -= damage
						if enemy.name == 'you':
							try: game.player.well_being_statement(attacker, game.player, counter, game, False)
							except: pass


	def weapon_type_swing(self, attacker, enemy):

		# CLEAVE ATTACK
		if self.wclass in ["greatsword","god sword","bastard sword","scythe","greataxe","god axe","claw gauntlets"]:

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
					if self.wclass == 'scythe':
						if unit.loc == (attacker.loc[0], enemy.loc[1] + 1):
							self.strike(attacker, unit, False)
						if unit.loc == (attacker.loc[0], enemy.loc[1] - 1):
							self.strike(attacker, unit, False)

				# Vertical Case
				elif y == 0:
					if unit.loc == (enemy.loc[0] + 1, enemy.loc[1]):
						self.strike(attacker, unit, False)
						cleave = True
					if unit.loc == (enemy.loc[0] - 1, enemy.loc[1]):
						self.strike(attacker, unit, False)
						cleave = True
					if self.wclass == 'scythe':
						if unit.loc == (enemy.loc[0] + 1, attacker.loc[1]):
							self.strike(attacker, unit, False)
						if unit.loc == (enemy.loc[0] - 1, attacker.loc[1]):
							self.strike(attacker, unit, False)

				# Corner case
				else:
					if unit.loc == (enemy.loc[0] + y, enemy.loc[1]):
						self.strike(attacker, unit, False)
						cleave = True
					if unit.loc == (enemy.loc[0], enemy.loc[1] + x):
						self.strike(attacker, unit, False)
						cleave = True
					if self.wclass == 'scythe':
						if unit.loc == (enemy.loc[0] + 2*y, enemy.loc[1]):
							self.strike(attacker, unit, False)
						if unit.loc == (enemy.loc[0], enemy.loc[1] + 2*x):
							self.strike(attacker, unit, False)

			if not cleave and self.wclass in ['greatsword','god sword'] and unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])): self.strike(attacker, unit, False)
			# --END------------------------------------

		if self.wclass in ["spear","polearm","lance","glaive"]:
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


	def weapon_type_effect(self, attacker, enemy, damage):


		# Blunt weapons
		if self.wclass in ["hammer","club","mace","flail","gauntlet"]:
			if enemy.equipped_armor.aclass == 'plate': damage *= 1.4

		if self.wclass in ["warhammer","greatclub","god hammer","fists","gauntlets"]:
			if enemy.equipped_armor.aclass == 'plate': damage *= 1.4

			# Stun
			if d(100) >= 65:
				for passive in enemy.passives:

					if passive[0] == "stunned":
						passive[1] = 1
						return damage

				enemy.passives.append(["stunned", 1])

		if self.wclass in ["greataxe","god axe","axe","claw gauntlet","claw gauntlets"]:
			damage *= (1 + max(0, (0.25 - enemy.calc_AC() / 50 )) )

		return int(damage)


	def apply_brands(self, attacker, enemy, damage, brand, brandhit):


		# APPLY BRANDS
		if brandhit:

			# Manage Flaming
			if brand == "flaming":

				for passive in enemy.passives:
					
					if passive[0] == "aflame": return damage

				enemy.passives.append(["aflame", Brands.dict["flaming"]["count"]])

			# Manage soulflame
			if brand == "soulflame":

				for passive in enemy.passives:
					
					if passive[0] == "drained":
						passive[1] = Brands.dict["drained"]["count"]
						return damage

				enemy.passives.append(["drained", Brands.dict["drained"]["count"]])
				enemy.dex -= Brands.dict["drained"]["dex_loss"]

			# Manage Vampiric
			if brand == "vampiric":

				# Manage Krog's Maw
				if self.sname == "Krog's Maw":
					heal = int(damage / 3)
					if attacker.hp <= attacker.maxhp and attacker.hp + heal > attacker.maxhp: game.after_hit.append(self.name + " grants " + attacker.name + " a shield of blood.")
					attacker.hp = min(int(attacker.maxhp * 1.2), attacker.hp + heal)
				else:
					# heal
					attacker.hp = min(attacker.maxhp, attacker.hp + int(damage / 3))

			# Manage Hellfire
			if brand == "hellfire": damage += int((1 - (enemy.hp / enemy.maxhp) ) * damage * 0.5)

			# Manage Envenomed
			if brand == "envenomed":

				# Manage Splinter
				count = 3 if self.sname == 'Splinter' else Brands.dict["envenomed"]["count"]

				for passive in enemy.passives:

					if passive[0] == "poisoned":
						passive[1] += count
						return damage

				enemy.passives.append(["poisoned", count])

			# Manage Silvered
			if brand == "silvered": damage *= 1.5

			# Manage Holy
			if brand == "holy": damage *= 1.8

			# Manage Antimagic
			if brand == "antimagic": damage *= 1.7

			# Manage Electrified
			if brand == "electrified":

				# Manage Mjölnir 2
				if self.sname == "Mjölnir":

					# Shock Radius
					def shock(enemy, affected = []):
						if enemy in affected: return
						affected.append(enemy)
						spaces = set([])
						for x in range(-1,2):
							for y in range(-1,2):
								if enemy.loc[0] + x >= 0 and enemy.loc[1] + y >= 0: spaces.add((enemy.loc[0] + x, enemy.loc[1] + y))
						# Find units affected
						for unit in game.units:
							if unit.loc in spaces and enemy != unit and unit not in affected and unit != attacker: shock(unit, affected)
						return affected[1:]

					affected = shock(enemy)
					# Hit string
					hit = ""
					thunder_damage = md(enemy.tier,3)
					for unit in affected:

						# Shock Resist
						if d(5) <= enemy.calc_resistances()[4]: continue

						unit.hp -= thunder_damage
						if unit.name == 'you':
							if len(hit) == 0: hit += "you"
							else: hit += ", you"
						else:
							if len(hit) == 0: hit += "the " + unit.name
							else: hit += ", the " + unit.name

					flav = " each" if len(affected) > 1 else ""

					if hit != "": game.after_hit.append(self.name + " smites " + hit + " with " + fg.yellow + "godly thunder" + fg.rs + flav + " for " + str(thunder_damage) + " damage!")
					# for unit in affected: game.player.well_being_statement(unit,attacker,self,game,False)

				else:
					if attacker.name == 'you': damage += md(attacker.level,2)
					else: damage += md(attacker.tier,2)

			# Manage Vorpal
			if brand == "vorpal":

				vdamage = int(len(enemy.passives) * enemy.hp / enemy.maxhp)
				game.check_passives(enemy, True)
				damage += vdamage


			# Manage Frozen=
			if brand == "frozen":

				for passive in enemy.passives:

					if passive[0] == "frozen":
						passive[1] += Brands.dict["frozen"]["count"]
						return damage

				enemy.passives.append(["frozen", d(Brands.dict["frozen"]["count"])])

		# Return DAMAGE
		return damage


	def damage_statement(self, attacker, enemy,  damage, brand, brandhit, ename, eposs):
		attacker_var, attackee_var =  str(attacker.name), str(enemy.name)
		name, wclass = self.name, self.wclass

		if self.wclass in Weapons.ranged_wclasses and self.hands > 0: name, wclass = attacker.quivered.name, attacker.quivered.wclass

		# Manage legendary and unique
		name = name if self.legendary and attacker.name == 'you' else "its " + name
		if attacker.name != 'you': attacker_var = attacker_var if attacker.namestring in Monsters.uniques else "The " + attacker_var
		if enemy.name != 'you': attackee_var = attackee_var if enemy.namestring in Monsters.uniques else "the " + attackee_var


		# Make the sentence awesome
		verb, preposition = Weapons.weapon_classes[wclass]

		# Manage the Glaive of Gore
		if self.sname == "the Glaive of Gore" and d(100) >= 9:

			enemy.str -= Brands.dict['disemboweled']['strred']

			# ------------------------
			applied = False
			for passive in enemy.passives:

				if passive[0] == "disemboweled":
					passive[1] = 3
					applied = True
					break

			if not applied: enemy.passives.append(["disemboweled", 3])
			# ------------------------
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " disembowels " + ename + " with " + name + " for " + str(damage) + " damage!")
			else:
				game.game_log.append("You disembowel " + attackee_var + " with " + name + " for " + str(damage) + " damage and weaken it!")

		# Manage God-Cleaver 2
		elif self.sname == "God-Cleaver" and enemy.god_cleaver_hits == 4:
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with " +  name + ", its blade glows red!")
			else:
				game.game_log.append("You " + verb + " " + name + " " + preposition + " " + attackee_var + " for " + str(damage) + " damage, your blade glows red!")

		# Manage God-Cleaver 3
		elif self.sname == "God-Cleaver" and enemy.god_cleaver_hits == 5:
			if type(attacker) == Monster:
				game.game_log.append("With a clean sweep " + attacker_var + " cleaves off " + enemy.info[1] +  " head!")
			else:
				game.game_log.append("With a clean sweep you cleave off " + attackee_var + "'s head with " + name + "!")
			enemy.hp = 0

		# Manage Kraken 6
		elif self.sname == "Kraken" and self.thrown:
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " throws " + name + " into " + ename +  " for " + str(damage) + " damage with!")
			else:
				game.game_log.append("You throw "+ name + " into " + attackee_var + " for " + str(damage) + " damage!")

		# Make the notes dank
		elif brand is None or not brandhit:
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with " +  name + "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + attackee_var + " for " + str(damage) + " damage!")

		elif brand == "holy":
			fg.color = Colors.array["bone"]
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with " + fg.color + "holy" + fg.rs + " "  + name + " and smites " + ename +  " down!")
			else:
				game.game_log.append("You smite " + attackee_var+ " with your " + fg.color + "holy" + fg.rs + " "+ str(wclass) + " for " + str(damage) + " damage!")

		elif brand == "silvered":
			fg.color = Colors.array["steel"]
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with "  + name + ", its " + fg.color + "silver" + fg.rs + " burns " + ename +  "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + attackee_var+ ", the " + fg.color + "silver" + fg.rs + " burns for " + str(damage) + " damage!")

		elif brand == "electrified":
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with "  + name + " and " + fg.yellow + "shocks" + fg.rs + " " + ename +  "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + attackee_var+ " and " + fg.yellow + "shock" + fg.rs + " it for " + str(damage) + " damage!")

		elif brand == "antimagic":
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with "  + name + ", " + eposs + " mana " + fg.magenta + "burns" + fg.rs + " inside!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + attackee_var+ ", its mana " + fg.magenta + "burns" + fg.rs + " for " + str(damage) + " damage!")

		elif brand == "vampiric":
			fg.color = Colors.array["red"]
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with "  + name + " and " + fg.color + "drains" + fg.rs + " " + eposs +  " life!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + attackee_var+ ", dealing " + str(damage) + " damage and " + fg.color + "draining" + fg.rs + " its life!")

		elif brand == "flaming":
			fg.color = Colors.array["fire"]
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with " + name + " and sets " + ename +  " " + fg.color + "aflame" + fg.rs + "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + attackee_var + ", dealing " + str(damage) + " damage and setting it " + fg.color + "aflame" + fg.rs + "!")
		elif brand == "runic":
			fg.color = Colors.array["lightblue"]
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " " + fg.color + "empowered" + fg.rs + " damage with " + name + "!")
			else:
				game.game_log.append("You " + verb + " your " + fg.color + "crackling" + fg.rs + " "+ str(wclass) + " " + preposition + " " + attackee_var + " to deal an empowered " + str(damage) + " damage!")
		elif brand == "soulflame":
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with " + name + " and saps " + eposs +  " will!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + attackee_var + ", dealing " + str(damage) + " damage and sapping its will!")
		elif brand == "possessed":
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + "'s' " + name + " lashes out ravenously at " + ename +  " for " + str(damage) + " damage!")
			else:
				game.game_log.append("Your " + str(wclass) + " lashes out ravenously at " + attackee_var + ", dealing " + str(damage) + " damage!")

		elif brand == "frozen":
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with " + name + " and " + fg.cyan + "freezes" + fg.rs + " " + ename +  "!")
			else:
				game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + attackee_var + ", dealing " + str(damage) + " damage and " + fg.cyan + "freezing" + fg.rs + " it!")

		elif brand == "hellfire":
			fg.color = Colors.array["orange"]
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with " + name + " and " + fg.color + "burning" + fg.rs + " " + eposs +  " soul!")
			else:
				game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + attackee_var + ", dealing " + str(damage) + " damage and " + fg.color + "burning" + fg.rs + " its soul!")

		elif brand == "vorpal":
			fg.color = Colors.array["purple"]
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + "'s " + fg.color + "vorpal" + fg.rs + " weapon ignites " + eposs +  " status effects with " + name + " and deals " + ename + " " + str(damage) + " damage!")
			else:
				game.game_log.append("You " + verb + " your " + fg.color + "vorpal" + fg.rs + " " + str(wclass) + " " + preposition + " " + attackee_var + " and ignite its status effects for " + str(damage) + " damage!")

		elif brand == "envenomed":
			if type(attacker) == Monster:
				game.game_log.append(attacker_var + " hits " + ename +  " for " + str(damage) + " damage with " + name + " and " + fg.green +"poisons" + fg.rs + " " + ename +  "!")
			else:
				game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + attackee_var + ", dealing " + str(damage) + " damage and " + fg.green + "poisoning" + fg.rs + " it!")

		# Add back after statement
		if len(game.after_hit) != 0:
			for line in game.after_hit: game.game_log.append(line)
			game.after_hit = []


class Tome():

	def __init__(self, spells, name, rep, color, hands, loc, brand = None):
		self.rep, self.color, self.hands, self.loc, self.brand = rep, color, hands, loc, brand
		self.wclass = "tome"

		# Purchasable Skills
		self.spells = spells

		fg.color = Colors.array[self.color]
		self.name, self.sname = fg.color + name + fg.rs, name

		# Magic Damage
		self.mdamage = 2

		# Legendary
		if self.sname in Weapons.legendaries:
			self.legendary = True
			try: game.legendaries_to_spawn.remove(self.sname)
			except: pass
		else:
			self.legendary = False

	def details(self):

		print(self.string())
		print("")
		print("Basic Class Tome.")
		print("")
		print("Provides 2 bonus magic damage when wielded.")

		if self.legendary:
			print(Descriptions.legendary[self.sname])
			print("")

		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def string(self):

		if self.brand is not None:
			fg.bcolor = Colors.array[Brands.colors[self.brand]]
			return (fg.bcolor + self.brand + fg.rs + ' '  + self.name)

		else:
			return (self.name)

class Armor():

	def __init__(self, name, rep, color,   aclass, armor_rating, encumbrance, enchantment, loc, brand = None):
		self.rep, self.color, self.aclass, self.armor_rating, self.encumbrance, self.enchantment, self.loc, self.brand = rep, color, aclass, armor_rating, encumbrance, enchantment, loc, brand

		fg.color = Colors.array[self.color]
		self.name, self.sname = fg.color + name + fg.rs, name

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = 0, 0, 0, 0, 0, 0

		# Legendary
		if self.sname in Weapons.legendaries:
			self.legendary = True
			try: game.legendaries_to_spawn.remove(self.sname)
			except: pass
		else:
			self.legendary = False

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


		# Manage Icy, Tempered, Insulated, Voidforged
		if self.brand == 'tempered':
			self.firer += 2
		if self.brand == 'icy':
			self.frostr += 2
		if self.brand == 'insulated':
			self.shockr += 2
		if self.brand == 'voidforged':
			self.mdefense += 2


	def details(self):

		if self.encumbrance > 0: encum = '-' + str(self.encumbrance)
		else: encum = '+' + str(abs(self.encumbrance))

		print(self.string(),' (' + self.aclass + ')')
		print("")
		print("Base armor rating:", str(self.armor_rating) + ',', "Base encumbrance:", encum)
		print("")

		if self.legendary:
			print(Descriptions.legendary[self.sname])
			print("")

		print(Descriptions.wclass[self.aclass])
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def string(self):

		enchstr = "+" + str(self.enchantment) if self.enchantment >= 0 else str(self.enchantment)
		fg.color = Colors.array[self.color]

		if self.brand is not None:
			fg.bcolor = Colors.array[Brands.colors[self.brand]]
			if self.sname[:4].lower() == 'the ': return (fg.color + self.sname[:4] + fg.rs + fg.bcolor + self.brand + fg.rs + " " + enchstr + ' ' + fg.color + self.sname[4:] + fg.rs)
			else: return (fg.bcolor + self.brand + fg.rs + " " + enchstr + ' ' + self.name)
		else:
			if self.sname[:4].lower() == 'the ': return (fg.color + self.sname[:4] + fg.rs + enchstr + ' ' + fg.color + self.sname[4:] + fg.rs)
			else: return (enchstr + ' ' + self.name)

class Shield():

	def __init__(self, name, rep, color, hands, armor_rating, encumbrance, enchantment, loc, brand = None):
		self.rep, self.color, self.hands, self.armor_rating, self.encumbrance, self.enchantment, self.loc, self.brand = rep, color, hands, armor_rating, encumbrance, enchantment, loc, brand
		self.wclass = "shield"

		fg.color = Colors.array[self.color]
		self.name, self.sname = fg.color + name + fg.rs, name

		# Legendary
		if self.sname in Weapons.legendaries:
			self.legendary = True
			try: game.legendaries_to_spawn.remove(self.sname)
			except: pass
		else:
			self.legendary = False

		# Magic Damage
		self.mdamage = 0

	def details(self):

		if self.encumbrance >= 0: encum = '-' + str(self.encumbrance)
		else: encum = '+' + str(abs(self.encumbrance))

		print(self.string())
		print("")
		print("This shield is " + str(self.hands) + "-handed.")
		print("Base armor rating:", str(self.armor_rating) + ',', "Base encumbrance:", encum)

		if self.legendary:
			print("")
			print(Descriptions.legendary[self.sname])

		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])

	def string(self):

		if self.brand is not None:
			fg.bcolor = Colors.array[Brands.colors[self.brand]]

			if self.enchantment >= 0: return (fg.bcolor + self.brand + fg.rs + " +" + str(self.enchantment) + ' ' + self.name)
			else: return (fg.bcolor + self.brand + fg.rs + ' ' + str(self.enchantment) + ' ' + self.name)
		else:
			# Positive Encahntment
			if self.enchantment >= 0: return ("+" + str(self.enchantment) + ' ' + self.name)
			else: return (str(self.enchantment) + ' ' + self.name)

class Mount():

	def __init__(self, roomfiller, rider, mount, ally):
		roomfiller.spawn(mount, rider.loc, ally, rider)
		self.unit = game.units[-1]

class Ammo():

	def __init__(self, name, rep, color, wclass, number, damage, loc, brand = None):
		self.rep, self.color, self.wclass, self.damage, self.number, self.loc, self.brand = rep, color, wclass, damage, number, loc, brand

		fg.color = Colors.array[self.color]
		self.name, self.sname = fg.color + name + fg.rs, name

	def details(self):
		brand = '' if self.brand is None else self.brand + ' '

		print(self.string(),' (' + self.wclass + ')')
		print("")
		if self.wclass in Ammos.thrown_amclasses: 
			data = Weapons.array[self.sname]
			weap = Weapon(self.name, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],None, None, None)
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
		fg.color = Colors.array[self.color]

		if self.brand is not None:
			fg.bcolor = Colors.array[Brands.colors[self.brand]]
			return (fg.bcolor + self.brand + fg.rs + ' ' + self.name + ' (' + str(self.number) + ')')
		else: return (self.name + ' (' + str(self.number) + ')')

class Trap():

	def __init__(self, damage, type, loc):
		self.damage, self.type, self.loc, self.rep, self.color = damage, type, loc,'*','darkred'

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

				# Explosive Resist
				resist = unit.calc_resistances()[5]
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
								 ["gorktooth choppa","ranger longbow","godclaw","gladius"],
								 ["claymore","khopesh","gorkjaw choppa","executioner axe","dwarven waraxe"],
								 ["witchhunter blade","glaive","dwarven crossbow","dwarven broadaxe"],
								 ["godfist","demonfist","demonclaw","glass dagger","bearded greataxe"] 	]
			self.color = "gold"
		
		elif self.type == "elven":
			self.pot_weapons = [ ["elven wooddagger","elven leafblade"],
								 ["elfrobe"],
								 ["elven leafblade","winged javelin"],
								 ["elven broadspear","elven longbow"],
								 ["elven longstaff"], 	]
			self.color = "gold"
		elif self.type == "dark elven":
			self.pot_weapons = [ ["thornblade","thornknife"],
								 ["thornarrow"],
								 ["blackwood longbow","ironscale mail"],
								 ["sunspear","sunlance"], 	]
			self.color = "purple"
		elif self.type == "wooden":
			self.pot_weapons = [["steel dagger","iron axe","spear","hammer","mace","iron longsword","club","iron shortsword"], 
								["crude shortbow","iron battleaxe","iron longsword","mace","flail","quarterstaff","iron bastard sword"], 
								["buckler shield", "wooden broadshield","trollhide shield","recurve bow"], 
								["iron battleaxe","iron greatsword","warhammer","spiked club","barbed javelin","longbow","falchion","scimitar"],
								["iron plate","iron chainmail","ironscale mail","scrap plate armor"],
								["steel axe","steel longsword","halberd","steel bastard sword","steel shortsword","bearded axe"],
								["steel greatsword","steel battleaxe","pike","greatflail","ranger longbow","steel shortsword"],
								["godfist","godclaw","claymore","gladius"] ]
			self.color = "brown"
		elif self.type == "orcish":
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
				legendary = game.legendaries_to_spawn[ d(len(game.legendaries_to_spawn)) - 1]
				game.map.room_filler.place_weapon(legendary, self.loc, int((d(self.tier) - 1) / 2))
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
						if Weapons.array[item_name][3] > 0 and item_name not in Weapons.legendaries:
							if d(100) + self.tier > 97: brand = Brands.weapon_brands[d(len(Brands.weapon_brands)) - 1]
						game.map.room_filler.place_weapon(item_name, self.loc, int((d(self.tier) - 1) / 2), brand)

					# If Armor
					elif item_name in Armors.array:

						# Chance for brand
						brand = Brands.armor_brands[d(len(Brands.armor_brands)) - 1] if d(100) + self.tier > 97 and item_name not in Weapons.legendaries else None
						game.map.room_filler.place_armor(item_name, self.loc, int((d(self.tier) - 1) / 2), brand)

					# If Shield
					elif item_name in Shields.array:
						game.map.room_filler.place_shield(item_name, self.loc, int((d(self.tier) - 1) / 2))

					# self.pot_weapons.remove(tier)

		# Place Ammo
		if d(10) + d(self.tier) > 6:

			# Chance for brand
			brand = None
			if d(100) + 2 * self.tier > 96: brand = Brands.ammo_brands[d(len(Brands.ammo_brands)) - 1]

			ammo = self.pot_ammo[min(len(self.pot_ammo) - 1, d(self.tier) - 1)]
			if ammo in Weapons.array: number = 2 * self.tier
			else: number = 5 + self.tier
			game.map.room_filler.place_ammo(ammo, self.loc, number, brand)
		self.opened = True





class Map():

	def __init__(self, game, room):

		self.map, self.game = room, game

		self.def_map_array = Maps.rooms[self.map][0]
		self.map_array = deepcopy(self.def_map_array)

		self.entry_point, self.exits = Maps.rooms[self.map][2], Maps.rooms[self.map][3]


		self.adjacent = {self.entry_point: None}
		for point in self.exits[1:]: self.adjacent[point] = None

		self.objects, self.allies = [], []

		self.filled = False

		self.construct_graph()

	def construct_graph(self):
		self.graph = {}
		height = len(self.map_array)
		width = len(self.map_array[0])


		for orgx in range(width):

			for orgy in range(height):

				for pair in [(0,1),(1,0),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(1,1)]:

					adx = pair[0] + orgx
					ady = pair[1] + orgy
					if 0 <= adx < width and 0 <= ady < height and (orgx != adx or orgy != ady):
						try: self.graph[(orgx,orgy)].append((adx,ady))
						except: self.graph[(orgx,orgy)] = [ (adx,ady) ]

	def fill(self):
		self.room_filler = RoomFiller(self.game.player.level, (15,2), self.map)
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
			# try:
			# 	print(item.name, item.loc)
			# except: print(item.loc)
			try:
				y, x = item.loc[0], item.loc[1]
				fg.color = Colors.array[item.color]
				self.map_array[x][y] = fg.color + item.rep + fg.rs
			except: game.items.remove(item)
		# Place each unit on the map
		for unit in game.units[::-1]:
			y, x = unit.loc[0], unit.loc[1]

			fg.color = Colors.array[unit.color]
			if unit.rider is not None:
				fg.color = Colors.array[unit.rider.color]
				bg.color = Colors.array[unit.color]
				self.map_array[x][y] = fg.color + bg.color + unit.rider.rep + rs.all
			elif unit.mount is not None:
				bg.color = Colors.array[unit.mount.unit.color]
				self.map_array[x][y] = fg.color + bg.color + unit.rep + rs.all 
			else:
				self.map_array[x][y] = fg.color + unit.rep + fg.rs 
				

		# Display the map
		for line in self.map_array: print("        " + self.parse(line))

	def change_room(self, new_room):

		room, newloc = new_room[0], new_room[1]
		self.objects = []


		# Store units
		for unit in game.units[1:]:
			if type(unit) == Monster:
				self.objects.append(unit)
			if unit in game.allies: self.allies.append(unit)

		for item in game.items:
			self.objects.append(item)

		# Clear units
		game.units, game.allies, game.items = [game.player], [game.player], []

		# Add old room's units
		for object in room.objects:
			game.units.append(object) if type(object) == Monster else game.items.append(object)
			if object in room.allies: game.allies.append(object)

		game.map = room

		# Place boyo on map
		if newloc == Maps.rooms[room.map][2]:
			self.game.player.loc = (newloc[0] + 1, newloc[1])
		else:
			self.game.player.loc = (newloc[0] - 1, newloc[1])



	def new_room(self, coords):

		# Store units
		for unit in game.units[1:]:
			if type(unit) == Monster: self.objects.append(unit)
			if unit in game.allies: self.allies.append(unit)

		for item in game.items: self.objects.append(item)

		# Clear units
		game.units, game.allies, game.items = [game.player], [game.player], []

		# Make new Map
		pot_maps = Maps.sizes[Maps.rooms[self.map][3][0][d(len(Maps.rooms[self.map][3][0])) - 1]]
		newmap = Map(self.game,pot_maps[ d(len(pot_maps)) - 1])
		game.map = newmap

		# Entry Point
		self.adjacent[coords] = (newmap, newmap.entry_point)
		newmap.adjacent[newmap.entry_point] = (self, coords)
		self.game.player.loc = (newmap.entry_point[0] + 1, newmap.entry_point[1])

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
		tier_group = game.bands
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
				unit = min(len(group) - 1, d(etier + bonus - max(i,bonus)    ) - 1)
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

					try:
						if game.map.square_identity(spawn_location) not in ['|', '-', ' ', '#','+','@','_'] and spawn_location != game.player.loc and spawn_location not in spawned:
							picked = True
							prev_loc = spawn_location
							spawned.add(prev_loc)
					except: pass


				self.spawn(group[unit] , spawn_location)

	def spawn(self, monster_name, loc, ally = False, mount_unit = None):
		data = Monsters.array[monster_name]
		try: other_items = data[14]
		except: other_items = None

		# Spawn Unit
		unit = Monster(monster_name, data[0],data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], loc, other_items)
		game.units.append(unit)
		if ally: game.allies.append(unit)

		# if mount_unit is not None:
		# 	mount_unit.rider = game.units[-1]
		# 	game.units[-1].mount = mount_unit

	def place_weapon(self, weapon, loc, enchantment = 0, brand = None):
		data = Weapons.array[weapon]

		# Manage Enchantment + Brand
		spawned_enchantment = data[4] + enchantment
		try: brand = data[8]
		except: pass

		# Create Weapon Object
		game.items.append(Weapon(weapon, data[0], data[1], data[2], data[3], spawned_enchantment, data[5], data[6], data[7], loc, brand))

	def place_armor(self, armor, loc, enchantment = 0, brand = None):
		data = Armors.array[armor]

		# Manage Enchantment + Brand
		spawned_enchantment = data[5] + enchantment
		try: brand = data[6]
		except: pass

		# Create Armor Object
		game.items.append(Armor(armor, data[0], data[1], data[2], data[3], data[4], data[5], loc, brand))

	def place_shield(self, armor, loc, enchantment = 0, brand = None):
		data = Shields.array[armor]

		# Manage Enchantment
		spawned_enchantment = data[5] + enchantment
		try: brand = data[6]
		except: pass

		#Create Shield Object
		game.items.append(Shield(armor, data[0], data[1], data[2], data[3], data[4], data[5], loc, brand))

	def place_ammo(self, ammo, loc, number, brand = None):
		data = Ammos.array[ammo]

		# Manage Enchantment
		try: brand = data[4]
		except: pass

		#Create Shield Object
		game.items.append(Ammo(ammo, data[0], data[1], data[2], number, data[3], loc, brand))

	def place_chest(self, type, tier, loc):
		game.items.append(Chest(type, tier, loc))










class Game():

	def __init__(self):

		# Manage Constants
		self.race = None
		self.pclass = None

		self.map = Map(self, 'starting_room')
		self.state = 'ongoing'
		self.room = 0
		self.bands = Bands.dicto[1]

		# Initiate Regen
		self.hregen, self.mregen, self.prev_valid_turn = 0, 0, True

		# Manage Units
		self.units, self.allies, self.items, self.seen = [], [], [], set([])
		self.legendaries_to_spawn = [weap for weap in Weapons.legendaries if weap not in Weapons.enemy_legendaries]

		# Manage Game Log
		self.game_log, self.temp_log = [], []
		self.after_hit = []

		# item order
		self.item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


	def character_select(self, info = False):
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("")
		print("GNG")
		print("---------------------------")
		print("")
		i, record = 0, {}
		for race, stats in CharacterInfo.races.items():
			fg.color = Colors.array[CharacterInfo.races[race][0][-1]]
			print(str(self.item_order[i]) + ") " + fg.color + race + fg.rs)
			if info: print( fg.color + Descriptions.races[race] + fg.rs)
			record[self.item_order[i]] = race
			i += 1


		race_decision = rinput("Which race will you play? Press '?' to toggle information.")

		if race_decision == '?':
			if not info: info = True
			else: info = False
			return self.character_select(info)
		elif race_decision in "1234567890": return False

		try:

			self.race = record[race_decision]



			goback = True


			while goback == True:

				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("")
				print("GNG")
				print("---------------------------")
				fg.color = Colors.array[CharacterInfo.races[self.race][0][-1]]
				print(fg.color + self.race + fg.rs + "      (Press spacebar to rechoose)")
				print("")

				i, record = 0, {}
				for pclass, stats in CharacterInfo.class_progression.items():
					print(str(self.item_order[i]) + ") " + pclass)
					record[self.item_order[i]] = pclass
					i += 1


				class_decision = rinput("Which class will you play?")

				if class_decision == " ":
					self.character_select()
					return
				if class_decision in self.item_order and self.item_order.index(class_decision) < len(CharacterInfo.class_progression):
					# game.race = record[race_decision]
					self.pclass = record[class_decision]

					# Create Player
					self.player = Player(CharacterInfo.races[self.race][0], CharacterInfo.races[self.race][1], self)

					self.player.race = self.race
					self.player.pclass = self.pclass
					self.units.append(self.player)
					self.allies.append(self.player)


					goback = False

		except: 
			self.character_select(info)


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
					if len(game.units) == len(game.allies):
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
					if len(game.units) == len(game.allies):
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
					if len(game.units) == len(game.allies):
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
					if len(game.units) == len(game.allies):
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
					if len(game.units) == len(game.allies):
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
					if len(game.units) == len(game.allies):
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
					if len(game.units) == len(game.allies):
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
					if len(game.units) == len(game.allies):
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
					# Manage Kraken 9
					if self.player.wielding[-1].sname == 'Kraken': self.player.wielding[-1].thrown = False
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
					if len(game.units) == len(game.allies):
						while self.player.hp < self.player.maxhp or self.player.mana < self.player.maxmana: action('.')
						game.temp_log.append("You feel well-rested")
						self.player.time = 0
					else:
						game.temp_log.append("There are enemies nearby!")

				# Manage Kraken 8
				# UPDATE THIS LIST WHENEVER YOU ADD MORE ACTIONS!!!!!!!!
				carrying = [weap for weap in self.player.wielding if weap.hands != 0]
				if move not in 'fiwW+':
					for unit in game.units[1:]:
						for item in unit.inventory:
							if item.sname == 'Kraken':
								if item.thrown and (self.player.hands >= 1 and self.player.race != 'Hill Troll' or len(carrying) != 2 and self.player.hands >= 1 and self.player.race == 'Hill Troll'):
									unit.inventory.remove(item)
									uname = unit.name if unit.namestring in Monsters.uniques else 'the ' + unit.name
									damage = d(item.damage)

									# Apply Effect
									unit.hp -= damage
									# ----------------------------
									applied = False
									for passive in unit.passives:

										if passive[0] == 'immobile':
											passive[1] += 2
											applied = True
											break

									if not applied: unit.passives.append(['immobile', 2])
									# ----------------------------

									self.game_log.append(item.name + ' rips out of ' + uname + ', dealing ' + str(damage) + ' damage, and returns to your hand!' )
									self.player.wielding.append(item)
									self.player.hands -= 1
									item.thrown = False
									self.player.well_being_statement(unit, self.player, item, self)
									break
					for item in self.items:
						if type(item) != Chest:
							if item.sname == 'Kraken':
								if item.thrown and (self.player.hands >= 1 and self.player.race != 'Hill Troll' or len(carrying) != 2 and self.player.hands >= 1 and self.player.race == 'Hill Troll'):
									self.items.remove(item)
									self.game_log.append(item.name + ' returns to your hand!' )
									self.player.wielding.append(item)
									self.player.hands -= 1
									item.thrown = False
									break

			else: game.temp_log.append("Invalid Move")









		# Manage Game Log
		self.game_log.append("                                                                     ")

		log_select = self.game_log[((len(Maps.rooms[game.map.map][0]) - 24) + len(self.temp_log)):]
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
			quivered_string = " " + self.player.quivered.string()

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

		if self.player.hp < self.player.maxhp / 3.2:
			fg.color = Colors.array['red']
		elif self.player.hp < self.player.maxhp / 1.6:
			fg.color = Colors.array['yellow']
		elif self.player.hp <= self.player.maxhp:
			fg.color = Colors.array['green']
		else:
			fg.color = Colors.array['fire']
		fg.lightblue = Colors.array['lightblue']


		print("Level " + str(self.player.level) + " " + self.player.race + " " + self.player.pclass)
		if self.player.hp <= self.player.maxhp: print("HP    " + fg.color + str(self.player.hp)+ "/" + str(self.player.maxhp) + fg.rs   + hpspace + "Wielding:" + weapon_string + "         Armor: " + self.player.equipped_armor.string())
		else: print("HP    " + fg.color + str(self.player.hp)+ fg.rs + fg.green + "/" + str(self.player.maxhp) + fg.rs   + hpspace + "Wielding:" + weapon_string + "         Armor: " + self.player.equipped_armor.string())
		print("MANA  " + fg.lightblue + str(self.player.mana) + "/" + str(self.player.maxmana) + fg.rs +  manaspace + "Quivered:" + quivered_string)

		# YOU DIE!!
		if self.player.hp <= 0:
			print("You have been slain!")
			print("You suck at this game bruh")
			self.state = "defeat"
			return


		# See Monster
		for unit in self.units[1:]:
			if unit not in self.seen and unit.rider is None:

				wielding = ""
				for item in unit.wielding[::-1]:
					if wielding == "" and item.hands > 0:
						if item.sname not in Weapons.legendaries:
							if item.sname[0].lower() in ['a','e','i','o','u']:
								warticle = 'an '
							else: warticle = 'a '
						else: warticle = ''
						wielding += item.name
					elif item.hands > 0: wielding += (", a " + item.name)

				if unit.namestring in Monsters.uniques:
					article = ''
				elif unit.namestring[0].lower() in ['a','e','i','o','u']:
					article = 'an ' 
				else:
					article = 'a '

				if len(wielding) == 0:
					if unit.mount is not None: game.game_log.append("You see " + article + unit.name   + " riding a " + unit.mount.unit.name + ", wearing " + unit.equipped_armor.name)
					else: game.game_log.append("You see " + article + unit.name  + ", wearing " + unit.equipped_armor.name)
				else:
					if unit.mount is not None:game.game_log.append("You see " + article + unit.name  + " riding a " + unit.mount.unit.name + ", wearing " + unit.equipped_armor.name + ", wielding " + warticle + wielding)
					else: game.game_log.append("You see " + article + unit.name + ", wearing " + unit.equipped_armor.name + ", wielding " + warticle + wielding)
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

				# Manage hastened
				if name == "hastened": unit.mspeed *= 4

				# Manage Indominable
				if name == "indominable":
					game.game_log.append(unit.info[0].capitalize() + " can now enter Valhalla in peace.")

				# Manage Iron Blessing
				if name == "blessed iron":
					if unit.name == 'you': game.game_log.append("Your iron blessing fades.")
					else: game.game_log.append("The " + unit.name + "'s iron blessing fades.")

				# Manage grotesque
				if name == "grotesque":
					unit.hp -= Brands.dict['grotesque']['bonushp']
					unit.maxhp -= Brands.dict['grotesque']['bonushp']
					unit.str -= Brands.dict['grotesque']['bonusstr']
					if unit.name == 'you': game.game_log.append("Your body returns to its normal shape.")
					else: game.game_log.append("The " + unit.name + "'s body returns to its normal shape.")

				# Manage Disemboweled
				if name == "disemboweled":
					unit.str += Brands.dict['disemboweled']['strred']

				# Manage Immobile
				if name == "immobile":
					game.game_log.append(unit.info[0] + " can move again.")

				unit.passives.remove([passive[0], passive[1]])

			if not purge: 

				# Manage Disemboweled
				if name == "disemboweled":

					damage = max(int(unit.hp * 0.1), 1)
					unit.hp -= damage

					if unit.name == 'you':game.game_log.append("Your wound " + fg.red + "bleeds" + fg.rs + " for " + str(damage) + " damage!")
					else: game.game_log.append("The open wound of " + unit.info[0] + " " + fg.red + "bleeds" + fg.rs + " for " + str(damage) + " damage!")

				# Manage poisoned
				if name == "poisoned":

					damage = count
					unit.hp -= damage

					game.game_log.append(fg.green + "Venom " + fg.rs + "stings " + unit.info[0] + " for " + str(damage) + " damage!")

				# Manage aflame
				if name == "aflame":

					damage = max(1, int(unit.con))
					unit.hp -= damage
					fg.color = Colors.array['fire']

					game.game_log.append(fg.color + "Fire " + fg.rs + "burns " + unit.info[0] + " for " + str(damage) + " damage!")

				# Manage Frozen
				if name == "frozen":
					unit.time += unit.mspeed
					if type(unit) == Player: game.game_log.append("You are " + fg.cyan + "frozen" + fg.rs + "!")
					else: game.game_log.append("The " + str(unit.name) + " is " + fg.cyan + "frozen" + fg.rs + " and cannot move!")


				# Stunned
				if name == "stunned":
					unit.time += unit.mspeed
					if type(unit) == Player: game.game_log.append("You are " + fg.magenta +"stunned" + fg.rs + "!")
					else: game.game_log.append("The " + str(unit.name) + " is " + fg.magenta +"stunned" + fg.rs + "!")



		# Check if unit is still alive
		if unit.hp <= 0 and type(unit) != Player:
			game.game_log.append("The " + unit.name + " dies from its wounds!")
			game.units.remove(unit)
			if unit in game.allies: game.allies.remove(unit)

			# Ooze Passive
			if 'split' in unit.spells: Spells.spells["split"][0]("split", unit, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler)

			# Mounts
			if unit.rider is not None:
				unit.rider.mount = None
			elif unit.mount is not None:
				unit.mount.unit.rider = None

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
if game.character_select() is not False: game.run()
# except:
# 	pass








