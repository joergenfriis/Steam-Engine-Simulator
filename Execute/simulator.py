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
# tilstand[24] = Roegtemperatur i skorsten
#
# virkning[0] = Omstyringens stilling paa modellen (0-100)
# virkning[1] = Modellens omdrejningshastighed (0-100%)
# virkning[2] = Oliestand i skueroer (0-100%)
# virkning[3] = Roeggastemperatur (50-650 grader)
# virkning[4] = Kedelvand i skueroer (0-100%)
# virkning[5] = Film i kooeje (1/0: afspilning eller pause)
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
# Joergen Friis 19.01.2018
#
#############################################################################

import pygame
import math
import time
import sys
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
import oliepumpe
import sekundaerLuft

print("Starter simulatorprogram")

# Initiering af simulatoren ################################################

print("Initiering")

time.sleep(10)

design = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
handling = [0,1,2,3,4,5,6,7,8,9,10,11]
tilstand = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
virkning = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]


servoTryk.vis(0.5,5) #For at faa instrumenterne til at falde til ro
                        # her kommer en tilsvarende linje til roegtemperatur

powernet.RelayAlloff()

# Saet designparametre

design[0] = 1
design[1] = 8900
design[2] = 32000
design[3] = 2
design[4] = 5
design[5] = 0.1
design[6] = 5
design[7] = 10
design[8] = 10
design[9] = 10
design[10] = 0.66
design[11] = 1.4
design[12] = 0.7
design[13] = 0.000278

# Aflaes handlinger

handling[0] = omstyring.Read_omstyring()
handling[1] = oliepumpe.Read_flowmaaler() * design[5]
handling[2] = primaerluft.Read_primaerluft()
handling[3] = sekundaerLuft.Read_sekundaerluft()
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
    design[8] = 50
    design[13] = 0.0333
    tilstand[13] = 95
else:
    design[8] = 10
    design[13] = 0.000278
    tilstand[13] = 40

# beregn tilstanden

tilstand[0] = 50
tilstand[1] = 0.5 * design[4]
tilstand[2] = 0
tilstand[3] = 0
tilstand[4] = 0
tilstand[5] = 0.5 * design[1]
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
tilstand[24] = 0

# beregn virkningerne

virkning[0] = 50
virkning[1] = 0
virkning[2] = int((tilstand[1]/design[4])*100)
virkning[3] = 0
virkning[4] = int((tilstand[5]/design[1])*100)
virkning[5] = 0
virkning[6] = 1
virkning[7] = 0
virkning[8] = 0
virkning[9] = 0
virkning[10] = 0
virkning[11] = 0
virkning[12] = 30
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
time.sleep(30)
IRremote.TVonOff()
time.sleep(10)
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
IRremote.TVpause()
pause=1                             # Naar pause=1 er billedet pauset
time.sleep(1)

# Start lydanlaegene

powernet.Relay5on()
time.sleep(1)
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

