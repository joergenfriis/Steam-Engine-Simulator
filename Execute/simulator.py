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
# design[1] = Kedelrumfang i liter (realistisk 7.690 l, paedagogisk 500 l)
# design[2] = Brandvaerdi af kul (32.000 kJ/kg)
# design[3] = Smoereolieforbrug pr time ved 100 % maskinydelse (2 liter)
# design[4] = Rumfang af smoereolietank (5 liter)
# design[5] = Skalering af oliepumpe (0.1)
# design[6] = Kedelvandstab (5 % af det tilfoerte damp kommer ikke retur)
# design[7] = Overtryksventil paa kedel (blaeser ved 10 bar)
# design[8] = Kedelvandshaner max flow i liter/sek
# design[9] = Kondensvandshaner max flow i liter/sek
# design[10] = Damphaner max flow i kg/sek
# design[11] = Laengde af transportbaand i meter
# design[12] = Max hastighed af transportbaand i meter/sek
# design[13] = Flyveaskeaflejring (tilstopning) % pr sekund
# design[14] = Max dampforbrug i maskine (kg/sek)
# design[15] = Starttemperatur i kedel
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
# tilstand[6] = Damptryk i bar (bar abs)
# tilstand[7] = luft i damprummet (0/1)
# tilstand[8] = Maskinydelse (0-100)
# tilstand[9] = Maskintelegraf (0-6)
# tilstand[10] = Indfyret effekt i kJ/sekund
# tilstand[11] = flyveaske i roegroer (0-100)
# tilstand[12] = tidspunkt for sidste rensning af roegroer
# tilstand[13] = vandtemperatur i kedel
# tilstand[14] = akummuleret damp ind til maskinen (kg)
# tilstand[15] = akkumuleret damp ud til atmosfaeren (kg)
# tilstand[16] = sikkerhedsventil aaben/lukket 1/0
# tilstand[17] = damp til raadighed i kedlen (kg)
# tilstand[18] = damp til raadighed for maskinen (kg)
# tilstand[19] = damp der lukkes ud til det fri (kg)
# tilstand[20] = Kondensat i kg/sek
# tilstand[21] = Temperatur i kondensator
# tilstand[22] = Tryk i kondensator
# tilstand[23] = forbrugt oliemaengde i liter/time
# tilstand[24] = Roegtemperatur i skorsten
# tilstand[25] = Enthalpi i kedlen
# tilstand[26] = Klar til sejlads (0/1)
#
# virkning[0] = Omstyringens stilling paa modellen (0-100)
# virkning[1] = Modellens omdrejningshastighed (0-100%)
# virkning[2] = Oliestand i skueroer (0-100%)
# virkning[3] = Roeggastemperatur (50-650 grader)
# virkning[4] = Kedelvand i skueroer (0-100%)
# virkning[5] = Film i kooeje (1/0: afspilning eller pause)
# virkning[6] = Vacuum i kondensator (0-1 bar)
# virkning[7] = Kedeltryk (0-10 bar overtryk)
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
# virkning[23] = Lyd af damp i roer
# virkning[24] = Aktivering af roegmaskine (1/0)
# virkning[25] = Lyd af dampfloejte (0-100%)
# 
#
# Joergen Friis 05.02.2018
#
#############################################################################

import pygame
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
import servoTemp
import sikkerhedsventil
import oliepumpe
import sekundaerLuft
import damptabel

