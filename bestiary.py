from random import randint

def d(range):
	return randint(1,range)

class Monsters():
	# self,      char, tier,    con, st, dex, int, cha, mspeed,  xp,  pot_weapons, pot_armor, other_items

	array = {

		# Goblins
		"Goblin" : 		   	 ["g",1,  1,2,3,1,1,0.9, 4, ['stabba','goblin spear','club'] , ['animal skin','bear hide']],
		"Goblin Archer" :    ["a",1,  2,1,4,1,1,0.85, 4, ['stabba'] , ['animal skin','bear hide'], ['goblin bow']],
		"Goblin Skirmisher" :["g",1,  3,2,3,1,1,0.85, 6, ['slica','choppa'] , ['bear hide'], ['buckler shield']],
		"Witch Goblin" :     ["w",2,  3,3,3,3,2,0.9, 8, ['stabba'] , ['troll hide'], ['poison breath']],
		"Goblin Nob" : 	     ["n",2,  4,3,2,1,3,1.0, 8, ['choppa', 'smasha'] , ['troll hide']],
		"Goblin Warboss" :   ["G",3,  5,4,4,2,6,0.95, 15,['big choppa','big slica', 'skull smasha'] , ['troll hide']],

		# Orcs
		"Orc Warboy" : 	   ["o",2,  3,4,3,2,3,1.1, 6, ['slica','choppa','smasha'] , ['bear hide', 'troll hide']],
		"Orc Archer" :     ["a",2,  3,3,4,2,3,1.0, 6, ['choppa', 'slica'] , ['bear hide', 'troll hide'], ['crude shortbow']],
		"Orc Warrior" :    ["o",2,  4,4,3,2,3,1.1, 9, ['slica','smasha','choppa'] , ['troll hide']],
		"Orc Warlock" :    ["W",3,  4,3,3,4,6,1.0, 15, ['toxic slica'] , ['wyvern scale armor','troll hide'], ['poison breath']],
		"Orc Berserker" :  ["b",3,  4,5,4,2,8,0.8, 15, ['choppa','slica'] , ['troll hide'], ['headbutt','choppa']],
		"Orc Nob" : 	   ["N",3,  4,5,3,2,6,1.2, 15, ['big choppa','big slica','skull smasha'] , ['berserker mail','scrap plate armor'], ['headbutt']],
		"Orc Warboss" :    ["O",5,  5,6,4,3,8,1.2, 30, ['boss choppa','ice choppa'] , ['Orcish dreadplate','scrap plate armor'], ['headbutt']],

		# Uruks
		"Uruk Warrior" :   ["u",3,  4,4,3,2,3,1.0, 15, ['hooked longsword'] , ['blackiron plate'], ['iron fang shield']],
		"Uruk Pikeman" :   ["u",3,  4,4,3,2,3,1.0, 15, ['uruk-hai pike'] , ['blackiron plate']],
		"Uruk Bolter" :    ["b",3,  4,3,4,2,3,0.9, 15, ['hooked longsword'] , ['blackiron plate'], ['uruk crossbow']],
		"Uruk Headhunter" :["h",4,  4,4,4,2,3,1.0, 22, ['hooked greatsword'] , ['blackiron plate']],
		"Uruk Berserker" : ["U",4,  5,4,3,2,3,1.0, 22, ['hooked greatsword'] , ['berserker mail'], ['headbutt']],
		"Uruk Bodyguard" : ["B",5,  6,5,3,2,3,1.2, 30, ['hooked greatsword','uruk-hai pike'] , ['blackiron plate'], ['iron fang shield','shield hit']],
		"Uruk Warlord" :   ["U",6,  6,6,3,2,3,1.0, 50, ['hooked greatsword'] , ['blackiron plate']],

		# Undead
		"Living Corpse" : 	  ["z",1,  2,2,1,1,10,1.3, 4, ['iron longsword','iron axe','iron dagger','mace'] , ['tattered garments',]],
		"Undead Legionaire" : ["z",2,  3,3,2,2,10,1.2, 8, ['iron longsword','iron axe','iron dagger','mace'] , ['tattered garments','rotted chainmail']],
		"Plague Bearer" :     ["p",2,  4,3,1,2,10,1.3, 8, ['iron longsword','iron axe','iron dagger','mace'] , ['rotted chainmail']],
		"Undead Hound" :  	  ["h",3,  4,3,1,3,10,0.7, 15, ['iron longsword','iron axe','iron dagger','mace'] , ['tattered garments']],
		"Flayed One" :    	  ["f",3,  4,2,1,4,10,0.8, 15, ['iron longsword','iron axe','iron dagger','mace'] , ['tattered garments']],
		"Undead Hulk" :   	  ["H",4,  7,4,1,3,10,1.7, 24, ['iron longsword','iron axe','iron dagger','mace'] , ['tattered garments']],

		# The Black Eye
		"Black Eye Cultist" :   ["c",2,  3,3,3,2,4,1.0, 8, ['iron dagger','mace'] , ['tainted robe']],
		"Black Eye Disciple" :  ["b",3,  4,3,3,4,4,0.9, 14, ['spiked mace'] , ['tainted robe']],
		"Black Eye Destroyer" : ["D",5,  4,3,3,4,4,1.0, 30, ['spiked mace'] , ['tainted robe'], ['dark transformation']],
		"Abomination" : 		["A",5,  6,6,1,1,4,1.6, 30, ['fist smash'] , ['tainted robe']],
		"Black Eye Prophet" :   ["P",6,  5,3,3,2,4,1.0, 50, ['spiked mace'] , ['tainted robe'], ['dark transformation']],
		"Black Eye Chosen" :    ["C",7,  7,3,3,2,4,1.0, 100, ['spiked mace'] , ['tainted robe'], ['dark transformation']],

		# Dark Elves
		"Dark Elf Scout" : 		["s",3,  4,3,5,4,4,0.95, 15, ['sun spear'] , ['blackiron plate']],
		"Dark Elf Hunter" : 	["h",4,  4,4,6,4,4,0.85, 23, ['sun spear'] , ['blackscale'], ['blackwood longbow']],
		"Dark Elf Praetorian" : ["d",4,  5,4,5,4,6,0.95, 23, ['sun spear'] , ['blackscale']],
		"Dark Elf Dragoon" :    ["D",5,  6,4,5,4,9,0.60, 30, ['sun spear'] , ['blackscale']],
		}

