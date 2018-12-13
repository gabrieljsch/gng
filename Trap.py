from Maps import Maps

from bestiary import Monsters
from codex import Weapons, Ammos, Brands
from Colors import Colors
# from Player import Player
from ai import *

from sty import fg, bg



class Trap:

	def __init__(self, damage, type, loc):
		self.damage, self.type, self.loc, self.rep, self.color = damage, type, loc,'*','darkred'
		self.base_string = "trap"

	def trip(self, game):
		if self.type == 'mine':
			# Blast Radius
			spaces, affected = set([]), []
			for x in range(-1,2):
				for y in range(-1,2):
					if self.loc[0] + x >= 0 and self.loc[1] + y >= 0: spaces.add((self.loc[0] + x, self.loc[1] + y))
			# Find units affected
			for unit in game.units:
				if unit.loc in spaces:
					if unit.loc == self.loc: triggerer = self.loc
					affected.append(unit)
			# Hit string
			hit = ""
			for unit in affected:

				# Explosive Resist
				resist = unit.calc_resistances()[5]
				if d(4) <= resist:
					if unit.name == 'you': game.game_log.append("You shrug off the mine's explosion!")
					else: game.game_log.append(unit.info[3] + " shrugs off the mine's explosion!")
					continue

				unit.hp -= self.damage
				if len(hit) == 0: hit += unit.info[0]
				else: hit += ", " + unit.info[0]
			try: game.game_log.append(triggerer.info[3]+ " sets off the mine, dealing " + str(self.damage) + " damage to " + hit + '!')
			except: game.game_log.append("The mine explodes, dealing " + str(self.damage) + " damage to " + hit + '!')

		game.items.remove(self)