from random import randint, shuffle
from bestiary import Monsters
from maps import Maps
from codex import Weapons, Armors, Tomes, Shields, Brands, Ammos
from descriptions import Descriptions, Colors
import ai

import sys, os
import termios, fcntl
import select
from sty import fg, bg, ef, rs

def d(range):
	return randint(1,range)

def md(range, number):
	sum = 0
	while number > 0:
		sum += d(range)
		number -= 1
	return sum

def color(statement, color):
	fg.color = Colors.array[color]
	return(fg.color + str(statement) + fg.rs)

def bcolor(statement, bcolor):
	bg.color = Colors.array[bcolor]
	return(bg.color + str(statement) + bg.rs)

def fullcolor(statement, fcolor, bcolor):
	fg.color, bg.color = Colors.array[fcolor], Colors.array[bcolor]
	return(fg.color + bg.color + str(statement) + rs.all)

def movement(decision, position):
	if decision == 'h': return (position[0] - 1, position[1])
	elif decision == 'j': return (position[0], position[1] + 1)
	elif decision == 'k': return (position[0], position[1] - 1)
	elif decision == 'l': return (position[0] + 1, position[1])
	elif decision == 'y': return (position[0] - 1, position[1] - 1)
	elif decision == 'u': return (position[0] + 1, position[1] - 1)
	elif decision == 'b': return (position[0] - 1, position[1] + 1)
	elif decision == 'n': return (position[0] + 1, position[1] + 1)
	else: return None

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
	try: decision = sys.stdin.read()
	except: print("Python interpreter could not keep up. Tell the idiot developer to fix his game.")

	# Reset the terminal:
	termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	return decision

def apply(unit, passive, count, stacking = False):

	for present_passive in unit.passives:

		if present_passive[0] == passive:
			if stacking: present_passive[1] += count
			else: present_passive[1] = count
			return

	unit.passives.append([passive, count])

class Spells():


