from sty import fg, bg, rs

class Colors:

	array = {
		'red' : (255, 10, 10),
		'orange' : (255, 150, 50),
		'fire' : (255,69,0),
		'green' : (50, 205, 50),
		'darkgreen' : (0,128,0),
		'springgreen' : (0,250,154),
		'yellow' : (255,255,0),
		'gold' : (212,175,55),
		'cyan' : (0,255,255),
		'blue' : (0,0,255),
		'lightblue' : (65,105,225),
		'brown' : (139,69,19),
		'darkbrown' : (84,42,14),
		'tan' : (205,133,63),
		'grey' : (105,105,105),
		'purple' : (128,0,128),
		'magenta' : (255,0,255),
		'salmon' : (250,128,114),
		'darkred' : (139, 0, 0),
		'bronze' : (205,127,50),
		'bone' : (238,232,170),
		'steel' : (119,136,153),
	}

	@staticmethod
	def color(statement, color):
		color = Colors.array[color]
		return fg(color[0], color[1], color[2]) + str(statement) + fg.rs

	@staticmethod
	def bcolor(statement, bcolor):
		bcolor = Colors.array[bcolor]
		return bg(bcolor[0], bcolor[1], bcolor[2]) + str(statement) + bg.rs

	@staticmethod
	def fullcolor(statement, fcolor, bcolor):
		color, bcolor = Colors.array[fcolor], Colors.array[bcolor]
		return fg(color[0], color[1], color[2]) + bg(bcolor[0], bcolor[1], bcolor[2]) + str(statement) + rs.all