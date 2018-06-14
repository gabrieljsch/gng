from random import randint, shuffle

def d(range):
	return randint(1,range)

class Monsters():
	# self,      char, etype, tier,    con, st, dex, int, cha, mspeed,  xp,  resistances(fr,fi,po,ac,sh,ex), pot_weapons, pot_armor, other_items

	array = {

		# Animals
		# Wolves
		"Wolf" : 	  	   	  ["w","beast",1,  2,2,2,2,1,0.75, 4, [1,0,0,0,0,0], ['fangs'] , ['wolf pelt']],
		"Direwolf" : 	   	  ["W","beast",2,  4,3,4,2,1,0.85, 8, [1,0,0,0,0,0], ['fangs'] , ['wolf pelt','direwolf pelt']],
		"Direwolf Cannibal" : ["c","beast",2,  3,4,4,2,1,0.75, 8, [1,0,0,0,0,0], ['blood fangs'] , ['wolf pelt']],
		"Direwolf Alpha" : 	  ["A","beast",3,  5,5,5,2,1,0.8, 15, [1,0,0,0,0,0], ['demon fangs','blood fangs'] , ['direwolf pelt']],

		# Kobolds
		"Kobold" : 		  ["k","kobold",1,  2,2,2,1,3,1.0, 4, [0,1,0,1,1,0], ['spear','iron shortsword',['hand axe','buckler shield']] , ['leather armor','troll hide']],
		"Kobold Archer" : ["a","kobold",1,  2,2,2,1,3,1.0, 4, [0,1,0,1,1,0], ['iron dagger','iron shortsword'] , ['leather armor','troll hide'],['crude shortbow','iron arrow']],
		"Kobold Mage" :   ["m","kobold",2,  2,3,3,4,3,1.0, 8, [0,1,0,1,1,0], ['iron dagger'] , ['leather armor','studded armor'],['flame tongue']],
		"Kobold Sneak" :  ["s","kobold",2,  3,3,3,3,3,0.9, 8, [0,1,0,1,1,0], [['iron dagger','iron dagger']] , ['leather armor','studded armor']],
		"Greater Kobold": ["K","kobold",3,  4,4,4,3,4,1.0, 15, [0,1,0,1,1,1], ['halberd','iron battleaxe',['steel axe','wooden broadshield']] , ['studded armor','drakescale']],

		# Goblins
		"Goblin" : 		   	   ["g","goblin",1,  2,2,3,1,1,0.9, 4, [0,0,0,0,0,0], ['stabba','goblin spear','club','bone club'] , ['wolf pelt','bear hide']],
		"Goblin Archer" :      ["a","goblin",1,  2,1,4,1,1,0.85, 4, [0,0,0,0,0,0], ['stabba'] , ['wolf pelt','bear hide'], ['goblin bow','iron arrow']],
		"Goblin Skirmisher":   ["g","goblin",1,  3,2,3,1,1,0.85, 6, [0,0,0,0,0,0], ['slica','choppa','bone club'] , ['bear hide'], ['buckler shield'], ['iron javelin']],
		"Goblin Spiderrider" : ["s","goblin",2,  4,2,4,1,3,0.6, 8, [0,0,0,0,0,0], ['goblin spear',['slica','buckler shield']], ['spider hide'], ['buckler shield']],
		"Witch Goblin" :       ["w","goblin",2,  3,3,3,3,3,0.9, 8, [0,0,1,0,0,0], ['bone club'] , ['troll hide'], ['poison breath']],
		"Goblin Nob" : 	       ["n","goblin",2,  4,3,2,1,2,1.0, 8, [0,0,0,0,0,0], ['smasha','choppa'] , ['troll hide','spider hide']],
		"Goblin Chief" :   	   ["G","goblin",3,  5,4,4,2,3,0.95, 15, [0,0,0,0,0,0], ['big choppa','big slica','skull smasha'] , ['berserker mail','leather armor']],

		# Orcs
		"Orc Warboy" : 	   ["o","orc",2,  3,4,3,2,2,1.1, 6, [0,0,0,0,0,0], ['slica','choppa','smasha'] , ['bear hide', 'troll hide']],
		"Orc Archer" :     ["a","orc",2,  3,3,4,2,2,1.0, 6, [0,0,0,0,0,0], ['choppa', 'slica'] , ['bear hide', 'troll hide'], ['crude shortbow','iron arrow']],
		"Orc Warrior" :    ["o","orc",2,  4,4,3,2,3,1.1, 9, [0,0,0,0,0,0], ['slica','smasha','choppa'] , ['troll hide','leather armor'], ['trollhide shield']],
		"Orc Berserker" :  ["b","orc",3,  4,5,4,2,3,0.8, 15, [1,1,1,0,1,0], ['iron greatsword',['choppa','slica']] , ['berserker mail','studded armor'], ['headbutt']],
		"Orc Nob" : 	   ["N","orc",4,  5,5,3,2,4,1.2, 15, [0,0,0,0,0,1], ['big choppa','big slica','skull smasha','ice choppa'] , ['berserker mail','scrap plate armor'], ['headbutt','green blood']],
		"Orc Warlock" :    ["W","orc",4,  4,3,3,4,4,1.0, 15, [0,0,3,0,0,0], ['toxic slica','oak staff'] , ['wyvernscale','studded armor'], ['poison breath','raise skeleton','green blood']],
		"Orc Warboss" :    ["O","orc",5,  6,6,4,3,5,1.2, 40, [0,0,0,0,0,3], ['boss choppa','ice choppa',['black ballista','big slica']] , ['Orcish dreadplate','scrap plate armor'], ['headbutt','iron bolt','green blood']],

		# Uruks
		"Uruk Warrior" :   ["u","uruk",3,  4,4,3,2,4,1.0, 15, [0,0,0,0,0,0], ['hooked longsword','spiked axe','spiked mace'] , ['blackiron plate'], ['blackiron shield']],
		"Uruk Pikeman" :   ["u","uruk",3,  4,4,3,2,4,1.0, 15, [0,0,0,0,0,0], ['uruk-hai pike'] , ['blackiron plate']],
		"Uruk Bolter" :    ["b","uruk",3,  4,3,4,2,4,0.9, 15, [0,0,0,0,0,0], ['hooked shortsword'] , ['blackiron plate'], ['uruk crossbow','iron bolt']],
		"Uruk Headhunter" :["h","uruk",4,  4,4,4,2,4,1.0, 22, [0,0,0,0,0,0], ['hooked broadsword'] , ['blackiron plate'], ['barbed javelin']],
		"Uruk Berserker" : ["U","uruk",4,  5,4,3,2,4,1.0, 22, [2,2,2,0,2,0], ['hooked broadsword'] , ['berserker mail'], ['headbutt']],
		"Uruk Bodyguard" : ["B","uruk",5,  6,5,3,2,6,1.2, 40, [0,0,0,0,0,0], ['uruk-hai pike', ['hooked broadsword','blackiron shield']], ['blackiron plate'], ['shield hit']],
		"Uruk Warlord" :   ["U","uruk",6,  7,6,4,2,6,1.0, 60, [0,0,0,0,0,0], ['hooked broadsword',['uruk crossbow','hooked longsword']] , ['blackiron plate'], ['blackiron shield','headbutt','steel bolt']],

		# Undead
		"Skeleton" : 	  	 ["s","skeleton",1,  2,2,1,1,2,1.1, 4, [0,0,5,0,0,0], ['iron longsword','iron axe','iron shortsword'] , ['tattered garments']],
		"Skeleton Archer" :  ["a","skeleton",2,  3,2,3,2,4,1.1, 8, [0,0,5,0,0,0], ['boneknife','iron dagger'] , ['tattered garments'],['recurve bow','iron arrow']],
		"Skeleton Warrior" : ["s","skeleton",2,  4,2,2,2,4,1.2, 8, [0,0,5,0,0,0], ['bone cleaver','sawtooth blade','bonemace'] , ['iron chainmail','studded armor'],['buckler shield']],

		"Living Corpse" : 	  ["z","undead",1,  2,2,1,1,3,1.3, 4, [0,0,0,0,0,0], ['iron longsword','iron axe','iron dagger'] , ['tattered garments',]],
		"Undead Legionaire" : ["z","undead",2,  3,3,2,2,4,1.2, 8, [0,0,0,0,0,0], ['bone cleaver','iron axe','mace'] , ['iron chainmail','rotted chainmail'],['boneshield']],
		"Plaguebearer" :      ["p","undead",2,  4,3,1,2,5,1.3, 8, [0,0,5,0,0,0], ['bone cleaver','flail','mace'] , ['rotted chainmail'],['vomit']],
		"Undead Hound" :  	  ["h","undead",3,  4,3,1,3,4,0.7, 15, [0,0,0,0,0,0], ['blood fangs'] , ['dog hide']],
		"Flayed One" :    	  ["f","undead",3,  4,2,1,4,5,0.8, 15, [0,0,0,0,0,0], ['bone claws'] , ['flayed skins']],
		"Undead Hulk" :   	  ["H","undead",4,  7,4,1,3,5,1.7, 24, [0,0,0,0,0,0], ['fist smash'] , ['tattered garments','rotted chainmail','flayed skins']],

		# The Black Eye
		"Cultist" :   	   		["c","man",2,  3,3,3,1,1,1.0, 8, [0,0,0,0,0,0],  ['mace',['hand axe','iron dagger']] , ['tainted robes']],
		"Cult Disciple" :  		["d","man",3,  3,3,3,3,3,1.0, 14, [0,0,0,0,0,0], ['sawtooth blade','flail'] , ['tainted robes'],['dark bolt']],
		"Cult Husk" :  			["h","undead",3,  4,3,2,1,1,1.3, 14, [1,1,1,1,1,0], ['iron bastard sword','bearded greataxe'] , ['tainted robes']],
		"Cult Gravewhisperer" : ["g","man",4,  4,3,3,4,5,1.0, 22, [0,0,0,0,0,0], ['warped staff'] , ['tainted robes'], ['raise skeleton']],
		"Abomination" :    		["A","undead",5,  6,6,1,1,2,1.6, 40, [0,0,0,0,0,0], ['fist smash'] , ['tainted robes']],
		"Cult Destroyer" : 		["D","man",5,  5,3,3,7,6,1.0, 60, [0,0,0,0,0,0], ['spiked mace'] , ['tainted robes'], ['dark transformation','bloodreave','deathmark']],
		"Cult Prophet" :   		["P","man",7,  7,3,3,6,7,1.0, 100, [0,0,0,0,0,0], ['warped staff'] , ['tainted robes'], ['raise skeleton','bloodreave','deathmark']],

		# Dark Elves
		"Dark Wardancer" :  ["s","elf",4,  3,3,5,4,3,0.80, 23, [1,0,0,0,0,0], [['thornknife','thornknife']] , ['ironscale mail']],
		"Dark Hunter" : 	 ["h","elf",5,  4,4,6,4,3,0.85, 40, [0,0,1,0,0,0], ['thornknife'] , ['ironscale mail','leather armor'], ['blackwood longbow','thornarrow']],
		"Dark Praetorian" : ["p","elf",5,  5,4,5,4,3,0.95, 40, [1,0,0,0,0,0], ['sun spear',['thornblade','gauntlet shield']] , ['blackscale']],
		"Dark Dragoon" :    ["d","elf",6,  6,4,5,4,4,0.60, 60, [1,0,1,1,0,0], ['sunlance','thornblade'] , ['blackscale']],
		"Dark Justicar" :   ["j","elf",6,  5,4,6,4,4,0.85, 60, [1,0,0,0,0,0], ['sun spear',['thornknife','thornknife']] , ['blackscale','thornmail'], ['gauntlet shield']],
		"Dark Archon" :   	 ["A","elf",7,  6,6,7,5,4,0.90, 100, [1,1,2,1,1,0], ['glaive',['thornblade','thornblade']] , ['blackscale','thornmail'], ['gauntlet shield']],

		# Demons
		"Rage Demon" :		  	["r","demon",3,  3,4,4,2,2,0.9, 15, [0,2,0,0,0,0], ['bloodletter'] , ['tainted robes','tattered garments']],
		"Pride Demon" :	  		["p","demon",3,  4,3,3,4,5,1.0, 15, [0,0,0,0,0,2], ['iron axe','bone cleaver'] , ['tainted robes','tattered garments'],['boneshield']],
		"Sloth Demon" :			["s","demon",3,  6,2,2,2,4,1.2, 15, [2,0,0,0,0,0], ['flail'] , ['tainted robes','tattered garments']],
		"Chaos Demon" :			["c","demon",3,  3,3,4,4,5,0.95, 15, [0,0,0,0,2,0], ['armored limb','horns','vomit'] , ['tainted robes','tattered garments'], ['blink','claws']],
		"Chosen Rage Demon" : 	["R","demon",6,  6,6,6,2,5,0.85, 60, [0,3,0,0,0,0], ['skullsplitter','greatflail'] , ['berserker mail']],
		"Chosen Pride Demon" : 	["P","demon",6,  6,5,4,4,8,1.0, 60, [0,0,0,0,0,3], ['filthaxe'] , ['tainted robes'],['boneshield']],
		"Chosen Sloth Demon" : 	["S","demon",6,  9,4,3,2,7,1.1, 60, [3,0,0,0,0,0], ['screamflail'] , ['tainted robes']],
		"Chosen Chaos Demon" :	["C","demon",6,  5,4,5,7,8,0.95, 60, [0,0,0,0,3,0], ['bone claws'] , ['tainted robes'], ['blink']],

		# Large Creatures
		"Ogre" : 		  ["O","ogre",1,  5,4,2,1,1,1.4, 15, [0,0,0,0,0,1], ['club','bone club'] , ['ogre hide','scrap plate armor']],
		"Green Ooze" : 	  ["Z","ooze",1,  5,3,3,3,2,1.1, 15, [0,0,3,0,0,0], ['jelly slap','acid slap'] , ['ooze skin']],
		"Giant Spider" :  ["S","spider",2,  4,4,4,2,3,0.7, 40, [0,0,2,0,0,0], ['fangs'] , ['spider hide'],['massive stinger']],
		"Cyclops Brute" : ["C","cyclops",3,  6,6,1,3,4,1.1, 60, [0,0,0,0,0,1], ['spiked club','greatflail','warhammer'] , ['troll hide','leather armor']],
		"Cave Troll" : 	  ["T","troll",4,  8,7,2,1,5,1.3, 100, [1,1,0,0,0,1], ['spiked club','stone fists'] , ['cave troll hide','scrap plate armor']],

		# Dragons
		"Fire Dragon" :  ["D","fire dragon",10,  12,8,7,6,8,1.1, 500, [0,2,0,0,0,0], ['dragon fangs','dragon tail'] , ['fire dragonscales']],
		"Frost Dragon" : ["D","frost dragon",10,  14,7,6,4,7,1.2, 500, [2,0,0,0,0,0], ['dragon fangs','dragon tail'] , ['frost dragonscales'], ['frost breath']],
		"Bone Dragon" :  ["D","bone dragon",10,  13,8,5,5,10,1.0, 500, [0,0,4,0,0,0], ['dragon fangs','dragon tail','horns'] , ['bone dragonscales']],
		}

