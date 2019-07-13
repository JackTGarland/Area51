import configparser
import os
import random
directory = os.listdir()

#Create var.ini if not found in directory
if 'var.ini' not in os.listdir():
    print("No config found, creating config.")
    config = configparser.ConfigParser()
    config['people'] = {'civilians': '150',
        'civilianHitRate': '33',
        'troops': '250',
        'troopHitRate': '85'}
    config['base'] = {'troopsPerFloor': '45',
        'floorMinimum': '50',
        'floorMaximum': '90',
        'aliensSpawn': '15',
        'doorTime': '15',
        'reinforcements': '60'
    }
    config['aliens'] = {'alignment': 'good'}

    with open('var.ini', 'w') as configfile:
        config.write(configfile)
config = configparser.ConfigParser()
config.sections()
config.read('var.ini')

print("storming Area-51")
print("civilian hit rate set to :" + config['people']['civilianHitRate'])
print("military hit rate set to :" + config['people']['troopHitRate'])

# We are just saving some information from the config into variables as we manipulate them later.
civPop = int(config['people']['civilians'])
milPop = int(config['people']['troops'])
civHitRate = int(config['people']['civilianHitRate'])
milHitRate = int(config['people']['troopHitRate'])
milKilled = 0
totalRounds = 0

#Fight function, this will but what determins who win's a battles and who losses.
def fight(milPop):
    round = 0
    global civPop
    global milKilled
    global civKilled
    milStartPop = milPop
    civStartPop = civPop
    while civPop > 0 and milPop > 0:
        turn = random.randrange(1,3)
        if turn == 1:
            atk = random.randrange(0,101)
            if atk <= civHitRate:
                milPop = milPop - 1
        else:
            atk = random.randrange(0,101)
            if atk <= milHitRate:
                civPop = civPop - 1
        round = round + 1
    if civPop <= 0:
        print("After a long battle the civilans have lost.")
        print("the fight Lasted ", round, " rounds.")
        milKilled = milKilled + milStartPop - milPop
        print(milStartPop - milPop, " Military personal were killed that floor.")
        return 'loss'
    else:
        print("Civilans have won the fight.")
        print("the fight Lasted ", round, " rounds.")
        print(civPop, " civilans remain.")
        milKilled = milKilled + milStartPop
        print(civStartPop - civPop, " Civilans were killed that floor.")
        return 'win'

#First call of fight, 
result = fight(milPop)

#Only if the civialans have won the first fight will it generate the rest of the base, no point running code that will never be used.
if result == 'win':
    numberOfFloors = random.randrange(int(config['base']['floorMinimum']),int(config['base']['floorMaximum'])+1)
    currentFloor = 1
    while currentFloor <= numberOfFloors and civPop > 0:
        troopsPerFloor = int(config['base']['troopsPerFloor'])
        print("Current floor ", currentFloor)
        if currentFloor >= int(config['base']['aliensSpawn']):
            if config['aliens']['alignment'] == 'good' and civHitRate < 100:
                civHitRate = civHitRate + 20
                if civHitRate > 100:
                    civHitRate = 100
            elif config['aliens']['alignment'] == 'bad':
                troopsPerFloor = troopsPerFloor - round(troopsPerFloor/10)
                print("Due to aliens there will only be", troopsPerFloor, "troops on this floor.")
                civPop - 10

        result = fight(troopsPerFloor)   
        if result == 'win':
            currentFloor = currentFloor + 1
        else:
            print("You made it to floor ", currentFloor)
            print(milKilled, " Military personal were killed.")
            print(int(config['people']['civilians']), "Civilans were killed.")
