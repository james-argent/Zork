import sys
import time
import random

#immutable strings and info
difficultyIntroMessage = "What difficulty would you like the game to be? Easy, Medium, or Hard?\n"
difficultySelectedMessage = "You have selected the difficulty: "
welcomeMessage = "Welcome to Westeros, "
inventoryMessage = "Your current inventory is: "
locationMessage = "Your current location is: "
healthMessage = "Your current health is: "
ateMessage = "You ate your "
drankMessage = "You drank your "
successMove = "You travelled "
dragonglassMessage = "You handed out the dragonglass."
nullMessage = "Looks like you forgot to say anything "
seaMessage = "You can't go there, that's the sea!"
alreadyDoneMessage = "You've already done that!"
fullStop = "."
illEquippedMessage = "You don't have any "
irrelevenceHint = "Not much to do here."
maxRangeMessage = "You better stay near the wall or the Night's Watch may think you're deserting!"
deserterMessage = "You've strayed too far from the wall and the Night's Watch have caught you and hung you as a deserter."
attackWarningMessage = "Careful, you're running out of time!"
takeMessage1 = "You put the "
takeMessage2 = " into your inventory."
wonMessage1 = "You helped prepare for the attack from the Others! You win! You achieved this in "
wonMessage2 = " turns."
endProgress1 = "Your achieved progress was "
endProgress2 = " out of "
deadMessage = "You died."
innappropriateMessage = "You can't do that here."
defaultDifficultyMessage = "You didn't enter a valid difficulty, so the difficulty has been set by default to medium."
othersAttackMessage = "Oh no, the Others attacked and you were unprepared!"
inventoryFullMessage = "Your inventory is too full!"
wightMessage = "You were attacked by wights!"
defaultUserName = "Jon Snow"
unknownCommand = "That command was unknown. Please enter another.\n"
unknownLocation = "This location doesn't have a name."
idleMessage = "What would you like to do now?\n"
null = ""
newLine = "\n"
quitCommand = "quit"

#movement stuff
directions = ("north", "east", "south", "west")
lowerRandom = 1
upperRandom = 8
horiVerti = (1, 0, 1, 0)
maxRange = 5
deadRange = maxRange + 1
advisedVisitLimit = 5
seaLimit = 2

#difficulty and turns stuff
easyTurns = 48
maxTurns = 100
hardTurns = 200
possibleDifficulties = ["easy","medium","hard"]
possibleMaxTurns = [easyTurns, maxTurns, hardTurns]
wightDamage = 1
foodHeal = 1
requiredPreparedness = 3
startingHealth = 10
maxHealth = 10
easyMode = False
warningCoefficient = 0.75

#item stuff
distributableItems = ["dragonglass"]
edibleItems = ["pork","mutton"]
drinkableItems = ["wine"]
useableItems = []
allItems = distributableItems + edibleItems + drinkableItems + useableItems
maxInventorySize = 7

#conversation stuff
samIntro = "Sam: Hey Jon! It's me, Sam."
samOptions = "a: Tell me about the whitewalkers.\nb: Tell me about the Wall.\nc: Bye.\n\n"
samReplies = ["a","b","c"]
samSentences = ["Sam: The whitewalkers are a race of ancient evil zombies which are kept at bay by the wall. They're weak to dragons and dragonglass," +
    "but they're invading soon and I don't think we're well equipped to fight them.","Sam: The wall has many castles along it, but only 3 of them are manned:" +
    "Castle Black, Eastwatch-by-the-Sea, and the Shadow Tower.","Sam: Bye Jon! I'm heading off to Oldtown."]

#information from the beginning which is subject to change
userLocationCoordinates = [0,0] # starting Coordinates, Castle Black
health = startingHealth
inventory = ["wine","mutton"]
completedCastles = []
currentLocationName = null
timeElapsed = 0

#common commands which just demand some information
knownCommands = ["inventory", "health"]
knownMessages = [inventoryMessage, healthMessage]
knownCurrent = [inventory, health]

##########################################################
######################## CLASSES #########################
##########################################################

