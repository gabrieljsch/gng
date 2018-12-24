from random import randint, shuffle

def d(range):
	return randint(1,range)

class Monsters():
	# self,      char, etype,  behavior type, tier,    con, st, dex, int, cha, mspeed,regen,  xp,  resistances(fr,fi,po,ac,sh,ex), pot_weapons, pot_armor, other_items

	array = {

		# Animals
		# Wolves
		"Wolf" : 	  	   	  ["w","steel","beast",'w',1,  2,2,2,2,1,0.75,12, 4, [1,0,0,0,0,0], ['fangs'] , ['wolf pelt']],
		"Direwolf" : 	   	  ["W","steel","beast",'w',2,  4,3,4,2,1,0.85,12, 8, [1,0,0,0,0,0], ['fangs'] , ['wolf pelt','direwolf pelt']],
		"Direwolf Cannibal" : ["c","red","beast",'w',2,  3,4,4,2,1,0.75,10, 8, [1,0,0,0,0,0], ['blood fangs'] , ['wolf pelt'],['furious charge']],
		"Direwolf Alpha" : 	  ["A","darkred","beast",'w',3,  5,5,5,2,1,0.8,12, 15, [1,0,0,0,0,0], ['demon fangs','blood fangs'] , ['direwolf pelt'],['furious charge']],

		# Kobolds
		"Kobold" : 		  ["k","orange","kobold",'w',1,  2,2,2,1,3,1.0,15, 4, [0,1,0,1,1,0], ['spear',"iron shortsword",['hand axe','buckler shield']] , ['leather armor','troll hide']],
		"Kobold Archer" : ["a","orange","kobold",'ar',1,  2,2,2,1,3,1.0,15, 4, [0,1,0,1,1,0], ['iron dagger','iron shortsword'] , ['leather armor','troll hide'],['crude shortbow','iron arrow']],
		"Kobold Mage" :   ["m","magenta","kobold",'ma',2,  2,3,3,4,3,1.0,15, 8, [0,1,0,1,1,0], [['iron dagger','Tome of Fire']] , ['leather armor','studded armor'],['flame tongue']],
		"Kobold Sneak" :  ["s","darkgreen","kobold",'ro',2,  3,3,3,3,3,0.9,15, 8, [0,1,0,1,1,0], [['iron dagger','iron dagger']] , ['leather armor','studded armor']],
		"Greater Kobold": ["K","darkred","kobold",'w',3,  4,4,4,3,4,1.0,15, 15, [0,1,0,1,1,1], ['halberd','iron battleaxe',['steel axe','wooden broadshield']] , ['studded armor','drakescale']],

		# Goblins
		"Goblin" : 		   	   ["g","yellow","goblin",'w',1,  2,2,3,1,1,0.9,8, 4, [0,0,0,0,0,0], ['stabba','goblin spear','club','bone club'] , ['wolf pelt','bear hide']],
		"Goblin Archer" :      ["a","yellow","goblin",'ar',1,  2,1,4,1,1,0.85,8, 4, [0,0,0,0,0,0], ['stabba'] , ['wolf pelt','bear hide'], ['goblin bow','iron arrow']],
		"Goblin Skirmisher":   ["g","yellow","goblin",'w',1,  3,2,3,1,1,0.85,7, 6, [0,0,0,0,0,0], ['slica','choppa','bone club'] , ['bear hide'], ['buckler shield'], ['iron javelin']],
		"Witch Goblin" :       ["w","magenta","goblin",'ma',2,  3,3,3,3,3,0.9,6, 8, [0,0,1,0,0,0], ['bone club'] , ['troll hide'], ['poison breath']],
		"Goblin Nob" : 	       ["g","orange","goblin",'w',2,  4,3,2,1,2,0.95,8, 8, [0,0,0,0,0,0], ['smasha','choppa'] , ['troll hide','spider hide']],
		"Goblin Spiderrider" : ["g","yellow","goblin",'w',2,  3,2,3,1,1,0.85,8, 15, [0,0,0,0,0,0], ['goblin spear','slica'], ['bear hide','ogre hide'], ['buckler shield','Giant Wolfspider']],
		"Goblin Chief" :   	   ["g","purple","goblin",'w',3,  5,4,4,2,3,0.9,7, 15, [0,0,0,0,0,0], ['big choppa','big slica','skull smasha'] , ['berserker mail','leather armor'], ['trollhide shield']],

		"Hobgoblin Skirmisher" : ["h","yellow","goblin",'w',4,  5,4,3,2,3,1.0,12, 40, [0,0,0,0,0,0], [['bearded axe','wooden broadshield'],['falchion','wooden broadshield'],'pike'] , ['iron chainmail','ironscale mail','studded armor'],['furious charge']],
		"Hobgoblin Defender" : 	 ["d","yellow","goblin",'w',4,  5,4,3,2,3,1.0,12, 40, [0,0,0,0,0,0], ['bearded axe','falchion'], ['iron chainmail','ironscale mail','studded armor'],['tower shield']],
		"Hobgoblin Bolter" :     ["b","yellow","goblin",'ar',4,  4,4,4,2,3,0.9,12, 40, [0,0,0,0,0,0], ['crossbow'] , ['iron chainmail','ironscale mail','studded armor'],['crossbow','iron bolt']],
		"Hobgoblin Earthmage" :  ["h","magenta","goblin",'ma',6,  6,4,4,7,5,1.0,11, 60, [0,0,0,0,0,0], ['falchion','ash staff'] , ['bearhide robes'],['Tome of Earth']],
		"Hobgoblin General" :    ["g","gold","goblin",'w',7,  7,6,6,7,5,1.0,11, 100, [0,0,0,0,0,0], ['bearded greataxe','witchhunter blade'], ['godforge chainmail','steel plate'],['tower shield']],

		# Orcs
		"Orc Warboy" : 	   ["o","green","orc",'w',2,  3,4,3,2,2,1.0,13, 6, [0,0,0,0,0,0], ['slica','choppa','smasha'] , ['bear hide', 'troll hide']],
		"Orc Archer" :     ["a","green","orc",'ar',2,  3,3,4,2,2,1.0,13, 6, [0,0,0,0,0,0], ['choppa', 'slica'] , ['bear hide', 'troll hide'], ['crude shortbow','iron arrow']],
		"Orc Warrior" :    ["o","darkgreen","orc",'w',2,  4,4,3,2,3,1.1,13, 9, [0,0,0,0,0,0], ['slica','smasha','choppa'] , ['troll hide','leather armor'], ['trollhide shield']],
		"Orc Berserker" :  ["b","red","orc",'w',3,  4,5,4,2,3,0.8,8, 15, [1,1,1,0,1,0], ['iron greatsword',['choppa','slica']] , ['berserker mail','iron chainmail'], ['headbutt','furious charge']],
		"Orc Brute" : 	   ["B","darkgreen","orc",'w',4,  5,5,3,2,4,1.2,13, 40, [1,0,0,0,0,1], ['big choppa','big slica','skull smasha','ice choppa'] , ['berserker mail','iron chainmail','scrap plate armor'], ['headbutt','green blood']],
		"Orc Warlock" :    ["W","magenta","orc",'mb',4,  4,3,3,4,4,1.1,8, 40, [0,0,3,0,0,0], ['toxic slica','oak staff'] , ['wyvernscale','studded armor'], ['poison breath','raise skeleton','green blood']],
		"Orc Warboss" :    ["O","darkred","orc",'w',5,  6,6,4,6,5,1.2,13, 50, [1,1,1,1,1,1], ['boss choppa','ice choppa',['black ballista','big slica']] , ['berserker mail','scrap plate armor','steel chainmail'], ['headbutt','furious charge','iron bolt','green blood']],

		"Warg" : 	   	   ["w","brown","beast",'w',2,  3,4,3,2,1,0.8,10, 8, [2,0,0,0,0,0], ['fangs'] , ['warg pelt']],
		"Feral Warg" : 	   ["w","darkbrown","beast",'w',3,  4,5,4,2,1,0.8,8, 15, [2,0,0,0,0,0], ['fangs'] , ['warg pelt'],['furious charge']],
		"Orc Warg-rider" : ["o","green","orc",'w',2,  3,4,3,2,2,1.1,13, 15, [0,0,0,0,0,0], ['slica','choppa','smasha'] , ['bear hide', 'troll hide'], ['Warg']],
		"Brute Warg-rider":["B","darkgreen","orc",'w',4,  5,5,3,2,4,1.2,13, 40, [0,0,0,0,0,1], ['big choppa','big slica','skull smasha','ice choppa'] , ['berserker mail','scrap plate armor'], ['Feral Warg','green blood']],

		"Orc Dethbrute" :  ["B","orange","orc",'w',5,  6,5,2,2,4,1.4,15, 50, [1,1,0,0,0,3], [['krogjaw choppa','trollhide shield'],['dethklaw','trollhide shield'],['krogtooth choppa','krogtooth choppa'],] , ['Orcish dreadplate'], ['headbutt','green blood']],

		"Ro'khan, Prophet of Krog" :  ["R","red","orc",'w',8,  7,7,4,6,8,1.2,13, 200, [1,1,0,0,0,1], ["Krog's Maw"] , ['Orcish dreadplate'], ['trollhide shield','furious charge','headbutt','green blood']],
		"Waa'zhok, Conduit of Krog" : ["W","purple","orc",'ma',6,  6,5,3,8,8,0.9,6, 80, [0,0,0,0,4,0], ['toxic slica','oak staff'] , ['necromancer robes'], ['chain lightning','raise skeleton','green blood']],

		# Uruks
		"Uruk Warrior" :   ["u","bronze","uruk",'w',3,  4,4,3,2,4,1.0,17, 15, [0,0,0,0,0,0], ['hooked longsword','spiked axe','spiked mace'] , ['blackiron plate'], ['blackiron shield']],
		"Uruk Pikeman" :   ["u","bronze","uruk",'w',3,  4,4,3,2,4,1.0,17, 15, [0,0,0,0,0,0], ['uruk-hai pike'] , ['blackiron plate']],
		"Uruk Bolter" :    ["b","bronze","uruk",'ar',3,  4,3,4,2,4,0.9,17, 15, [0,0,0,0,0,0], ['hooked shortsword'] , ['blackiron plate'], ['uruk crossbow','iron bolt']],
		"Uruk Headhunter" :["h","steel","uruk",'ar',4,  4,4,4,2,4,1.0,17, 22, [0,0,0,0,0,0], ['hooked broadsword',['spiked axe','spiked axe']] , ['blackiron plate'], ['barbed javelin']],
		"Uruk-hai" : 	   ["u","red","uruk",'w',4,  5,4,3,2,4,0.8,10, 22, [2,0,2,0,2,0], ['hooked broadsword'] , ['berserker mail'], ['headbutt','furious charge']],
		"Uruk Bodyguard" : ["u","purple","uruk",'w',5,  6,5,3,2,6,1.2,17, 40, [0,0,0,0,0,0], ['uruk-hai pike', ['hooked broadsword','blackiron shield']], ['blackiron plate'], ['shield hit']],
		"Uruk Warlord" :   ["U","darkred","uruk",'w',6,  7,6,4,2,6,1.0,17, 60, [0,0,0,0,0,0], ['hooked broadsword',['uruk crossbow','hooked longsword']] , ['blackiron plate'], ['blackiron shield','furious charge','headbutt','steel bolt']],

		# Undead
		"Skeleton" : 	  	  ["s","bone","skeleton",'w',1,  2,2,1,1,2,1.1,50, 4, [0,0,5,0,0,0], ['iron longsword','iron axe','iron shortsword'] , ['tattered garments']],
		"Skeleton Archer" :   ["a","bone","skeleton",'ar',2,  3,2,3,2,4,1.1,50, 8, [0,0,5,0,0,0], ['boneknife','iron dagger'] , ['tattered garments'],['recurve bow','iron arrow']],
		"Skeleton Warrior" :  ["w","bone","skeleton",'w',2,  4,2,2,2,4,1.2,50, 8, [0,0,5,0,0,0], ['bone cleaver','sawtooth blade','bonemace'] , ['iron chainmail','studded armor'],['buckler shield']],

		"Living Corpse" : 	   ["z","bone","undead",'w',1,  2,2,1,1,1,1.3,20, 4, [0,0,0,0,0,0], ['iron longsword','iron axe','iron dagger','mace'] , ['tattered garments',]],
		"Undead Legionnaire" : ["z","steel","undead",'w',2,  3,3,2,2,1,1.2,14, 8, [0,0,0,0,0,0], ['bone cleaver','iron axe','mace'] , ['iron chainmail','rotted chainmail'],['boneshield']],
		"Plaguebearer" :       ["p","darkgreen","undead",'w',2,  4,3,1,2,2,1.2,12, 8, [0,0,5,0,0,0], ['bone cleaver','flail'] , ['rotted chainmail'],['vomit','filth explosion']],
		"Undead Hound" :  	   ["h","tan","undead",'w',3,  4,3,2,3,4,0.6,14, 15, [0,0,0,0,0,0], ['blood fangs'] , ['dog hide'],['furious charge','pounce']],
		"Flayed One" :    	   ["f","red","undead",'w',3,  4,4,3,1,2,0.7,6, 15, [0,0,0,0,0,0], ['bone claws'] , ['flayed skins']],
		"Undead Immortal" :    ["i","steel","undead",'w',4,  5,4,3,4,5,1.0,8, 24, [0,0,0,0,0,0], [['steel shortsword','steel shortsword'],['steel longsword','bronze aegis'],['spear','bronze aegis']] , ['steel chainmail']],
		"Rotting Hulk" :       ["H","darkgreen","undead",'w',4,  7,4,1,3,5,1.7,12, 24, [0,0,0,0,0,0], ['fist smash'] , ['tattered garments','rotted chainmail','flayed skins'],['vomit','filth explosion']],

		"Lich Eternal" :	   ["l","cyan","undead",'w',7,  6,6,3,10,4,1.1,8, 100, [5,0,0,0,0,0], [['khopesh', 'steel kiteshield'],'glaive'] , ['godforge chainmail']],
		"Lich Bonesinger" :	   ["l","magenta","undead",'ma',7,  5,5,4,10,8,1.0,10, 100, [5,0,0,0,0,0], ['glass dagger'] , ['godforge chainmail']],

		# The Black Eye
		"Cultist" :   	   		["c","purple","man",'w',2,  3,3,3,1,1,1.0,14, 8, [0,0,0,0,0,0],  ['mace',['hand axe','iron dagger']] , ['tainted robes']],
		"Cult Disciple" :  		["d","blue","man",'mb',3,  3,3,3,3,2,1.0,14, 14, [0,0,0,0,0,0], ['sawtooth blade',['Tome of the Black Eye','iron dagger']] , ['tainted robes'],['dark bolt']],
		"Cult Husk" :  			["h","bone","undead",'w',3,  4,3,2,1,1,1.3,20, 14, [1,1,1,1,1,0], ['iron bastard sword','bearded greataxe'] , ['tainted robes']],
		"Cult Gravewhisperer" : ["g","orange","man",'ma',4,  4,3,3,4,5,1.0,14, 22, [0,0,0,0,0,0], ['warped staff'] , ['tainted robes'], ['raise skeleton']],
		"Abomination" :    		["A","bone","abomination",'w',6,  7,7,1,1,2,1.6,10, 60, [0,0,0,0,0,0], ['fist smash'] , ['tainted robes']],
		"Cult Destroyer" : 		["d","darkred","man",'ma',6,  5,3,3,7,5,1.0,14, 60, [0,0,0,0,0,0], ['spiked mace'] , ['tainted robes'], ['dark transformation','bloodreave','deathmark']],
		"Cult Prophet" :   		["P","magenta","man",'ma',7,  7,3,3,6,6,1.0,8, 100, [0,0,0,0,0,0], ['warped staff'] , ['tainted robes'], ['raise skeleton','bloodreave','deathmark']],

		# Ironkeep Warsquad
		"Ironkeep Knight" : 	["k","steel","man",'w',5,  6,4,3,4,4,1.3,14, 40, [0,0,0,0,0,0], [['steel longsword','steel kiteshield'],'halberd','steel battleaxe'], ['steel plate']],
		"Iron Priest" : 		["p","bronze","man",'ms',6,  6,4,2,6,4,1.2,9, 60, [0,0,0,0,0,0], [['Tome of Iron','iron staff'],'warhammer'], ['iron chainmail'],['iron blessing'],['evening rites']],
		"Ironkeep Confessor" : 	["c","steel","man",'w',7,  5,7,5,5,4,1.1,14, 100, [0,0,0,0,0,0], ['crusader greatsword'], ['ironkeep robes'],['evening rites']],
		"Iron Dreadnought" :	["D","grey","machine",'w',8,  8,8,2,1,1,1.4,50, 200, [0,0,5,0,0,5], ['foehammers'], ['iron plate']],

		# Dreads
		"Repair Bot" : 		["r","red",  "machine",'re',2,  3,1,3,5,1,1.0,50, 40, [0,0,3,0,0,0], ['bardiche'], ['bronze mail']],
		"Assault Unit" : 	["f","steel","machine",'w',5,  5,5,1,4,4,1.5,50, 40, [1,0,3,0,0,2], [['scimitar','bronze aegis'],['blastmace','bronze aegis'],'shockglaive'], ['bronze mail']],
		"Harrier Unit" : 	["h","steel","machine",'ar',5,  4,5,2,4,4,1.4,50, 40, [1,0,3,0,0,2], ['falchion'], ['bronze mail'],['machine crossbow','steel bolt']],
		"Mageslayer Unit" : ["f","magenta","machine",'w',6,  6,6,1,4,6,1.1,50, 40, [1,0,3,0,0,2], ['voidscythe'], ['warpbeast hide']],

		# Chronids
		"Drone" : 		   ["c","bone","chronid",'w',2,  2,3,4,1,1,0.9,6, 6, [0,0,0,0,0,0], ['claws'] , ['chronid shell']],
		"Ripper Drone" :   ["r","yellow","chronid",'w',3,  2,3,4,1,1,0.9,7, 14, [0,0,0,0,0,0], ['claws'] , ['chronid shell'],['claws','furious charge']],
		"Screamer Drone" : ["s","yellow","chronid",'w',3,  2,3,4,3,2,0.9,7, 14, [0,0,0,0,0,0], ['claws'] , ['chronid shell'],['bioscream']],
		"Hive Warrior" :   ["W","orange","chronid",'w',4,  5,5,3,2,1,1.0,7, 25, [0,0,0,0,0,0], ['bioscream','reaper talon','plated limb','bonesword'] , ['chronid shell'],['claws']],
		"Broodmage" :  	   ["b","purple","chronid",'ma',5,  4,4,4,8,5,1.0,6, 40, [0,0,0,0,0,0], ['bone claws'] , ['chronid shell'],['armored limb']],
		"Behemoth" :  	   ["B","bone","chronid",'w',6,  8,5,1,2,1,1.8,8, 60, [0,0,0,0,0,0], ['fist smash'] , ['chronid plate'],['claws','plated limb']],
		"Hivelord" : 	   ["H","red","chronid",'w',7,  7,7,5,8,4,1.0,8, 100, [0,0,0,0,0,0], [['reaper talon','reaper talon'],['bonesword','bonesword']] , ['chronid plate'],['plated limb','bone claws']],

		"the Worldeater" : ["W","bone","chronid",'w',10,  9,8,2,10,5,1.5,7, 700, [0,0,0,0,0,0], [['bonesword','bonesword','bonesword','Skullrazor']] , ['chronid plate'],[]],

		# Dark Elves
		"Wardancer" :  		["w","purple","elf",'w',4,  3,3,5,4,3,0.80,10, 23, [1,0,0,0,0,0], [['thornknife','thornknife']] , ['ironscale mail','leather armor']],
		"Dark Huntress" : 	["h","purple","elf",'ar',5,  4,4,6,4,3,0.85,10, 40, [0,0,1,0,0,0], ['thornknife'] , ['ironscale mail','leather armor'], ['blackwood longbow','thornarrow']],
		"Dark Praetorian" : ["p","purple","elf",'w',5,  5,4,5,4,3,0.95,10, 40, [1,0,0,0,0,0], ['sunspear',['thornblade','gauntlet shield']] , ['blackscale']],
		"Dragoon" :    		["d","magenta","elf",'w',6,  5,4,5,4,4,0.85,10, 60, [1,0,1,1,0,0], ['sunlance','thornblade'] , ['blackscale'],['Tortured Warsteed']],
		"Dark Justicar" :   ["j","magenta","elf",'w',6,  5,4,6,4,4,0.85,6, 60, [1,0,0,0,0,0], ['sunspear',['thornknife','thornknife']] , ['blackscale','thornmail'], ['gauntlet shield','furious charge']],
		"Archon" :   		["A","darkred","elf",'w',7,  6,6,7,5,4,0.90,7, 100, [1,1,2,1,1,0], ['glaive',['thornblade','thornblade']] , ['blackscale','thornmail'], ['gauntlet shield']],

		# Demons
		# Tier 5
		"Reaverfiend" :	["r","red","demon",'w',3,  3,4,4,2,2,0.9,11, 15, [0,1,0,0,0,0], ['bloodletter'] , ['tainted robes','tattered garments']],
		"Skulltracker" :["s","bone","demon",'w',3,  4,3,3,4,5,1.0,14, 15, [0,0,0,0,0,2], ['iron axe','bone cleaver'] , ['tainted robes','tattered garments'],['boneshield']],
		"Bloodhulk" :	["B","orange","demon",'w',3,  6,2,2,2,4,1.2,9, 15, [2,0,0,0,0,0], ['flail'] , ['tainted robes','tattered garments']],
		"Chaos Spawn" :	["c","magenta","demon",'mb',3,  3,3,4,4,5,0.95,5, 15, [0,0,0,0,2,0], ['armored limb','horns','vomit'] , ['tainted robes','tattered garments'], ['blink','claws']],
		# Tier 4
		"Frozen Devil" : ["f","cyan","demon",'w',4,  4,4,4,4,4,1.1,14, 24, [3,0,0,0,0,0], ['flail'] , ['tainted robes','tattered garments']],
		# Tier 3
		# Tier 2
		"Hellfiend" :  ["h","red","demon",'w',6,  6,6,6,2,5,0.85,11, 60, [0,3,0,0,0,0], ['skullsplitter','greatflail'] , ['berserker mail'],['tail smash','horns']],
		"Foul One" :   ["f","darkgreen","demon",'w',6,  6,5,4,4,8,1.2,12, 60, [0,0,4,4,0,0], ['filthaxe'] , ['tainted robes'],['boneshield']],
		"Gorehulk" :   ["G","darkred","demon",'w',6,  9,4,3,2,7,1.3,8, 60, [3,0,0,0,0,0], ['screamflail'] , ['tainted robes']],
		"Changeling" : ["c","purple","demon",'mb',6,  5,4,5,7,8,0.95,5, 60, [0,0,0,0,3,0], ['bone claws'] , ['tainted robes'], ['blink']],
		# Tier 1

		# Oozes
		"Lesser Ooze" :   ["z","green","ooze",'w',1,  2,2,1,1,2,1.2,7, 8,  [0,0,1,0,1,1], ['jelly slap'] , ['ooze skin']],
		"Green Ooze" : 	  ["Z","green","ooze",'w',3,  5,3,3,3,2,1.3,10, 15, [0,0,3,0,3,0], ['acid slap'] , ['ooze skin'],['split']],
		"Orange Ooze" :   ["Z","orange","ooze",'w',3,  3,5,3,3,2,1.2,8, 15, [0,0,0,0,3,0], ['jelly slap'] , ['ooze skin'],['split']],
		"Clear Ooze" :    ["Z","steel","ooze",'w',3,  4,4,4,2,1,1.3,5, 15, [0,0,0,0,3,3], ['jelly slap'] , ['ooze skin'],['split']],
		"Death Ooze" : 	  ["Z","darkred","ooze",'w',4,  6,4,4,4,3,1.4,8, 25, [0,0,1,0,3,3], ['jelly slap'] , ['bone skin'],['split']],

		# Spiders
		"Spiderling" : 		 ["s","tan","spider",'w',1,  1,1,4,1,1,0.7,8, 4, [0,0,2,0,0,0], ['fangs'] , ['spiderling skin']],
		"Giant Wolfspider" : ["w","brown","spider",'w',3,  4,4,4,4,2,0.8,8, 14, [0,0,2,0,0,0], ['fangs'] , ['spider hide'],['pounce']],
		"Fateweaver" : 		 ["f","bone","spider",'aa',3,  3,3,4,4,2,0.8,7, 15, [0,0,2,0,0,0], ['fangs'] , ['spider hide'],['web shot']],
		"Armored Crawler" :  ["A","steel","spider",'w',5,  6,4,4,5,5,1.0,9, 40, [0,0,3,0,0,2], ['fangs'] , ['armored spider plates'],[]],
		"Black Widower" :    ["w","red","spider",'ro',5,  5,5,5,5,3,0.8,7, 40, [0,0,5,0,1,0], ['spider fangs'] , ['massive stinger','spider hide'],[]],
		"Broodmother" :  	 ["B","magenta","spider",'w',5,  7,2,2,5,1,1.5,9, 40, [0,0,2,0,0,0], ['fangs'] , ['armored spider plates'],[]],
		"Lich Crawler" : 	 ["l","cyan","spider",'w',6,  6,6,5,4,5,0.8,9, 60, [3,0,2,0,0,0], ['lich fangs'] , ['spider hide'],['pounce']],
		"Tomblurker Spider" :["t","darkred","spider",'ro',6,  5,7,6,4,2,0.7,8, 60, [0,0,3,0,3,0], ['spider fangs'] , ['spider hide'],['massive stinger','pounce']],
		"Spider Queen" : 	 ["Q","purple","spider",'w',7,  7,6,5,4,5,0.9,8, 100, [0,0,4,0,3,0], ['spider fangs','blood fangs'] , ['armored spider plates'],['massive stinger','pounce']],


		# Ogres
		"Ogre" : 		  	 ["O","orange","ogre",'w',2,  5,4,2,1,1,1.4,8, 15, [0,0,0,0,0,1], ['club','bone club'] , ['ogre hide','scrap plate armor']],
		"Ogre Berserker" : 	 ["O","red","ogre",'w',5,  6,7,3,1,1,1.2,7, 15, [2,2,5,2,0,1], ['spiked club','bone club'] , ['berserker mail','ironscale mail'],['furious charge']],

		# Cyclops
		"Cyclops Brute" : 	 ["C","bronze","cyclops",'w',3,  6,6,1,3,4,1.2,22, 60, [0,0,0,0,0,1], ['spiked club','greatflail','warhammer'] , ['troll hide','leather armor']],
		"Cyclops Hurler" : 	 ["C","blue","cyclops",'ar',6,  7,6,3,5,5,1.1,20, 60, [0,0,0,0,0,1], ['spiked club'] , ['studded armor','leather armor'],['large boulder']],

		# Troll
		"Cave Troll" : 	  	 ["T","bone","troll",'w',6,  8,7,2,1,5,1.3,18, 100, [1,1,0,0,0,1], ['spiked club','stone fists'] , ['cave troll hide','scrap plate armor']],
		"Wartroll" : 	  	 ["T","darkred","troll",'w',8,  9,9,3,1,5,1.5,16, 100, [1,1,0,0,0,1], ['spiked club','trollhammer'] , ['iron plate','scrap plate armor']],

		"Dane, Son of Erick" : ["D","yellow","troll",'w',8,  8,7,2,10,5,1.3,18, 300, [1,1,0,0,0,1], ["Mjölnir"] , ['steel plate'],['Flame Dragon']],

		# Dragons
		"Flame Dragon" : ["D","red","dragon",'w',10,  12,8,7,6,8,1.1,11, 500, [0,2,0,0,0,0], ['dragon fangs'] , ['fire dragonscales'], ['dragon tail']],
		"Frost Dragon" : ["D","cyan","dragon",'w',10,  14,7,6,4,7,1.2,14, 500, [2,0,0,0,0,0], ['dragon fangs'] , ['frost dragonscales'], ['frost breath','dragon tail']],
		"Dracolich" :  	 ["D","bone","dragon",'w',12,  14,8,6,5,10,1.0,25, 500, [0,0,4,0,0,0], ['dragon fangs'] , ['bone dragonscales'],['dragon tail','horns']],

		# the Four Horsemen
		"War" :  	   ["W","red","spirit",'w',7,  6,8,4,1,5,1.2,10, 100, [1,1,0,0,0,1], ["warscythe"] , ['steel chainmail'],['Tortured Warsteed']],
		"Famine" :     ["F","blue","spirit",'w',7,  6,8,4,1,5,1.2,8, 100, [1,1,0,0,0,1], ["warscythe"] , ['steel chainmail'],['Tortured Warsteed']],
		"Pestilence" : ["P","green","spirit",'w',7,  6,8,4,1,5,1.2,4, 100, [1,1,0,0,0,1], ["warscythe"] , ['steel chainmail'],['Tortured Warsteed']],
		"Death" :  	   ["D","purple","spirit",'w',7,  6,8,4,1,5,1.2,15, 100, [1,1,0,0,0,1], ["warscythe"] , ['steel chainmail'],['Tortured Warsteed']],

		# Mounts
		"Wild Horse" : 		   ["h","brown","beast",'c',3,  4,2,4,1,8,0.7,9, 15, [0,0,0,0,0,0], ['hooves'] , ['horse hide']],
		"Tortured Warsteed" :  ["h","darkred","beast",'w',3,  3,3,3,1,8,0.7,7, 15, [2,2,0,0,0,0], ['hooves'] , ['horse hide']],


		}

	# Unique, named enemies
	uniques = ["Dane, Son of Erick", "Ro'khan, Prophet of Krog", "Waa'zhok, Conduit of Krog" ,"the Worldeater"]

	# Not affected by bleeds or vampiric
	dont_bleed = ["skeleton","machine","spirit","ooze"]

	# Bonus damage from silver weapons
	silver_vulnerable = ["undead","skeleton","abomination","vampire","werewolf"]

	# Bonus damage from holy weapons
	holy_vulnerable = ["demon","undead","skeleton","abomination"]




