#Set up to be easily changeable

#size of windows
PAUSE_SIZE = (200,150)
MINIMAP_MAX_SIZE = (800,800)
START_FULLSCREEN = True

#start tile for gameplay
STARTING_TILE = "D"

#player meeple colours, acts as player keys too
PLAYER_COLOUR_LIST = ["Red", "Blue", "Lime", "Yellow", "Magenta", "Cyan"]

#game display colours
BG_DEFAULT_COLOUR = "gray94"
CASTLE_COLOUR = "Orange"
ROAD_COLOUR = "Grey"
FIELD_COLOUR = "Green"
MONESTRY_COLOUR = "indianred1"
COA_COLOUR_1 = "White"
COA_COLOUR_2 = "Blue"
UNCLAIMED_BG_COLOUR = "White"

#size of tile grid canvas for main game
TILE_SIZE = 100
TILE_GRID_X = 11
TILE_GRID_Y = 9

#bot evaluation weights
OPPOSITION_MULT = 0.3
MEEPLE_VALUE_FUNCTION = [18,36,0.7,104]
INCOMPLETE_MULT_FUNCTION = [18,36,1,-22.6]
MEEPLE_REMAINING_VALUE_FUNCTION = [0.6,5,3]
