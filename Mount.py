

class Mount:

	def __init__(self, roomfiller, rider, mount, ally):
		roomfiller.spawn(mount, rider.loc, ally, rider)
