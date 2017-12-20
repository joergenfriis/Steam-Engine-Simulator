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
# design[0] = Kedelrumfang i liter (realistisk 7.690 l, pædagogisk 500 l)
# design[1] = Brandvaerdi af kul (7.600 kcal/kg)
# design[2] = Smoereolieforbrug pr time ved 100 % maskinydelse (2 liter)
# design[3] = Rumfang af smoereolietank (5 liter)
# design[4] = Skalering af oliepumpe (0.1)
# design[5] = Kedelvandstab (5 % af det tilførte damp kommer ikke retur)
# design[6] = Overtryksventil paa kedel (blaeser ved 10 bar)
# design[7] = Antal sekunder mellem hver opdatering
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
# tilstand[1] = Olie i oliebeholder i liter (0 til design[3])
# tilstand[2] = Primaer luft i m3/sek
# tilstand[3] = Sekundaer luft i m3/sek
# tilstand[4] = Forbraendingshastighed i kg kul pr. minut
# tilstand[5] = Vand i kedel i liter
# tilstand[6] = Damptryk i bar (overtryk)
# tilstand[7] = luft i damprummet (0-100%)
# tilstand[8] = Maskinydelse (0-100)
# tilstand[9] = Maskintelegraf (0-6)
#
# virkning[0] = Omstyringens stilling paa modellen (0-100)
# virkning[1] = Modellens omdrejningshastighed (0-100%)
# virkning[2] = Oliestand i skueroer (0-100%)
# virkning[3] = Roeggastemperatur (50-650 grader)
# virkning[4] = Kedelvand i skueroer (0-100%)
# virkning[5] = Film i kooeje (0/1: afspilning eller pause)
# virkning[6] = Vacuum i kondensator (0-1 bar)
# virkning[7] = Kedeltryk (0-10 bar)
# virkning[8] = Hastighed af transportbaand (0-?? m/s)
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
# virkning[20] = Maskintelegrafens stilling
# 
#
# Joergen Friis 20.12.2017
#
#############################################################################

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

print("Starter simulatorprogram")

# Initiering af simulatoren ################################################

print("Initiering")

design[0] = 7690
design[1] = 7600
design[2] = 2
design[3] = 5
design[4] = 0.1
design[5] = 5
design[6] = 10
design[7] = 1

# aflaes programvaelger og juster designparametre tilsvarende

tilstand[0] = 50
tilstand[1] = 2.5
tilstand[2] = 0
tilstand[3] = 0
tilstand[4] = 0
tilstand[5] = design[0] * 0.5
tilstand[6] = 0
tilstand[7] = 100
tilstand[8] = 0
tilstand[9] = 3

virkning[0] = 50
virkning[1] = 0
virkning[2] = (tilstand[1]/design[3])*100
virkning[3] = 0
virkning[4] = (tilstand[5]/design[0])*100
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

# Toem transportbaandet for kul
transport.TransportGo(150)  
time.sleep(5)
transport.TransportStop()

# Nulstil vejecellen
vejecelle.Reset_vejecelle()

# Udfoer alle virkninger
servo.gangskifte(virkning[0]) 
model.ModelRun(virkning[1],virkning[0])
skueglasOlie.set(virkning[2])
servo.smokeTemp(virkning[3])
skueglasKedel(virkning[4])
# Her kommer noget om styring af fjernsyn
servo.kondensatorTryk(virkning[6])
servo.kedelTryk(virkning[7])
transport.TransportGo(virkning[8])
# Her kommer noget om styring af overtryksventilen
if (virkning[10] == 1):
    powernet.Relay4on()
if (virkning[11] == 1):
    powernet.Relay4on()
# Her kommer noget om styring af lyd
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
virkning[11] = 1
tid = 0

# Drift af simulatoren ######################################################

while True:
    time.sleep(design[7])
    tid = tid + 1

    # registrer handlinger
    handling[0] = omstyring.Read_omstyring()
    handling[1] = 
    











