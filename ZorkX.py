import sys
import time

#stuff that should never change and doesn't fit the other categories
nameRequest = "What is your name, adventurer?\n"
welcomeMessage = "Welcome to Westeros, "
inventoryMessage = "Your current inventory is: "
locationMessage = "Your current location is: "
healthMessage = "Your current health is: "
quitMessage = "If you would like to quit, just close the console."
ateMessage = "You ate your "
drankMessage = "You drank your "
dragonglassMessage = "You handed out the dragonglass."
usedMessage = "You used your "
nullMessage = "Looks like you forgot to say anything "
wonMessage = "You helped defeat the attack from the Others! You win! The program will now close."
seaMessage = "You can't go there, that's the sea!"
fullStop = "."
maxRangeMessage = "You better stay near the wall or the Night's Watch may think you're deserting!"
deserterMessage = "You've strayed too far from the wall and the Night's Watch have caught you and hung you as a deserter."
attackWarningMessage = "Careful, you're running out of time!"
takeMessage1 = "You put the "
takeMessage2 = " into your inventory."
deadMessage = "You died."
othersAttackMessage = "Oh no, the Others attacked and you were unprepared!"
inventoryFullMessage = "Your inventory is too full!"
defaultUserName = "Jon Snow"
unknownCommand = "That command was unknown. Please enter another.\n"
unknownLocation = "This location doesn't have a name."
idleMessage = "What would you like to do now?\n"
userNameWrong = nullMessage + ", I will just call you " + defaultUserName + ".\n"
null = ""
newLine = "\n"
directions = ("north", "east", "south", "west")
successMove = "You travelled "
timeElapsed = 0
horiVerti = (1, 0, 1, 0)
maxInventorySize = 7
maxTurns = 100
requiredPreparedness = 3
maxRange = 5
deadRange = maxRange + 1
warningTurn = maxTurns / 0.75
distributableItems = ["dragonglass"]
edibleItems = ["pork","mutton"]
drinkableItems = ["wine"]
completedCastles = []

class Location:
    def __init__(self, x, y, name, comment, item, winCon):
        self.x = x
        self.y = y
        self.name = name
        self.comment = comment
        self.item = item
        self.winCon = winCon

locationsList = [Location(0, 0, "Castle Black", "You're home, but something's not right, Ser Alliser Thorne always seems to be plotting something...", "", True),
                 Location(2, 0, "Eastwatch-by-the-Sea", "One of the only manned castles along the wall. The castle furthest East.", "", True),
                 Location(-2, 0, "The Shadow Tower", "One of the three remaining manned castles along the wall.", "", True),
                 Location(-1, 1, "Crastor's Keep", "Keep your hands off of his daughter wives or he'll kill you. There's some tasty pork roasting over the fire.", "pork", False),
                 Location(-2, 2, "The Fist of the First Men", "A big battle happened here, but where are the dead brothers? There is a pile of dragonglass...", "dragonglass", False),
                 Location(2, 2, "Hardhome", "The wildings have a settlement here. Better not disturb them.", "", False),
                 Location(0, -1, "Moletown", "Known for its attractive qualities.", "", False),
                 Location(0, -2, "Winterfell", "My old home. The north remembers.", "", False),
                 Location(2, -2, "The Dreadfort", "The seat of the traitorous House Bolton.", "", False),
                 Location(0, -3, "Moat Cailin", "An important location by which to control the Neck.", "", False),
                 Location(-1, 0, "Icemark", "An abandoned castle along the wall. There's noone here.", "", False),
                 Location(1, 0, "Rimegate", "An abandoned castle along the wall. There's noone here.", "", False)]

#information about your character which is subject to change
userLocationCoordinates = [0,0] # Castle Black
health = 10
inventory = ["wine","mutton"]
currentLocationName = ""

#arrays which must be the same length
knownCommands = ["inventory", "health", "quit"]
knownMessages = [inventoryMessage, healthMessage, quitMessage]
knownCurrent = [inventory, health, null]

#general commands
def checkInput(thingToCheck):
    for i in range (len(knownCommands)):
        if knownCommands[i] in thingToCheck:
            print (knownMessages[i] + str(knownCurrent[i]))

#tells the user where they are or just gives the coordinates if the place has no recorded name
def identifyLocation(coordinates):
    found = False
    for i in range (len(locationsList)):
        if coordinates[0] == (locationsList[i]).x and coordinates[1] == (locationsList[i]).y:
            print (locationMessage + (locationsList[i]).name)
            print ((locationsList[i]).comment)
            found = True
            global currentLocationName
            currentLocationName = (locationsList[i]).name
    if found == False:
        print (locationMessage + str(coordinates))
        print (unknownLocation)

#3 second delay and exit
def loseGame():
    time.sleep(3)
    sys.exit(0)

#if the user doesn't enter a name, they're given a default name
userName = input(nameRequest)
if len(userName) < 1:
        print (userNameWrong)
        time.sleep(0.5)
        userName = defaultUserName

#introductory messages
print (welcomeMessage + userName + fullStop + newLine)
print (inventoryMessage + str(inventory))
print (healthMessage + str(health) + newLine)

#keep the game going as long as the user is 'alive'
while health > 0:
    reply = False
    inventoryAction = False

    #update the user on their situation
    identifyLocation(userLocationCoordinates)

    #ask for next action
    command = input(idleMessage)
    command = command.lower()
    print (newLine)

    if command == null:
        print (nullMessage + fullStop + newLine)
        reply = True

    for knownCommand in knownCommands:
        if knownCommand in command:
            checkInput(command)
            reply = True
 
    #picking up an item
    for location in locationsList:
        if currentLocationName == location.name:
            if location.item in command and location.item is not null:
                if len(inventory) < maxInventorySize:
                    inventory.append(location.item)
                    print (takeMessage1 + location.item + takeMessage2)
                else:
                    print (inventoryFullMessage)
                reply = True
                inventoryAction = True
               
    #using up an item in the inventory
    if inventoryAction == False:
        for item in inventory:
            if item in command:
                for location in locationsList:
                    if currentLocationName == location.name:
                        if item in distributableItems and location.winCon == True:
                            print (dragonglassMessage)
                            if location.name not in completedCastles:
                                completedCastles.append(location.name)
                            inventory.remove(item)
                            reply = True
                            break
                if item in edibleItems:
                    print (ateMessage + item + fullStop)
                    inventory.remove(item)
                    reply = True
                    break
                if item in drinkableItems:
                    print (drankMessage + item + fullStop)
                    inventory.remove(item)
                    reply = True
                    break

    #deals with movement
    for dir in range(len(directions)):
        if directions[dir] in command:
            if (directions[dir] == directions[1] and userLocationCoordinates[0] == 2) or (directions[dir] == directions[3] and userLocationCoordinates[0] == -2):
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
                    loseGame()
                if abs(userLocationCoordinates[0]) + abs(userLocationCoordinates[1]) >= maxRange:
                    print (maxRangeMessage)
    
    #for if the user's command was unrecognised
    if reply == False:
        print (unknownCommand)

    #win condition
    if len(completedCastles) == requiredPreparedness:
        print (wonMessage)
        loseGame()
        
    #passage of time
    timeElapsed += 1

    #the loss condition of the game
    if timeElapsed == maxTurns:
        print(othersAttackMessage)
    if timeElapsed == warningTurn:
        print(attackWarningMessage)

print (deadMessage)
loseGame()