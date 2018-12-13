import termios, fcntl
import select
from sty import fg, bg, rs
from Descriptions import Descriptions, Colors
from codex import Weapons, Ammos, Brands, Armors, Shields, Tomes, Potions


def color(statement, color):
	color = Colors.array[color]
	return fg(color[0], color[1], color[2]) + str(statement) + fg.rs

def bcolor(statement, bcolor):
	bcolor = Colors.array[bcolor]
	return bg(bcolor[0], bcolor[1], bcolor[2]) + str(statement) + bg.rs

def fullcolor(statement, fcolor, bcolor):
	color, bcolor = Colors.array[fcolor], Colors.array[bcolor]
	return fg(color[0], color[1], color[2]) + bg(bcolor[0], bcolor[1], bcolor[2]) + str(statement) + rs.all

class Potion:

	def __init__(self, name, color_tone, loc, number = 1):
		self.rep, self.color, self.number, self.loc = '!', color_tone, number, loc

		self.name, self.base_string = color(name, self.color), name

	def drink(self, user):

		if self.base_string == "healing potion":

			user.hp = min(user.maxhp, user.hp + 20)

			if user.name == 'you': game.game_log.append('You drink a ' + self.name + '; you feel better.' )
			else: game.game_log.append(user.info[3] + ' drinks a ' + self.name + '; it seems better.')

		elif self.base_string == "orcblood potion":

			game.check_passives(user, True)

			if user.name == 'you': game.game_log.append('You drink a ' + self.name + '; you feel normal.' )
			else: game.game_log.append(user.info[3] + ' drinks a ' + self.name + '; it looks back to normal.')

		elif self.base_string == "resistance potion":

			apply(user, 'resistant', 30, stacking=True)
			user.frostr, user.firer, user.poisonr, user.acidr, user.shockr, user.expr = user.frostr+3, user.firer+3, user.poisonr+3, user.acidr+3, user.shockr+3, user.expr+3

			if user.name == 'you': game.game_log.append('You drink a ' + self.name + '; you feel more resistant.')
			else: game.game_log.append(user.info[3] + ' drinks a ' + self.name + '; it looks more resistant.')

		elif self.base_string == "quicksilver potion":

			apply(user, 'hastened', 20, stacking=True)
			user.mspeed = user.mspeed / 4

			if user.name == 'you': game.game_log.append('You drink a ' + self.name + '; you feel restless.' )
			else: game.game_log.append(user.info[3] + ' drinks a ' + self.name + '; it seems restless.')

		self.number -= 1
		if self.number == 0: user.inventory.remove(self)

	def details(self):

		print(self)
		print("")
		print(Descriptions.potions[self.base_string])
		print("You are carrying " + str(self.number) + ".")

	def __str__(self):

		return self.name + ' (' + str(self.number) + ')'