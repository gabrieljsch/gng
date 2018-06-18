from random import randint, shuffle

def d(range):
	return randint(1,range)

class Monsters():
	# self,      char, etype, tier,    con, st, dex, int, cha, mspeed,  xp,  resistances(fr,fi,po,ac,sh,ex), pot_weapons, pot_armor, other_items

	array = {

		# Animals
		# Wolves
		"Wolf" : 	  	   	  ["w","steel","beast",1,  2,2,2,2,1,0.75, 4, [1,0,0,0,0,0], ['fangs'] , ['wolf pelt']],
		"Direwolf" : 	   	  ["W","steel","beast",2,  4,3,4,2,1,0.85, 8, [1,0,0,0,0,0], ['fangs'] , ['wolf pelt','direwolf pelt']],
		"Direwolf Cannibal" : ["c","red","beast",2,  3,4,4,2,1,0.75, 8, [1,0,0,0,0,0], ['blood fangs'] , ['wolf pelt']],
		"Direwolf Alpha" : 	  ["A","darkred","beast",3,  5,5,5,2,1,0.8, 15, [1,0,0,0,0,0], ['demon fangs','blood fangs'] , ['direwolf pelt']],

		# Kobolds
		"Kobold" : 		  ["k","orange","kobold",1,  2,2,2,1,3,1.0, 4, [0,1,0,1,1,0], ['spear','iron shortsword',['hand axe','buckler shield']] , ['leather armor','troll hide']],
		"Kobold Archer" : ["a","orange","kobold",1,  2,2,2,1,3,1.0, 4, [0,1,0,1,1,0], ['iron dagger','iron shortsword'] , ['leather armor','troll hide'],['crude shortbow','iron arrow']],
		"Kobold Mage" :   ["m","magenta","kobold",2,  2,3,3,4,3,1.0, 8, [0,1,0,1,1,0], ['iron dagger'] , ['leather armor','studded armor'],['flame tongue']],
		"Kobold Sneak" :  ["s","darkgreen","kobold",2,  3,3,3,3,3,0.9, 8, [0,1,0,1,1,0], [['iron dagger','iron dagger']] , ['leather armor','studded armor']],
		"Greater Kobold": ["K","darkred","kobold",3,  4,4,4,3,4,1.0, 15, [0,1,0,1,1,1], ['halberd','iron battleaxe',['steel axe','wooden broadshield']] , ['studded armor','drakescale']],

		# Goblins
		"Goblin" : 		   	   ["g","yellow","goblin",1,  2,2,3,1,1,0.9, 4, [0,0,0,0,0,0], ['stabba','goblin spear','club','bone club'] , ['wolf pelt','bear hide']],
		"Goblin Archer" :      ["a","yellow","goblin",1,  2,1,4,1,1,0.85, 4, [0,0,0,0,0,0], ['stabba'] , ['wolf pelt','bear hide'], ['goblin bow','iron arrow']],
		"Goblin Skirmisher":   ["g","yellow","goblin",1,  3,2,3,1,1,0.85, 6, [0,0,0,0,0,0], ['slica','choppa','bone club'] , ['bear hide'], ['buckler shield'], ['iron javelin']],
		"Goblin Spiderrider" : ["s","brown","goblin",2,  4,2,4,1,3,0.6, 8, [0,0,0,0,0,0], ['goblin spear',['slica','buckler shield']], ['spider hide'], ['buckler shield']],
		"Witch Goblin" :       ["w","magenta","goblin",2,  3,3,3,3,3,0.9, 8, [0,0,1,0,0,0], ['bone club'] , ['troll hide'], ['poison breath']],
		"Goblin Nob" : 	       ["n","yellow","goblin",2,  4,3,2,1,2,1.0, 8, [0,0,0,0,0,0], ['smasha','choppa'] , ['troll hide','spider hide']],
		"Goblin Chief" :   	   ["G","purple","goblin",3,  5,4,4,2,3,0.95, 15, [0,0,0,0,0,0], ['big choppa','big slica','skull smasha'] , ['berserker mail','leather armor']],

		# Orcs
		"Orc Warboy" : 	   ["o","green","orc",2,  3,4,3,2,2,1.1, 6, [0,0,0,0,0,0], ['slica','choppa','smasha'] , ['bear hide', 'troll hide']],
		"Orc Archer" :     ["a","green","orc",2,  3,3,4,2,2,1.0, 6, [0,0,0,0,0,0], ['choppa', 'slica'] , ['bear hide', 'troll hide'], ['crude shortbow','iron arrow']],
		"Orc Warrior" :    ["o","darkgreen","orc",2,  4,4,3,2,3,1.1, 9, [0,0,0,0,0,0], ['slica','smasha','choppa'] , ['troll hide','leather armor'], ['trollhide shield']],
		"Orc Berserker" :  ["b","red","orc",3,  4,5,4,2,3,0.8, 15, [1,1,1,0,1,0], ['iron greatsword',['choppa','slica']] , ['berserker mail','studded armor'], ['headbutt']],
		"Orc Nob" : 	   ["N","darkgreen","orc",4,  5,5,3,2,4,1.2, 15, [0,0,0,0,0,1], ['big choppa','big slica','skull smasha','ice choppa'] , ['berserker mail','scrap plate armor'], ['headbutt','green blood']],
		"Orc Warlock" :    ["W","magenta","orc",4,  4,3,3,4,4,1.0, 15, [0,0,3,0,0,0], ['toxic slica','oak staff'] , ['wyvernscale','studded armor'], ['poison breath','raise skeleton','green blood']],
		"Orc Warboss" :    ["O","darkred","orc",5,  6,6,4,3,5,1.2, 40, [0,0,0,0,0,3], ['boss choppa','ice choppa',['black ballista','big slica']] , ['Orcish dreadplate','scrap plate armor'], ['headbutt','iron bolt','green blood']],

		# Uruks
		"Uruk Warrior" :   ["u","steel","uruk",3,  4,4,3,2,4,1.0, 15, [0,0,0,0,0,0], ['hooked longsword','spiked axe','spiked mace'] , ['blackiron plate'], ['blackiron shield']],
		"Uruk Pikeman" :   ["u","steel","uruk",3,  4,4,3,2,4,1.0, 15, [0,0,0,0,0,0], ['uruk-hai pike'] , ['blackiron plate']],
		"Uruk Bolter" :    ["b","steel","uruk",3,  4,3,4,2,4,0.9, 15, [0,0,0,0,0,0], ['hooked shortsword'] , ['blackiron plate'], ['uruk crossbow','iron bolt']],
		"Uruk Headhunter" :["h","steel","uruk",4,  4,4,4,2,4,1.0, 22, [0,0,0,0,0,0], ['hooked broadsword'] , ['blackiron plate'], ['barbed javelin']],
		"Uruk-hai" : 	   ["u","red","uruk",4,  5,4,3,2,4,1.0, 22, [2,0,2,0,2,0], ['hooked broadsword'] , ['berserker mail'], ['headbutt']],
		"Uruk Bodyguard" : ["u","purple","uruk",5,  6,5,3,2,6,1.2, 40, [0,0,0,0,0,0], ['uruk-hai pike', ['hooked broadsword','blackiron shield']], ['blackiron plate'], ['shield hit']],
		"Uruk Warlord" :   ["U","dark_red","uruk",6,  7,6,4,2,6,1.0, 60, [0,0,0,0,0,0], ['hooked broadsword',['uruk crossbow','hooked longsword']] , ['blackiron plate'], ['blackiron shield','headbutt','steel bolt']],

		# Undead
		"Skeleton" : 	  	 ["s","bone","skeleton",1,  2,2,1,1,2,1.1, 4, [0,0,5,0,0,0], ['iron longsword','iron axe','iron shortsword'] , ['tattered garments']],
		"Skeleton Archer" :  ["a","bone","skeleton",2,  3,2,3,2,4,1.1, 8, [0,0,5,0,0,0], ['boneknife','iron dagger'] , ['tattered garments'],['recurve bow','iron arrow']],
		"Skeleton Warrior" : ["w","bone","skeleton",2,  4,2,2,2,4,1.2, 8, [0,0,5,0,0,0], ['bone cleaver','sawtooth blade','bonemace'] , ['iron chainmail','studded armor'],['buckler shield']],

		"Living Corpse" : 	  ["z","bone","undead",1,  2,2,1,1,3,1.3, 4, [0,0,0,0,0,0], ['iron longsword','iron axe','iron dagger'] , ['tattered garments',]],
		"Undead Legionaire" : ["z","steel","undead",2,  3,3,2,2,4,1.2, 8, [0,0,0,0,0,0], ['bone cleaver','iron axe','mace'] , ['iron chainmail','rotted chainmail'],['boneshield']],
		"Plaguebearer" :      ["p","darkgreen","undead",2,  4,3,1,2,5,1.3, 8, [0,0,5,0,0,0], ['bone cleaver','flail','mace'] , ['rotted chainmail'],['vomit']],
		"Undead Hound" :  	  ["h","tan","undead",3,  4,3,1,3,4,0.7, 15, [0,0,0,0,0,0], ['blood fangs'] , ['dog hide']],
		"Flayed One" :    	  ["f","red","undead",3,  4,2,1,4,5,0.8, 15, [0,0,0,0,0,0], ['bone claws'] , ['flayed skins']],
		"Undead Hulk" :   	  ["H","bone","undead",4,  7,4,1,3,5,1.7, 24, [0,0,0,0,0,0], ['fist smash'] , ['tattered garments','rotted chainmail','flayed skins']],

		# The Black Eye
		"Cultist" :   	   		["c","purple","man",2,  3,3,3,1,1,1.0, 8, [0,0,0,0,0,0],  ['mace',['hand axe','iron dagger']] , ['tainted robes']],
		"Cult Disciple" :  		["d","blue","man",3,  3,3,3,3,3,1.0, 14, [0,0,0,0,0,0], ['sawtooth blade','flail'] , ['tainted robes'],['dark bolt']],
		"Cult Husk" :  			["h","bone","undead",3,  4,3,2,1,1,1.3, 14, [1,1,1,1,1,0], ['iron bastard sword','bearded greataxe'] , ['tainted robes']],
		"Cult Gravewhisperer" : ["g","orange","man",4,  4,3,3,4,5,1.0, 22, [0,0,0,0,0,0], ['warped staff'] , ['tainted robes'], ['raise skeleton']],
		"Abomination" :    		["A","bone","undead",5,  6,6,1,1,2,1.6, 40, [0,0,0,0,0,0], ['fist smash'] , ['tainted robes']],
		"Cult Destroyer" : 		["D","darkred","man",6,  5,3,3,7,6,1.0, 60, [0,0,0,0,0,0], ['spiked mace'] , ['tainted robes'], ['dark transformation','bloodreave','deathmark']],
		"Cult Prophet" :   		["P","magenta","man",7,  7,3,3,6,7,1.0, 100, [0,0,0,0,0,0], ['warped staff'] , ['tainted robes'], ['raise skeleton','bloodreave','deathmark']],

		# Ironkeep Warsquad
		"Ironkeep Knight" : 	["k","steel","man",5,  6,4,3,4,4,1.3, 40, [0,0,0,0,0,0], [['steel longsword','steel kite shield'],'halberd'], ['steel plate']],
		"Iron Priest" : 		["p","bronze","man",6,  6,4,2,6,4,1.2, 40, [0,0,0,0,0,0], [['spiked mace','iron staff'],'warhammer'], ['iron chainmail']],
		"Ironkeep Confessor" : 	["c","steel","man",7,  5,7,5,5,4,1.1, 40, [0,0,0,0,0,0], ['crusader greatsword'], ['ironkeep robes']],
		"Iron Dreadnought" :	["D","grey","machine",8,  8,8,2,1,1,1.4, 40, [0,0,5,0,0,5], ['foehammers'], ['iron plate']],

		# Dark Elves
		"Dark Wardancer" :  ["s","orange","elf",4,  3,3,5,4,3,0.80, 23, [1,0,0,0,0,0], [['thornknife','thornknife']] , ['ironscale mail']],
		"Dark Huntress" : 	["h","orange","elf",5,  4,4,6,4,3,0.85, 40, [0,0,1,0,0,0], ['thornknife'] , ['ironscale mail','leather armor'], ['blackwood longbow','thornarrow']],
		"Dark Praetorian" : ["p","orange","elf",5,  5,4,5,4,3,0.95, 40, [1,0,0,0,0,0], ['sun spear',['thornblade','gauntlet shield']] , ['blackscale']],
		"Dark Dragoon" :    ["d","orange","elf",6,  6,4,5,4,4,0.60, 60, [1,0,1,1,0,0], ['sunlance','thornblade'] , ['blackscale']],
		"Dark Justicar" :   ["j","orange","elf",6,  5,4,6,4,4,0.85, 60, [1,0,0,0,0,0], ['sun spear',['thornknife','thornknife']] , ['blackscale','thornmail'], ['gauntlet shield']],
		"Dark Archon" :   	["A","orange","elf",7,  6,6,7,5,4,0.90, 100, [1,1,2,1,1,0], ['glaive',['thornblade','thornblade']] , ['blackscale','thornmail'], ['gauntlet shield']],

		# Demons
		"Reaverfiend" :			["r","red","demon",3,  3,4,4,2,2,0.9, 15, [0,1,0,0,0,0], ['bloodletter'] , ['tainted robes','tattered garments']],	
		"Skulltracker" :  		["b","bone","demon",3,  4,3,3,4,5,1.0, 15, [0,0,0,0,0,2], ['iron axe','bone cleaver'] , ['tainted robes','tattered garments'],['boneshield']],
		"Maw Hulk" :			["m","orange","demon",3,  6,2,2,2,4,1.2, 15, [2,0,0,0,0,0], ['flail'] , ['tainted robes','tattered garments']],
		"Chaos Spawn" :			["c","magenta","demon",3,  3,3,4,4,5,0.95, 15, [0,0,0,0,2,0], ['armored limb','horns','vomit'] , ['tainted robes','tattered garments'], ['blink','claws']],
		"Chosen Reaverfiend" : 	["R","darkred","demon",6,  6,6,6,2,5,0.85, 60, [0,3,0,0,0,0], ['skullsplitter','greatflail'] , ['berserker mail']],
		"Chosen Skulltracker" : ["B","bone","demon",6,  6,5,4,4,8,1.0, 60, [0,0,0,0,0,3], ['filthaxe'] , ['tainted robes'],['boneshield']],
		"Chosen Maw Hulk" : 	["M","orange","demon",6,  9,4,3,2,7,1.1, 60, [3,0,0,0,0,0], ['screamflail'] , ['tainted robes']],
		"Chosen Chaos Spawn" :	["C","purple","demon",6,  5,4,5,7,8,0.95, 60, [0,0,0,0,3,0], ['bone claws'] , ['tainted robes'], ['blink']],

		# Oozes
		"Green Ooze" : 	  ["G","green","ooze",3,  5,3,3,3,2,1.3, 15, [0,0,3,0,3,0], ['acid slap'] , ['ooze skin'],['split']],
		"Bone Ooze" : 	  ["B","bone","ooze",3,  5,3,3,3,2,1.4, 15, [0,0,0,0,3,3], ['jelly slap'] , ['bone skin'],['split']],
		"Lesser Ooze" :   ["z","green","ooze",1,  2,2,1,1,2,1.2, 8,  [0,0,1,0,1,1], ['jelly slap'] , ['ooze skin']],

		# Spiders
		"Spiderling" : 		 ["s","tan","spider",1,  1,2,4,1,1,0.7, 4, [0,0,2,0,0,0], ['fangs'] , ['spiderling skin']],
		"Giant Wolfspider" : ["w","brown","spider",3,  4,4,4,4,2,0.8, 14, [0,0,2,0,0,0], ['fangs'] , ['spider hide'],['pounce']],
		"Fateweaver" : 		 ["f","bone","spider",3,  3,3,4,4,2,0.8, 15, [0,0,2,0,0,0], ['fangs'] , ['spider hide'],['pounce']],
		"Armored Crawler" :  ["A","steel","spider",5,  4,4,4,4,2,0.8, 40, [0,0,3,0,0,2], ['fangs'] , ['armored spider plates'],[]],
		"Black Widower" :    ["W","red","spider",5,  4,4,4,4,2,0.8, 40, [0,0,4,0,1,0], ['spider fangs'] , ['massive stinger','spider hide'],[]],
		"Broodmother" :  	 ["B","magenta","spider",5,  6,2,2,5,1,1.5, 40, [0,0,2,0,0,0], ['fangs'] , ['armored spider plates'],[]],
		"Lich Crawler" : 	 ["l","cyan","spider",6,  5,5,3,4,5,0.8, 60, [3,0,2,0,0,0], ['lich fangs'] , ['spider hide'],['pounce']],
		"Tomb Lurker" : 	 ["t","darkred","spider",6,  4,7,6,4,2,0.7, 60, [0,0,3,0,3,0], ['spider fangs'] , ['spider hide'],['massive stinger','pounce']],
		"Spider Queen" : 	 ["Q","purple","spider",7,  7,6,5,4,5,0.9, 100, [0,0,4,0,3,0], ['spider fangs','blood fangs'] , ['armored spider plates'],['massive stinger','pounce']],


		# Large Creatures
		"Ogre" : 		  	 ["O","orange","ogre",1,  5,4,2,1,1,1.4, 15, [0,0,0,0,0,1], ['club','bone club'] , ['ogre hide','scrap plate armor']],
		"Cyclops Brute" : 	 ["C","orange","cyclops",3,  6,6,1,3,4,1.1, 60, [0,0,0,0,0,1], ['spiked club','greatflail','warhammer'] , ['troll hide','leather armor']],
		"Cave Troll" : 	  	 ["T","orange","troll",4,  8,7,2,1,5,1.3, 100, [1,1,0,0,0,1], ['spiked club','stone fists'] , ['cave troll hide','scrap plate armor']],

		# Dragons
		"Fire Dragon" :  ["D","red","fire dragon",10,  12,8,7,6,8,1.1, 500, [0,2,0,0,0,0], ['dragon fangs'] , ['fire dragonscales'], ['dragon tail']],
		"Frost Dragon" : ["D","cyan","frost dragon",10,  14,7,6,4,7,1.2, 500, [2,0,0,0,0,0], ['dragon fangs'] , ['frost dragonscales'], ['frost breath','dragon tail']],
		"Dracolich" :  	 ["D","bone","bone dragon",12,  14,8,6,5,10,1.0, 500, [0,0,4,0,0,0], ['dragon fangs'] , ['bone dragonscales'],['dragon tail','horns']],
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
 						 	    ['Orc Warboy'],
 						 	    ['Orc Warrior', 'Orc Berserker'],
 						 	    ['Orc Nob'],
 						 	    ['Orc Nob','Orc Warlock'],
 						 	    ['Orc Warboss'],
 						 	    ['Orc Nob'],
 			] ),
 		'Undead Horde' : (2, [  ['Living Corpse'], 
 								['Living Corpse'], 
 								['Living Corpse','Living Corpse','Undead Legionaire','Plaguebearer'],
 								['Undead Legionaire', 'Undead Legionaire','Plaguebearer','Flayed One'],
 								['Undead Legionaire', 'Plaguebearer','Flayed One'],
 								['Undead Hound','Flayed One'],
 								['Undead Hulk'],
 			] ),
 		'Uruk Warband' : (-1, [ ['Uruk Warrior'], 
 								['Uruk Bolter'], 
 								['Uruk Warrior','Uruk Warrior','Uruk Pikeman', 'Uruk Pikeman'],
 								['Uruk Bolter','Uruk-hai'],
 								['Uruk Headhunter','Uruk Headhunter','Uruk-hai'],
 								['Uruk Warlord'],
 								['Uruk Bodyguard'],
 			] ),

 		'Dark Elf Guild' :  (-2, [  ['Dark Wardancer','Dark Wardancer','Dark Praetorian'], 
	 								['Dark Wardancer','Dark Huntress'], 
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

 		'Demon Horde' : (0, [   ['Reaverfiend','Chaos Spawn','Skulltracker','Maw Hulk'], 
 								['Reaverfiend','Chaos Spawn','Skulltracker','Maw Hulk'], 
 								['Reaverfiend','Chaos Spawn','Skulltracker','Maw Hulk'],
 								['Reaverfiend','Chaos Spawn','Skulltracker','Maw Hulk'], 
 								['Skulltracker','Maw Hulk','Chaos Spawn','Reaverfiend'],
 								['Chaos Spawn','Reaverfiend','Reaverfiend','Reaverfiend'],
 								[],
 								['Chosen Reaverfiend','Chosen Skulltracker','Chosen Maw Hulk','Chosen Chaos Spawn'],
 								[],
 								['Chosen Maw Hulk','Chosen Reaverfiend','Chosen Skulltracker','Chosen Chaos Spawn'],
 			] ),

 		'Jelly Band' :  (-2, [  ['Green Ooze', 'Bone Ooze'], 
	 							['Green Ooze', 'Bone Ooze'], 
	 							[],
	 							[],
	 							[],
	 							[],
	 							[],
	 							[],
	 							[],
	 							[],
	 							[]
	 		] ),

 		'Ironkeep Warsquad' :  (1, [    ['Ironkeep Knight'], 
	 									['Ironkeep Knight'], 
	 									['Iron Priest'],
	 									[],
	 									['Ironkeep Confessor','Iron Dreadnought'],
	 									[],
	 									['Ironkeep Knight'],
	 									[],
	 									[],
	 									[],
	 									[]
	 		] ),

 		'Spider Cave' :  (+3, [ ['Spiderling'], 
	 							['Spiderling'], 
	 							['Spiderling'],
	 							['Spiderling'],
	 							['Spiderling','Spiderling','Giant Wolfspider'],
	 							[],
	 							['Giant Wolfspider'],
	 							[],
	 							['Fateweaver','Giant Wolfspider','Fateweaver'],
	 							['Armored Crawler','Broomother','Black Widower'],
	 							[],
	 							['Armored Crawler','Black Widower','Broodmother'],
	 							['Lich Crawler','Tomb Lurker'],
	 							[],
	 							['Spider Queen']
	 		] ),

 		'Wandering Monster' : (0, [	['Ogre','Green Ooze','Giant Wolfspider','Cyclops Brute','Cave Troll']	
 			] ),

 		'Dragon Nest' : (0, [	['Fire Dragon','Frost Dragon','Bone Dragon']	
 			] ),


 	}

 	dicto = { 	   1 : ['Orc Band','Undead Horde','Wandering Monster','Wolf Den','Kobold Party','Spider Cave'
 						],
 				   2 : [
 				   		],
 				   3 : ['Black Eye Cult','Demon Horde'
 				   		],
 				   4 : ['Uruk Warband','Dark Elf Guild','Black Eye Cult','Jelly Band'
 				   		],
 				   5 : [
 				   		'Wolf Den','Kobold Party'],
 				   6 : [
 				   		],
 				   7 : ['Ironkeep Warsquad'
 				   		],
 				   8 : [
 				   		],
 				   9 : [
 				   		],
 				   10 : ['Dragon Nest'
 				   		],
 				   11 : [
 				   		],
 				   }

 	# dicto = { 	   1 : ['Dragon Nest'],
 	# 			   }

