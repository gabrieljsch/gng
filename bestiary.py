from random import randint

def d(range):
	return randint(1,range)

class Monsters():
	# self,      char, etype, tier,    con, st, dex, int, cha, mspeed,  xp,  pot_weapons, pot_armor, other_items

	array = {

		# Animals
		# Wolves
		"Wolf" : 	  	   	  ["w","beast",1,  2,2,2,2,1,0.75, 4, ['fangs'] , ['wolf pelt']],
		"Direwolf" : 	   	  ["W","beast",2,  4,4,4,2,1,0.85, 8, ['fangs'] , ['wolf pelt']],
		"Direwolf Cannibal" : ["c","beast",2,  3,4,4,2,1,0.75, 8, ['blood fangs'] , ['wolf pelt']],
		"Direwolf Alpha" : 	  ["A","beast",3,  5,5,5,2,1,0.8, 15, ['demon fangs','blood fangs'] , ['wolf pelt']],

		# Kobolds
		"Kobold" : 		  ["k","kobold",1,  2,2,2,1,3,1.0, 4, ['spear','iron shortsword',['hand axe','buckler shield']] , ['leather armor','troll hide']],
		"Kobold Archer" : ["a","kobold",1,  2,2,2,1,3,1.0, 4, ['iron dagger','iron shortsword'] , ['leather armor','troll hide'],['crude shortbow','iron arrow']],
		"Kobold Mage" :   ["m","kobold",2,  2,3,3,4,3,1.0, 8, ['iron dagger'] , ['leather armor','studded armor'],['flame tongue']],
		"Kobold Sneak" :  ["s","kobold",2,  3,3,3,3,3,0.9, 8, [['iron dagger','iron dagger']] , ['leather armor','studded armor']],
		"Greater Kobold": ["K","kobold",3,  4,4,4,3,4,1.0, 15, ['halberd','iron battleaxe',['steel axe','wooden broadshield']] , ['studded armor','drakescale']],

		# Goblins
		"Goblin" : 		   	   ["g","goblin",1,  2,2,3,1,1,0.9, 4, ['stabba','goblin spear','club','bone club'] , ['wolf pelt','bear hide']],
		"Goblin Archer" :      ["a","goblin",1,  2,1,4,1,1,0.85, 4, ['stabba'] , ['wolf pelt','bear hide'], ['goblin bow','iron arrow']],
		"Goblin Skirmisher":   ["g","goblin",1,  3,2,3,1,1,0.85, 6, ['slica','choppa','bone club'] , ['bear hide'], ['buckler shield']],
		"Goblin Spiderrider" : ["s","goblin",2,  4,2,4,1,3,0.6, 8, ['goblin spear','slica'] , ['spider hide'], ['buckler shield']],
		"Witch Goblin" :       ["w","goblin",2,  3,3,3,3,3,0.9, 8, ['bone club'] , ['troll hide'], ['poison breath']],
		"Goblin Nob" : 	       ["n","goblin",2,  4,3,2,1,2,1.0, 8, ['smasha','choppa'] , ['troll hide','spider hide']],
		"Goblin Chief" :   	   ["G","goblin",3,  5,4,4,2,3,0.95, 15,['big choppa','big slica','skull smasha'] , ['berserker mail','leather armor']],

		# Orcs
		"Orc Warboy" : 	   ["o","orc",2,  3,4,3,2,2,1.1, 6, ['slica','choppa','smasha'] , ['bear hide', 'troll hide']],
		"Orc Archer" :     ["a","orc",2,  3,3,4,2,2,1.0, 6, ['choppa', 'slica'] , ['bear hide', 'troll hide'], ['crude shortbow','iron arrow']],
		"Orc Warrior" :    ["o","orc",2,  4,4,3,2,3,1.1, 9, ['slica','smasha','choppa'] , ['troll hide','leather armor'], ['trollhide shield']],
		"Orc Warlock" :    ["W","orc",3,  4,3,3,4,4,1.0, 15, ['toxic slica'] , ['wyvernscale','studded armor'], ['poison breath']],
		"Orc Berserker" :  ["b","orc",3,  4,5,4,2,3,0.8, 15, ['iron greatsword',['choppa','slica']] , ['berserker mail','studded armor'], ['headbutt']],
		"Orc Nob" : 	   ["N","orc",4,  5,5,3,2,4,1.1, 15, ['big choppa','big slica','skull smasha','ice choppa'] , ['berserker mail','scrap plate armor'], ['headbutt']],
		"Orc Warboss" :    ["O","orc",5,  6,6,4,3,5,1.1, 30, ['boss choppa','ice choppa',['black ballista','big slica']] , ['Orcish dreadplate','scrap plate armor'], ['headbutt','iron arrow']],

		# Uruks
		"Uruk Warrior" :   ["u","uruk",3,  4,4,3,2,4,1.0, 15, ['hooked longsword','spiked axe','spiked mace'] , ['blackiron plate'], ['blackiron shield']],
		"Uruk Pikeman" :   ["u","uruk",3,  4,4,3,2,4,1.0, 15, ['uruk-hai pike'] , ['blackiron plate']],
		"Uruk Bolter" :    ["b","uruk",3,  4,3,4,2,4,0.9, 15, ['hooked shortsword'] , ['blackiron plate'], ['uruk crossbow','steel arrow']],
		"Uruk Headhunter" :["h","uruk",4,  4,4,4,2,4,1.0, 22, ['hooked greatsword'] , ['blackiron plate'], ['barbed javelin']],
		"Uruk Berserker" : ["U","uruk",4,  5,4,3,2,4,1.0, 22, ['hooked greatsword'] , ['berserker mail'], ['headbutt']],
		"Uruk Bodyguard" : ["B","uruk",5,  6,5,3,2,6,1.2, 30, ['uruk-hai pike',['hooked greatsword','blackiron shield','shield hit']] , ['blackiron plate']],
		"Uruk Warlord" :   ["U","uruk",6,  7,6,4,2,6,1.0, 60, ['hooked broadsword',['uruk crossbow','hooked longsword']] , ['blackiron plate'], ['blackiron shield','headbutt','steel arrow']],

		# Undead
		"Living Corpse" : 	  ["z","undead",1,  2,2,1,1,3,1.3, 4, ['iron longsword','iron axe','iron dagger'] , ['tattered garments',]],
		"Undead Legionaire" : ["z","undead",2,  3,3,2,2,4,1.2, 8, ['bone cleaver','iron axe','mace'] , ['iron chainmail','rotted chainmail'],['boneshield']],
		"Plaguebearer" :      ["p","undead",2,  4,3,1,2,5,1.3, 8, ['bone cleaver','flail','mace'] , ['rotted chainmail'],['vomit']],
		"Undead Hound" :  	  ["h","undead",3,  4,3,1,3,4,0.7, 15, ['blood fangs'] , ['dog hide']],
		"Flayed One" :    	  ["f","undead",3,  4,2,1,4,5,0.8, 15, ['bone claws'] , ['flayed skins']],
		"Undead Hulk" :   	  ["H","undead",4,  7,4,1,3,5,1.7, 24, ['fist smash'] , ['tattered garments','rotted chainmail','flayed skins']],

		# The Black Eye
		"Black Eye Cultist" :   ["c","man",2,  3,3,3,2,2,1.0, 8, ['mace',['iron dagger','iron dagger']] , ['tainted robe']],
		"Black Eye Disciple" :  ["b","man",3,  4,3,3,4,3,0.9, 14, ['spiked mace'] , ['tainted robe'],['dark bolt']],
		"Black Eye Destroyer" : ["D","man",5,  4,3,3,5,6,1.0, 30, ['spiked mace'] , ['tainted robe'], ['dark transformation','bloodreave']],
		"Abomination" : 		["A","man",5,  6,6,1,1,2,1.6, 30, ['fist smash'] , ['tainted robe']],
		"Black Eye Prophet" :   ["P","man",6,  5,3,3,7,6,1.0, 60, ['spiked mace'] , ['tainted robe'], ['dark transformation','bloodreave']],
		"Black Eye Chosen" :    ["C","man",7,  7,3,3,6,7,1.0, 100, ['spiked mace'] , ['tainted robe'], ['dark transformation','bloodreave']],

		# Dark Elves
		"Guild Scout" : 	 ["s","elf",3,  4,3,5,4,3,0.95, 15, [['thornknife','thornknife']] , ['ironscale mail']],
		"Guild Hunter" : 	 ["h","elf",4,  4,4,6,4,4,0.85, 23, ['sun spear'] , ['ironscale mail'], ['blackwood longbow','iron arrow']],
		"Guild Praetorian" : ["d","elf",4,  5,4,5,4,4,0.95, 23, ['sun spear',['thornblade','gauntlet shield']] , ['blackscale']],
		"Guild Dragoon" :    ["D","elf",5,  6,4,5,4,5,0.60, 30, ['sun spear'] , ['blackscale']],
		"Guild Justicar" :   ["j","elf",5,  6,4,6,4,5,0.85, 30, ['sun spear'] , ['blackscale'], ['gauntlet shield']],

		# Demons
		"Rage Demon" :		  	["r","demon",3,  4,4,4,2,2,0.9, 15, ['bloodletter'] , ['tainted robe','tattered garments','berserker mail']],
		"Plague Demon" :	  	["p","demon",3,  4,3,3,4,5,1.0, 15, ['filthaxe'] , ['tainted robe','tattered garments']],
		"Sloth Demon" :			["s","demon",3,  6,3,2,2,4,1.2, 15, ['flail'] , ['tainted robe','tattered garments']],
		"Chaos Demon" :			["c","demon",3,  4,3,4,4,5,0.95, 15, ['steel dagger'] , ['tainted robe','tattered garments'], ['blink']],
		"Chosen Rage Demon" : 	["R","demon",6,  6,6,6,2,5,0.85, 60, ['skullsplitter','greatflail'] , ['berserker mail']],
		"Chosen Plague Demon" : ["P","demon",6,  6,5,4,4,8,1.0, 60, ['filthaxe'] , ['tainted robe']],
		"Chosen Sloth Demon" : 	["S","demon",6,  9,5,3,2,7,1.1, 60, ['screamflail'] , ['tainted robe']],
		"Chosen Chaos Demon" :	["C","demon",6,  5,4,5,7,8,0.95, 60, ['steel dagger'] , ['tainted robe'], ['blink']],

		# Large Creatures
		"Ogre" : 		  ["O","ogre",1,  5,4,2,1,1,1.4, 15, ['club','bone club'] , ['ogre hide','scrap plate armor']],
		"Green Ooze" : 	  ["O","ooze",1,  4,4,2,1,2,1.2, 15, ['jelly slap','acid slap'] , ['ooze skin']],
		"Giant Spider" :  ["S","spider",2,  4,4,4,2,3,0.7, 30, ['fangs'] , ['spider hide'],['massive stinger']],
		"Cyclops Brute" : ["C","cyclops",3,  6,6,1,3,4,1.1, 60, ['spiked club','greatflail','warhammer'] , ['troll hide','leather armor']],
		"Cave Troll" : 	  ["T","troll",4,  8,7,2,1,5,1.3, 100, ['spiked club','stone fists'] , ['cave troll hide','scrap plate armor']],

		# Dragons
		"Fire Dragon" :  ["D","fire dragon",10,  12,8,7,6,8,1.1, 500, ['dragon fangs','dragon tail'] , ['fire dragonscales']],
		"Frost Dragon" : ["D","frost dragon",10,  14,7,6,4,10,1.2, 500, ['dragon fangs','dragon tail'] , ['frost dragonscales']],
		}

