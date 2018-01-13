# simulator.py
#
# Hovedprogram til drift af dampmaskinesimulatoren paa Det Gamle Vaerft.
#
# Datastruktur:
# design[]      Valg af designparametre sker naar der vaelges programmodus
# handling[]    Programmet indlaeser operatoerens handlinger
# tilstand[]    Programmet beregner maskinens tilstand
# virkning[]    Programmet giver ordre til de relevante slaver om virkning
#
# design[0] = Antal sekunder mellem hver opdatering
# design[1] = Kedelrumfang i liter (realistisk 7.690 l, pædagogisk 500 l)
# design[2] = Brandvaerdi af kul (32.000 kJ/kg)
# design[3] = Smoereolieforbrug pr time ved 100 % maskinydelse (2 liter)
# design[4] = Rumfang af smoereolietank (5 liter)
# design[5] = Skalering af oliepumpe (0.1)
# design[6] = Kedelvandstab (5 % af det tilførte damp kommer ikke retur)
# design[7] = Overtryksventil paa kedel (blaeser ved 10 bar)
# design[8] = Kedelvandshaner max flow i liter/sek
# design[9] = Kondensvandshaner max flow i liter/sek
# design[10] = Damphaner max flow i kg/sek
# design[11] = Længde af transportbånd i meter
# design[12] = Max hastighed af transportbånd i meter/sek
# design[13] = Flyveaskeaflejring (tilstopning) % pr sekund
#
# handling[0] = Omstyring (0-100)
# handling[1] = Indpumpet olie siden start (liter)
# handling[2] = Aabning af primaert luftspjaeld (0-100)
# handling[3] = Aabning af sekundaert luftspjaeld (0-100)
# handling[4] = Kulmaengde i fyrkanal (kg)
# handling[5] = Kedelvand ind (0-100)
# handling[6] = Kedelvand ud (0-100)
# handling[7] = Kondensator ind (0-100)
# handling[8] = Kondensator ud (0-100)
# handling[9] = Damp ind (0-100)
# handling[10] = Damp ud (0-100)
# handling[11] = Programvalg (0-4)
#
# tilstand[0] = Omstyringens stilling (0-100)
# tilstand[1] = Olie i oliebeholder i liter (0 til design[4])
# tilstand[2] = Forbraendingshastighed i kg kul pr. sekund
# tilstand[3] = Aktuel brandvaerdi af kul i kJ/kg
# tilstand[4] = Roegtemperatur i kedel
# tilstand[5] = Vand i kedel i liter
# tilstand[6] = Damptryk i bar (overtryk)
# tilstand[7] = luft i damprummet (0-100%)
# tilstand[8] = Maskinydelse (0-100)
# tilstand[9] = Maskintelegraf (0-6)
# tilstand[10] = Indfyret effekt i kJ/sekund
# tilstand[11] = flyveaske i røgrør (0-100)
# tilstand[12] = tidspunkt for sidste rensning af røgrør
# tilstand[13] = vandtemperatur i kedel
# tilstand[14] = akummuleret damp ind
# tilstand[15] = akkumuleret damp ud
# tilstand[16] = sikkerhedsventil aaben/lukket 1/0
# tilstand[17] = damp til raadighed i kedlen
# tilstand[18] = damp til raadighed for maskinen
# tilstand[19] = damp der lukkes ud til det fri
# tilstand[20] = Kondensat i kg/sek
# tilstand[21] = Temperatur i kondensator
# tilstand[22] = Tryk i kondensator
# tilstand[23] = forbrugt oliemaengde i liter/time
#
# virkning[0] = Omstyringens stilling paa modellen (0-100)
# virkning[1] = Modellens omdrejningshastighed (0-100%)
# virkning[2] = Oliestand i skueroer (0-100%)
# virkning[3] = Roeggastemperatur (50-650 grader)
# virkning[4] = Kedelvand i skueroer (0-100%)
# virkning[5] = Film i kooeje (0/1: afspilning eller pause)
# virkning[6] = Vacuum i kondensator (0-1 bar)
# virkning[7] = Kedeltryk (0-10 bar)
# virkning[8] = Hastighed af transportbaand (0-design[12] m/s)
# virkning[9] = Vand fra overtryksventil (0/1)
# virkning[10] = Lys i brandkammer (0/1)
# virkning[11] = Varme i brandkammer (0/1)
# virkning[12] = Lyd af forberedelse til sejlads (0-100 %)
# virkning[13] = Lyd af dampmaskine (0-100 %)
# virkning[14] = Lyd af vand i roer (0-100 %)
# virkning[15] = Lyd af vand, der pjasker (0-100 %)
# virkning[16] = Lyd af blaesende overtryksventil (0-100 %)
# virkning[17] = Lyd af maskine, der skal smoeres (0-100 %)
# virkning[18] = Lyd af maskinhaveri (0-100 %)
# virkning[19] = Lys i kontrollampe (1/0)
# virkning[20] = Maskintelegrafens stilling (1-7: FF-FB)
# virkning[21] = Kommando i taleroer
# virkning[22] = Lyd af maskintelegraf floejte
# virkning[23] = Lyd af damp i rør
# 
#
# Joergen Friis 06.01.2018
#
#############################################################################