#allows for the referral of locations' attributes by referring to the actual attribute names
class Location:
    def __init__(self, x, y, name, comment, item = "", winCon = False, visits = 0):
        self.x = x
        self.y = y
        self.name = name
        self.comment = comment
        self.item = item
        self.winCon = winCon
        self.visits = visits

#list of all of the known locations in the program
locationsList = [Location(0, 0, "Castle Black", "You're home, but something's not right, Ser Alliser Thorne always seems to be plotting something...", winCon = True),
                 Location(2, 0, "Eastwatch-by-the-Sea", "One of the only manned castles along the wall. The castle furthest East.", winCon = True),
                 Location(-2, 0, "The Shadow Tower", "One of the three remaining manned castles along the wall.", winCon = True),
                 Location(-1, 1, "Crastor's Keep", "Keep your hands off of his daughter wives or he'll kill you. There's some tasty pork roasting over the fire.", "pork"),
                 Location(-2, 2, "The Fist of the First Men", "A big battle happened here, but where are the dead brothers? There is a pile of dragonglass...", "dragonglass"),
                 Location(2, 2, "Hardhome", "The wildings have a settlement here. Better not disturb them."),
                 Location(0, -1, "Moletown", "Known for its brothel."),
                 Location(0, -4, "Winterfell", "My old home. The north remembers."),
                 Location(2, -3, "The Dreadfort", "The seat of the traitorous House Bolton."),
                 Location(-1, 0, "Icemark", "An abandoned castle along the wall. There's noone here."),
                 Location(1, 0, "Rimegate", "An abandoned castle along the wall. There's noone here."),
                 Location(-1, -1, "Queen's Crown", "An abandoned holdfast and village."),
                 Location(2, -2, "Karhold", "A strong northern castle and the seat of House Karstark.")]

##########################################################
####################### FUNCTIONS ########################
##########################################################

#tells the user where they are or just gives the coordinates if the place has no recorded name
def identifyLocation(coordinates, easyMode):
    global found
    found = False
    for i in range (len(locationsList)):
        currentLocation = locationsList[i]
        if coordinates[0] == locationsList[i].x and coordinates[1] == locationsList[i].y:
            print (locationMessage + locationsList[i].name)
            print (locationsList[i].comment)
            locationsList[i].visits += 1
            if locationsList[i].visits >= advisedVisitLimit and locationsList[i].winCon == False and locationsList[i].item == null:
                print (irrelevenceHint)
            found = True
            print 
            global currentLocationName
            currentLocationName = locationsList[i].name
    if found == False:
        if easyMode == True:
            print (locationMessage + str(coordinates))
        print (unknownLocation)

#4 second delay and exit
def slowEndGame():
    time.sleep(4)
    sys.exit(0)

#no delay and exit
def quickEndGame():
    sys.exit(0)
    
#general commands
def checkInput(thingToCheck):
    for i in range (len(knownCommands)):
        if knownCommands[i] in thingToCheck:
            print (knownMessages[i] + str(knownCurrent[i]))

#decides if you'll randomly be attacked
def randomAttack():
    global attack
    x = random.randint(lowerRandom, upperRandom) # chance of an attack is 1/range
    if x == lowerRandom:
        attack = True
    else:
        attack = False

#recursive conversation function
def samTalk():
    validAnswer = False
    samRequest = input(samOptions)
    for i in range (len(samReplies)):
        if samRequest == samReplies[i]:
            print (newLine + samSentences[i] + newLine)
            validAnswer = True
    if samRequest == samReplies[len(samReplies)-1]:
        return
    if validAnswer == False:
        print (unknownCommand)
    samTalk()

##########################################################
#################  THE  PROGRAM  BEGINS  #################
##########################################################

#user selects a difficulty level, medium by default
difficulty = input(difficultyIntroMessage)
difficulty = difficulty.lower()
for i in range(len(possibleDifficulties)):
    if difficulty == possibleDifficulties[i]: #easy mode
        maxTurns = possibleMaxTurns[i]
        easyMode = True
        print (difficultySelectedMessage + difficulty + fullStop + newLine)
if difficulty not in possibleDifficulties:
    difficulty = possibleDifficulties[1] #medium
    print (defaultDifficultyMessage)
