import ai
from Maps import Maps
from ai import *

from bestiary import Monsters, Bands
from codex import Weapons, Ammos, Brands, Armors, Shields, Tomes, Potions
from Spells import Spells
from Weapon import Weapon
from Armor import Armor
from Shield import Shield
from Tome import Tome
from Ammo import Ammo
from Potion import Potion
from Trap import Trap
from Chest import Chest
from Monster import Monster
from Mount import Mount


# noinspection PyBroadException
class RoomFiller:

	def __init__(self, tier, pos, map, game):
		self.tier, self.pos, self.map = tier, pos, map
		self.game = game

	@staticmethod
	def place_trap(self, damage, trap_type, loc):
		self.game.items.append( Trap( damage, trap_type, loc))

	def place(self):

		# Fill if specified by map
		if Maps.rooms[self.map][4]: self.fill()

		# Place Chests
		for loc, chance in Maps.rooms[self.map][1]:

			# Pick Chest Type
			roll = d(100)
			if roll + 2*self.tier > 106: chest_type = "golden"
			elif roll + 2*self.tier > 103: chest_type = "elven"
			elif roll + 2*self.tier > 97: chest_type = "dark elven"
			elif roll + 2*self.tier > 20: chest_type = "wooden"
			else: chest_type = "orcish"

			if d(100) <= chance: self.place_chest(chest_type, self.game.player.level, loc)

	def fill(self):

		# Tier and Band pick
		enemy_tier = min(self.tier, len(Bands.dicto))
		tier_group = self.game.bands
		band = tier_group[d(len(tier_group)) - 1]

		# Bonuses and actual bands
		bonus, groups = Bands.formations[band]

		# Cut off some units
		squad = groups[:self.tier + bonus]
		spawned = set([])

		# For each member of squad, spawn it
		for i in range( len(squad)):

			group = groups[i]

			# Choose which units to spawn
			if len(group) > 0:
				unit = min(len(group) - 1, d(enemy_tier + bonus - max(i, bonus)) - 1)

				picked = False
				while not picked:

					# Pick spawn location
					try: spawn_location = (d(int(len(Maps.rooms[self.map][0][0]))) - 1, d(len(Maps.rooms[self.map][0])) - 1)
					except: spawn_location = (d(len(Maps.rooms[self.map][0][0])) - 1, d(len(Maps.rooms[self.map][0])) - 1)

					try:
						forbidden, forbidden_squares = Maps.rooms[self.map][5], set([])

						for x in range(-forbidden[1], forbidden[1] + 1):
							for y in range(-forbidden[1], forbidden[1] + 1): forbidden_squares.add((x + forbidden[0][0],y + forbidden[0][1]))
						if spawn_location in forbidden_squares: continue
					except IndexError: pass

					try:
						if self.game.map.square_identity(spawn_location) not in {'|', '-', ' ', '#', '+', '@', '_'} and spawn_location != self.game.player.loc and spawn_location not in spawned:
							picked = True
							prev_loc = spawn_location
							spawned.add(prev_loc)
					except: pass


				self.spawn(group[unit] , spawn_location)

	def spawn(self, monster_name, loc, ally=False, mount_unit = None):
		data = Monsters.array[monster_name]
		try: other_items = data[16]
		except IndexError: other_items = None

		pot_weapons = data[14]
		pot_armor = data[15]

		# Spawn Unit
		unit = Monster(self.game, monster_name, data[0],data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], loc, other_items)

		# Give innate weapons / shields
		if other_items is not None:
			for item in other_items:
				if item in Ammos.array:
					unit.give_ammo(item)
				elif item in Weapons.array:
					unit.give_weapon(item)
				elif item in Shields.array:
					unit.give_shield(item)
				elif item in Spells.spells:
					unit.spells.append(item)
				elif item in Tomes.array:
					unit.give_tome(item)
				elif item in Potions.array:
					unit.give_potion(item)
				elif item in Monsters.array:
					ally = True if unit in self.game.allies else False
					unit.mount = Mount(self.game.map.room_filler, unit, item, ally)
					unit.mount.unit = self.game.units[-1]
					unit.mount.unit.rider = unit
				else:
					unit.traits.append(item)

		# Give Weapon and Armor
		items = pot_weapons[d(len(pot_weapons)) - 1]
		if type(items) != list: items = [items]
		for item in items:
			if item in Weapons.array:
				unit.give_weapon(item)
			elif item in Shields.array:
				unit.give_shield(item)
			elif item in Tomes.array:
				unit.give_tome(item)
		unit.give_armor(pot_armor[d(len(pot_armor)) - 1])

		self.game.units.append(unit)
		if ally: self.game.allies.append(unit)

	def place_weapon(self, weapon, loc, enchantment=0, brand=None):
		data = Weapons.array[weapon]

		# Manage Enchantment + Brand
		spawned_enchantment = data[4] + enchantment
		try: brand = data[8]
		except IndexError: pass

		# Create Weapon Object
		self.game.items.append(Weapon(self.game, weapon, data[0], data[1], data[2], data[3], spawned_enchantment, data[5], data[6], data[7], loc, brand))

	def place_armor(self, armor, loc, enchantment=0, brand=None):
		data = Armors.array[armor]

		# Manage Enchantment + Brand
		spawned_enchantment = data[5] + enchantment
		try: brand = data[6]
		except IndexError: pass

		# Create Armor Object
		self.game.items.append(Armor(armor, data[0], data[1], data[2], data[3], data[4], spawned_enchantment, loc, brand))

	def place_shield(self, armor, loc, enchantment=0, brand=None):
		data = Shields.array[armor]

		# Manage Enchantment
		spawned_enchantment = data[5] + enchantment
		try: brand = data[6]
		except IndexError: pass

		# Create Shield Object
		self.game.items.append(Shield(self.game, armor, data[0], data[1], data[2], data[3], data[4], spawned_enchantment, loc, brand))


	def place_ammo(self, ammo, loc, number, brand=None):
		data = Ammos.array[ammo]

		# Manage Enchantment
		try: brand = data[4]
		except IndexError: pass

		# Create Ammo Object
		self.game.items.append(Ammo(ammo, data[0], data[1], data[2], number, data[3], loc, brand))


	def place_potion(self, pot, loc, number):
		data = Ammos.array[pot]

		# Create Potion Object
		self.game.items.append(Ammo(pot, data, loc, number))

	def place_chest(self, chest_type, tier, loc):
		self.game.items.append(Chest(chest_type, tier, loc, self.game))

	def give_weapon(self, unit, weapon, hands=True):
		data = Weapons.array[weapon]
		player = True if unit.name == "you" else False

		if player:
			# Manage Brand + Probability
			try: brand = data[8]
			except IndexError: brand = None
			try: prob = data[9]
			except IndexError: prob = None

			if hands: unit.hands -= data[3]

			# Create Weapon Object
			if data[2] in Weapons.ranged_wclasses and data[3] > 0:
				unit.inventory.append( Weapon(self.game, weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], None, brand, prob))
				weapon = unit.inventory[-1]
			else:
				unit.wielding.append( Weapon(self.game, weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], None, brand, prob))
				weapon = unit.wielding[-1]


		else:
			# Manage Enchantment
			spawned_enchantment = data[4]
			if d(10) + (1.5 * unit.tier) > 13: spawned_enchantment += d(int(max(1, unit.tier / 2))) - 1

			# Manage Brand + Probability
			try: brand = data[8]
			except:
				if d(100) > 99 - unit.tier and data[3] > 0 and weapon not in Weapons.legendaries:
					brand = Brands.weapon_brands[d(len(Brands.weapon_brands)) - 1]
				else: brand = None
			try: prob = data[9]
			except: prob = None

			# Create Weapon Object
			unit.wielding.append( Weapon(weapon, data[0], data[1], data[2], data[3], spawned_enchantment, data[5], data[6], data[7], None, brand, prob))
			weapon = unit.wielding[-1]

		try: self.game.legendaries_to_spawn.remove(weapon.base_string)
		except: pass

		return weapon
