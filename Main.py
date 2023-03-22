"""
Header
Hier komen alle libraries die in het programma gebruikt worden
"""
import xlwings as xw
import matplotlib.pyplot as plt
import sys
from PyQt5 import QtWidgets
from string import ascii_uppercase
import functions
import Klassen_Schermen
from logging import getLogger
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm


"""
Body
Hier komen alle functies
"""
@xw.sub
def Test():
    """
    functie om functie van tekstkleurveranderen te testen

    Returns
    -------
    None.

    """
    book = xw.Book.caller()
    #testen met protected en unprotected sheet
    # sheet = book.sheets["Test Julia"]
    # sterftetafel = book.sheets["Sterftetafels"]
    # sheet.api.Protect(Password = functions.wachtwoord())
    
    # sterftetafel.cells(7,6).value = "sheet protected"
    # #haal waarde uit sheet
    # waarde = sheet.cells(6,2).value
    # #print opgehaalde tekst
    # sterftetafel.cells(6,6).value = waarde
    
    # #waarde printen in sheet
    # sheet.api.Unprotect(Password = functions.wachtwoord())
    # sheet.cells(9,2).value = "Test printen"
    
    
    # sht = "Sterftetafels"   #"deelnemersbestand"
    # sheets = [sht]
    # functions.tekstkleurSheets(book, sheets, zicht = 0)
    # sht = "deelnemersbestand"
    #sheets = ["Sterftetafels", "AG2020", "Gegevens pensioencontracten"]
    # sheets = ["Berekeningen"]
    # functions.tekstkleurSheets(book, sheets, zicht = 1)
    
    
    
    
    vergelijken = book.sheets["Vergelijken"]
    flexopslag = book.sheets["Flexopslag"]
    #keuzeCel = "J13"
    rijNr = int(float(flexopslag.cells(15,"B").value))
    
    #deelnemerobject inladen
    deelnemer = functions.getDeelnemersbestand(book, rijNr)
    deelnemer.activeerFlexibilisatie()      #maak pensioenobjecten aan
    
    afbeeldingen = []
    for cel in ["J13"]:
        #gekozen afbeelding inlezen
        gekozenAfbeelding = vergelijken[cel].value 
        ID = functions.flexopslagNaamNaarID(book, gekozenAfbeelding)
        afbeeldingen.append(ID)
    
    vlakken = [vergelijken.range((14,10))]
    
    vlak = vergelijken.range((14,10))
    gekozenAfbeelding = vergelijken["J13"].value 
    ID = functions.flexopslagNaamNaarID(book, gekozenAfbeelding)
    
    #functions.maak_afbeelding(deelnemer, ID = ID, titel = f"{ID} - Een super coole title")
    
    # for pic in vergelijken.pictures:
    #     for vlak, i in enumerate(vlakken):
    #         if pic.top == vlak.top and pic.left == vlak.left:
    #             #als naam afbeelding in box niet gelijk is aan naam gekozen afbeelding
    #             if pic.name != afbeeldingen[i]:
    #                 #afbeelding terugverplaatsen
    #                 teller = afbeeldingen[i].split()[-1]-1
    #                 rij = int(12 + (teller%4)*22)
    #                 kolom = int(17 + ((teller - teller%4)/4)*8)
    #                 afbeelding = vergelijken.pictures[pic.name]
    #                 afbeelding.top = vergelijken.range((rij,kolom)).top
    #                 afbeelding.left = vergelijken.range((rij,kolom)).left
                    
    #         #juiste afbeelding op vlak zetten
    #         afbeelding = vergelijken.pictures[afbeeldingen[i]]
    #         afbeelding.top = vlak.top
    #         afbeelding.left = vlak.left
    
    for pic in vergelijken.pictures:
        if pic.top == vlak.top and pic.left == vlak.left:
            #als naam afbeelding in box niet gelijk is aan naam gekozen afbeelding
            if pic.name != ID:
                #afbeelding terugverplaatsen
                
                teller = int(pic.name.split()[-1])-1
                rij = int(12 + (teller%4)*22)
                kolom = int(17 + ((teller - teller%4)/4)*8)
                afbeelding = vergelijken.pictures[pic.name]
                afbeelding.top = vergelijken.range((rij,kolom)).top
                afbeelding.left = vergelijken.range((rij,kolom)).left
                
        #juiste afbeelding op vlak zetten
        afbeelding = vergelijken.pictures[ID]
        afbeelding.top = vlak.top
        afbeelding.left = vlak.left

@xw.sub
def Schermen():
    """
    Functie die de logger importeerd en het keuzescherm opent

    Returns
    -------
    None.

    """
    
    logger = functions.setup_logger("Main") if not getLogger("Main").hasHandlers() else getLogger("Main")
    app = 0
    app = QtWidgets.QApplication(sys.argv)
    if functions.isBeheerder(xw.Book.caller()):
        windowBeheerder = Klassen_Schermen.Beheerderkeuzes(xw.Book.caller(), logger)
        windowBeheerder.show()
        app.exec_()
    else:
        window = Klassen_Schermen.Functiekeus(xw.Book.caller(), logger)
        window.show()
        app.exec_()

    
    
@xw.sub
def delimage():
    book = xw.Book.caller()
    uitvoer = book.sheets["Vergelijken"]
    print(uitvoer.pictures["testnaam"].height)
    uitvoer.pictures["testnaam"].api.Delete()
    
    




