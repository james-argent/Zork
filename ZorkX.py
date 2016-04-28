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
defaultUserName = "Jon Snow"
unknownCommand = "That command was unknown. Please enter another."
idleMessage = "What would you like to do now?\n"
userNameWrong = nullMessage + ", I will just call you " + defaultUserName + fullStop
null = ""
directions = ["north", "east", "south", "west"]
successMove = "You travelled "
horiVertiHoriVerti = [0, 1, 0, 1] #horizontal/vertical swap

#subject to change
location = [0,0]
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
    print (locationMessage + str(location))

    #ask for next action
    command = input(idleMessage)

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
                location[horiVertiHoriVerti[i]] += 1
            else:
                location[horiVertiHoriVerti[i]] -= 1
            replies += 1
            print (successMove + directions[i] + fullStop)
    
    #for if the user's command was unrecognised
    if (replies == 0):
        print (unknownCommand)