warningTurn = round(maxTurns * warningCoefficient)

#introductory messages
print (welcomeMessage + defaultUserName + fullStop + newLine)
print (inventoryMessage + str(inventory))
print (healthMessage + str(health) + newLine)

print (samIntro)
samTalk()

#keep the game going as long as the user is 'alive'
while health > 0:
    reply = False
    inventoryAction = False

    #update the user on their situation
    identifyLocation(userLocationCoordinates, easyMode)

    #ask for next action
    command = input(idleMessage)
    command = command.lower()
    print (newLine)

    #catches if the user didn't put in an input
    if command == null:
        print (nullMessage + fullStop + newLine)
        reply = True

    if command == quitCommand:
        quickEndGame()

    #catches the generic requests "inventory", "health"
    for knownCommand in knownCommands:
        if knownCommand in command:
            checkInput(command)
            reply = True
 
    #picking up an item
    for location in locationsList:
        if currentLocationName == location.name:
            if location.item in command and location.item is not null and found == True:
                if len(inventory) < maxInventorySize:
                    inventory.append(location.item)
                    print (takeMessage1 + location.item + takeMessage2)
                else:
                    print (inventoryFullMessage)
                reply = True
                inventoryAction = True
            if location.item in command and location.item is not null and found == False and reply == False:
                print(innappropriateMessage)
                reply = True
               
    #using up an item in the inventory
    if inventoryAction == False:
        for item in inventory:
            if item in command:
                for location in locationsList:
                    if currentLocationName == location.name:
                        if item in distributableItems and location.winCon == True:
                            if location.name in completedCastles and reply == False:
                                print(alreadyDoneMessage)
                                reply = True
                            if location.name not in completedCastles and reply == False:
                                completedCastles.append(location.name)
                                inventory.remove(item)
                                print (dragonglassMessage)
                                reply = True
                                break
                if item in edibleItems:
                    print (ateMessage + item + fullStop)
                    inventory.remove(item)
                    reply = True
                    if health < maxHealth:
                        health += foodHeal
                        print (healthMessage + str(health))
                    break
                if item in drinkableItems:
                    print (drankMessage + item + fullStop)
                    inventory.remove(item)
                    reply = True
                    break

    #deals with movement
    for dir in range(len(directions)):
        if directions[dir] in command:
            if (directions[dir] == directions[1] and userLocationCoordinates[0] == seaLimit) or (directions[dir] == directions[3] and userLocationCoordinates[0] == -seaLimit):
                print (seaMessage)
                reply = True
            else:
                if dir <= 1:
                    userLocationCoordinates[horiVerti[dir]] += 1
                else:
                    userLocationCoordinates[horiVerti[dir]] -= 1
                reply = True
                print (successMove + directions[dir] + fullStop)
                if abs(userLocationCoordinates[0]) + abs(userLocationCoordinates[1]) >= deadRange:
                    print (deserterMessage)
                    slowEndGame()
                if abs(userLocationCoordinates[0]) + abs(userLocationCoordinates[1]) >= maxRange:
                    print (maxRangeMessage)

    #if north of the wall, random attacks may occur
    if userLocationCoordinates[1] > 0:
        randomAttack()
        if attack == True:
            health -= wightDamage
            print (wightMessage + newLine + healthMessage + str(health))

    #correct command, but wrong situation
    if reply == False:
        for item in allItems:
            if item in command:
                print (illEquippedMessage + item + fullStop)
                reply = True
    
    #for if the user's command was unrecognised
    if reply == False:
        print (unknownCommand)

    #win condition
    if len(completedCastles) == requiredPreparedness:
        print (wonMessage1 + str(timeElapsed) + wonMessage2)
        slowEndGame()
        
    #passage of time
    timeElapsed += 1

    #the loss condition of the game
    if timeElapsed == maxTurns:
        print(othersAttackMessage + newLine + endProgress1 + len(completedCastles) + endProgress2 + requiredPreparedness + fullStop)
        slowEndGame()
    if timeElapsed == warningTurn:
        print(attackWarningMessage)

print (deadMessage)
slowEndGame()