
from maps import Maps

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


	path = shortest_path((one.loc[0], one.loc[1]), (other.loc[0], other.loc[1]), Maps.rooms[game.map.map][0], game)

	if path is not None: one.loc = path[1]

	else: move_towards(one,other,game.map)





def shortest_path(looker, other, map_arr, game):

	# Make Graph

	a_dict = {}

	height, width = len(map_arr), len(map_arr[0])

	for orgx in range(width):

		for orgy in range(height):

			for x in range(-1,2):
				for y in range(-1,2):

					adx = x + orgx
					ady = y + orgy
					if 0 <= adx < width and 0 <= ady < height and (orgx != adx or orgy != ady):
						try: a_dict[(orgx,orgy)].append((adx,ady))
						except: a_dict[(orgx,orgy)] = [ (adx,ady) ]


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

				if map_arr[neighbor[1]][neighbor[0]] in set(['|', '-', '#', ' ', '+']) or neighbor in locs: continue
				
				new = path[:]
				new.append(neighbor)
				queue.append(new)

				if neighbor == other: return new

			visited.add(node)

	return None






def los(looker, other, map_arr, game):

	a_dict = {}


	height = len(map_arr)
	width = len(map_arr[0])


	for orgx in range(width):

		for orgy in range(height):


			for x in range(-1,2):
				

				adx = x + orgx
				ady = orgy
				if 0 <= adx < width and 0 <= ady < height and (orgx != adx or orgy != ady):
					try: a_dict[(orgx,orgy)].append((adx,ady))
					except: a_dict[(orgx,orgy)] = [ (adx,ady) ]

			for y in range(-1,2):
				adx = orgx
				ady = y + orgy
				if 0 <= adx < width and 0 <= ady < height and (orgx != adx or orgy != ady):
						try: a_dict[(orgx,orgy)].append((adx,ady))
						except: a_dict[(orgx,orgy)] = [ (adx,ady) ]

	visited = set([])
	queue = [[looker]]


	locs = set([])
	for unit in game.units:
		if other != (unit.loc[0], unit.loc[1]): locs.add((unit.loc[0], unit.loc[1]))

	while len(queue) > 0:

		path = queue.pop(0)
		node = path[-1]

		if node not in visited:
			for neighbor in a_dict[node]:

				if neighbor in locs: continue
				
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

					if boole:

						otherb = True

						for cnode in new:
							if map_arr[cnode[1]][cnode[0]] in set(['|', '-', '#','+']):
								otherb = False
								break

						if otherb: return new

			visited.add(node)

	return None



						