baggrund = pygame.mixer.Sound("Sound/maskinrumStart.ogg")
assens = pygame.mixer.Sound("Sound/anloebAssens.ogg")
pumpe = pygame.mixer.Sound("Sound/multiPumpe.ogg")
dampflute = pygame.mixer.Sound("Sound/dampfloejte.ogg")
damp = pygame.mixer.Sound("Sound/dampUd.ogg")
luft = pygame.mixer.Sound("Sound/luftUd.ogg")
langsom = pygame.mixer.Sound("Sound/langsom.ogg")
halvKraft = pygame.mixer.Sound("Sound/halvKraft.ogg")
fuldKraft = pygame.mixer.Sound("Sound/fuldKraft.ogg")
vand = pygame.mixer.Sound("Sound/vandIroer.ogg")
vandpjask = pygame.mixer.Sound("Sound/vandPjask.ogg")
overtryksventil = pygame.mixer.Sound("Sound/overtryksventil.ogg")
maskinpiv = pygame.mixer.Sound("Sound/maskinKnirk.ogg")
maskinhaveri = pygame.mixer.Sound("Sound/maskinSammenbrud.ogg")
maskintelegraf = pygame.mixer.Sound("Sound/maskintelegraf.ogg")
flute = pygame.mixer.Sound("Sound/floejteTelegraf.ogg")
skipper01 = pygame.mixer.Sound("Sound/skipper01.ogg")
skipper02 = pygame.mixer.Sound("Sound/skipper02.ogg")
skipper03 = pygame.mixer.Sound("Sound/skipper03.ogg")
skipper04 = pygame.mixer.Sound("Sound/skipper04.ogg")
skipper05 = pygame.mixer.Sound("Sound/skipper05.ogg")
skipper06 = pygame.mixer.Sound("Sound/skipper06.ogg")
skipper07 = pygame.mixer.Sound("Sound/skipper07.ogg")
skipper08 = pygame.mixer.Sound("Sound/skipper08.ogg")
skipper09 = pygame.mixer.Sound("Sound/skipper09.ogg")
skipper10 = pygame.mixer.Sound("Sound/skipper10.ogg")
skipper11 = pygame.mixer.Sound("Sound/skipper11.ogg")
skipper12 = pygame.mixer.Sound("Sound/skipper12.ogg")
skipper13 = pygame.mixer.Sound("Sound/skipper13.ogg")
skipper14 = pygame.mixer.Sound("Sound/skipper14.ogg")
skipper15 = pygame.mixer.Sound("Sound/skipper15.ogg")
skipper16 = pygame.mixer.Sound("Sound/skipper16.ogg")
chief01 = pygame.mixer.Sound("Sound/chief01.ogg")
chief02 = pygame.mixer.Sound("Sound/chief02.ogg")
chief03 = pygame.mixer.Sound("Sound/chief03.ogg")
chief04 = pygame.mixer.Sound("Sound/chief04.ogg")
chief05 = pygame.mixer.Sound("Sound/chief05.ogg")
chief06 = pygame.mixer.Sound("Sound/chief06.ogg")
chief07 = pygame.mixer.Sound("Sound/chief07.ogg")
chief08 = pygame.mixer.Sound("Sound/chief08.ogg")
chief09 = pygame.mixer.Sound("Sound/chief09.ogg")

if (handling[11] != 0):
    channel1.set_volume(virkning[12]/100,0)        # spiller kun i venstre kanal = maskinrum
    channel1.play(baggrund, loops = -1)     # spiller uendeligt

# Udfoer alle virkninger
model.ModelRun(virkning[1],virkning[0])
time.sleep(1)
skueglasOlie.set(virkning[2])
time.sleep(1)
servo.smokeTemp(virkning[3])
time.sleep(1)
skueglasKedel.set(virkning[4])
time.sleep(1)
servoTryk.vis(virkning[6],virkning[7])
time.sleep(1)
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
indpumpetFoer = 0
startTid = int(time.clock())

powernet.Relay10on()  #Simulator klar lys


# Drift af simulatoren ######################################################

