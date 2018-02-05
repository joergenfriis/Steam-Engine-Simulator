# Haendelsesafhaengige ordrer midlertidigt parkeret her


        # Haandtering af haendelsesafhaengige ordrer: Gal retning

        if ((virkning[20] in [0,1,2]) and (virkning[0] < 45) and (virkning[1] > 0)) or ((virkning[20] in [4,5,6]) and (virkning[0] > 55) and (virkning[1] > 0)):
            galRetning = 1
        else:
            galRetning = 0

        if (galRetning == 1) and (galRetningTid == 0):
            galRetningTid = realTid

        print("Gal retning = ",galRetning)

        if ((realTid - galRetningTid) > 5) and ((realTid - callTime) > 30) and (galRetning == 1):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            #channel12.set_volume(0,1)
            #channel12.play(skipper04, loops=0)       # Gal retning
            #print("Gal retning ")
            #time.sleep(3)
            if virkning[20] in [0,1,2]:
                channel12.set_volume(0,1)
                channel12.play(skipper06, loops=0)   # Frem
                realTid = realTid - 5               # For atgive tid til at udfoere ordren
            if virkning[20] in [4,5,6]:
                channel12.set_volume(0,1)
                channel12.play(skipper05, loops=0)   # Bak
                realTid = realTid - 5
            galRetning = 0
            galRetningTid = 0
            callTime = realTid

        # Haandtering af haendelsesafhaengige ordrer: Gal hastighed

        if (virkning[20] == 3) and ((virkning[0] < 45) or (virkning[0] > 55)) and (galHastighed == 0):
            galHastighed = 1
        else:
            galHastighed = 0

        if ((virkning[20] in [0,6]) and (virkning[1] <= 66) and (galHastighed == 0)):
            galHastighed = 2
        else:
            galHastighed = 0

        if ((virkning[20] in [1,5]) and ((virkning[1] > 66) or (virkning[1] < 33)) and (galHastighed == 0)):
            galHastighed = 3
        else:
            galHastighed = 0

        if ((virkning[20] in [2,4]) and (virkning[1] >= 33) and (galHastighed == 0)):
            galHastighed = 4
        else:
            galHastighed = 0

        if (virkning[20] in [0,1,2,4,5,6]) and (virkning[1] == 0) and (galHastighed == 0):
            galHastighed = 5
        else:
            galHastighed = 0

        if (galHastighed > 0) and (galHastighedTid == 0):
            galHastighedTid = realTid

        print("Gal hastighed = ",galHastighed)    

        if (((realTid - galHastighedTid) > 5) and ((realTid - callTime) > 30) and (galHastighed > 0)):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            if (galHastighed == 1):
                channel12.set_volume(0,1)
                channel12.play(skipper15, loops=0)      # Stop
                realTid = realTid - 5 
            if (galHastighed == 2):
                channel12.set_volume(0,1)
                channel12.play(skipper07, loops=0)      # Tror du det er et hvilehjem
                time.sleep(3)
                if virkning[20] == 1:
                    channel12.set_volume(0,1)
                    channel12.play(skipper09, loops=0)  # Fuld kraft frem
                    realTid = realTid - 5 
                if virkning[20] == 7:
                    channel12.set_volume(0,1)
                    channel12.play(skipper12, loops=0)  # Fuld kraft bak
                    realTid = realTid - 5 
            if (galHastighed == 3):
                if virkning[1] > 66:
                    channel12.set_volume(0,1)
                    channel12.play(skipper08, loops=0)  # Tag det roligt
                    time.sleep(3)
                    if virkning[20] == 2:
                        channel12.set_volume(0,1)
                        channel12.play(skipper10, loops=0)  # Halv kraft frem
                        realTid = realTid - 5 
                    if virkning[20] == 6:
                        channel12.set_volume(0,1)
                        channel12.play(skipper13, loops=0)  # Halv kraft bak
                        realTid = realTid - 5 
                if virkning[1] < 33:
                    channel12.play(skipper07, loops=0)  # Tror du det er et hvilehjem
                    time.sleep(3)
                    if virkning[20] == 2:
                        channel12.set_volume(0,1)
                        channel12.play(skipper10, loops=0)  # Halv kraft frem
                        realTid = realTid - 5 
                    if virkning[20] == 6:
                        channel12.set_volume(0,1)
                        channel12.play(skipper13, loops=0)  # Halv kraft bak
                        realTid = realTid - 5 
            if (galHastighed == 4):
                channel12.set_volume(0,1)
                channel12.play(skipper08, loops=0)      # Tag det roligt
                time.sleep(3)
                if virkning[20] == 3:
                    channel12.set_volume(0,1)
                    channel12.play(skipper11, loops=0)  # Ganske langsomt frem
                    realTid = realTid - 5 
                if virkning[20] == 5:
                    channel12.set_volume(0,1)
                    channel12.play(skipper14, loops=0)  # Ganske langsomt bak
                    realTid = realTid - 5 
            if (galHastighed == 5):
                channel12.set_volume(0,1)
                channel12.set_volume(0,1)
                channel12.play(skipper16, loops=0)      # Vi kan ikke ligge her hele dagen
                realTid = realTid - 5 
            galHastighed = 0
            galHastighedTid = 0
            callTime = realTid

        # Haandtering af haendelsesafhaengige råd:

        if (virkning[7] < 8) and (virkning[8] == 0) and (fejlBetjening == 0):
            fejlBetjening = 1
        else:
            fejlBetjening = 0

        if (virkning[8] > 1) and (tilstand[7] > 0) and (fejlBetjening == 0):
            fejlBetjening = 2
        else:
            fejlBetjening = 0

        if (handling[2] < 100) and (virkning[7] < 8) and (fejlBetjening == 0):
            fejlBetjening = 3
        else:
            fejlBetjening = 0

        if (handling[3] > 10) and (fejlBetjening == 0):
            fejlBetjening = 4
        else:
            fejlBetjening = 0

        if (virkning[7] > 9) and (fejlBetjening == 0):
            fejlBetjening = 5
        else:
            fejlBetjening = 0

        if (virkning[2] < 10) and (fejlBetjening == 0):
            fejlBetjening = 6
        else:
            fejlBetjening = 0

        if ((virkning[4] > 80) or (virkning[4] < 70)) and (fejlBetjening == 0):
            fejlBetjening = 7
        else:
            fejlBetjening = 0

        if (handling[7] < 90) and (fejlBetjening == 0):
            fejlBetjening = 8
        else:
            fejlBetjening = 0

        if (handling[8] < 90) and (fejlBetjening == 0):
            fejlBetjening = 9
        else:
            fejlBetjening = 0

        print("Fejlbetjening = ",fejlBetjening)

        if (fejlBetjening > 0) and (fejlBetjeningTid == 0):
            fejlBetjeningTid = realTid
        else:
            fejlBetjeningTid = 0

        if ((realTid - fejlBetjeningTid) > 5) and ((realTid - callTime) > 30) and (fejlBetjening == 1):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief01, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid

        if ((realTid - fejlBetjeningTid) > 5) and ((realTid - callTime) > 30) and (fejlBetjening == 2):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief02, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid

        if ((realTid - fejlBetjeningTid) > 15) and ((realTid - callTime) > 30) and (fejlBetjening == 3):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief03, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid
                
        if ((realTid - fejlBetjeningTid) > 5) and ((realTid - callTime) > 30) and (fejlBetjening == 4):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief04, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid

        if ((realTid - fejlBetjeningTid) > 5) and ((realTid - callTime) > 30) and (fejlBetjening == 5):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief05, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid
        
        if ((realTid - fejlBetjeningTid) > 5) and ((realTid - callTime) > 30) and (fejlBetjening == 6):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief06, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid
        
        if ((realTid - fejlBetjeningTid) > 5) and ((realTid - callTime) > 30) and (fejlBetjening == 7):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief07, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid

        if ((realTid - fejlBetjeningTid) > 5) and ((realTid - callTime) > 30) and (fejlBetjening == 8):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief08, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid
                                         
        if ((realTid - fejlBetjeningTid) > 5) and ((realTid - callTime) > 30) and (fejlBetjening == 9):
            #channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(3)
            channel12.set_volume(0,1)
            channel12.play(chief09, loops=0)
            fejlBetjening = 0
            fejlBetjeningTid = 0
            callTime = realTid
        
