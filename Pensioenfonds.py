"""
Header
Hier komen alle libraries die in het programma gebruikt worden
"""


"""
Body
Hier komen alle functies
"""
class Pensioenfonds():
    """
    Een class waarin de informatie over een pensioenfonds van een deelnemer staat opgeslagen.
    
    book : xlwings.Book
        Het excel bestand waarin het programma runned.
    pensioenrij : int
        De rij waarin de informatie over het pensioenfonds staat.
    OPenPP : tuple
        Een tuple met de waarde van het ouderdomspensioen en het partnerpensioen.
    """
    
    def __init__(self, gegevensSheet, kolommen, pensioen):
        OPenPP = pensioen[0]
        gegevensRij = pensioen[1]
        
        
        self._naam = gegevensSheet.range((gegevensRij, kolommen["naamkolom"])).value
        self._volNaam = ""
        self.volledigeNaam()
        
        self._pensioenleefijd = gegevensSheet.range((gegevensRij, kolommen["pensioenleeftijdkolom"])).value
        self._rente = float(gegevensSheet.range((gegevensRij, kolommen["rentekolom"])).options(numbers = float).value)
        self._sterftetafel = gegevensSheet.range((gegevensRij, kolommen["sterftetafelkolom"])).value
        
        self._ouderdomsPensioen = OPenPP[0]
        self._partnerPensioen = OPenPP[1]
    
    def volledigeNaam(self):
        if self._naam == "ZL": self._volNaam = "ZwitserLeven"
        elif self._naam == "Aegon OP65": self._volNaam = self._naam
        elif self._naam == "Aegon OP67": self._volNaam = self._naam
        elif self._naam == "NN OP65": self._volNaam = "Nationale Nederlanden OP65"
        elif self._naam == "NN OP67": self._volNaam = "Nationale Nederlanden OP67"
        elif self._naam == "PF VLC OP68": self._volNaam = "Pensioenfonds VLC OP68"
            
    @property
    def pensioenVolNaam(self):
        return self._volNaam
    
    @property
    def pensioenNaam(self):
        return self._naam
    
    @property
    def pensioenleefijd(self):
        return self._pensioenleefijd
    
    @property
    def rente(self):
        return self._rente
    
    @property
    def sterftetafel(self):
        return self._sterftetafel
    
    @property
    def ouderdomsPensioen(self):
        return self._ouderdomsPensioen
    
    @property
    def partnerPensioen(self):
        return self._partnerPensioen
    
    