def start(valg):
    print("Koerer hovedprogram ",valg)

    # Initiering af simulatoren ############################################

    print("Initialisering")

    design = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    handling = [0,1,2,3,4,5,6,7,8,9,10,11]
    tilstand = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
    virkning = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

    dampTabel = damptabel.damptabel
    tilstandTabel = damptabel.dampTilstand
    
    # Saet designparametre

    design[0] = 1       # Skal overvejes naar alt andet virker
    design[1] = 8900
    design[2] = 32000
    design[3] = 2
    design[4] = 5
    design[5] = 0.1
    design[6] = 5
    design[7] = 10
    design[8] = design[1]/200   # Er fastsat saa skueroeret kan foelge med.
    design[9] = 10
    design[10] = 0.75  # Svarer til 140% af den damp der kan dannes pr sek.
    design[11] = 1.4
    design[12] = 0.7
    design[13] = 0.000278
    design[14] = 0.29
    design[15] = 95

    # Aflaes handlinger

    handling[0] = omstyring.Read_omstyring()
    handling[1] = oliepumpe.Read_flowmaaler() * design[5]
    handling[2] = primaerluft.Read_primaerluft()
    primaerluftKorrektion = handling[2]                 # Til brug for 0-stilling af enkoder
    print("Primaerluft korrektion = ",primaerluftKorrektion)
    handling[3] = sekundaerLuft.Read_sekundaerluft()
    handling[4] = vejecelle.Read_vejecelle() / 1000
    handling[5] = ventiler.readKedelvandInd()
    handling[6] = ventiler.readKedelvandUd()
    handling[7] = ventiler.readKondensatorvandInd()
    handling[8] = ventiler.readKondensatorvandUd()
    handling[9] = ventiler.readDampInd()
    handling[10] = ventiler.readDampUd()
    handling[11] = programvalg.read()

    if handling[11] != valg:
        return

    # aflaes programvaelger og juster designparametre tilsvarende

    if ((handling[11] == 2) or (handling[11] == 4)):
        design[1] = 500
        design[3] = 20
        design[6] = 0.1
        design[8] = design[1]/200
        design[13] = 0.0333
        design[14] = 0.29
        design[15] = 95
    else:
        design[1] = 7690
        design[3] = 2
        design[6] = 5
        design[8] = design[1]/200
        design[13] = 0.000278
        design[14] = 0.29
        design[15] = 40

    # beregn tilstanden

    tilstand[0] = 50
    tilstand[1] = 0.5 * design[4]
    tilstand[2] = 0
    tilstand[3] = 0
    tilstand[4] = 0
    tilstand[5] = 0.6 * design[1]
    tilstand[6] = 1
    tilstand[7] = 1
    tilstand[8] = 0
    tilstand[9] = 3
    tilstand[10] = 0
    tilstand[11] = 0
    tilstand[12] = 0
    tilstand[13] = design[15]
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
    tilstand[25] = 0
    tilstand[26] = 0

    # beregn virkningerne

    virkning[0] = 50
    virkning[1] = 0
    virkning[2] = int((tilstand[1]/design[4])*100)
    virkning[3] = 0
    virkning[4] = int((tilstand[5]/design[1])*100)
    virkning[5] = 0
    virkning[6] = 1
    virkning[7] = tilstand[6] - 1
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
    virkning[24] = 1
    virkning[25] = 0

    if programvalg.read() != valg:
        return


    # Beregn kedlens samlede enthalpi i starttilstanden vha damptabellen
    for x in range(len(dampTabel)):
        if dampTabel[x][1] > tilstand[13]:
            break
    enthalpiVand = damptabel.interpol(dampTabel[x-1][1],dampTabel[x-1][3],tilstand[13],dampTabel[x][1],dampTabel[x][3])
    enthalpiDamp = damptabel.interpol(dampTabel[x-1][1],dampTabel[x-1][4],tilstand[13],dampTabel[x][1],dampTabel[x][4])
    volumenDamp = damptabel.interpol(dampTabel[x-1][1],dampTabel[x-1][2],tilstand[13],dampTabel[x][1],dampTabel[x][2])
    tilstand[17] = (((design[1]-tilstand[5])/1000)/volumenDamp)         # kg damp i kedlen
    tilstand[25] = tilstand[5]*enthalpiVand + tilstand[17]*enthalpiDamp # enthalpi i kedlen

    # Toem transportbaandet for kul
    transport.TransportGo(150)  
    time.sleep(5)
    transport.TransportStop()

    # Nulstil vejecellen
    vejecelle.Reset_vejecelle()

    # Nulstil oliepumpen
    oliepumpe.Reset_flowmaaler()

    if programvalg.read() != valg:
        return


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

    if programvalg.read() != valg:
        return


    # Start lydanlaegene

    pygame.mixer.init(channels=2)       # Mixeren saettes til stereo
    pygame.mixer.set_num_channels(12)
    channel1 = pygame.mixer.Channel(0) # Baggrundslyd, der spiller hele tiden
    channel2 = pygame.mixer.Channel(1) # Lyd af hovedmaskinen der koerer
    channel3 = pygame.mixer.Channel(2) # Maskintelegraf og beskedfloejte
    channel4 = pygame.mixer.Channel(3) # Multifunktionspumpe
    channel5 = pygame.mixer.Channel(4) # Lyd af vand i roer
    channel6 = pygame.mixer.Channel(5) # Lyd fra damphaner
    channel7 = pygame.mixer.Channel(6) # Lyd af sikkerhedsventil
    channel8 = pygame.mixer.Channel(7) # Mislyde fra maskinen
    channel9 = pygame.mixer.Channel(8) # Maskinhaveri
    channel10 = pygame.mixer.Channel(9) # Dampfloejte
    channel11 = pygame.mixer.Channel(10) # Vandpjask
    channel12 = pygame.mixer.Channel(11) # Ordrer fra broen

    channel3.set_volume(1.0,0.0)
    channel12.set_volume(0.0,1.0)

    # Try upto 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range(30):
        try:
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
            #skipper04 = pygame.mixer.Sound("Sound/skipper04.ogg")
            #skipper05 = pygame.mixer.Sound("Sound/skipper05.ogg")
            #skipper06 = pygame.mixer.Sound("Sound/skipper06.ogg")
            #skipper07 = pygame.mixer.Sound("Sound/skipper07.ogg")
            #skipper08 = pygame.mixer.Sound("Sound/skipper08.ogg")
            #skipper09 = pygame.mixer.Sound("Sound/skipper09.ogg")
            #skipper10 = pygame.mixer.Sound("Sound/skipper10.ogg")
            #skipper11 = pygame.mixer.Sound("Sound/skipper11.ogg")
            #skipper12 = pygame.mixer.Sound("Sound/skipper12.ogg")
            #skipper13 = pygame.mixer.Sound("Sound/skipper13.ogg")
            #skipper14 = pygame.mixer.Sound("Sound/skipper14.ogg")
            #skipper15 = pygame.mixer.Sound("Sound/skipper15.ogg")
            #skipper16 = pygame.mixer.Sound("Sound/skipper16.ogg")
            #chief01 = pygame.mixer.Sound("Sound/chief01.ogg")
            #chief02 = pygame.mixer.Sound("Sound/chief02.ogg")
            #chief03 = pygame.mixer.Sound("Sound/chief03.ogg")
            #chief04 = pygame.mixer.Sound("Sound/chief04.ogg")
            #chief05 = pygame.mixer.Sound("Sound/chief05.ogg")
            #chief06 = pygame.mixer.Sound("Sound/chief06.ogg")
            #chief07 = pygame.mixer.Sound("Sound/chief07.ogg")
            #chief08 = pygame.mixer.Sound("Sound/chief08.ogg")
            #chief09 = pygame.mixer.Sound("Sound/chief09.ogg")
            Success = True
            break
        except:
            print("Uventet fejl ved aabning af lydfil: ", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Opening of sound file failed after 30 retries")
    
    if programvalg.read() != valg:
        return


    powernet.Relay5on()
    time.sleep(1)

    if (handling[11] != 0):
        channel1.set_volume(virkning[12]/100,0)        # spiller kun i venstre kanal = maskinrum
        channel1.play(baggrund, loops = -1)     # spiller uendeligt

    # Udfoer alle virkninger
    model.ModelReset()
    time.sleep(1)
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

    virkning[19] = 1
    tid = 0
    galRetning = 0
    galRetningTid = 0
    galHastighed = 0
    galHastighedTid = 0
    fejlBetjening = 0
    fejlBetjeningTid = 0
    callTime = 0
    indpumpetFoer = 0
    smokeStart = 0
    roeg = False
    startTid = time.time()

    time.sleep(1)
    powernet.Relay3on()   #Roegmaskine varmer op
    time.sleep(1)
    powernet.Relay10on()  #Simulator klar lys
    time.sleep(1)
    # Initiering faerdig

    # Drift af simulatoren ######################################################

    print("Program start")
    print()

    while handling[11] == valg:
        time.sleep(design[0])
        tid = tid + 1

        if (tilstand[6] > 3) and (tilstand[26] == 0):
            tilstand[26] = 1

        if (tilstand[26] == 0):
            startTid = time.time()
        realTid = int(time.time() - startTid)

        # REGISTRER HANDLINGER  ####################################################
        handling[0] = omstyring.Read_omstyring()
        handling[1] = oliepumpe.Read_flowmaaler() * design[5]
        handling[2] = primaerluft.Read_primaerluft() - primaerluftKorrektion
        if handling[2] > 100:
            handling[2] = 100
        handling[3] = sekundaerLuft.Read_sekundaerluft()
        handling[4] = vejecelle.Read_vejecelle() / 1000
        handling[5] = ventiler.readKedelvandInd()
        handling[6] = ventiler.readKedelvandUd()
        handling[7] = ventiler.readKondensatorvandInd()
        handling[8] = ventiler.readKondensatorvandUd()
        handling[9] = ventiler.readDampInd()
        handling[10] = ventiler.readDampUd()
        handling[11] = programvalg.read()

        # BEREGN TILSTANDE ########################################################

        # Omstyring

        tilstand[0] = handling[0]

        # Flyveaske i roer (deaktiveret indtil sensorerne i roegroererne virker)

        # tilstand [11] = (tid-tilstand [12]) * design [13]
        
        # Energiproduktion

        if (handling[4]<0.5):
            tilstand[2] = 0
            tilstand[3] = design[2]*(100-tilstand[11])/100
            tilstand[10] = 0
            tilstand[4] = 40
                
        if ((handling[4] >= 0.5) and (handling[4] < 22.5) and (handling[3] <= 10)):
            tilstand[2] = (handling[2]+handling[3])*27.3/20/3600
            tilstand[3] = design[2]*((100-4*(10-handling[3]))/100)*(100-tilstand[11])/100
            tilstand[10] = tilstand[2]*tilstand[3]
            tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

        if ((handling[4] >= 0.5) and (handling[4] < 22.5) and (handling[3] > 10)):
            tilstand[2] = (handling[2]+10)*27.3/20/3600
            tilstand[3] = design[2]*(100-tilstand[11])/100
            tilstand[10] = tilstand[2]*tilstand[3]
            tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

        if ((handling[4] >= 22.5) and (handling[4] < 45) and (handling[3] <= 10)):
            tilstand[2] = ((handling[2]*(100-(handling[4]-22.5)*100/22.5)/100)+handling[3])*27.3/20/3600
            tilstand[3] = design[2]*((100-4*(10-handling[3]))/100)*(100-tilstand[11])/100
            tilstand[10] = tilstand[2]*tilstand[3]
            tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

        if ((handling[4] >= 22.5) and (handling[4] < 45) and (handling[3] > 10)):
            tilstand[2] = ((handling[2]*(100-(handling[4]-22.5)*100/22.5)/100)+10)*27.3/20/3600
            tilstand[3] = design[2]*(100-tilstand[11])/100
            tilstand[10] = tilstand[2]*tilstand[3]
            tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

        if ((handling[4] > 45) and (handling[3] <= 10)):
            tilstand[2] = handling[3]*27.3/20/3600
            tilstand[3] = design[2]*((100-4*(10-handling[3]))/100)*(100-tilstand[11])/100
            tilstand[10] = tilstand[2]*tilstand[3]
            tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

        if((handling[4] > 45) and (handling[3] > 10)):
            tilstand[2] = 10*27.3/20/3600
            tilstand[3] = design[2]*(100-tilstand[11])/100
            tilstand[10] = tilstand[2]*tilstand[3]
            tilstand[4] = ((tilstand[3]/4.1868)/(0.24*(1+20)))+18

        # Dampproduktion A -> F
        # A: opslag i damptabellen ved den aktuelle temperatur

        for x in range(len(dampTabel)):
            if dampTabel[x][1] > tilstand[13]:
                break
        enthalpiVandSpc = damptabel.interpol(dampTabel[x-1][1],dampTabel[x-1][3],tilstand[13],dampTabel[x][1],dampTabel[x][3])
        enthalpiDampSpc = damptabel.interpol(dampTabel[x-1][1],dampTabel[x-1][4],tilstand[13],dampTabel[x][1],dampTabel[x][4])
        volumenDampSpc = damptabel.interpol(dampTabel[x-1][1],dampTabel[x-1][2],tilstand[13],dampTabel[x][1],dampTabel[x][2])

        # B: vand ind og ud
        tilstand[5] = tilstand[5] + (handling[5]/100)*design[8] - (handling[6]/100)*design[8] - (tilstand[18] + tilstand[19]) + tilstand[20]
        tilstand[25] = tilstand[25] + (handling[5]/100)*design[8]*dampTabel[0][3] - (handling[6]/100)*design[8]*enthalpiVandSpc + tilstand[20]*dampTabel[15][3]                                 

        # C: energi ind og ud
        if (handling[4] > 0.5):
            tilstand[25] = tilstand[25] + tilstand[10]
        else:
            tilstand[25] = tilstand[25] - 31.2*(tilstand[13]-20)*(70*design[1]/7690)*4.184/3600

        # D: damp ud
        if (tilstand[6] > 11):
            tilstand[16] = 1
        else:
            tilstand[16] = 0

        if ((handling[9]+handling[10]+tilstand[16]) == 0):
            tilstand[18] = 0
            tilstand[19] = 0

        if handling[9] > 5:
            if tilstand[17] > 0.29:
                tilstand[18] = 0.29 * handling[9]/100
            else:
                tilstand[18] = tilstand[17]
            
        if tilstand[16] == 1:
            tilstand[19] = tilstand[17] - tilstand[18]
        else:
            tilstand[19] = (tilstand[17] - tilstand[18]) * handling[10]/100
            
            
        tilstand[17] = tilstand[17] - (tilstand[18] + tilstand[19]) 
        tilstand[14] = tilstand[14] + tilstand[18]
        tilstand[15] = tilstand[15] + tilstand[19]
        tilstand[25] = tilstand[25] - (tilstand[18] + tilstand[19])*enthalpiDampSpc

        # E: Beregn ny damptabel, dampTilstand, (p (bar abs), t (0C), kedlens samlede enthalpi (kJ))

        for y in range(len(tilstandTabel)):
            tilstandTabel[y][2] = tilstand[5]*dampTabel[y][3]+tilstand[17]*dampTabel[y][4]

        # F: Find tryk og temperatur for den nye tilstand

        for x in range(len(tilstandTabel)):
            if tilstandTabel[x][2] > tilstand[25]:
                break

        tilstand[6] = damptabel.interpol(tilstandTabel[x-1][2],tilstandTabel[x-1][0],tilstand[25],tilstandTabel[x][2],tilstandTabel[x][0])
        if tilstand[6] > 11.5:
            tilstand[6] = 11.5
        if tilstand[6] < 0.5:
            tilstand[6] = 0.5
        tilstand[13] = damptabel.interpol(tilstandTabel[x-1][2],tilstandTabel[x-1][1],tilstand[25],tilstandTabel[x][2],tilstandTabel[x][1])
        tilstand[17] = ((design[1]-tilstand[5])/1000)/volumenDampSpc

        
        # Roeggastemperatur i skorsten

        if tilstand[2] > 0:
            if ((handling[3] <= 10) and (tilstand[2]>0)):
                tilstand[24] = tilstand[13] + 50
            if ((handling[3] > 10) and (tilstand[2]>0)):
                tilstand[24] = tilstand[13] + 50 - 30*(handling[3]/100)
            tilstand[24] = tilstand[24] + (600-tilstand[24])* tilstand[11]/100
        else:
            tilstand[24] = 50

        # Luftbalance

        if (tilstand[14] > 0) and (tilstand[7] == 1):
            if tilstand[15] > ((design[1] - tilstand[5])* 1.29/1000):
                tilstand[7] = 0
                design[14] = design[14] * 1.1           # Vi oeger maskinens dampbehov, hvis der er luft i dampen

        # Fortaetning af damp i kondensatoren

        tilstand[20] = tilstand[18]*(100 - design[6])/100
        
        if tilstand[18] > 0:
            tilstand[21] = 99-(handling[7]*0.9)
        else:
            tilstand[21] = 9
        
        for x in range(len(dampTabel)):
            if dampTabel[x][1] > tilstand[21]:
                break

        tilstand[22] = damptabel.interpol(dampTabel[x-1][1], dampTabel[x-1][0], tilstand[21], dampTabel[x][1], dampTabel[x][0])
        
        if (tilstand[22] > 1) or (tilstand[18] == 0):
            tilstand[22] = 1
        
        # Maskinydelse

        tilstand[8] = int(100*(tilstand[18]/design[14])*((tilstand[6]-tilstand[22])/9)*(abs(tilstand[0]-50)/50)*(handling[8]/100))
                                                                           
        # Oliebalance

        tilstand[1] = tilstand[1] + handling[1]-indpumpetFoer - design[3]*tilstand[8]*0.01/3600
        indpumpetFoer = handling[1]


        # BEREGN OG UDFOER VIRKNINGER  ###########################################################################

        virkning[0] = handling[0]
                        
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
        servoTemp.vis(virkning[3])
                         
        virkning[4] = int(tilstand[5]/design[1]*100)
        if virkning[4] > 100:
            virkning[4] = 100
        skueglasKedel.set(virkning[4])

        virkning[6] = tilstand[22]
        virkning[7] = tilstand[6] - 1  # Manometeret viser bar overtryk
        if virkning[7] < 0:
            virkning[7] = 0
        servoTryk.vis(virkning[6],virkning[7])

        if (tilstand[2] > 0) and (tid % 10 == 0):       # fordi baandet ikke kan koere langsommere end 0,1 m/s = speed 15
            virkning[8] = tilstand[2] * design[11]/handling[4]
            speed = int(virkning[8] * 255 * 10 / design[12])
            if speed < 15:
                speed = 15
            transport.TransportGo(speed)
        else:
            transport.TransportStop()
                         
        virkning[9] = tilstand[16]
        if virkning[9] == 1:
            sikkerhedsventil.sikkerhedsventilOn()
        else:
            sikkerhedsventil.sikkerhedsventilOff()
        
        if handling[4] > 1:
            virkning[10] = 1
            powernet.Relay4on()
            virkning[11] = 1
            powernet.Relay4on()
        else:
            virkning[10] = 0
            powernet.Relay4off()
            virkning[11] = 0
            powernet.Relay4off()

        if tilstand[8] > 0:
            virkning[5] = 1
            if (pause == 1):
                IRremote.TVpause()
                pause = 0
        else:
            virkning[5] = 0
            if (pause == 0):
                IRremote.TVpause()
                pause = 1
                

        #virkning[12] anvendes kun i initialiseringen

        virkning[14] = max(handling[5], handling[6])
        if virkning[14] > 10:
            channel4.set_volume(virkning[14]/100,0)
            if not channel4.get_busy():
                channel4.play(vand,loops=-1)
        else:
            channel4.stop()
                    
        
        if ((tilstand[5] > design[1]) or (tilstand[1] > design[4])):
            virkning[15] = 100
        else:
            virkning[15] = 0

        if virkning[15] > 10:
            channel11.set_volume(virkning[15]/100,0)
            if not channel11.get_busy():
                channel11.play(vandpjask, loops=-1)
        else:
            channel11.stop()

        if tilstand[16] == 1:
            virkning[16] = 100
        else:
            virkning[16] = 0

        if tilstand[6] > 3:
            virkning[23] = handling[10]
            if virkning[23] > 10:
                channel6.set_volume(virkning[23]/100,0)
                if not channel6.get_busy():
                    if (tilstand[15] < (design[1]-tilstand[5])/(1.7259*1000)):
                        channel6.play(luft, loops = -1)
                    else:
                        channel6.play(damp, loops =-1)
            else:
                channel6.stop()

        if virkning[16] > 10:
            channel7.set_volume(virkning[16]/100,0)
            if not channel7.get_busy():
                channel7.play(overtryksventil, loops=-1)
        else:
            channel7.stop()

        if tilstand[1] < 1:
            virkning[17] = 100-100*tilstand[1]
        else:
            virkning[17] = 0

        if ((virkning[17] > 10) and (tilstand[8] > 0)):
            channel8.set_volume(virkning[17]/100,0)
            if not channel8.get_busy():
                channel8.play(maskinpiv, loops=-1)
        else:
            channel8.stop()

        if tilstand[1] < 0.1:
            virkning[18] = 100
            virkning[1] = 0
        else:
            virkning[18] = 0

        if virkning[18] > 10:
            channel9.set_volume(virkning[18]/100,0)
            if not channel9.get_busy():
                channel9.play(maskinhaveri, loops=0)
        else:
            channel9.stop()

        #virkning[19] anvendes kun i initialiseringen

        # Her saettes spilforloebet ##############################################################################


        if (realTid > 10) and (realTid <= 20):
            if virkning[21] != 101:
                virkning[21] = 101
                virkning[24] = 1
                channel3.set_volume(1,0)
                channel3.play(flute, loops=0)
                time.sleep(5)
                channel12.set_volume(0,1)
                channel12.play(skipper01, loops=0)       # Fem minutter til afgang
                callTime = realTid


        if (realTid > 290) and (realTid <305):
            if virkning[20] != 8:
                virkning[20] = 8
                servo.maskintelegraf_FS()
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=2, maxtime=1000)
                
                
                
        if (realTid > 305) and (realTid <= 325):
            if virkning[20] != 2:
                virkning[20] = 2
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LF()
                

        if (realTid > 325) and (realTid <= 345):
            if virkning[20] != 4:
                virkning[20] = 4
                servo.maskintelegraf_LB()
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                

        if (realTid > 345) and (realTid <= 365):
            if virkning[20] != 2:
                virkning[20] = 2
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LF()
                

        if (realTid > 365) and (realTid <= 390):
            if virkning[20] != 1:
                virkning[20] = 1
                servo.maskintelegraf_HF()
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                        

        if (realTid > 390) and (realTid < 965):
            if virkning[20] != 0:
                virkning[20] = 0
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_FF()

                
        if (realTid > 800) and (realTid <= 900):            # Roegmaskine aktiveres
            #print("Virkning[24] = ",virkning[24])
            if virkning[24] != 0:
                virkning[24] = 0
                tilstand[11] = 100
                powernet.Relay9on()
                #print("Roeg aktiveres")
                roeg = True
                smokeStart = realTid

        if (roeg == True) and ((realTid - smokeStart) < 310):
            if (realTid - smokeStart) > 90:
                powernet.Relay9off()
                #print("Roeg stoppes")
                time.sleep(3)
                powernet.Relay7on()
                #print("Ventilator taendes")
                tilstand[11] = 0
                roeg = False
            if (realTid - smokeStart) > 300:
                smokeStart = 0

        if (realTid > 900) and (realTid < 950):
            if virkning[21] != 102:
                virkning[21] = 102
                channel3.set_volume(1,0)
                channel3.play(flute, loops=0)
                time.sleep(5)
                channel12.set_volume(0,1)
                channel12.play(skipper02, loops=0)           # 200 meter til havnemolen
                callTime = realTid

                
        if (realTid > 968) and (realTid <= 1033):
           if virkning[20] != 2:
                virkning[20] = 2
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LF()
                

        if (realTid > 1033) and (realTid <= 1055):
            if virkning[20] != 4:
                virkning[20] = 4
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LB()
                

        if (realTid > 1055) and (realTid <= 1092):
            if virkning[20] != 2:
                virkning[20] = 2
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LF()
                

        if (realTid > 1092) and (realTid <= 1118):
            if virkning[20] != 4:
                virkning[20] = 4
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LB()
                

        if (realTid > 1118) and (realTid <= 1231):
            if virkning[20] != 2:
                virkning[20] = 2
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LF()
                

        if (realTid > 1231) and (realTid <= 1259):
            if virkning[20] != 4:
                virkning[20] = 4
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LB()
                

        if (realTid > 1259) and (realTid <= 1290):
            if virkning[20] != 2:
                virkning[20] = 2
                servo.maskintelegraf_LF()
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                

        if (realTid > 1290) and (realTid <= 1317):
            if virkning[20] != 4:
                virkning[20] = 4
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LB()
                

        if (realTid > 1317) and (realTid <= 1387):
            if virkning[20] != 2:
                virkning[20] = 2
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LF()
                

        if (realTid > 1387) and (realTid <= 1403):
            if virkning[20] != 4:
                virkning[20] = 4
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LB()
                

        if (realTid > 1403) and (realTid <= 1600):
           if virkning[20] != 2:
                virkning[20] = 2
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_LF()
                

        if (realTid > 1603) and (realTid <= 1610):
            if virkning[20] != 3:
                virkning[20] = 3
                virkning[25] = 1
                channel3.set_volume(1,0)
                channel3.play(maskintelegraf, loops=0)
                servo.maskintelegraf_FS()

                
        if (realTid > 1615) and (realTid <= 1630):
            if virkning[25] > 0:
                channel9.set_volume(virkning[25],0)
                channel9.play(dampflute, loops=0)
                virkning[25] = 0

                

        if (realTid > 1630) and (realTid <= 1650):
            if virkning[21] != 103:
                virkning[21] = 103
                #channel3.set_volume(1,0)
                channel3.play(flute, loops=0)
                time.sleep(5)
                channel12.set_volume(0,1)
                channel12.play(skipper03, loops=0)      # Tak for sejladsen
                callTime = realTid

        if realTid > 1700:
            IRremote.TVonOff()
            powernet.RelayAlloff()
            return      # Programmet stopper efter et gennemloeb af spillet og starter for fra med ny initiering


    # DEBUGGING  ###############################################################################

        
        print("Cykl = {:>4.0f}\tp = {:>4.2f} bar\tt = {:>6.2f} 0C\tE(ind) = {:>6.2f} kJ/sek  \tDamp i kedlen = {:>6.4f} kg\tMaskinydelse = {:>6.0f} %\t\tReal tid = {:>6.0f} %\t\Kedel_ind = {:>6.0f} %\t\Kedel_ud = {:>6.0f}".format(tid,tilstand[6],tilstand[13],tilstand[10],tilstand[17],tilstand[8],realTid,handling[5],handling[6]))

    #    for i in range(0,12):
    #        print("Handling[",i,"] = ",handling[i])
    #
    #    print("******************************************************")
    #    
    #    for i in range(0,27):
    #        print("Tilstand[",i,"] = ",tilstand[i])
    #
    #   print("******************************************************")
    #
    #    for i in range(0,26):
    #        print("Virkning[",i,"] = ",virkning[i])
    #
    #    print("******************************************************")