@xw.sub
#Idee voor berekeningen uitvoeren: Functies schrijven
def invoer_test_klikken():
    #sheets en book opslaan in variabelen
    book = xw.Book.caller()
    invoer = book.sheets["Tijdelijk invoerscherm"]
    
    #unprotect sheet
    invoer.api.Unprotect(Password = functions.wachtwoord())
    #Berekeningskolommen leegmaken
    kolommen = invoer.range((1,8), (80,130))
    Uitkomst_kolommen = invoer.range((10,6), (20,6))
    #Kolommen legen waar de berekeningen komen
    kolommen.clear_contents()
    Uitkomst_kolommen.clear_contents()
    
    regeling_range = invoer.range((10,1), (20,1))
    pensioenbedragen = invoer.range((10,2), (20,2))
    sterftetafel_range = invoer.range((10,3), (20,3))
    rentes = invoer.range((10,4), (20,4))
    pensioenleeftijd_range = invoer.range((10,5), (20,5))
    koopsomfactor_range = invoer.range((10,6), (20,6))
    basis_koopsom = invoer.range((10,7), (20,7))

    pensioenleeftijd=[]
    rente=[]
    letters=[]
    for p in range(5):
        if len(letters) >= 26:
            for i in ascii_uppercase:
                letters.append(letters[p-1] + i)
        else:
            for i in ascii_uppercase:
                letters.append(i)  
      
    for c in range(2,12):
        pensioenleeftijd_range(c).value= regeling_range(c).value[-2:]

    counter=1
    for i in range(1,12):
        if pensioenbedragen(i).value != None:
            kolom_t = (counter-1)*10+9
            kolom_jaar = (counter-1)*10+10
            kolom_leeftijd = (counter-1)*10+11
            kolom_tpx = (counter-1)*10+12
            kolom_tqx = (counter-1)*10+13
            kolom_tqx_juli = (counter-1)*10+14
            kolom_dt = (counter-1)*10+15
            kolom_dt_juli = (counter-1)*10+16

            rente.append(rentes(i).value)
            pensioenleeftijd.append(pensioenleeftijd_range(i).value)
            

            # blok1 = list()
            # blok1.append(["t", "Jaar", "Leeftijd", "tpx", "tqx", "tqx op 1 juli", "dt", "dt op 1 juli"])
            # blok1.append(["0", '=year(B4)+' + str(int(pensioenleeftijd[i-1])), '=$E' + str(i+9), 1, 0, '=if({0}3<>"", (((13 - month($B$4)) * {1}2) + ((month($B$4) - 1) * {1}3)) / 12, "")'.format(letters[kolom_leeftijd - 1], letters[kolom_tqx - 1]), '=if({0}2<>"", (1+$D${1})^-{2}2, "")'.format(letters[kolom_leeftijd-1], str(i+9), letters[kolom_t-1]),\
            #               '=if({0}3<>"", (1+$D${1})^-({2}2 + (month($B$4)-1)/12), "")'.format(letters[kolom_leeftijd-1], str(i + 9), letters[kolom_t-1])])
            # for rij in range(59): blok1.append(['=1+{}{}'.format(letters[kolom_t-1], str(rij+2)),\
            #                                    '=1+{}{}'.format(letters[kolom_jaar-1], str(rij+2)),\
            #                                        '=if({0}{1}<119, 1+{0}{1},"")'.format(letters[kolom_leeftijd-1], str(rij+2)),\
            #                                            functions.tpxFormule(sterftetafel_range(i).value, rij, letters[kolom_leeftijd-1], letters[kolom_jaar-1], letters[kolom_tpx-1]),\
            #                                                '=if({0}{1}<>"", 1-{2}{1}, "")'.format(letters[kolom_leeftijd-1], str(rij+3), letters[kolom_tpx-1]),\
            #                                                    '=if({0}{1}<>"", (((13 - month($B$4)) * {2}{3}) + ((month($B$4) - 1) * {2}{1})) / 12, "")'.format(letters[kolom_leeftijd - 1], str(rij + 4), letters[kolom_tqx - 1], str(rij + 3)),\
            #                                                        '=if({0}{1}<>"", (1+$D${2})^-{3}{1}, "")'.format(letters[kolom_leeftijd-1], str(rij+3), str(i+9), letters[kolom_t-1]),\
            #                                                            '=if({0}{1}<>"", (1+$D${2})^-({3}{4} + (month($B$4)-1)/12), "")'.format(letters[kolom_leeftijd-1], str(rij+4), str(i + 9), letters[kolom_t-1], str(rij+3))\
            #                                                                ])
            # invoer.range((1, kolom_t), (61, kolom_t+7)).options(ndims = 2).formula = blok1
            

            invoer.range((1, kolom_t)).formula = [["t"]]
            invoer.range((2, kolom_t)).formula = [["0"]]
            invoer.range((3, kolom_t), (61, kolom_t)).formula = [['=1+' + letters[kolom_t-1] + '2']]
            
            invoer.range((1, kolom_jaar)).value = "Jaar"
            invoer.range((2, kolom_jaar)).formula = [['=year(B4)+' + str(int(pensioenleeftijd[i-1]))]]
            invoer.range((3, kolom_jaar), (61, kolom_jaar)).formula = [['=1+' + letters[kolom_jaar-1] + '2']]
            
            invoer.range((1, kolom_leeftijd)).value= "Leeftijd"
            invoer.range((2, kolom_leeftijd)).formula= [['=$E' + str(i+9)]]
            invoer.range((3, kolom_leeftijd), (61, kolom_leeftijd)).formula= [['=if(' + letters[kolom_leeftijd-1] + '2<119, 1+' + letters[kolom_leeftijd-1] + '2,"")']]
            
            invoer.range((1, kolom_tqx)).value= "tqx"
            invoer.range((2, kolom_tqx), (61, kolom_tqx)).formula= [['=if(' + letters[kolom_leeftijd-1] + '2<>"", 1-' + letters[kolom_tpx-1] + '2, "")']]

            invoer.range((1, kolom_tqx_juli)).value= "tqx op 1 juli"
            invoer.range((2, kolom_tqx_juli), (61, kolom_tqx_juli)).formula= [['=if(' + letters[kolom_leeftijd-1] + '3<>"", (((13-month($B$4))*' + letters[kolom_tqx-1] + '2)+((month($B$4)-1)*' + letters[kolom_tqx-1] + '3))/12, "")']]

            
            invoer.range((1, kolom_dt)).value= "dt"
            invoer.range((2, kolom_dt), (61, kolom_dt)).formula= [['=if(' + letters[kolom_leeftijd-1] + '2<>"", (1+$D$' + str(i+9) + ')^-' + letters[kolom_t-1] + '2, "")']]
            
            invoer.range((1, kolom_dt_juli)).value= "dt op 1 juli"
            invoer.range((2, kolom_dt_juli), (61, kolom_dt_juli)).formula= [['=if(' + letters[kolom_leeftijd-1] + '3<>"", (1+$D$' + str(i+9) + ')^-(' + letters[kolom_t-1] + '2+(month($B$4)-1)/12), "")']]

            if sterftetafel_range(i).value== "AG_2020":
                invoer.range((1, kolom_tpx)).value= "tpx"
                invoer.range((2, kolom_tpx)).value= 1
                print('=if(' + letters[kolom_leeftijd-1] + '3<>"", (1-INDEX(INDIRECT($C$' + str(i+9) + '),' + letters[kolom_leeftijd-1] + '2+1, ' + letters[kolom_jaar-1] + '2-2018))*' + letters[kolom_tpx-1] + '2,"")')
                invoer.range((3, kolom_tpx), (61, kolom_tpx)).formula= [['=if(' + letters[kolom_leeftijd-1] + '3<>"", (1-INDEX(INDIRECT($C$' + str(i+9) + '),' + letters[kolom_leeftijd-1] + '2+1, ' + letters[kolom_jaar-1] + '2-2018))*' + letters[kolom_tpx-1] + '2,"")']]

            else:
                invoer.range((1, kolom_tpx)).value= "tpx"
                invoer.range((2, kolom_tpx), (61, kolom_tpx)).formula= [['=if(' + letters[kolom_leeftijd-1] + '2<>"", INDEX(INDIRECT($C$' + str(i+9) + '),' + letters[kolom_leeftijd-1] + '2+1,1) / INDEX(INDIRECT($C$' + str(i+9) + '),$' + letters[kolom_leeftijd-1] + '$2+1,1),"")']]

            if regeling_range(i).value== "ZL":
                koopsomfactor_range(i).value= 0
                basis_koopsom(i).value= pensioenbedragen(i).value

    
            
            if regeling_range(i).value== "ZL":
                koopsomfactor_range(i).value= 0
                basis_koopsom(i).value= pensioenbedragen(i).value
                
            elif "OP" in regeling_range(i).value:
                koopsomfactor_range(i).formula= [['=ROUND(SUMPRODUCT(' + letters[kolom_tpx-1] + '2:' + letters[kolom_tpx-1] + '61,' + letters[kolom_dt-1] + '2:' + letters[kolom_dt-1] + '61),3)']]
                basis_koopsom(i).value= float(pensioenbedragen(i).value)*koopsomfactor_range(i).value
                
            else:
                koopsomfactor_range(i).formula = [['=ROUND(SUMPRODUCT(' + letters[kolom_tpx-1] + '2:' + letters[kolom_tpx-1] + '61,' + letters[kolom_tqx_juli-1] +'2:' + letters[kolom_tqx_juli-1] + '61,'+ letters[kolom_dt_juli-1] + '2:' + letters[kolom_dt_juli-1] + '61),3)']]
                basis_koopsom(i).value = float(pensioenbedragen(i).value)*koopsomfactor_range(i).value

            counter+= 1
            
        else:
            basis_koopsom(i).value= 0
            rente.append(0)
            pensioenleeftijd.append(0)
    #sheet protecten
    invoer.api.Protect(Password = functions.wachtwoord())
 
