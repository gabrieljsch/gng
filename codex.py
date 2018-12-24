from random import randint

import sys, os
import termios, fcntl
import select

def d(max_number):
	return randint(1,max_number)

def md(max_number, die_number):
	total = 0
	while die_number > 0:
		total += d(max_number)
		die_number -= 1
	return total

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
	except: print("Python interpreter could not keep up.")

	# Reset the terminal:
	termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	return decision




class Armors:
	# self, name, rep, aclass,  armor_rating, encumbrance, enchantment,  brand(optional)

	array = {

		# Garments and Robes
		"tattered garments" : ['[','grey','garments',1,0, 0],
		"wool robes" : 		  ['[','darkbrown','robes',2,0, 0],
		"tainted robes" : 	  ['[','darkred','robes',4,0, -d(3)],
		"necromancer robes" : ['[','red','robes',2,1, d(2)],
		"bearhide robes" : 	  ['[','darkbrown','robes',3,0, 0],
		"elfrobe" :			  ['[','gold','robes',4,1, d(2)],
		"battle-cleric robes":['[','yellow','robes',5,3, 0],
		"ironkeep robes":	  ['[','bone','robes',6,6, 0],

		# Skins and Hides
		"wolf pelt" : 		['[','grey','hide',1,0, 0],
		"spiderling skin" : ['[','bone','hide',1,-2, 0],
		"direwolf pelt" :   ['[','grey','hide',2,0, 0,'spiked'],
		"bear hide" :   	['[','brown','hide',2,0, 0],
		"ooze skin" :   	['[','green','hide',2,-1, 0],
		"warg pelt" : 		['[','darkbrown','hide',2,1, 0],
		"bone skin" :   	['[','bone','hide',2,1, 0,'spiked'],
		"ogre hide" : 		['[','yellow','hide',3,2, 0],
		"horse hide" :   	['[','brown','hide',2,2, 0],
		"dog hide" : 		['[','tan','hide',3,1, 0],
		"troll hide" :  	['[','yellow','hide',4,2, 0],
		"spider hide" : 	['[','tan','hide',4,1, 0],
		"flayed skins" : 	['[','darkred','hide',5,1, 0],
		"cave troll hide" : ['[','grey','hide',6,4, 0],
		"warpbeast hide" :  ['[','purple','hide',7,6, 0,'voidforged'],

		# Hide Armors
		"leather armor" : 	['[','tan','hide',4,2, 0],
		"hide armor" : 		['[','tan','hide',5,3, 0],
		"studded armor" : 	['[','darkbrown','hide',7,5, 0],

		# Scale Armors
		"chronid shell" :  ['[','bone','scale',3,0, 0],
		"ironscale mail" : ['[','steel','scale',6,3, 0],
		"drakescale" :     ['[','cyan','scale',2,1, d(3)],
		"wyvernscale" :    ['[','magenta','scale',3,3, d(4)],
		"blackscale" : 	   ['[','darkred','scale',6,2, 0],
		# Dragonscales
		"fire dragonscales" :  ['[','red','scale',8,4, d(4),'tempered'],
		"frost dragonscales" : ['[','cyan','scale',9,7, d(4),'icy'],
		"shadow dragonscales" :['[','purple','scale',7,-2, d(4)],
		"bone dragonscales" :  ['[','bone','scale',6,5, d(4),'spiked'],
		"gold dragonscales" :  ['[','gold','scale',10,7, d(4),'runic'],

		# Chainmail Armors
		"rotted chainmail" : 	[']','brown','chainmail',5,4, 0],
		"thornmail": 			[']','darkred','chainmail',5,3, 0,'spiked'],
		"berserker mail" :   	[']','red','chainmail',6,4, 0],
		"iron chainmail" :   	[']','grey','chainmail',7,6, 0],
		"bronze mail" :   		[']','bronze','chainmail',7,4, 0],
		"steel chainmail" :  	[']','steel','chainmail',9,7, 0],
		"godforge chainmail" :  [']','gold','chainmail',10,6, 0],
		"elven swiftmail" : 	[']','gold','chainmail',8,6, 0, 'runic'],

		# Plate Armors
		"chronid plate" : 		  [']','bone','plate',7,3, 0],
		"blackiron plate" :   	  [']','grey','plate',8,6, 0],
		"armored spider plates" : [']','steel','plate',8,5, 0],
		"scrap plate armor" : 	  [']','brown','plate',9,12, 0],
		"iron plate" :  	  	  [']','grey','plate',9,9, 0],
		"steel plate" : 	  	  [']','steel','plate',11,10, 0],
		"Orcish dreadplate" : 	  [']','darkred','plate',12,18, 0],

		# Legendary Armor
		"Kain's Pact" :   	 ['[','red','robes',7,2, d(5)],
		"the Phasic Robes" : ['[','salmon','robes',6,1, d(5)],

		"Plaguebringer" : 	 ['[','darkgreen','chainmail',9,6, d(5)],

		"Bloodshell" : 	  	 [']','darkred','plate',10,4, d(5), 'spiked'],
		"God-Frame" :     	 [']','gold','plate',13,13, d(5)],
		}



