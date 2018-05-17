from random import randint
from bestiary import Monsters
from maps import Maps
import ai

def d(range):
	return randint(1,range)

def md(range, number):
	sum = 0
	while number > 0:
		sum += d(range)
		number -= 1
	return sum



class Armors():
	# self, name, rep,  armor_rating, encumberance, enchantment,  brand(optional)

	array = {

		# Garments and Robes
		"tattered garments" : ['[',1,0, 0],
		"tainted robe" : 	  ['[',6,0, -d(4)],

		# Skins and Hides
		"animal skin" : 	['[',1,0, 0],
		"bear hide" :   	['[',2,0, 0],
		"troll hide" :  	['[',4,1, 0],

		# Hide and Scale Armors
		"iron scale mail" :    ['[',2,1, d(3)],
		"drake scale armor" :  ['[',0,2, d(4)],
		"wyvern scale mail" :  ['[',2,2, d(5)],
		"blackscale" : 		   ['[',6,1, 0],

		# Conventional Armors
		"rotted chainmail" : [']',4,2, 0],
		"berserker mail" :   [']',5,3, 0],
		"iron chainmail" :   [']',6,5, 0],

		# Plate Armors
		"scrap plate armor" : [']',8,10, 0, 'plate'],
		"blackiron plate" :   [']',8,8, 0, 'plate'],
		"Orcish dreadplate" : [']',12,18, 0, 'plate'],
		"steel plate armor" : [']',10,9, 0, 'plate'],

		# Legendary Armor
		"God-Frame" :     [']',13,13, 0, 'angelic'],
		"Kain's Pact" :   ['[',6,0, d(3), 'demonic'],
		"Bloodshell" : 	  ['[',9,4, 0, 'barbed'],
		}

class Shields():

	array = {
		# self,rep    name, armor_rating, encumberance, enchantment

		"buckler shield" : 	  ['}',3,1,0],
		"blackiron shield" :  ['}',6,3,0],
		"bronze aegis" :      ['}',5,1,1],
		"steel kite shield" : ['}',8,5,0],
		"tower shield" :  	  ['}',12,6,0],
		"gauntlet shield" :   ['}',4,0,0],
		}


class CharacterRaces():
	# 		(17)    con, st, dex, inte, cha, mspeed, reg    innate weapons (power, ability)

	races = {
		"Cytherean" :  [[2,2,4,5,3,1.0, 12], [("wraithwalk", True)]],
		"Gnome" :      [[2,3,5,4,3,0.8, 11], []],
		"Hobbit" :     [[2,3,4,3,5,0.9, 11], []],
		"Elf" : 	   [[3,3,4,4,3,0.9, 13], []],
		"Terran" :     [[4,3,3,3,4,1.0, 15], []],
		"Ghoul" :      [[4,4,4,2,1,1.1,  8], []],
		"Dragonborn" : [[4,5,2,3,1,1.2, 13], ["tail smash"]],
		"Black Orc" :  [[5,4,2,2,1,1.3, 15], ["headbutt"]],
		"Dwarf" : 	   [[6,3,2,3,2,1.3, 10], []],
		"Troll" :	   [[6,5,1,1,1,1.4, 16], []],
	}


class Brands():
	dict = {
		"drained": {"count": 3, "dex_loss": 3},
		"flaming": {"count": 2, "damage": 4},
		"envenomed": {"count": 4, "damage": 2},
		"grotesque": {"bonushp": 20, "bonusstr": 4},
		"frozen": {"count": 2},
	}