@xw.sub
def AfbeeldingVerplaatsen(vak):
    book = xw.Book.caller()
    vergelijken = book.sheets["Vergelijken"]
    
    if vak == 1:
        vlak = vergelijken.range((14,10))
        keuzecel = "J13"
        #gekozenAfbeelding = vergelijken["J13"].value
    elif vak == 2:
        vlak = vergelijken.range((38,2))
        keuzecel = "B37"
        #gekozenAfbeelding = vergelijken["B37"].value
    else: #vak == 3 of iets anders
        vlak = vergelijken.range((38,10))
        keuzecel = "J37"
        #gekozenAfbeelding = vergelijken["J37"].value
    
    try:
        gekozenAfbeelding = vergelijken[keuzecel].value
        ID = functions.flexopslagNaamNaarID(book, gekozenAfbeelding)
    except:
        ID = "-"
        vergelijken["M2"].value == "ID is leeg of -" 
    vergelijken.api.Unprotect(Password = functions.wachtwoord())
    for pic in vergelijken.pictures:
        if pic.top == vlak.top and pic.left == vlak.left: #als er een afbeelding al in staat
            
            if pic.name != ID: #als naam afbeelding in box niet gelijk is aan naam gekozen afbeelding
                #afbeelding terugverplaatsen
                
                teller = int(pic.name.split()[-1])-1
                rij = int(12 + (teller%4)*22)
                kolom = int(17 + ((teller - teller%4)/4)*8)
                afbeelding = vergelijken.pictures[pic.name]
                afbeelding.top = vergelijken.range((rij,kolom)).top
                afbeelding.left = vergelijken.range((rij,kolom)).left
        if ID != "-":
            #juiste afbeelding op vlak zetten
            afbeelding = vergelijken.pictures[ID]
            afbeelding.top = vlak.top
            afbeelding.left = vlak.left
    vergelijken.api.Protect(Password = functions.wachtwoord())
       
