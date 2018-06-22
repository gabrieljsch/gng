from random import randint, shuffle
from bestiary import Monsters
from maps import Maps
import ai

import sys, os
import termios, fcntl
import select

def d(range):
	return randint(1,range)

def md(range, number):
	sum = 0
	while number > 0:
		sum += d(range)
		number -= 1
	return sum

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





class Armors():
	# self, name, rep, aclasas,  armor_rating, encumberance, enchantment,  brand(optional)

	array = {

		# Garments and Robes
		"tattered garments" : ['[','grey','garments',1,0, 0],
		"wool robes" : 		  ['[','darkbrown','robes',2,0, 0],
		"tainted robes" : 	  ['[','darkred','robes',4,0, -d(3)],
		"necromancer robes" : ['[','red','robes',2,1, d(2)],
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

		# Hide Armors
		"leather armor" : 	['[','tan','hide',4,2, 0],
		"hide armor" : 		['[','tan','hide',5,3, 0],
		"studded armor" : 	['[','darkbrown','hide',7,5, 0],

		# Scale Armors
		"ironscale mail" : ['[','steel','scale',2,3, d(2)],
		"drakescale" :     ['[','cyan','scale',2,4, d(3)],
		"wyvernscale" :    ['[','magenta','scale',3,4, d(4)],
		"blackscale" : 	   ['[','darkred','scale',6,1, 0],
		# Dragonscales
		"fire dragonscales" :  ['[','red','scale',8,5, d(4),'tempered'],
		"frost dragonscales" : ['[','cyan','scale',9,7, d(4),'icy'],
		"bone dragonscales" :  ['[','bone','scale',6,4, d(4),'spiked'],

		# Chainmail Armors
		"rotted chainmail" : [']','brown','chainmail',4,2, 0],
		"thornmail": 		 [']','darkred','chainmail',4,1, 0,'spiked'],
		"berserker mail" :   [']','red','chainmail',5,3, 0],
		"iron chainmail" :   [']','grey','chainmail',6,5, 0],
		"steel chainmail" :  [']','steel','chainmail',8,6, 0],

		# Plate Armors
		"blackiron plate" :   	  [']','grey','plate',7,6, 0],
		"armored spider plates" : [']','steel','plate',7,4, 0],
		"scrap plate armor" : 	  [']','brown','plate',8,11, 0],
		"iron plate" :  	  	  [']','grey','plate',8,8, 0],
		"steel plate" : 	  	  [']','steel','plate',10,9, 0],
		"Orcish dreadplate" : 	  [']','darkred','plate',12,18, 0],

		# Legendary Armor
		"God-Frame" :     [']','gold','plate',13,13, d(3)],
		"Kain's Pact" :   ['[','darkred','robes',6,0, d(6)],
		"Bloodshell" : 	  ['[','red','plate',9,4, d(6), 'spiked'],
		}



class Shields():

	array = {
		# self,rep    name, hands, armor_rating, encumberance, enchantment, brand

		# Innate
		"armored limb" : 	  ['}','bone',0,3,0,0],

		"buckler shield" : 	  ['}','brown',1,3,1,0],
		"trollhide shield" :  ['}','orange',1,4,2,0],
		"gauntlet shield" :   ['}','steel',1,4,0,0],
		"boneshield" :		  ['}','bone',1,5,4,0],
		"wooden broadshield" :['}','brown',1,5,3,0],
		"bronze aegis" :      ['}','bronze',1,5,1,1],
		"blackiron shield" :  ['}','grey',1,6,4,0],
		"steel kite shield" : ['}','steel',1,8,5,0],
		"tower shield" :  	  ['}','darkbrown',1,12,6,0],
		}


class Brands():
	dict = {
	# Status Effects, and COUNTS GIVEN BY WEAPON BRANDS
		"drained": {"count": 3, "dex_loss": 3},
		"flaming": {"count": 2},
		"envenomed": {"count": 2},
		"grotesque": {"bonushp": 20, "bonusstr": 4},
		"frozen": {"count": 2},
	}

	# Manage brands
	weapon_brands = ["flaming","frozen","silvered","envenomed","hellfire","infernal","vampiric","antimagic","electrified"]

	ammo_brands = ["flaming","frozen","silvered","envenomed","antimagic"]

	armor_brands = ["spiked","tempered","icy"]

	colors = {
		"flaming": "fire",
		"frozen": "cyan",
		"silvered": "steel",
		"envenomed": "darkgreen",
		"hellfire": "orange",
		"infernal": "darkred",
		"vampiric": "red",
		"antimagic": "magenta",
		"electrified": "yellow",
		"holy": "bone",

		"spiked": "bone",
		"tempered": "red",
		"icy": "cyan",
	}