class Shields:

	array = {
		# self,rep    name, hands, armor_rating, encumbrance, enchantment, brand

		# Innate
		"armored limb" : 	  ['}','bone',0,3,0,0],
		"plated limb" : 	  ['}','bone',0,5,0,0],

		"buckler shield" : 	  ['}','brown',1,3,1,0],
		"trollhide shield" :  ['}','orange',1,4,2,0],
		"gauntlet shield" :   ['}','steel',1,4,0,0],
		"boneshield" :		  ['}','bone',1,5,4,0],
		"wooden broadshield" :['}','brown',1,5,3,0],
		"bronze aegis" :      ['}','bronze',1,5,1,1],
		"blackiron shield" :  ['}','grey',1,6,4,0],
		"steel kiteshield" :  ['}','steel',1,8,5,0],
		"tower shield" :  	  ['}','darkbrown',1,12,6,0],

		"dwarven broadshield":['}','bronze',2,18,12,0],

		# Legendary Shields
		"Baal's Generator":   ['}','purple',1,8,1,0],
		"the Black Cross":    ['}','grey',1,15,7,0],
		"Invictus": 		  ['}','gold',1,11,4,0],
		}

class Tomes:

	array = {

		# Class Tomes
		"Tome of the Warrior" : [ [("furious charge", 1, 'trait'),	 ("battlecry", 3, 'ability')], 	1, 'darkred'],
		"Tome of the Ranger" :  [ [("martial draw", 1, 'trait'), 	 ("double shot", 2, 'ability')],   1, 'darkgreen'],
		"Tome of the Rogue" :   [ [("deadly precision", 1, 'trait'), ("combat roll", 2, 'ability')],  1, 'bronze'],
		"Tome of the Mage" :    [ [("magic missile", 1, 'spell'),	 ("mana flow", 2, 'trait'),     ("blink", 3, 'spell'),   		("chain lightning", 3, 'spell')], 1, 'blue'],
		"Tome of the Warlock" : [ [("dark bolt", 1, 'spell'),    	 ("life leech", 2, 'trait'),    ("raise skeleton", 3, 'spell'), ("death's hand", 3, 'spell')],    1, 'purple'],
		"Tome of the Paladin" : [ [("bless weapon", 1, 'spell'), 	 ("evening rites", 2, 'trait'), ("flash heal", 3, 'spell')], 									  1, 'bone'],

		"Tome of the Black Eye" : [ [("dark bolt", 1, 'spell'),   ("bloodreave", 4, 'spell'),("dark transformation", 5, 'ability'),("deathmark", 5, 'spell')], 1, 'magenta'],
		"Tome of Iron" : 		  [ [("iron blessing", 3, 'spell')], 1, 'steel'],
		"Tome of Venom" : 		  [ [("poison breath", 1, 'spell'), ("ignite venom", 3, 'spell')], 1, 'green'],
		"Tome of Earth" : 		  [ [("tremor strike", 4, 'spell')], 1, 'tan'],
		"Tome of Fire" :		  [ [("flame tongue", 2, 'spell')], 1, 'fire'],
		"Tome of Ice" : 		  [ [], 1, 'cyan'],
		"Tome of Electricity" :   [ [("chain lightning", 3, 'spell'), ("thunderbolt", 3, 'spell')], 1, 'yellow'],
	}


class Potions:

	array = {

		"healing potion" : "red",
		"orcblood potion" : "darkgreen",
		"resistance potion" : "orange",
		"quicksilver potion" : "steel",

	}