import pygame
import math
import lyd
import time
import powernet
import transport
import servo
import model
import vejecelle
import flowmaaler
import omstyring
import skueglasOlie
import skueglasKedel
import primaerluft
import ventiler
import programvalg
import IRremote
import servoTryk
import sikkerhedsventil

print("Starter simulatorprogram")

# Initiering af simulatoren ################################################

print("Initiering")

# Saet designparametre

design[0] = 1
design[1] = 8900
design[2] = 7600
design[3] = 2
design[4] = 5
design[5] = 0.1
design[6] = 5
design[7] = 10
design[8] = 3
design[9] = 3
design[10] = 0.66
design[11] = 1.4
design[12] = 0.7
design[13] = 0.000278

# Aflaes handlinger

handling[0] = omstyring.Read_omstyring()
handling[1] = oliepumpe.Read_flowmaaler() * design[5]
handling[2] = primaerluft.Read_primaerluft()
handling[3] = sekundaerluft.Read_sekundaerluft()
handling[4] = vejecelle.Read_vejecelle() / 1000
handling[5] = ventiler.readKedelvandInd()
handling[6] = ventiler.readKedelvandUd()
handling[7] = ventiler.readKondensatorvandInd()
handling[8] = ventiler.readKondensatorvandUd()
handling[9] = ventiler.readDampInd()
handling[10] = ventiler.readDampUd()
handling[11] = programvalg.read()

# aflaes programvaelger og start demoprogram hvis det er valgt

if (handling[11] == 1):
    while true:
        demo.demo()

# aflaes programvaelger og juster designparametre tilsvarende

if ((handling[11] == 2) or (handling[11] == 4)):
    design[2] = 160000
    deign[13] = 0.0333
    tilstand[13] = 95
else:
    design[2] = 32000
    design[13] = 0.000278
    tilstand[13] = 40

# beregn tilstanden

tilstand[0] = 50
tilstand[1] = 0.5 * design[4]
tilstand[2] = 0
tilstand[3] = 0
tilstand[4] = 0
tilstand[5] = design[1] * 0.5
tilstand[6] = 0
tilstand[7] = 100
tilstand[8] = 0
tilstand[9] = 3
tilstand[10] = 0
tilstand[11] = 0
tilstand[12] = 0
tilstand[13] = tilstand[13]
tilstand[14] = 0
tilstand[15] = 0
tilstand[16] = 0
tilstand[17] = 0
tilstand[18] = 0
tilstand[19] = 0
tilstand[20] = 0
tilstand[21] = 0
tilstand[22] = 0
tilstand[23] = 0

# beregn virkningerne

virkning[0] = 50
virkning[1] = 0
virkning[2] = (tilstand[1]/design[4])*100
virkning[3] = 0
virkning[4] = (tilstand[5]/design[1])*100
virkning[5] = 0
virkning[6] = 1
virkning[7] = 0
virkning[8] = 0
virkning[9] = 0
virkning[10] = 0
virkning[11] = 0
virkning[12] = 100
virkning[13] = 0
virkning[14] = 0
virkning[15] = 0
virkning[16] = 0
virkning[17] = 0
virkning[18] = 0
virkning[19] = 0
virkning[20] = tilstand[9]
virkning[21] = 0
virkning[22] = 0
virkning[23] = 0

