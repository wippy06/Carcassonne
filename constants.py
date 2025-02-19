#Set up to be easily changeable

#size of windows
PAUSE_SIZE = (300,200)
SIGN_IN_OUT_SIZE = (300,300)
MINIMAP_MAX_SIZE = (800,800)
ACHIEVEMENTS_SIZE = (800,600)
START_FULLSCREEN = True

#start tile for gameplay
STARTING_TILE = "D"

#player meeple colours, acts as player keys too
PLAYER_COLOUR_LIST = ["Red", "Blue", "Lime", "Yellow", "Magenta", "Cyan"]

#game display options
TEXT_FONT = "Trebuchet MS"
BUTTON_DEFAULT_COLOUR = "grey94"
FRAME_TOP_BAR_COLOUR = "darkturquoise"
FRAME_BG_DEFAULT_COLOUR = "darkslategray1"

#tile colours
EMPTY_COLOUR = "lightskyblue"
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
MEEPLE_VALUE_FUNCTION = [18,36,0.4,59]
INCOMPLETE_MULT_FUNCTION = [13.9,36,1.2,-24]
MEEPLE_REMAINING_VALUE_FUNCTION = [0.8,5,3]

#key binds for game play frame
    #move view up
    #move view down
    #move view left
    #move view right
    #centre view to home
    #rotate preview tile clockwise
    #rotate preview tile anticlockwise
    #confirm placement
    #claim north side
    #claim east side
    #claim south side
    #claim west side
    #claim centre side
    #remove claim
    #open/close minimap
CONTROLS = ["w","s","a","d","z","e","q","c","1","2","3","4","5","r","x"]