@xw.sub
def AfbeeldingKiezen():
    """
    Functie die de gekozen afbeelding op de vergelijkings sheet kiest
    """
    
    #sheets en book opslaan in variabelen
    book = xw.Book.caller()
    sheet = book.sheets["Vergelijken"]
    flexopslag = book.sheets["Flexopslag"]
    if str(flexopslag.cells(2, 5).value) != "None":   #alleen als er nog flexibilisaties opgeslagen zijn
        #gekozen afbeelding inlezen
        gekozenAfbeelding = sheet.cells(6,"B").value
        #naam van gekozen afbeelding op sheet printen
        sheet.cells(8, "M").value = gekozenAfbeelding
        
        #Deelnemer toegevoegd zodat er gekeken kan worden naar het oude pensioen. Ik heb alleen nog geen idee hoe
        #rijnummer deelnemer zoeken
        rijNr = int(float(flexopslag.cells(15,"B").value))
        
        #deelnemerobject inladen
        deelnemer = functions.getDeelnemersbestand(book, rijNr)
        deelnemer.activeerFlexibilisatie()      #maak pensioenobjecten aan
        
        #book.sheets["Sterftetafels"].cells(15, 5).value = deelnemer.achternaam
        oudpensioen = []
        for i in deelnemer.pensioenen:
            pensioen = []
            pensioen.append(i.pensioenNaam)             #0
            pensioen.append(str(i.pensioenleeftijd))    #1
            pensioen.append("0") #De maand              #2
            pensioen.append(i.ouderdomsPensioen)        #3
            pensioen.append(i.partnerPensioen)          #4
            oudpensioen.append(pensioen)            
            
        nieuwpensioen = functions.UitlezenFlexopslag(book, gekozenAfbeelding)
        
        eenperjaar = functions.geld_per_leeftijd(oudpensioen, nieuwpensioen)
        
        eenperjaaroud = eenperjaar[0]
        eenperjaarnieuw = eenperjaar[1]
        
        verhaalstart = 536
        verhaallijn = verhaalstart
        
        
        
        #book.sheets["Sterftetafels"].cells(15, 5).value = oudpensioen
        
        pdf_canvas = Canvas("test.pdf")
        pdf_canvas.setFont("Helvetica", 11)
        halfbreedte = cm*10.5
        
        totOPoud = 0
        pdf_canvas.drawString(40+halfbreedte, 550, "Met uw oude pensioen")
        for i in eenperjaaroud:
            totOPoud = totOPoud + i[1]
            oudverhaal = "ontving u vanaf  "+ i[0]+ " €" + str(totOPoud)+ " per jaar aan OP"
            pdf_canvas.drawString(40+halfbreedte, verhaallijn, oudverhaal)
            verhaallijn -= 14
            
        totPPoud = 0
        for i in oudpensioen:
            totPPoud = totPPoud + int(i[4])
        
        PPoudverhaal = "Uw oude partner pensioen was €" + str(totPPoud) + " per jaar"
        pdf_canvas.drawString(40 + halfbreedte, verhaallijn-14, PPoudverhaal)
        
        verhaallijn = verhaalstart
        
        pdf_canvas.drawString(40, 550, "Met uw nieuwe pensioen")
        
        totOPnieuw = 0
        for i in eenperjaarnieuw:
            totOPnieuw = totOPnieuw + i[1]
            if "maand" in i[0]:
                nieuwverhaal = "ontvangt u vanaf  "+ i[0] 
                pdf_canvas.drawString(40, verhaallijn, nieuwverhaal)
                verhaallijn -= 14
                nieuwverhaal = "€" + str(totOPnieuw)+ " per jaar aan OP"
                pdf_canvas.drawString(120, verhaallijn, nieuwverhaal)
            else:
                nieuwverhaal = "ontvangt u vanaf  "+ i[0]+ " €" + str(totOPnieuw)+ " per jaar aan OP"
                pdf_canvas.drawString(40, verhaallijn, nieuwverhaal)
            verhaallijn -= 14
        
        
        totPPnieuw = 0
        for i in nieuwpensioen:
            totPPnieuw = totPPnieuw + int(float(i[17]))
        
        PPnieuwverhaal = "Uw nieuwe partner pensioen is €" + str(totPPnieuw) + " per jaar"
        pdf_canvas.drawString(40, verhaallijn-14, PPnieuwverhaal)
        
        functions.nieuwe_pagina(pdf_canvas, halfbreedte)
        startschrijfhoogte = 720
        schrijfhoogte = startschrijfhoogte
        # oudpensioenimg = "pensioenplaatje.png"
        # nieuwpensioenimg = "pensioenplaatje2.png"
        
        # pdf_canvas.drawImage(nieuwpensioen, 40, 575, 250, 193)
        # pdf_canvas.drawImage(oudpensioen, 40 + halfbreedte, 575, 250, 193)
        # nieuwe_pagina(pdf_canvas, halfbreedte)
        #staat nog in commentaar, omdat een manier van afbeelding maken/lezen moet worden gevonden
        
        
        benodigde_indexen = [0, 1, 2, 15, 17, 4, 5, 7, 9, 10, 11, 13]
        #4 start 5, 7(8)
        #9 start 10,11,13(14) past 15(16) aan
        
        
        p = 1 # hoeveelste pensioen neergezet wordt
        for pensioen in nieuwpensioen:
            labels = ["Pensioenfonds", "Vervroegen/Uitstellen?", "Pensioenleeftijd", "Nieuw OP", "Nieuw PP", "Uitruilen?", "Volgorde", pensioen[6],"Hoog/Laag?", "volgorde",  "Duur", pensioen[12]]
            benodigdeantwoorden = []
            for l in benodigde_indexen:
                if l == 2:
                    if pensioen[1] == "Ja":
                        antwoord = functions.leeftijd_notatie(pensioen[2], pensioen[3])
                        #voor nu is dit de enige plek, maar met het verhaal en oud pensioen moet dit meer toegepast worden
                        # if pensioen[3] == "0":
                        #     antwoord = pensioen[2] + " jaar"
                        # elif pensioen[3] == "1":
                        #     antwoord = pensioen[2] + " jaar en 1 maand"
                        # else:
                        #     antwoord = pensioen[2] + " jaar en " + pensioen[3] + " maanden"
                    else:
                        antwoord =  functions.leeftijd_notatie(oudpensioen[p-1][1], "0")
                        
                elif l == 15:
                    if pensioen[9] == "Ja":
                        hoog = "€" + str(int(float(pensioen[l]))) + " hoog"
                        laag = "€" + str(int(float(pensioen[l+1]))) + " laag"
                        if pensioen[10] == "Hoog-laag":
                            antwoord = hoog + " " + laag
                        else:
                            antwoord = laag + " " + hoog
                    else:
                        antwoord = "€" + str(int(float(pensioen[l])))
                elif l == 17:
                    antwoord = "€" + str(int(float(pensioen[l])))
                        
                elif l == 5 or l == 7: #opties die alleen bij uitruilen horen
                    if pensioen[4] == "Ja":
                        if l == 7:
                            if pensioen[l-1] == "Verhouding":
                                antwoord = pensioen[l] + ":" + pensioen[l+1]
                            else:
                                antwoord = pensioen[l]
                        else:
                            antwoord = pensioen[l]
                    else:
                        antwoord = ""
                elif l == 10 or l == 11 or l == 13: #opties die alleen bij hoog-laag horen
                    if pensioen[9] == "Ja":
                        if l == 13:
                            if pensioen[l-1] == "Verhouding":
                                antwoord = pensioen[l] + ":" + pensioen[l+1]
                            else:
                                antwoord = pensioen[l]
                        else:
                            antwoord = pensioen[l]
                    else:
                        antwoord = ""
                
                else:
                    antwoord = pensioen[l]
                benodigdeantwoorden.append(antwoord)
                
            #antwoorden noteren
            if p%3 == 1:
                pdf_canvas.showPage()
                functions.nieuwe_pagina(pdf_canvas, halfbreedte)
                schrijfhoogte = startschrijfhoogte
            k = 0
            for j in labels:
                if k == 0: # fonds
                    pdf_canvas.drawString(40 + halfbreedte, schrijfhoogte, j)
                    pdf_canvas.drawString(180 + halfbreedte, schrijfhoogte, oudpensioen[p-1][0])
                elif k == 2: #leeftijd
                    pdf_canvas.drawString(40 + halfbreedte, schrijfhoogte, j)
                    oud_leeftijd = functions.leeftijd_notatie(oudpensioen[p-1][1], "0")
                    pdf_canvas.drawString(180 + halfbreedte, schrijfhoogte, oud_leeftijd)
                elif k == 3: #OP
                    pdf_canvas.drawString(40 + halfbreedte, schrijfhoogte, "Oud OP")
                    pdf_canvas.drawString(180 + halfbreedte, schrijfhoogte, "€" + str(oudpensioen[p-1][3]))
                elif k == 4: #PP
                    pdf_canvas.drawString(40 + halfbreedte, schrijfhoogte, "Oud PP")
                    pdf_canvas.drawString(180 + halfbreedte, schrijfhoogte, "€" + str(oudpensioen[p-1][4]))
                pdf_canvas.drawString(40, schrijfhoogte, j)
                #antwoord = self._pensioen[self._benodigde_indexen[k]]
                antwoord = benodigdeantwoorden[k]
                pdf_canvas.drawString(180, schrijfhoogte, antwoord)
                schrijfhoogte = schrijfhoogte -14
                k+=1
            schrijfhoogte = schrijfhoogte -25
            p+=1
        pdf_canvas.save()
        
    else:
        functions.Mbox("foutmelding", "Er zijn geen flexibilisaties opgeslagen. \nMaak eerst een nieuwe flexibilisatie aan.", 0)
    
