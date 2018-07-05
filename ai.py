
from maps import Maps

from random import shuffle

def move_towards(one, other, map):

	x = one.loc[0]
	y = one.loc[1]

	dx = one.loc[0] - other.loc[0]
	dy = one.loc[1] - other.loc[1]

	if dx == 0 or dy == 0:

		if dx == 0:
			if dy < 0:
				if map.can_move((x, y + 1)): one.loc = (one.loc[0], one.loc[1] + 1)
			else:
				if map.can_move((x, y - 1)): one.loc = (one.loc[0], one.loc[1] - 1)

		if dy == 0:
			if dx < 0:
				if map.can_move((x + 1, y)): one.loc = (one.loc[0] + 1, one.loc[1])
			else:
				if map.can_move((x - 1, y)): one.loc = (one.loc[0] - 1, one.loc[1])

	else:


		if dx <= 1 and dy <= 1:
			if map.can_move((x + 1, y + 1)):
				one.loc = (one.loc[0] + 1, one.loc[1] + 1)
			else:
				if dx > dy:
					if map.can_move((x + 1, y)):
						one.loc = (one.loc[0] + 1, one.loc[1])
						return
					if map.can_move((x, y + 1)):
						one.loc = (one.loc[0], one.loc[1] + 1)
				else:
					if map.can_move((x, y + 1)):
						one.loc = (one.loc[0], one.loc[1] + 1)
						return
					if map.can_move((x + 1, y)):
						one.loc = (one.loc[0] + 1, one.loc[1])

		elif dx >= 1 and dy >= 1:
			if map.can_move((x - 1, y - 1)):
				one.loc = (one.loc[0] - 1, one.loc[1] - 1)
			else:
				if dx > dy:

					if map.can_move((x - 1, y)):
						one.loc = (one.loc[0] - 1, one.loc[1])
						return
					if map.can_move((x, y - 1)):
						one.loc = (one.loc[0], one.loc[1] - 1)
				else:
					if map.can_move((x, y - 1)):
						one.loc = (one.loc[0], one.loc[1] - 1)
						return
					if map.can_move((x - 1, y)):
						one.loc = (one.loc[0] - 1, one.loc[1])

		elif dx <= 1 and dy >= 1:
			if map.can_move((x + 1, y - 1)):
				one.loc = (one.loc[0] + 1, one.loc[1] - 1)
			else:
				if dx > dy:
					if map.can_move((x + 1, y)):
						one.loc = (one.loc[0] + 1, one.loc[1])
						return
					if map.can_move((x, y - 1)):
						one.loc = (one.loc[0], one.loc[1] - 1)
				else:
					if map.can_move((x, y - 1)):
						one.loc = (one.loc[0], one.loc[1] - 1)
						return
					if map.can_move((x + 1, y)):
						one.loc = (one.loc[0] + 1, one.loc[1])

		elif dx >= 1 and dy <= 1:
			if map.can_move((x - 1, y + 1)):
				one.loc = (one.loc[0] - 1, one.loc[1] + 1)
			else:
				if dx > dy:
					if map.can_move((x - 1, y)):
						one.loc = (one.loc[0] - 1, one.loc[1])
						return
					if map.can_move((x, y + 1)):
						one.loc = (one.loc[0], one.loc[1] + 1)
				else:
					if map.can_move((x, y + 1)):
						one.loc = (one.loc[0], one.loc[1] + 1)
						return
					if map.can_move((x - 1, y)):
						one.loc = (one.loc[0] - 1, one.loc[1])


def smart_move_towards(one, other, game):


	path = shortest_path((one.loc[0], one.loc[1]), (other.loc[0], other.loc[1]), game.map, game)

	if path is not None: one.loc = path[1]

	else: move_towards(one,other,game.map)





def shortest_path(looker, other, map_arr, game, blockers = True):

	a_dict = game.map.graph


	visited = set([])
	queue = [[looker]]

	locs = set([])
	for unit in game.units:
		if other != (unit.loc[0], unit.loc[1]): locs.add((unit.loc[0], unit.loc[1]))

	while queue:

		path = queue.pop(0)
		node = path[-1]

		if node not in visited:

			for neighbor in a_dict[node]:

				# Exception Squares
				if (game.map.map_array[neighbor[1]][neighbor[0]] in set(['|', '-', '#', ' ', '+','_']) or neighbor in locs) and blockers: continue
				
				new = path[:]
				new.append(neighbor)
				queue.append(new)

				if neighbor == other: return new

			visited.add(node)

	return None






def los(looker, other, map_arr, game, range = False):


	a_dict = game.map.graph


	visited = set([])
	queue = [[looker]]


	locs = set([])
	for unit in game.units:
		if other != (unit.loc[0], unit.loc[1]): locs.add((unit.loc[0], unit.loc[1]))

	while queue:

		path = queue.pop(0)
		node = path[-1]

		# Pre-determined range!!!!
		if range is not False and len(path) > range: continue

		if node not in visited:
			for neighbor in a_dict[node]:

				# Exception Squares
				if game.map.map_array[neighbor[1]][neighbor[0]] in set(['|', '-', '#', '+','_']) or neighbor in locs: continue

				new = path[:]
				new.append(neighbor)
				queue.append(new)

				if neighbor == other:

					boole = True

					if other[0] >= looker[0] and other[1] >= looker[1]:
						for cnode in new[1:-1]:
							if not (other[0] >= cnode[0] >= looker[0] and other[1] >= cnode[1] >= looker[1]):
								boole = False
								break
					elif other[0] >= looker[0] and other[1] <= looker[1]:
						for cnode in new[1:-1]:
							if not (other[0] >= cnode[0] >= looker[0] and other[1] <= cnode[1] <= looker[1]):
								boole = False
								break
					elif other[0] <= looker[0] and other[1] >= looker[1]:
						for cnode in new[1:-1]:
							if not (other[0] <= cnode[0] <= looker[0] and other[1] >= cnode[1] >= looker[1]):
								boole = False
								break
					elif other[0] <= looker[0] and other[1] <= looker[1]:
						for cnode in new[1:-1]:
							if not (other[0] <= cnode[0] <= looker[0] and other[1] <= cnode[1] <= looker[1]):
								boole = False
								break

					if boole: return new

			visited.add(node)

	return None



						