class Bands():  # Tier Bonus :   formations

 	formations = {

 		'Wolf Den' :      (2, [ ['Wolf'], 
 								['Wolf','Direwolf Cannibal'], 
 						 	    ['Wolf','Direwolf Cannibal'],
 						 	    ['Direwolf','Direwolf Cannibal'],
 						 	    ['Direwolf Cannibal'],
 						 	    ['Direwolf Alpha'],
 			] ),
 		'Kobold Party' : (2, [  ['Kobold'], 
 								['Kobold Archer'], 
 						 	    ['Kobold','Kobold','Kobold Mage','Greater Kobold'],
 						 	    [],
 						 	    ['Kobold Mage','Kobold Sneak'],
 						 	    ['Greater Kobold'],
			] ),
 		'Orc Band' :      (1, [ ['Goblin','Goblin Archer','Goblin Nob','Goblin Spiderrider', 'Goblin Chief'], 
 								['Goblin Archer','Goblin Skirmisher','Witch Goblin','Orc Warboy','Orc Nob'], 
 						 	    ['Goblin', 'Orc Archer', 'Orc Warboy', 'Orc Warrior', 'Orc Nob'],
 						 	    ['Orc Warrior'],
 						 	    ['Orc Warrior', 'Orc Berserker'],
 						 	    ['Orc Nob'],
 						 	    ['Orc Nob','Orc Warlock'],
 						 	    ['Orc Warboss'],
 						 	    ['Orc Nob'],
 			] ),
 		'Undead Horde' : (2, [  ['Living Corpse'], 
 								['Living Corpse'], 
 								['Living Corpse','Living Corpse','Undead Legionaire'],
 								['Undead Legionaire', 'Undead Legionaire','Plaguebearer','Flayed One'],
 								['Undead Legionaire', 'Plaguebearer','Flayed One'],
 								['Undead Hound','Flayed One'],
 								['Undead Hulk'],
 			] ),
 		'Uruk Warband' : (-1, [ ['Uruk Warrior'], 
 								['Uruk Bolter'], 
 								['Uruk Warrior','Uruk Warrior','Uruk Pikeman', 'Uruk Pikeman'],
 								['Uruk Bolter'],
 								['Uruk Headhunter','Uruk Headhunter','Uruk Berserker'],
 								['Uruk Warlord'],
 								['Uruk Bodyguard'],
 			] ),

 		'Dark Elf Guild' :  (-2, [  ['Dark Wardancer','Dark Wardancer','Dark Praetorian'], 
	 								['Dark Wardancer','Dark Hunter'], 
	 								['Dark Praetorian'],
	 								[],
	 								['Dark Dragoon','Dark Justicar'],
	 								['Dark Praetorian'],
	 								['Dark Justicar','Dark Dragoon'],
	 								[],
	 								['Dark Archon']
		] ),

		'Black Eye Cult' :  (0, [   ['Cultist', 'Cultist','Cultist','Cult Disciple'], 
	 								['Cultist', 'Cultist','Cultist','Cult Disciple'], 
	 								['Cult Disciple'],
	 								[],
	 								['Cult Gravewhisperer'],
	 								['Cult Husk','Cult Husk','Cult Destroyer'],
	 								[],
	 								['Cult Destroyer'],
	 								[],
	 								[],
	 								['Cult Prophet']
			] ),

 		'Demon Horde' : (0, [   ['Rage Demon','Chaos Demon','Pride Demon','Sloth Demon'], 
 								['Rage Demon','Chaos Demon','Pride Demon','Sloth Demon'], 
 								['Rage Demon','Chaos Demon','Pride Demon','Sloth Demon'],
 								['Rage Demon','Chaos Demon','Pride Demon','Sloth Demon'], 
 								['Pride Demon','Sloth Demon','Chaos Demon','Rage Demon'],
 								['Sloth Demon','Rage Demon','Rage Demon','Rage Demon'],
 								[],
 								['Chosen Rage Demon','Chosen Pride Demon','Chosen Sloth Demon','Chosen Chaos Demon'],
 								[],
 								['Chosen Sloth Demon','Chosen Rage Demon','Chosen Pride Demon','Chosen Chaos Demon'],
 			] ),

 		'Wandering Monster' : (0, [	['Ogre','Green Ooze','Giant Spider','Cyclops Brute','Cave Troll']	
 			] ),

 		'Dragon Nest' : (0, [	['Fire Dragon','Frost Dragon','Bone Dragon']	
 			] ),


 	}

 	dicto = { 	   1 : ['Orc Band','Undead Horde','Wandering Monster','Wolf Den','Kobold Party'],
 				   2 : ['Orc Band','Undead Horde','Wandering Monster','Wolf Den','Kobold Party'],
 				   3 : ['Orc Band','Undead Horde','Black Eye Cult','Wandering Monster','Wolf Den','Kobold Party','Demon Horde'],
 				   4 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Wolf Den','Kobold Party','Demon Horde'],
 				   5 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Demon Horde'],
 				   6 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Demon Horde'],
 				   7 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Demon Horde'],
 				   8 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Demon Horde'],
 				   }

 	# dicto = { 	   1 : ['Black Eye Cult'],
 	# 			   2 : ['Wolf Den'],
 	# 			   3 : ['Uruk Warband'],
 	# 			   4 : ['Uruk Warband'],
 	# 			   5 : ['Demon Horde'],
 	# 			   }

