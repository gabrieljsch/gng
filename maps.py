
class Maps():

		rooms =  { 'square_room' : ( [
		['|','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-','-'],

		['|','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-','#','.','.','.','.','.','.','.','|'],

		['+','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.','.','#','.','.','.','.','.','.','.','+'],

		['|','.','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.','.','#','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','.','.','.','#','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','#','#','.','#','#','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','#','#','.','.','.','.','.','-','-','-','-','-',' ',' ',' ',' ','~','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','#','#','#','#',' ','.','.','.','.','.','.','.','#','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','#','#',' ',' ',' ','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.',' ',' ','#','#','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.',' ','#','#','#','#','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','#','#','#','#','.','.','.','.','.','+'],

		['|','.','.','.','.','.','.','.','.','.',' ',' ','#','#','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','#','#',' ',' ',' ','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','-',' '],

		['|','.','.','.','.','.','#','#','#','#',' ','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' '],

		['|','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','~','.','.','.','~','.','.','.','.','.','.','.','.','.','.','.','.','-','|',' ',' ',' '],

		['|','.','.','.','.','.','.','.','.','|','-','-','-','-','-','|','.','.','#','~','.','.','.','~','#','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' ',' '],

		['|','_','_','_','_','_','_','_','_','|',' ',' ',' ',' ','-','_','_','_','_',' ',' ',' ',' ','_','_','_','_','_','_','_','_','_','_','_','_',' ',' ',' ',' ',' '] ], 

		# Chests
		[((28,2), 30), ((26,2), 100)],

		# Entrances
		(0,2),

		# Exits
		[['small'],(40,2), (40,10)], 

		# Populate
		True),


		'bridge_crossing' : ( [

		[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

		[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

		[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

		[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

		[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

		[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

		[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

		['-','-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-','-','-'],

		['|','.','.','.','|','.','.','#','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','#','#','#','#','.','.','.','|'],

		['|','.','.','.','|','#','#','.','.','~','~','~','~','~','~',' ','~','~','~','~','~','~','~','~','~','~','~','~','.','.','.','#','#','.','.','.','+'],

		['+','.','.','.','.','.','.','.','.','~','~','~','~','~',' ','~','~','~','~','~','~','~','~','~','~','~','~','~','.','.','.','.','#','.','.','.','|'],

		['|','.','.','.','|','.','.','.','.','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~',' ','~','~','#','.','.','.','.','.','.','.','|'],

		['|','.','-','-','-','-','#','#','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','~','#','#','.','.','.','.','.','|',' '],

		['|','_','_','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','_','_','_','_','_','_','_','|',' '] ],

		# Chests
		[((33,8), 30), ((16, 4), 100)],

		# Entrances
		(0,10),

		# Exits
		[['small','medium','large'],(36,9)], 

		# Populate
		True,

		# Restricted Spawn Areas
		((17,4),3)),



		'fort_entrance' : ( [
		[' ',' ',' ',' ','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],

		[' ',' ',' ',' ','|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','|',' ',' ',' ',' ',' ','|'],

		[' ',' ',' ','|','.','.','.','.','#','#','.','.','.','.','#','.','.','.','.','.','.','.','.','#','.','.','.','.','.','|',' ',' ',' ',' ',' ','|'],

		[' ',' ','|','.','.','.','.','#','#','#','#','.','.','.','.','.','.','.','.','.','.','.','.','#','#','#','.','.','.','|',' ',' ',' ',' ',' ','|'],

		[' ','|','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','|',' ',' ',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.',' ',' ',' ',' ',' ','.','.','.','.','.','.','.','.','#','.','.','.','.','-','-','-',' ',' ',' ','|'],

		['+','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','#','#','.','.','.','.','+',' ',' ',' ','|'],

		['|','.','.','.','.','.','.','.','.','.','.',' ',' ',' ',' ',' ','.','.','.','.','.','.','.','.','.','.','#','.','.','.','.','|',' ',' ',' ','|'],

		['|','_','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','-','-','-',' ',' ',' ','|'],

		[' ','|','.','.','.','.','.','#','#','#','#','.','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','.','|',' ',' ',' ',' ',' ','|'],

		[' ','|','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','.','|',' ',' ',' ',' ',' ','|'],

		[' ','|','#','#','.','.','.','.','.','.','#','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','#','.','.','|',' ',' ',' ',' ',' ','|'],

		[' ','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'] ],

		# Chests
		[],

		# Entrances
		(0,6),

		# Exits
		[['fort_interior'],(31,6)], 

		# Populate
		True),


		'fort_hallway' : ( [
		['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],

		['|',' ','+','.','.','.','#','#','#','.','.','.','.','.','.','.','.','.','.','.','#','.','.','.','.','.','.','.','.','.','.','.','.','+',' ','|'],

		['|',' ','|','.','.','.','.','.','.','.','#','.','_','.','.','.','.','#','.','.','.','.','.','.','.','.','.','.','_','.','.','.','.','|',' ','|'],

		['|',' ',' ','|','.','.','-','-','-','-','-','|',' ','|','-','-','-','-','-','-','-','-','-','-','-','-','-','|',' ','|','-','-','-','-','-','-'],

		['-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '] ],

		# Chests
		[],

		# Entrances
		(2,1),

		# Exits
		[['fort_interior'],(33,1)], 

		# Populate
		True),



		'fort_exit' : ( [
		['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',' ',' ',' ',' ','-','-','-','-','-','-','-','-'],

		['|',' ',' ',' ',' ','|','.','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ','|','.','#','#','.','.','.','.','|'],

		['|',' ',' ',' ',' ','|','.','#','.','.','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|',' ',' ',' ',' ','|','.','#','.','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|',' ',' ',' ',' ','|','.','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.','.','.','|'],

		['|',' ',' ',' ','-','-','.','.','.','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','.','.','.','.','.','.','.','.','+'],

		['|',' ',' ',' ','|','.','.','.','.','.','.',' ',' ',' ',' ','#','#',' ',' ',' ',' ',' ',' ',' ','#','#',' ',' ',' ',' ','-','.','.','.','.','.','.','|'],

		['|',' ',' ',' ','+','.','.','.','.','.','|',' ',' ',' ','#','#','#','#',' ',' ',' ',' ',' ','#','#','#','#',' ',' ',' ',' ','|','.','.','.','.','.','|'],

		['|',' ',' ',' ','-','-','.','.','.','.','|',' ',' ',' ',' ','#','#',' ',' ',' ',' ',' ',' ',' ','#','#',' ',' ',' ',' ',' ','|','_','_','.','.','.','|'],

		['|',' ',' ',' ',' ','|','.','#','#','.','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','.','.','|'],

		['|',' ',' ',' ',' ','|','.','.','.','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','_','_','|'],

		['|',' ',' ',' ',' ','|','.','.','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],

		['-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '] ],

		# Chests
		[],

		# Entrances
		(4,7),

		# Exits
		[['small','medium','large'],(37,5)], 

		# Populate
		True,

		# Restricted Spawn Areas
		((5,7),3)),






		'starting_room' : ( [
		['-','-','-','-','-','-','-','-','-','-','-','-','-','-',' ',' ',' ',' '],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','|','-',' ',' ',' '],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' '],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','-','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','+'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','-','|'],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' '],

		['|','.','.','.','.','.','.','.','.','.','.','.','.','|',' ',' ',' ',' '],

		['-','-','-','-','-','-','-','-','-','-','-','-','-','-',' ',' ',' ',' '] ],

		# Chests
		[((9,5), 100)],

		# Entrances
		(0,0),

		# Exits
		[['small','medium','large'],(17,5)], 

		# Populate
		False),








		 }


		sizes = {
			'small' : ['bridge_crossing'],
			'medium' : ['square_room'],
			'large' : ['square_room','fort_entrance'],
			'fort_interior' : ['fort_hallway','fort_exit'],
		}

		# sizes = {
		# 	'small' : ['fort_hallway'],
		# 	'medium' : ['fort_hallway'],
		# 	'large' : ['fort_hallway'],
		# 	'fort_interior' : ['fort_hallway'],
		# }


