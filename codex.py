from random import randint, shuffle
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
		"tattered garments" : ['[','robes',1,0, 0],
		"tainted robe" : 	  ['[','robes',6,0, -d(4)],
		"necromancer robes" : ['[','robes',2,0, d(3), "corrupted"],

		# Skins and Hides
		"wolf pelt" : 		['[','hide',1,0, 0],
		"bear hide" :   	['[','hide',2,0, 0],
		"spider hide" :   	['[','hide',2,-1, 0],
		"dog hide" : 		['[','hide',3,1, 0],
		"ooze skin" :   	['[','hide',2,0, 0],
		"ogre hide" : 		['[','hide',3,2, 0],
		"troll hide" :  	['[','hide',4,2, 0],
		"cave troll hide" : ['[','hide',6,4, 0],
		"spider hide" : 	['[','hide',4,1, 0],
		"flayed skins" : 	['[','hide',5,1, 0],

		# Hide Armors
		"leather armor" : 	['[','hide',5,2, 0],
		"studded armor" : 	['[','hide',7,5, 0],

		# Scale Armors
		"ironscale mail" : ['[','scale',2,3, d(3)],
		"drakescale" :     ['[','scale',1,4, d(4)],
		"wyvernscale" :    ['[','scale',3,5, d(5)],
		"blackscale" : 	   ['[','scale',6,1, 0],
		# Dragonscales
		"fire dragonscales" :  ['[','fire scale',8,5, d(4)],
		"frost dragonscales" : ['[','frost scale',9,7, d(4)],

		# Conventional Armors
		"rotted chainmail" : [']','chainmail',4,2, 0],
		"berserker mail" :   [']','chainmail',5,3, 0],
		"iron chainmail" :   [']','chainmail',6,5, 0],

		# Plate Armors
		"scrap plate armor" : [']','plate',8,10, 0],
		"blackiron plate" :   [']','plate',8,8, 0],
		"Orcish dreadplate" : [']','plate',12,18, 0],
		"steel plate armor" : [']','plate',10,9, 0],

		# Legendary Armor
		"God-Frame" :     [']','plate',13,13, d(3), 'angelic'],
		"Kain's Pact" :   ['[','robes',6,0, d(6), 'demonic'],
		"Bloodshell" : 	  ['[','plate',9,4, d(6), 'barbed'],
		}

class Shields():

	array = {
		# self,rep    name, hands, armor_rating, encumberance, enchantment

		"buckler shield" : 	  ['}',1,3,1,0],
		"wooden broadshield" :['}',1,5,3,0],
		"trollhide shield" :  ['}',1,4,1,0],
		"boneshield" :		  ['}',1,5,4,0],
		"blackiron shield" :  ['}',1,6,4,0],
		"bronze aegis" :      ['}',1,5,1,1],
		"steel kite shield" : ['}',1,8,5,0],
		"tower shield" :  	  ['}',1,12,6,0],
		"gauntlet shield" :   ['}',1,4,0,0],
		}


class CharacterRaces():
	# 		(17)    con, st, dex, inte, cha, mspeed, reg    innate weapons (power, ability)

	races = {
		"Cytherean" :  [[2,2,4,5,3,1.0, 12], [("wraithwalk", True)]],
		"Gnome" :      [[2,3,5,4,3,0.8, 11], []],
		"Hobbit" :     [[2,3,4,3,5,0.9, 11], []],
		"Elf" : 	   [[3,3,4,4,3,1.0, 13], []],
		"Terran" :     [[4,3,3,3,4,1.0, 15], []],
		"Naga" :       [[4,3,4,4,1,0.9, 20], ["tail smash"]],
		"Ghoul" :      [[4,4,4,2,1,1.1,  8], [("feral bite", True)]],
		"Dragonborn" : [[4,5,2,3,2,1.2, 13], [("flame tongue", True), "tail smash"]],
		"Black Orc" :  [[5,4,2,2,1,1.3, 15], ["headbutt"]],
		"Dwarf" : 	   [[6,3,2,3,2,1.3, 10], []],
		"Hill Troll" : [[6,5,1,1,1,1.4, 16], []],
	}


class Brands():
	dict = {
		"drained": {"count": 3, "dex_loss": 3},
		"flaming": {"count": 2},
		"envenomed": {"count": 2},
		"grotesque": {"bonushp": 20, "bonusstr": 4},
		"frozen": {"count": 2},
	}

	# Manage brands
	brands = ["flaming","frozen","silvered","envenomed","hellfire","infernal","vampiric","spectral"]