class Bands():  # Tier Bonus :   formations

 	formations = {

 		'Orc Band' :      (1, [ ['Goblin','Goblin Archer','Goblin Nob','Goblin Nob', 'Goblin Warboss'], 
 								['Goblin','Goblin Skirmisher','Witch Goblin','Orc Warboy','Orc Nob'], 
 						 	    ['Goblin', 'Orc Archer', 'Orc Warboy', 'Orc Warrior', 'Orc Nob'],
 						 	    ['Orc Warrior'],
 						 	    ['Orc Warrior', 'Orc Berserker'],
 						 	    ['Orc Nob'],
 						 	    ['Orc Warboss'],
 			] ),
 		'Undead Horde' : (2, [  ['Living Corpse'], 
 								['Living Corpse'], 
 								['Living Corpse','Living Corpse','Undead Legionaire'],
 								['Undead Legionaire', 'Plague Bearer'],
 								['Undead Legionaire', 'Plague Bearer'],
 								[],
 								[],
 			] ),
 		'Uruk Warband' :  (-1, [ ['Uruk Warrior'], 
 								['Uruk Bolter'], 
 								['Uruk Warrior', 'Uruk Warrior','Uruk Pikeman', 'Uruk Pikeman'],
 								[],
 								['Uruk Headhunter', 'Uruk Headhunter','Uruk Berserker'],
 								['Uruk Warlord'],
 								['Uruk Bodyguard'],
 			] ),

 		'Dark Elf Raiding Party' :  (-1, [  ['Dark Elf Scout', 'Dark Elf Praetorian'], 
			 								['Dark Elf Scout', 'Dark Elf Hunter'], 
			 								['Dark Elf Praetorian'],
			 								[],
			 								['Dark Elf Dragoon'],
			 								[],
			 								[],
 			] ),

 		'Black Eye Cult' :  		(0, [   ['Black Eye Cultist', 'Black Eye Cultist'], 
			 								['Black Eye Cultist', 'Black Eye Cultist'], 
			 								['Black Eye Disciple'],
			 								['Black Eye Disciple','Black Eye Disciple','Black Eye Destroyer'],
			 								['Black Eye Destroyer'],
			 								[],
			 								['Black Eye Prophet'],
 			] ),


 	}

 	dicto = { 	   1 : ['Orc Band','Undead Horde'],
 				   2 : ['Orc Band','Undead Horde','Black Eye Cult'],
 				   3 : ['Orc Band','Undead Horde','Dark Elf Raiding Party','Black Eye Cult'],
 				   4 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Raiding Party','Black Eye Cult'],
 				   5 : ['Orc Band','Undead Horde','Uruk Warband','Dark Elf Raiding Party','Black Eye Cult'],
 				   }

