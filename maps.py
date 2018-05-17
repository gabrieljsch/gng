
class Maps():

		rooms =  { 'square_room' : ( [
		['|','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','-','-','-','-','-','-','-','|'],

		['|','.','.','.','.','.','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','-','-','-','-','-','-','-','#','.','.','.','.','.','.','.','|'],

		['+','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','.','#','.','.','.','.','.','.','.','+'],

		['|','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','.','.','.','.','.','.','.','#','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','.','.','.','#','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','-','-','-','-','#','#','.','#','#','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','#','#','.','.','.','.','.','-','-','-','-','-','|',' ',' ',' ','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','#','#','#','#','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','#','#','#','#','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','#','#','#','#','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','+'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','|',' ',' ',' ','|','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'] ], 

		# Chests
		[('normal', (28,2)), ('normal', (26,2))],

		# Entrances
		(0,2),

		# Exits
		[(40,2), (40,13)], 

		# Populate
		True),


		'bridge_crossing' : ( [
		['-','-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-','-'],

		['|','.','.','.','|','|','.','.','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','.','.','|','|','.','.','.','|'],

		['|','.','.','.','|','|','.','.','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','.','.','|','|','.','.','.','+'],

		['+','.','.','.','.','.','.','.','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','.','.','|','|','.','.','.','|'],

		['|','.','.','.','|','|','.','.','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','.','.','.','.','.','.','.','|'],

		['|','.','.','.','|','|','.','.','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','.','.','.','.','.','.','.','|'],

		['-','-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-','-'] ],

		# Chests
		[('orc', (2,2))],

		# Entrances
		(0,3),

		# Exits
		[(36,2)], 

		# Populate
		True),


		'fort_entrance' : ( [
		['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['+','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','+',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ','|'],

		['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'] ],

		# Chests
		[],

		# Entrances
		(0,6),

		# Exits
		[(28,6)], 

		# Populate
		True),






		'starting_room' : ( [
		['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','+'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'] ],

		# Chests
		[('normal', (9,5))],

		# Entrances
		(0,0),

		# Exits
		[(17,5)], 

		# Populate
		False),








		 }


		sizes = {
			'small' : ['bridge_crossing','fort_entrance'],
			'medium' : [],
			'large' : ['square_room','fort_entrance']
		}