class Ammos():
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
		"throwing axe" :   ['/','grey', 'throwing axe', 6],
		"throwing knife" : ['/','grey', 'throwing knife', 3],
	}

	thrown_amclasses = set(["javelin","throwing axe","throwing knife","stone"])

	projectile = {
		"bow" :      set(["arrow"]),
		"crossbow" : set(["bolt"]),
		"ballista" : set(["bolt","arrow"]),
		"god bow" : set(["bolt","arrow"])

	}


class Weapons():
	# self,  name, rep, wclass hands,  enchantment, damage, to_hit, speed,   brand(optional), (percent to swing) 

	array = {

		# Innate Weapons
		# Hands
		"fist" : 	   	  	['','bone','fist',0, 0, 3, 9, 0.7, None, 100],
		"fist smash" : 	  	['','bone','fists',0, 0, 15, -2, 1.8, None, 100],
		"stone fists" : 	['%','grey','fists',4, 0, 22, -4, 2.2, None, 100],
		"foehammers" : 		['%','steel','fists',4, 0, 18, -3, 2.2, 'hellfire', 100],
		"claws" : 	   		['','bone','claws',0, 0, 7, 3, 0.85, None, 100],
		"bone claws" : 	   	['','bone','claws',0, 0, 10, 2, 0.9, None, 100],

		# Head
		"horns" :  	   	  	['','bone','horns',0, 0, 7, 0, 0.9, None, 55],
		"headbutt" :   	  	['','darkred','head',0, 0, 8, -1, 0.9, None, 30],

		# Fangs
		"fangs" : 	      	['','bone','fangs',0, 0, 7, 0, 0.8, None, 90],
		"blood fangs" : 	['','darkred','fangs',0, 0, 8, 0, 0.8, "vampiric", 85],
		"spider fangs" :	['','darkgreen','fangs',0, 0, 8, -1, 0.9, "envenomed", 90],
		"lich fangs" : 		['','cyan','fangs',0, 0, 10, 0, 1.2, "frozen", 85],
		"demon fangs" : 	['','red','fangs',0, 0, 10, 0, 0.9, "hellfire", 90],
		"dragon fangs" : 	['','bone','fangs',0, 0, 15, 0, 1.3, None, 90],

		# Tail
		"massive stinger" : ['','green','stinger',0, d(3), 8, -1, 0.9, "envenomed", 40],
		"tail smash" : 	  	['','tan','tail',0, 0, 6, 2, 0.8, None, 30],
		"dragon tail" : 	['','darkred','tail',0, 0, 8, 1, 0.8, None, 25],
		"acid slap" : 	  	['','green','appendage',0, d(2), 6, 1, 1.1, "envenomed", 90],
		"jelly slap" : 		['','purple','appendage',0, d(2), 7, 1, 1.1, None, 95],
		"shield hit" : 	  	['','steel','shield',0, 0, 5, 5, 1.0, None, 15],

		# Feet
		"hooves" : 	  		['','steel','hooves',0, 0, 5, 1, 1.0, None, 25],

		# Ranged Innate
		"vomit" :      		['','grey','darkgreen',0, 0, 6, 0, 1.2, None, 40],



	# Basic Weapons

		# Blunt
		"hammer" :       ['%','grey','hammer',1, 0, 10, 0, 1.2],
		"warhammer" :    ['%','steel','warhammer',2, 0, 15, -4, 1.4],
		"trollhammer" :  ['%','steel','warhammer',3, 0, 20, -6, 2.2],
		"club" : 	     ['%','brown','club',1, 0, 9, -1, 1.1],
		"spiked club" :  ['%','darkbrown','greatclub',2, 0, 16, -4, 1.7],
		"flail" : 		 ['%','grey','flail',1, 0, 10, -3, 1.3],
		"greatflail" : 	 ['%','grey','flail',2, 0, 17, -6, 1.5],
		"mace" : 		 ['%','yellow','mace',1, 0, 9, 0, 1.2],
		"spiked mace" :  ['%','yellow','mace',1, 0, 10, -1, 1.25],

		# Staves
		"oak staff" :	 ['/','brown','staff',1, 0, 5, 4, 1.0],
		"iron staff" :	 ['/','grey','staff',1, 0, 8, 1, 1.3],
		"warped staff" : ['/','darkbrown','staff',1, 0, 7, 2, 1.1],
		"quarterstaff" : ['/','brown','staff',2, 0, 10, 2, 1.1],

		# Polearms
		"spear" :	['/','brown','spear',1, 0, 8, 0, 1],
		"pike" :	['/','grey','pike',2, 0, 10, 0, 1.2],
		"halberd" : ['/','grey','polearm',2, 0, 12, -2, 1.15],
		"lance" :   ['/','grey','lance',2, 0, 11, -1, 1],
		"bardiche" :['/','steel','polearm',2, 0, 13, -2, 1.4],

		# Blades
		"iron dagger" :        ['!','grey','dagger',1, 0, 5, 3, 0.75],
		"steel dagger" : 	   ['!','steel','dagger',1, 0, 6, 4, 0.8],
		"iron longsword" :     ['!','grey','sword',1, 0, 7, 1, 1.0],
		"steel longsword" :    ['!','steel','sword',1, 0, 9, 1, 1.0],
		"iron shortsword" :    ['!','grey','sword',1, 0, 6, 2, 0.9],
		"steel shortsword" :   ['!','steel','sword',1, 0, 8, 3, 0.9],
		"iron bastard sword" : ['!','grey','bastard sword',2, 0, 11, -1, 1.2],
		"steel bastard sword" :['!','steel','bastard sword',2, 0, 13, -1, 1.1],
		"iron greatsword" :    ['!','grey','greatsword',2, 0, 11, -2, 1.2],
		"steel greatsword" :   ['!','steel','greatsword',2, 0, 13, -2, 1.2],

		# Axes
		"hand axe" : 		['&','grey','axe',1, 0, 7, 0, 0.9],
		"iron axe" : 	    ['&','grey','axe',1, 0, 8, -1, 1.1],
		"bearded axe" : 	['&','steel','axe',1, 0, 7, 1, 1.1],
		"bearded greataxe" :['&','grey','greataxe',2, 0, 11, -3, 1.1],
		"iron battleaxe" :  ['&','grey','greataxe',2, 0, 12, -3, 1.3],
		"steel axe" : 	    ['&','steel','axe',1, 0, 10, -1, 1.1],
		"steel battleaxe" : ['&','steel','greataxe',2, 0, 14, -3, 1.3],


		# Orcish Weapons
		"goblin spear": ['/','brown','spear',1, 0, 7, 3, 1],
		"bone club" :   ['%','bone','club',1, 0, 9, -2, 1.2],
		"smasha": 		['%','brown','hammer',1, 0, 10, -2, 1.2],
		"skull smasha": ['%','darkbrown','warhammer',2, 0, 17, -5, 1.5],
		"stabba" :      ['!','grey','knife',1, 0, 6, 2, 0.85],
		"slica" :       ['!','grey','sword',1, 0, 8, 0, 1],
		"big slica" :   ['!','grey','greatsword',2, 0, 11, -1, 1.2],
		"choppa" :      ['&','grey','axe',1, 0, 8, -1, 1.1],
		"big choppa" :  ['&','grey','greataxe',2, 0, 13, -3, 1.3],
		"boss choppa" : ['&','grey','greataxe',2, 0, 16, -4, 1.5],

		"toxic slica":  ['!','darkgreen','sword',1, 0, 9, 0, 1, "envenomed"],
		"ice choppa":   ['&','cyan','greataxe',2, 0, 13, -2, 1.4, "frozen"],

		# Uruk Weapons
		"hooked longsword" :     ['!','grey','sword',1, 0, 9, 1, 1.1],
		"hooked shortsword" :    ['!','grey','sword',1, 0, 8, 2, 1.0],
		"spiked axe"  : 		 ['&','grey','axe',1, 0, 10, -2, 1.2],
		"hooked broadsword" :    ['!','grey','greatsword',2, 0, 16, -3, 1.25],
		"uruk-hai pike" :    	 ['/','darkbrown','pike', 2, 0, 12, -1, 1.2],

		# Demon Weapons
		"bloodletter" :     ['!','darkred','demon sword',1, 0, 9, -2, 1.0],
		"skullsplitter" :   ['!','darkred','greataxe',2, 0, 16, -5, 1.6],
		"filthaxe" :   		['!','darkgreen','axe',1, 0, 9, -3, 1.3,"envenomed"],
		"screamflail" :   	['!','red','flail',1, 0, 11, -4, 1.4,"infernal"],

		# Dark Elf Weapons
		"thornknife" : ['!','darkgreen','knife',1, 0, 5, 3, 0.65],
		"thornblade" : ['!','darkgreen','sword',1, 0, 8, 0, 0.9],
		"sun spear" :  ['/','fire','spear',1, 0, 9, 0, 1.2, "flaming"],
		"sunlance" :   ['/','fire','lance',2, 0, 10, 0, 1.3, "flaming"],

		# Elvish Weapons
		"elven wooddagger":  ['!','gold','dagger', 1, 0, 7, 6, 0.65],
		"elven leafblade" :  ['!','gold','bastard sword', 2, 0, 13, 0, 0.95],
		"elven broadspear" : ['/','gold','spear', 2, 0, 12, 2, 0.95],
		"elven longstaff" :  ['/','gold','staff',1, 0, 8, 6, 0.9],

		# Bone Weapons
		"boneknife" :      ['!','bone','knife',1, 0, 7, 3, 1.0],
		"bone cleaver" :   ['!','bone','sword',1, 0, 9, 2, 1.2],
		"sawtooth blade" : ['!','bone','sword',1, 0, 10, -1, 1.2],
		"bonemace" : 	   ['%','bone','mace',1, 0, 10, 0, 1.5],

		# Top-tier
		"gorktooth choppa" :  	['&','darkred','axe',1, 0, 10, -1, 1.2,'hellfire'],
		"khopesh"			: 	['!','steel','sword',1, 0, 12, -2, 1.3],
		"witchhunter blade" : 	['!','steel','sword',1, 0, 10, 3, 1.0,"antimagic"],
		"claymore" :     	  	['!','steel','greatsword',2, 0, 16, -3, 1.3],
		"glaive" :      	  	['/','steel','polearm',2, 0, 14, -2, 1.2],
		"executioner's axe" : 	['&','darkred','greataxe',2, 0, 17, -2, 1.5],
		"gorkjaw choppa" :    	['&','darkred','greataxe',2, 0, 18, -4, 1.6,'hellfire'],
		"dwarven broadaxe" :  	['&','gold','greataxe',2, 0, 18, -4, 1.6],
		"crusader greatsword" : ['!','steel','greatsword',2, 0, 14, -1, 1.3,'holy'],


		# Ranged Weapons

		# Thrown
		"iron javelin" : 	  ['/','grey','javelin',1, 0, 3, 0, 1.2],
		"large boulder" : 	  ['/','grey','stone',3, 0, 11, -3, 2.4],
		"barbed javelin" : 	  ['/','darkred','javelin',1, 0, 4, -1, 1.3],
		"throwing axe" : 	  ['%','grey','throwing axe',1, 0, 3, -1, 1.3],
		"throwing knife" : 	  ['%','grey','throwing knife',1, 0, 3, 0, 0.9],

		"winged javelin" : 	  ['/','gold','javelin',1, 0, 3, 3, 0.8],


		# Projectile
		"goblin bow" :        [')','yellow','bow',2, 0, 5, -4, 1.3],
		"crude shortbow" :    [')','brown','bow',2, 0, 6, -4, 1.35],
		"shortbow" : 		  [')','brown','bow',2, 0, 6, -1, 1.4],
		"recurve bow " : 	  [')','darkbrown','bow',2, 0, 7, -1, 1.4],
		"blackwood longbow" : [')','darkbrown','bow',2, 0, 7, 1, 1.4],
		"longbow" :    		  [')','brown','bow',2, 0, 8, 0, 1.7],

		"elven longbow" :     [')','gold','bow',2, 0, 8, 1, 1.3],

		"uruk crossbow" :     [')','darkred','crossbow',2, 0, 10, 0, 2],

		"ranger longbow" :    [')','darkbrown','bow',2, 0, 10, 1, 1.6],
		"dwarven crossbow" :  [')','gold','crossbow',2, 0, 12, 0, 2],
		"black ballista" : 	  [')','red','bow',3, 0, 12, 0, 2.6],



# Add a Legendary
# ------------------------------------------------------------------

		# Legendary Weapons
		"The Glaive of Gore" :    	  ['/','darkred','polearm',     2, d(5), 16, 0, 1.2],
		"The Singing Spear of Dorn" : ['/','fire','god spear',   1, d(5), 12, 3, 0.75, 'flaming'],
		"The Black Axe of Borke" :    ['&','red','god axe',     2, -10, 28, -5, 1.6, 'vampiric'],
		"Bloodreaver" :          	  ['!','darkred','demon sword', 1, -6, 24, -3, 1, 'vampiric'],
		"Nighthunter" :     	  	  ['%','magenta','bastard sword',  2, d(5), 16, 6, 1.2, 'silvered'],
		"Dawn" :        	  	  	  ['%','fire','sword',  	  1, d(5), 12, 2, 1.0, 'flaming'],
		"Longclaw" :              	  ['!','gold','greatsword',  2, d(5), 18, 5, 1.1],
		"God-Cleaver" : 		 	  ['!','gold','god sword',   2, d(5), 22, -10, 1.4, 'hellfire'],
		"Worldshaper" :     	 	  ['%','purple','god hammer',  2, d(5), 25, -12, 1.6, 'frozen'],
		"Thor's Hammer" :     	 	  ['%','gold','god hammer',  2, d(5), 23, -10, 1.8,'electrified'],

		"Talon" : 					  [')','gold','god bow',     2, d(5), 14, 4, 1.3],
		}

	legendary_weapons = ["The Glaive of Gore","The Singing Spear of Dorn","The Black Axe of Borke","Nighthunter",
						"Dawn","Longclaw","Bloodreaver","The God-Cleaver","Worldshaper","Talon"]