# DEFINE spells

	def leap(name, attacker, enemy, game, map, roomfiller, ability = False):

		if attacker.name == 'you':

			orig_position = attacker.loc[:]
			valid = False

			spaces = [i for i in range((len(Maps.rooms[game.map.map][0]) + 10))]

			while not valid:

				print("=======================================================================================")

				game.map.display(game)
				mloc = attacker.loc

				# Choose Direction
				if orig_position != attacker.loc: length = len(ai.los(attacker.loc, orig_position, map, game, False)) - 1
				else: length = 0

				print("Distance:", str(length) + '/' + str(Spells.spells['leap'][5]))
				decision = rinput("Leap where?")

				for i in range(len(spaces)): print(" ")

				prev_position = attacker.loc

				# Choose Direction
				if movement(decision, attacker.loc) is not None: mloc = movement(decision, attacker.loc)

				# NOTE: FIX ONCE HAVE INFO FOR ENTER BUTTON
				# --------------------------------------------------------------------------

				elif decision in [char for char in "abcdefghiklmnopqrstuvwxyz1234567890"]:
					game.temp_log.append("That is not a valid option.")
					return False

				los = ai.los(mloc, orig_position, map, game, False)

				if game.map.square_identity(mloc) in ['|','#','-'] or los is None:
					print(los)
					if attacker.name == 'you': print("You cannot go there.")
				elif len(los) - 1 > Spells.spells['leap'][5]:
					length = len(los) - 1
					print("That space is out of range.")
				else:
					attacker.loc = mloc
					if los is not None: print(los)
					else: print("ELSE")

				if decision == '\n':
					# Check Space
					if not game.map.can_move(mloc, True) or game.map.square_identity(mloc) == '+':
						attacker.loc = orig_position
						game.temp_log.append("You can't land there.")
						return False
					valid = True
					game.game_log.append("You leap and land again on the ground!")
					return True

				# --------------------------------------------------------------------------


		# TO IMPLEMENT: Not Player

		# else:
		# 	print("IM TRYING")
		# 	spaces = []
		# 	for x in range(-1,2):
		# 		for y in range(-1,2):
		# 			if attacker.loc[0] + x >= 0 and attacker.loc[1] + y >= 0 and (x != 0 or y != 0): spaces.append((attacker.loc[0] + x, attacker.loc[1] + y))
		# 	shuffle(spaces)

		# 	for space in spaces:
		# 		if game.map.can_move(space) and game.map.square_identity != '+':
		# 			# Place Trap
		# 			roomfiller.place_trap(damage,'mine',space)
		# 			game.game_log.append("The " + attacker.name + " throws down an explosive mine!")
		# 			return True
		# 	return False

	def combat_roll(name, attacker, enemy, game, map, roomfiller, ability = False):

		if attacker.name == 'you':

			orig_position = attacker.loc[:]
			valid = False

			spaces = [i for i in range((len(Maps.rooms[game.map.map][0]) + 10))]

			while not valid:

				print("=======================================================================================")

				game.map.display(game)
				mloc = attacker.loc

				# Choose Direction
				if orig_position != attacker.loc: length = len(ai.shortest_path(attacker.loc, orig_position, map, game, False)) - 1
				else: length = 0

				print("Distance:", str(length) + '/' + str(Spells.spells['combat roll'][5]))
				decision = rinput("Roll where?")

				for i in range(len(spaces)): print(" ")

				prev_position = attacker.loc

				# Choose Direction
				if movement(decision, attacker.loc) is not None: mloc = movement(decision, attacker.loc)

				# NOTE: FIX ONCE HAVE INFO FOR ENTER BUTTON
				# --------------------------------------------------------------------------

				elif decision in [char for char in "abcdefghiklmnopqrstuvwxyz1234567890"]:
					game.temp_log.append("That is not a valid option.")
					return False

				if game.map.square_identity(mloc) in ['|','#','-']:
					if attacker.name == 'you': print("You cannot go there.")
				elif len(ai.shortest_path(mloc, orig_position, map, game, False)) - 1 > Spells.spells['combat roll'][5]:
					length = len(ai.shortest_path(attacker.loc, orig_position, map, game, False)) - 1
					print("That space is out of range.")
				else:
					attacker.loc = mloc

				if decision == '\n':
					# Check Space
					if not game.map.can_move(mloc, True) or game.map.square_identity(mloc) == '+':
						attacker.loc = orig_position
						game.temp_log.append("You can't land there.")
						return False
					valid = True
					game.game_log.append("You swiftly roll across the floor!")

					if attacker.quivered is not None:
						if attacker.quivered.wclass in Ammos.thrown_amclasses: attacker.fire()

					return True

				# --------------------------------------------------------------------------


		# TO IMPLEMENT: Not Player

		# else:
		# 	print("IM TRYING")
		# 	spaces = []
		# 	for x in range(-1,2):
		# 		for y in range(-1,2):
		# 			if attacker.loc[0] + x >= 0 and attacker.loc[1] + y >= 0 and (x != 0 or y != 0): spaces.append((attacker.loc[0] + x, attacker.loc[1] + y))
		# 	shuffle(spaces)

		# 	for space in spaces:
		# 		if game.map.can_move(space) and game.map.square_identity != '+':
		# 			# Place Trap
		# 			roomfiller.place_trap(damage,'mine',space)
		# 			game.game_log.append("The " + attacker.name + " throws down an explosive mine!")
		# 			return True
		# 	return False


	def tripmine(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(3, 1 + 1/2 * attacker.dex))

		if attacker.name == 'you':
			# Choose Direction
			decision = rinput("Place the mine in which direction?")

			if decision not in ['h','j','k','l','u','y','b','n']:
				game.temp_log.append("That is not a valid direction.")
				return False
			# Choose Direction
			if movement(decision, attacker.loc) is not None: mloc = movement(decision, attacker.loc)

			# Check Space
			if not game.map.can_move(mloc) or game.map.square_identity(mloc) == '+':
				if attacker.name == 'you': game.temp_log.append("You cannot place a mine there.")
				return False

			roomfiller.place_trap(damage,'mine',mloc)
			game.game_log.append("You throw an explosive mine on the dungeon floor!")
			return True

		# Not Player
		else:
			spaces = []
			for x in range(-1,2):
				for y in range(-1,2):
					if attacker.loc[0] + x >= 0 and attacker.loc[1] + y >= 0 and (x != 0 or y != 0): spaces.append((attacker.loc[0] + x, attacker.loc[1] + y))
			shuffle(spaces)

			for space in spaces:
				if game.map.can_move(space) and game.map.square_identity != '+':
					# Place Trap
					roomfiller.place_trap(damage,'mine',space)
					game.game_log.append(attacker.info[3] + " throws down an explosive mine!")
					return True
			return False


	def green_blood(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Check Condition
		if len(attacker.passives) == 0:
			if attacker.name == 'you': game.temp_log.append("You have nothing your blood needs to purge.")
			return False

		# Heal for each
		heal = int(attacker.maxhp / 5 * len(attacker.passives))
		attacker.hp = min(attacker.maxhp, attacker.hp + heal)

		# Apply Affect + flavor text
		if attacker.name != 'you': game.game_log.append(attacker.info[4] + " blood purges it of all its stasuses and heals for " + str(heal) + " health!")
		else: game.game_log.append("Your blood purges you of all your statuses and heals you for " + str(heal) + " health!")

		# Purge passives
		game.check_passives(attacker,True)
		return True


	def dark_transformation(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'grotesque', 20

		# Check Condition
		if attacker.hp * 2.5 > attacker.maxhp:
			if attacker.name == 'you': game.temp_log.append("You haven't given enough blood.")
			return False


		# Apply Affect + flavor text
		if attacker.name != 'you':
			game.units.remove(attacker)

			roomfiller.spawn("Abomination",attacker.loc)

			game.game_log.append(attacker.info[3] + " mutters a chant, it twists into a grotesque shape!")
		else:
			apply(attacker, status, count)
			attacker.hp += Brands.dict[status]['bonushp']
			attacker.maxhp += Brands.dict[status]['bonushp']
			attacker.str += Brands.dict[status]['bonusstr']
			game.game_log.append("Your body twists into a huge, grotesque abomination!")
		return True

	def split(name, attacker, enemy, game, map, roomfiller, ability = False):

		if attacker.hp > 0: return False

		spaces = []
		for x in range(-1,2):
			for y in range(-1,2):
				if attacker.loc[0] + x >= 0 and attacker.loc[1] + y >= 0 and (x != 0 or y != 0): spaces.append((attacker.loc[0] + x, attacker.loc[1] + y))
		shuffle(spaces)


		# Apply Affect + flavor text
		if attacker.tier <= 4: ooze = "Lesser Ooze"
		else: ooze = "Clear Ooze"
		roomfiller.spawn(ooze,attacker.loc)

		# Change Color
		newooze = game.units[-1]
		newooze.color = attacker.color
		newooze.name = color(newooze.namestring, newooze.color)
		newooze.info = ('the ' + newooze.name, 'the ' + newooze.name + "'s", 'its', 'The ' + newooze.name, 'The ' + newooze.name + "'s")

		for space in spaces:
			if game.map.can_move(space) and game.map.square_identity != '+':

				if attacker in game.allies: roomfiller.spawn(ooze,space, True)
				else: roomfiller.spawn(ooze,space)

				# Change Color
				newooze = game.units[-1]
				newooze.color = attacker.color
				newooze.name = color(newooze.namestring, newooze.color)
				newooze.info = ('the ' + newooze.name, 'the ' + newooze.name + "'s", 'its', 'The ' + newooze.name, 'The ' + newooze.name + "'s")

				# Flavor Text
				game.game_log.append(attacker.info[3] + " splits into two smaller jellies!")	
				return True

		game.game_log.append(attacker.info[3] + " splits into a smaller jelly!")
		return True

	def filth_explosion(name, attacker, enemy, game, map, roomfiller, ability = False):

		if attacker.hp > 0: return False

		spaces, affected = [], []
		for x in range(-1,2):
			for y in range(-1,2):
				if attacker.loc[0] + x >= 0 and attacker.loc[1] + y >= 0 and (x != 0 or y != 0): spaces.append((attacker.loc[0] + x, attacker.loc[1] + y))
		shuffle(spaces)

		for unit in game.units:
			if unit.loc in spaces: affected.append(unit)

		if len(affected) == 0: return False

		damage = int(attacker.maxhp / 5)

		# Hit string
		hit, healed = "",""
		for unit in affected:
			heal = False
			# See if hurt or heal
			if unit.name == 'you':
				if unit.race in ['Ghoul']: heal = True
			else:
				if unit.etype in ['undead']: heal = True

			if not heal:
				if len(hit) == 0: hit += unit.info[0]
				else: hit +=  ", " + unit.info[0]
				unit.hp -= damage
			else:
				if len(healed) == 0: healed += unit.info[0]
				else: healed +=  ", " + unit.info[0]
				unit.hp = min(unit.maxhp, unit.hp + damage)
		if len(hit) == 0 and len(healed) == 0: game.game_log.append(attacker.info[3] + " explodes into a cloud of filth and decay!")
		elif len(hit) != 0 and len(healed) == 0: game.game_log.append(attacker.info[3] + " explodes into a cloud of filth and decay, dealing " + str(damage) + " damage to " + hit +'!')
		elif len(hit) == 0 and len(healed) != 0: game.game_log.append(attacker.info[3] + " explodes into a cloud of filth and decay, healing " + str(damage) + " to " + healed +'!')
		else: game.game_log.append(attacker.info[3] + " explodes into a cloud of filth and decay, dealing " + str(damage) + " damage to " + hit + ' and healing ' + str(damage) + ' to ' + healed +'!')

		return True

	def raise_skeleton(name, attacker, enemy, game, map, roomfiller, ability = False):

		spaces = []
		for x in range(-3,4):
			for y in range(-3,4):
				if attacker.loc[0] + x >= 0 and attacker.loc[1] + y >= 0 and (x != 0 or y != 0): spaces.append((attacker.loc[0] + x, attacker.loc[1] + y))
		shuffle(spaces)

		for space in spaces:
			if game.map.can_move(space) and game.map.square_identity != '+':
				# Spawn Skeleton
				if d(attacker.int) <= 3: Skeleton = "Skeleton"
				else: Skeleton = "Skeleton Warrior"

				if attacker in game.allies: roomfiller.spawn(Skeleton,space, True)
				else: roomfiller.spawn(Skeleton,space)
				# Flavor Text
				if attacker.name != 'you':
					game.game_log.append(attacker.info[3] + " calls a " + Skeleton + " to rise from its grave!")
				else:
					game.game_log.append("You call upon a " + Skeleton + " to rise up from the ground!")
				return True

		# No free spaces
		if attacker.name == 'you': game.temp_log.append("There are no places to raise a skeleton!")
		return False

	def wraithwalk(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = "wraithform", 5

		# Check Condition
		for passive in attacker.passives:
			if passive[0] == "wraithform":
				if attacker.name == 'you': game.temp_log.append("You are already in wraithform.")
				return False

		# Apply Affect + flavor text
		attacker.passives.append([status, 2 * count])
		passives = [passive[0] for passive in attacker.passives]
		print(passives)

		if attacker.name != 'you':
			game.game_log.append(attacker.info[3] + " " + color("flickers","cyan") + " from the material plane and reappears!")
			while "wraithform" in passives:
				if attacker.mana < attacker.maxmana: attacker.mana += 1
				if attacker.hp < attacker.maxhp and d(10) > 7: attacker.hp  += 1
				attacker.time = 0
				attacker.turn()
				passives = [passive[0] for passive in attacker.passives]
				count -= 1

				if count == 0:
					break
		else:
			game.game_log.append("You " + color("flicker","cyan") + " from the material plane")
			while "wraithform" in passives:
				if attacker.mana < attacker.maxmana: attacker.mana += 1
				if attacker.hp < attacker.maxhp and d(10) > 7: attacker.hp += 1
				attacker.time = 0
				game.player_turn(game.map)
				passives = [passive[0] for passive in attacker.passives]
				count -= 1

				if count == 0:
					break

		return True

	def blink(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Check Condition
		if attacker.name != 'you':
			if len(ai.los(attacker.loc, enemy.loc, Maps.rooms[game.map.map][0], game )) - 1 > 3: return False

		spaces = []
		for x in range(-3,4):
			for y in range(-3,4):
				if (x != 0 or y != 0): spaces.append((max(0,attacker.loc[0] + x), max(0,attacker.loc[1] + y)))
		shuffle(spaces)

		for space in spaces:
			if game.map.can_move(space):
				if game.map.square_identity != '+':
					# Move
					attacker.loc = space
					# Flavor Text
					if attacker.name != 'you':
						game.game_log.append(attacker.info[3] + " " + color("blinks","lightblue") + " and reappears!")
					else:
						game.game_log.append("You " + color("blink","lightblue") + " and reappear!")
					return True

		# No free spaces
		if attacker.name == 'you': game.temp_log.append("There are no places to blink to!")
		return False


	def poison_breath(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'poisoned', 2

		# Poison Resist
		resist = enemy.calc_resistances()[2]
		if d(4) <= resist:
			if enemy.name == 'you': game.game_log.append("You shrug off the cloud of " + color("poison gas","green") + " bellowed by " + attacker.info[0] + "!")
			else: game.game_log.append(enemy.info[3] + " shrugs off " + attacker.info[1] + " cloud of " + color("poison gas","green") + "!")
			return True

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You bellow a cloud of " + color("poison gas","green") + " at " + enemy.info[0] + ", poisoning it!")
		else: game.game_log.append(attacker.info[3] + " bellows a cloud of " + color("poison gas","green") + ", poisoning " + enemy.info[0] + "!")

		# Apply Effect
		apply(enemy, status, count, stacking = True)
		return True

	def ignite_venom(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Condition
		poisoned = False
		for passive in enemy.passives:
			if passive[0] == 'poisoned':
				poisoned = True
				ct = passive[1]
				enemy.passives.remove(passive)
				break
		if not poisoned:
			if attacker.name == 'you': game.game_log.append("There is no venom for you to ignite.")
			return False

		# Damage
		damage = ct * 4

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You turn the " + color("venom","green") + " in " + enemy.info[0] + " to explosive fire, dealing " + str(damage) + " damage!")
		else: game.game_log.append(attacker.info[3] + " turns the " + color("venom","green") + " in " + enemy.info[0] + " to explosive fire, dealing " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)

		return True

	def spectral_sword(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Condition
		if attacker.hands < 1:
			if attacker.name == 'you': game.temp_log.append('You do not have a free hand to use.')
			return False

		attacker.give_weapon("spectral sword")
		attacker.wielding[-1].damage = max(min(attacker.int + attacker.calc_mdamage(), 15), 7)

		apply(attacker,'spectral sword',30)

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You conjure a " + color("spectral sword","springgreen") + " in your free hand!")
		else: game.game_log.append(attacker.info[3] + " conjures a " + color("spectral sword","springgreen") + " in its free hand!")

		return True

	def envenom(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		passive, brand, hits, coated, bonus = 'envenomed', 'envenomed', 3, False, False

		# Weapons
		for item in attacker.wielding:
			if item.wclass in Weapons.weapon_classes and item.hands > 0:
				try:
					if item.wclass not in Weapons.ranged_wclasses and item.brand != brand and not item.legendary:

						for passive in attacker.passives:
							if passive[0] == 'envenomed':
								passive[1] = hits
								bonus = True
						if not bonus: item.passives.append([passive, hits])
						item.brand = brand
						coated = True
				except: pass

		# Ammo
		if attacker.quivered is not None:
			if attacker.quivered.brand != brand:
				# Envenom quiver
				attacker.quivered.brand = brand
				coated = True
				# Check other ammo
				for thing in attacker.inventory:
					if thing.name in Ammos.array and thing != attacker.quivered:
						if thing.name == attacker.quivered.name and thing.brand == attacker.quivered.brand:
							attacker.quivered.number += thing.number
							attacker.inventory.remove(thing)
							break

		if not coated:
			if attacker.name == 'you': game.temp_log.append("There is nothing for you to envenom right now.")
			return False

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You coat your weapons in your " + color("deadly poison","green") + "!")
		else: game.game_log.append(attacker.info[3] + " coats its weapons in a " + color("deadly poison","green") + "!")

		return True

	def bless_weapon(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		passive, brand, hits, coated, bonus = 'holy', 'holy', 3, False, False

		# Weapons
		for item in attacker.wielding:
			if item.wclass in Weapons.weapon_classes and item.hands > 0:
				try:
					if item.wclass not in Weapons.ranged_wclasses and item.brand != brand and not item.legendary:

						for passive in attacker.passives:
							if passive[0] == 'holy':
								passive[1] = hits
								bonus = True
						if not bonus:
							item.passives.append([passive, hits])
						item.brand = brand
						coated = True
				except: pass

		# Ammo
		if attacker.quivered is not None:
			if attacker.quivered.brand != brand:
				# Envenom quiver
				attacker.quivered.brand = brand
				coated = True
				# Check other ammo
				for thing in attacker.inventory:
					if thing.name in Ammos.array and thing != attacker.quivered:
						if thing.name == attacker.quivered.name and thing.brand == attacker.quivered.brand:
							attacker.quivered.number += thing.number
							attacker.inventory.remove(thing)
							break

		if not coated:
			if attacker.name == 'you': game.temp_log.append("There is no weapon for you to bless right now.")
			return False

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You invoke to deity to " + color("bless","bone") + " your weapon, giving it divine power!")
		else: game.game_log.append(attacker.info[3] + " invokes its deity to " + color("bless","bone") + " its weapon with divine power!")

		return True

	def flame_tongue(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'aflame', d(2)
		if ability: damage = int(md(2, 1 + 1/2 * attacker.str))
		else: damage = max(0, int(md(2, 1/2 + 1/2 * attacker.int) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense) )

		# Fire Resist
		resist = enemy.calc_resistances()[1]
		if d(4) <= resist:
			if enemy.name == 'you': game.game_log.append("You shrug off a tongue of " + color("flame","fire") + " breathed by " + attacker.info[0] + "!")
			else: game.game_log.append(enemy.info[3] + " shrugs off " + attacker.info[1] + " burst of " + color("flame","fire") + "!")
			return True

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You breathe a burst of " + color("flame","fire") + " at " + enemy.info[0] + ", dealing " + str(damage) + " damage and setting it " + color("aflame","fire") + "!")
		else: game.game_log.append(attacker.info[3] + " breathes a burst of " + color("flame","fire") + ", dealing " + enemy.info[0] + " " + str(damage) + " damage and setting " + enemy.info[0] + " " + color("aflame","fire") + "!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)

		# Apply Effect
		apply(enemy, status, count)
		return True

	def pounce(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Condition
		los = ai.los(attacker.loc, enemy.loc, Maps.rooms[game.map.map][0], game )
		if len(los) <= 2:
			if attacker.name == 'you': game.temp_log.append("You're too close to do that!")
			return False

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You pounce onto " + enemy.info[0] + "!")
		else: game.game_log.append(attacker.info[3] + " pounces on " + enemy.info[0] + "!")


		attacker.loc = los[-2]

		# Strike
		for weapon in attacker.wielding:
			if weapon.wclass in Weapons.weapon_classes and weapon.hands == 0:
				weapon.strike(attacker, enemy)
		return True

	def battlecry(name, attacker, enemy, game, map, roomfiller, ability = False):

		tempac = 0

		# Check Condition
		for unit in game.units:
			if unit == attacker: continue
			distance = ai.shortest_path(attacker.loc, unit.loc, Maps.rooms[game.map.map][0], game, blockers = False)
			if len(distance) - 1 <= Spells.spells['battlecry'][5]: tempac += 1

		if tempac == 0:
			if attacker.name == 'you': game.temp_log.append("There are no enemies in range, it would have no effect!")
			return False

		# Apply Effect
		attacker.unbreakableac = tempac
		attacker.innate_ac += tempac
		apply(attacker, 'unbreakable', 10)
		if attacker.name == 'you': game.game_log.append('You roar out a ' + color('battlecry','darkred') + ' that emboldens you, granting you ' + str(tempac) + ' armor.')
		return True

	def double_shot(name, attacker, enemy, game, map, roomfiller, ability = False):

		# NOTE: only for player

		# Condition
		if attacker.quivered.number < 2: 
			if attacker.name == 'you': game.game_log.append("You do not have enough ammo quivered.")
			return False

		return attacker.fire(mod = 'double shot')

	def web_shot(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		if attacker.name == 'you': status, count = 'immobile', d(max(1, attacker.int - d(enemy.cha)))
		else: status, count = 'immobile', d(max(1, attacker.tier * 2 - d(enemy.cha)))
		if ability: damage = int(md(1, 1/2 + 1/2 * attacker.dex))
		else: damage = max(0, int(md(1, 1/2 + 1/2 * attacker.int) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense) )

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You shoot a net of " + color("webs","bone") + " at " + enemy.info[0] + ", dealing " + str(damage) + " damage and rendering it immobile!")
		else: game.game_log.append(attacker.info[3] + " shoots a net of " + color("webs","bone") + " at " + enemy.info[0] + ", dealing " + str(damage) + " and rendering " + enemy.info[0] + " immobile!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)

		# Apply Effect
		apply(enemy, status, count)
		return True


	def iron_grit(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'indominable', 9

		# Check condition
		if attacker.name != 'you':
			for name, count in attacker.passives:
				if name == státus: return
			if attacker.hp > attacker.maxhp / 3: return False

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You ready yourself to enter Valhalla!")
		else: game.game_log.append(attacker.info[3] + " readies itself to enter Valhalla!")

		# Apply Effect
		apply(attacker, status, count)
		return True

	def repair_matrix(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status = 'repair matrix'
		count = min(30, 10 + attacker.level) if attacker.name == 'you' else min(30, 10 + attacker.tier)

		# Check condition
		if attacker.name != 'you':
			for name, count in attacker.passives:
				if name == status: return
			if attacker.hp > attacker.maxhp / 3: return False

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You reroute power from your offensive processes to your repair systems!")
		else: game.game_log.append(attacker.info[3] + " reroutes power from your offensive processes to its repair systems!")


		# Apply Effect
		attacker.strloss = int(2 * attacker.str / 3)
		attacker.acgain = int(attacker.con / 2)
		attacker.prereg = attacker.reg
		attacker.msgain = attacker.mspeed
		
		attacker.str -= attacker.strloss
		attacker.innate_ac += attacker.acgain
		attacker.reg = 2
		attacker.mspeed += attacker.msgain
		apply(attacker, status, count)
		return True

	def iron_blessing(name, attacker, enemy, game, map, roomfiller, ability = False):

		# TODO: ATTEMPT TO MAKE UNIVERSAL BUFF TEMPLATE LIKE I DID FOR SPELLS

		# Traits
		status, count = 'blessed iron', 8

		if attacker.name == 'you':
			if len(game.allies) == 1: target = attacker
			else:

				print("                                                                     ")
				print("---------------------------------------------------------------------------------------")
				print(status)
				print("                                                                     ")
				print("=======================================================================================")
				print("                                                                     ")
				for i in range(len(game.allies)):

					unit = game.allies[i]

					print(str(game.item_order[i]) + " - " + unit.name)
				print("                                                                     ")
				print("=======================================================================================")


				decision = rinput("Bestow " + spell_name + " on which target?")


				if decision in game.item_order and game.item_order.index(decision) < len(game.allies):

					# Choose Legal Enemy
					target = game.allies[game.item_order.index(decision)]
				else:
					game.temp_log-append('That is not a valid unit.')
					return False

				# Heal machine case
				if target.etype == 'machine':
					if target.hp != target.maxhp:
						heal = min(target.maxhp - target.hp, int(md(3, 1 + attacker.cha)))
						target.hp += heal
						game.game_log.append("You " + color("bless","steel") + " the machine spirit of " + target.info[0]  + ", healing it!")
						return True


			# Heal self if Felltron
			if target == attacker:

				if attacker.name == 'you':
					if attacker.race in ['Felltron']:

						if attacker.hp != attacker.maxhp:
							heal = min(attacker.maxhp - attacker.hp, int(md(3, 1 + attacker.cha)))
							attacker.hp += heal
							game.game_log.append("You " + color("bless","steel") + " your machine spirit, healing yourself!")

							return True

				game.game_log.append("You " + color("bless","steel") + " your weapons and armor, they feel lighter!")
			else: game.game_log.append("You " + color("bless","steel") + " " + target.info[1] + " weapons and armor, they seem lighter!")

			# Apply Effect
			apply(target, status, count)
			return True

		# Non-player case
		# TODO: Range of ability
		# TODO: Dont cast multiple times on same target
		else:
			targets = game.allies + [game.player] if attacker in game.allies else game.units
			closest, range = attacker, attacker.range_from_player
			if range is None: range = 100
			for unit in targets:
				if unit in game.allies + [game.player] and attacker not in game.allies + [game.player]: continue
				if attacker != unit and unit.etype == 'machine' and unit.hp != unit.maxhp:
					heal = min(unit.maxhp - unit.hp, int(md(3, 1 + attacker.cha)))
					unit.hp += heal
					game.game_log.append(attacker.info[3] + " " + color("blesses","steel") + " the machine spirit of " + unit.info[0]  + ", healing it!")
					return True
				elif attacker != unit:
					if unit.range_from_player <= range: closest, range = unit, unit.range_from_player


			if range > 6: return False

			# Flavor Text
			if attacker == closest: game.game_log.append(attacker.info[3] + " " + color("blesses","steel") + " its weapons and armor, they seem lighter!")
			elif closest.name == 'you': game.game_log.append(attacker.info[3] + " " + color("blesses","steel") + " your weapons and armor, they feel lighter!")
			else: game.game_log.append(attacker.info[3] + " " + color("blesses","steel") + " " + closest.info[1] + " weapons and armor, they seem lighter!")

			# Apply Effect
			apply(closest, status, count)
			return True

	def frost_breath(name, attacker, enemy, game, map, roomfiller,  ability = False):

		# Traits
		status, count = "frozen", 3
		if ability: damage = int(md(2, 1/2 + 1/2 * attacker.str))
		else: damage = max(0, int(md(2, 1/2 + 1/2 * attacker.int))  + attacker.calc_mdamage() - enemy.equipped_armor.mdefense)

		def freeze(attacker, enemy):

			# Frost Resist
			resist = enemy.calc_resistances()[0]
			if d(4) <= resist:
				if enemy.name == 'you': game.game_log.append("You shrug off the wave of " + color("frost","cyan") + " breathed by " + attacker.info[0] + "!")
				else: game.game_log.append(enemy.info[3] + " shrugs off " + attacker.info[1] + " wave of " + color("frost","cyan") + "!")
				return True

			# Flavor Text
			if attacker.name == 'you' and enemy.name != 'you': game.game_log.append("You breathe a wave of " + color("frost","cyan") + " that hits " + enemy.info[0] + ", dealing " + str(damage) + " damage and " + color("freezing","cyan") + " it!")
			else: game.game_log.append(attacker.info[3] + " breathes a wave of " + color("frost","cyan") + " that " + color("freezes","cyan") + " " + enemy.info[0] + " and deals " + str(damage) + " damage!")

			# Manage damage
			enemy.hp -= damage
			if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)

			# Apply effect
			apply(enemy, status, count, stacking = True)


		# Check Condition
		tar = False
		for unit in game.units:
			if unit == attacker: continue
			los = ai.los(attacker.loc, unit.loc, Maps.rooms[game.map.map][0], game)
			if los is not None:
				if len(los) - 1 <= Spells.spells['frost breath'][5]:
					freeze(attacker, unit)
					tar = True
		if not tar:
			game.temp_log.append("There are no targets in range")
			return False

		return True

	def tremor_strike(name, attacker, enemy, game, map, roomfiller,  ability = False):

		# Traits
		status, count = "stunned", 2
		if ability: damage = max( 0, int(md(3, 1/2 + 1/2 * attacker.str)  ) )
		else: damage = int(md(3, 1/2 + 1/2 * attacker.int) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense)

		if attacker.name == 'you': game.game_log.append("You slam the ground, causing a huge " + color("shockwave","tan") + " of force to barrel outwards.")
		else: game.game_log.append(attacker.info[3] + " slams the ground, causing a huge " + color("shockwave","tan") + " of force to barrel outwards.")

		def slam(attacker, enemy):

			# Apply effect
			extra = ''
			if d(100) >= 50:
				apply(enemy, status, count, stacking = True)
				extra = ' and ' + color("stunning","magenta") + ' you' if enemy.name == 'you' else ' and ' + color("stunning","magenta") + ' it'

			# Flavor Text
			game.game_log.append("The " + color("shockwave","tan") + " slams into " + enemy.info[0] + ", dealing " + str(damage) + " damage" + extra + "!")

			# Manage damage
			enemy.hp -= damage
			if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)


		# Check Condition
		tar = False
		for unit in game.units:
			if unit == attacker: continue
			distance = ai.shortest_path(attacker.loc, unit.loc, Maps.rooms[game.map.map][0], game, blockers = False)
			if len(distance) - 1 <= Spells.spells['tremor strike'][5]:
				slam(attacker, unit)
				tar = True
		if not tar:
			game.temp_log.append("There are no targets in range")
			return False

		return True

	def magic_missile(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = max(0, int(md(2, 3/2 + 1/2 * attacker.int) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense))

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You conjure a speeding " + color("phantom arrow","magenta") + ", dealing " + str(damage) + " damage to " + enemy.info[0] + "!")
		else: game.game_log.append(attacker.info[3] + " conjures a speeding " + color("phantom arrow","magenta") + ", dealing " + enemy.info[0] + " " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)
		return True

	def flash_heal(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		heal = min(attacker.maxhp - attacker.hp, int(md(2, 1 + attacker.cha)))

		# Check Condition
		if attacker.hp == attacker.maxhp:
			if attacker.name == 'you': game.temp_log.append("You are already at full health.")
			return False

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You are bathed in the light of your god, you are " + color("healed","bone") + " for " + str(heal) + " health!")
		else: game.game_log.append(attacker.info[3] + " is bathed in the light of its god, " + color("healing","bone") + " for " + str(heal) + " health!")

		# Manage damage
		attacker.hp += heal
		return True

	def wild_equilibrium(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Check Condition
		if attacker.hp == attacker.mana:
			if attacker.name == 'you': game.temp_log.append("Your " + color("spirit","springgreen") + " is already balanced.")
			return False

		# Traits
		type = None
		if attacker.hp > attacker.mana:
			attacker.mana = min(attacker.hp, attacker.maxmana)
			type = 'mana'

		else:
			attacker.hp = min(attacker.mana, attacker.maxhp)
			type = 'health'

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("Your " + color("spirit","springgreen") + " balances itself, restoring " + type + "!")
		else: game.game_log.append(attacker.info[3] + " balances its " + color("spirit","springgreen") + ", restoring "  + type + "!")

		return True

	def bloodreave(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = max(0, int(md(4, max(2, 3/2 + 1/2 * attacker.int) + attacker.calc_mdamage()  - enemy.equipped_armor.mdefense)))
		self_dam = d(max(1, int(damage / 3)))

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You vomit a stream of " + color("boiling blood","darkred") + ", dealing " + str(damage) + " damage to " + enemy.info[0] + " and " + str(self_dam) + " damage to yourself!")
		else: game.game_log.append(attacker.info[3] + " vomits a stream of " + color("boiling blood","darkred") + ", dealing " + enemy.info[0] + " " + str(damage) + " damage and some to itself!")

		# Manage damage
		enemy.hp -= damage
		attacker.hp -= self_dam
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)
		return True


	def dark_bolt(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = max(0, int(md(2, 2 + 1/2 * attacker.int) + attacker.calc_mdamage()  - enemy.equipped_armor.mdefense))

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You blast "  + enemy.info[0] + " with a " + color("dark bolt","purple") + ", dealing it " + str(damage) + " damage!")
		else: game.game_log.append(attacker.info[3] + " blasts " + enemy.info[0] + " with a " + color("dark bolt","purple") + ", dealing " + enemy.info[0] + " " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)
		return True

	def deaths_hand(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You unleash a huge " + color("shadow hand","purple") + " that grabs "  + enemy.info[0] + "!")
		else: game.game_log.append(attacker.info[3] + " unleashes a huge " + color("shadow hand","purple") + " that grabs " + enemy.info[0] + "!")

		# Apply Effects
		count = int(attacker.int / 2)
		apply(enemy, 'immobile', count)
		apply(enemy, 'aflame', count)
		apply(enemy, 'poisoned', count)
		return True

	def feral_bite(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(3, attacker.str))

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You " + color("bite","red") + " your teeth into "  + enemy.info[0] + ", dealing it " + str(damage) + " damage!")
		else: game.game_log.append(attacker.info[3] + " " + color("bite","red") + " its teeth into " + attacker.info[0] + " for " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)
		return True

	def deathmark(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'marked', 10

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You mutter an ancient curse, a " + color("black mark","darkred") + " appears on " + enemy.info[0] + "!")
		else: game.game_log.append(attacker.info[3] + " mutters an ancient curse, a " + color("black mark","darkred") + " appears on " + enemy.info[0] + "!")

		# Apply Effect
		apply(enemy, status, count)
		return True

	def thunderbolt(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count, extra = 'stunned', 2, ''
		damage = max(0, int(md(2, 1/2 + attacker.int) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense) )

		# Fire Resist
		resist = enemy.calc_resistances()[4]
		if d(5) <= resist:
			if enemy.name == 'you': game.game_log.append("You shrug off a " + color("thunderbolt","yellow") + " sent by " + attacker.info[0] + "!")
			else: game.game_log.append(enemy.info[3] + " shrugs off " + attacker.info[1] + " " + color("thunderbolt","yellow") + "!")
			return True

		# Apply Effect
		if d(100) >= 50:
			apply(enemy, status, count)
			extra = ' and ' + color("stunning","magenta") + ' you' if enemy.name == 'you' else ' and ' + color("stunning","magenta") + ' it'

		# Flavor Text
		if attacker.name == 'you': game.game_log.append("You call a bolt of crackling " + color("lightning","yellow") + " onto " + enemy.info[0] + ", dealing " + str(damage) + " damage" + extra + "!")
		else: game.game_log.append(attacker.info[3] + " calls a bolt of crackling " + color("lightning","yellow") + " onto " + enemy.info[0] + ", dealing " + str(damage) + " damage" + extra + "!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)

		return True

	def chain_lightning(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = max(0, int(md(2, 1 + 1/3 * attacker.int) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense))
		bounce_chance = 80

		def chain(attacker, enemy, zapped = set()):

			# Base case:
			if enemy in zapped: return

			# Shock Resist
			resist = enemy.calc_resistances()[4]
			if d(4) <= resist:
				if enemy.name == 'you': game.game_log.append("You shrug off the conjured " + color("wild lightning","yellow") + "!")
				else: game.game_log.append(enemy.info[3]+ " shrugs off " + attacker.info[1] + " " + color("wild lightning","yellow") + "!")
				return True

			# Flavor Text
			if attacker.name == 'you' and enemy.name != 'you':
				game.game_log.append("You blast "  + enemy.info[0] + " with " + color("wild lightning","yellow") + ", dealing it " + str(damage) + " damage!")
			elif attacker.name == 'you' and enemy.name == 'you':
				game.game_log.append("You zap yourself with " + color("wild lightning","yellow") + ", you take " + str(damage) + " damage!")
			elif attacker == enemy:
				game.game_log.append(attacker.info[3] + " zaps itself with " + color("wild lightning","yellow") + ", taking " + str(damage) + " damage!")
			else:
				game.game_log.append(attacker.info[3] + " blasts " + enemy.info[0] + " with " + color("wild lightning","yellow") + ", dealing " + str(damage) + " damage!")

			# Manage damage
			enemy.hp -= damage
			if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)
			zapped.add(enemy)

			# Chain Effect
			for unit in game.units:
				los = ai.los(enemy.loc, unit.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:
					if unit not in zapped and len(los) - 1 <= 2 and d(100) >= 100 - bounce_chance: chain(attacker, unit, zapped)

			return True

		return chain(attacker, enemy)





	# List spell schools
	spell_schools = {
		# Spells
		"fire" : 			["flame tongue"],
		"frost" : 			["frost breath"],
		"electricity" : 	["chain lightning", "thunderbolt"],
		"poison" : 			["envenom","poison breath","ignite venom"],
		"necromancy" : 		["dark bolt","raise skeleton","bloodreave","dark transformation","deathmark","death's hand","life leech"],
		"holy" : 			["flash heal","bless weapon","evening rites"],
		"wind" : 			[],
		"earth" : 			["tremor strike"],
		"conjuration" : 	["magic missile","spectral sword"],
		"translocation" : 	["blink","wraithwalk"],
		"transmutation" : 	[],
		"iron" : 			["iron blessing"],

		# Abilities
		"acrobatics" : ["leap","combat roll","martial draw","deadly precision","double shot"],
		"ferocity" :   ["feral bite","pounce","web shot","furious charge","battlecry"],
		"wild" :       ["wild equilibrium","green blood","split","filth explosion"],
		"tech" :       ["repair matrix","tripmine","iron grit"],
		"mystical" :   ["mana flow"],
	} 

	school_info = {
		# Spells
		"fire" : 			["fire","flaming"],
		"frost" : 			["cyan","frozen"],
		"electricity" : 	["yellow","electrified"],
		"poison" : 			["green","envenomed"],
		"necromancy" : 		["purple","vampiric"],
		"holy" : 			["bone","holy"],
		"wind" : 			["lightblue","hellfire"],
		"earth" : 			["tan","flaming"],
		"conjuration" : 	["magenta","runic"],
		"translocation" : 	["blue","antimagic"],
		"transmutation" : 	["springgreen","vorpal"],
		"iron" : 			["steel","silvered"],

		# Ability Categories
		"acrobatics" : ["salmon",None],
		"ferocity" :   ["darkred",None],
		"wild" :       ["springgreen",None],
		"tech" :       ["steel",None],
		"mystical" :   ["blue",None],

	} 





	# List Spells
	spells = {

		# ORG						Name, mana, time, target?, maxrange?, range (optional)

		# Basic Spells

		# Mage Skills
		"magic missile" :  		(magic_missile,   		3, 1.15, True, False),
		"blink" : 				(blink, 				4, 1.0,  False, False),
		"chain lightning" : 	(chain_lightning, 		8, 1.4,  True, True,  6),
		"spectral sword" : 		(spectral_sword, 		6, 1.0,  False, False),
		# Warlock Skills
		"dark bolt" :  			(dark_bolt, 			3, 1.2,  True, True,  7),
		"death's hand" :  		(deaths_hand, 			7, 1.5,  True, True,  5),  
		"raise skeleton" : 		(raise_skeleton,   		6, 2.5,  False, False), 
		# Paladin Skills
		"flash heal":			(flash_heal, 			10, 1.3,  False, False), 
		"bless weapon" : 		(bless_weapon,      	10, 1.2,  False, False),
		# Warrior Skills
		"battlecry" : 			(battlecry,      	    10, 1.0,  False, False, 2),
		# Ranger Skills
		"double shot" : 		(double_shot,      	    7, 0,    False, False),
		# Rogue Skills
		"combat roll" : 		(combat_roll,      	    6, 1.0,  False, False, 2),



		# Black Orc
		"green blood" : 		(green_blood,   		10, 0.5,  False, False),
		# Cytherean
		"wraithwalk" : 			(wraithwalk,   			9, 0,  False, False),
		# Dragonborn
		"flame tongue" :  		(flame_tongue,      	5, 1.2,  True, True,  4),
		# Dwarf
		"iron grit" :  			(iron_grit,      		15, 0.6,  False, False),
		# Elf
		"wild equilibrium" : 	(wild_equilibrium, 		20, 1.5,  False, False), 
		# Felltron
		"repair matrix" : 		(repair_matrix, 		25, 1.0,  False, False), 
		# Ghoul
		"feral bite" : 			(feral_bite,      		7, 0.9,  True, True,  1),
		# Gnome
		"tripmine" : 			(tripmine,      		10,1.0,  False, False),
		# Hobbit
		"leap" : 				(leap,      			6,1.0,  False, False, 4),
		# Naga
		"envenom" : 			(envenom,      			10,2.0,  False, False),

		# Ooze
		"split" : 				(split,      			0,1.5,  False, False),

		# Spider
		"pounce" : 				(pounce,      			7,1.2,  True, True, 4),
		"web shot" :  			(web_shot,      		6, 1.2,  True, True,  8),

		# Undead
		"filth explosion" : 	(filth_explosion,      	0,1.5,  False, False),

		# Fire
		# Frost
		"frost breath" :  		(frost_breath,      	9, 1.3,  False, False, 3),
		# Necromancy
		"dark transformation" : (dark_transformation,   0, 3.0,  False, False),
		"deathmark" :  			(deathmark, 			10, 1.4,  True, False),
		"bloodreave" :  		(bloodreave, 			6, 1.2,  True, True,  6), 
		# Electricity
		"thunderbolt" : 		(thunderbolt, 			7, 1.6,  True, True,  6),
		# Earth
		"tremor strike" : 		(tremor_strike, 		10, 1.5,  False, True,  6),
		# Poison
		"poison breath" :  		(poison_breath,   		4, 1.2,  True, True,  4), 
		"ignite venom" :  		(ignite_venom,   		6, 1,  True, True,  7),
		# Iron
		"iron blessing" :  		(iron_blessing,      	10, 1.5,  False, False),
		}