class Brands:

	dict = {
		# Status Effects, and COUNTS GIVEN BY WEAPON BRANDS
		"drained": {"count": 3, "dex_loss": 3},
		"flaming": {"count": 2},
		"envenomed": {"count": 2},
		"grotesque": {"bonushp": 30, "bonusstr": 4},
		"disemboweled": {"strred": 3},
		"frozen": {"count": 2},
	}

	# Manage brands

	# Brands to be randomly given to items in chests and equipped by monsters

	weapon_brands = ["flaming","frozen","silvered","envenomed","hellfire","soulflame","vampiric","antimagic","electrified"]

	ammo_brands = ["flaming","frozen","silvered","envenomed","antimagic","electrified","vorpal"]

	armor_brands = ["spiked","tempered","icy","insulated","voidforged"]

	colors = {
		"flaming": "fire",
		"frozen": "cyan",
		"silvered": "steel",
		"runed": "gold",
		"envenomed": "darkgreen",
		"hellfire": "orange",
		"soulflame": "darkred",
		"vampiric": "red",
		"antimagic": "magenta",
		"electrified": "yellow",
		"holy": "bone",
		"vorpal": "purple",
		"possessed": "springgreen",

		"spiked": "bone",
		"tempered": "red",
		"icy": "cyan",
		"insulated": "yellow",
		"voidforged": "magenta",
		"runic": "gold",
	}


class Ammos:
	#                   rep, wclass, damage
	array = {
		# Arrows/Bolts
		"iron arrow" :     ['(','grey', 'arrow', 1],
		"steel arrow" :    ['(','steel', 'arrow', 2],
		"thornarrow" : 	   ['(','darkgreen', 'arrow', 1,'envenomed'],
		"iron bolt" : 	   ['(','grey', 'bolt', 1],
		"steel bolt" : 	   ['(','steel', 'bolt', 2],

		# Javelins
		"iron javelin" :   ['/','grey', 'javelin', 5],
		"large boulder" :  ['/','grey', 'stone', 3],
		"winged javelin" : ['/','gold', 'javelin', 5],
		"barbed javelin" : ['/','darkred', 'javelin', 6],

		# Other
		"throwing axe" :     ['&','steel', 'throwing axe', 6],
		"throwing knife" :   ['!','steel', 'throwing knife', 3],
		"dwarven swiftaxe" : ['&','gold', 'throwing axe', 7],
	}

	thrown_amclasses = {"javelin", "throwing axe", "throwing knife", "stone"}

	projectile = {
		"bow" : {"arrow"},
		"crossbow" : {"bolt"},
		"ballista" : {"bolt", "arrow"},
		"god bow" : {"bolt", "arrow"}

	}


