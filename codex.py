from random import randint
from bestiary import Monsters
import ai

def d(range):
	return randint(1,range)


class Weapons():
	# self,  name, rep, wclass hands,  enchantment, damage, to_hit, speed,   brand(optional), (percent to swing) 

	array = {

		# Innate Weapons
		"fist" : 	   ['','fist',0, 0, 1, 9, 0.7, None, 100],
		"horns" :  	   ['','horns',0, 0, 6, 0, 0.7, None, 50],
		"headbutt" :   ['','head',0, 0, 8, -1, 1.0, None, 10],
		"tail smash" : ['','tail',0, 0, 6, 2, 0.8, None, 25],
		"shield hit" : ['','shield',0, 0, 5, 5, 1.0, None, 15],
		"fist smash" : ['','fists',0, 0, 17, -2, 1.6, None, 100],



	# Basic Weapons

		# Blunt
		"hammer" :       ['%','hammer',1, 0, 10, 0, 1.2],
		"warhammer" :    ['%','hammer',2, 0, 15, -4, 1.4],
		"club" : 	     ['%','club',1, 0, 9, -1, 1.1],
		"mace" : 		 ['%','mace',1, 0, 9, 0, 1.0],
		"spiked mace" :  ['%','mace',1, 0, 10, -1, 1.15],

		# Polearms
		"spear" :        ['/','spear',1, 0, 9, 1, 1],
		"sun spear" :    ['/','spear',1, 0, 9, 0, 0.9, "flaming"],
		"halberd" :      ['/','polearm',2, 0, 11, 0, 1.15],

		# Blades
		"iron dagger" :        ['!','dagger',1, 0, 6, 4, 0.75],
		"steel dagger" : 	   ['!','dagger',1, 0, 7, 5, 0.8],
		"iron longsword" :     ['!','sword',1, 0, 7, 1, 0.9],
		"steel longsword" :    ['!','sword',1, 0, 9, 1, 1.0],
		"steel bastard sword" :['!','bastard sword',2, 0, 12, -1, 1.2],
		"claymore" :     	   ['!','greatsword',2, 0, 14, -3, 1.4],

		# Axes
		"iron axe" : 	    ['&','axe',1, 0, 9, -1, 1.1],
		"iron battleaxe" :  ['&','axe',2, 0, 12, -2, 1.1],
		"steel axe" : 	    ['&','axe',1, 0, 11, -1, 1.1],
		"steel battleaxe" : ['&','axe',2, 0, 14, -2, 1.1],



		# Orcish Weapons
		"goblin spear": ['/','spear',1, 0, 7, 3, 1],
		"smasha": 		['%','hammer',1, 0, 10, -2, 1.2],
		"skull smasha": ['%','hammer',2, 0, 16, -5, 1.5],
		"stabba" :      ['!','dagger',1, 0, 7, 2, 0.85],
		"slica" :       ['!','sword',1, 0, 8, 0, 1],
		"big slica" :   ['!','greatsword',2, 0, 11, -1, 1.2],
		"choppa" :      ['&','axe',1, 0, 9, -1, 1.1],
		"big choppa" :  ['&','axe',2, 0, 13, -3, 1.2],
		"boss choppa" : ['&','axe',2, 0, 16, -4, 1.4],

		"toxic slica":  ['!','sword',1, 0, 9, 0, 1, "envenomed"],
		"ice choppa":   ['&','axe',2, 0, 13, -2, 1.5, "frozen"],


		# Uruk Weapons
		"hooked longsword" :     ['!','sword',1, 0, 9, 2, 1.1],
		"hooked greatsword" :    ['!','greatsword',2, 0, 15, -3, 1.25],
		"uruk-hai pike" :    	 ['/','pike', 2, 0, 11, -1, 1.2],

		# Elvish Weapons
		"elvish leafblade" :  ['!','sword', 2, 0, 12, 0, 1.0],
		"elvish broadspear" : ['/','spear', 2, 0, 12, 0, 1.0],

		# Bone Weapons
		"bone cleaver" :   ['!','sword',1, 0, 9, 2, 1.2],
		"sawtooth blade" : ['!','sword',1, 0, 11, -1, 1.2],


		# Ranged Weapons
		"goblin bow" :        [')','bow',2, 0, 5, -4, 0.9],
		"crude shortbow" :    [')','bow',2, 0, 6, -4, 0.95],
		"blackwood longbow" : [')','bow',2, 0, 8, -1, 1.0],
		"ranger longbow" :    [')','bow',2, 0, 8, 0, 1.3],
		"uruk crossbow" :     ['(','crossbow',2, 0, 9, 0, 2],


		# Legendary Weapons
		"The Glaive of Gore" :    ['/','polearm',     1, 3, 14, 0, 1.2],
		"Singing Spear of Dorn" : ['/','god spear',   1, d(7), 12, 3, 0.7, 'flaming'],
		"Black Axe of Borke" :    ['&','god axe',     2, -10, 30, -5, 1.6, 'vampiric'],
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

	def dark_transformation(attacker, enemy, game, map, roomfiller):
		
		if attacker.hp > attacker.maxhp / 3:
			return False


		if attacker.name != 'you':
			game.units.remove(attacker)

			data = Monsters.array["Abomination"]
			roomfiller.spawn("Abomination",attacker.loc)

			game.game_log.append("The " + attacker.name + " mutters a chant, he twists into a grotesque shape!")
			attacker.time += 2
			return True

	def poison_breath(attacker, enemy, game, map, roomfiller):

		# Traits
		status = 'poisoned'
		count = 3
		manacost = 3


		# See if in range
		los = ai.los(attacker.loc, enemy.loc, map, game)

		if los is None or attacker.mana < manacost:
			return False
		if len(los) - 2  >  3:
			return False

		if attacker.name == 'you':
			game.game_log.append("You bellow a cloud of poison gas at the " + enemy.name + ", poisoning it!")
		else:
			game.game_log.append("The " + attacker.name + " bellows a cloud of poison gas, poisoning you!")

		# Manage time and mana
		attacker.time += 1.1
		attacker.mana -= manacost


		for passive in enemy.passives:

			if passive[0] == status:
				passive[1] += count
				return True

		enemy.passives.append([status, count])
		return True










	# List Spells
	spells = {

		# Orc Spells
		"poison breath" :  poison_breath,

		# Black Eye Spells
		"dark transformation" : dark_transformation,
		}








class Armors():
	# self, name, rep,  armor_rating, encumberance, enchantment,  brand(optional)

	array = {

		# Garments and Robes
		"tattered garments" : ['[',0,0, 0],
		"tainted robe" : 	  ['[',7,0, -d(4)],

		# Skins and Hides
		"animal skin" : 	['[',0,0, 0],
		"bear hide" :   	['[',1,0, 0],
		"troll hide" :  	['[',3,1, 0],

		# Hide and Scale Armors
		"iron scale mail" :    ['[',2,0, d(2)],
		"drake scale armor" :  ['[',0,0, d(3)],
		"wyvern scale mail" :  ['[',2,0, d(4)],
		"blackscale" : 		   ['[',6,1, 0],

		# Conventional Armors
		"rotted chainmail" : [']',3,2, 0],
		"berserker mail" :   [']',5,3, 0],
		"iron chainmail" :   [']',6,5, 0],

		# Plate Armors
		"scrap plate armor" : [']',8,10, 0, 'plate'],
		"blackiron plate" :   [']',8,8, 0, 'plate'],
		"Orcish dreadplate" : [']',12,18, 0, 'plate'],
		"steel plate armor" : [']',10,9, 0, 'plate'],

		# Legendary Armor
		"God-Frame" :     [']',13,17, d(10), 'angelic'],
		"Kain's Pact" :   ['[',7,0, d(6), 'demonic'],
		}

class Shields():

	array = {
		# self,rep    name, armor_rating, encumberance, enchantment

		"buckler shield" : 	  ['}',3,1,0],
		"iron fang shield" :  ['}',6,3,0],
		"bronze aegis" :      ['}',5,1,0],
		"steel kite shield" : ['}',8,5,0],
		"tower shield" :  	  ['}',12,6,0],
		}


class CharacterRaces():
	# 		(17)    con, st, dex, inte, cha, mspeed, reg    innate weapons

	races = {
		"Cytherean" :  [[2,2,4,5,3,1.0, 12], []],
		"Gnome" :      [[2,3,5,4,3,0.8, 11], []],
		"Hobbit" :     [[2,3,4,3,5,0.9, 11], []],
		"Elf" : 	   [[3,3,4,4,3,0.9, 13], []],
		"Terran" :     [[4,3,3,3,4,1.0, 15], []],
		"Ghoul" :      [[4,4,4,2,1,1.1, 8], []],
		"Dragonborn" : [[4,5,2,3,1,1.2, 13], ["tail smash"]],
		"Black Orc" :  [[5,4,2,2,1,1.3, 15], ["headbutt"]],
		"Dwarf" : 	   [[6,3,2,3,2,1.3, 10], []],
		"Troll" :	   [[6,5,1,1,1,1.4, 16], []],
	}


class Brands():
	dict = {
		"frozen": {"count": 3, "dex_loss": 3},
		"flaming": {"count": 2, "damage": 4},
		"envenomed": {"count": 4, "damage": 2},
	}




