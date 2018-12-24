from Maps import Maps
from ai import *

from bestiary import Monsters, Bands
from codex import Weapons, Brands
from Spells import Spells
from CharacterInfo import CharacterInfo
from Descriptions import Descriptions
from Colors import Colors
from Player import Player
from Weapon import Weapon
from Armor import Armor
from Shield import Shield
from Trap import Trap
from Chest import Chest
from Monster import Monster
from RoomFiller import RoomFiller

from copy import deepcopy

import sys, os
import termios, fcntl
import select



'''
TODO:

- fix BFS
- Change frost breath
- Helmets
- More Potions
- hand crossbows, maybe make it so can fire 2 at once?
- Legendary chops arrows from air, Dominus
- Nerf dual-wielding
- Buff ability template, enemies casting buffs on already-buffed bois
- enemy behavior types
- Finish class tomes
'''


# noinspection PyBroadException
class Map:

	def __init__(self, game, room):

		self.map, self.game = room, game

		self.def_map_array = Maps.rooms[self.map][0]
		self.map_array = deepcopy(self.def_map_array)

		self.entry_point, self.exits = Maps.rooms[self.map][2], Maps.rooms[self.map][3]


		self.adjacent = {self.entry_point: None}
		for point in self.exits[1:]: self.adjacent[point] = None

		self.objects, self.allies = [], []

		self.filled = False

		self.room_filler = None

		self.graph = {}

		self.construct_graph()

	def construct_graph(self):
		height = len(self.map_array)
		width = len(self.map_array[0])


		for original_x in range(width):

			for original_y in range(height):

				for pair in [(0,1),(1,0),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:

					adx = pair[0] + original_x
					ady = pair[1] + original_y
					if 0 <= adx < width and 0 <= ady < height and (original_x != adx or original_y != ady):
						try: self.graph[(original_x,original_y)].append((adx,ady))
						except: self.graph[(original_x,original_y)] = [(adx,ady)]

	def fill(self):
		self.room_filler = RoomFiller(self.game.player.level, (15,2), self.map, self.game)
		self.room_filler.place()

	@staticmethod
	def parse(line):

		# Parse for display
		art = ""
		for char in line: art += char
		return art


	def display(self):

		# Reset Map
		self.map_array = deepcopy(self.def_map_array)

		# Place items
		for item in game.items:

			try:
				y, x = item.loc[0], item.loc[1]
				self.map_array[x][y] = Colors.color(item.rep, item.color)
			except: game.items.remove(item)
		# Place each unit on the map
		for unit in game.units[::-1]:
			y, x = unit.loc[0], unit.loc[1]

			if unit.rider is not None: self.map_array[x][y] = Colors.fullcolor(unit.rider.rep, unit.rider.color,unit.color )
			elif unit.mount is not None: self.map_array[x][y] = Colors.fullcolor(unit.rep, unit.color,unit.mount.unit.color )
			else: self.map_array[x][y] = Colors.color(unit.rep, unit.color)


		# Display the map
		for line in self.map_array: print("        " + self.parse(line))

	def change_room(self, new_room):

		room, new_location = new_room[0], new_room[1]
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
		for room_object in room.objects:
			game.units.append(room_object) if type(room_object) == Monster else game.items.append(room_object)
			if room_object in room.allies: game.allies.append(room_object)

		game.map = room

		# Place boy on map
		if new_location == Maps.rooms[room.map][2]: self.game.player.loc = (new_location[0] + 1, new_location[1])
		else: self.game.player.loc = (new_location[0] - 1, new_location[1])

	# noinspection PyTypeChecker
	def new_room(self, coordinates):

		# Store units
		for unit in game.units[1:]:
			if type(unit) == Monster: self.objects.append(unit)
			if unit in game.allies: self.allies.append(unit)

		for item in game.items: self.objects.append(item)

		# Clear units
		game.units, game.allies, game.items = [game.player], [game.player], []

		# Make new Map
		pot_maps = Maps.sizes[Maps.rooms[self.map][3][0][d(len(Maps.rooms[self.map][3][0])) - 1]]
		new_map = Map(self.game,pot_maps[ d(len(pot_maps)) - 1])
		game.map = new_map

		# Entry Point
		self.adjacent[coordinates] = (new_map, new_map.entry_point)
		new_map.adjacent[new_map.entry_point] = (self, coordinates)
		self.game.player.loc = (new_map.entry_point[0] + 1, new_map.entry_point[1])

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
			if loc == unit.loc: return False
		return True



class Game:

	def __init__(self):

		# Manage Constants
		self.race = None
		self.pclass = None
		self.player = None

		self.map = Map(self, 'starting_room')
		self.state = 'ongoing'
		self.room = 0
		self.bands = Bands.dicto[1]
		self.room_filler = None

		# Initiate Prev
		self.prev_valid_turn = True

		# Manage Units
		self.units, self.allies, self.items, self.seen = [], [], [], set([])
		self.legendaries_to_spawn = [weapon for weapon in Weapons.legendaries if weapon not in Weapons.enemy_legendaries]

		# Manage Game Log
		self.game_log, self.temp_log = [], []
		self.after_hit = []

		# item order
		self.item_order = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


	def character_select(self, info=False):
		for i in range(27):
			print("")
		print("GNG")
		print("---------------------------")
		print("")
		i, record = 0, {}
		for race, stats in CharacterInfo.races.items():
			print(str(self.item_order[i]) + ") " + Colors.color(race, CharacterInfo.races[race][0][-1]))
			if info: print( Colors.color(Descriptions.races[race],CharacterInfo.races[race][0][-1] ) )
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

			go_back = True

			while go_back:

				for i in range(27):
					print("")
				print("GNG")
				print("---------------------------")

				print(Colors.color(self.race, CharacterInfo.races[self.race][0][-1]) + "      (Press spacebar to rechoose)")
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
					self.pclass = record[class_decision]

					# Create Player
					self.player = Player(CharacterInfo.races[self.race][0], CharacterInfo.races[self.race][1], CharacterInfo.races[self.race][2], self)

					self.player.race = self.race
					self.player.pclass = self.pclass
					self.units.append(self.player)
					self.allies.append(self.player)

					go_back = False

		except IndexError:
			self.character_select(info)


	def run(self):
		while self.state == 'ongoing':

			if not self.map.filled:
				self.map.fill()
				self.map.filled = True

			#  Turn Finder
			min_time = self.player.time
			indices = []
			for i in range(len(game.units)):
				unit = game.units[i]
				if unit.time < min_time:
					indices = [i]
					min_time = unit.time
				elif unit.time == min_time: indices.append(i)

			if self.player.time == 0 and min_time == 0: self.prev_valid_turn = False
			else: self.prev_valid_turn = True

			for index in indices:
				try: tunit = game.units[index]
				except IndexError: continue

				if self.prev_valid_turn: self.check_passives(tunit)
				if tunit.time != min_time: continue

				if type(tunit) == Monster:
					if tunit.hp > 0: tunit.turn(self)
				elif type(tunit) == Player: self.player_turn(self.map)

			for unit in game.units: unit.time -= min_time



	def player_turn(self, map):


		def action(move):
			x, y = self.player.loc[0], self.player.loc[1]


			# Base Case
			if move in 'hHjJkKlLyYuUbBnN,.wWfrsdSaqi+':

				# Attack Move
				if move in "hjklyubn": self.atk_mv(map, movement(move, self.player.loc) )

				# GOD MODE
				elif move == '+':
					self.player.innate_ac += 200
					game.game_log.append("You're no fun")
					self.player.equipped_armor.mdefense += 200

				# drink
				elif move == 'd': self.player.drink()


				# Run Right
				elif move == 'L':
					if len(game.units) == len(game.allies):
						while map.can_move((x + 1, y)):
							if map.square_identity((x + 1, y)) != '+':
								action('l')
								x, y = self.player.loc[0], self.player.loc[1]
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Up
				elif move == 'K':
					if len(game.units) == len(game.allies):
						while map.can_move((x, y - 1)):
							if map.square_identity((x, y - 1)) != '+':
								action('k')
								x, y = self.player.loc[0], self.player.loc[1]
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Down
				elif move == 'J':
					if len(game.units) == len(game.allies):
						while map.can_move((x, y + 1)):
							if map.square_identity((x, y + 1)) != '+':
								action('j')
								x, y = self.player.loc[0], self.player.loc[1]
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run Left
				elif move == 'H':
					if len(game.units) == len(game.allies):
						while map.can_move((x - 1, y)):
							if map.square_identity((x - 1, y)) != '+':
								action('h')
								x, y = self.player.loc[0], self.player.loc[1]
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run UL
				elif move == 'Y':
					if len(game.units) == len(game.allies):
						while map.can_move((x - 1, y - 1)):
							if map.square_identity((x - 1, y - 1)) != '+':
								action('y')
								x, y = self.player.loc[0], self.player.loc[1]
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run UR
				elif move == 'U':
					if len(game.units) == len(game.allies):
						while map.can_move((x + 1, y - 1)):
							if map.square_identity((x + 1, y - 1)) != '+':
								action('u')
								x, y = self.player.loc[0], self.player.loc[1]
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run DL
				elif move == 'B':
					if len(game.units) == len(game.allies):
						while map.can_move((x - 1, y + 1)):
							if map.square_identity((x - 1, y + 1)) != '+':
								action('b')
								x, y = self.player.loc[0], self.player.loc[1]
								self.player.time = 0
								self.check_passives(self.player)
							else: break
					else:
						game.temp_log.append("There are enemies nearby!")
				# Run DR
				elif move == 'N':
					if len(game.units) == len(game.allies):
						while map.can_move((x + 1, y + 1)):
							if map.square_identity((x + 1, y + 1)) != '+':
								action('n')
								x, y = self.player.loc[0], self.player.loc[1]
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
						if len(self.player.cooldowns) > 0: game.temp_log.append("All your abilities are on cooldown.")
						else: game.temp_log.append("You don't have any abilities.")
				# wield
				elif move == 'w':
					self.player.wield(Weapon)
					# Manage Kraken 8
					if len(self.player.wielding) > 0:
						if self.player.wielding[-1].base_string == 'Kraken': self.player.wielding[-1].thrown = False
				# Wear
				elif move == 'W': self.player.wield(Armor)
				# Stash
				elif move == "S": self.player.stash()
				# inventory
				elif move == "i": self.player.inventoryize()
				# Investigate
				elif move == ',': self.investigate()
				# Wait
				elif move == '.': self.player.time += self.player.mspeed
				# rest
				elif move == 'r':
					if len(game.units) == len(game.allies):
						while self.player.hp < self.player.maxhp or self.player.mana < self.player.maxmana:
							action('.')
							self.check_passives(self.player)
						game.temp_log.append("You feel well-rested")
						self.player.time = 0
					else: game.temp_log.append("There are enemies nearby!")

				# Manage Kraken 7
				# TODO: UPDATE THIS LIST WHENEVER YOU ADD MORE ACTIONS!!!!!!!!
				carrying = [weapon for weapon in self.player.wielding if weapon.hands != 0]
				if move not in 'fiwW+d':
					for unit in game.units[1:]:
						for item in unit.inventory:
							if item.base_string == 'Kraken':
								if item.thrown and (self.player.hands >= 1 and self.player.race != 'Hill Troll' or len(carrying) != 2 and self.player.hands >= 1 and self.player.race == 'Hill Troll'):
									unit.inventory.remove(item)
									damage = d(item.damage)

									# Apply Effect
									unit.hp -= damage
									apply(unit, 'immobile', 2, stacking = True)

									self.game_log.append(item.name + ' rips out of ' + unit.info[0] + ', dealing ' + str(damage) + ' damage, and returns to your hand!' )
									self.player.wielding.append(item)
									self.player.hands -= 1
									item.thrown = False
									self.player.well_being_statement(unit, self.player, item, self)
									break
					for item in self.items:
						if type(item) != Chest:
							if item.base_string == 'Kraken':
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

		log_select = self.game_log[((len(Maps.rooms[game.map.map][0]) - 25) + len(self.temp_log)):]
		print("=======================================================================================")

		# Display Game Log
		for line in log_select: print(line)
		for line in self.temp_log: print(line)

		# Reset Temp Log
		self.temp_log = []

		# Check level-up
		self.player.check_level_up()


		print("=======================================================================================")
		print("                                                                     ")

		# Display map
		self.map.display()
		print("                                                                     ")


		# Print HP / Mana / Wielding / Wearing
		weapon_string = ""

		for item in self.player.wielding:
			if item.hands != 0:

				# Hand String Formulation
				hands = item.hands

				# Hill Troll Passive
				if self.player.race == "Hill Troll":
					if item.hands >= 3: hands = 2
					elif item.hands == 2: hands = 1

				weapon_string += ' ' + str(item) + " (" + str(hands) + "h)"

		# Wielding Nothing
		if weapon_string == "": weapon_string = " none"

		# Quiver String
		if self.player.quivered is None: quivered_string = " none"
		else:
			quivered_string = " " + str(self.player.quivered)

		hp_space = "              "
		for i in range(len(str(self.player.hp)) + len(str(self.player.maxhp))): hp_space = hp_space[:-1]

		mana_space = "              "
		for i in range(len(str(self.player.mana)) + len(str(self.player.maxmana))): mana_space = mana_space[:-1]




		# Check for indominable!
		if self.player.hp <= 0:
			for name, count in self.player.passives:
				if name == 'indominable':
					game.game_log.append("You refuse to die!")
					self.player.hp = 1

		if self.player.hp < self.player.maxhp / 3.2: hp_color = 'red'
		elif self.player.hp < self.player.maxhp / 1.6: hp_color = 'yellow'
		elif self.player.hp <= self.player.maxhp: hp_color = 'green'
		else: hp_color = 'fire'


		print("Level " + str(self.player.level) + " " + self.player.race + " " + self.player.pclass)
		if self.player.hp <= self.player.maxhp: print("HP    " + Colors.color(str(self.player.hp)+ "/" + str(self.player.maxhp),hp_color) + hp_space + "Wielding:" + weapon_string + "         Armor: " + str(self.player.equipped_armor))
		else: print("HP    " + Colors.color(self.player.hp, hp_color) + Colors.color("/" + str(self.player.maxhp), 'green') + hp_space + "Wielding:" + weapon_string + "         Armor: " + str(self.player.equipped_armor))
		print("MANA  " + Colors.color(str(self.player.mana) + "/" + str(self.player.maxmana),'lightblue') + mana_space + "Quivered:" + quivered_string)

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
					if item.base_string not in Weapons.legendaries:
						if item.base_string[0].lower() in {'a','e','i','o','u'}:
							enemy_article = 'an '
						else: enemy_article = 'a '
					else: enemy_article = ''
					if wielding == "" and item.hands > 0:
						wielding += enemy_article + item.name
					elif item.hands > 0: wielding += (", " + enemy_article + item.name)

				if unit.namestring in Monsters.uniques:
					article = ''
				elif unit.namestring[0].lower() in {'a','e','i','o','u'}:
					article = 'an '
				else:
					article = 'a '

				if len(wielding) == 0:
					if unit.mount is not None: game.game_log.append("You see " + article + unit.name + " riding a " + unit.mount.unit.name + ", wearing " + unit.equipped_armor.name)
					else: game.game_log.append("You see " + article + unit.name + ", wearing " + unit.equipped_armor.name)
				else:
					if unit.mount is not None:game.game_log.append("You see " + article + unit.name + " riding a " + unit.mount.unit.name + ", wearing " + unit.equipped_armor.name + ", wielding " + wielding)
					else: game.game_log.append("You see " + article + unit.name + ", wearing " + unit.equipped_armor.name + ", wielding " + wielding)
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


	def atk_mv(self, map, coordinates):
		# Find melee weapons
		weapons = [item for item in self.player.wielding[::-1] if
				 type(item) == Weapon and item.wclass not in Weapons.ranged_wclasses]
		carrying = [item for item in self.player.wielding[::-1] if type(item) in {Weapon, Shield} and item.hands > 0]

		# Manage Invictus 1
		for item in carrying:
			if item.base_string == "Invictus":
				weapons.append(Weapon(self, "Invictus", "}", "gold", "shield", item.hands, item.enchantment, 10, 0, 0.9, None))

		# Initial weapons
		initial_weapons = len(weapons)

		if map.square_identity(coordinates) in {'|', '-', ' ', '#', '_'}: return

		if map.square_identity(coordinates) == '+':
			if map.adjacent[coordinates] is None:
				self.map.new_room(coordinates)
				self.player.time += 1
				return '+'
			else:
				self.map.change_room(map.adjacent[coordinates])
				self.player.time += 1
				return '+'

		# Check if square is occupied for ATTACK
		for unit in self.units:

			# Make sure it's a monster and adjacent to it
			if coordinates == unit.loc and type(unit) == Monster:

				# Equip fists
				if len(carrying) == 0 or (
						len(carrying) == 1 and self.player.race == "Hill Troll" and weapons[-1].wclass not in {"gauntlets", "claw gauntlets"} or type(
						carrying[-1]) == Shield and len(carrying) == 1):
					if len(carrying) == 0 and self.player.race == "Hill Troll":
						fists = self.room_filler.give_weapon(self.player, 'fist smash')
						weapons.append(fists)
					else:
						fists = self.player.give_weapon('fist')
						weapons.append(fists)

				# Attack with each weapon
				ranged = True
				for item in weapons:
					ranged = False
					item.strike(self.player, unit, game)
					if unit.hp <= 0: break

				# Manage Wraithform
				for passive in self.player.passives:
					if passive[0] == 'wraithform':
						self.player.passives.remove(passive)
						self.game_log.append("You break from the material plane!")

				# Not wielding melee weapon
				if ranged:
					self.temp_log.append("You are not wielding any melee weapons.")
					return

				# Enemy Well-being Statement
				try:
					self.player.well_being_statement(unit, self, item, self)
				except:
					pass

				# Unequip fists
				while len(weapons) > initial_weapons:
					self.player.wielding.pop()
					weapons.pop()
				# Unarmed wspeed
				max_attack_speed = 0.9 - (0.05 * self.player.dex)

				# Calc Attack Speed
				if len(weapons) != 0:
					max_attack_speed = 0
					for weapon in weapons:
						if weapon.speed > max_attack_speed and weapon.wclass not in Weapons.ranged_wclasses: max_attack_speed = weapon.speed

				# Attack time
				self.player.time += max_attack_speed

				# Don't Move
				return

		# Manage Immobile
		for name, count in self.player.passives:
			if name == 'immobile':
				self.temp_log.append("You can't move!")
				return

		# Check for Traps
		for item in self.items:
			if type(item) == Trap and item.loc == coordinates:
				item.trip(self)

		# Check whats on the ground
		ground_booty = ""

		for item in self.items:

			if coordinates == item.loc and type(item) == Chest:
				if item.opened:
					self.game_log.append("You see here an opened chest")
				else:
					article = "an" if item.chest_type[0] in {'a', 'e', 'i', 'o', 'u'} else 'a'
					self.game_log.append("You see here " + article + " " + item.chest_type + " chest")

			# Look for loot on the ground in case of a move
			elif coordinates == item.loc:
				if len(ground_booty) == 0:
					ground_booty += str(item)
				else:
					ground_booty += ', ' + str(item)

		# Add ground loot to the log
		if len(ground_booty) != 0: self.game_log.append("You see here: " + ground_booty)

		# Manage Lances
		if self.player.mount is not None:
			for weapon in weapons:
				if weapon.wclass == 'lance':
					for unit in self.units[1:]:
						if unit.loc == (
						self.loc[0] - 2 * (self.loc[0] - coordinates[0]), self.loc[1] - 2 * (self.loc[1] - coordinates[1])):
							weapon.strike(self, unit, game, False)
							break

		# Manage Furious Charge
		elif "furious charge" in self.player.traits:
			for unit in self.units[1:]:
				if unit.loc == (self.loc[0] - 2 * (self.loc[0] - coordinates[0]), self.loc[1] - 2 * (self.loc[1] - coordinates[1])):
					for weapon in weapons: weapon.strike(self, unit, game)
					break

		# move unit
		self.player.loc = coordinates
		self.player.time += self.player.mspeed


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
				print(game.item_order[i] + sign + str(drops[i]))
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
			print("Pick up which items?")
			inp, outp, err = select.select([sys.stdin], [], [])
			decision = sys.stdin.read()

			# Reset the terminal:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
			fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

			if decision in {'1','2','3','4','5','6','7','8','9'}:
				leave = True
			elif decision in game.item_order:
				if game.item_order.index(decision) < len(drops):

					if drops[game.item_order.index(decision)] in pickups:
						# Legal item drop
						pickups.remove(drops[game.item_order.index(decision)])
					else:
						# Legal item pickup
						pickups.add(drops[game.item_order.index(decision)])

			elif decision == '\n':
				for item in pickups:
					self.player.pick_up(item)
				leave = True




	def check_passives(self, unit, purge=False):

		# Manage Plaguebringer
		if unit.equipped_armor.base_string == 'Plaguebringer' and not purge and d(100) >= 50:
			spaces, affected = [], []
			for x in range(-2,3):
				for y in range(-2,3):
					if x != 0 or y != 0: spaces.append((max(0, unit.loc[0] + x), max(0, unit.loc[1] + y)))

			# Find units affected
			for other_unit in game.units:
				if other_unit.loc in spaces and other_unit != unit and other_unit.calc_resistances()[2] < 1: affected.append(other_unit)

			if len(affected) != 0:
				game.game_log.append(unit.equipped_armor.name + ' blasts a burst of green filth from its vents.')

				for affected_unit in affected: apply(affected_unit, 'poisoned', 1, stacking=True)


		if not purge:
			# Reduce Cooldowns for player
			# ------------------
			if type(unit) == Player:
				# Reduce
				for cooldown_tuple in unit.cooldowns:
					cooldown_tuple[1] -= 1

					# Add back
					if cooldown_tuple[1] == 0:
						unit.abilities.append(cooldown_tuple[0])
						self.game_log.append("You can use " + str(cooldown_tuple[0]) + " again!")
						unit.cooldowns.remove(cooldown_tuple)

			# Regen Health
			if unit.hp < unit.maxhp:

				# Increment Counter
				unit.hregen += 1

				# Regen one health
				if unit.hregen >= (unit.reg - 1/4 * unit.con):

					unit.hp += 1
					unit.hregen = 0

			# Regen Mana
			if unit.mana < unit.maxmana:

				# Increment Counter
				if 'mana flow' in unit.traits: unit.mregen += 2
				else: unit.mregen += 1

				# Regen one health
				if unit.mregen >= (14 - unit.int):

					unit.mana += 1
					unit.mregen = 0

		for passive in unit.passives:

			name = passive[0]
			count = passive[1]


			# Decrement Count
			passive[1] -= 1
			if passive[1] <= 0 or purge:

				# Remove Dhampir passive
				if name == "bloodlust":
					unit.dex -= 4
					unit.str -= 2
					game.game_log.append("You regain control of your bloodlust.")
					for weapon in unit.wielding:
						if weapon.base_string == "thirstfangs":
							unit.wielding.remove(weapon)
							break

				# Manage drained
				if name == "drained": unit.dex += Brands.dict["drained"]["dex_loss"]

				# Manage hastened
				elif name == "hastened":
					if unit.name == 'you': game.game_log.append("You feel yourself slowing down.")
					else: game.game_log.append(unit.info[3] + " seems to have slowed down.")
					unit.mspeed *= 4

				# Manage Indominable
				elif name == "indominable":
					game.game_log.append(unit.info[3] + " can now enter Valhalla in peace.")

				# Manage Indominable
				elif name == "repair matrix":
					if unit.name == 'you': game.game_log.append("You reroute power back to your offensive systems.")
					else: game.game_log.append(unit.info[3] + " reroutes power back to its offensive systems.")
					unit.str += unit.strength_loss
					unit.innate_ac -= unit.acgain
					unit.reg = unit.prereg
					unit.mspeed -= unit.msgain

				# Manage Iron Blessing
				elif name == "blessed iron":
					game.game_log.append(unit.info[4] + " iron blessing fades.")

				# Manage Resistant
				elif name == "resistant":
					unit.frostr, unit.firer, unit.poisonr, unit.acidr, unit.shockr, unit.expr = unit.frostr-3, unit.firer-3, unit.poisonr-3, unit.acidr-3, unit.shockr-3, unit.expr-3
					game.game_log.append(unit.info[4] + " bonus resistances fade.")

				# Manage Spectral Weapons
				elif name[:8] == "spectral":

					if name[9:18] == "godhammer": name = name[20:]
					removed = False

					for item in game.items:
						if item.base_string == name:
							game.items.remove(item)
							color_tone = item.color
							removed = True
							break
					if not removed:
						for item in unit.inventory:
							if type(item) == Weapon:
								if item.base_string == name:
									unit.inventory.remove(item)
									color_tone = item.color
									removed = True
									break
					if not removed:
						for weapon in unit.wielding:
							if weapon.base_string == name:
								unit.wielding.remove(weapon)
								color_tone = weapon.color
								if unit.name == 'you': unit.hands += weapon.hands
								break

					game.game_log.append(unit.info[4] + " " + Colors.color(name, color_tone) + " dissolves into the air.")

				# Manage Unbreakable
				elif name == 'unbreakable':
					unit.innate_ac -= unit.unbreakableac
					game.game_log.append(unit.info[3] + " no longer can feel no pain.")

				# Manage grotesque
				elif name == "grotesque":
					unit.hp -= Brands.dict['grotesque']['bonushp']
					unit.maxhp -= Brands.dict['grotesque']['bonushp']
					unit.str -= Brands.dict['grotesque']['bonusstr']
					game.game_log.append(unit.info[4] + " body returns to its normal shape.")

				# Manage Disemboweled
				elif name == "disemboweled":
					unit.str += Brands.dict['disemboweled']['strred']

				# Manage Immobile
				elif name == "immobile":
					game.game_log.append(unit.info[0] + " can move again.")

				unit.passives.remove([passive[0], passive[1]])

			if not purge:

				# Manage Disemboweled
				if name == "disemboweled":

					damage = max(int(unit.hp * 0.1), 1)
					unit.hp -= damage

					game.game_log.append(unit.info[4] + " wound " + Colors.color("bleeds","red") + " for " + str(damage) + " damage!")

				# Manage poisoned
				elif name == "poisoned":

					damage = count
					unit.hp -= damage

					game.game_log.append(Colors.color("Venom","green") + " stings " + unit.info[0] + " for " + str(damage) + " damage!")

				# Manage aflame
				elif name == "aflame":

					damage = max(1, int(unit.con*1.2))
					unit.hp -= damage

					game.game_log.append(Colors.color("Fire","fire") + " burns " + unit.info[0] + " for " + str(damage) + " damage!")

				# Manage Frozen
				elif name == "frozen":
					unit.time += unit.mspeed
					if type(unit) == Player: game.game_log.append("You are " + Colors.color("frozen","cyan") + "!")
					else: game.game_log.append(unit.info[3]+ " is " + Colors.color("frozen","cyan") + " and cannot move!")


				# Stunned
				elif name == "stunned":
					unit.time += unit.mspeed
					if type(unit) == Player: game.game_log.append("You are " + Colors.color("stunned","magenta") + "!")
					else: game.game_log.append(unit.info[3] + " is " + Colors.color("stunned","magenta") + "!")

		# Dhampir Passive
		if type(unit) == Player and unit.race == "Dhampir":

			# Apply effect
			if "bloodlust" not in unit.currentPassives() and 0 < unit.hp <= unit.maxhp / 3:
				unit.passives.append( ["bloodlust",30])
				unit.dex += 4
				unit.str += 2
				unit.wielding.append(Weapon(self, "thirstfangs",'','red','fangs',0, 0, 0, 0, 0.3, None,"vampiric"))
				unit.wielding[-1].damage = min(14, unit.str)
				game.game_log.append("You become enraged with " + Colors.color("bloodlust","red") + "!")




		# Check if unit is still alive
		if unit.hp <= 0 and type(unit) != Player:
			game.game_log.append(unit.info[3] + " dies from its wounds!")
			game.units.remove(unit)
			if unit in game.allies: game.allies.remove(unit)

			# Ooze Passive
			if 'split' in unit.spells: Spells.spells["split"][0]("split", unit, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler)
			elif 'filth explosion' in unit.spells: Spells.spells["filth explosion"][0]("filth explosion", unit, unit, game, Maps.rooms[game.map.map][0], game.map.room_filler)


			# Mounts
			if unit.rider is not None:
				unit.rider.mount = None
			elif unit.mount is not None:
				unit.mount.unit.rider = None

			# Drop Loot
			unit.drop_booty(game)

			# XP Gain
			game.player.xp += unit.xp + int(d(game.player.cha) / 2)











# GLOBAL FUNCTIONS




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





game = Game()
if game.character_select() is not False: game.run()








