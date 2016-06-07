##Code made by Juan Carlos Aguilera Pérez
##For further information can email me at aguilerap.jc@gmail.com
import random
import sys
import motion
import time
from naoqi import ALProxy

#State 1 to 6 have the same way to work

#State 1 Function it will wait for 3 secs to the user to press the Tactil
#If the player does not press it, will return 0 and end the execution,
#else it will return 1 , and continue the game
def state1_Rear_Tactil(memory,LED):
        print("Estado 1 Rear Tactil")
    start = time.time()
        end = 0
        pressed = 0
        while(memory.getData("RearTactilTouched") <> 1.0 and end <  3.0):
             end = time.time()-start
             pressed = 1
    
        if(end >= 3):
                pressed = 0
        if(pressed == 0):
                print("Game Over")
        LED.fadeRGB('FaceLeds',1.0,0,0,1.0)
        LED.fadeRGB('FaceLeds',1.0,1.0,1.0,0.5)                
        return 0
        else:
                print("Great")
                LED.fadeRGB('FaceLeds',0,1.0,0,1.0)
        LED.fadeRGB('FaceLeds',1.0,1.0,1.0,0.5)
                return 1

##########################################################################
###########Add here the functions of the states that are missing##########
##########################################################################


#Wait function used to wait between the say and the call of the function
#Allows the user to be prepared to press any sensor 
def wait05_State():


#State that generate the random numbers and call the sensor methods 
def TransitionState(memory,speech,LED):
    on = 1
    state = random.randrange(1,6,1)
    stateArr = [0]*10
    counter = 0
    state = random.randrange(1,6,1)
    stateArr[counter] = state
    #Use of ALTextToSpeech proxy to say the sequence to follow
    while(on == 1):
        speech.say("Listen to the secuence")
        for x in xrange(0,counter+1):
            if(stateArr[x] == 1):
                speech.say("Rear Tactil")
                wait05_State()
            elif(stateArr[x] == 2):
                speech.say("Front Tactil")
                wait05_State()
            elif(stateArr[x] == 3):
                speech.say("Right Hand")
                wait05_State()
            elif(stateArr[x] == 4):
                speech.say("Left Hand")
                wait05_State()
            elif(stateArr[x] == 5):
                speech.say("Right Foot")
                wait05_State()
            elif(stateArr[x] == 6):
                speech.say("Left Foot")
                wait05_State()

        #Call the state for each case   
    for x in xrange(0,counter+1):
            actState = stateArr[x]
            if(actState == 1):
                on = state1_Rear_Tactil(memory,LED)
                if(on == 0):
                    break
            ##Add the states that are missing 
            ##Those state could be added by elif()
            else:
                print("State Error")
                    
        state = random.randrange(1,6,1)
        counter +=1
        if(counter >= 10): 
            speech.say("Congratulations you WIN!!!")
            LED.rasta(2)
            InitialState(memory,speech,LED,0)
        counter = 0;
    else:
        LED.fadeRGB('FaceLeds',1.0,0,0,1.0)
        speech.say("So sad, You Lose")      
        LED.fadeRGB('FaceLeds',1.0,1.0,1.0,0.5)    
        InitialState(memory,speech,LED,0)
        counter = 0;

    stateArr[counter] = state

def InitialState(memory,speech,LED,replay):
    #replay = 1 Play Game
    #replay = 0 Waiting for an answer of the player
    #replay = 2 Player dont want to play anymore, finish the game
    if(replay == 1):
    speech.say("Touch middle tactil to start the game")
        print("Presione sensor tactil medio para comenzar")
        while(memory.getData("MiddleTactilTouched") <> 1.0):
            1+1
        
        print("El Juego comenzara ahora")
        TransitionState(memory,speech,LED)
    elif(replay == 2):
        speech.say("Game Over")
        print("Juego Terminado")
    main(0)
    else:
        speech.say("To play again touch front Tactil, else touch rear tactil")
        print("Si desea jugar de nuevo presione el Tactil Frontal, de lo contrario presione Tactil trasero")
        while(replay == 0):
            if(memory.getData("FrontTactilTouched")):
                replay = 1
                InitialState(memory,speech,LED,replay)
            elif(memory.getData("RearTactilTouched")):
                replay = 2
                InitialState(memory,speech,LED,replay)
                
        
def main(robotIP):
    # 1.5
        # Create proxy to ALMemory
    ##Robot IP received as a parameter on Terminal
        IP = robotIP
        PORT = 9559
    #Initialization of Proxies(Aldebaran API's objects)
        memory  = ALProxy("ALMemory", IP, PORT)
        motion  = ALProxy("ALMotion", IP, PORT)
        posture = ALProxy("ALRobotPosture", IP, PORT)
        speech  = ALProxy("ALTextToSpeech",IP,PORT)
        LED     = ALProxy("ALLeds",IP,PORT) 
    replay=1;
        LED.setIntensity('FaceLeds',1.0)
    InitialState(memory,speech,LED,replay)
    

if __name__ == "__main__":
    robotIp = "127.0.0.1"

    if len(sys.argv) <= 1:
        print "Usage python motion_walk.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)