from Maps import Maps

from bestiary import Monsters
from codex import Weapons, Ammos, Brands, Shields
from Spells import Spells
from Descriptions import Descriptions
from Colors import Colors
from ai import *
from Shield import Shield

def apply(unit, passive, count, stacking=False):

	for present_passive in unit.passives:

		if present_passive[0] == passive:
			if stacking: present_passive[1] += count
			else: present_passive[1] = count
			return

	unit.passives.append([passive, count])


class Weapon:

	def __init__(self,  game, name, rep, color_tone, wclass, hands, enchantment, damage, to_hit, speed,   loc, brand=None, probability=None):

		self.game = game

		# Initialize Weapon Stats
		self.rep, self.color, self.wclass, self.hands, self.enchantment, self.damage, self.to_hit, self.speed, self.loc, self.brand, self.origbrand, self.probability = rep, color_tone, wclass, hands, enchantment, damage, to_hit, speed, loc, brand, brand, probability

		# Initialize Passives, kills
		self.passives, self.kills = [], 0

		# Initiate names, info
		self.name, self.base_string = Colors.color(name, self.color), name

		# Spell Damage
		self.mdamage = 1 if wclass in {'staff'} else 0

		# Deal with prob
		if self.probability is None: self.probability = 100

		# Ranged Brands
		if self.wclass in Weapons.ranged_wclasses:
			self.range = 2 * damage + to_hit
			self.brand = None
		if self.wclass in Ammos.thrown_amclasses:
			self.range = 2 * damage + to_hit

		# Legendary
		self.legendary = True if self.base_string in Weapons.legendaries else False

		self.thrown = False

	@staticmethod
	def give_weapon(unit, weapon, hands=True, brand=None, enchantment=0):
		data = Weapons.array[weapon]

		# Manage Brand + Probability
		try: brand = data[8]
		except IndexError: pass
		try: prob = data[9]
		except IndexError: prob = None

		enchantment = enchantment + data[4]

		weapon = Weapon(unit.game, weapon, data[0], data[1], data[2], data[3], enchantment, data[5], data[6], data[7], None, brand, prob)
		if hands < data[3] and hands:
			unit.inventory.append(weapon)
		else:
			if hands: unit.hands -= data[3]
			unit.wielding.append(weapon)
		return weapon

	@staticmethod
	def make_weapon(weapon, game):
		data = Weapons.array[weapon]

		# Manage Brand + Probability
		try: brand = data[8]
		except IndexError: brand = None
		try: prob = data[9]
		except IndexError: prob = None

		# Create Weapon Object
		return Weapon(game, weapon, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], None, brand, prob)

	def details(self):

		if self.to_hit >= 0: to_hit = '+' + str(self.to_hit)
		else: to_hit = str(self.to_hit)

		print(self, ' (' + self.wclass + ')')
		print("")
		print("This weapon is " + str(self.hands) + "-handed.")
		print("Base damage:", str(self.damage) + ',', "Base to-hit:", to_hit)
		if self.wclass in Weapons.ranged_wclasses: print("Range:",self.range)
		print("Swing speed:", self.speed)
		print("")

		if self.legendary:
			print(Descriptions.legendary[self.base_string])
			print("")

		print(Descriptions.wclass[self.wclass][0])
		if self.wclass[-1] != 's': print("Being a " + self.wclass + ', ' + Descriptions.wclass[self.wclass][1].lower())
		else: print("Being " + self.wclass + ', ' + Descriptions.wclass[self.wclass][1].lower())
		if self.brand is not None:
			print("")
			print(Descriptions.brand[self.brand])
		if self.kills != 1: print("You have slain",str(self.kills),"enemies with this weapon.")
		else: print("You have slain",str(self.kills),"enemy with this weapon.")

	def __str__(self):

		enchantment_string = "+" + str(self.enchantment) if self.enchantment >= 0 else str(self.enchantment)

		if self.brand is not None:
			if self.base_string[:4].lower() == 'the ': return Colors.color(self.base_string[:4], self.color) + Colors.color(self.brand, Brands.colors[self.brand]) + " " + enchantment_string + ' ' + Colors.color(self.base_string[4:], self.color)
			else: return Colors.color(self.brand, Brands.colors[self.brand]) + " " + enchantment_string + ' ' + self.name
		else:
			if self.base_string[:4].lower() == 'the ': return Colors.color(self.base_string[:4], self.color) + enchantment_string + ' ' + Colors.color(self.base_string[4:], self.color)
			else: return enchantment_string + ' ' + self.name

	def strike(self, attacker, enemy, game, firstswing=True, baal_reflect=False):


		if enemy.rider is not None:
			if d(10) >= 7 or self.wclass in {"spear","god spear","pike","lance","polearm","glaive","trident"}:
				self.strike(attacker, enemy.rider, self.game, firstswing)
				return


		brand, wclass, to_hit, brand_hit, critical = self.brand, self.wclass, self.to_hit, False, False

		# Check for enemy statuses
		frozen, marked = False, False
		for passive in enemy.passives:
			if passive[0] == "frozen": frozen = True
			if passive[0] == "marked" and wclass not in {'fist','fists'}: marked = True

		# Declare Quivered
		quivered = attacker.quivered if not baal_reflect else enemy.quivered

		# Swing Probability
		if d(100) > (100 - self.probability):

			# Manage the Trident of Atlas
			if self.base_string == "the Trident of Atlas" and firstswing:

				spaces, affected = [], []
				for x in range(-3, 4):
					for y in range(-3, 4):
						if x != 0 or y != 0: spaces.append((max(0, attacker.loc[0] + x), max(0, attacker.loc[1] + y)))

				# Find units affected
				for other_unit in game.units:
					if other_unit.loc in spaces and other_unit != attacker: affected.append(other_unit)

				delta = [attacker.loc[0] - enemy.loc[0], attacker.loc[1] - enemy.loc[1]]
				hit = ""

				for affected_unit in affected:

					if affected_unit == enemy: continue
					if self.game.map.can_move((affected_unit.loc[0] - 2*delta[0], affected_unit.loc[1] - 2*delta[1])):
						affected_unit.loc = (affected_unit.loc[0] - 2*delta[0], affected_unit.loc[1] - 2*delta[1])
					elif self.game.map.can_move((affected_unit.loc[0] - delta[0], affected_unit.loc[1] - delta[1])):
						affected_unit.loc = (affected_unit.loc[0] - delta[0], affected_unit.loc[1] - delta[1])

					if affected_unit.name == 'you':
						if len(hit) == 0: hit += "you"
						else: hit += ", you"
					else:
						if len(hit) == 0: hit += "the " + affected_unit.name
						else: hit += ", the " + affected_unit.name

				if hit != "": self.game.after_hit.append("Seaward winds from " + self.name + " blow away " + hit + "!")


			# Weapon Swing
			if firstswing: self.weapon_type_swing(attacker, enemy)

			# Calc Encumbrance
			self_encumb, enemy_encumb = attacker.equipped_armor.encumbrance, enemy.equipped_armor.encumbrance

			for item in attacker.wielding:
				if type(item) == Shield: self_encumb += item.encumbrance
			for item in enemy.wielding:
				if type(item) == Shield: enemy_encumb += item.encumbrance

			# Blessed Iron Passive
			for passive in attacker.passives:
				if passive[0] == "blessed iron":
					self_encumb = min(0, self_encumb)
					to_hit = max(0, to_hit)
			for passive in enemy.passives:
				if passive[0] == "blessed iron": enemy_encumb = min(0, enemy_encumb)


			# TO HIT formula / Manage Godfinger / Manage Baal's Generator 4
			if (d(100) + (4 * (attacker.dex - enemy.dex)) + (2 * to_hit) + self.enchantment > 40 + 1.5 * (self_encumb - enemy_encumb)) or frozen or self.base_string == "Godfinger" or baal_reflect:

				# Keep projectiles
				if self.hands > 0 and self.wclass in Weapons.ranged_wclasses or self.wclass in Ammos.thrown_amclasses:
					already_in = False
					for item in enemy.inventory:
						if quivered.same_value(item):
							item.number += 1
							already_in = True
							break
					# Quivereds are same lol
					if enemy.quivered is not None:
						if quivered.same_value(enemy.quivered):
							enemy.quivered.number += 1
							already_in = True

					if not already_in: enemy.inventory.append(quivered.one_ammo())
					# if not already_in: enemy.inventory.append(Ammo(quivered.base_string,quivered.rep,quivered.color,quivered.wclass,1,quivered.damage,None,quivered.brand))

				# Shield Block

				# Dagger passive
				if wclass not in {'dagger','knife','scream'}:
					for weapon in enemy.wielding:
						if type(weapon) == Shield:

							# Block Chance / Manage Baal's Generator 1
							if d(100) > max(50, 90 - (3 * weapon.armor_rating)) or (wclass in Weapons.ranged_wclasses and weapon.base_string == "Baal's Generator"):

								# Manage the Gauntlets of Mars
								if self.base_string == "the Gauntlets of Mars":
									damage = int(d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC() ) )

									# Stun
									apply(enemy, 'stunned', 1)

									# Manage runic Armor
									if enemy.equipped_armor.brand == 'runic' and enemy.mana > 0:
										mana_damage = min(enemy.mana, damage)
										enemy.mana -= mana_damage
										enemy.hp -= damage - mana_damage
									else:
										# Resolve Damage
										enemy.hp -= damage

									# Flavor Text
									if attacker.name != "you": self.game.game_log.append("You smash through " + enemy.info[1] + " shield with " + self.name + ", dealing " + str(damage) + " damage and " + Colors.color("stunning","magenta") + " it!")
									else: self.game.game_log.append(attacker.info[3] + " smashes through " + attacker.info[1] + " shield with " + self.name + ", dealing " + str(damage) + " damage and " + Colors.color("stunning","magenta") + " " + enemy.info[0] + "!")
									return

								# Manage Kraken 3
								if self.base_string == "Kraken" and self.thrown:
									self.loc = enemy.loc
									self.game.items.append(self)
									attacker.wielding.remove(self)
									if attacker.name == 'you': attacker.hands += 1


								# Block Statement

								# Legendary shield
								if not weapon.legendary:
									if attacker.name != 'you': poss = "your "
									else: poss = "its "
								else: poss = ""
								if attacker.name != "you": self.game.game_log.append("You block " + attacker.info[1] + " " + self.name + " with " + poss + weapon.name + "!")
								else:
									if self.legendary: self.game.game_log.append(enemy.info[3] + " blocks " + self.name + " with " + poss + weapon.name + "!")
									else: self.game.game_log.append(enemy.info[3] + " blocks " + attacker.info[1] + " " + self.name + " with " + poss + weapon.name + "!")

								# Manage Baal's Generator 2
								if weapon.base_string == "Baal's Generator" and wclass in Weapons.ranged_wclasses and d(100) >= 66:
									self.strike(enemy, attacker, game, firstswing, baal_reflect=True)

								return


				# DAMAGE Formula


				# Projectile weapon
				if self.wclass in Weapons.ranged_wclasses and self.hands > 0:
					damage = max(0, int(d(self.damage) + d(quivered.damage) + attacker.dex / 2 + self.enchantment - ( 0.75 * enemy.calc_AC())))
					brand, wclass = quivered.brand, quivered.wclass
				# Thrown Weapon
				elif self.wclass in Ammos.thrown_amclasses and self.hands > 0:
					damage = max(0, int(d(self.damage) + d(quivered.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC())))
					brand, wclass = quivered.brand, quivered.wclass
				# Manage Kraken 6
				elif self.base_string == 'Kraken' and self.thrown:
					damage = max(0, int(d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC())))
				# Melee weapon / Manage Invictus 2
				else:
				# elif self.base_string in Weapons.array or self.base_string == "Invictus":
					# Manage Runed weapon
					if brand == 'runed': damage = max(0, int(d(self.damage) + attacker.str / 1.5 + self.enchantment))
					# REGULAR MELEE HIT
					elif self.base_string == "Skullrazor": damage = max(0, int(d(self.damage) + attacker.str / 1.5 + self.enchantment))
					# Manage demon sword
					elif self.wclass in {'demon sword'}: damage = max(0, int(d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.50 * enemy.calc_AC())))
					# Manage scream
					elif self.wclass in {'scream'}: damage = max(0, int(d(self.damage) + attacker.cha / 1.5 + self.enchantment))
					# REGULAR MELEE HIT
					else: damage = max(0, int(d(self.damage) + attacker.str / 1.5 + self.enchantment - ( 0.75 * enemy.calc_AC())))

					# Manage Deadly Precision
					if 'deadly precision' in attacker.traits:
						if d(100) >= 99 and self.wclass not in {'knife','dagger'} or d(100) >= 97 and self.wclass in {'knife','dagger'}:
							damage *= 3
							critical = True

					# Managed Spiked Armor
					if enemy.equipped_armor.brand == 'spiked' and damage > 0 and d(10) > 3: barb_damage = d(max(1, int(1/2 * damage)))

				# Marked passive
				if marked:
					damage = int(self.damage + attacker.str + self.enchantment - ( 0.5 * enemy.calc_AC()))
					for passive in enemy.passives:
						if passive[0] == 'marked': enemy.passives.remove(passive)
						if brand == "vorpal": damage *= 2
						break


				# Calc Resistances
				frostr, firer, poisonr, acidr, shockr, expr = enemy.calc_resistances()

				# Manage God-Cleaver 1
				if self.base_string == 'God-Cleaver': enemy.god_cleaver_hits += 1

				# Apply Brands and resistances
				if not critical:
					if brand == "envenomed": brand_hit = d(100) > 50 and d(4) > poisonr
					elif brand == "flaming":
						# Manage Dawn
						if self.base_string == 'Dawn': brand_hit = d(6) > firer
						else: brand_hit = d(100) > 60 and d(4) > firer
					elif brand == "electrified":
						# Manage Mjölnir 1
						if self.base_string == "Mjölnir": brand_hit = d(100) > 30 and d(6) > shockr
						else: brand_hit = d(100) > 40 and d(4) > shockr
					elif brand == "soulflame": brand_hit = True if d(100) > 65 and "evening rites" not in enemy.traits else False
					elif brand == "frozen": brand_hit = d(100) > 80 and d(4) > frostr
					elif brand == "antimagic": brand_hit = True if len(enemy.spells) > 0 else False
					elif brand == "possessed": brand_hit = d(100) > 80
					elif brand == "vorpal": brand_hit = True if len(enemy.passives) != 0 else False
					elif brand == "holy":
						if enemy.name != 'you': brand_hit = True if enemy.etype in Monsters.holy_vulnerable else False
						else: brand_hit = True if enemy.race in {"Demonkin","Dhampir"} else False
					elif brand == "silvered":
						if enemy.name != 'you': brand_hit = True if enemy.etype in Monsters.silver_vulnerable else False
						else: brand_hit = True if enemy.race in {"Ghoul","Dhampir"} else False
					elif brand == "vampiric":
						if enemy.name != 'you': brand_hit = False if enemy.etype in Monsters.dont_bleed or "evening rites" in enemy.traits else True
						else: brand_hit = False if enemy.race in {"Dread"} or "evening rites" in enemy.traits else True
					elif brand == "runed":
						brand_hit = False
						if attacker.mana >= self.damage / 2:
							attacker.mana -= int(self.damage / 2)
							brand_hit = True
					elif brand == "hellfire": brand_hit = True if "evening rites" not in enemy.traits else False
					elif brand is not None: brand_hit = True


					# Manage Dominus
					for weapon in enemy.wielding:
						if weapon.base_string == "Dominus":
							brand_hit = False
							break


				# Apply Brands
				if not marked and damage > 0 and brand_hit: damage = self.apply_brands(attacker, enemy, damage, brand)


				# Weapon class effects
				damage = self.weapon_type_effect(attacker, enemy, damage)

				# Marked
				if marked:
					verb, preposition = Weapons.weapon_classes[wclass]
					if attacker.name != "you": self.game.game_log.append(attacker.info[3] + " ignites " + enemy.info[1] + " mark with its " + wclass + ", tearing " + enemy.info[1] + " body apart for " + str(damage) + " damage!")
					else: self.game.game_log.append("You ignite the " + enemy.info[1] + " mark with your " + wclass + ", tearing its body apart for " + str(damage) + " damage!")

				# Manage Baal's Generator 3
				elif baal_reflect:
					self.game.game_log.append(Colors.color("Baal's Generator", Shields.array["Baal's Generator"][1]) + " reflects the " + quivered.name + " back at " + enemy.info[0] + ", dealing " + str(damage) + " damage!")

				# No damage case
				elif damage <= 0:
					damage = 0

					if attacker.name != "you": self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " with its " + wclass + " but does no damage!")
					else: self.game.game_log.append("You " + Weapons.weapon_classes[wclass][0] + " your " + str(wclass) + " " + Weapons.weapon_classes[wclass][1] + " " + enemy.info[0] + " but deal no damage!")

				# Damage Case - Statement
				else: self.damage_statement(attacker, enemy, damage, brand, brand_hit, critical, quivered)

				# Check passives
				if brand_hit:
					for passive in self.passives:
						passive[1] -= 1

						if passive[1] == 0:
							self.passives.remove(passive)
							self.brand = self.origbrand


				# Manage the Blasting Rod
				if self.base_string == 'the Blasting Rod':
					Spells.thunderbolt("thunderbolt",attacker, enemy, game, map, game.room_filler, verbose=False)

				# Manage runic Armor
				if enemy.equipped_armor.brand == 'runic' and enemy.mana > 0:
					mana_damage = min(enemy.mana, damage)
					enemy.mana -= mana_damage
					enemy.hp -= damage - mana_damage
				else:
					# Resolve Damage
					enemy.hp -= damage

				# Manage Spiked
				try:
					self.game.game_log.append(enemy.info[4] + ' spikes deal ' + str(barb_damage) + ' damage back to ' + attacker.info[0] + '!')

					# Manage runic Armor
					if attacker.equipped_armor.brand == 'runic' and attacker.mana > 0:
						mana_damage = min(attacker.mana, barb_damage)
						attacker.mana -= mana_damage
						attacker.hp -= barb_damage - mana_damage
					else:
						# Resolve Damage
						attacker.hp -= barb_damage

						# Manage Bloodshell
						if enemy.equipped_armor.base_string == "Bloodshell":
							health_back = d(barb_damage)
							enemy.hp = min(enemy.maxhp, enemy.hp + health_back)
							self.game.game_log.append(enemy.equipped_armor.name + " collects the blood and heals " + enemy.info[0] + " for " + str(health_back) + " health!")

					# Check if unit is still alive
					if attacker.name != "you":
						self.game.player.well_being_statement(attacker, enemy, "spikes", estatus=False)

				except: pass

				# Manage Possessed
				if brand == "possessed" and brand_hit: self.strike(attacker, enemy, self.game)

				# Manage the Phasic Robes
				if enemy.equipped_armor.base_string == "the Phasic Robes" and self.wclass not in Weapons.ranged_wclasses:
					Spells.blink("blink", enemy, enemy, self.game, Maps.rooms[self.game.map.map][0], self.game.map.room_filler)

				# Manage God-Frame
				if enemy.equipped_armor.base_string == "God-Frame" and self.wclass not in Weapons.ranged_wclasses and d(100) >= 90:
					# Stun
					apply(attacker, 'stunned', 1)
					self.game.game_log.append(enemy.equipped_armor.name + " unleashes a shockwave of energy that " + Colors.color("stuns","magenta") + " " + attacker.info[0] + "!")



				# Manage the Singing Spear
				if self.base_string == "the Singing Spear" and d(100) >= 75:

					brands = ["flaming","frozen","envenomed","hellfire","soulflame","vampiric","electrified","vorpal","holy","runed","possessed"]
					verbs = ["whistles","sings","shouts","whispers","belts","hums"]
					types = ["sweet","brisk","harsh","soft","crashing","melodic","thundering"]

					self.brand = brands[d(len(brands)) - 1]
					self.color = Brands.colors[self.brand]
					self.name = Colors.color(self.base_string, Brands.colors[self.brand])
					self.game.game_log.append(self.name + " " + verbs[d(len(verbs)) - 1] + " a " + types[d(len(verbs)) - 1] + " melody.")

				# Manage Kraken 2
				if self.base_string == 'Kraken' and self.thrown:
					enemy.inventory.append(self)
					attacker.wielding.remove(self)
					if attacker.name == 'you': attacker.hands += 1



				# Check to see who weapon killed
				for unit in self.game.units[1:]:
					if unit == attacker: continue
					if baal_reflect: self.game.player.well_being_statement(unit, attacker, self, estatus=False)
					else: self.game.player.well_being_statement(unit, attacker, self, estatus=False)

			# Miss Case
			else:

				# Manage Kraken 4
				if self.base_string == "Kraken" and self.thrown:
					self.loc = enemy.loc
					self.game.items.append(self)
					attacker.wielding.remove(self)
					if attacker.name == 'you': attacker.hands += 1

				# Manage blades
				counter = None
				for weapon in enemy.wielding:
					if type(weapon) == Weapon:
						if weapon.wclass in {"sword","bastard sword","demon sword","god sword"} and self.wclass not in Weapons.ranged_wclasses:

							# Manage Nightsbane
							if weapon.base_string == "Nightsbane":
								if attacker.name != 'you':
									if attacker.etype in Monsters.silver_vulnerable: counter = weapon
								else:
									if attacker.race in {"Ghoul"}: counter = weapon
							else:
								# Normal Counter chance
								if d(100) + 3 * enemy.dex > 75: counter = weapon

				if firstswing:

					# Miss statement
					if self.wclass in Weapons.ranged_wclasses:
						if attacker.name != "you": self.game.game_log.append(attacker.info[3] + " shoots at " + enemy.info[0] + " with its " + self.wclass + " but misses.")
						else: self.game.game_log.append("You closely miss " + enemy.info[0] + " with your " + self.wclass + "!")
					elif self.wclass in Ammos.thrown_amclasses:
						if attacker.name != "you": self.game.game_log.append(attacker.info[3] + " hurls a " + self.wclass + " at " + enemy.info[0] + " but misses.")
						else: self.game.game_log.append("You closely miss " + enemy.info[0] + " with your " + self.wclass + "!")
					else:
						if attacker.name != "you": self.game.game_log.append(attacker.info[3] + " swings at " + enemy.info[0] + " with its " + self.wclass + " but misses.")
						else: self.game.game_log.append("You closely miss " + enemy.info[0] + " with your " + self.wclass + "!")

				# Riposte with blade
				if counter is not None:
					damage = int(d(int(counter.damage * 0.75)) + attacker.str / 1.5 + counter.enchantment - ( 0.75 * attacker.calc_AC()))
					if damage > 0:

						# Manage Bloodreaver
						if counter.base_string == "Bloodreaver":
							# Apply Effect
							apply(attacker, 'marked', 10)

							if attacker.name != "you": self.game.game_log.append("You counter " + attacker.info[0] + " with " + counter.name + " for " + str(damage) + " damage and mark it with a " + Colors.color("black mark","darkred") + "!")
							else: self.game.game_log.append(enemy.info[3] + " counters " + attacker.info[0] + " with " + counter.name + " for " + str(damage) + " damage and marks you with a " + Colors.color("black mark","darkred") + "!")
						else:
							if attacker.name != "you": self.game.game_log.append("You counter " + attacker.info[0] + " with your blade for " + str(damage) + " damage!")
							else: self.game.game_log.append(enemy.info[3] + " counters " + attacker.info[0] + " with its blade for " + str(damage) + " damage!")

						# Manage runic Armor
						if attacker.equipped_armor.brand == 'runic' and attacker.mana > 0:
							mana_damage = min(attacker.mana, damage)
							attacker.mana -= mana_damage
							attacker.hp -= damage - mana_damage
						else:
							# Resolve Damage
							attacker.hp -= damage
						if enemy.name == 'you':
							try: self.game.player.well_being_statement(attacker, game.player, counter, estatus=False)
							except: pass

			# Add back after statement
			if len(self.game.after_hit) != 0:
				for line in self.game.after_hit: self.game.game_log.append(line)
				self.game.after_hit = []


	def weapon_type_swing(self, attacker, enemy):

		# CLEAVE ATTACK
		if self.wclass in {"greatsword","god sword","bastard sword","scythe","greataxe","god axe","claw gauntlets"}:

			# CLEAVE Attack
			# --START--------------------------------
			y = attacker.loc[0] - enemy.loc[0]
			x = attacker.loc[1] - enemy.loc[1]

			for unit in self.game.units:
				cleave = False

				# Horizontal Case
				if x == 0:
					if unit.loc == (enemy.loc[0], enemy.loc[1] + 1):
						self.strike(attacker, unit, self.game, firstswing=False)
						cleave = True
					if unit.loc == (enemy.loc[0], enemy.loc[1] - 1):
						self.strike(attacker, unit, self.game, firstswing=False)
						cleave = True
					if self.wclass == 'scythe':
						if unit.loc == (attacker.loc[0], enemy.loc[1] + 1):
							self.strike(attacker, unit, self.game, firstswing=False)
						if unit.loc == (attacker.loc[0], enemy.loc[1] - 1):
							self.strike(attacker, unit, self.game, firstswing=False)

				# Vertical Case
				elif y == 0:
					if unit.loc == (enemy.loc[0] + 1, enemy.loc[1]):
						self.strike(attacker, unit, self.game, firstswing=False)
						cleave = True
					if unit.loc == (enemy.loc[0] - 1, enemy.loc[1]):
						self.strike(attacker, unit, self.game, firstswing=False)
						cleave = True
					if self.wclass == 'scythe':
						if unit.loc == (enemy.loc[0] + 1, attacker.loc[1]):
							self.strike(attacker, unit, self.game, firstswing=False)
						if unit.loc == (enemy.loc[0] - 1, attacker.loc[1]):
							self.strike(attacker, unit, self.game, firstswing=False)

				# Corner case
				else:
					if unit.loc == (enemy.loc[0] + y, enemy.loc[1]):
						self.strike(attacker, unit, self.game, firstswing=False)
						cleave = True
					if unit.loc == (enemy.loc[0], enemy.loc[1] + x):
						self.strike(attacker, unit, self.game, firstswing=False)
						cleave = True
					if self.wclass == 'scythe':
						if unit.loc == (enemy.loc[0] + 2*y, enemy.loc[1]):
							self.strike(attacker, unit, self.game, firstswing=False)
						if unit.loc == (enemy.loc[0], enemy.loc[1] + 2*x):
							self.strike(attacker, unit, self.game, firstswing=False)

			if not cleave and self.wclass in {'greatsword','god sword'} and unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])): self.strike(attacker, unit, self.game, False)
			# --END------------------------------------


		elif self.wclass in {"spear","polearm","lance","glaive","trident"}:
			for unit in self.game.units:
				if unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, self.game, firstswing=False)
					break



		elif self.wclass in {"pike","god spear"}:
			for unit in self.game.units:
				if unit.loc == (attacker.loc[0] - 2 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 2 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, self.game, firstswing=False)
				elif unit.loc == (attacker.loc[0] - 3 * (attacker.loc[0] - enemy.loc[0]), attacker.loc[1] - 3 * (attacker.loc[1] - enemy.loc[1])):
					self.strike(attacker, unit, self.game, firstswing=False)


	def weapon_type_effect(self, attacker, enemy, damage):


		# Blunt weapons
		if self.wclass in {"hammer","club","mace","flail","gauntlet","maul"}:
			if enemy.equipped_armor.aclass == 'plate': damage *= 1.4

		elif self.wclass in {"warhammer","greatclub","god hammer","fists","gauntlets"}:
			if enemy.equipped_armor.aclass == 'plate': damage *= 1.4

			# Stun
			if d(100) >= 65: apply(enemy, 'stunned', 1)

		elif self.wclass in {"greataxe","god axe","axe","claw gauntlet","claw gauntlets"}:
			damage *= (1 + max(0, (0.25 - enemy.calc_AC() / 50)))

		return int(damage)


	def apply_brands(self, attacker, enemy, damage, brand):

		# Manage Flaming
		if brand == "flaming": apply(enemy, 'aflame', Brands.dict["flaming"]["count"])

		# Manage soulflame
		elif brand == "soulflame": apply(enemy, 'drained', Brands.dict["drained"]["count"])

		# Manage Vampiric
		elif brand == "vampiric":

			# Manage Krog's Maw
			if self.base_string == "Krog's Maw":
				heal = int(damage / 3)
				if attacker.hp <= attacker.maxhp < attacker.hp + heal: self.game.after_hit.append(self.name + " grants " + attacker.name + " a shield of blood.")
				attacker.hp = min(int(attacker.maxhp * 1.2), attacker.hp + heal)
			else:
				# heal
				attacker.hp = min(attacker.maxhp, attacker.hp + int(damage / 3))

		# Manage Hellfire
		elif brand == "hellfire": damage += int((1 - (enemy.hp / enemy.maxhp)) * damage * 0.5)

		# Manage Envenomed
		elif brand == "envenomed":
			# Manage Splinter
			count = 3 if self.base_string == 'Splinter' else Brands.dict["envenomed"]["count"]

			apply(enemy, 'poisoned', count, stacking=True)

		# Manage Silvered
		elif brand == "silvered": damage *= 1.6

		# Manage Holy
		elif brand == "holy": damage *= 1.8

		# Manage Antimagic
		elif brand == "antimagic": damage *= 1.7

		# Manage Electrified
		elif brand == "electrified":

			# Manage Mjölnir 2
			if self.base_string == "Mjölnir":

				# Shock Radius
				def shock(target, affected=[]):
					if target in affected: return
					affected.append(target)
					spaces = set([])
					for x in range(-1,2):
						for y in range(-1,2):
							if target.loc[0] + x >= 0 and target.loc[1] + y >= 0: spaces.add((target.loc[0] + x, target.loc[1] + y))
					# Find units affected
					for other_unit in self.game.units:
						if other_unit.loc in spaces and target != other_unit and other_unit not in affected and other_unit != attacker: shock(other_unit, affected)
					return affected[1:]

				affected = shock(enemy)
				# Hit string
				hit = ""
				thunder_damage = md(enemy.tier,3)
				for unit in affected:

					# Shock Resist
					if d(5) <= enemy.calc_resistances()[4]: continue

					unit.hp -= thunder_damage
					if unit.name == 'you':
						if len(hit) == 0: hit += "you"
						else: hit += ", you"
					else:
						if len(hit) == 0: hit += "the " + unit.name
						else: hit += ", the " + unit.name

				flavor = " each" if len(affected) > 1 else ""

				if hit != "": self.game.after_hit.append(self.name + " smites " + hit + " with " + Colors.color("godly thunder","yellow") + flavor + " for " + str(thunder_damage) + " damage!")

			else:
				if attacker.name == 'you': damage += md(attacker.level,2)
				else: damage += md(attacker.tier,2)

		# Manage Vorpal
		elif brand == "vorpal":

			damage += int(len(enemy.passives) * enemy.maxhp / 5)
			self.game.check_passives(enemy, purge=True)


		# Manage Frozen
		elif brand == "frozen": apply(enemy, 'frozen', Brands.dict["frozen"]["count"], stacking=True)

		# Return DAMAGE
		return damage


	def damage_statement(self, attacker, enemy, damage, brand, brand_hit, critical, quivered):
		name, wclass = self.name, self.wclass

		if self.wclass in Weapons.ranged_wclasses and self.hands > 0: name, wclass = quivered.name, quivered.wclass

		# Manage legendary and unique
		name = name if self.legendary else "its " + name

		# Make the sentence awesome
		verb, preposition = Weapons.weapon_classes[wclass]

		# Manage the Glaive of Gore
		if self.base_string == "the Glaive of Gore" and d(100) >= 9:

			enemy.str -= Brands.dict['disemboweled']['strred']
			apply(enemy, 'disemboweled', 3)

			# ------------------------
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " disembowels " + enemy.info[0] + " with " + name + " for " + str(damage) + " damage!")
			else:
				self.game.game_log.append("You disembowel " + enemy.info[0] + " with " + name + " for " + str(damage) + " damage and weaken it!")

		# Manage God-Cleaver 2
		elif self.base_string == "God-Cleaver" and enemy.god_cleaver_hits == 4:
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + ", its blade glows red!")
			else:
				self.game.game_log.append("You " + verb + " " + name + " " + preposition + " " + enemy.info[0] + " for " + str(damage) + " damage, your blade glows red!")

		# Manage God-Cleaver 3
		elif self.base_string == "God-Cleaver" and enemy.god_cleaver_hits == 5:
			if attacker.name != "you":
				self.game.game_log.append("With a clean sweep " + attacker.info[0] + " cleaves off " + enemy.info[1] + " head!")
			else:
				self.game.game_log.append("With a clean sweep you cleave off " + enemy.info[1] + " head with " + name + "!")
			enemy.hp = 0

		# Manage Kraken 5
		elif self.base_string == "Kraken" and self.thrown:
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " throws " + name + " into " + enemy.info[0] + " for " + str(damage) + " damage with!")
			else:
				self.game.game_log.append("You throw " + name + " into " + enemy.info[0] + " for " + str(damage) + " damage!")

		# critical Strike
		elif critical:
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " deftly strikes " + enemy.info[1] + " vital point with " + name + ", dealing " + str(damage) + " damage!")
			else:
				self.game.game_log.append("You deftly " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[1] + " vital point, dealing " + str(damage) + " damage!")

		# Regular hit
		elif brand is None or not brand_hit:
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + "!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + " for " + str(damage) + " damage!")

		elif brand == "holy":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + Colors.color("holy","bone") + " " + name + " and smites " + enemy.info[0] + " down!")
			else:
				self.game.game_log.append("You smite " + enemy.info[0]+ " with your " + Colors.color("holy","bone") + " "+ str(wclass) + " for " + str(damage) + " damage!")

		elif brand == "silvered":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + ", its " + Colors.color("silver","steel") + " burns " + enemy.info[0] + "!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + ", the " + Colors.color("silver","steel") + " burns for " + str(damage) + " damage!")

		elif brand == "electrified":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + " and " + fg.yellow + "shocks" + fg.rs + " " + enemy.info[0] + "!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + " and " + fg.yellow + "shock" + fg.rs + " it for " + str(damage) + " damage!")

		elif brand == "antimagic":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + ", " + enemy.info[1] + " mana " + fg.magenta + "burns" + fg.rs + " inside!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + ", its mana " + fg.magenta + "burns" + fg.rs + " for " + str(damage) + " damage!")

		elif brand == "vampiric":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + " and " + Colors.color("drains","red") + " " + enemy.info[1] + " life!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + ", dealing " + str(damage) + " damage and " + Colors.color("draining","red") + " its life!")

		elif brand == "flaming":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + " and sets " + enemy.info[0] + " " + Colors.color("aflame","fire") + "!")
			else:
				self.game.game_log.append("You " + verb + " your "+ str(wclass) + " " + preposition + " " + enemy.info[0] + ", dealing " + str(damage) + " damage and setting it " + Colors.color("aflame","fire") + "!")
		elif brand == "runed":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " " + Colors.color("empowered","lightblue") + " damage with " + name + "!")
			else:
				self.game.game_log.append("You " + verb + " your " + Colors.color("crackling","lightblue") + " " + str(wclass) + " " + preposition + " " + enemy.info[0] + " to deal an empowered " + str(damage) + " damage!")
		elif brand == "soulflame":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + " and saps " + enemy.info[1] + " will!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + ", dealing " + str(damage) + " damage and sapping its will!")
		elif brand == "possessed":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[4] + " " + name + " lashes out ravenously at " + enemy.info[0] + " for " + str(damage) + " damage!")
			else:
				self.game.game_log.append("Your " + str(wclass) + " lashes out ravenously at " + enemy.info[0] + ", dealing " + str(damage) + " damage!")

		elif brand == "frozen":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + " and " + fg.cyan + "freezes" + fg.rs + " " + enemy.info[0] + "!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + ", dealing " + str(damage) + " damage and " + fg.cyan + "freezing" + fg.rs + " it!")

		elif brand == "hellfire":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + " and " + Colors.color("burning","orange") + " " + enemy.info[1] + " soul!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + ", dealing " + str(damage) + " damage and " + Colors.color("burning","orange") + " its soul!")

		elif brand == "vorpal":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[4] + " " + Colors.color("vorpal","purple") + " weapon ignites " + enemy.info[1] + " status effects with " + name + " and deals " + enemy.info[0] + " " + str(damage) + " damage!")
			else:
				self.game.game_log.append("You " + verb + " your " + Colors.color("vorpal","purple") + " " + str(wclass) + " " + preposition + " " + enemy.info[0] + " and ignite its status effects for " + str(damage) + " damage!")

		elif brand == "envenomed":
			if attacker.name != "you":
				self.game.game_log.append(attacker.info[3] + " hits " + enemy.info[0] + " for " + str(damage) + " damage with " + name + " and " + Colors.color("poisons","green") + " " + enemy.info[0] + "!")
			else:
				self.game.game_log.append("You " + verb + " your " + str(wclass) + " " + preposition + " " + enemy.info[0] + ", dealing " + str(damage) + " damage and " + Colors.color("poisoning","green") + " it!")