class Weapons():
	# self,  name, rep, wclass hands,  enchantment, damage, to_hit, speed,   brand(optional), (percent to swing) 

	array = {

		# Innate Weapons
		"fists" : 	   ['','fist',0, 0, 3, 9, 0.7, None, 100],
		"horns" :  	   ['','horns',0, 0, 6, 0, 0.7, None, 50],
		"headbutt" :   ['','head',0, 0, 8, -1, 0.9, None, 15],
		"tail smash" : ['','tail',0, 0, 6, 2, 0.8, None, 25],
		"shield hit" : ['','shield',0, 0, 5, 5, 1.0, None, 15],
		"fist smash" : ['','fists',0, 0, 17, -2, 1.6, None, 100],



	# Basic Weapons

		# Blunt
		"hammer" :       ['%','hammer',1, 0, 10, 0, 1.2],
		"warhammer" :    ['%','hammer',2, 0, 15, -4, 1.4],
		"club" : 	     ['%','club',1, 0, 9, -1, 1.3],
		"mace" : 		 ['%','mace',1, 0, 9, 0, 1.2],
		"spiked mace" :  ['%','mace',1, 0, 10, -1, 1.25],

		# Polearms
		"spear" :        ['/','spear',1, 0, 9, -1, 1],
		"sun spear" :    ['/','spear',1, 0, 9, 0, 1.1, "flaming"],
		"halberd" :      ['/','polearm',2, 0, 11, -2, 1.15],

		# Blades
		"iron dagger" :        ['!','dagger',1, 0, 6, 4, 0.75],
		"steel dagger" : 	   ['!','dagger',1, 0, 7, 5, 0.8],
		"iron longsword" :     ['!','sword',1, 0, 7, 1, 0.9],
		"steel longsword" :    ['!','sword',1, 0, 9, 1, 1.0],
		"steel bastard sword" :['!','bastard sword',2, 0, 12, -1, 1.2],
		"claymore" :     	   ['!','greatsword',2, 0, 14, -3, 1.4],

		# Axes
		"iron axe" : 	    ['&','axe',1, 0, 8, -1, 1.1],
		"iron battleaxe" :  ['&','axe',2, 0, 11, -2, 1.1],
		"steel axe" : 	    ['&','axe',1, 0, 10, -1, 1.1],
		"steel battleaxe" : ['&','axe',2, 0, 13, -2, 1.1],



		# Orcish Weapons
		"goblin spear": ['/','spear',1, 0, 7, 3, 1],
		"bone club" :   ['%','club',1, 0, 9, -2, 1.1],
		"smasha": 		['%','hammer',1, 0, 10, -2, 1.2],
		"skull smasha": ['%','hammer',2, 0, 16, -5, 1.5],
		"stabba" :      ['!','dagger',1, 0, 7, 2, 0.85],
		"slica" :       ['!','sword',1, 0, 8, 0, 1],
		"big slica" :   ['!','greatsword',2, 0, 11, -1, 1.2],
		"choppa" :      ['&','axe',1, 0, 8, -1, 1.1],
		"big choppa" :  ['&','axe',2, 0, 12, -3, 1.2],
		"boss choppa" : ['&','axe',2, 0, 15, -4, 1.4],

		"toxic slica":  ['!','sword',1, 0, 9, 0, 1, "envenomed"],
		"ice choppa":   ['&','axe',2, 0, 12, -2, 1.5, "frozen"],


		# Uruk Weapons
		"hooked longsword" :     ['!','sword',1, 0, 9, 2, 1.1],
		"hooked greatsword" :    ['!','greatsword',2, 0, 15, -3, 1.25],
		"uruk-hai pike" :    	 ['/','pike', 2, 0, 10, -1, 1.2],

		# Elvish Weapons
		"elvish leafblade" :  ['!','sword', 2, 0, 12, 0, 1.0],
		"elvish broadspear" : ['/','spear', 2, 0, 10, 2, 1.0],

		# Bone Weapons
		"bone cleaver" :   ['!','sword',1, 0, 9, 2, 1.2],
		"sawtooth blade" : ['!','sword',1, 0, 11, -1, 1.2],


		# Ranged Weapons
		"goblin bow" :        [')','bow',2, 0, 5, -4, 1.2],
		"crude shortbow" :    [')','bow',2, 0, 6, -4, 1.25],
		"blackwood longbow" : [')','bow',2, 0, 8, -1, 1.3],
		"ranger longbow" :    [')','bow',2, 0, 8, 0, 1.6],
		"uruk crossbow" :     ['(','crossbow',2, 0, 9, 0, 2],


		# Legendary Weapons
		"The Glaive of Gore" :    ['/','polearm',     1, 3, 14, 0, 1.2],
		"Singing Spear of Dorn" : ['/','god spear',   1, d(7), 12, 3, 0.7, 'flaming'],
		"Black Axe of Borke" :    ['&','god axe',     2, -10, 28, -5, 1.6, 'vampiric'],
		"Bloodreaver" :           ['!','demon sword', 1, -6, 24, 6, 1, 'vampiric'],
		"Longclaw" :              ['!','greatsword',  2, d(10), 18, 5, 1.1],
		"God-Cleaver" : 		  ['!','god sword',   2, d(5), 22, -10, 1.4, 'hellfire'],
		"Worldshaper" :     	  ['%','god hammer',  2, d(10), 25, -15, 1.6, 'frozen']
		}


	weapon_classes = { 
		# "You VERB your WCLASS PREPOSITION the ENEMY for __ damage!"
		# Class of weapon : verb, preposition

		# Innate Weapons
		"fist" : ['punch', 'into'],
		"fists" : ['slam', 'onto'],
		"horns" : ["stab", "into"],
		"head" : ["smash", "onto"],
		"tail" : ["smash", "into"],

		# Basic Weapons
		"shield" : ["smash", "into"],
		"hammer" : ["crash", "on"],
		"spear" : ["thrust","into"],
		"pike" : ["thurst", "into"],
		"dagger" : ["stab", "into"],
		"axe" : ["hack", "into"],
		"greataxe" : ["carve", "into"],
		"club" : ["smash", "onto"],
		"mace" : ["smash", "onto"],
		"sword" : ["slice", "into"],
		"demon sword" : ["carve", "inside"],
		"greatsword" : ["cleave", "into"],
		"bastard sword" : ["slash", "into"],
		"polearm" : ["slice", "into"],

		# Ranged Weapons
		"bow" : ["loose", "into"],
		"crossbow" : ["fire", "into"],

		# God weapons
		"god spear" : ["plunge", "deep into"],
		"god sword" : ["carve", "deep into"],
		"god axe" :   ["chop","through"],
		"god hammer" :["smash","on"],
		}



	ranged_wclasses = set(["bow", "crossbow"])







	# DEFINE spells

	def dark_transformation(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status = 'grotesque'
		count = 20

		# Check Condition
		if attacker.hp * 3 > attacker.maxhp:
			if attacker.name == 'you':
				game.temp_log.append("You haven't given enough blood.")
			return False


		# Apply Affect + flavor text
		if attacker.name != 'you':
			game.units.remove(attacker)

			data = Monsters.array["Abomination"]
			roomfiller.spawn("Abomination",attacker.loc)

			game.game_log.append("The " + attacker.name + " mutters a chant, he twists into a grotesque shape!")
			attacker.time += time
		else:
			attacker.passives.append([status, count])
			attacker.hp += Brands.dict[status]['bonushp']
			attacker.maxhp += Brands.dict[status]['bonushp']
			attacker.str += Brands.dict[status]['bonusstr']
			game.game_log.append("Your body twists into a huge, grotesque abomination!")
		return True

	def wraithwalk(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		count = 5
		status = "wraithform"

		# Check Condition
		for passive in attacker.passives:
			if passive[0] == "wraithform":
				if attacker.name == 'you': game.temp_log.append("You have wraithwalked too recently.")
				return False

		# Apply Affect + flavor text
		attacker.passives.append([status, 2 * count])

		if attacker.name != 'you':
			game.game_log.append("The " + attacker.name + " flickers from the material plane and reappears!")
			while count > 0:
				if attacker.mana < attacker.maxmana: attacker.mana += 1
				attacker.time = 0
				attacker.turn()
				count -= 1
		else:
			game.game_log.append("You flicker from the material plane")
			while count > 0:
				if attacker.mana < attacker.maxmana: attacker.mana += 1
				attacker.time = 0
				game.player_turn(game.map)
				count -= 1

		return True


	def poison_breath(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status = 'poisoned'
		count = md(2,2)

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You bellow a cloud of poison gas at the " + enemy.name + ", poisoning it!")
		else:
			game.game_log.append("The " + attacker.name + " bellows a cloud of poison gas, poisoning you!")

		# Apply Effect
		for passive in enemy.passives:

			if passive[0] == status:
				passive[1] += count
				return True

		enemy.passives.append([status, count])
		return True

	def fire_breath(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status = 'aflame'
		count = d(2)
		if ability: damage = int(md(2, attacker.str))
		else: damage = int(md(2, 1/2 + 1/2 * attacker.int))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You breathe a pillar of flame at the " + enemy.name + ", dealing " + str(damage) + " damage and setting it aflame!")
		else:
			game.game_log.append("The " + attacker.name + " breathes a huge pillar of flame, dealing you " + str(damage) + " damage and setting you aflame!")

		# Manage damage
		enemy.hp -= damage
		if attacker.name != 'you': game.player.well_being_statement(enemy, game)

		# Apply Effect
		for passive in enemy.passives:

			if passive[0] == status:
				passive[1] = count
				return True

		enemy.passives.append([status, count])
		return True

	def frost_breath(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		if ability: damage = int(md(2, 1/2 + 1/2 * attacker.str))
		else: damage = int(md(2, 1/2 + 1/2 * attacker.int))

		def freeze(attacker, enemy, game, map, roomfiller, ability = False):

			# Flavor Text
			if attacker.name == 'you' and enemy.name != 'you':
				game.game_log.append("You breathe a wave of frost that hits the " + enemy.name + ", dealing " + str(damage) + " damage and freezing it!")
			else:
				game.game_log.append("The " + attacker.name + " breathes a wave of frost that hits you for " + str(damage) + " damage and freezes you!")

			# Manage damage
			enemy.hp -= damage
			if enemy.name != 'you': game.player.well_being_statement(enemy, game)
			enemy.time += 4

		# Check Condition
		tar = False
		for unit in game.units:
			los = ai.los(attacker.loc, unit.loc, Maps.rooms[game.map.map][0], game)
			if los is not None:
				if len(los) - 1 <= Weapons.spells['frost breath'][5]:
					freeze(attacker, unit, game, map, roomfiller, ability)
					tar = True
		if not tar:
			game.temp_log.append("There are no targets in range")
			return False

		return True

	def magic_missile(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(2, 1/2 + 1/2 * attacker.int))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You conjure a speeding phantom arrow, dealing " + str(damage) + " damage to the " + enemy.name + "!")
		else:
			game.game_log.append("The " + attacker.name + " conjures a speeding phantom arrow, dealing you " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if attacker.name != 'you': game.player.well_being_statement(enemy, game)
		return True

	def bloodreave(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(4, max(2, 1 + 1/2 * attacker.int)))
		self_dam = d(int(damage / 3))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You vomit a stream of boiling blood, dealing " + str(damage) + " damage to the " + enemy.name + " and " + str(self_dam) + " damage to yourself!")
		else:
			game.game_log.append("The " + attacker.name + " vomits a stream of boiling blood, dealing you " + str(damage) + " damage and " + str(self_dam)  + " to itself!")

		# Manage damage
		enemy.hp -= damage
		attacker.hp -= self_dam
		if attacker.name != 'you': game.player.well_being_statement(enemy, game)
		return True


	def dark_bolt(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(3, 1 + 1/2 * attacker.int))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You blast the "  + enemy.name + " with a dark bolt, dealing it " + str(damage) + " damage!")
		else:
			game.game_log.append("The " + attacker.name + " blasts you with a dark bolt, dealing you " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if attacker.name != 'you': game.player.well_being_statement(enemy, game)
		return True

	def chain_lightning(attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(2, 1/2 + 1/2 * attacker.int))
		bounce_chance = 80

		def chain(attacker, enemy, game, map, roomfiller, ability = False, zapped = set()):

			# Base case:
			if enemy in zapped: return

			# Flavor Text
			if attacker.name == 'you' and enemy.name != 'you':
				game.game_log.append("You zap the "  + enemy.name + " with wild lightning, dealing it " + str(damage) + " damage!")
			elif enemy.name == 'you':
				game.game_log.append("You zap yourself with wild lightning, dealing yourself " + str(damage) + " damage!")
			else:
				game.game_log.append("The " + attacker.name + " blasts you with wild lightning, dealing you " + str(damage) + " damage!")

			# Manage damage
			enemy.hp -= damage
			if enemy.name != 'you': game.player.well_being_statement(enemy, game)
			zapped.add(enemy)

			# Chain Effect
			for unit in game.units:
				los = ai.los(enemy.loc, unit.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:
					if unit not in zapped and len(los) - 1 <= 2 and d(100) >= 100 - bounce_chance: chain(attacker, unit, game, map, roomfiller, ability, zapped)

			return True

		return chain(attacker, enemy, game, map, roomfiller, ability)










	# List Spells
	spells = {

		# ORG						Name, mana, time, targetbool ?, target?, range (optional)

		# Basic Spells
		"magic missile" :  		(magic_missile,   		3, 1.15, True, False),
		"chain lightning" : 	(chain_lightning, 		8, 1.4,  True, True,  6),

		# Dragonborn
		"fire breath" :  		(fire_breath,      		5, 1.2,  True, True,  4),
		"frost breath" :  		(frost_breath,      	7, 1.3,  False, False, 3),
		# Cytherean
		"wraithwalk" : 			(wraithwalk,   			0, 0,  False, False),

		# Orc Spells
		"poison breath" :  		(poison_breath,   		4, 1.2,  True, True,  3), 
		# Black Eye Spells
		"dark transformation" : (dark_transformation,   0, 3.0,  False, False),
		"dark bolt" :  			(dark_bolt, 			5, 1.6,  True, True,  5), 
		"bloodreave" :  		(bloodreave, 			5, 1.2,  True, True,  7), 
		}