# ------------------------------------------------------------------


	weapon_classes = { 
		# "You VERB your WCLASS PREPOSITION the ENEMY for __ damage!"
		# Class of weapon : verb, preposition

		# Innate Weapons
		"fist" : ['punch', 'into'],
		"claws" : ['tear', 'into'],
		"fists" : ['slam', 'onto'],
		"fangs" : ['bite', 'into'],
		"horns" : ['punch', 'into'],
		"stinger" : ["stab", "into"],
		"tail" : ["smash", "into"],
		"head" : ["smash", "into"],
		"tail" : ["smash", "into"],
		"appendage" : ["slap","into"],
		"hooves" : ["stomp","onto"],

		# Shield
		"shield" : ["smash", "into"],

		# Blunt
		"hammer" : ["crash", "on"],
		"warhammer" : ["crash", "onto"],
		"club" : ["smash", "onto"],
		"greatclub" : ["smash", "onto"],
		"mace" : ["smash", "onto"],
		"flail" : ["smash", "into"],

		# Polearm
		"spear" : ["thrust","into"],
		"pike" : ["thurst", "into"],
		"lance" : ["drive", "into"],
		"polearm" : ["slice", "into"],

		# Dagger
		"dagger" : ["stab", "into"],
		"knife" : ["slip", "into"],

		# Axe
		"axe" : ["hack", "into"],
		"greataxe" : ["carve", "into"],

		# Sword
		"sword" : ["slice", "into"],
		"demon sword" : ["carve", "inside"],
		"greatsword" : ["cleave", "into"],
		"bastard sword" : ["slash", "into"],

		# Staff
		"staff" : ["strike", "into"],

		# Ranged Weapons
		"arrow" : ["loose", "into"],
		"bolt" : ["fire", "into"],
		"vomit" : ["hurl", "onto"],
		"javelin" : ["hurl", "into"],
		"stone" : ["hurl", "into"],
		"throwing axe" : ["hurl", "into"],
		"throwing knife" : ["stick", "into"],

		# God weapons
		"god spear" : ["plunge", "deep into"],
		"god sword" : ["carve", "deep into"],
		"god axe" :   ["chop","through"],
		"god hammer" :["smash","on"],
		}



	ranged_wclasses = set(["bow","crossbow","vomit","ballista","god bow"])








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
				if orig_position != attacker.loc: length = len(ai.shortest_path(attacker.loc, orig_position, map, game, False)) - 1
				else: length = 0

				print("Distance:", str(length) + '/' + str(Weapons.spells['leap'][5]))
				decision = rinput("Leap where? Press spacebar to confirm.")

				for i in range(len(spaces)): print(" ")

				# if decision not in ['h','j','k','l','u','y','b','n',' ']:
				# 	print("That is not a valid direction.")


				prev_position = attacker.loc

				if decision == 'h': mloc = (attacker.loc[0] - 1, attacker.loc[1])
				elif decision == 'j': mloc = (attacker.loc[0], attacker.loc[1] + 1)
				elif decision == 'k': mloc = (attacker.loc[0], attacker.loc[1] - 1)
				elif decision == 'l': mloc = (attacker.loc[0] + 1, attacker.loc[1])
				elif decision == 'y': mloc = (attacker.loc[0] - 1, attacker.loc[1] - 1)
				elif decision == 'u': mloc = (attacker.loc[0] + 1, attacker.loc[1] - 1)
				elif decision == 'b': mloc = (attacker.loc[0] - 1, attacker.loc[1] + 1)
				elif decision == 'n': mloc = (attacker.loc[0] + 1, attacker.loc[1] + 1)
				elif decision == ' ': pass

				# NOTE: FIX ONCE HAVE INFO FOR ENTER BUTTON
				# --------------------------------------------------------------------------

				elif decision in [char for char in "abcdefghiklmnopqrstuvwxyz1234567890"]:
					game.temp_log.append("That is not a valid option.")
					return False

				if game.map.square_identity(mloc) in ['|','#','-']:
					if attacker.name == 'you': print("You cannot go there.")
				elif len(ai.shortest_path(mloc, orig_position, map, game, False)) - 1 > Weapons.spells['leap'][5]:
					length = len(ai.shortest_path(attacker.loc, orig_position, map, game, False)) - 1
					print("That space is out of range.")
				else:
					attacker.loc = mloc

				if decision == ' ':
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


	def tripmine(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(3, 1 + 1/2 * attacker.dex))

		if attacker.name == 'you':
			# Choose Direction
			decision = rinput("Place the mine in which direction?")

			if decision not in ['h','j','k','l','u','y','b','n']:
				game.temp_log.append("That is not a valid direction.")
				return False

			if decision == 'h': mloc = (attacker.loc[0] - 1, attacker.loc[1])
			elif decision == 'j': mloc = (attacker.loc[0], attacker.loc[1] + 1)
			elif decision == 'k': mloc = (attacker.loc[0], attacker.loc[1] - 1)
			elif decision == 'l': mloc = (attacker.loc[0] + 1, attacker.loc[1])
			elif decision == 'y': mloc = (attacker.loc[0] - 1, attacker.loc[1] - 1)
			elif decision == 'u': mloc = (attacker.loc[0] + 1, attacker.loc[1] - 1)
			elif decision == 'b': mloc = (attacker.loc[0] - 1, attacker.loc[1] + 1)
			elif decision == 'n': mloc = (attacker.loc[0] + 1, attacker.loc[1] + 1)

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
					game.game_log.append("The " + attacker.name + " throws down an explosive mine!")
					return True
			return False


	def green_blood(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Check Condition
		if len(attacker.passives) == 0:
			if attacker.name == 'you':
				game.temp_log.append("You have nothing your blood needs to purge.")
			return False


		# Apply Affect + flavor text
		if attacker.name != 'you':
			game.game_log.append("The " + attacker.name + "'s blood purges it of all its stasuses!")
		else:
			game.game_log.append("Your blood purges you of all your statuses!")

		# Purge passives
		game.check_passives(attacker,True)
		return True


	def dark_transformation(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'grotesque', 20

		# Check Condition
		if attacker.hp * 2.5 > attacker.maxhp:
			if attacker.name == 'you':
				game.temp_log.append("You haven't given enough blood.")
			return False


		# Apply Affect + flavor text
		if attacker.name != 'you':
			game.units.remove(attacker)

			roomfiller.spawn("Abomination",attacker.loc)

			game.game_log.append("The " + attacker.name + " mutters a chant, he twists into a grotesque shape!")
		else:
			attacker.passives.append([status, count])
			attacker.hp += Brands.dict[status]['bonushp']
			attacker.maxhp += Brands.dict[status]['bonushp']
			attacker.str += Brands.dict[status]['bonusstr']
			game.game_log.append("Your body twists into a huge, grotesque abomination!")
		return True

	def split(name, attacker, enemy, game, map, roomfiller, ability = False):

		spaces = []
		for x in range(-1,2):
			for y in range(-1,2):
				if attacker.loc[0] + x >= 0 and attacker.loc[1] + y >= 0 and (x != 0 or y != 0): spaces.append((attacker.loc[0] + x, attacker.loc[1] + y))
		shuffle(spaces)


		# Apply Affect + flavor text
		if attacker.name != 'you':

			if attacker.tier <= 3:
				ooze = "Lesser Ooze"
			else:
				ooze = "Bone Ooze"
			roomfiller.spawn(ooze,attacker.loc)

			for space in spaces:
				if game.map.can_move(space) and game.map.square_identity != '+':

					if attacker in game.allies: roomfiller.spawn(ooze,space, True)
					else: roomfiller.spawn(ooze,space)

					# Flavor Text
					game.game_log.append("The " + attacker.name + " splits into two smaller jellies!")	
					return True

			game.game_log.append("The " + attacker.name + " splits into a smaller jelly!")
			return True

		else:
			pass
			# TODO: Implement Player??
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
					game.game_log.append("The " + attacker.name + " calls a " + Skeleton + " to rise from its grave!")
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
				if attacker.name == 'you': game.temp_log.append("You have wraithwalked too recently.")
				return False

		# Apply Affect + flavor text
		attacker.passives.append([status, 2 * count])

		if attacker.name != 'you':
			game.game_log.append("The " + attacker.name + " flickers from the material plane and reappears!")
			while count > 0:
				if attacker.mana < attacker.maxmana: attacker.mana += 1
				if attacker.hp < attacker.maxhp: attacker.hp += 1
				attacker.time = 0
				attacker.turn()
				count -= 1
		else:
			game.game_log.append("You flicker from the material plane")
			while count > 0:
				if attacker.mana < attacker.maxmana: attacker.mana += 1
				if attacker.hp < attacker.maxhp: attacker.hp += 1
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
		status, count = 'poisoned', 2

		# Poison Resist
		resist = enemy.calc_resistances()[2]
		if d(4) <= resist:
			if enemy.name == 'you':
				game.game_log.append("You shrug off the cloud of poison gas bellowed by the " + attacker.name + "!")
			else:
				game.game_log.append("The " + enemy.name + " shrugs off your cloud of poison gas!")
			return True

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You bellow a cloud of poison gas at the " + enemy.name + ", poisoning it!")
		else:
			game.game_log.append("The " + attacker.name + " bellows a cloud of poison gas, poisoning " + enemy.info[0] + "!")

		# Apply Effect
		for passive in enemy.passives:

			if passive[0] == status:
				passive[1] += count
				return True

		enemy.passives.append([status, count])
		return True

	def envenom(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		brand, coated = 'envenomed', False

		# Weapons
		for item in attacker.wielding:
			if item.wclass in Weapons.weapon_classes and item.hands > 0:
				if item.wclass not in Weapons.ranged_wclasses and item.brand != brand:
					item.brand = brand
					coated = True

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
		if attacker.name == 'you':
			game.game_log.append("You coat your weapons in your deadly poison!")
		else:
			game.game_log.append("The " + attacker.name + " coats its weapons in a deadly poison!")

		return True

	def flame_tongue(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'aflame', d(2)
		if ability: damage = int(md(2, 1 + 1/2 * attacker.str))
		else: damage = max(0, int(md(2, 1/2 + 1/2 * attacker.int) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense) )


		# Fire Resist
		resist = enemy.calc_resistances()[1]
		if d(4) <= resist:
			if enemy.name == 'you':
				game.game_log.append("You shrug off the tongue of flame breathed by the " + attacker.name + "!")
			else:
				game.game_log.append("The " + enemy.name + " shrugs off your burst of flame!")
			return True

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You breathe a burst of flame at the " + enemy.name + ", dealing " + str(damage) + " damage and setting it aflame!")
		else:
			game.game_log.append("The " + attacker.name + " breathes a burst of flame, dealing " + enemy.info[0] + " " + str(damage) + " damage and setting " + enemy.info[0] + " aflame!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)

		# Apply Effect
		for passive in enemy.passives:

			if passive[0] == status:
				passive[1] = count
				return True

		enemy.passives.append([status, count])
		return True

	def pounce(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Condition
		los = ai.los(attacker.loc, enemy.loc, Maps.rooms[game.map.map][0], game )
		if len(los) <= 2:
			if attacker.name == 'you': game.temp_log.append("You're too close to do that!")
			return False

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You pounce onto the " + enemy.name + "!")
		else:
			game.game_log.append("The " + attacker.name + " pounces on " + enemy.info[0] + "!")


		attacker.loc = los[-2]

		# Strike
		for weapon in attacker.wielding:
			if weapon.wclass in Weapons.weapon_classes and weapon.hands == 0:
				weapon.strike(attacker, enemy)
		return True


	def iron_grit(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'indominable', 9

		# Check condition
		if attacker.name != 'you':
			for name, count in attacker.passives:
				if name == "indominable": return
			if attacker.hp > attacker.maxhp / 3: return False

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You ready yourself to enter Valhalla!")
		else:
			game.game_log.append("The " + attacker.name + " readies itself to enter Valhalla!")

		# Apply Effect
		for passive in attacker.passives:

			if passive[0] == status:
				passive[1] = count
				return True

		attacker.passives.append([status, count])
		return True

	def iron_blessing(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'blessed iron', 8

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You bless your weapons and armor, they feel lighter!")
		else:
			game.game_log.append("The " + attacker.name + " blesses its weapons and armor!")

		# Apply Effect
		for passive in attacker.passives:

			if passive[0] == status:
				passive[1] = count
				return True

		attacker.passives.append([status, count])
		return True

	def frost_breath(name, attacker, enemy, game, map, roomfiller,  ability = False):

		# Traits
		status, count = "frozen", 3
		if ability: damage = max( 0, int(md(2, 1/2 + 1/2 * attacker.str) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense) )
		else: damage = int(md(2, 1/2 + 1/2 * attacker.int))

		def freeze(attacker, enemy):

			# Frost Resist
			resist = enemy.calc_resistances()[0]
			if d(4) <= resist:
				if enemy.name == 'you':
					game.game_log.append("You shrug off the wave of frost breathed by the " + attacker.name + "!")
				else:
					game.game_log.append("The " + enemy.name + " shrugs off your wave of frost!")
				return True

			# Flavor Text
			if attacker.name == 'you' and enemy.name != 'you':
				game.game_log.append("You breathe a wave of frost that hits the " + enemy.name + ", dealing " + str(damage) + " damage and freezing it!")
			else:
				game.game_log.append("The " + attacker.name + " breathes a wave of frost that freezes " + enemy.info[0] + " and deals " + str(damage) + " damage!")

			# Manage damage
			enemy.hp -= damage
			if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)

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
		damage = max(0, int(md(2, 3/2 + 1/2 * attacker.int) + attacker.calc_mdamage() - enemy.equipped_armor.mdefense))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You conjure a speeding phantom arrow, dealing " + str(damage) + " damage to the " + enemy.name + "!")
		else:
			game.game_log.append("The " + attacker.name + " conjures a speeding phantom arrow, dealing " + enemy.info[0] + " " + str(damage) + " damage!")

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
		if attacker.name == 'you':
			game.game_log.append("You are bathed in the light of your god, you are healed for " + str(heal) + " health!")
		else:
			game.game_log.append("The " + attacker.name + " is bathed in the light of its god, healing for " + str(heal) + " health!")

		# Manage damage
		attacker.hp += heal
		return True

	def wild_equilibrium(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Check Condition
		if attacker.hp == attacker.mana:
			if attacker.name == 'you': game.temp_log.append("Your spirit is already balanced.")
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
		if attacker.name == 'you':
			game.game_log.append("Your spirit balances itself, restoring " + type + "!")
		else:
			game.game_log.append("The " + attacker.name + " balances its spirit, restoring "  + type + "!")

		return True

	def bloodreave(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = max(0, int(md(4, max(2, 3/2 + 1/2 * attacker.int) + attacker.calc_mdamage()  - enemy.equipped_armor.mdefense)))
		self_dam = d(max(1, int(damage / 3)))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You vomit a stream of boiling blood, dealing " + str(damage) + " damage to the " + enemy.name + " and " + str(self_dam) + " damage to yourself!")
		else:
			game.game_log.append("The " + attacker.name + " vomits a stream of boiling blood, dealing " + enemy.info[0] + " " + str(damage) + " damage and some to itself!")

		# Manage damage
		enemy.hp -= damage
		attacker.hp -= self_dam
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)
		return True


	def dark_bolt(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = max(0, int(md(2, 2 + 1/2 * attacker.int) + attacker.calc_mdamage()  - enemy.equipped_armor.mdefense))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You blast the "  + enemy.name + " with a dark bolt, dealing it " + str(damage) + " damage!")
		else:
			game.game_log.append("The " + attacker.name + " blasts " + enemy.info[0] + " with a dark bolt, dealing " + enemy.info[0] + " " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)
		return True

	def feral_bite(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		damage = int(md(3, attacker.str))

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You bite your teeth into the "  + enemy.name + ", dealing it " + str(damage) + " damage!")
		else:
			game.game_log.append("The " + attacker.name + " bites its teeth into " + attacker.info[0] + " for " + str(damage) + " damage!")

		# Manage damage
		enemy.hp -= damage
		if enemy.name != 'you': game.player.well_being_statement(enemy, attacker, name, game)
		return True

	def deathmark(name, attacker, enemy, game, map, roomfiller, ability = False):

		# Traits
		status, count = 'marked', 10

		# Flavor Text
		if attacker.name == 'you':
			game.game_log.append("You mutter an ancient curse, a black mark appears on the " + enemy.name + "!")
		else:
			game.game_log.append("The " + attacker.name + " mutters an ancient curse, a black mark appears on " + enemy.info[0] + "!")

		# Apply Effect
		for passive in enemy.passives:

			if passive[0] == status:
				passive[1] = count
				return True

		enemy.passives.append([status, count])
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
				if enemy.name == 'you':
					game.game_log.append("You shrug off the conjured wild lightning!")
				else:
					game.game_log.append("The " + enemy.name + " shrugs off your wild lightning!")
				return True

			# Flavor Text
			if attacker.name == 'you' and enemy.name != 'you':
				game.game_log.append("You blast the "  + enemy.name + " with wild lightning, dealing it " + str(damage) + " damage!")
			elif attacker.name == 'you' and enemy.name == 'you':
				game.game_log.append("You zap yourself with wild lightning, dealing yourself " + str(damage) + " damage!")
			elif attacker == enemy:
				game.game_log.append("The " + attacker.name + " zaps itself with wild lightning, dealing it " + str(damage) + " damage!")
			else:
				game.game_log.append("The " + attacker.name + " blasts you with wild lightning, dealing " + enemy.info[0] + " " + str(damage) + " damage!")

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










	# List Spells
	spells = {

		# ORG						Name, mana, time, targetbool ?, target?, range (optional)

		# Basic Spells

		# Mage Spells
		"magic missile" :  		(magic_missile,   		3, 1.15, True, False),
		"chain lightning" : 	(chain_lightning, 		8, 1.4,  True, True,  6),
		# Warlock Spells
		"dark bolt" :  			(dark_bolt, 			3, 1.2,  True, True,  7), 
		"raise skeleton" : 		(raise_skeleton,   		6, 2.5,  False, False), 

		# Paladin Spells / Abilities
		"flash heal":			(flash_heal, 			10, 1.3,  False, False), 
		"iron blessing" :  		(iron_blessing,      	10, 1.5,  False, False),
		# Warrior Spells / Abilities

		# Black Orc
		"green blood" : 		(green_blood,   		10, 0.5,  False, False),
		# Cytherean
		"wraithwalk" : 			(wraithwalk,   			9, 0,  False, False),
		# Dragonborn
		"flame tongue" :  		(flame_tongue,      	5, 1.2,  True, True,  4),
		"frost breath" :  		(frost_breath,      	9, 1.3,  False, False, 3),
		# Dwarf
		"iron grit" :  			(iron_grit,      		15, 0.6,  False, False),
		# Elf
		"wild equilibrium" : 	(wild_equilibrium, 		20, 1.5,  False, False), 
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

		# Black Eye Spells
		"dark transformation" : (dark_transformation,   0, 3.0,  False, False),
		"deathmark" :  			(deathmark, 			10, 1.4,  True, False),
		"bloodreave" :  		(bloodreave, 			6, 1.2,  True, True,  6), 
		# Demon Spells
		"blink" : 				(blink, 				4, 1.0,  False, False),
		# Orc Spells
		"poison breath" :  		(poison_breath,   		4, 1.2,  True, True,  4), 
		}









