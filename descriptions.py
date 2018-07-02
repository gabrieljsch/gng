

class Colors():

	array = {
		'red' : ('rgb', (255, 10, 10)),
		'orange' : ('rgb', (255, 150, 50)),
		'fire' : ('rgb', (255,69,0)),
		'green' : ('rgb', (50, 205, 50)),
		'darkgreen' : ('rgb', (0,128,0)),
		'yellow' : ('rgb', (255,255,0)),
		'gold' : ('rgb', (212,175,55)),
		'cyan' : ('rgb', (0,255,255)),
		'blue' : ('rgb', (0,0,255)),
		'lightblue' : ('rgb', (65,105,225)),
		'brown' : ('rgb', (139,69,19)),
		'darkbrown' : ('rgb', (84,42,14)),
		'tan' : ('rgb', (205,133,63)),
		'grey' : ('rgb', (105,105,105)),
		'purple' : ('rgb', (128,0,128)),
		'magenta' : ('rgb', (255,0,255)),
		'salmon' : ('rgb', (250,128,114)),
		'darkred' : ('rgb', (139,0,0)),
		'bronze' : ('rgb', (205,127,50)),
		'bone' : ('rgb', (238,232,170)),
		'steel' : ('rgb', (119,136,153)),
	}





class Descriptions():

	wclass = {
		# Weapons
		# Augmented Innate
		"fists" : ["A weapon carried in or fuzed with the hand to increase punching power."],

		# Blunt
		"hammer" : ["A blunt weapon with a flat head and a sturdy handle.","This weapon does bonus damage against enemies wearing plate armor."],
		"warhammer" : ["A large blunt weapon with a double-sided flat head and a sturdy handle.","TThis weapon does bonus damage against enemies wearing plate armor and has a chance to stun the target."],
		"club" : ["A simple blunt weapon used for smashing.","This weapon does bonus damage against enemies wearing plate armor."],
		"greatclub" : ["A simple but enormous blunt weapon used for crushing.","This weapon does bonus damage against enemies wearing plate armor and has a chance to stun the target."],
		"mace" : ["A blunt weapon with a spherical head and a sturdy handle.","This weapon does bonus damage against enemies wearing plate armor."],
		"flail" : ["A blunt weapon comprised of a spiked steel ball attached to a sturdy handle with a chain.","This weapon does bonus damage against enemies wearing plate armor."],

		# Polearm
		"spear" : ["A light polearm with a long shaft and sharp tip.","This weapon strikes the enemy behind the target on a successful hit."],
		"pike" : ["A two-handed polearm with an extremely long shaft and sharp tip.", "This weapon strikes the next two enemies behind the target on a successful hit."],
		"lance" : ["A light polearm with a pointed tip, usually used while mounted.", "This weapon strikes the enemy behind the target on a successful hit."],
		"polearm" : ["A weapon with a long shaft and sharp metal head used for chopping.", "This weapon strikes the enemy behind the target on a successful hit."],

		# Dagger
		"dagger" : ["A short, sharpened blade with a sturdy grip.","This weapon cannot be blocked by a shield."],
		"knife" : ["A short weapon with a sturdy grip and large one-sided blade.","This weapon cannot be blocked by a shield."],

		# Axe
		"axe" : ["A martial weapon with a short shaft and sharpened head.", "This weapon does increased damage to lightly armored enemies."],
		"greataxe" : ["A large martial weapon with a long shaft and heavy head.", "This weapon cleaves adjacent enemies on hits and does increased damage to lightly armored enemies."],

		# Sword
		"sword" : ["A martial weapon with a long sharp blade attached to a hilt.", "This weapon gives you a chance to counter when an enemy attack misses."],
		"demon sword" : ["A sword forged from the blood of thousands of beings.", "This weapon ignores more armor than other weapons and gives you a chance to counter when an enemy attack misses."],
		"greatsword" : ["A large martial weapon with a long blade and two-handed grip.", "This weapon cleaves adjacent enemies on hits or, if none are adjacent, strikes the enemy behind the target."],
		"bastard sword" : ["A large martial weapon with a long blade and a one-and-a-half-handed grip.", "This weapon cleaves adjacent enemies on hits and has a chance to counter when an enemy attack misses."],

		# Staff
		"staff" : ["A long rod that can be made of wood or metal.", "This weapon imparts extra spell damage to the holder."],

		# Ranged Weapons
		"bow" : ["A bent shaft with a bowstring used to launch projectiles at long distances.","This weapon can fire both arrows and bolts."],
		"crossbow" : ["A platform with a winding mechanism used to launch projectiles at high speeds.","This weapon can only fire bolts."],
		"ballista" : ["A large weapon platform, usually mounted to the floor, that launches heavy projectiles.","This weapon can fire both bolts and arrows."],
		"god bow" : ["A bent shaft with a bowstring used to launch projectiles at long distances, initially owned by a god.","This weapon can only fire arrows."],

		# Projectiles
		"arrow" : "A light projectile with a sharp tip and feathered butt.",
		"bolt" : "A short, heavier projectile that can punch through heavy armor.",
		"javelin" : "A balanced polearm with a sharp tip and a weighted butt used for throwing.",
		"stone" : "An especially round stone, perfect for throwing.",
		"throwing axe" : "A smaller, more balanced axe used for throwing.",

		# God weapons
		"god spear" : ["A polearm with a long shaft and sharp head, initially owned by a god.", "This weapon strikes the next two enemies behind the target on a successful hit."],
		"god sword" : ["A large weapon with a long blade and two-handed grip, initially owned by a god.", "This weapon can counter and cleaves adjacent enemies on hits or, if none are adjacent, strikes the enemy behind the target."],
		"god axe" :   ["A large weapon with a long shaft and heavy head, initially owned by a god.","This weapon cleaves adjacent enemies on hits and does increased damage to lightly armored enemies."],
		"god hammer" :["A large blunt weapon with a double-sided flat head and a sturdy handle, initially owned by a god.","This weapon does bonus damage against enemies wearing plate armor and has a chance to stun the target."],


		# Armors
		"garments" : "Common clothes worn in the cities.",
		"robes" : "Light armor offering the user a greater freedom of movement.",
		"hide" : "Medium armor fashioned from the skin of an animal.",
		"scale" : "Medium armor fashioned from the tough scales of a creature.",
		"chainmail" : "Tough armor fashioned from interwoven metal rings.",
		"plate" : "Extremely tough armor made of metal. Vulnerable to blunt weaponry.",

	}

	brand = {
		# Weapon
		"envenomed" : "This weapon has a chance to poison the enemy. Poison damage stacks progressively with successive strikes.",
		"flaming" : "This weapon has a chance to light enemies aflame.",
		"frozen" : "This weapon has a chance to freeze an enemy.",
		"silvered" : "This weapon deals extra damage to undead and unholy creatures.",
		"hellfire" : "This weapon deals more damage as the target's health decreases.",
		"infernal" : "This weapon has a chance to sap the dexterity of the target.",
		"vampiric" : "This weapon steals life from the target on hits.",
		"antimagic" : "This weapon deals extra damage to spellcasters.",

		# Armor
		"spiked" : "This armor has a chance to deal some physical damage back to attackers.",
		"icy" : "This armor provides moderate frost resistance to the wearer.",
		"tempered" : "This armor provides moderate fire resistance to the wearer.",
	}

	skill = {
		"poison breath" : ["You breathe a cloud of noxious gas at your enemy in hopes of poisoning them."],
		"magic missile" : ["You conjure a phantasmal arrow of energy to strike your foe at any range."],
		"combat roll" : ["Roll 2 squares across the floor, then throw a quivered throwing weapon at a random in-range enemy."],
		"chain lightning" : ["You fire wild lightning into the air at a specific target. The lightning has a chance to bounce on every unit in 2 squares."],
		"blink" : ["You can willingly translocate a random square within a short range."],
		"bless weapon" : ["You call upon your deity to bless your weapon to smite down demons and the unholy."],
		"dark bolt" : ["You blast a foe with a bolt cursed with black fire."],
		"bloodreave" : ["You set your blood on fire to burn the soul of your enemies."],
		"flash heal" : ["You call upon your deity to heal your wounds in so you may smite down your foes."],
		"raise skeleton" : ["You command a fallen warrior from centuries past to rise and fight for you."],
		"dark transformation" : ["When have been drained of enough blood, cast a ritual to tranform into a hideous abomination for a time."],
		"martial draw" : ["You swing at a random in-range enemy when you draw a weapon."],
		"furious charge" : ["You gain a mad ferocity. You strike enemies in the same direction you moved."],


	}