#book.sheets["Vergelijken"].cells(2, "O").value = "Test"
@xw.sub
def AfbeeldingVerwijderen():
    """
    Functie die de gekozen afbeelding op de vergelijkings sheet verwijderd
    """
    
    #sheets en book opslaan in variabelen
    book = xw.Book.caller()
    Vergelijken = book.sheets["Vergelijken"]
    Opslag = book.sheets["Flexopslag"]
    if str(Opslag.cells(2, 5).value) != "None":   #alleen als er nog flexibilisaties opgeslagen zijn
        #gekozen afbeelding inlezen
        gekozenAfbeelding = Vergelijken.cells(6,"B").value
        #vragen of echt verwijderd moet worden
        controle = functions.Mbox("Afbeelding verwijderen", f"Wilt u de flexibilisatie '{gekozenAfbeelding}' echt verwijderen?\nU kunt deze actie niet ongedaan maken.", 4)
        if controle == "Ja":
            #ID van de gekozen afbeelding opzoeken
            ID = functions.flexopslagNaamNaarID(book, gekozenAfbeelding)
            #Vergelijken.cells(11, "O").value = ID
            
            #gekozen afbeelding verwijderen
            try:
                Vergelijken.pictures[ID].delete()
            except:
                functions.Mbox("Foutmelding", f"Het verwijderen van flexibilisatie '{gekozenAfbeelding}' lukt niet.\n Het AfbeeldingID bestaat niet", 0)
            
            #tellen hoeveel opgeslagen flexibiliseringen en hoeveel pensioenen
            Flexopslag = functions.FlexopslagVinden(xw.Book.caller(), gekozenAfbeelding)
            
            startKolom = Flexopslag[0]
            laatsteKolom = Flexopslag[1]
            aantalPensioenen = Flexopslag[2]
            rijen = aantalPensioenen*20 + 4
            #opslag sheet unprotecten
            Opslag.api.Unprotect(Password = functions.wachtwoord())
            if startKolom != laatsteKolom: #er zijn meer dan 1 flexibilisaties opgeslagen
                #verwijderen gegevens verwijderde flexibilisatie
                Opslag.range((1,startKolom-1),(rijen,startKolom+1)).clear_contents()
                #flexibilisaties na verwijderde blok opschuiven
                Opslag.cells(1,startKolom-1).value = Opslag.range((1,startKolom+3),(rijen,laatsteKolom+1)).value
            #laatste (of enige) kolom verwijderen
            Opslag.range((1,laatsteKolom-1),(rijen,laatsteKolom+1)).clear()
            #opslag sheet protecten
            Opslag.api.Protect(Password = functions.wachtwoord())
            
            try:
                #drop down op vergelijkingssheet updaten
                functions.vergelijken_keuzes()
            except:
                #laatste opslag is verwijderd, dus drop down legen
                Vergelijken["B6"].value = ""
    
    else: #er zijn geen flexibilisaties opgeslagen
        #keuzecel in vergelijkingssheet legen
        Vergelijken["B6"].value = ""
        functions.Mbox("foutmelding", "Er zijn geen flexibilisaties opgeslagen. \nMaak eerst een nieuwe flexibilisatie aan.", 0)
    
    