# Toem transportbaandet for kul
transport.TransportGo(150)  
time.sleep(5)
transport.TransportStop()

# Nulstil vejecellen
vejecelle.Reset_vejecelle()

# Nulstil oliepumpen
oliepumpe.Reset_flowmaaler()

# Taend fjernsynet i kooejet
powernet.Relay6on()
time.sleep(10)
IRremote.TVonOff()
time.sleep(5)
IRremote.TVrightArrow()
time.sleep(1)
IRremote.TVrightArrow()
time.sleep(1)
IRremote.TVok()
time.sleep(1)
IRremote.TVok()
time.sleep(1)
IRremote.TVrightArrow()
time.sleep(1)
IRremote.TVrightArrow()
time.sleep(1)
IRremote.TVrightArrow()
time.sleep(1)
IRremote.TVok()
time.sleep(1)
IRremote.Pause()
pause=1                             # Naar pause=1 er billedet pauset

# Start lydanlaegene
powernet.Relay5on
pygame.mixer.init(channels=2)       # Mixeren saettes til stereo
pygame.mixer.set_num_channels(11)
channel1 = pygame.mixer.Channel(0) # Baggrundslyd, der spiller hele tiden
channel2 = pygame.mixer.Channel(1) # Lyd af hovedmaskinen der koerer
channel3 = pygame.mixer.Channel(2) # Maskintelegraf, beskedfloejte og ordrer fra broen
channel4 = pygame.mixer.Channel(3) # Multifunktionspumpe
channel5 = pygame.mixer.Channel(4) # Lyd af vand i roer
channel6 = pygame.mixer.Channel(5) # Lyd fra damphaner
channel7 = pygame.mixer.Channel(6) # Lyd af sikkerhedsventil
channel8 = pygame.mixer.Channel(7) # Mislyde fra maskinen
channel9 = pygame.mixer.Channel(8) # Maskinhaveri
channel10 = pygame.mixer.Channel(9) # Dampfloejte
channel11 = pygame.mixer.Channel(10) # Vandpjask

if (handling[11] != 0):
    channel1.set_volume(virkning[12],0)        # spiller kun i venstre kanal = maskinrum
    channel1.play(lyd.baggrund, loops = -1)     # spiller uendeligt
    
# Udfoer alle virkninger
servo.gangskifte(virkning[0]) 
model.ModelRun(virkning[1],virkning[0])
skueglasOlie.set(virkning[2])
servo.smokeTemp(virkning[3])
skueglasKedel(virkning[4])
servoTryk(virkning[6],virkning[7])
transport.TransportGo(virkning[8])
if (virkning[9] == 1):
    sikkerhedsventil.sikkerhedsventilOn()
    time.sleep(1)
    sikkerhedsventil.sikkerhedsventilOff()
else:
    sikkerhedsventil.sikkerhedsventilOff()
if (virkning[10] == 1):
    powernet.Relay4on()
if (virkning[11] == 1):
    powernet.Relay4on()

if (virkning[19] == 1):
    powernet.Relay10on()
if (virkning[20] == 0):
    servo.maskintelegraf_FF()
if (virkning[20] == 1):
    servo.maskintelegraf_HF()
if (virkning[20] == 2):
    servo.maskintelegraf_LF()
if (virkning[20] == 3):
    servo.maskintelegraf_FS()
if (virkning[20] == 4):
    servo.maskintelegraf_LB()
if (virkning[20] == 5):
    servo.maskintelegraf_HB()
if (virkning[20] == 6):
    servo.maskintelegraf_FB()

# Initiering faerdig
virkning[19] = 1
tid = 0
galRetning = 0
galRetningTid = 0
galHastighed = 0
galHastighedTid = 0
fejlBetjening = 0

# Drift af simulatoren ######################################################

