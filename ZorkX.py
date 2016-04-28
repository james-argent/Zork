#stuff that should never change and doesn't fit the other categories
nameRequest = "What is your name, adventurer?\n"
welcomeMessage = "Welcome to Westeros, "
inventoryMessage = "Your current inventory is: "
locationMessage = "Your current location is: "
healthMessage = "Your current health is: "
quitMessage = "If you would like to quit, just close the console."
usedMessage = "You used your "
nullMessage = "Looks like you forgot to say anything"
fullStop = "."
lostMessage = "You died."
defaultUserName = "Jon Snow"
unknownCommand = "That command was unknown. Please enter another."
unknownLocation = "This location doesn't have a name."
idleMessage = "What would you like to do now?\n"
userNameWrong = nullMessage + ", I will just call you " + defaultUserName + fullStop
null = ""
directions = ["north", "east", "south", "west"]
successMove = "You travelled "
horiVerti = [1, 0, 1, 0] #horizontal/vertical

#location tuples (x-coordinate, y-coordinate, location name, location comment)
location1 = (0, 0, "Castle Black", "You're home, but something's not right, Ser Alliser Thorne seems to be plotting something...")
location2 = (1, 0, "Eastwatch-by-the-Sea", "One of the only manned castles along the wall. The castle furthest East.")
location3 = (-1, 0, "The Shadow Tower", "One of the three remaining manned castles along the wall.")
location4 = (0, 1, "Crastor's Keep", "Keep your hands off of his daughters/wives or he'll kill you.")
location5 = (0, 2, "The Fist of the First Men", "A big battle happened here, but where are the dead brothers?")
location6 = (1, 2, "Hardhome", "The wildings have a settlement here. Better not disturb them.")
location7 = (0, -1, "Moletown", "Known for its attractive qualities.")
location8 = (0, -2, "Winterfell", "My old home. The north remembers.")
location9 = (1, -2, "The Dreadfort", "The seat of the traitorous House Bolton.")
location10 = (0, -3, "Moat Cailin", "An important location by which to control the Neck.")
tuplesList = location1, location2, location3, location4, location5, location6, location7, location8, location9, location10

#information about your character which is subject to change
location = [0,0] # Castle Black
health = 10
inventory = ["wine","mutton"]

#arrays which must be the same length
knownCommands = ["inventory", "health", "quit"]
knownMessages = [inventoryMessage, healthMessage, quitMessage]
knownCurrent = [inventory, health, null]

#general commands
def checkInput(thingToCheck, currentInventory, currentHealth):
    for i in range (0, len(knownCommands)):
        if (knownCommands[i] in thingToCheck):
            print (knownMessages[i] + str(knownCurrent[i]))

#tells the user where they are or just gives the coordinates if the place has no recorded name
def identifyLocation(location):
    found = False
    for i in range (0, len(tuplesList)):
        if location[0] == (tuplesList[i])[0] and location[1] == (tuplesList[i])[1]:
            print (locationMessage + (tuplesList[i])[2])
            print ((tuplesList[i])[3])
            found = True
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
    replies = 0

    #update the user on their situation
    identifyLocation(location)

    #ask for next action
    command = input(idleMessage)
    command = command.lower()

    if command == null:
        print (nullMessage + fullStop)
        replies += 1

    for i in range(0, len(knownCommands)):
        if ((knownCommands[i]) in command):
            checkInput(command, inventory, health)
            replies += 1
    
    #using up an item in the inventory
    for i in range (0, len(inventory)):
        if inventory[i] in command:
            print (usedMessage + inventory[i] + fullStop)
            inventory.remove(inventory[i])
            replies += 1
            break

    #deals with movement
    for i in range (0, (len(directions))):
        if (directions[i] in command):
            if (i <= 1):
                location[horiVerti[i]] += 1
            else:
                location[horiVerti[i]] -= 1
            replies += 1
            print (successMove + directions[i] + fullStop)
    
    #for if the user's command was unrecognised
    if (replies == 0):
        print (unknownCommand)

print (lostMessage)