@xw.sub
def afbeelding_aanpassen():
    """
    Functie die de gekozen afbeelding op de vergelijkings sheet als basis neemt voor nieuwe flexibilisaties
    """
    
    #sheets en book opslaan in variabelen
    book = xw.Book.caller()
    sheet = book.sheets["Vergelijken"]
    flexopslag = book.sheets["Flexopslag"]
    if str(flexopslag.cells(2, 5).value) != "None":   #alleen als er nog flexibilisaties opgeslagen zijn
        #gekozen afbeelding inlezen
        gekozenAfbeelding = sheet.cells(6,"B").value 
        
        #gegevens van gekozen afbeelding inladen
        opslag = functions.UitlezenFlexopslag(book, gekozenAfbeelding)
        #rijnummer deelnemer zoeken
        rijNr = int(float(flexopslag.cells(15,"B").value))
        
        #deelnemerobject inladen
        deelnemer = functions.getDeelnemersbestand(book, rijNr)
        deelnemer.activeerFlexibilisatie()      #maak pensioenobjecten aan
        
        #lijst met pensioennamen van de deelnemer 
        pensioennamen = []  
        for i in opslag:
            pensioennamen.append(i[0])
        
        #lijst met pensioennamen langsgaan en opgeslagen flexibilisatiegegevens per pensioen toevoegne aan flexibiliseringsobject van het deelnemersobject
        for i,p in enumerate(pensioennamen):
            for flexibilisatie in deelnemer.flexibilisaties:
                #als het flexibilisatieobject bij het pensioen uit de lijst pensioennamen hoort
                if flexibilisatie.pensioen.pensioenNaam == p:
                    #met properties flexibilisaties opslaan in objecten flexibilisatie
                    pensioengegevens = opslag[i]
                    #leeftijd aanpassen
                    if pensioengegevens[1] == "Ja":
                        flexibilisatie.leeftijd_Actief = True
                    elif pensioengegevens[1] == "Nee":
                        flexibilisatie.leeftijd_Actief = False
                    flexibilisatie.leeftijdJaar = int(float(pensioengegevens[2]))
                    flexibilisatie.leeftijdMaand = int(float(pensioengegevens[3]))
                    
                    #uitruilen
                    if pensioengegevens[4] == "Ja":
                        flexibilisatie.OP_PP_Actief = True
                    elif pensioengegevens[4] == "Nee":
                        flexibilisatie.OP_PP_Actief = False
                        #volgorde
                    flexibilisatie.OP_PP_UitruilenVan = pensioengegevens[5]
                        #methode
                    flexibilisatie.OP_PP_Methode = pensioengegevens[6]
                    if pensioengegevens[6] == "Verhouding":
                        flexibilisatie.OP_PP_Verhouding_OP = int(float(pensioengegevens[7]))
                        flexibilisatie.OP_PP_Verhouding_PP = int(float(pensioengegevens[8]))
                    elif pensioengegevens[6] == "Percentage":
                        flexibilisatie.OP_PP_Percentage = int(float(pensioengegevens[7]))
                    
                    
                    #hoog-laag-constructie
                    if pensioengegevens[9] == "Ja":
                        flexibilisatie.HL_Actief = True
                    elif pensioengegevens[9] == "Nee":
                        flexibilisatie.HL_Actief = False
                        #volgorde
                    flexibilisatie.HL_Volgorde = pensioengegevens[10]
                        #duur
                    flexibilisatie.HL_Jaar = int(float(pensioengegevens[11]))
                        #methode
                    flexibilisatie.HL_Methode = pensioengegevens[12]
                    if pensioengegevens[12] == "Verhouding":
                        flexibilisatie.HL_Verhouding_Hoog = int(float(pensioengegevens[13]))
                        flexibilisatie.HL_Verhouding_Laag = int(float(pensioengegevens[14]))
                    elif pensioengegevens[12] == "Verschil":
                        flexibilisatie.HL_Verschil = int(float(pensioengegevens[13]))
                    
                    
        
        
        #scherm flexmenu openen
        logger = functions.setup_logger("Main") if not getLogger("Main").hasHandlers() else getLogger("Main")
        app = 0
        app = QtWidgets.QApplication(sys.argv)
        window = Klassen_Schermen.Flexmenu(xw.Book.caller(), deelnemer, logger)
        window.invoerVerandering(num = 0)
        window.show()
        app.exec_()
    else:
        functions.Mbox("foutmelding", "Er zijn geen flexibilisaties opgeslagen. \nMaak eerst een nieuwe flexibilisatie aan.", 0)
    
@xw.sub
def NieuweFlexibilisatie():
    """
    Functie die het flexmenu scherm opnieuw opent voor de juiste deelnemer
    """
    
    #sheet en book opslaan in variabelen
    book = xw.Book.caller()
    flexopslag = book.sheets["Flexopslag"]
    if str(flexopslag.cells(15,"B").value) != "None":   #alleen als er nog flexibilisaties opgeslagen zijn
        #rijnummer deelnemer zoeken
        rijNr = int(float(flexopslag.cells(15,"B").value))
        #deelnemerobject inladen
        deelnemer = functions.getDeelnemersbestand(book, rijNr)
        deelnemer.activeerFlexibilisatie()      #maak pensioenobjecten aan
        
        #scherm flexmenu openen
        logger = functions.setup_logger("Main") if not getLogger("Main").hasHandlers() else getLogger("Main")
        app = 0
        app = QtWidgets.QApplication(sys.argv)
        window = Klassen_Schermen.Flexmenu(xw.Book.caller(), deelnemer, logger)
        
        window.show()
        app.exec_()
    else:
        functions.Mbox("foutmelding", "Er is geen deelnemer opgeslagen. \nGelieve eerst een deelnemer te selecteren via de knop 'Andere deelnemer'.", 0)
        