class Bands:  # Tier Bonus :   formations

	formations = {

		'Wolf Den' :      (2, [ ['Wolf'],
								['Wolf'],
								['Wolf','Direwolf Cannibal'],
								['Direwolf','Direwolf Cannibal'],
								['Direwolf Cannibal'],
								['Direwolf Alpha'],
			]),
		'Kobold Party' : (2, [  ['Kobold'],
								['Kobold Archer'],
								['Kobold','Kobold','Kobold Mage','Greater Kobold'],
								[],
								['Kobold Mage','Kobold Sneak'],
								['Greater Kobold'],
			]),
		'Orc Band' :      (1, [ ["Goblin",'Goblin Archer','Goblin Nob','Goblin Spiderrider', 'Goblin Chief'],
								['Goblin Archer','Goblin Skirmisher','Witch Goblin','Orc Warboy','Orc Brute'],
								['Goblin', 'Orc Archer', 'Orc Warboy', 'Orc Warrior', 'Orc Brute'],
								['Orc Warboy'],
								['Orc Warrior', 'Orc Berserker'],
								['Orc Brute'],
								['Orc Brute','Orc Warlock'],
								['Orc Warboy'],
								['Orc Warboss'],
								['Orc Warboy'],
								['Orc Brute'],
			]),
		'Hobgoblin Squad' :(-2, [ ['Hobgoblin Skirmisher','Hobgoblin Defender'],
								 ['Hobgoblin Defender'],
								 ['Hobgoblin Skirmisher','Hobgoblin Defender'],
								 ['Hobgoblin Bolter'],
								 [],
								 ['Hobgoblin Earthmage'],
								 [],
								 ['Hobgoblin General'],
								 [],
								 [],
								 [],
			]),
		'Orc Hunting Party' :(-1,[ ['Feral Warg'],
								   ['Feral Warg'],
								   ['Orc Warg-rider'],
								   ['Orc Warg-rider'],
								   ['Orc Warg-rider'],
								   ['Brute Warg-rider'],
								   ['Feral Warg'],
								   ['Brute Warg-rider'],
								   ['Brute warg-rider'],
			]),
		'Undead Horde' : (2, [  ['Living Corpse'],
								['Living Corpse'],
								['Living Corpse','Living Corpse','Undead Legionnaire','Plaguebearer'],
								['Undead Legionnaire', 'Undead Legionnaire','Plaguebearer','Flayed One'],
								['Undead Legionnaire', 'Plaguebearer','Flayed One'],
								['Living Corpse'],
								['Undead Hound','Flayed One'],
								['Living Corpse'],
								['Rotting Hulk'],
			]),
		'Uruk Warband' : (-1, [ ['Uruk Warrior'],
								['Uruk Bolter'],
								['Uruk Warrior','Uruk Pikeman'],
								['Uruk Bolter','Uruk-hai'],
								['Uruk Headhunter','Uruk Headhunter','Uruk-hai'],
								['Uruk Warrior'],
								['Uruk Warlord'],
								['Uruk Bodyguard'],
								['Uruk Bodyguard'],
			]),

		'Dark Elf Guild' :  (-2, [  ['Wardancer','Wardancer','Dark Praetorian'],
									['Wardancer','Dark Huntress'],
									['Dark Praetorian'],
									[],
									['Dragoon','Dark Justicar'],
									['Dark Praetorian'],
									['Dark Justicar','Dragoon'],
									['Dark Praetorian'],
									[],
									['Archon']
		]),

		'Black Eye Cult' :  (0 + 4, [   ['Cultist', 'Cultist','Cultist','Cult Disciple'],
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
			]),

		'Demon Horde' : (0, [   ['Reaverfiend','Chaos Spawn','Skulltracker','Bloodhulk'],
								['Reaverfiend','Chaos Spawn','Skulltracker','Bloodhulk'],
								['Reaverfiend','Chaos Spawn','Skulltracker','Bloodhulk'],
								['Reaverfiend','Chaos Spawn','Skulltracker','Bloodhulk'],
								['Reaverfiend','Chaos Spawn','Skulltracker','Bloodhulk'],
								['Reaverfiend','Chaos Spawn','Skulltracker','Bloodhulk'],
								[],
								[],
								[],
								[],
			]),

		'Jelly Band' :  (-2, [  ['Green Ooze','Clear Ooze'],
								['Orange Ooze','Green Ooze'],
								['Clear Ooze','Orange Ooze'],
								[],
								['Death Ooze'],
								[],
								['Death Ooze'],
								[],
								[],
								[],
								[]
			]),

		'Dread Formation' :(-4, [['Assault Unit'],
									['Assault Unit'],
									['Repair Bot'],
									['Repair Bot'],
									['Harrier Unit'],
									[],
									['Mageslayer Unit'],
									['Assault Unit','Harrier Unit'],
									[],
									[],
									[]
			]),


		'Chronid Hive' :  (1,  [['Drone'],
								['Drone'],
								['Drone'],
								['Ripper Drone','Screamer Drone'],
								['Ripper Drone','Screamer Drone'],
								['Ripper Drone','Screamer Drone','Hive Warrior'],
								['Hive Warrior'],
								['Drone'],
								['Behemoth'],
								['Broodmage'],
								['Ripper Drone','Screamer Drone','Hive Warrior'],
								['Hivelord'],
								[]
			]),

		'Ironkeep Warsquad' :  (-4, [   ['Ironkeep Knight'],
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
			]),

		'Spider Cave' :  (+3, [ ['Spiderling'],
								['Spiderling'],
								['Spiderling'],
								['Spiderling'],
								['Spiderling','Spiderling','Giant Wolfspider'],
								[],
								['Giant Wolfspider'],
								['Fateweaver','Giant Wolfspider','Fateweaver'],
								['Armored Crawler','Broodmother','Black Widower'],
								[],
								['Armored Crawler','Black Widower','Broodmother'],
								['Lich Crawler','Tomblurker Spider'],
								[],
								['Spider Queen']
			]),

		'Lone Rider' : (+3, [ ["Kobold Mage"],
			]),

		'Wandering Monster' : (0, [	['Ogre','Direwolf Alpha','Cyclops Brute','Cave Troll','Ogre Berserker','Cyclops Hurler','Wartroll']
			]),

		'Dragon Nest' : (0, [	['Flame Dragon','Frost Dragon','Bone Dragon']
			]),

		'Dane and the CS Nerds' :  (10, [  ["Dane, Son of Erick"],
											['Wartroll'],
											['Cyclops Hurler'],
											['Wartroll'],
											['Ogre Berserker'],
			]),

		"Ro'khan's Warpath" :  (10, [   ["Ro'khan, Prophet of Krog"],
											["Waa'zhok, Conduit of Krog"],
											['Orc Dethbrute'],
											['Orc Dethbrute'],
											['Orc Dethbrute'],
											['Orc Brute'],
											['Orc Brute'],
											['Orc Brute'],
											['Orc Brute'],
			]),

		"the Earthshakers": (10, [  ['Ripper Drone'],
									  ['Ripper Drone'],
									  ['Ripper Drone'],
									  ['Ripper Drone'],
									  ['Ripper Drone'],
									   ["Behemoth"],
									   ['Behemoth'],
									   ["Behemoth"],
									   ['the Worldeater'],
									   ]),

		'Revelation' :  		(10, [  ['Death'],
										['Famine'],
										['War'],
										['Pestilence'],
			]),





	}

	dicto = {	   1 : ['Orc Band', 'Undead Horde', 'Wandering Monster', 'Wolf Den', 'Kobold Party', 'Spider Cave',
						],  # -----
				   2 : [
						],  # -----
				   3 : ['Black Eye Cult', 'Demon Horde', 'Chronid Hive',
						],  # -----
				   4 : ['Uruk Warband', 'Dark Elf Guild', 'Black Eye Cult', 'Jelly Band',
						],  # -----
				   5 : ['Orc Hunting Party','Hobgoblin Squad',
						'Wolf Den', 'Kobold Party'],  # -----
				   6 : [
						],  # -----
				   7 : ['Ironkeep Warsquad',
						],  # -----
				   8 : ['Dread Formation',
						],  # -----
				   9 : [
						],  # -----
				   10: ['Dragon Nest',
						],  # -----
				   11 : [
						],  # -----
				   12 : [
						],  # -----
				   13 : [
						],  # -----
				   14 : [
						],  # -----
				   15 : ['Dane and the CS Nerds',
						],  # -----
				   16 : ['Revelation',
						],  # -----
				   17 : [
						],  # -----
				   18 : ["Ro'khan's Warpath",
						],  # -----
				   19 : [
						],  # -----
				   20 : ["the Earthshakers"
						],  # -----
					}

	# dicto = { 	   1 : ['the Earthshakers',
	# 					], # -----
	# 				2 : [
	# 					], # -----
	# 			   3 : [
	# 					], # -----
	# 			   4 : [
	# 					], # -----
	# 			   5 : [
	# 					], # -----
	# 			   6 : [
	# 					], # -----
	# 			   7 : [
	# 					], # -----
	# 			   8 : [
	# 					], # -----
	# 			   9 : [
	# 					], # -----
	# 			   10: ['Dragon Nest',
	# 					], # -----
	# 			   11 : [
	# 					], # -----
	# 				12 : [
	# 					], # -----
	# 				13 : [
	# 					], # -----
	# 				14 : [
	# 					], # -----
	# 				15 : ['Dane and the CS Nerds',
	# 					], # -----
	# 				16 : ['Revelation',
	# 					], # -----
	# 				17 : [
	# 					], # -----
	# 				18 : ["Ro'khan's Worldeaters",
	# 					], # -----
	# 				19 : [
	# 					], # -----
	# 			   }

