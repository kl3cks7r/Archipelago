from enum import Enum

class CSPacket(Enum):
    READINFO = 0
    RUNTSC = 1
    READFLAGS = 2
    RUNEVENTS = 3
    READMEM = 4
    WRITEMEM = 5
    READSTATE = 6
    ERROR = 255
    DISCONNECT = 255

class CSTrackerAutoTab(Enum):
    UNDEFINED = 0
    '''Includes all other rooms not covered (no tab switch)'''
    MIMIGA_VILLAGE = 1
    '''Includes Mimiga Village, First Cave, and Graveyard rooms'''
    EGG_CORRIDOR = 2
    '''Includes Egg Corridor and Ruined Egg Corridor rooms'''
    GRASSTOWN = 3
    '''Includes Grasstown rooms'''
    SAND_ZONE = 4
    '''Includes Sand Zone rooms'''
    LABYRINTH = 5
    '''Includes Labryinth, Core, and Waterway rooms'''
    PLANTATION = 6
    '''Includes Plantation, Outer Wall, and Last Cave rooms'''
    SACRED_GROUNDS = 7
    '''Includes Balcony and Sacred Grounds rooms'''

class CSTrackerEvent(Enum):
    SAVED_SUE = 0
    '''Occurs when you talk to Sue in Egg Corridor'''
    SAVED_KAZUMA = 1
    '''Occurs after destroying the shelter door in Grasstown'''
    SAVED_CURLY = 2
    '''Occurs after Curly is carried through the Main Artery'''
    USED_MA_PIGNON = 3
    '''Occurs after feeding Curly Ma Pignon'''
    DEFEATED_BALROG_1 = 3
    '''Occurs after defeating Balrog in Mimiga Village'''
    DEFEATED_IGOR = 4
    '''Occurs after defeating Igor in Egg Corridor'''
    DEFEATED_BALROG_2 = 5
    '''Occurs after defeating Balrog in Power Room'''
    DEFEATED_BALFROG = 6
    '''Occurs after defeating Balfrog in Gum'''
    DEFEATED_CURLY = 7
    '''Occurs after defeating Curly in Sand Zone Residence'''
    DEFEATED_OMEGA = 8
    '''Occurs after defeating Omega in Sand Zone'''
    DEFEATED_TOROKO = 9
    '''Occurs after defeating Frenzied Toroko in Sand Zone Warehouse'''
    DEFEATED_PUU_BLACK = 10
    '''Occurs after defeating Puu Black in Old Clinic'''
    DEFEATED_MONSTER_X = 11
    '''Occurs after defeating Monster X in Labrynith'''
    DEFEATED_BALROG_3 = 12
    '''Occurs after defeating Balrog in Boulder Chamber'''
    DEFEATED_CORE = 13
    '''Occurs after defeating the Core'''
    DEFEATED_IRONHEAD = 14
    '''Occurs after defeating Ironhead in Main Artery'''
    DEFEATED_THE_SISTERS = 15
    '''Occurs after defeating The Sisters in Ruined Egg Observation Chamber'''
    DEFEATED_MA_PIGNON = 16
    '''Occurs after defeating Ma Pignon in Store Room'''
    DEFEATED_RED_DEMON = 17
    '''Occurs after defeating Red Demon in Hidden Last Cave'''
    FINAL_BOSS = 18
    '''Occurs after defeating Undead Core or Ballos (depending on goal)'''