class Weapons:
	# self,  name, rep, wclass hands,  enchantment, damage, to_hit, speed,   brand(optional), (percent to swing)

	array = {

		# Innate Weapons
		# ---------------------------------------------------------------------
		# Hands
		"fist" : 	   	  	['','bone','fist',0, 0, 3, 9, 0.6, None, 100],
		"fist smash" : 	  	['','bone','fists',0, 0, 15, -2, 1.8, None, 100],
		"claws" : 	   		['','bone','claws',0, 0, 6, 3, 0.8, None, 100],
		"bone claws" : 	   	['','bone','claws',0, 0, 9, 2, 0.9, None, 100],
		"reaper talon" : 	['','bone','scythe',0, 0, 14, 0, 1.5, None, 100],

		# Head
		"horns" :  	   	  	['','bone','horns',0, 0, 7, 0, 0.9, None, 55],
		"headbutt" :   	  	['','darkred','head',0, 0, 8, -1, 0.9, None, 30],

		# Fangs
		"fangs" : 	      	['','bone','fangs',0, 0, 7, 0, 0.8, None, 95],
		"blood fangs" : 	['','darkred','fangs',0, 0, 8, 0, 0.8, "vampiric", 85],
		"spider fangs" :	['','darkgreen','fangs',0, 0, 8, -1, 0.9, "envenomed", 90],
		"lich fangs" : 		['','cyan','fangs',0, 0, 10, 0, 1.2, "frozen", 85],
		"demon fangs" : 	['','red','fangs',0, 0, 10, 0, 0.9, "soulflame", 90],
		"dragon fangs" : 	['','bone','fangs',0, 0, 15, 0, 1.3, None, 90],

		# Tail
		"massive stinger" : ['','green','stinger',0, d(3), 8, -1, 0.9, "envenomed", 40],
		"tail smash" : 	  	['','tan','tail',0, 0, 6, 2, 0.8, None, 30],
		"dragon tail" : 	['','darkred','tail',0, 0, 8, 1, 0.8, None, 25],
		"acid slap" : 	  	['','green','appendage',0, d(2), 6, 1, 1.1, "envenomed", 95],
		"jelly slap" : 		['','purple','appendage',0, d(2), 7, 1, 1.1, None, 95],
		"shield hit" : 	  	['','steel','shield',0, 0, 5, 5, 1.0, None, 15],

		# Feet
		"hooves" : 	  		['','steel','hooves',0, 0, 5, 1, 1.0, None, 30],

		# Ranged Innate / Auras
		"vomit" :      		['','darkgreen','vomit',0, 0, 6, 0, 1.2, None, 40],
		"bioscream" :       ['','magenta','scream',0, 0, 6, 10, 1.4, None, 25],
		# ---------------------------------------------------------------------



	# Basic Weapons

		# Conjured Weapons
		"spectral sword" : 	     ['!','springgreen','sword',1, 0, 0, 3, 0.9],
		"brighthammer":		 	 ['%', 'bone', 'hammer', 1, 0, 0, 0, 1.0, "holy"],
		"blightmaul": 		 	 ['%', 'darkred', 'maul', 1, 0, 0, -1, 1.2, "soulflame"],
		"crackhammer": 			 ['%', 'yellow', 'hammer', 1, 0, 0, -1, 0.9, "electrified"],
		"sunhammer": 			 ['%', 'fire', 'hammer', 1, 0, 0, 3, 1.1, "flaming"],
		"frostmace": 			 ['%', 'cyan', 'mace', 1, 0, 0, 4, 1.2, "frozen"],
		"doomhammer": 		     ['%', 'orange', 'hammer', 1, 0, 0, -2, 0.8, "hellfire"],
		"dreadmace": 			 ['%', 'purple', 'mace', 1, 0, 0, 2, 1.0, "vorpal"],
		"bloodmaul": 			 ['%', 'red', 'maul', 1, 0, 0, 0, 0.9, "vampiric"],
		"soulflail": 			 ['%', 'springgreen', 'flail', 1, 0, 0, 0, 1.0, "possessed"],
		"fangmace": 			 ['%', 'darkgreen', 'mace', 1, 0, 0, 3, 1.1, "envenomed"],

		# Blunt / Gauntlets
		# ---------------------------------------------------------------------
		"club" : 	     ['%','brown','club',1, 0, 9, -1, 1.2],
		"hammer" :       ['%','grey','hammer',1, 0, 10, -1, 1.4],
		"mace" : 		 ['%','bronze','mace',1, 0, 9, 0, 1.3],
		"flail" : 		 ['%','grey','flail',1, 0, 12, -4, 1.6],
		"spiked mace" :  ['%','bronze','mace',1, 0, 11, -1, 1.3],
		"godfist" : 	 ['%','gold','gauntlet',1, 0, 15, -2, 1.8, "runed"],
		"godclaw" : 	 ['&','gold','claw gauntlet',1, 0, 12, 0, 1.3, "electrified"],

		"spiked club" :  ['%','darkbrown','greatclub',2, 0, 16, -4, 1.7],
		"greatflail" : 	 ['%','grey','flail',2, 0, 17, -6, 1.6],
		"warhammer" :    ['%','steel','warhammer',2, 0, 15, -4, 1.5],
		"trollhammer" :  ['%','bone','warhammer',3, 0, 20, -6, 2.2],
		"stone fists" :  ['%','grey','fists',4, 0, 22, -4, 2.3],
		"foehammers" : 	 ['%','orange','fists',4, 0, 19, -3, 2, 'hellfire'],
		# ---------------------------------------------------------------------


		# Staves
		# ---------------------------------------------------------------------
		"oak staff" :	 ['/','brown','staff',1, 0, 5, 4, 1.0],
		"ash staff" :	 ['/','darkbrown','staff',1, 0, 6, 1, 0.9],
		"iron staff" :	 ['/','grey','staff',1, 0, 8, 1, 1.3],
		"warped staff" : ['/','darkbrown','staff',1, 0, 7, 2, 1.1],

		"quarterstaff" : ['/','brown','staff',2, 0, 10, 2, 1.1],
		# ---------------------------------------------------------------------


		# Polearms
		# ---------------------------------------------------------------------
		"spear" :	  ['/','brown','spear',1, 0, 8, 0, 1],

		"pike" :	  ['/','grey','pike',2, 0, 10, 0, 1.2],
		"trident" :   ['/','bronze','polearm',1, 0, 9, 1, 1],
		"halberd" :	  ['/','grey','polearm',2, 0, 12, -2, 1.15],
		"bardiche" :  ['/','steel','polearm',2, 0, 13, -2, 1.4],
		"glaive" : 	  ['/','steel','glaive',2, 0, 14, -2, 1.2],
		"warscythe" : ['/','darkred','scythe',2, 0, 17, -2, 1.8],

		"lance" : 	  ['/','grey','lance',2, 0, 11, -1, 1],
		# ---------------------------------------------------------------------


		# Blades
		# ---------------------------------------------------------------------
		# Daggers
		"iron dagger" :        ['!','grey','dagger',1, 0, 5, 3, 0.75],
		"steel dagger" : 	   ['!','steel','dagger',1, 0, 6, 4, 0.8],
		"glass dagger" : 	   ['!','bone','dagger',1, 0, 7, 3, 0.7],

		# Shortswords
		"iron shortsword" :    ['!','grey','sword',1, 0, 6, 2, 0.9],
		"falchion" :   		   ['!','bronze','sword',1, 0, 8, 0, 1.0],
		"steel shortsword" :   ['!','steel','sword',1, 0, 8, 3, 0.9],
		"gladius" :   		   ['!','steel','sword',1, 0, 8, 3, 0.8],

		# Longswords
		"iron longsword" :     ['!','grey','sword',1, 0, 7, 1, 1.0],
		"cutlass" :    		   ['!','steel','sword',1, 0, 8, 3, 1.15],
		"scimitar"			:  ['!','bronze','sword',1, 0, 10, -1, 1.2],
		"steel longsword" :    ['!','steel','sword',1, 0, 9, 1, 1.0],
		"khopesh"			:  ['!','bronze','sword',1, 0, 12, -2, 1.3],
		"witchhunter blade" :  ['!','steel','sword',1, 0, 10, 3, 1.0,"antimagic"],

		# Bastard swords
		"iron bastard sword" : ['!','grey','bastard sword',2, 0, 11, -1, 1.2],
		"steel bastard sword" :['!','steel','bastard sword',2, 0, 13, -1, 1.1],
		"eviscerator" :		   ['!','bronze','bastard sword',2, 0, 14, 0, 1.3],

		# 2-handed swords
		"iron greatsword" :    ['!','grey','greatsword',2, 0, 11, -2, 1.3],
		"steel greatsword" :   ['!','steel','greatsword',2, 0, 13, -2, 1.2],
		"claymore" :     	   ['!','steel','greatsword',2, 0, 16, -3, 1.3],
		"crusader greatsword" :['!','steel','greatsword',2, 0, 14, -1, 1.3,'flaming'],
		# ---------------------------------------------------------------------


		# Axes
		# ---------------------------------------------------------------------
		"hand axe" : 		['&','grey','axe',1, 0, 7, 0, 0.9],
		"iron axe" : 	    ['&','grey','axe',1, 0, 8, -1, 1.1],
		"bearded axe" : 	['&','steel','axe',1, 0, 7, 1, 1.0],
		"steel axe" : 	    ['&','steel','axe',1, 0, 10, -1, 1.1],
		"chainaxe" : 	    ['&','bronze','axe',1, 0, 11, -2, 1.2],

		"iron battleaxe" :    ['&','grey','greataxe',2, 0, 12, -3, 1.3],
		"bearded greataxe" :  ['&','steel','greataxe',2, 0, 11, -1, 1.1],
		"steel battleaxe" :   ['&','steel','greataxe',2, 0, 14, -3, 1.3],
		"executioner axe" :   ['&','darkred','greataxe',2, 0, 17, -4, 1.6],
		# ---------------------------------------------------------------------


		# Orcish Weapons
		# ---------------------------------------------------------------------
		# Common
		"goblin spear": ['/','brown','spear',1, 0, 7, 3, 1],
		"bone club" :   ['%','bone','club',1, 0, 9, -2, 1.2],
		"smasha": 		['%','brown','hammer',1, 0, 10, -2, 1.2],
		"skull smasha": ['%','darkbrown','warhammer',2, 0, 17, -5, 1.5],
		"stabba" :      ['!','grey','knife',1, 0, 6, 2, 0.85],
		"slica" :       ['!','grey','sword',1, 0, 8, 0, 1],
		"big slica" :   ['!','bronze','greatsword',2, 0, 11, -1, 1.2],
		"choppa" :      ['&','grey','axe',1, 0, 8, -1, 1.1],
		"big choppa" :  ['&','bronze','greataxe',2, 0, 13, -3, 1.3],

		# Uncommon
		"toxic slica":       ['!','darkgreen','sword',1, 0, 9, 0, 1, "envenomed"],
		"ice choppa": 	     ['&','cyan','greataxe',2, 0, 13, -3, 1.5, "frozen"],
		"boss choppa" : 	 ['&','orange','greataxe',2, 0, 16, -4, 1.5],

		# Rare
		"krogtooth choppa" : ['&','darkred','axe',1, 0, 10, -1, 1.2,'hellfire'],
		"krogjaw choppa" :   ['&','darkred','greataxe',2, 0, 18, -4, 1.6,'hellfire'],
		"dethklaw" : 	 	 ['&','orange','claw gauntlet',1, 0, 15, -3, 1.8],
		# ---------------------------------------------------------------------


		# Uruk Weapons
		# ---------------------------------------------------------------------
		"hooked longsword" :     ['!','steel','sword',1, 0, 9, 1, 1.1],
		"hooked shortsword" :    ['!','steel','sword',1, 0, 8, 2, 1.0],
		"spiked axe"  : 		 ['&','steel','axe',1, 0, 10, -2, 1.3],
		"hooked broadsword" :    ['!','bronze','greatsword',2, 0, 15, -3, 1.4],
		"uruk-hai pike" :    	 ['/','darkbrown','pike', 2, 0, 12, -1, 1.2],
		# ---------------------------------------------------------------------


		# Demon Weapons
		# ---------------------------------------------------------------------
		"bloodletter" :     ['!','darkred','bastard sword',2, 0, 10, -2, 1.0],
		"filthaxe" :   		['&','darkgreen','axe',1, 0, 9, -3, 1.3,"envenomed"],
		"skullsplitter" :   ['!','red','greataxe',2, 0, 16, -5, 1.5],
		"screamflail" :   	['%','bone','flail',1, 0, 11, -4, 1.4,"soulflame"],
		"demonfist" : 	 	['%','red','gauntlet',1, 0, 17, -4, 2.1, "soulflame"],
		"demonclaw" : 	    ['&','red','claw gauntlet',1, 0, 13, -3, 1.6, "hellfire"],
		# ---------------------------------------------------------------------


		# Dark Elf Weapons
		# ---------------------------------------------------------------------
		"thornknife" : ['!','purple','knife',1, 0, 5, 3, 0.65],
		"thornblade" : ['!','purple','sword',1, 0, 8, 0, 0.9],
		"sunspear" :   ['/','fire','spear',1, 0, 9, 0, 1.2, "flaming"],
		"sunlance" :   ['/','fire','lance',2, 0, 10, 0, 1.3, "flaming"],
		# ---------------------------------------------------------------------


		# Dread Weapons
		# ---------------------------------------------------------------------
		"voidscythe":   ['/','magenta','scythe', 2, 0, 14, 0, 1.7,"antimagic"],
		"blastmace" :   ['%','orange','mace',1, 0, 11, 0, 1.5,"electrified"],
		"powerglaive" : ['/','yellow','glaive',2, 0, 13, -1, 1.4,"electrified"],
		# ---------------------------------------------------------------------


		# Elvish Weapons
		# ---------------------------------------------------------------------
		"elven wooddagger":  ['!','gold','dagger', 1, 0, 7, 6, 0.65],
		"elven leafblade" :  ['!','gold','bastard sword', 2, 0, 13, 0, 0.9],
		"elven broadspear" : ['/','gold','spear', 2, 0, 12, 2, 0.95],
		"elven longstaff" :  ['/','gold','staff',1, 0, 8, 6, 0.9],
		# ---------------------------------------------------------------------


		# Dwarven Weapons
		# ---------------------------------------------------------------------
		"dwarven longhammer" :  ['%','gold','hammer',2, 0, 12, -2, 1.3],
		"dwarven broadhammer" : ['%','gold','warhammer',2, 0, 18, -2, 1.8],
		"dwarven waraxe" :  	['&','gold','axe',1, 0, 11, -1, 1.2],
		"dwarven broadaxe" :  	['&','gold','greataxe',2, 0, 18, -4, 1.6],
		# ---------------------------------------------------------------------


		# Bone Weapons
		# ---------------------------------------------------------------------
		"bonemace" : 	   ['%','bone','mace',1, 0, 10, 0, 1.5],
		"boneknife" :      ['!','bone','knife',1, 0, 7, 3, 1.0],
		"bone cleaver" :   ['!','bone','sword',1, 0, 9, 2, 1.2],
		"bonesword" :      ['!','bone','sword',1, 0, 8, 2, 1.1],
		"sawtooth blade" : ['!','bone','sword',1, 0, 10, -1, 1.2],
		# ---------------------------------------------------------------------


		# Ranged Weapons
		# ---------------------------------------------------------------------
		# Thrown
		"iron javelin" : 	  ['/','grey','javelin',1, 0, 3, 0, 1.2],
		"barbed javelin" : 	  ['/','darkred','javelin',1, 0, 4, -1, 1.3],
		"winged javelin" : 	  ['/','gold','javelin',1, 0, 3, 3, 0.8],

		"large boulder" : 	  ['%','grey','stone',3, 0, 11, -3, 2.4],
		
		"throwing axe" : 	  ['&','grey','throwing axe',1, 0, 3, -1, 1.3],
		"dwarven swiftaxe" :  ['&','gold','throwing axe',1, 0, 5, -1, 1.2],

		"throwing knife" : 	  ['!','grey','throwing knife',1, 0, 3, 0, 0.9],


		# Projectile
		"goblin bow" :        [')','yellow','bow',2, 0, 5, -4, 1.3],
		"crude shortbow" :    [')','brown','bow',2, 0, 6, -4, 1.35],
		"shortbow" : 		  [')','brown','bow',2, 0, 6, -1, 1.4],
		"recurve bow " : 	  [')','darkbrown','bow',2, 0, 7, -1, 1.4],
		"blackwood longbow" : [')','darkbrown','bow',2, 0, 7, 1, 1.4],
		"longbow" :    		  [')','brown','bow',2, 0, 8, 0, 1.7],
		"hand crossbow" :     [')','tan','crossbow',1, 0, 5, -1, 1.2],
		"crossbow" :     	  [')','darkbrown','crossbow',2, 0, 10, 0, 2],
		"machine crossbow" :  [')','steel','crossbow',2, 0, 7, -4, 0.85],

		"elven longbow" :     [')','gold','bow',2, 0, 8, 2, 1.3],

		"uruk crossbow" :     [')','darkred','crossbow',2, 0, 11, -1, 2.2],

		"ranger longbow" :    [')','darkbrown','bow',2, 0, 10, 1, 1.6],
		"dwarven crossbow" :  [')','gold','crossbow',2, 0, 12, 0, 2],
		"black ballista" : 	  [')','darkred','bow',3, 0, 13, -2, 2.6],
		# ---------------------------------------------------------------------



# Add a Legendary
# ------------------------------------------------------------------

		# Legendary Weapons
		"the Glaive of Gore" :    	  ['/','darkred','glaive',  2, d(5), 16, 0, 1.2],
		"the Singing Spear" : 		  ['/','orange','god spear',   2, d(5), 12, 3, 0.75],
		"Soulreaper" :    	  		  ['/','cyan','scythe',  2, d(5), 17, -2, 2],

		"Kraken" : 					  ['&','springgreen','axe',  1, d(5), 13, 0, 1.1],
		"Krog's Maw" :    		  	  ['&','red','god axe',     2, d(5), 19, -5, 1.6, 'vampiric'],

		"Swiftspike" :        	  	  ['!','salmon','dagger',  	 1, d(5), 7, 3, 0.4],
		"Splinter" :        	  	  ['!','darkgreen','knife',  1, d(5), 8, 4, 0.9, 'envenomed'],
		"Dawn" :        	  	  	  ['!','fire','sword',  	  1, d(5), 12, 2, 1.0, 'flaming'],
		"Bloodreaver" :          	  ['!','darkred','demon sword', 1, -d(5), 17, -3, 1.2],
		"Nightsbane" :     	  	 	  ['!','steel','bastard sword',  2, d(5), 16, 4, 1.2, 'silvered'],
		"Longfang" :              	  ['!','steel','bastard sword',  2, d(5), 14, 3, 1.0],
		"Skullrazor" : 				  ['!','bone','greatsword', 2, d(5), 12, -1, 1.6],
		"God-Cleaver" : 		 	  ['!','orange','executioner greatsword',   2, d(5), 23, -5, 1.7],

		"Worldshaper" :     	 	  ['%','gold','god hammer',  2, d(5), 25, -12, 2.3, 'runed'],
		"Mjölnir" :     	 	  	  ['%','gold','god hammer',  1, d(5), 15, -1, 1.3, 'electrified'],

		"the Gauntlets of Mars": 	  ['&','red','gauntlets',  2, d(5), 20, 0, 1.8],
		"the Talons of Belial": 	  ['&','bone','claw gauntlets',  2, d(5), 15, 0, 1.0],

		"the Blasting Rod": 		  ['/', 'steel', 'staff', 1, d(5), 10, 2, 1.1],

		"Tempest" : 				  [')','gold','god bow',     2, d(5), 12, 0, 1.4],
		"Godfinger" : 				  [')','salmon','god bow',     2, d(5), 8, 20, 2],
		}
				# Legendaries
					# Weapons
	legendaries = {"the Glaive of Gore", "the Singing Spear", "Krog's Maw", "Nightsbane", "Splinter",
				   "Dawn", "Longfang", "Bloodreaver", "God-Cleaver", "Worldshaper", "Tempest", "Godfinger",
				   "Mjölnir", "Soulreaper", "Swiftspike", "the Gauntlets of Mars", "the Talons of Belial",
				   "Kraken", "the Blasting Rod", "Skullrazor",
				    # Shields
				   "Baal's Generator","Invictus","the Black Cross",
				    # Armor
				   "God-Frame", "Bloodshell", "Kain's Pact", "Plaguebringer", "the Phasic Robes"}
	enemy_legendaries = ["Mjölnir", "Krog's Maw", "Skullrazor"]