while True:
    time.sleep(design[0]) 
    tid = tid + 1
    realTid = int(time.clock()) - startTid

    # REGISTRER HANDLINGER  ####################################################
    handling[0] = omstyring.Read_omstyring()
    handling[1] = oliepumpe.Read_flowmaaler() * design[5]
    handling[2] = primaerluft.Read_primaerluft()
    handling[3] = sekundaerLuft.Read_sekundaerluft()
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

    # Omstyring

    tilstand[0] = handling[0]

    # Flyveaske i roer

    tilstand [11] = (tid-tilstand [12]) * design [13]
    
    # Energiproduktion

    if (handling[4]<0.5):
        print("Energiproduktion valg 1")
        tilstand[2] = 0
        #virkning[8] = 0
        tilstand[3] = design[2]*(100-tilstand[11])/100
        tilstand[10] = 0
        tilstand[4] = 40

    if ((handling[4] >= 0.5) and (handling[4] < 22.5) and (handling[3] <= 10)):
        print("Energiproduktion valg 2")
        tilstand[2] = (handling[2]+handling[3])*27.3/20/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-4*(10-handling[3]))*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

    if ((handling[4] >= 0.5) and (handling[4] < 22.5) and (handling[3] > 10)):
        print("Energiproduktion valg 3")
        tilstand[2] = (handling[2]+10)*27.3/20/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

    if ((handling[4] >= 22.5) and (handling[4] < 45) and (handling[3] <= 10)):
        print("Energiproduktion valg 4")
        tilstand[2] = ((handling[2]*(100-(handling[4]-22.5)*100/22.5)/100)+handling[3])*27.3/20/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-4*(10-handling[3]))*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

    if ((handling[4] >= 22.5) and (handling[4] < 45) and (handling[3] > 10)):
        print("Energiproduktion valg 5")
        tilstand[2] = ((handling[2]*(100-(handling[4]-22.5)*100/22.5)/100)+10)*27.3/20/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

    if ((handling[4] > 45) and (handling[3] <= 10)):
        print("Energiproduktion valg 6")
        tilstand[2] = handling[3]*27.3/20/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-4*(10-handling[3]))*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

    if((handling[4] > 45) and (handling[3] > 10)):
        print("Energiproduktion valg 7")
        tilstand[2] = 10*27.3/20/3600
        #virkning[8] = tilstand[2]*design[11]/handling[4]
        tilstand[3] = design[2]*(100-tilstand[11])/100
        tilstand[10] = tilstand[2]*tilstand[3]
        tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

    # Dampproduktion eller fortaetning

    lnTryk = math.log(tilstand[6] +1)
    print("lnTryk = ",lnTryk)
    potensTryk = math.pow(tilstand[6]+1,-0.939)
    print("potensTryk = ",potensTryk)

    print("tilstand[13], kedeltemperatur, = ",tilstand[13])
    print("ligevaegtstemperatur: 27.606 * lnTryk + 100 = ",27.606 * lnTryk + 100)
    
    while ((int(tilstand[13]) != int(27.606 * lnTryk + 100)) and (tilstand[13] > 100)):
        print("Ej ligevaegt")

        if int(tilstand[13]) > int(27.606 * lnTryk + 100):
            print("for varm")
            print("tilstand[5], liter vand i kedel, foer = ",tilstand[5])
            if tilstand[5] >1:
                tilstand[5] = tilstand[5] - 1
            print("tilstand[5], liter vand i kedel, efter = ",tilstand[5])
            tilstand[13] = tilstand[13] - (531.33 - 18.22 * lnTryk)/4.186 / tilstand[5]
            print("tilstand[13], kedeltemperatur, efter = ",tilstand[13])
            V = 1.7259 * potensTryk
            print("V, volumen af dannet damp = ",V)
            Vd = (design[1] - tilstand[5])/1000
            print("Vd, volumen af damprummet = ",Vd)
            print("tilstand[6], kedeltryk i bar overtryk, foer = ",tilstand[6])
            tilstand[6] = tilstand[6] + V/Vd
            print("tilstand[6], kedeltryk i bar overtryk, efter = ",tilstand[6])

        if int(tilstand[13]) < int(27.606 * lnTryk + 100):
            print("for kold")
            print("tilstand[5], liter vand i kedel, foer = ",tilstand[5])
            tilstand[5] = tilstand[5] + 1
            print("tilstand[5], liter vand i kedel, efter = ",tilstand[5])
            tilstand[13] = tilstand[13] + (531.33 - 18.22 * lnTryk)/4.186 / tilstand[5]
            print("tilstand[13], kedeltemperatur, efter = ",tilstand[13])
            V = 1.7259 * potensTryk
            print("V, volumen af fortaettet damp = ",V)
            Vd = (design[1] - tilstand[5])/1000
            print("Vd, volumen af damprummet = ",Vd)
            print("tilstand[6], kedeltryk i bar overtryk, foer = ",tilstand[6])
            tilstand[6] = tilstand[6] - V/Vd
            print("tilstand[6], kedeltryk i bar overtryk, efter = ",tilstand[6])

    if (virkning[8] > 0):
        tilstand[13] = tilstand[13] + tilstand[10] * 1/4.186/ tilstand[5]
        print("Kedeltemperatur efter indfyring = ",tilstand[13])

    if (virkning[8] <= 0):
        tilstand[13] = tilstand[13] - 31.2 * (tilstand[13] - 20) * 70 * 4.184/3600 * 1/4.186/tilstand[5]
        print("Kedeltemperatur efter afkoeling = ",tilstand[13])
        
    # Roeggastemperatur i skorsten

    if ((handling[3] <= 10) and (tilstand[2]>0)):
        tilstand[24] = tilstand[13] + 50

    if ((handling[3] > 10) and (tilstand[2]>0)):
        tilstand[24] = tilstand[13] + 50 - 30*(handling[3]/100)

    tilstand[24] = tilstand[24] + (600-tilstand[24])* tilstand[11]/100

    # Dampdistribution

    if (tilstand[6] > 10):
        tilstand[16] = 1

    tilstand[17] = ((design[1] - tilstand[5]) / 1000) / 1.7295 * potensTryk

    if ((handling[9]+handling[10]+tilstand[16]) == 0):
        tilstand[18] = 0
        tilstand[19] = 0
    else:
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
    print("tilstand[5] foer = ",tilstand[5])
    tilstand[5] = tilstand[5] + (((handling[5]/100)*design[8]) - ((handling[6]/100)*design[8]) + tilstand[20])
    print("tilstand[5] efter = ",tilstand[5])
    # Maskinydelse

    tilstand[8] = int(100*(tilstand[18]/0.29)*(tilstand[6]-tilstand[22])/10*math.fabs(tilstand[0]-50)*handling[8])
                                                                           
    # Oliebalance

    tilstand[1] = tilstand[1] + handling[1]-indpumpetFoer - design[3]*tilstand[8]
    indpumpetFoer = handling[1]


    # BEREGN OG UDFOER VIRKNINGER  ###########################################################################

    virkning[0] = handling[0]
    servo.gangskifte(virkning[0])
                    
    virkning[1] = tilstand[8]
    model.ModelRun(virkning[1],virkning[0])
    channel2.set_volume(virkning[1],0)   
    if (virkning[1] > 0) and (virkning[1] <= 33):
        channel2.play(langsom, loops=-1)
    if (virkning[1] > 33) and (virkning[1] <=66):
        channel2.play(halvKraft, loops=-1)
    if (virkning[1] > 66):
        channel2.play(fuldKraft, loops=-1)
    
    virkning[2] = int(tilstand[1]/design[4]*100)
    if virkning[2] > 100:
        virkning[2] = 100
    skueglasOlie.set(virkning[2])
    
    virkning[3] = tilstand[24]
    # Er ikke programmeret endnu på Arduino og i Python. Afventer printplader.
                     
    virkning[4] = int(tilstand[5]/design[1]*100)
    if virkning[4] > 100:
        virkning[4] = 100
    skueglasKedel.set(virkning[4])

    virkning[6] = tilstand[22]
    virkning[7] = tilstand[6]
    servoTryk.vis(virkning[6],virkning[7])
                     
    virkning[8] = tilstand[2]*design[11]/handling[4] # i m/s. Paa et senere tidspunkt skal denne algoritme aendres til intervaldrift.
    speed = int(virkning[8]*255/design[12])
    if speed < 3:
        speed = 0
    if (speed >= 3) and (speed < 15):
        speed = 15
    if speed >= 15:
        speed = speed
    transport.TransportGo(speed)
                     
    virkning[9] = tilstand[16]
    if virkning[9] == 1:
        sikkerhedsventil.sikkerhedsventilOn()
    else:
        sikkerhedsventil.sikkerhedsventilOff()
    
    if virkning[8] > 0:
        virkning[5] = 1
        if (pause == 1):
            IRremote.TVpause()
            pause = 0
        virkning[10] = 1
        powernet.Relay4on()
        virkning[11] = 1
        powernet.Relay4on()
    else:
        virkning[5] = 0
        if (pause == 0):
            IRremote.TVpause()
            pause = 1
        virkning[10] = 0
        powernet.Relay4off()
        virkning[11] = 0
        powernet.Relay4off()

    #virkning[12] anvendes kun i initialiseringen

    virkning[14] = max(handling[5], handling[6], handling[7])
    channel5.set_volume(virkning[14]/100,0)
    if not channel5.get_busy():
        channel5.play(vand,loops=-1)
        
    if ((tilstand[5] > design[1]) or (tilstand[1] > design[4])):
        virkning[15] = 100
    else:
        virkning[15] = 0

    channel11.set_volume(virkning[15]/100,0)
    if not channel11.get_busy():
        channel11.play(vandpjask, loops=-1)

    if tilstand[16] == 1:
        virkning[16] = 100
    else:
        virkning[16] = 0

    channel7.set_volume(virkning[16]/100,0)
    if not channel7.get_busy():
        channel7.play(overtryksventil, loops=-1)

    if tilstand[1] < 1:
        virkning[17] = 100-100*tilstand[1]
    else:
        virkning[17] = 0

    channel8.set_volume(virkning[17]/100,0)
    if not channel8.get_busy():
        channel8.play(maskinpiv, loops=-1)

    if tilstand[1] < 0.1:
        virkning[18] = 100
        virkning[1] = 0
    else:
        virkning[18] = 0

    channel9.set_volume(virkning[18]/100,0)
    if not channel9.get_busy():
        channel9.play(maskinhaveri, loops=0)

    #virkning[19] anvendes kun i initialiseringen

    if realTid <= 1:
        if virkning[21] != 101:
            virkning[21] = 101
            channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(5)
            channel3.set_volume(0,1)
            channel3.play(skipper01, loops=0)
            callTime = tid


    if realTid == 300:
        if virkning[20] != 8:
            virkning[20] = 8
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0, maxtime=1000)
            servo.maskintelegraf_FF()
            time.sleep(1)
            channel3.play(maskintelegraf, loops=0, maxtime=1000)
            servo.maskintelegraf_FB()
            time.sleep(1)
            channel3.play(maskintelegraf, loops=0, maxtime=1000)
            servo.maskintelegraf_FS()
            time.sleep(1)
            
    if (realTid > 305) and (tid <= 315):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LF()

    if (realTid > 315) and (tid <= 325):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LB()

    if (realTid > 325) and (tid <= 345):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LF()

    if (realTid > 345) and (tid <= 390):
        if virkning[20] != 2:
            Virkning[20] = 2
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_HF()

    if (realTid > 390) and (tid < 965):
        if virkning[20] != 1:
            virkning[20] = 1
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_FF()

    if realTid == 900:
        if virkning[21] != 102:
            virkning[21] = 102
            channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(5)
            channel3.set_volume(0,1)
            channel3.play(skipper02, loops=0)
            callTime = tid

    if realTid == 965:
        if virkning[20] != 8:
            virkning[20] = 8
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0, maxtime=1000)
            servo.maskintelegraf_FF()
            time.sleep(1)
            channel3.play(maskinteleraf, loops=0, maxtime=1000)
            servo.maskintelegraf_FB()
            time.sleep(1)
            channel3.play(maskintelegraf, loops=0, maxtime=1000)
            servo.maskintelegraf_FS()
            time.sleep(1)
            
    if (realTid > 968) and (realTid <= 1033):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LF()

    if (realTid > 1033) and (realTid <= 1055):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LB()

    if (realTid > 1055) and (realTid <= 1092):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LF()

    if (realTid > 1092) and (realTid <= 1118):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LB()

    if (realTid > 1118) and (realTid <= 1231):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LF()

    if (realTid > 1231) and (realTid <= 1259):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LB()

    if (realTid > 1259) and (realTid <= 1290):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LF()

    if (realTid > 1290) and (realTid <= 1317):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LB()

    if (realTid > 1317) and (realTid <= 1387):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LF()

    if (realTid > 1387) and (realTid <= 1403):
        if virkning[20] != 5:
            virkning[20] = 5
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LB()

    if (realTid > 1403) and (realTid <= 1630):
        if virkning[20] != 3:
            virkning[20] = 3
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_LF()

    if realTid > 1603:
        if virkning[20] != 4:
            virkning[20] = 4
            channel3.set_volume(1,0)
            channel3.play(maskintelegraf, loops=0)
            servo.maskintelegraf_FS()

    if realTid == 1630:
        if virkning[21] != 103:
            virkning[21] = 103
            channel3.set_volume(1,0)
            channel3.play(flute, loops=0)
            time.sleep(5)
            channel3.set_volume(0,1)
            channel3.play(skipper03, loops=0)
            callTime = tid

    # Haandtering af haendelsesafhaengige ordrer: Gal retning

    if ((virkning[20] in [1,2,3]) and (virkning[0] < 50)) or ((virkning[20] in [5,6,7]) and (virkning[0] > 50)):
        galRetning = 1
    else:
        galRetning = 0

    if (galRetning == 1) and (galRetningTid == 0):
        galRetningTid = realTid

    if ((tid - galRetningTid) > 15) and ((tid - callTime) > 30) and (galRetning == 1):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(skipper04, loops=0)
        time.sleep(3)
        if virkning[20] in [1,2,3]:
            channel3.play(skipper06, loops=0)
        else:
            channel3.play(skipper05, loops=0)
        galRetningTid = 0
        callTime = realTid

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
        galHastighedTid = realTid

    if (((tid - galHastighedTid) > 15) and ((tid - callTime) > 30) and (galHastighed > 0)):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        if (galHastighed == 1):
            channel3.play(skipper15, loops=0)
        if (galHastighed == 2):
            channel3.play(skipper07, loops=0)
            time.sleep(2)
            if virkning[20] == 1:
                channel3.play(skipper09, loops=0)
            if virkning[20] == 7:
                channel3.play(skipper12, loops=0)
        if (galHastighed == 3):
            if virkning[1] > 66:
                channel3.play(skipper08, loops=0)
                time.sleep(2)
                if virkning[20] == 2:
                    channel3.play(skipper10, loops=0)
                if virkning[20] == 6:
                    channel3.play(skipper13, loops=0)
            if virkning[1] < 33:
                channel3.play(skipper07, loops=0)
                time.sleep(2)
                if virkning[20] == 2:
                    channel3.play(skipper10, loops=0)
                if virkning[20] == 6:
                    channel3.play(skipper13, loops=0)
        if (galHastighed == 4):
            channel3.play(skipper08, loops=0)
            time.sleep(2)
            if virkning[20] == 3:
                channel3.play(skipper11, loops=0)
            if virkning[20] == 5:
                channel3.play(skipper14, loops=0)
        if (galHastighed == 5):
            channel3.play(skipper16, loops=0)
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
        fejlBetjeningTid = realTid
    else:
        fejlBetjeningTid = 0

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 1):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief01, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 2):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief02, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 3):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief03, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0
            
    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 4):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief04, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0    

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 5):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief05, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0    
        
    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 6):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief06, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0     
        
    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 7):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief07, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0   

    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 8):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief08, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0   
                                     
    if ((tid - fejlBetjeningTid) > 15) and ((tid - callTime) > 30) and (fejlBetjening == 9):
        channel3.set_volume(1,0)
        channel3.play(flute, loops=0)
        time.sleep(3)
        channel3.set_volume(0,1)
        channel3.play(chief09, loops=0)
        fejlBetjening = 0
        fejlBetjeningTid = 0    
    

  # DEBUGGING  ###############################################################################

    print("Cyklusser = ",tid)
    print("Real tid = ",realTid)

    for i in range(0,12):
        print("Handling[",i,"] = ",handling[i])

    print("******************************************************")
    
    for i in range(0,25):
        print("Tilstand[",i,"] = ",tilstand[i])

    print("******************************************************")

    for i in range(0,24):
        print("Virkning[",i,"] = ",virkning[i])

    print("******************************************************")


  
    

    



    