class Ammos():
	#                   rep, wclass, damage
	array = {
		# Arrows/Bolts
		"iron arrow" :     ['(', 'arrow', 1],
		"steel arrow" :    ['(', 'arrow', 2],
		"iron bolt" : 	   ['(', 'bolt', 1],
		"steel bolt" : 	   ['(', 'bolt', 2],

		# Javelins
		"iron javelin" :   ['/', 'javelin', 5],
		"barbed javelin" : ['/', 'javelin', 6],

		# Other
		"throwing axe" :   ['/', 'throwing axe', 6],
	}

	thrown_amclasses = set(["javelin","throwing axe"])

	projectile = {
		"bow" : set(["arrow"]),
		"crossbow" : set(["bolt"]),
		"ballista" : set(["bolt","arrow"]),

	}


class Weapons():
	# self,  name, rep, wclass hands,  enchantment, damage, to_hit, speed,   brand(optional), (percent to swing) 

	array = {

		# Innate Weapons
		# Hands
		"fists" : 	   	  	['','fist',0, 0, 3, 9, 0.7, None, 100],
		"fist smash" : 	  	['','fists',0, 0, 17, -2, 1.6, None, 100],
		"stone fists" : 	['%','fists',4, 0, 22, -4, 2.3, None, 100],
		"bone claws" : 	   	['','claws',0, 0, 10, 2, 0.9, None, 100],

		# Head
		"horns" :  	   	  	['','horns',0, 0, 7, 0, 0.9, None, 50],
		"headbutt" :   	  	['','head',0, 0, 8, -1, 0.9, None, 20],

		# Fangs
		"fangs" : 	      	['','fangs',0, 0, 8, 0, 0.8, None, 90],
		"blood fangs" : 	['','fangs',0, 0, 8, 0, 0.8, "vampiric", 85],
		"lich fangs" : 		['','fangs',0, 0, 10, 0, 1.2, "frozen", 85],
		"demon fangs" : 	['','fangs',0, 0, 10, 0, 0.9, "hellfire", 90],
		"dragon fangs" : 	['','fangs',0, 0, 15, 0, 1.3, None, 90],

		# Tail
		"massive stinger" : ['','stinger',0, d(3), 8, -1, 0.9, "envenomed", 40],
		"tail smash" : 	  	['','tail',0, 0, 6, 2, 0.8, None, 30],
		"dragon tail" : 	['','tail',0, 0, 8, 1, 0.8, None, 25],
		"acid slap" : 	  	['','appendage',0, d(2), 6, 1, 1.1, "envenomed", 85],
		"jelly slap" : 		['','appendage',0, d(2), 9, 1, 1.1, None, 95],
		"shield hit" : 	  	['','shield',0, 0, 5, 5, 1.0, None, 15],

		# Ranged Innate
		"vomit" :      ['','vomit',0, 0, 6, 0, 1.2, None, 40],



	# Basic Weapons

		# Blunt
		"hammer" :       ['%','hammer',1, 0, 10, 0, 1.2],
		"warhammer" :    ['%','warhammer',2, 0, 15, -4, 1.4],
		"club" : 	     ['%','club',1, 0, 9, -1, 1.3],
		"spiked club" :  ['%','club',2, 0, 16, -4, 1.7],
		"flail" : 		 ['%','flail',1, 0, 10, -2, 1.3],
		"greatflail" : 	 ['%','flail',2, 0, 17, -6, 1.5],
		"mace" : 		 ['%','mace',1, 0, 9, 0, 1.2],
		"spiked mace" :  ['%','mace',1, 0, 10, -1, 1.25],

		# Polearms
		"spear" :        ['/','spear',1, 0, 9, -1, 1],
		"pike" :      	 ['/','pike',2, 0, 10, 0, 1.2],
		"halberd" :      ['/','polearm',2, 0, 12, -2, 1.15],

		# Blades
		"iron dagger" :        ['!','dagger',1, 0, 5, 4, 0.75],
		"steel dagger" : 	   ['!','dagger',1, 0, 6, 5, 0.8],
		"iron longsword" :     ['!','sword',1, 0, 7, 1, 1.0],
		"steel longsword" :    ['!','sword',1, 0, 9, 1, 1.0],
		"iron shortsword" :    ['!','sword',1, 0, 6, 2, 0.9],
		"steel bastard sword" :['!','bastard sword',2, 0, 13, -1, 1.1],
		"iron greatsword" :    ['!','greatsword',2, 0, 11, -2, 1.2],
		"steel greatsword" :   ['!','greatsword',2, 0, 13, -2, 1.2],

		# Axes
		"hand axe" : 		['&','axe',1, 0, 7, 0, 0.8],
		"iron axe" : 	    ['&','axe',1, 0, 8, -1, 1.1],
		"iron battleaxe" :  ['&','greataxe',2, 0, 12, -3, 1.3],
		"steel axe" : 	    ['&','axe',1, 0, 10, -1, 1.1],
		"steel battleaxe" : ['&','greataxe',2, 0, 14, -3, 1.3],


		# Orcish Weapons
		"goblin spear": ['/','spear',1, 0, 7, 3, 1],
		"bone club" :   ['%','club',1, 0, 9, -2, 1.2],
		"smasha": 		['%','hammer',1, 0, 10, -2, 1.2],
		"skull smasha": ['%','warhammer',2, 0, 17, -5, 1.5],
		"stabba" :      ['!','dagger',1, 0, 6, 2, 0.85],
		"slica" :       ['!','sword',1, 0, 8, 0, 1],
		"big slica" :   ['!','greatsword',2, 0, 11, -1, 1.2],
		"choppa" :      ['&','axe',1, 0, 8, -1, 1.1],
		"big choppa" :  ['&','greataxe',2, 0, 13, -3, 1.3],
		"boss choppa" : ['&','greataxe',2, 0, 16, -4, 1.4],

		"toxic slica":  ['!','sword',1, 0, 9, 0, 1, "envenomed"],
		"ice choppa":   ['&','greataxe',2, 0, 13, -2, 1.4, "frozen"],

		# Uruk Weapons
		"hooked longsword" :     ['!','sword',1, 0, 9, 1, 1.1],
		"hooked shortsword" :    ['!','sword',1, 0, 8, 2, 1.0],
		"spiked axe"  : 		 ['&','axe',1, 0, 10, -2, 1.2],
		"hooked greatsword" :    ['!','greatsword',2, 0, 16, -3, 1.25],
		"uruk-hai pike" :    	 ['/','pike', 2, 0, 12, -1, 1.2],

		# Demon Weapons
		"bloodletter" :     ['!','demon sword',1, 0, 9, -2, 1.0],
		"skullsplitter" :   ['!','greataxe',2, 0, 16, -5, 1.5],
		"filthaxe" :   		['!','axe',1, 0, 9, -3, 1.3,"envenomed"],
		"screamflail" :   	['!','flail',1, 0, 12, -4, 1.3],

		# Dark Elf Weapons
		"thornknife" : ['!','dagger',1, 0, 6, 2, 0.7],
		"thornblade" : ['!','sword',1, 0, 8, 0, 0.9],
		"sun spear" :  ['/','spear',1, 0, 9, 0, 1.2, "flaming"],

		# Elvish Weapons
		"elven leafblade" :  ['!','sword', 2, 0, 13, 0, 0.95],
		"elven broadspear" : ['/','spear', 2, 0, 12, 2, 0.95],

		# Bone Weapons
		"bone cleaver" :   ['!','sword',1, 0, 9, 2, 1.2],
		"sawtooth blade" : ['!','sword',1, 0, 11, -1, 1.2],

		# Top-tier
		"witchhunter blade" : ['!','sword',1, 0, 10, 3, 1.0,"spectral"],
		"claymore" :     	  ['!','greatsword',2, 0, 16, -3, 1.3],
		"glaive" :      	  ['/','polearm',2, 0, 14, -2, 1.2],


		# Ranged Weapons

		# Thrown
		"iron javelin" : 	  ['/','javelin',1, 0, 3, 0, 1.2],
		"barbed javelin" : 	  ['/','javelin',1, 0, 4, -1, 1.3],
		"throwing axe" : 	  ['%','throwing axe',1, 0, 3, -1, 1.3],

		# Projectile
		"goblin bow" :        [')','bow',2, 0, 5, -4, 1.3],
		"crude shortbow" :    [')','bow',2, 0, 6, -4, 1.35],
		"blackwood longbow" : [')','bow',2, 0, 7, -1, 1.5],
		"ranger longbow" :    [')','bow',2, 0, 7, 0, 1.7],
		"elven longbow" :     [')','bow',2, 0, 7, 1, 1.5],
		"uruk crossbow" :     [')','crossbow',2, 0, 9, 0, 2],
		"black ballista" : 	  [')','bow',3, 0, 11, 0, 2.2],


		# Legendary Weapons
		"The Glaive of Gore" :    ['/','polearm',     1, 3, 14, 0, 1.2],
		"Singing Spear of Dorn" : ['/','god spear',   1, d(7), 12, 3, 0.75, 'flaming'],
		"Black Axe of Borke" :    ['&','god axe',     2, -10, 28, -5, 1.6, 'vampiric'],
		"Bloodreaver" :           ['!','demon sword', 1, -6, 24, 6, 1, 'vampiric'],
		"Nighthunter" :     	  ['%','bastard sword',  2, d(10), 16, 6, 1.2, 'silvered'],
		"Dawnbringer" :     	  ['%','sword',  	  1, d(8), 12, 2, 1.0, 'flaming'],
		"Longclaw" :              ['!','greatsword',  2, d(10), 18, 5, 1.1],
		"God-Cleaver" : 		  ['!','god sword',   2, d(5), 22, -10, 1.4, 'hellfire'],
		"Worldshaper" :     	  ['%','god hammer',  2, d(10), 25, -15, 1.6, 'frozen'],
		}


	weapon_classes = { 
		# "You VERB your WCLASS PREPOSITION the ENEMY for __ damage!"
		# Class of weapon : verb, preposition

		# Innate Weapons
		"fist" : ['punch', 'into'],
		"claws" : ['tear', 'into'],
		"fists" : ['slam', 'onto'],
		"fangs" : ['bites', 'into'],
		"stinger" : ["stab", "into"],
		"tail" : ["smash", "into"],
		"head" : ["smash", "into"],
		"tail" : ["smash", "into"],
		"appendage" : ["slap","into"],

		# Basic Weapons
		"shield" : ["smash", "into"],
		"hammer" : ["crash", "on"],
		"warhammer" : ["crash", "onto"],
		"spear" : ["thrust","into"],
		"pike" : ["thurst", "into"],
		"dagger" : ["stab", "into"],
		"axe" : ["hack", "into"],
		"greataxe" : ["carve", "into"],
		"club" : ["smash", "onto"],
		"mace" : ["smash", "onto"],
		"flail" : ["smash", "into"],
		"sword" : ["slice", "into"],
		"demon sword" : ["carve", "inside"],
		"greatsword" : ["cleave", "into"],
		"bastard sword" : ["slash", "into"],
		"polearm" : ["slice", "into"],

		# Ranged Weapons
		"arrow" : ["loose", "into"],
		"bolt" : ["fire", "into"],
		"vomit" : ["hurl", "onto"],
		"ballista" : ["launch", "into"],
		"javelin" : ["hurl", "into"],
		"throwing axe" : ["hurl", "into"],

		# God weapons
		"god spear" : ["plunge", "deep into"],
		"god sword" : ["carve", "deep into"],
		"god axe" :   ["chop","through"],
		"god hammer" :["smash","on"],
		}



	ranged_wclasses = set(["bow", "crossbow","vomit","ballista"])








	# DEFINE spells

	def dark_transformation(name, attacker, enemy, game, map, roomfiller, ability = False):

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
		else:
			attacker.passives.append([status, count])
			attacker.hp += Brands.dict[status]['bonushp']
			attacker.maxhp += Brands.dict[status]['bonushp']
			attacker.str += Brands.dict[status]['bonusstr']
			game.game_log.append("Your body twists into a huge, grotesque abomination!")
		return True

	def wraithwalk(name, attacker, enemy, game, map, roomfiller, ability = False):

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

	def blink(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Check Condition
		if attacker.name != 'you':
			if len(ai.los(attacker.loc, enemy.loc, Maps.rooms[game.map.map][0], game )) - 1 > 3: return False

		spaces = []
		for x in range(-3,4):
			for y in range(-3,4):
				if x > 0 and y > 0 and (x != 0 or y != 0): spaces.append((attacker.loc[0] + x, attacker.loc[1] + y))
		shuffle(spaces)

		for space in spaces:
			if game.map.can_move(space):
				if game.map.square_identity != '+':
					# Move
					attacker.loc = space
					# Flavor Text
					if attacker.name != 'you':
						game.game_log.append("The " + attacker.name + " blinks and reappears!")
					else:
						game.game_log.append("You blink and reappear!")
					return True

		# No free spaces
		if attacker.name == 'you': game.temp_log.append("There are no places to blink to!")
		return False


	def poison_breath(name, attacker, enemy, game, map, roomfiller, ability = False):

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

	def flame_tongue(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status = 'aflame'
		count = d(2)
		if ability: damage = int(md(2, attacker.str))
		else: damage = int(md(2, 1/2 + 1/2 * attacker.int))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You breathe a burst of flame at the " + enemy.name + ", dealing " + str(damage) + " damage and setting it aflame!")
		else:
			game.game_log.append("The " + attacker.name + " breathes a burst of flame, dealing you " + str(damage) + " damage and setting you aflame!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, name, game)

		# Apply Effect
		for passive in enemy.passives:

			if passive[0] == status:
				passive[1] = count
				return True

		enemy.passives.append([status, count])
		return True

	def frost_breath(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status = "frozen"
		count = 4
		if ability: damage = int(md(2, 1/2 + 1/2 * attacker.str))
		else: damage = int(md(2, 1/2 + 1/2 * attacker.int))

		def freeze(attacker, enemy):

			# Flavor Text
			if attacker.name == 'you' and enemy.name != 'you':
				game.game_log.append("You breathe a wave of frost that hits the " + enemy.name + ", dealing " + str(damage) + " damage and freezing it!")
			else:
				game.game_log.append("The " + attacker.name + " breathes a wave of frost that hits you for " + str(damage) + " damage and freezes you!")

			# Manage damage
			enemy.hp -= damage
			if enemy.name != 'you': game.player.well_being_statement(enemy, name, game)

			# Apply effect
			for passive in enemy.passives:

				if passive[0] == status:
					passive[1] += count
					return

			enemy.passives.append([status, count])


		# Check Condition
		tar = False
		for unit in game.units:
			los = ai.los(attacker.loc, unit.loc, Maps.rooms[game.map.map][0], game)
			if los is not None:
				if len(los) - 1 <= Weapons.spells['frost breath'][5]:
					freeze(attacker, unit)
					tar = True
		if not tar:
			game.temp_log.append("There are no targets in range")
			return False

		return True

	def magic_missile(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(2, 1/2 + 1/2 * attacker.int))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You conjure a speeding phantom arrow, dealing " + str(damage) + " damage to the " + enemy.name + "!")
		else:
			game.game_log.append("The " + attacker.name + " conjures a speeding phantom arrow, dealing you " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, name, game)
		return True

	def bloodreave(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(4, max(2, 1 + 1/2 * attacker.int)))
		self_dam = d(int(damage / 3))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You vomit a stream of boiling blood, dealing " + str(damage) + " damage to the " + enemy.name + " and " + str(self_dam) + " damage to yourself!")
		else:
			game.game_log.append("The " + attacker.name + " vomits a stream of boiling blood, dealing you " + str(damage) + " damage and some to itself!")

		# Manage damage
		enemy.hp -= damage
		attacker.hp -= self_dam
		if enemy.name != 'you': game.player.well_being_statement(enemy, name, game)
		return True


	def dark_bolt(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(3, 1 + 1/2 * attacker.int))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You blast the "  + enemy.name + " with a dark bolt, dealing it " + str(damage) + " damage!")
		else:
			game.game_log.append("The " + attacker.name + " blasts you with a dark bolt, dealing you " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, name, game)
		return True

	def feral_bite(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(3, attacker.str))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You bite your teeth into the "  + enemy.name + ", dealing it " + str(damage) + " damage!")
		else:
			game.game_log.append("The " + attacker.name + " bites its teeth into you for " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, name, game)
		return True

	def chain_lightning(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(2, 1/2 + 1/3 * attacker.int))
		bounce_chance = 80

		def chain(attacker, enemy, zapped = set()):

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
			if enemy.name != 'you': game.player.well_being_statement(enemy, name, game)
			zapped.add(enemy)

			# Chain Effect
			for unit in game.units:
				los = ai.los(enemy.loc, unit.loc, Maps.rooms[game.map.map][0], game )
				if los is not None:
					if unit not in zapped and len(los) - 1 <= 2 and d(100) >= 100 - bounce_chance: chain(attacker, unit, zapped)

			return True

		return chain(attacker, enemy)










	# List Spells
	spells = {

		# ORG						Name, mana, time, targetbool ?, target?, range (optional)

		# Basic Spells
		"magic missile" :  		(magic_missile,   		3, 1.15, True, False),
		"chain lightning" : 	(chain_lightning, 		8, 1.4,  True, True,  6),
		"blink" : 				(blink, 				4, 1.0,  False, False),

		# Ghoul
		"feral bite" : 			(feral_bite,      		6, 0.9,  True, True,  1),
		# Dragonborn
		"flame tongue" :  		(flame_tongue,      	5, 1.1,  True, True,  4),
		"frost breath" :  		(frost_breath,      	7, 1.3,  False, False, 3),
		# Cytherean
		"wraithwalk" : 			(wraithwalk,   			9, 0,  False, False),

		# Orc Spells
		"poison breath" :  		(poison_breath,   		4, 1.2,  True, True,  3), 
		# Black Eye Spells
		"dark transformation" : (dark_transformation,   0, 3.0,  False, False),
		"dark bolt" :  			(dark_bolt, 			5, 1.6,  True, True,  5), 
		"bloodreave" :  		(bloodreave, 			5, 1.2,  True, True,  7), 
		}









