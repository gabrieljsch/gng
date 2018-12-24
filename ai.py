
from random import randint

def d(max_number):
	return randint(1,max_number)

def md(max_number, die_number):
	total = 0
	while die_number > 0:
		total += d(max_number)
		die_number -= 1
	return total

def adjacent_to(one, two):
	return True if (abs(one.loc[0] - two.loc[0]) <= 1) and (abs(one.loc[1] - two.loc[1]) <= 1) else False

def movement(decision, position):
	if decision == 'h': return position[0] - 1, position[1]
	elif decision == 'j': return position[0], position[1] + 1
	elif decision == 'k': return position[0], position[1] - 1
	elif decision == 'l': return position[0] + 1, position[1]
	elif decision == 'y': return position[0] - 1, position[1] - 1
	elif decision == 'u': return position[0] + 1, position[1] - 1
	elif decision == 'b': return position[0] - 1, position[1] + 1
	elif decision == 'n': return position[0] + 1, position[1] + 1
	else: return None

def move_towards(one, other, map):

	# Simple move towards, when no path can be made

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

		elif dx <= 1 <= dy:
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

		elif dx >= 1 >= dy:
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





# def shortest_path(looker, other, map_arr, game, blockers = True):

# 	a_dict = game.map.graph


# 	visited = set([])
# 	queue = [[looker]]

# 	locs = set([(unit.loc[0], unit.loc[1]) for unit in game.units if other != (unit.loc[0], unit.loc[1])])

# 	while queue:

# 		path = queue.pop(0)
# 		node = path[-1]

# 		if node not in visited:

# 			for neighbor in a_dict[node]:

# 				# Exception Squares
# 				if (game.map.map_array[neighbor[1]][neighbor[0]] in set(['|', '-', '#', ' ', '+','_']) or neighbor in locs) and blockers: continue
				
# 				new = path[:]
# 				new.append(neighbor)
# 				queue.append(new)

# 				if neighbor == other: return new

# 			visited.add(node)

# 	return None



def shortest_path(looker, other, map_arr, game, blockers = True):

	a_dict = game.map.graph


	paths = {}
	startvisited, endvisited = set([]), set([])
	squeue, equeue = [[looker]], [[other]]

	locs = set([(unit.loc[0], unit.loc[1]) for unit in game.units if other != (unit.loc[0], unit.loc[1])])

	i = 0

	while squeue or equeue:
		i += 1

		if squeue:

			spath = squeue.pop(0)
			snode = spath[-1]

			if snode not in startvisited:

				# Exit 1
				if snode in endvisited: return spath[:-1] + paths[snode][::-1]

				for neighbor in a_dict[snode]:

					# Exit 2
					if neighbor == other: return spath + [neighbor]

					# Exception Squares
					if (game.map.map_array[neighbor[1]][neighbor[0]] in {'|', '-', '#', ' ', '+','_'} or neighbor in locs) and blockers: continue
					
					new = spath[:] + [neighbor]
					squeue.append(new)

				startvisited.add(snode)
				paths[snode] = spath

		if equeue:

			epath = equeue.pop(0)
			enode = epath[-1]

			if enode not in endvisited:

				# Exit 3
				if enode in startvisited: return paths[enode][:-1] + epath[::-1]

				for neighbor in a_dict[enode]:

					# Exception Squares
					if (game.map.map_array[neighbor[1]][neighbor[0]] in {'|', '-', '#', ' ', '+', '_'} or neighbor in locs) and blockers: continue
					
					new = epath[:] + [neighbor]
					equeue.append(new)

				endvisited.add(enode)
				paths[enode] = epath

	return None






def los(looker, other, map_arr, game, range = False):




	def lostest(new):

		if other[0] >= looker[0] and other[1] >= looker[1]:
			for cnode in new[1:-1]:
				if game.map.map_array[cnode[1]][cnode[0]] in {'|', '-', '#', '+', '_'} or cnode in locs or not (other[0] >= cnode[0] >= looker[0] and other[1] >= cnode[1] >= looker[1]):
					return None
		elif other[0] >= looker[0] and other[1] <= looker[1]:
			for cnode in new[1:-1]:
				if game.map.map_array[cnode[1]][cnode[0]] in {'|', '-', '#', '+', '_'} or cnode in locs or not (other[0] >= cnode[0] >= looker[0] and other[1] <= cnode[1] <= looker[1]):
					return None
		elif other[0] <= looker[0] and other[1] >= looker[1]:
			for cnode in new[1:-1]:
				if game.map.map_array[cnode[1]][cnode[0]] in {'|', '-', '#', '+', '_'} or cnode in locs or not (other[0] <= cnode[0] <= looker[0] and other[1] >= cnode[1] >= looker[1]):
					return None
		elif other[0] <= looker[0] and other[1] <= looker[1]:
			for cnode in new[1:-1]:
				if game.map.map_array[cnode[1]][cnode[0]] in {'|', '-', '#', '+', '_'} or cnode in locs or not (other[0] <= cnode[0] <= looker[0] and other[1] <= cnode[1] <= looker[1]):
					return None

		return new








	a_dict = game.map.graph


	paths = {}
	startvisited, endvisited = set([]), set([])
	squeue, equeue = [[looker]],[[other]]

	# Unique for LOS, last part is VERY important
	locs = set([(unit.loc[0], unit.loc[1]) for unit in game.units if other != (unit.loc[0], unit.loc[1]) and game.player.loc != (unit.loc[0], unit.loc[1])])

	while squeue or equeue:

		if squeue:

			spath = squeue.pop(0)
			# print("spath",spath)
			snode = spath[-1]

			# Pre-determined range!!!!
			if range is not False and len(spath) > range: continue

			if snode not in startvisited:

				# Exit 1
				if snode in endvisited:
					# print("G1")
					# print(spath[:-1] + paths[snode][::-1])
					# print(lostest(spath[:-1] + paths[snode][::-1]))
					return lostest(spath[:-1] + paths[snode][::-1])


				for neighbor in a_dict[snode]:

					# Exit 2
					if neighbor == other:
						# print("G2")
						return spath + [neighbor]

					new = spath[:] + [neighbor]
					squeue.append(new)

				startvisited.add(snode)
				paths[snode] = spath

		if equeue:

			epath = equeue.pop(0)
			# print("epath",epath)
			enode = epath[-1]

			# Pre-determined range!!!!
			if range is not False and len(epath) > range: continue

			if enode not in endvisited:

				# Exit 3
				if enode in startvisited:
					# print("G3")
					return lostest(paths[enode][:-1] + epath[::-1])

				for neighbor in a_dict[enode]:

					new = epath[:] + [neighbor]
					equeue.append(new)

				endvisited.add(enode)
				paths[enode] = epath

	return None
