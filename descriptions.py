from sty import Rule, Render

class Colors():

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





class Descriptions():


	legendary = {
		# Weapons
		"the Glaive of Gore" : "This rustic glaive was forged during the first wars of men. Its intensely sharp blade and opposite fleshhooks allow it to easily disembowel enemies with a single motion. Rivulets in the blade allow blood to flow from the blade down the shaft of the weapon in streams.",
			# 10% Chance to cause disembowled effect, which causes a bleeding damage over time and weakens the afflicted.
		"Soulreaper" : "This ancient warscythe's blade glows a faint blue, indiscernible whispers are heard when wielding it. Its blade emerges from a skull on its shaft fashioned from femurs, which pulsate lightly...as if the weapon were breathing.",
			# Increasing damage with kill tiers, 6 tiers, at last tier also gains possessed brand.
		"the Singing Spear" : "This ornate spear can be heard emitting musical tones when moving, it was once wielded by Huehuecóyotl. Its broad head has eight bloodletting holes, and its sturdy wooden shaft is wrapped in faded yet colorful linen bands.",
			# Chance to change brand with every hit.
		"Kraken" : "This ancient axe looks as if it had lain at the bottom of the ocean for centuries. Barnacles, coral, and in places even moss adorn this weapon like so many ornaments. Its simple design and light frame allow it to be thrown with relative ease and deadly effectiveness.",
			# This axe can be thrown but takes a turn to return, but deals secondary damage and immobillizes when ripped out of an enemy to return to user, assuming a hand is free.
		"Krog's Maw" : "This huge waraxe is the size of a mortal man, for it is said once to be wielded by the orc deity himself. Its single head is covered in huge teeth, spinning on mechanical chains to rend flesh. Records of those slain by this axe are depicted in crude markings along its ivory haft.",
			# Can gain a overshield equal to a fifth of max health with this weapon when healing over max health with its vampiric brand.
		"Splinter" : "This deadly knife is coated in black adder venom that stops the heart of its victims in seconds. Its black single-edged blade blends into the grip without a hilt to separate, and its guard is wrapped by a thin, bone-white linen cloth.",
			# Applies 3 venom stacks instead of normal 2 on brand hit.
		"Swiftspike" : "This elegant dagger is constructed of elf glass and wyvern bone. This dagger is lighter in the hand than the empty hand itself, a strange visible force resides within the glass of its blade.",
			# Killing an enemy with this grants a burst of speed for a few turns.
		"Dawn" : "This ornate shortsword glows hot-red when sheathed and bursts into white-hot flame when drawn. Its short, double-edged blade is decorated with carvings of laurels and olive branches, and in its bronze pommel rests a brilliant diamond, which seems to burn brighter than the blade itself.",
			# Always applies flaming brand, and need more fire resistance to resist its fire brand.
		"Bloodreaver" : "This demon sword resembles a large falchion doused in blood. Its one sharp edge is jagged yet razor sharp, and blood seemingly flows through veins carved into the blade. In the center of its red hilt lies a large hole, in which floats a pulsating black amethyst. No one has dared to try removing it...",
			# Counters with this weapon apply a deathmark to the enemy.
		"Nightsbane" : "This bastard sword of legend has a name feared by all creatures of darkness. Its blade is forged entirely from blessed dark silver, its dark-golden hilt and guard in the form of a sharp cross. A vial of holy water rests in center of the hilt, and scrolls covered in holy words are wrapped around the weapon's grip.",
			# Automatically counter enemies who would be affected by silver brand.
		"Longfang" : "This beautiful bastard sword runs black and white with twisted vein patterns of damascus steel. The blade is inscribed with strange magical runes, one for each school of magic. The pommel is dominated by the ivory tooth of some creature, as long as the grip and as straight as a spike.",
			# Casting a spell while wielding this weapon grants this weapon the brand corresponding to the type of spell for a single hit.  
		"God-Cleaver" : "This executioner greatsword has a name feared by all but the one who wields it. Once this blade tastes the blood of a victim four times, the fifth is guaranteed to end its life, regardless of magic and deception. Its blade is as long as a mortal man is tall, and its fully-engraved blade glows a faint orange.",
			# After 4 damaging hits with this weapon, the next hit will execute the target (if its not a unique?).
		"Worldshaper" : "This legendary hammer is the size of a mortal man, for it is said to have been wielded by Odin. A crackling blue energy field surrounds this golden hammer at all times. Its single golden head sits atop its long mithril shaft, and a brilliant opal rests on its large pommel.",
			# Killing enemies with this weapon restores a quarter tank of mana.
		"Mjölnir" : "This hammer of legend was once wielded by the god Thor, it still crackles with his thunderous energy. Its short haft is offset by its enourmous, almost rectangular head, decorated with ancient runes and images of Yggdrasil.",
			# Electrified brand hit bounces thunder to adjacent enemies.
		"the Gauntlets of Mars": "These ancient stone gauntlets generate a small energy field around them. The blood-red stone of the gauntlets are carved with ancient symbols of war and battle, and numerous cracks and battlescars adorn the edges of the weapons.",
			# Blocking this weapon instead causes full damage and the blocker to be stunned.
		"the Talons of Belial": "These bone-white gauntlets hold in place two long, razor-sharp talons each. The talons are each longer than the gauntlet ítself and curve near the end slightly in towards the gauntlet. Its a miracle if anything comes into contact with one of the talons and isn't shorn completely in half.", 
			# Killing an enemy causes enemies of a lower tier in small radius to be feared for a few turns (feared also reduces ac slightly).
		"Tempest" : "This golden bow radiates with flashes of dark storms and bright sunbeams, for it was once wielded by Horus himself. It takes great strength to draw the string fully back, for the bow easily can retain its intended shape while strung indefinitely.",
			# Also fires quivered ammo at 2 other random enemies in range.
		"Godfinger" : "This seemingly normal bow somehow operates without a bowstring. When drawn, a blue phantasmal hand is seen over the user's own, assisting in the bow's operation. It is said that the bow has yet to miss a target, no matter the operator.",
			# You can never miss your target when firing this bow.

		# Armor
		"Kain's Pact" : "These fiery robes burn blood red to the eye. The robes utilize an ornate leather breastplate, resembling a rib-cage, to allow its users more protection than normal robes. Wearers are able to cast spells when magical energy is spent...for a price.",
			# Can cast spells with health when not enough mana.
		"the Phasic Robes" : "These ethereal robes seem to ebb and flow independent of the user's movements. The pinkish-orange robes feel as if they are made of heavy wool, but are as light as if from silk. Wearers are often seen appearing in multiple locations within the same time.",
			# Getting hit by a melee attack causes you to blink.
		"Plaguebringer" : "This feared chainmail armor uses inbuilt vents to spread infectious diseases through the air. The chainmail is rusty and almost green with packed filth, and spikes holding heads of various defeated opponents are adorned on its backplate.",
			# Emits an aura of plague, applying one stack of poison to enemies in radius 2.
		"God-Frame" : "This set of golden plate armor is designed to protect a god from everything possible. It is beautifully engraved with scenes of myth and legend, and on its backplate is welded a force generator that can emit bursts of stunning energy.",
			# Small chance to stun attackers on taking a hit.
		"Bloodshell" : "This dark red plate armor is covered in small white teeth, which seem to breathe and react to the touch. In place of a chest pauldron, this armor utilizes a cracked monstrous chronid skrull, teeth flared outwards.",
			# Damage done by spikes also heals you for a percent.

	}

	wclass = {
		# Weapons
		# Augmented Innate
		"fists" :["Weapons carried in or fuzed with the hand to increase punching power."],
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
		"glaive" : ["A weapon with a long shaft and a long, sharp metal head used for chopping.", "This weapon strikes the enemy behind the target on a successful hit."],
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
		"executioner greatsword" : ["An extremely large martial weapon with a heavy blade and two-handed grip.", "This weapon deals heavy damage to a single target."],

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
		# Spells and Abilities
		"poison breath" : ["You breathe a cloud of noxious gas at your enemy to poison them."],
		"magic missile" : ["You conjure a phantasmal arrow of energy to pierce your foe at any range."],
		"combat roll" : ["Roll 2 squares across the floor, then throw a quivered throwing weapon at a random in-range enemy."],
		"chain lightning" : ["You fire wild lightning into the air at a specific target. The lightning has a chance to bounce on every unit within 2 squares."],
		"thunderbolt" : ["You call down a huge bolt of lightning and thunder to smite your foe. The thunderbolt has a chance to stun the target."],
		"blink" : ["You willingly translocate to a random square within a short range."],
		"bless weapon" : ["You call upon your deity to temporarily bless your weapon to smite down demons and the unholy."],
		"tremor strike" : ["You slam your fists into the ground, creating a damaging shockwave around you that also has a good chance to stun."],
		"dark bolt" : ["You blast a foe with a bolt cursed with a burning black fire."],
		"death's hand" : ["You unleash a ghostly hand to grab a target, rendering it immobile, setting it aflame, and also poisoning it."],
		"bloodreave" : ["You set your blood on fire and spray it to burn the soul of your enemies."],
		"flash heal" : ["You call upon your deity to heal your wounds so you may smite down your foes."],
		"raise skeleton" : ["You command a fallen warrior from centuries past to rise and fight for you."],
		"dark transformation" : ["When you have been drained of enough blood, cast a ritual to temporarily tranform into a hideous abomination."],
		"iron blessing" : ["You bless an ally's armor and weapons, reducing their encumbrance. Casting on a machine will heal it instead."],
		"deathmark" : ["You curse a target with the black mark, which ignites when the target is hit by a physical attack."],
		"spectral sword" : ["You conjure a phantasmal sword from the energy around you. The sword's damage is equal to your intelligence."],
		"double shot" : ["You nock two arrows on your bow in hopes of showering death upon the enemy."],
		"battlecry" : ["You conjure a phantasmal sword from the energy around you. The sword's damage is equal to your intelligence."],
		# Traits
		"furious charge" : ["You gain a mad ferocity. You strike adjacent enemies in the same direction you move."],
		"deadly precision" : ["You target weaknesses in enemies' armor, giving you a chance to critically strike with hits. The chance is doubled when using knives and daggers."],
		"martial draw" : ["You swing at a random adjacent enemy when you draw a melee weapon."],
		"evening rites" : ["You prayers and rituals make you immune to the effects of hellfire, soulflame, and vampiric weapons."],
		"life leech" : ["Your damaging spells drain enemies to heal you for some of their damage."],
		"mana flow" : ["Your connection to mana lets you regenerates it at twice its normal rate."],


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


	potions = {
		"healing potion": "This potion made from various herbs heals the drinker for 20 health.",
		"orcblood potion": "This potion made from the blood of an orc purges the drinker from all status effects.",
		"resistance potion": "This potion grants the drinker vastly increased resistances to the elements for a short time.",
		"quicksilver potion" : "This potion grants the drinker incredibly quick movement speed for a while.",
	}