while True:
    time.sleep(design[0]) 
    tid = tid + 1

    # REGISTRER HANDLINGER  ####################################################
    handling[0] = omstyring.Read_omstyring()
    handling[1] = oliepumpe.Read_flowmaaler() * design[5]
    handling[2] = primaerluft.Read_primaerluft()
    handling[3] = sekundaerluft.Read_sekundaerluft()
    handling[4] = vejecelle.Read_vejecelle() / 1000
    handling[5] = ventiler.readKedelvandInd()
    handling[6] = ventiler.readKedelvandUd()
    handling[7] = ventiler.readKondensatorvandInd()
    handling[8] = ventiler.readKondensatorvandUd()
    handling[9] = ventiler.readDampInd()
    handling[10] = ventiler.readDampUd()
    handling[11] = programvalg.read()

    if (handling[11] == 0):
        break

    # BEREGN TILSTANDE ########################################################

    # Flyveaske i roer

    tilstand [11] = (tid-tilstand [12]) * design [13]
    

    # Energiproduktion

    if (handling[4]<0.5):
        tilstand[2] = 0
        #virkning[8] = 0
        tilstand[3] = design[2]*(100-tilstand[11])/100
        tilstand[10] = 0
        tilstand[4] = 40

    if ((handlig[4] >= 0.5) and (handling[4] < 22.5) and (handling[3] <= 10)):
        tilstand[2] = (handling[2]+handling[3])*27.3/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-4*(10-handling[3]))*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = tilstand[3]/(0.24*(1+20))+18

    if ((handling[4] >= 0.5) and (handling[4] < 22.5) and (handling[3] > 10)):
        tilstand[2] = (handling[2]+10)*27.3/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = tilstand[3]/(0.24*(1+20))+18

    if ((handling[4] >= 22.5) and (handling[4] < 45) and (handling[3] <= 10)):
        tilstand[2] = ((handling[2]*(100-(handling[4]-22.5)*100/22.5)/100)+handling[3])*27.3/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-4*(10-handling[3]))*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = tilstand[3]/(0.24*(1+20))+18

    if ((handling[4] >= 22.5) and (handling[4] < 45) and (handling[3] > 10)):
        tilstand[2] = ((handling[2]*(100-(handling[4]-22.5)*100/22.5)/100)+10)*27.3/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = tilstand[3]/(0.24*(1+20))+18

    if ((handling[4] > 45) and (handling[3] <= 10)):
        tilstand[2] = handling[3]*27.3/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-4*(10-handling[3]))*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = tilstand[3]/(0.24*(1+20))+18

    if((handling[4] > 45) and (handling[3] > 10)):
        tilstand[2] = 10*27.3/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = tilstand[3]/(0.24*(1+20))+18

    # Dampproduktion eller fortaetning

    while int(tilstand[13]) != int(27.606 * math.log(tilstand[6]) + 107.98):

        if int(tilstand[13]) > int(27.606 * math.log(tilstand[6]) + 107.98):
            tilstand[5] = tilstand[5] - 1
            tilstand[13] = tilstand[13] - (531.33 - 18.22 * math.log(tilstand[6]))/4.186 / tilstand[5]
            V = 1.7259 * math.pow(tilstand[6],-0.939)
            Vd = (design[1] - tilstand[5])/1000
            tilstand[6] = tilstand[6] + V/Vd

        if int(tilstand[13]) < int(27.606 * math.log(tilstand[6]) + 107.98):
            tilstand[5] = tilstand[5] + 1
            tilstand[13] = tilstand[13] + (531.33 - 18.22 * math.log(tilstand[6]))/4.186 / tilstand[5]
            V = 1.7259 * math.pow(tilstand[6],-0.939)
            Vd = (design[1] - tilstand[5])/1000
            tilstand[6] = tilstand[6] - V/Vd

    if (virkning[8] > 0):
        tilstand[13] = tilstand[13] + tilstand[10] * tid / tilstand[5]

    if (virkning[8] <= 0):
        tilstand[13] = tilstand[13] - 31.2 * (tilstand[13] - 20) * 70 * 4.184/3600 * tid/tilstand[5]
        
    # Roeggastemperatur

    if (handling[3] <= 10):
        tilstand[4] = tilstand[13] + 50

    if (handling[3] > 10):
        tilstand[4] = tilstand[13] + 50 - 30*(handling[3]/100)

    tilstand[4] = tilstand[4] + (600-tilstand[4])* tilstand[11]/100

    # Dampdistribution

    if (tilstand[6] > 10):
        tilstand[16] = 1

    tilstand[17] = ((design[1] - tilstand[5]) / 1000) / 1.7295 * math.pow(tilstand[6],-0.939)
    tilstand[18] = handling[9] / (handling[9] + handling[10] + tilstand[16]*100)*tilstand[17]/100
    tilstand[19] = handling[10] / (handling[9] + handling[10] + tilstand[16]*100)*tilstand[17]/100
    tilstand[14] = tilstand[14] + tilstand[18]
    tilstand[15] = tilstand[15] + tilstand[19]

    # Luftbalance

    if (tilstand[15] < (tilstand[14] + (design[1]-tilstand[5])/1.7259*1000)):
        tilstand[18] = tilstand[18]*0.9

    # Fortaetning af damp i kondensatoren

    tilstand[20] = tilstand[18]*design[6]/100
    tilstand[21] = 99-(handling[7]*0.9)
    tilstand[22] = 0.000002*math.pow(tilstand[21],3)-0.0001*math.pow(tilstand[21],2)+0.004*tilstand[21]-0.0184
        
    # Vandbalance i kedel

    tilstand[5] = tilstand[5] + (handling[5]*design[8] - handling[6]*design[8] + tilstand[20])*design[1]

    # Maskinydelse

    tilstand[8] = 100*(tilstand[18]/0.29)*(tilstand[6]-tilstand[22])/10*math.fabs(tilstand[0]-50)*handling[8]
                                                                           
    # Oliebalance

    tilstand[1] = handling[1]-design[3]*tilstand[8]


    # DEBUGGING  ###############################################################################

    print(" Tid = ",tid)
    for i in range(0,23):
        print("Tilstand[",i,"] = ",tilstand[i])

    print("******************************************************")
    


    # BEREGN OG UDFOER VIRKNINGER  ###########################################################################

    virkning[0] = handling[0]
    servo.gangkifte(virkning[0])
                    
    virkning[1] = tilstand[8]
    model.ModelRun(virkning[1],virkning[0])
    channel2.set_volume(virkning[1],0)   
    if (virkning[1] > 0) and (virkning[1] <= 33):
        channel2.play(lyd.langsom, loop=-1)
    if (virkning[1] > 33) and (virkning[1] <=66):
        channel2.play(lyd.halvKraft, loop=-1)
    if (virkning[1] > 66):
        channel2.play(lyd.fuldKraft, loop=-1)
    
    virkning[2] = tilstand[1]/design[4]*100
    skueglasOlie.set(virkning[2])
    
    virkning[3] = tilstand[4]
    # Er ikke programmeret endnu på Arduino og i Python. Afventer printplader.
                     
    virkning[4] = tilstand[5]/design[1]*100
    skueglasVand.set(virkning[4])

    virkning[6] = tilstand[22]
    virkning[7] = tilstand[6]
    servoTryk.vis(virkning[6],virkning[7])
                     
    virkning[8] = tilstand[2]*design[11]/handling[4] # i m/s
    speed = virkning[8]*255/design[12]
    transport.TransportGo(speed)
                     
    virkning[9] = tilstand[16]
    if virkning[9] == 1:
        sikkerhedsventil.sikkerhedsventilOn()
    else:
        sikkerhedsventil.sikkerhedsventilOff()
    
    if virkning[8] > 0:
        virkning[5] = 1
        if (pause == 0) and (virkning[5] == 1):
            IRremote.TVpause()
            pause = 1
        virkning[10] = 1
        powernet.Relay4on()
        virkning[11] = 1
        powernet.Relay4on()
    else:
        virkning[5] = 0
        if (pause == 1) and (virkning[5] == 0):
            IRremote.TVpause()
            pause = 0
        virkning[10] = 0
        powernet.Relay4off()
        virkning[11] = 0
        powernet.Relay4off()

    #virkning[12] anvendes kun i initialiseringen

    virkning[14] = max(handling[5], handling[6], handling[7])
    channel5.set_volume(virkning[14]/100,0)
    if not channel5.get_busy():
        channel5.play(lyd.vand,loop=-1)
        
    if ((tilstand[5] > design[1]) or (tilstand[1] > design[4])):
        virkning[15] = 100
    else:
        virkning[15] = 0

    channel11.set_volume(virkning[15]/100,0)
    if not channel11.get_busy():
        channel11.play(lyd.vandpjask, loop=-1)

    if tilstand[16] == 1:
        virkning[16] = 100
    else:
        virkning[16] = 0

    channel7.set_volume(virkning[16]/100,0)
    if not channel7.get_busy():
        channel7.play(lyd.sikkerhedsventil, loop=-1)

    if tilstand(1) < 1:
        virkning[17] = 100-100*tilstand[1]
    else:
        virkning[17] = 0

    channel8.set_volume(virkning[17]/100,0)
    if not channel8.get_busy():
        channel8.play(lyd.maskinpiv, loop=-1)

    if tilstand[1] < 0.1:
        virkning[18] = 100
        virkning[1] = 0
    else:
        virkning[18] = 0

    channel9.set_volume(virkning[18]/100,0)
    if not channel9.get_busy():
        channel9.play(lyd.maskinhaveri, loop=0)

    #virkning[19] anvendes kun i initialiseringen

    if tid <= 1:
        if virkning[21] != 101:
            virkning[21] = 101
            channel3.set_volume(1,0)
            channel3.play(lyd.flute, loop=0)
            time.sleep(5)
            channel3.set_volume(0,1)
            channel3.play(lyd.skipper01, loop=0)
            callTime = tid


    if tid == 300:
        if virkning[20] != 8:
            virkning[20] = 8
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0, maxtime=1000)
            servo.maskintelegraf_FF()
            time.sleep(1)
            channel3.play(lyd.maskinteleraf, loop=0, maxtime=1000)
            servo.maskintelegraf_FB()
            time.sleep(1)
            channel3.play(lyd.maskintelegraf, loop=0, maxtime=1000)
            servo.maskintelegraf_FS()
            time.sleep(1)
            
    if (tid > 305) and (tid <= 315):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LF()

    if (tid > 315) and (tid <= 325):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LB()

    if (tid > 325) and (tid <= 345):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LF()

    if (tid > 345) and (tid <= 390):
        if virkning[20] != 2:
            Virkning[20] = 2
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_HF()

    if (tid > 390) and (tid < 965):
        if virkning[20] != 1:
            virkning[20] = 1
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_FF()

    if tid == 900:
        if virkning[21] != 102:
            virkning[21] = 102
            channel3.set_volume(1,0)
            channel3.play(lyd.flute, loop=0)
            time.sleep(5)
            channel3.set_volume(0,1)
            channel3.play(lyd.skipper02, loop=0)
            callTime = tid

    if tid == 965:
        if virkning[20] != 8:
            virkning[20] = 8
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0, maxtime=1000)
            servo.maskintelegraf_FF()
            time.sleep(1)
            channel3.play(lyd.maskinteleraf, loop=0, maxtime=1000)
            servo.maskintelegraf_FB()
            time.sleep(1)
            channel3.play(lyd.maskintelegraf, loop=0, maxtime=1000)
            servo.maskintelegraf_FS()
            time.sleep(1)
            
    if (tid > 968) and (tid <= 1033):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LF()

    if (tid > 1033) and (tid <= 1055):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LB()

    if (tid > 1055) and (tid <= 1092):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LF()

    if (tid > 1092) and (tid <= 1118):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LB()

    if (tid > 1118) and (tid <= 1231):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LF()

    if (tid > 1231) and (tid <= 1259):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LB()

    if (tid > 1259) and (tid <= 1290):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LF()

    if (tid > 1290) and (tid <= 1317):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LB()

    if (tid > 1317) and (tid <= 1387):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LF()

    if (tid > 1387) and (tid <= 1403):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LB()

    if (tid > 1403) and (tid <= 1630):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_LF()

    if tid > 1603:
        if virkning[20] != 4:
            virkning[20] = 4
            channel3.set_volume(1,0)
            channel3.play(lyd.maskintelegraf, loop=0)
            servo.maskintelegraf_FS()

    if tid == 1630:
        if virkning[21] != 103:
            virkning[21] = 103
            channel3.set_volume(1,0)
            channel3.play(lyd.flute, loop=0)
            time.sleep(5)
            channel3.set_volume(0,1)
            channel3.play(lyd.skipper03, loop=0)
            callTime = tid

    # Haandtering af haendelsesafhaengige ordrer: Gal retning

    if ((virkning[20] in [1,2,3]) and (virkning[0] < 50)) or ((virkning[20] in [5,6,7]) and (virkning[0] > 50)):
        galRetning = 1
    else:
        galRetning = 0

    if (galRetning == 1) and (galRetningTid == 0):
        galRetningTid = tid

    if ((tid - galRetningTid) > 15) and ((tid - callTime) > 30) and (galRetning == 1):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.skipper04, loop=0)
        time.sleep(3)
        if virkning[20] in [1,2,3]:
            channel3.play(lyd.skipper06, loop=0)
        else:
            channel3.play(lyd.skipper05, loop=0)
        galRetningTid = 0
        callTime = tid

    # Haandtering af haendelsesafhaengige ordrer: Gal hastighed

    if (virkning[20] == 4) and (virkning[0] > 5) and (galHastighed == 0):
        galHastighed = 1
    else:
        galHastighed = 0

    if ((virkning[20] in [1,7]) and (virkning[1] <= 66) and (galHastiged == 0)):
        galHastighed = 2
    else:
        galHastighed = 0

    if ((virkning[20] in [2,6]) and ((virkning[1] > 66) or (virkning[1] < 33)) and (galHastighed == 0)):
        galHastighed = 3
    else:
        galHastighed = 0

    if ((virkning[20] in [3,5]) and (virkning[1] >= 33) and (galHastighed == 0)):
        galHastighed = 4
    else:
        galHastighed = 0

    if (virkning[20] in [1,2,3,5,6,7]) and (virkning[1] == 0) and (galHastighed == 0):
        galHastighed = 5
    else:
        galHastighed = 0

    if (galHastighed > 0) and (galHastighedTid == 0):
        galHastighedTid = tid

    if (((tid - galHastighedTid) > 15) and ((tid - callTime) > 30) and (galHastighed > 0)):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        if (galHastighed == 1):
            channel3.play(lyd.skipper15, loop=0)
        if (galHastighed == 2):
            channel3.play(lyd.skipper07, loop=0)
            time.sleep(2)
            if virkning[20] == 1:
                channel3.play(lyd.skipper09, loop=0)
            if virkning[20] == 7:
                channel3.play(lyd.skipper12, loop=0)
        if (galHastighed == 3):
            if virkning[1] > 66:
                channel3.play(lyd.skipper08, loop=0)
                time.sleep(2)
                if virkning[20] == 2:
                    channel3.play(lyd.skipper10, loop=0)
                if virkning[20] == 6:
                    channel3.play(lyd.skipper13, loop=0)
            if virkning[1] < 33:
                channel3.play(lyd.skipper07, loop=0)
                time.sleep(2)
                if virkning[20] == 2:
                    channel3.play(lyd.skipper10, loop=0)
                if virkning[20] == 6:
                    channel3.play(lyd.skipper13, loop=0)
        if (galHastighed == 4):
            channel3.play(lyd.skipper08, loop=0)
            time.sleep(2)
            if virkning[20] == 3:
                channel3.play(lyd.skipper11, loop=0)
            if virkning[20] == 5:
                channel3.play(lyd.skipper14, loop=0)
        if (galHastighed == 5):
            channel3.play(lyd.skipper16, loop=0)
        galHastighed = 0
        galHastighedTid = 0

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

    if (fejlBetjening > 0) and (fejlBetjeningTid == 0):
        fejlBetjeningTid = tid

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 1):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief01, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 2):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief02, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 3):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief03, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0
            
    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 4):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief04, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0    

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 5):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief05, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0    
        
    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 6):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief06, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0     
        
    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 7):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief07, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0   

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 8):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief08, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0   
                                     
    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 9):
        channel3.set_volume(1,0)
        channel3.play(lyd.flute, loop=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(lyd.chief09, loop=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0    
    


    

    



    
