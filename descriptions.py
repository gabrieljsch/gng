

class Colors():

	array = {
		'red' : ('rgb', (255, 10, 10)),
		'orange' : ('rgb', (255, 150, 50)),
		'fire' : ('rgb', (255,69,0)),
		'green' : ('rgb', (50, 205, 50)),
		'darkgreen' : ('rgb', (0,128,0)),
		'springgreen' : ('rgb', (0,250,154)),
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


	legendary = {
		# Weapons
		"the Glaive of Gore" : "",
			# 
		"Soulreaper" : "This ancient warscythe's blade glows a faint blue, indiscernible whispers are heard when wielding it. Its blade emerges from a skull on its shaft fashioned from femurs, which pulsate lightly...as if the weapon were breathing.",
			# Increasing damage with kill tiers, 6 tiers, at last tier also gains possessed brand.
		"the Singing Spear" : "This ornate spear can be heard emitting musical tones when wielded. Its broad head has eight bloodletting holes, and its sturdy wooden shaft is wrapped in faded yet colorful linen bands.",
			# Chance to change brand with every hit.
		"Gork's Maw" : "",
			# Can gain a temporary overshield with this weapon when healing over max health.
		"Splinter" : "This deadly knife is coated in black adder venom that stops the heart of its victims in seconds. Its black single-edged blade blends into the grip without a hilt to separate, and its guard is wrapped by a thin, bone-white linen cloth.",
			# Applies 3 venom stacks instead of normal 2 on brand hit.
		"Swiftspike" : "",
			# 
		"Dawn" : "This ornate shortsword glows hot-red when sheathed and bursts into white-hot flame when drawn. Its short, double-edged blade is decorated with carvings of laurels and olive branches, and in its bronze pommel rests a brilliant ruby, which seems to burn brighter than the blade itself.",
			# Always applies flaming brand, and need more fire resistance to resist its fire.
		"Bloodreaver" : "done",
			# Counters with this weapon apply a deathmark to the enemy.
		"Nightsbane" : "done",
			# Automatically counter enemies who would be affected by silver brand.
		"Longfang" : "done",
			# Casting a spell while wielding this weapon grants this weapon a powerful execution passive for next hit.
		"God-Cleaver" : "",
			# 
		"Worldshaper" : "",
			# Killing enemies with this weapon restores a moderate amount of mana.
		"Mjölnir" : "done",
			# Electrified brand hit has a good chance to bounce to adjacent enemies.
		"the Gauntlets of Mars": "",
			# Blocking this weapon instead causes some damage and the blocker to be stunned.
		"the Talons of Belial": "", 
			# Killing an enemy causes enemies of a lower tier in small radius to be feared for a few turns (feared also reduces ac slightly).
		"Tempest" : "",
			# 
		"Whisper" : "",
			# 

		# Armor
		"Kain's Pact" : "",
			# Getting hit by a melee attack causes you to blink.
		"Plaguebringer" : "",
			# Emits an aura of plague, damaging enemies in a certain radius.
		"God-Frame" : "",
			# Small chance to stun attacker on taking a hit.
		"Bloodshell" : "",
			# Damage done by spikes also heal you for a percent.

	}

	wclass = {
		# Weapons
		# Augmented Innate
		"fists" : ["Weapons carried in or fuzed with the hand to increase punching power."],
		"fist" : ["A weapon carried in or fuzed with the hand to increase punching power."],
		"claw" : ["A weapon carried in or fuzed with the hand, with built-in claws to rend flesh.","This weapon does increased damage to lightly armored enemies"],

		# Blunt
		"hammer" : ["A blunt weapon with a flat head and a sturdy handle.","This weapon does bonus damage against enemies wearing plate armor."],
		"warhammer" : ["A large blunt weapon with a double-sided flat head and a sturdy handle.","This weapon does bonus damage against enemies wearing plate armor and has a chance to stun the target."],
		"club" : ["A simple blunt weapon used for smashing.","This weapon does bonus damage against enemies wearing plate armor."],
		"greatclub" : ["A simple but enormous blunt weapon used for crushing.","This weapon does bonus damage against enemies wearing plate armor and has a chance to stun the target."],
		"mace" : ["A blunt weapon with a spherical head and a sturdy handle.","This weapon does bonus damage against enemies wearing plate armor."],
		"flail" : ["A blunt weapon comprised of a spiked steel ball attached to a sturdy handle with a chain.","This weapon does bonus damage against enemies wearing plate armor."],
		"gauntlet" : ["A weapon worn over the hand of the user to increase punching power.","This weapon does bonus damage against enemies wearing plate armor."],
		"gauntlets" : ["A pair of weapons worn over the hands of the user to increase punching power.","These weapons do bonus damage against enemies with plate armor and have a chance to stun the target."],
		"claw gauntlet" : ["A weapon worn over the hand with inbuilt talons to rend enemies.", "This weapon does increased damage to lightly armored enemies."],
		"claw gauntlets" : ["A pair of weapons worn over the hand with inbuilt talons to rend enemies.", "This weapon cleaves adjacent enemies on hits and does increased damage to lightly armored enemies."],

		# Polearm
		"spear" : ["A light polearm with a long shaft and sharp tip.","This weapon strikes the enemy behind the target on a successful hit."],
		"pike" : ["A two-handed polearm with an extremely long shaft and sharp tip.", "This weapon strikes the next two enemies behind the target on a successful hit."],
		"lance" : ["A light polearm with a pointed tip, usually used while mounted.", "This weapon strikes the enemy behind the target on a successful hit."],
		"polearm" : ["A weapon with a long shaft and sharp metal head used for chopping.", "This weapon strikes the enemy behind the target on a successful hit."],
		"scythe" : ["A polearm with a long curved blade that can carve men in two.", "This weapon cleaves two adjacent units on either side of the target on a successful hit."],

		# Dagger
		"dagger" : ["A short, sharpened blade with a sturdy grip.","This weapon cannot be blocked by a shield."],
		"knife" : ["A short weapon with a sturdy grip and large one-sided blade.","This weapon cannot be blocked by a shield."],

		# Axe
		"axe" : ["A martial weapon with a short shaft and sharpened head.", "This weapon does increased damage to lightly armored enemies."],
		"greataxe" : ["A large martial weapon with a long shaft and heavy head.", "This weapon cleaves adjacent enemies on hits and does increased damage to lightly armored enemies."],

		# Sword
		"sword" : ["A martial weapon with a long sharp blade attached to a hilt.", "This weapon gives you a chance to counter when an enemy attack misses."],
		"demon sword" : ["A sword forged from the blood of thousands of beings.", "This weapon ignores some armor and gives you a chance to counter when an enemy attack misses."],
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
		"throwing knife" : "A balanced knife used for throwing at longer ranges.",

		# God weapons
		"god spear" : ["A polearm with a long shaft and sharp head, initially owned by a god.", "This weapon strikes the next two enemies behind the target on a successful hit."],
		"god sword" : ["A large weapon with a long blade and two-handed grip, initially owned by a god.", "This weapon can counter and cleaves adjacent enemies on hits or, if none are adjacent, strikes the enemy behind the target."],
		"god axe" :   ["A large weapon with a long shaft and heavy head, initially owned by a god.","This weapon cleaves adjacent enemies on hits and does increased damage to lightly armored enemies."],
		"god hammer" :["A large blunt weapon with a double-sided flat head and a sturdy handle, initially owned by a god.","This weapon does bonus damage against enemies wearing plate armor and has a chance to stun the target."],


		# Armors
		"garments" : "Common apparel worn in the cities and streets.",
		"robes" : "Light armor offering the user a greater freedom of movement and magic resistance.",
		"hide" : "Medium armor fashioned from the skin of an animal.",
		"scale" : "Medium armor fashioned from the tough scales of a creature.",
		"chainmail" : "Tough armor fashioned from interwoven metal rings.",
		"plate" : "Extremely tough full-body armor made of metal or tough composite. Vulnerable to blunt weaponry.",

	}

	brand = {
		# Weapon
		"envenomed" : "This weapon has a chance to poison the enemy. Poison damage stacks progressively with successive strikes.",
		"electrified" : "This weapon has a chance to shock those struck, dealing flat damage increasing with enemy level.",
		"flaming" : "This weapon has a chance to light enemies aflame.",
		"frozen" : "This weapon has a chance to freeze victims of its strikes.",
		"silvered" : "This weapon deals extra damage to the undead, vampires, werewolves, and abominations.",
		"holy" : "This blessed weapon deals extra damage to demons and the undead.",
		"hellfire" : "This weapon deals more damage as the target's health decreases.",
		"soulflame" : "This infernal weapon has a chance to siphon the dexterity of the target.",
		"vampiric" : "This cursed weapon steals life from the victims of its strikes.",
		"antimagic" : "This weapon deals extra damage to spellcasters and users of magic.",
		"runic" : "This weapon expends mana to deliver strikes that ignore enemy armor when possible.",
		"vorpal" : "This infernal weapon clears victims of status effects and deals bonus damage for each.",
		"possessed" : "This possessed weapon hits multiple times for each strike... if it feels so inclined.",

		# Armor
		"spiked" : "This spiked armor has a chance to reflect some physical damage back to attackers.",
		"icy" : "This frosted armor provides moderate frost resistance to the wearer.",
		"tempered" : "This firefirged armor provides moderate fire resistance to the wearer.",
		"insulated" : "This padded armor provides moderate shock resistance to the wearer.",
		"voidforged" : "This glowing armor provides moderate magic defense to the wearer.",
		"runic" : "This well-adorned armor transfers physical damage to your mana reserves before your health reserves.",
	}

	skill = {
		"poison breath" : ["You breathe a cloud of noxious gas at your enemy to poison them."],
		"magic missile" : ["You conjure a phantasmal arrow of energy to pierce your foe at any range."],
		"combat roll" : ["Roll 2 squares across the floor, then throw a quivered throwing weapon at a random in-range enemy."],
		"chain lightning" : ["You fire wild lightning into the air at a specific target. The lightning has a chance to bounce on every unit within 2 squares."],
		"blink" : ["You willingly translocate to a random square within a short range."],
		"bless weapon" : ["You call upon your deity to temporarily bless your weapon to smite down demons and the unholy."],
		"dark bolt" : ["You blast a foe with a bolt cursed with a burning black fire."],
		"bloodreave" : ["You set your blood on fire and spray it to burn the soul of your enemies."],
		"flash heal" : ["You call upon your deity to heal your wounds so you may smite down your foes."],
		"raise skeleton" : ["You command a fallen warrior from centuries past to rise and fight for you."],
		"dark transformation" : ["When you have been drained of enough blood, cast a ritual to temporarily tranform into a hideous abomination."],
		"martial draw" : ["You swing at a random adjacent enemy when you draw a weapon."],
		"furious charge" : ["You gain a mad ferocity. You strike adjacent enemies in the same direction you move."],
		"iron blessing" : ["You bless an ally's armor and weapons, reducing their encumbrance. Casting on a machine will heal it instead."],


	}	

	races = {
		"Cytherean" : "A race of ethereal humanoids hailing from Venus, characterized by their intelligence and ability to temporarily walk through time.",
		"Gnome" : "A race of crafty, agile humanoids, characterized by their dexterity and ability to set explosive mines.",
		"Hobbit" : "A race of small but hardy humanoids, characterized by their charisma, dexterity, and their ability to leap moderate distances.",
		"Elf" : "A ancient race of noble humanoids, characterized by their intelligence, dexterity, and their ability to restore health and mana.",
		"Terran" : "A race of adventurous humanoids hailing from Earth, characterized by their charisma and ability to learn quickly.",
		"Naga" : "A race of reptilian humanoids, characterized by their speed and ability to temporarily poison their weapons at will.",
		"Ghoul" : "A race of decaying undead creatures, characterized by their quick regeneration and ability to tear foes apart with their teeth.",
		"Dragonborn" : "An ancient race of half-dragon humanoids, characterized by their strength and ability to breathe fire.",
		"Black Orc" : "A race of barbaric humanoid warriors, characterized by their melee proficiency and ability to purge their blood of status effects.",
		"Felltron" : "A race of ancient, sentient robotic humanoids, characterized by their strength, constitution, and very slow health regeneration.",
		"Dwarf" : "A race of stout humanoids with homes deep underground, characterized by their constitution and ability to fight long after they receive mortal wounds.",
		"Hill Troll" : "A race of hulking, brute humanoids, characterized by their huge stature and ability to wield larger weapons with great ease.",
	}