class Bands():  # Tier Bonus :   formations

 	formations = {

 		'Wolf Den' :      (2, [ ['Wolf'], 
 								['Wolf'], 
 						 	    ['Wolf'],
 						 	    ['Direwolf','Direwolf Cannibal'],
 						 	    ['Direwolf Cannibal'],
 						 	    ['Direwolf Alpha'],
 			] ),
 		'Kobold Party' : (2, [ ['Kobold'], 
 								['Kobold Archer'], 
 						 	    ['Kobold','Kobold','Kobold Mage','Greater Kobold'],
 						 	    [],
 						 	    ['Kobold Mage','Kobold Sneak'],
 						 	    ['Greater Kobold'],
			] ),
 		'Orc Band' :      (1, [ ['Goblin','Goblin Archer','Goblin Nob','Goblin Spiderrider', 'Goblin Chief'], 
 								['Goblin','Goblin Skirmisher','Witch Goblin','Orc Warboy','Orc Nob'], 
 						 	    ['Goblin', 'Orc Archer', 'Orc Warboy', 'Orc Warrior', 'Orc Nob'],
 						 	    ['Orc Warrior'],
 						 	    ['Orc Warrior', 'Orc Berserker'],
 						 	    ['Orc Nob'],
 						 	    ['Orc Nob'],
 						 	    ['Orc Warboss'],
 						 	    ['Orc Nob'],
 			] ),
 		'Undead Horde' : (2, [  ['Living Corpse'], 
 								['Living Corpse'], 
 								['Living Corpse','Living Corpse','Undead Legionaire'],
 								['Undead Legionaire', 'Plaguebearer'],
 								['Undead Legionaire', 'Plaguebearer'],
 								['Undead Hound','Flayed One'],
 								['Undead Hulk'],
 			] ),
 		'Uruk Warband' : (-1, [ ['Uruk Warrior'], 
 								['Uruk Bolter'], 
 								['Uruk Warrior', 'Uruk Warrior','Uruk Pikeman', 'Uruk Pikeman'],
 								['Uruk Bolter'],
 								['Uruk Headhunter', 'Uruk Headhunter','Uruk Berserker'],
 								['Uruk Warlord'],
 								['Uruk Bodyguard'],
 			] ),

 		'Dark Elf Guild' :  (-1, [  ['Guild Scout','Guild Scout','Guild Praetorian'], 
	 								['Guild Scout','Guild Hunter'], 
	 								['Guild Praetorian'],
	 								[],
	 								['Guild Dragoon','Guild Justicar'],
	 								['Guild Praetorian'],
	 								['Guild Justicar','Guild Dragoon'],
		] ),

		'Black Eye Cult' :  (0, [   ['Black Eye Cultist', 'Black Eye Cultist'], 
	 								['Black Eye Cultist', 'Black Eye Cultist'], 
	 								['Black Eye Disciple'],
	 								['Black Eye Disciple','Black Eye Disciple','Black Eye Destroyer'],
	 								['Black Eye Destroyer'],
	 								[],
	 								['Black Eye Prophet'],
			] ),

 		'Demon Horde' : (0, [   ['Rage Demon','Plague Demon','Sloth Demon','Chaos Demon'], 
 								['Plague Demon','Sloth Demon','Chaos Demon','Rage Demon'], 
 								['Chaos Demon','Rage Demon','Sloth Demon','Plague Demon'],
 								['Rage Demon','Plague Demon','Sloth Demon','Chaos Demon'], 
 								['Plague Demon','Sloth Demon','Chaos Demon','Rage Demon'],
 								['Chaos Demon','Rage Demon','Sloth Demon','Plague Demon'],
 								[],
 								['Chosen Rage Demon','Chosen Plague Demon','Chosen Sloth Demon','Chosen Chaos Demon'],
 								[],
 								['Chosen Sloth Demon','Chosen Rage Demon','Chosen Plague Demon','Chosen Chaos Demon'],
 			] ),
 		'Wandering Monster' : (0, [	['Ogre','Green Ooze','Giant Spider','Cyclops Brute','Cave Troll']	
 			] ),


 	}

 	# dicto = { 	   1 : ['Orc Band','Undead Horde','Wandering Monster','Wolf Den','Kobold Party'],
 	# 			   2 : ['Orc Band','Undead Horde','Wandering Monster','Wolf Den','Kobold Party'],
 	# 			   3 : ['Orc Band','Undead Horde','Dark Elf Guild','Black Eye Cult','Wandering Monster','Wolf Den','Kobold Party','Demon Horde'],
 	# 			   4 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Wolf Den','Kobold Party','Demon Horde'],
 	# 			   5 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Demon Horde'],
 	# 			   6 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Demon Horde'],
 	# 			   7 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Demon Horde'],
 	# 			   8 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Guild','Black Eye Cult','Wandering Monster','Demon Horde'],
 	# 			   }

 	dicto = { 	   1 : ['Kobold Party'],
 				   2 : ['Kobold Party'],
 				   3 : ['Kobold Party'],
 				   4 : ['Kobold Party'],
 				   5 : ['Demon Horde'],
 				   }