# ------------------------------------------------------------------


	weapon_classes = { 
		# "You VERB your WCLASS PREPOSITION the ENEMY for __ damage!"
		# Class of weapon : verb, preposition

		# Innate Weapons
		"fist" : ['punch', 'into'],
		"claw" : ['tear', 'into'],
		"claws" : ['tear', 'into'],
		"fists" : ['slam', 'onto'],
		"fangs" : ['bite', 'into'],
		"horns" : ['punch', 'into'],
		"stinger" : ["stab", "into"],
		"tail" : ["smash", "into"],
		"head" : ["smash", "into"],
		"appendage" : ["slap", "into"],
		"hooves" : ["stomp", "onto"],

		# Shield
		"shield" : ["smash", "into"],

		# Blunt
		"hammer" : ["crash", "on"],
		"warhammer" : ["crash", "onto"],
		"god hammer" :["smash", "on"],
		"club" : ["smash", "onto"],
		"greatclub" : ["smash", "onto"],
		"mace" : ["smash", "onto"],
		"maul": ["smash", "into"],
		"flail" : ["smash", "into"],
		"gauntlet" : ['punch', 'into'],
		"gauntlets" : ['punch', 'into'],
		"claw gauntlet" : ['slice', 'into'],
		"claw gauntlets" : ['slice', 'into'],

		# Polearm
		"spear" : ["thrust","into"],
		"pike" : ["thrust", "into"],
		"god spear" : ["plunge", "deep into"],
		"lance" : ["drive", "into"],
		"polearm" : ["slice", "into"],
		"glaive" : ["slice", "into"],
		"scythe" : ["carve", "into"],

		# Dagger
		"dagger" : ["stab", "into"],
		"knife" : ["slash", "into"],

		# Axe
		"axe" : ["hack", "into"],
		"greataxe" : ["carve", "into"],
		"god axe" :   ["chop","through"],

		# Sword
		"sword" : ["slice", "into"],
		"demon sword" : ["carve", "inside"],
		"bastard sword" : ["slash", "into"],
		"god sword" : ["carve", "deep into"],
		"greatsword" : ["cleave", "into"],
		"executioner greatsword" : ["cleave", "into"],
		
		# Staff
		"staff" : ["strike", "into"],

		# Ranged Weapons
		"arrow" : ["loose", "into"],
		"bolt" : ["fire", "into"],
		"vomit" : ["hurl", "onto"],
		"scream" : ["blast", "at"],
		"javelin" : ["hurl", "into"],
		"stone" : ["hurl", "into"],
		"throwing axe" : ["hurl", "into"],
		"throwing knife" : ["stick", "into"],
		
		}



	ranged_wclasses = {"bow", "crossbow", "vomit", "scream", "ballista", "god bow"}


















