from random import randint, shuffle

def d(range):
	return randint(1,range)

def md(range, number):
	sum = 0
	while number > 0:
		sum += d(range)
		number -= 1
	return sum


class CharacterInfo():
	# 		(17)    con, st, dex, inte, cha, mspeed, reg,  resistances(fr,fi,po,ac,sh,ex)   class equipment,   innate weapons (power, ability)

	races = {
		"Cytherean" :  [[2,2,4,5,3,0.9, 12, [0,0,0,0,3,3]], [("wraithwalk",True)]],
		"Gnome" :      [[2,3,6,4,3,0.7, 11, [0,0,0,0,0,0]], [("tripmine",True)]],
		"Hobbit" :     [[2,3,5,3,6,0.8, 11, [1,1,1,1,1,1]], [("leap", True)]],
		"Elf" : 	   [[3,3,5,4,3,1.0,  9, [0,0,0,0,0,0]], [("wild equilibrium",True)]],
		"Terran" :     [[4,3,3,3,5,1.0, 14, [0,0,0,0,0,0]], []],
		"Naga" :       [[4,3,4,4,1,0.9, 22, [0,0,3,0,0,0]], [("envenom",True), "tail smash"]],
		"Ghoul" :      [[4,4,4,2,1,1.1,  6, [0,0,0,3,0,0]], [("feral bite",True)]],
		"Dragonborn" : [[4,5,2,3,2,1.3, 14, [0,2,0,0,0,0]], [("flame tongue",True), "tail smash"]],
		"Black Orc" :  [[5,4,2,2,2,1.3, 15, [2,0,0,0,0,0]], [("green blood",True),"headbutt"]],
		"Dwarf" : 	   [[6,3,2,3,3,1.4, 10, [0,0,0,0,0,2]], [("iron grit",True)]],
		"Hill Troll" : [[6,5,1,1,1,1.6, 16, [0,0,0,0,0,0]], []],
	}

	race_starting_equipment = {
		"Cytherean" :  [["iron shortsword","buckler shield","hide armor"],
						["mace","buckler shield","hide armor"],
						["shortbow","iron shortsword","iron arrow","leather armor"],
						["iron dagger","iron dagger","throwing knife","leather armor"],
						["oak staff","wool robes",("magic missile",False)],
						["oak staff","wool robes",("dark bolt",False)]],

		"Gnome" :      [["iron shortsword","buckler shield","hide armor"],
						["hammer","buckler shield","hide armor"],
						["shortbow","iron shortsword","iron arrow","leather armor"],
						["iron dagger","iron dagger","throwing knife","leather armor"],
						["oak staff","wool robes",("magic missile",False)],
						["oak staff","wool robes",("dark bolt",False)]],

		"Hobbit" :     [["iron shortsword","buckler shield","hide armor"],
						["hammer","buckler shield","hide armor"],
						["shortbow","iron shortsword","iron arrow","leather armor"],
						["iron dagger","iron dagger","throwing knife","leather armor"],
						["oak staff","wool robes",("magic missile",False)],
						["oak staff","wool robes",("dark bolt",False)]],

		"Elf" : 	   [["spear","buckler shield","hide armor"],
						["mace","buckler shield","hide armor"],
						["shortbow","iron shortsword","iron arrow","leather armor"],
						["iron dagger","iron dagger","throwing knife","leather armor"],
						["oak staff","wool robes",("magic missile",False)],
						["oak staff","wool robes",("dark bolt",False)]],

		"Terran" :     [["iron longsword","buckler shield","hide armor"],
						["mace","buckler shield","hide armor"],
						["shortbow","iron shortsword","iron arrow","leather armor"],
						["iron dagger","iron dagger","throwing knife","leather armor"],
						["oak staff","wool robes",("magic missile",False)],
						["oak staff","wool robes",("dark bolt",False)]],

		"Naga" :       [["iron shortsword","buckler shield","hide armor"],
						["mace","buckler shield","hide armor"],
						["shortbow","iron dagger","iron arrow","leather armor"],
						["iron dagger","iron dagger","leather armor"],
						["iron dagger","wool robes",("poison breath",False)],
						["iron dagger","wool robes",("dark bolt",False)]],

		"Ghoul" :      [["iron axe","buckler shield","hide armor"],
						["mace","buckler shield","hide armor"],
						["crude shortbow","iron shortsword","iron arrow","leather armor"],
						["iron dagger","iron dagger","iron javelin","leather armor"],
						["iron dagger","tainted robes",("magic missile",False)],
						["iron dagger","tainted robes",("dark bolt",False)]],

		"Dragonborn" : [["iron axe","buckler shield","hide armor"],
						["mace","buckler shield","hide armor"],
						["crude shortbow","iron shortsword","iron arrow","leather armor"],
						["iron dagger","iron dagger","iron javelin","leather armor"],
						["oak staff","wool robes",("magic missile",False)],
						["oak staff","wool robes",("dark bolt",False)]],

		"Black Orc" :  [["iron axe","buckler shield","hide armor"],
						["smasha","buckler shield","hide armor"],
						["crude shortbow","slica","iron arrow","troll hide"],
						["hand axe","hand axe","throwing axe","troll hide"],
						["oak staff","wool robes",("poison breath",False)],
						["oak staff","wool robes",("dark bolt",False)]],

		"Dwarf" : 	   [["iron axe","buckler shield","hide armor"],
						["hammer","buckler shield","hide armor"],
						["shortbow","hand axe","iron arrow","leather armor"],
						["hand axe","hand axe","throwing axe","leather armor"],
						["oak staff","wool robes",("magic missile",False)],
						["oak staff","wool robes",("dark bolt",False)]],

		"Hill Troll" : [["club","hide armor"],
						["club","hide armor"],
						["crude shortbow","iron dagger","iron arrow","bear hide"],
						["iron dagger","bear hide","iron javelin"],
						["iron dagger","wolf pelt",("poison breath",False)],
						["iron dagger","wolf pelt",("dark bolt",False)]],
	}

	class_list = ["Warrior","Paladin","Ranger","Rogue","Mage","Warlock"]

	class_progression = { # spells / level
		"Warrior" : ['str'],
		"Paladin" : ['con', ['flash heal','deathmark']],
		"Ranger" : ['dex'],
		"Rogue" : ['dex'],
		"Mage" : ['int', ['chain lightning','flame tongue']],
		"Warlock" : ['int',['raise skeleton']],
	}

