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
nullMessage = "Looks like you forgot to say anything"
fullStop = "."
takeMessage1 = "You put the "
takeMessage2 = " into your inventory."
deadMessage = "You died."
othersAttackMessage = "Oh no, the Others attacked and you were unprepared!"
inventoryFullMessage = "Your inventory is too full!"
defaultUserName = "Jon Snow"
unknownCommand = "That command was unknown. Please enter another."
unknownLocation = "This location doesn't have a name."
idleMessage = "What would you like to do now?\n"
userNameWrong = nullMessage + ", I will just call you " + defaultUserName + "."
null = ""
directions = ("north", "east", "south", "west")
successMove = "You travelled "
timeElapsed = 0
horiVerti = (1, 0, 1, 0) #horizontal/vertical

#location tuples (x-coordinate, y-coordinate, location name, location comment)
loc1 = [0, 0, "Castle Black", "You're home, but something's not right, Ser Alliser Thorne always seems to be plotting something...",""]
loc2 = [1, 0, "Eastwatch-by-the-Sea", "One of the only manned castles along the wall. The castle furthest East.",""]
loc3 = [-1, 0, "The Shadow Tower", "One of the three remaining manned castles along the wall.",""]
loc4 = [0, 1, "Crastor's Keep", "Keep your hands off of his daughter wives or he'll kill you. There's some tasty pork roasting over the fire.","pork"]
loc5 = [0, 2, "The Fist of the First Men", "A big battle happened here, but where are the dead brothers? There is a pile of dragonglass...","dragonglass"]
loc6 = [1, 2, "Hardhome", "The wildings have a settlement here. Better not disturb them.",""]
loc7 = [0, -1, "Moletown", "Known for its attractive qualities.",""]
loc8 = [0, -2, "Winterfell", "My old home. The north remembers.",""]
loc9 = [1, -2, "The Dreadfort", "The seat of the traitorous House Bolton.",""]
loc10 = [0, -3, "Moat Cailin", "An important location by which to control the Neck.",""]
locationsList = [loc1, loc2, loc3, loc4, loc5, loc6, loc7, loc8, loc9, loc10]

#information about your character which is subject to change
location = [0,0] # Castle Black
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
def identifyLocation(location):
    found = False
    for i in range (len(locationsList)):
        if location[0] == (locationsList[i])[0] and location[1] == (locationsList[i])[1]:
            print (locationMessage + (locationsList[i])[2])
            print ((locationsList[i])[3])
            found = True
            global currentLocationName
            currentLocationName = (locationsList[i])[2]
    if found == False:
        print (locationMessage + str(location))
        print (unknownLocation)

#if the user doesn't enter a name, they're given a default name
userName = input(nameRequest)
if (len(userName) < 1):
        print (userNameWrong)
        userName = defaultUserName

#introductory messages
print (welcomeMessage + userName + fullStop)
print (inventoryMessage + str(inventory))
print (healthMessage + str(health))

#keep the game going as long as the user is 'alive'
while health > 0:
    reply = False
    inventoryAction = False

    #update the user on their situation
    identifyLocation(location)

    #ask for next action
    command = input(idleMessage)
    command = command.lower()

    if command == null:
        print (nullMessage + fullStop)
        reply = True

    for i in range (len(knownCommands)):
        if ((knownCommands[i]) in command):
            checkInput(command)
            reply = True
 
    #picking up an item
    for i in range (len(locationsList)):
        if currentLocationName == (locationsList[i])[2]:
            if (((locationsList[i])[4]) in command) and ((locationsList[i])[4] is not null):
                if (len(inventory)) < 7:
                    inventory.append((locationsList[i])[4])
                    print (takeMessage1 + (locationsList[i])[4] + takeMessage2)
                else:
                    print (inventoryFullMessage)
                reply = True
                inventoryAction = True
               
    #using up an item in the inventory
    if inventoryAction == False:
        for item in inventory:
            if item in command:
                if item == "dragonglass":
                    print (dragonglassMessage)
                    inventory.remove(item)
                    reply = True
                    break
                if item == "pork" or item == "mutton":
                    print (ateMessage + item + fullStop)
                    inventory.remove(item)
                    reply = True
                    break
                if item == "wine":
                    print (drankMessage + item + fullStop)
                    inventory.remove(item)
                    reply = True
                    break

    #deals with movement
    for i in range (len(directions)):
        if (directions[i] in command):
            if (i <= 1):
                location[horiVerti[i]] += 1
            else:
                location[horiVerti[i]] -= 1
            reply = True
            print (successMove + directions[i] + fullStop)
    
    #for if the user's command was unrecognised
    if reply == False:
        print (unknownCommand)
        
    #passage of time
    timeElapsed += 1

    #the loss condition of the game
    if timeElapsed == 50:
        print(othersAttackMessage)
        health = 0

print (deadMessage)