@xw.sub
def AndereDeelnemer():
    """
    Functie die het deelnemerselectie scherm opent
    """
    controle = functions.Mbox("Andere deelnemer selecteren", "Door een andere deelnemer te selecteren zullen de huidige gegevens op de vergelijken sheet verwijderd worden.\nU kunt deze actie niet ongedaan maken.", 1)
    if controle == "OK Clicked":
        #scherm Deelnemerselectie openen
        logger = functions.setup_logger("Main") if not getLogger("Main").hasHandlers() else getLogger("Main")
        app = 0
        app = QtWidgets.QApplication(sys.argv)
        window = Klassen_Schermen.Deelnemerselectie(xw.Book.caller(), logger)
        window.show()
        app.exec_()
    
@xw.sub
def BeheerderskeuzesOpenen():
    """
    Functie die het scherm met de beheerderskeuzes opent
    """
    
    #scherm Beheerderkeuzes openen
    logger = functions.setup_logger("Main") if not getLogger("Main").hasHandlers() else getLogger("Main")
    app = 0
    app = QtWidgets.QApplication(sys.argv)
    windowBeheerder = Klassen_Schermen.Beheerderkeuzes(xw.Book.caller(), logger)
    windowBeheerder.show()
    app.exec_()
    
@xw.sub
def InEnUitloggen() :
    """
    functie om in of uit te loggen als beheerder

    Returns
    -------
    None.

    """
    book = xw.Book.caller()
    logger = functions.setup_logger("Main") if not getLogger("Main").hasHandlers() else getLogger("Main")
    if functions.isBeheerder(book):
        #beheerder is ingelogd, dus wil uitloggen
        controle = functions.Mbox("Uitloggen", "Weet u zeker dat u wilt uitloggen?",4)
        if controle == "Ja":
            app = 0
            app = QtWidgets.QApplication(sys.argv)
            windowBeheerder = Klassen_Schermen.Beheerderkeuzes(xw.Book.caller(), logger)
            windowBeheerder.btnUitloggenClicked()
            app.exec_()
        
    else:
        #beheerder is niet ingelogd, dus wil inloggen
        app = 0
        app = QtWidgets.QApplication(sys.argv)
        windowInloggen = Klassen_Schermen.Inloggen(xw.Book.caller(), logger)
        windowInloggen.show()
        app.exec_()
                 
