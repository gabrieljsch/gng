from codex import Weapons, Ammos, Brands, Armors, Shields, Tomes, Potions
from Spells import Spells
from CharacterInfo import CharacterInfo
from Descriptions import Descriptions
from Colors import Colors
from Weapon import Weapon
from Armor import Armor
from Shield import Shield
from Tome import Tome
from Ammo import Ammo
from Potion import Potion
from Maps import Maps
from bestiary import Bands

from ai import *
import ai

import sys, os
import termios, fcntl
import select


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

def apply(unit, passive, count, stacking=False):

	for present_passive in unit.passives:

		if present_passive[0] == passive:
			if stacking: present_passive[1] += count
			else: present_passive[1] = count
			return

	unit.passives.append([passive, count])


# noinspection PyBroadException
class Player:

	def __init__(self, statsheet, innate_equipment, god, game):

		self.game = game

		# Initialize Location, Time
		self.loc, self.range_from_player, self.time = (2, 5), 0, 0

		# Initialize Representation
		self.rep, self.name, self.info, self.passives, self.race, self.pclass, self.god = '@', "you", ('you', 'your', 'your', 'You', 'Your'), [], None, self.game.pclass, god

		# Initialize Stats
		self.con, self.str, self.dex, self.int, self.cha, self.mspeed, self.reg = statsheet[:7]

		# Initialize Resistances
		self.frostr, self.firer, self.poisonr, self.acidr, self.shockr, self.expr = statsheet[7]

		# Initialize Color
		self.color = statsheet[8]

		# Class bonus
		if CharacterInfo.class_progression[self.pclass][0] == 'con': self.con += 1
		elif CharacterInfo.class_progression[self.pclass][0] == 'str': self.str += 1
		elif CharacterInfo.class_progression[self.pclass][0] == 'dex': self.dex += 1
		elif CharacterInfo.class_progression[self.pclass][0] == 'int': self.int += 1
		elif CharacterInfo.class_progression[self.pclass][0] == 'cha': self.cha += 1

		self.maxhp = 5 + self.con * 5 + self.str
		self.hp = self.maxhp

		self.maxmana = 4 + 4 * self.int
		self.mana = self.maxmana

		# Regen
		self.hregen, self.mregen = 0, 0

		# Mount
		self.rider, self.mount = None, None

		# Inventory, Spells
		self.inventory, self.spells, self.abilities, self.cooldowns = [], ["godhammer","deathmark","frost breath"], ["double shot"], []

		# Initialize Equipment
		self.wielding, self.hands, self.total_hands, self.quivered = [], 2, 2, None

		# Manage God-Cleaver Passive
		self.god_cleaver_hits = 0

		# Apply Racial Passives
		self.skill_points, self.innate_ac, self.traits = 0, 0, []
		self.racial_bonuses()

		# Innate Equipment
		for equipment in innate_equipment:
			if equipment in Weapons.array: self.give_weapon(equipment)
			elif equipment[0] in Spells.spells and equipment[1]: self.abilities.append(equipment[0])
			elif equipment[0] in Spells.spells and not equipment[1]: self.spells.append(equipment[0])

		# Class Equipment
		for item in CharacterInfo.race_starting_equipment[self.game.race][CharacterInfo.class_list.index(self.game.pclass)]:
			if item in Ammos.array:
				data = Ammos.array[item]
				if data[2] in Ammos.thrown_amclasses: number = 6
				else: number = 20
				self.inventory.append(Ammo(item,data[0],data[1],data[2], number,data[3],None))
				self.quivered = self.inventory[-1]
			elif item in Weapons.array:
				self.give_weapon(item)
			elif item in Shields.array:
				data = Shields.array[item]
				try: brand = data[6]
				except IndexError: brand = None
				self.wielding.append(Shield(self.game,item,data[0],data[1],data[2],data[3],data[4],data[5],None,brand))
				self.hands -= data[2]
			elif item in Armors.array:
				data = Armors.array[item]
				try: brand = data[6]
				except IndexError: brand = None
				self.equipped_armor = Armor(item,data[0],data[1],data[2],data[3],data[4],data[5],None,brand)
			elif type(item) == tuple:
				if item[1]: self.abilities.append(item[0])
				else: self.spells.append(item[0])


		# Give Class Tome
		tome = 'Tome of the ' + self.game.pclass
		data = Tomes.array[tome]
		self.inventory.append(Tome(data[0], tome, '_', data[2], data[1], None))

		# Give Healing Potions
		data = Potions.array["healing potion"]
		self.inventory.append(Potion("healing potion",data, None, number=2))

		# Initialize Level, XP
		self.level, self.xp, self.xp_levels = 1, 0, 12




	def read(self, tome):
		skillnums = '123456789'

		spaces = [i for i in range(25 - (2 * len(tome.spells)))]

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

				# Get color
				for school, school_spells in Spells.spell_schools.items():
					if spell[0] in school_spells:
						color_tone = Spells.school_info[school][0]
						break


				print(skillnums[tome.spells.index(spell)] + ') ' + Colors.color(spell[0], color_tone))
				print("")

			decision = rinput("Which skill will you investigate?")

			if decision in skillnums and skillnums.index(decision) < len(tome.spells):
				skill = tome.spells[skillnums.index(decision)][0]
				cost = tome.spells[skillnums.index(decision)][1]
				stype = tome.spells[skillnums.index(decision)][2]

				# Get color
				for school, school_spells in Spells.spell_schools.items():
					if skill in school_spells:
						color_tone = Spells.school_info[school][0]
						break

				print("=======================================================================================")
				print("")
				print("")
				print("")
				print(Colors.color(skill.upper(), color_tone) + "  ("+stype+") : " + str(cost) + " points")
				print("")
				print(Descriptions.skill[skill][0])
				print("")

				if skill in self.traits or skill in self.abilities or skill in self.spells:
					print("You already know this skill.")

					decision = rinput("(G)o back")

					if decision.lower() == 'g': repeat = True
				else:
					decision = rinput("You have " + str(self.skill_points) + " skill points. (B)uy or (G)o back?")

					if decision.lower() == 'g': repeat = True
					elif decision.lower() == 'b':
						if self.skill_points < cost:
							print("You do not have enough points for that.")
							spaces.pop()
							repeat = True
						else:
							if stype == 'trait': self.traits.append(skill)
							elif stype == 'spell': self.spells.append(skill)
							elif stype == 'ability': self.abilities.append(skill)
							self.skill_points -= cost

							self.game.game_log.append("You learn " + skill + "!")




	def calc_resistances(self):
		return [self.frostr + self.equipped_armor.frostr, self.firer + self.equipped_armor.firer, self.poisonr + self.equipped_armor.poisonr, self.acidr + self.equipped_armor.acidr, self.shockr + self.equipped_armor.shockr, self.expr + self.equipped_armor.expr]

	def calc_mdamage(self):
		sd = 0
		for weapon in self.wielding: sd += weapon.mdamage
		return sd

	def quiver_string(self):
		if self.quivered.brand is None:
			if self.quivered.number > 1: self.game.game_log.append("You quiver " + str(self.quivered.number) + " " + self.quivered.name + "s!")
			else: self.game.game_log.append("You quiver 1 " + self.quivered.name + "!")
		else:
			if self.quivered.number > 1: self.game.game_log.append("You quiver " + str(self.quivered.number) + " " + self.quivered.brand + ' ' + self.quivered.name + "s!")
			else: self.game.game_log.append("You quiver 1 " + self.quivered.brand + ' ' + self.quivered.name + "!")


	def racial_bonuses(self):

		# Innate bonuses
		if self.game.race == 'Black Orc': self.innate_ac += 1
		if self.game.race == 'Dragonborn': self.innate_ac += 2
		if self.game.race == 'Dread': self.innate_ac += 2
		if self.game.race == 'Hill Troll':
			self.innate_ac += 1
			self.hands, self.total_hands = 4, 4
		if self.game.race == "Terran": self.skill_points += 2


	def quiver(self, bypass=None):

		if bypass is None:

			ammo = [thing for thing in self.inventory if type(thing) == Ammo and thing != self.quivered]

			if len(ammo) != 0:
				print("=======================================================================================")
				print("                                                                     ")
				for i in range(len(ammo)): print(str(self.game.item_order[i]) + " - " + str(ammo[i]))
				print("                                                                     ")
				print("=======================================================================================")

				decision = rinput("Quiver What?")

				if decision in self.game.item_order and self.game.item_order.index(decision) < len(ammo):

					try:
						if Weapons.array[ammo[self.game.item_order.index(decision)].base_string][3] > self.total_hands:
							self.game.temp_log.append("That item is too heavy for you to quiver.")
							return
					except: pass

					# Quiver Item
					self.quivered = ammo[self.game.item_order.index(decision)]

				else: self.game.temp_log.append("That is not a valid option")

			else: self.game.temp_log.append("You have nothing to quiver.")

		else: self.quivered = bypass

		self.time += self.mspeed

		# Quiver Statement
		self.quiver_string()

	def drink(self, bypass=None):

		if bypass is None:

			potions = [thing for thing in self.inventory if type(thing) == Potion]

			if len(potions) != 0:
				print("=======================================================================================")
				print("                                                                     ")
				for i in range(len(potions)): print(str(self.game.item_order[i]) + " - " + str(potions[i]))
				print("                                                                     ")
				print("=======================================================================================")

				decision = rinput("Drink which potion?")

				if decision in self.game.item_order and self.game.item_order.index(decision) < len(potions):

					# Drink Potion
					potions[self.game.item_order.index(decision)].drink(self, self.game)

				else: self.game.temp_log.append("That is not a valid option")

			else: self.game.temp_log.append("You are carrying no potions.")

		else: bypass.drink(self, self.game)

		self.time += self.mspeed





	def fire(self, mod=None):

		# Throwing weapon
		thrown = False
		kraken = True if [weapon for weapon in self.wielding if weapon.base_string == 'Kraken'] else False

		# Manage Kraken 1
		if kraken: thrown = True


		if self.quivered is not None:

			# Manage throwing Weapons
			if self.quivered.wclass in Ammos.thrown_amclasses and not kraken:
				thrown = True
				# Create Throwing platform
				self.give_weapon(self.quivered.base_string, hands=False)



		for item in self.wielding:

			# Ranged Projectile Thrower
			if item.wclass in Weapons.ranged_wclasses or (item.wclass in Ammos.thrown_amclasses or item.base_string == 'Kraken' and mod not in {'double shot'}):


				if item.base_string == 'Kraken': item.range = 8

				# Check for quiver
				elif self.quivered is None:
					self.game.temp_log.append("You do not have the correct ammo type quivered.")
					return
				# Wrong ammo type
				elif item.wclass in Weapons.ranged_wclasses and self.quivered.wclass not in Ammos.projectile[item.wclass]:
					self.game.temp_log.append("You do not have the correct ammo type quivered.")
					if thrown: self.wielding.pop()
					return False

				units_in_range = []
				for unit in self.game.units[1:]:
					los = ai.los(self.loc, unit.loc, Maps.rooms[self.game.map.map][0], self.game)
					if los is not None and len(los) - 1 <= item.range: units_in_range.append(unit)

				# Ranged range
				if len(units_in_range) != 0:
					print("=======================================================================================")
					print("                                                                     ")
					for i in range(len(units_in_range)): print(str(self.game.item_order[i]) + " - " + units_in_range[i].name)
					print("                                                                     ")
					print("=======================================================================================")


					decision = rinput("Aim at which enemy?")

					if decision in self.game.item_order and self.game.item_order.index(decision) < len(units_in_range):

						# Choose Legal Enemy
						unit = units_in_range[self.game.item_order.index(decision)]
						self.time += item.speed
						attacks = 1
						if mod == 'double shot': attacks += 1

						# Attack
						for i in range(attacks):
							if item.base_string == 'Kraken': item.thrown = True
							item.strike(self, unit, self.game)

							# Manage Tempest
							if item.base_string == "Tempest":
								units_in_range.remove(unit)
								others = 2
								while len(units_in_range) != 0 and others > 0:
									other_unit = units_in_range[d(len(units_in_range)) - 1]
									item.strike(self, other_unit, self.game)
									units_in_range.remove(other_unit)
									others -= 1

							# Remove Ammo
							if not kraken:
								self.quivered.number -= 1
								if self.quivered.number == 0:
									self.inventory.remove(self.quivered)
									self.quivered = None

						# Remove throwing weapon
						if thrown and not kraken: self.wielding.pop()

						# Well-being
						try: self.well_being_statement(unit, self, item)
						except: pass

						# Return, to see that we used a ranged weapon
						return True

					else:
						self.game.temp_log.append("That is not a valid input")
						# Remove throwing weapon

						if thrown and not kraken: self.wielding.pop()
						return False

				else:
					self.game.temp_log.append("There are no targets in range!")

					# Remove throwing weapon
					if thrown and not kraken: self.wielding.pop()
					return False

		self.game.temp_log.append("You are not wielding a ranged weapon!")

		# Remove throwing weapon
		if thrown and not kraken: self.wielding.pop()
		return False


	def well_being_statement(self, enemy, attacker, means, estatus=True):

		# If enemy is defeated
		if enemy.hp <= 0:

			# Remove enemy
			self.game.units.remove(enemy)
			if enemy in self.game.allies: self.game.allies.remove(enemy)

			# Check for Indominbable
			if 'indominable' in enemy.currentPassives():
				enemy.hp = 1
				self.game.game_log.append(enemy.info[3] + " refuses to die!")
				return

			# If kill with weapon
			legendary = False
			if type(means) == Weapon:

				kill_weapon = means

				legendary = True if kill_weapon.legendary else False
				means = means.name

			# Flavor Text
			verb = 'slay' if attacker.name == 'you' else 'slays'
			if not legendary:
				if attacker.name == 'you': poss = "your "
				else: poss = "its "
			else:
				poss = ""
			self.game.game_log.append( attacker.info[3] + " " + verb + " " + enemy.info[0] + " with " + poss + means + "!")


			# Mounts
			if enemy.rider is not None: enemy.rider.mount = None
			elif enemy.mount is not None: enemy.mount.unit.rider = None


			# Add to weapon kill count
			try:
				kill_weapon.kills += 1

				# Manage Worldshaper
				if kill_weapon.base_string == "Worldshaper":
					attacker.mana = min(attacker.maxmana, int(attacker.mana + attacker.mana / 4))
					self.game.game_log.append(kill_weapon.name + " saps " + Colors.color('mana','lightblue') + " from the falling corpse.")

				# Manage Swiftspike
				if kill_weapon.base_string == "Swiftspike":
					attacker.mspeed = attacker.mspeed / 4
					apply(attacker, 'hastened', 5)
					self.game.game_log.append(kill_weapon.name + " grants you a burst of movement speed!")

				# Manage Soulreaper
				if kill_weapon.base_string == "Soulreaper":

					kill_progression = [20,50,90,140,200,300]
					if kill_weapon.kills in kill_progression:
						kill_weapon.damage += 1
						if kill_weapon.kills == kill_progression[-1]:
							self.game.game_log.append(kill_weapon.name + " is sated.")
							kill_weapon.brand = 'possessed'
						else: self.game.game_log.append(kill_weapon.name + " demands more blood.")

				# Manage the Talons of Belial
				if kill_weapon.base_string == "the Talons of Belial":

					# Fear Radius
					spaces, affected = set([]), []
					for x in range(-3,4):
						for y in range(-3,4):
							if enemy.loc[0] + x >= 0 and enemy.loc[1] + y >= 0: spaces.add((enemy.loc[0] + x, enemy.loc[1] + y))
					# Find units affected
					for unit in self.game.units[1:]:
						if unit.loc in spaces and unit != attacker and unit.tier < enemy.tier:
							affected.append(unit)

					if len(affected) != 0:
						for unit in affected: apply(unit, 'terrified', 5)
						self.game.game_log.append("The shredded remains of " + enemy.info[0] + " left by " + kill_weapon.name + " make its underlings flee in terror!")
			except: pass

			# Ooze Passive / Filth explosion
			if 'split' in enemy.spells: Spells.spells["split"][0]("split", enemy, enemy, self.game, Maps.rooms[self.game.map.map][0], self.game.map.room_filler)
			elif 'filth explosion' in enemy.spells: Spells.spells["filth explosion"][0]("filth explosion", enemy, enemy, self.game, Maps.rooms[self.game.map.map][0], self.game.map.room_filler)



			# Drop Loot
			enemy.drop_booty()

			# XP Gain
			self.xp += enemy.xp + int(d(self.cha) / 2)

		elif estatus:
			# Enemy is virile
			if enemy.hp / enemy.maxhp > 0.9: self.game.game_log.append(enemy.info[3] + " seems uninjured.")

			# Enemy over 70%
			elif enemy.hp / enemy.maxhp > 0.7: self.game.game_log.append(enemy.info[3] + " seems only lightly wounded.")

			# Enemy over 30%
			elif enemy.hp / enemy.maxhp > 0.3: self.game.game_log.append(enemy.info[3] + " seems moderately wounded.")

			# Enemy under 30%
			elif enemy.hp > 0: self.game.game_log.append(enemy.info[3] + " seems nearly dead!")





	def cast(self, type, array):

		print("=======================================================================================")
		print("                                                                     ")
		for i in range(len(array)):

			# Get color
			for school, school_spells in Spells.spell_schools.items():
				if array[i] in school_spells:
					color_tone = Spells.school_info[school][0]
					break

			if type == "spell": print(str(self.game.item_order[i]) + " - " + Colors.color(array[i], color_tone) + " (" + str(Spells.spells[array[i]][1]) + " mana)")
			else: print(str(self.game.item_order[i]) + " - " + Colors.color(array[i], color_tone) + " (" + str(Spells.spells[array[i]][1] * 3) + " turns)")

		print("                                                                     ")
		print("=======================================================================================")

		# Controller
		print("")
		if type == "spell": decision = rinput("Use which spell?")
		else: decision = rinput("Use which ability?")

		# Valid Spell
		if decision in self.game.item_order and self.game.item_order.index(decision) < len(array):
			spell, spell_name = Spells.spells[array[self.game.item_order.index(decision)]][0], array[self.game.item_order.index(decision)]
		else:
			self.game.temp_log.append("That is not a valid input")
			return

		# Correct color
		for school, school_spells in Spells.spell_schools.items():
			if array[self.game.item_order.index(decision)] in school_spells:
				color_tone = Spells.school_info[school][0]
				break

		# Check Mana / Kain's Pact
		if type == "spell":

			# Check Mana
			kainspact = False
			if self.mana < Spells.spells[spell_name][1]:

				# Manage Kain's Pact
				if self.equipped_armor.base_string != "Kain's Pact":
					self.game.temp_log.append("You don't have enough mana to cast that.")
					return
				else:
					print(self.equipped_armor.name + " draws power from your health!")
					kainspact = True



		# There is a target
		if Spells.spells[spell_name][3]:
			# Get units in range
			units_in_range = []
			for unit in self.game.units[1:]:
				los = ai.los(self.loc, unit.loc, Maps.rooms[self.game.map.map][0], self.game )
				if los is None: continue
				if Spells.spells[spell_name][4]:
					if len(los) - 1 <= Spells.spells[spell_name][5]: units_in_range.append(unit)
				else: units_in_range.append(unit)
			units_in_range = units_in_range[::-1]

			# Ranged range
			if len(units_in_range) != 0:
				print("                                                                     ")
				print("---------------------------------------------------------------------------------------")
				print(Colors.color(spell_name, color_tone))
				print("                                                                     ")
				print("=======================================================================================")
				print("                                                                     ")
				for i in range(len(units_in_range)):

					unit = units_in_range[i]

					print(str(self.game.item_order[i]) + " - " + unit.name)
				print("                                                                     ")
				print("=======================================================================================")



				decision = rinput("Cast " + Colors.color(spell_name, color_tone) + " at which target?")


				if decision in self.game.item_order and self.game.item_order.index(decision) < len(units_in_range):

					# Choose Legal Enemy
					unit = units_in_range[self.game.item_order.index(decision)]

				else:
					self.game.temp_log.append("That is not a valid input")
					return
			else:
				self.game.temp_log.append("There are no targets in range!")
				return
		else:
			print(Colors.color(spell_name, color_tone))
			unit = self

		# Manage life leech 1
		previous_enemy_hp = unit.hp

		if type == "spell":
			# Enemy Resist spell
			if d(100) / 100 <= max(0.05, min(0.7, (unit.cha / 2) / self.int)) and not Spells.spells[spell_name][3] and unit != self:
				self.time += Spells.spells[spell_name][2]
				if kainspact:self.hp -= Spells.spells[spell_name][1]
				else: self.mana -= Spells.spells[spell_name][1]
				self.game.game_log.append(unit.info[3] + " resists your " + spell_name + "!")

			elif spell(spell_name, self, unit, self.game, Maps.rooms[self.game.map.map][0], self.game.map.room_filler):
				if kainspact:self.hp -= Spells.spells[spell_name][1]
				else: self.mana -= Spells.spells[spell_name][1]
				self.time += Spells.spells[spell_name][2]
			else: return
		else:
			if spell(spell_name, self, unit, self.game, Maps.rooms[self.game.map.map][0], self.game.map.room_filler, True):
				self.time += Spells.spells[spell_name][2]
				self.cooldowns.append( [spell_name, Spells.spells[spell_name][1] * 3] )
				self.abilities.remove(spell_name)
			else: return


		# Manage the Black Cross 1
		if type == "spell":
			for unit in self.game.units:
				for item in unit.wielding:
					if item.base_string == "the Black Cross":
						self.game.game_log.append("Yet " + item.name + " condemns your use of magic, it " + Colors.color("ignites","fire") + " your flesh!")
						apply(self, "aflame", 3)



		# Manage Longfang
		if type == "spell":
			for weapon in self.wielding:
				if weapon.base_string == "Longfang" and len(weapon.passives) == 0:
					for school, spells in Spells.spell_schools.items():
						if spell_name in spells:
							if school in Spells.school_info:
								if Spells.school_info[school][1] is not None:
									weapon.passives = [[Spells.school_info[school][1] , 1]]
									weapon.brand = Spells.school_info[school][1]
									self.game.game_log.append(weapon.name + " absorbs the power of your spell and becomes " + Colors.color(weapon.brand, Brands.colors[weapon.brand]) + "!")
									break

		# Manage life leech 2
		if unit.hp < previous_enemy_hp and unit != self and "life leech" in self.traits:
			heal = min( d(int((previous_enemy_hp - unit.hp) / 2)) , self.maxhp - self.hp)
			self.hp += heal
			if heal > 0: self.game.game_log.append("Your dark magic " + Colors.color("leeches", "purple") + " " + str(heal) + " health from " + unit.info[3] + ".")

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
		self.game.game_log.append("You feel hardier...")

	def inc_str(self):
		self.str += 1
		self.hp +=  1
		self.maxhp += 1
		self.game.game_log.append("You feel stronger...")

	def inc_dex(self):
		self.dex += 1
		self.game.game_log.append("You feel more agile...")

	def inc_int(self):
		self.int += 1
		self.mana += 4
		self.maxmana += 4
		self.game.game_log.append("You feel smarter...")

	def inc_cha(self):
		self.cha += 1
		self.game.game_log.append("You feel more charismatic...")







	def check_level_up(self):

		# See if enough xp for a level up
		while self.xp >= self.xp_levels:

			# Increment Level
			self.level += 1
			self.skill_points += 1
			try:
				for band in Bands.dicto[self.level]:
					try: self.game.bands.remove(band)
					except: self.game.bands.append(band)
			except IndexError: pass

			# Gain HP/mana
			bonushp = d(self.con)
			self.hp += 2 + bonushp
			self.maxhp += 2 + bonushp
			self.mana += 2
			self.maxmana += 2

			# Racial level-ups
			self.racial_level_bonuses()


			print("You've leveled up to level " + str(self.level) + "!")
			self.game.game_log.append("You've leveled up to level " + str(self.level) + "!")
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
				if item_type == Weapon: self.game.temp_log.append("You're not carrying any other weapons!")
				elif item_type == Armor: self.game.temp_log.append("You're not carrying any other armor!")
				return

			else:
				print("=======================================================================================")
				print("                                                                     ")
				for i in range(len(item_array)): print(self.game.item_order[i] + " - " + str(item_array[i]))
				print("                                                                     ")
				print("=======================================================================================")


				decision = rinput("Equip which item?")

				if decision in self.game.item_order and self.game.item_order.index(decision) < len(item_array):
					item = item_array[self.game.item_order.index(decision)]
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
			if item.wclass in Weapons.ranged_wclasses and item.hands > 1 or item.wclass in {'gauntlets','claw gauntlets'}:
				# Remove current weapons
				for weap in carrying:
					self.wielding.remove(weap)
					self.inventory.append(weap)

				# Wield Weapon
				self.hands = 0
				self.wielding.append(item)
				self.inventory.remove(item)
				if item.legendary: self.game.game_log.append("You draw " + item.name + "!")
				else: self.game.game_log.append("You draw your " + item.name + ".")

				self.time += self.mspeed

			# Not enough total hands
			elif item.hands > self.total_hands or item.hands > 1 and item.wclass != 'bastard sword' and self.race in {'Gnome','Hobbit'}:
				self.game.temp_log.append("You cannot wield that weapon!")

			# Not enough FREE Hands
			elif self.hands < item.hands or len(carrying) == 2:

				# Already carrying something
				if len(carrying) == 2 and item.hands < self.total_hands:

					# Equipped string UI
					equipped = ""
					for i in range(len(carrying)):
						if len(equipped) != 0: equipped += ', ' + '(' + str(self.game.item_order[i]) + ") " +  str(carrying[i])
						else: equipped += '(' + str(self.game.item_order[i]) + ") " + str(carrying[i])

					print("")
					decision = rinput("Swap for " + equipped + "?")

					if decision in self.game.item_order and self.game.item_order.index(decision) < len(carrying):
						ditem = carrying[self.game.item_order.index(decision)]

						# Remove chosen item
						if ditem.legendary: self.game.game_log.append("You put away " + ditem.name + '.')
						else: self.game.game_log.append("You put away the " + ditem.name + '.')
						self.wielding.remove(ditem)
						self.inventory.append(ditem)
						self.hands += ditem.hands
					else:
						self.game.temp_log.append("That is not a valid option.")
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
				if item.legendary: self.game.game_log.append("You draw " + item.name + "!")
				else: self.game.game_log.append("You draw your " + item.name + ".")

			# Enough free hands
			else:
				# Wield item
				self.wielding.append(item)
				self.inventory.remove(item)
				self.hands -= item.hands
				if item.legendary: self.game.game_log.append("You draw " + item.name + "!")
				else: self.game.game_log.append("You draw your " + item.name + ".")


			# Manage Martial Draw
			if 'martial draw' in self.traits and type(item) == Weapon:
				x, y = self.loc
				squares = []
				for i in range(3):
					for j in range(3):
						squares.append([x - 1 + i, y - 1 + j])
				targets = []
				for unit in self.game.units[1:]:
					if unit in self.game.allies: continue
					if [unit.loc[0], unit.loc[1]] in squares:
						targets.append(unit)

				if len(targets) != 0:
					target = targets[d(len(targets)) - 1]
					self.wielding[-1].strike(self, target, self.game)



		# Equip Armor
		elif type(item) == Armor:
			self.inventory.append(self.equipped_armor)
			self.equipped_armor = item
			self.inventory.remove(item)
			if item.legendary: self.game.game_log.append("You put on " + item.name + "!")
			else: self.game.game_log.append("You put on your " + item.name + "!")

		# Take a turn
		self.time += self.mspeed

	def stash(self, bypass=None):

		if bypass is None:

			# Carrying
			carrying = [thing for thing in self.wielding if thing.hands > 0]

			if len(carrying) > 0:

				# Equipped string UI
				equipped = ""
				for i in range(len(carrying)):
					if len(equipped) != 0: equipped += ', ' + '(' + str(self.game.item_order[i]) + ") " +  str(carrying[i])
					else: equipped += '(' + str(self.game.item_order[i]) + ") " + str(carrying[i])

				print("")
				print("Put what into your inventory?")
				decision = rinput(equipped)

				if decision in self.game.item_order and self.game.item_order.index(decision) < len(carrying):
					ditem = carrying[self.game.item_order.index(decision)]


				else:
					self.game.temp_log.append("That is not a valid option.")
					return

			else:
				self.game.temp_log.append("You are not carrying anything.")
				return
		elif type(bypass) == Ammo:
			if self.quivered.number == 1: self.game.game_log.append("You put away the " + self.quivered.name + '.')
			else: self.game.game_log.append("You put away the " + self.quivered.name + 's.')
			self.quivered = None
			self.time += self.mspeed
			return
		else: ditem = bypass

		# Remove chosen item
		if ditem.legendary: self.game.game_log.append("You put away " + ditem.name + '.')
		else: self.game.game_log.append("You put away the " + ditem.name + '.')
		self.wielding.remove(ditem)
		self.inventory.append(ditem)
		self.hands += ditem.hands
		self.time += self.mspeed

	# noinspection PyTypeChecker
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
				weaps,shields,armors,ammos,tomes,potions = [],[],[],[],[],[]
				for item in items:
					if type(item) == Ammo: ammos.append(item)
					elif type(item) == Weapon: weaps.append(item)
					elif type(item) == Shield: shields.append(item)
					elif type(item) == Armor: armors.append(item)
					elif type(item) == Tome: tomes.append(item)
					elif type(item) == Potion: potions.append(item)
				combined = weaps + shields + armors + ammos + tomes + potions
				j = 0

				print("=======================================================================================")
				print("                                                                     ")
				if len(weaps) != 0: print("Weapons")
				for i in range(len(weaps)):
					print(self.game.item_order[j] + " - " + str(weaps[i]))
					j += 1
				if len(shields) != 0: print("Shields")
				for i in range(len(shields)):
					print(self.game.item_order[j] + " - " + str(shields[i]))
					j += 1
				if len(armors) != 0: print("Armor")
				for i in range(len(armors)):
					print(self.game.item_order[j] + " - " + str(armors[i]))
					j += 1
				if len(ammos) != 0: print("Ammo")
				for i in range(len(ammos)):
					print(self.game.item_order[j] + " - " + str(ammos[i]))
					j += 1
				if len(tomes) != 0: print("Tomes")
				for i in range(len(tomes)):
					print(self.game.item_order[j] + " - " + str(tomes[i]))
					j += 1
				if len(potions) != 0: print("Potions")
				for i in range(len(potions)):
					print(self.game.item_order[j] + " - " + str(potions[i]))
					j += 1
				print("                                                                     ")
				print("=======================================================================================")

				decision = rinput("Inspect an item?")


				if decision in self.game.item_order and self.game.item_order.index(decision) < len(combined):
					ditem = combined[self.game.item_order.index(decision)]


					print("")
					print("=======================================================================================")

					# Details
					ditem.details()

				else:
					self.game.temp_log.append("That is not a valid option.")
					return

				# Inventory Options

				# Ammo
				if type(ditem) == Ammo:
					if ditem == self.quivered:
						decision = rinput("(S)tow, (D)rop, or (G)o back?")
						if decision.lower() == 's': self.stash(ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						else: self.game.temp_log.append("That is not a valid option.")
					else:
						decision = rinput("(Q)uiver, (D)rop, or (G)o back?")
						if decision.lower() == 'q': self.quiver(ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						else: self.game.temp_log.append("That is not a valid option.")
				# Weapon / Shield
				elif type(ditem) == Weapon or type(ditem) == Shield:
					if ditem in self.wielding:
						decision = rinput("(S)tow, (D)rop, or (G)o back?")
						if decision.lower() == 's': self.stash(ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						else: self.game.temp_log.append("That is not a valid option.")
					else:
						decision = rinput("(W)ield, (D)rop, or (G)o back?")
						if decision.lower() == 'w': self.wield(Weapon,ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						else: self.game.temp_log.append("That is not a valid option.")
				# Tome
				elif type(ditem) == Tome:
					if ditem in self.wielding:
						decision = rinput("(S)tow, (R)ead, (D)rop, or (G)o back?")
						if decision.lower() == 's': self.stash(ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						elif decision.lower() == 'r': self.read(ditem)
						else: self.game.temp_log.append("That is not a valid option.")
					else:
						decision = rinput("(W)ield, (R)ead, (D)rop, or (G)o back?")
						if decision.lower() == 'w': self.wield(Weapon,ditem)
						elif decision.lower() == 'd': self.drop(ditem)
						elif decision.lower() == 'g': go_back = True
						elif decision.lower() == 'r': self.read(ditem)
						else: self.game.temp_log.append("That is not a valid option.")
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
				# Potion
				if type(ditem) == Potion:
					decision = rinput("(D)rink, or (G)o back?")
					if decision.lower() == 'd': self.drink(ditem)
					elif decision.lower() == 'g': go_back = True
					else: self.game.temp_log.append("That is not a valid option.")


		else: self.game.temp_log.append("You have nothing in your inventory!")


	def pick_up(self, item):
		item.loc = None
		already_in = False
		if type(item) == Ammo:
			for thing in self.inventory:
				if type(thing) == Ammo and thing.base_string == item.base_string and thing.brand == item.brand:
					thing.number += item.number
					already_in = True
					break
		elif type(item) == Potion:
			for thing in self.inventory:
				if type(thing) == Potion and thing.base_string == item.base_string:
					thing.number += item.number
					already_in = True
					break

		self.game.items.remove(item)
		if not already_in: self.inventory.append(item)
		if type(item) in {Ammo, Potion}:
			if item.number > 1: self.game.game_log.append("You pick up " + str(item.number) + ' ' + item.name + "s.")
			else: self.game.game_log.append("You pick up the " + item.name + ".")
		elif item.legendary:
			self.game.game_log.append("You pick up " + item.name + "!")
		else:
			self.game.game_log.append("You pick up the " + item.name + ".")
		self.time += self.mspeed

	def drop(self,item):
		item.loc = self.loc
		if item == self.quivered: self.quivered = None
		else:
			try: self.hands += item.hands
			except: pass

		try: self.wielding.remove(item)
		except: del self.inventory[self.inventory.index(item)]


		self.game.items.append(item)
		try:
			article = "" if item.legendary else "the "
		except: article = "the "
		try: self.game.game_log.append("You drop " + article + str(item.number) + ' ' + item.name + "s")
		except: self.game.game_log.append("You drop " + article + item.name)
		self.time += self.mspeed

	# noinspection PyTypeChecker
	def give_weapon(self, weapon, hands=True):
		data = Weapons.array[weapon]

		# Manage Brand + Probability
		try: brand = data[8]
		except IndexError: brand = None
		try: prob = data[9]
		except IndexError: prob = None

		if hands: self.hands -= data[3]

		# Create Weapon Object
		if data[2] in Weapons.ranged_wclasses and data[3] > 0:
			self.inventory.append(Weapon(self.game, weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],None, brand, prob))
			return self.inventory[-1]
		else:
			self.wielding.append(Weapon(self.game, weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], None, brand, prob))
			return self.wielding[-1]


	def calc_AC(self):
		return d(int(max(1, (self.equipped_armor.armor_rating + self.equipped_armor.enchantment) / 2))) + int((self.equipped_armor.armor_rating + self.equipped_armor.enchantment) / 2) + self.innate_ac

	def currentPassives(self):
		current = [name for name, count in self.passives]
		return current

	def removePassive(self, specified):
		for passive in self.passives:
			if passive[0] == specified:
				self.passives.remove(passive)
				return True
		return False