@xw.sub
def flexibilisaties_testen():
   book = xw.Book.caller()
   invoer = book.sheets["Tijdelijk invoerscherm"] 
   
   flexibilisaties= invoer.range((24,2), (55,6))
   
   regeling_range= invoer.range((10,1), (20,1))
   aanspraken = invoer.range((10,2), (20,2))
   pensioenleeftijd= invoer.range((10,5), (20,5))
   koopsomfactor= invoer.range((10,6), (20,6))
   basis_koopsom= invoer.range((10,7), (20,7))
   
   koopsommen = basis_koopsom.value
   regelingen= regeling_range.value  

   #loop voor rijen
   for i in range(1,5):
       regeling = (i-1)*10+1
       soort = (i-1)*10+2
       verhouding = (i-1)*10+3
       duur = (i-1)*10+4
       factor_OP = (i-1)*10+5
       factor_PP = (i-1)*10+6
       aanspraak_OP = (i-1)*10+7
       aanspraak_PP = (i-1)*10+8
       
       factor_deel1 = (i-1)*10+5
       factor_deel2 = (i-1)*10+6
       aanspraak_deel1 = (i-1)*10+7
       aanspraak_deel2 = (i-1)*10+8

       flex_vak = invoer.range((factor_OP+23, 2), (aanspraak_PP+23, 5))
       flex_vak.clear_contents()

       #loop voor kolommen
       for c in range(1,5):
           if flexibilisaties(regeling, c).value != None:
               rij= regelingen.index(flexibilisaties(regeling, c).value)
               if "vervroegen" in flexibilisaties(soort, c).value or "verlaten" in flexibilisaties(soort, c).value:
                   #Bij corresponderende pensioenregelingsrij de hoeveelheid vervroegen/verlaten optellen
                   pensioenleeftijd(rij+1).value = pensioenleeftijd(rij+1).value + flexibilisaties(duur, c).value
                   pensioenleeftijd(rij+2).value = pensioenleeftijd(rij+2).value + flexibilisaties(duur, c).value
                   flexibilisaties(factor_OP, c).formula = koopsomfactor(rij+1).formula
                   flexibilisaties(factor_PP, c).formula = koopsomfactor(rij+2).formula
                   flexibilisaties(aanspraak_OP, c).value = round(float(koopsommen[rij]) / flexibilisaties(factor_OP, c).value)
                   flexibilisaties(aanspraak_PP, c).value = round(float(koopsommen[rij+1]) / flexibilisaties(factor_PP, c).value)
                   
                   OP_nieuw = float(flexibilisaties(aanspraak_OP, c).value)
                   PP_nieuw = float(flexibilisaties(aanspraak_PP, c).value)

               elif "AOW" in flexibilisaties(soort, c).value:
                   flexibilisaties(factor_OP, c).value = "Berekeningen komen later"
                       
               
               elif  "uitruilen" in flexibilisaties(soort, c).value:
                   uitruilen_naar = flexibilisaties(soort, c).value[-2:]
                   flexibilisaties(factor_OP, c).formula = koopsomfactor(rij+1).formula
                   flexibilisaties(factor_PP, c).formula = koopsomfactor(rij+2).formula
                   
                   if ":" in str(flexibilisaties(verhouding, c).value):
                       verhouding_uitruilen = int(flexibilisaties(verhouding, c).value[-2:])/100
                       if uitruilen_naar == "PP":
                           flexibilisaties(aanspraak_OP, c).value = float(koopsommen[rij]) / (flexibilisaties(factor_OP, c).value + verhouding_uitruilen * flexibilisaties(factor_PP, c).value)
                           flexibilisaties(aanspraak_PP, c).value = round(float(flexibilisaties(aanspraak_OP, c).value) * verhouding_uitruilen + PP_nieuw)
                           flexibilisaties(aanspraak_OP, c).value = round(flexibilisaties(aanspraak_OP, c).value)
                           
                           OP_nieuw = float(flexibilisaties(aanspraak_OP, c).value)
                           PP_nieuw = float(flexibilisaties(aanspraak_PP, c).value)
                       else:
                           flexibilisaties(aanspraak_PP, c).value = float(koopsommen[rij+1]) / (flexibilisaties(factor_PP, c).value + verhouding_uitruilen * flexibilisaties(factor_OP, c).value)
                           flexibilisaties(aanspraak_OP, c).value = round(float(flexibilisaties(aanspraak_PP, c).value) * verhouding_uitruilen + OP_nieuw)
                           flexibilisaties(aanspraak_PP, c).value = round(flexibilisaties(aanspraak_PP, c).value)
                           
                           OP_nieuw = float(flexibilisaties(aanspraak_OP, c).value)
                           PP_nieuw = float(flexibilisaties(aanspraak_PP, c).value)
                           
                   else:
                       if uitruilen_naar == "PP":
                           verschil_uitruilen = flexibilisaties(verhouding, c).value * OP_nieuw
                           flexibilisaties(aanspraak_OP, c).value = round(OP_nieuw - verschil_uitruilen)
                           flexibilisaties(aanspraak_PP, c).value = round(verschil_uitruilen * flexibilisaties(factor_OP, c).value / flexibilisaties(factor_PP, c).value + PP_nieuw)
                           
                           OP_nieuw = float(flexibilisaties(aanspraak_OP, c).value)
                           PP_nieuw = float(flexibilisaties(aanspraak_PP, c).value)
                       else:
                           verschil_uitruilen = flexibilisaties(verhouding, c).value * PP_nieuw
                           flexibilisaties(aanspraak_PP, c).value = round(PP_nieuw - verschil_uitruilen)
                           flexibilisaties(aanspraak_OP, c).value = round(verschil_uitruilen * flexibilisaties(factor_PP, c).value / flexibilisaties(factor_OP, c).value + OP_nieuw)
                           
                           OP_nieuw = float(flexibilisaties(aanspraak_OP, c).value)
                           PP_nieuw = float(flexibilisaties(aanspraak_PP, c).value)
    
               else:
                   flex_duur = int(flexibilisaties(duur, c).value)
                   x = koopsomfactor(rij+1).formula
                   
                   if x.index('61') != None:
                       y = x.replace('61', str(flex_duur+1))

                   if x.index('2') != None:
                       z = x.replace('2', str(flex_duur+2))
                       
                   #Hoog-Laag constructie    
                   if "hoog" in flexibilisaties(soort, c).value:
                       flexibilisaties(factor_deel1, c).formula = y 
                       if ":" in str(flexibilisaties(verhouding, c).value):
                           soort_HL = int(flexibilisaties(verhouding, c).value[-2:])/100
                           flexibilisaties(factor_deel2, c).formula = y + '+' + z[1:] + '*' + str(soort_HL)
                           flexibilisaties(aanspraak_deel1, c).value = (OP_nieuw * koopsomfactor(rij+1).value) / flexibilisaties(factor_deel2, c).value
                           flexibilisaties(aanspraak_deel2, c).value = round(float(flexibilisaties(aanspraak_deel1, c).value) * soort_HL)
                           flexibilisaties(aanspraak_deel1, c).value = round(flexibilisaties(aanspraak_deel1, c).value)

                       else:
                           soort_HL = flexibilisaties(verhouding, c).value
                           flexibilisaties(factor_deel2, c).formula = z
                           flexibilisaties(aanspraak_deel1, c).value = ((OP_nieuw * koopsomfactor(rij+1).value) + soort_HL*flexibilisaties(factor_deel2, c).value)/koopsomfactor(rij+1).value
                           flexibilisaties(aanspraak_deel2, c).value = round(flexibilisaties(aanspraak_deel1, c).value - soort_HL)
                           flexibilisaties(aanspraak_deel1, c).value = round(flexibilisaties(aanspraak_deel1, c).value)

                   #Laag-Hoog constructie        
                   else:
                       if ":" in str(flexibilisaties(verhouding, c).value):
                           soort_HL = int(flexibilisaties(verhouding, c).value[:2])/100
                           y = y + '*' + str(soort_HL)
                           flexibilisaties(factor_deel1, c).formula = y 
                           flexibilisaties(factor_deel2, c).formula = y + '+' + z[1:] 
                           flexibilisaties(aanspraak_deel2, c).value = (OP_nieuw * koopsomfactor(rij+1).value) / flexibilisaties(factor_deel2, c).value
                           flexibilisaties(aanspraak_deel1, c).value = round(float(flexibilisaties(aanspraak_deel2, c).value) * soort_HL)
                           flexibilisaties(aanspraak_deel2, c).value = round(flexibilisaties(aanspraak_deel2, c).value)
                           
                       else:
                           flexibilisaties(factor_deel1, c).formula = y 
                           soort_HL = flexibilisaties(verhouding, c).value
                           flexibilisaties(factor_deel2, c).formula = z
                           flexibilisaties(aanspraak_deel1, c).value = (OP_nieuw * koopsomfactor(rij+1).value - soort_HL * flexibilisaties(factor_deel2, c).value)/koopsomfactor(rij+1).value
                           flexibilisaties(aanspraak_deel2, c).value = round(flexibilisaties(aanspraak_deel1, c).value + soort_HL)
                           flexibilisaties(aanspraak_deel1, c).value = round(flexibilisaties(aanspraak_deel1, c).value)
                    
                           
       