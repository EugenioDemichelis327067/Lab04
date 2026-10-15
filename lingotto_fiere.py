class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.nome=nome
        self.stands={}
        self.espositori={}
        self.assegnazioni={}


    """Aggiungere setter e getter se necessari"""
    # TODO

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""

        self.file_path=file_path
        try:
            with open(file_path, "r") as infile:
                for riga in infile:
                    riga=riga.strip().split(",")
                    if len(riga)==3:
                        codice = riga[0]
                        nome=riga[1]
                        cognome=riga[2]
                        e=Espositore(codice,nome,cognome)
                        self.espositori[codice]=e

                    elif len(riga)==4:
                        codice=riga[0]
                        dimensioni=float(riga[1])
                        padiglione=riga[2]
                        prezzoFinale=float(riga[3])
                        c=Stand(codice,dimensioni,padiglione,prezzoFinale)
                        self.stands[codice]=c
                    elif len(riga)== 5:
                        try:
                            int(riga[4])
                            codice = riga[0]
                            dimensioni = float(riga[1])
                            padiglione = riga[2]
                            prezzo = float(riga[3])
                            numeroPrese=int(riga[4])
                            prezzoFinale=prezzo * (1 + 0.07 * numeroPrese)
                            c = StandConPrese(codice, dimensioni, padiglione, prezzo,prezzoFinale)
                            self.stands[codice] = c
                        except ValueError:
                            codice = riga[0]
                            dimensioni = float(riga[1])
                            padiglione = riga[2]
                            prezzo = float(riga[3])
                            posizione = riga[4]
                            prezzoFinale= prezzo*1.3
                            c = StandPremium(codice, dimensioni, padiglione, prezzoFinale, posizione)
                            self.stands[codice] = c

        except FileNotFoundError:
            raise FileNotFoundError(f"file {file_path} non trovato")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        standDaAssociare=self.stands[codice_stand]
        espositoreDaAssociare=self.espositori[codice_espositore]
        if standDaAssociare.libero and espositoreDaAssociare.disponibilita:
            self.assegnazioni[codice_stand]=codice_espositore
            standDaAssociare.libero=False
            espositoreDaAssociare.disponibilita=False
            espositoreDaAssociare.standAssegnato=codice_stand
        elif not standDaAssociare.libero:
            raise Exception(f"lo stand {codice_stand} non è libero")
        elif not espositoreDaAssociare.libero:
            raise Exception(f"l'espositore da associare' {codice_espositore} non è disponibile")


    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for key,value in self.espositori.items():
            print(value)


    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        standOrdinatiPerPrezzo=sorted(self.stands.items(), key=lambda c: c[1].prezzoFinale )
        return standOrdinatiPerPrezzo



class Espositore:
    def __init__(self,codice,nome,cognome):
        self.codice=codice
        self.nome=nome
        self.cognome=cognome
        self.disponibilita=True
    def __str__(self):
        return f'{self.codice} {self.nome} {self.cognome}'
class Stand:
    def __init__(self,codice,dimensioniMetriQuadri,padiglione,prezzoFinale):
        self.codice=codice
        self.dimensioniMetriQuadri=dimensioniMetriQuadri
        self.padiglione=padiglione
        self.prezzoFinale=prezzoFinale
        self.libero=True
    @property
    def dimensioniMetriQuadri(self):
        return self._dimensioniMetriQuadri
    @dimensioniMetriQuadri.setter
    def dimensioniMetriQuadri(self,valore):
        if valore<0:
            raise ValueError("metri quadri negativi")
        self._dimensioniMetriQuadri=valore
    @property
    def prezzo(self):
        return self._prezzoFinale
    @prezzo.setter
    def prezzo(self,valore):
        if valore<0:
            raise ValueError("prezzo negativo")
        self._prezzoFinale=valore
    def __str__(self):
        return f'codice Stand: {self.codice}; dimensioniMetriQuadri: {self.dimensioniMetriQuadri}; padiglione: {self.padiglione}; prezzoFinale: {self.prezzoFinale}'

    def __repr__(self):
        return self.__str__()

class StandConPrese(Stand):
    def __init__(self,codice,dimensioniMetriQuadri,padiglione,prezzoFinale,numeroPrese):
        super().__init__(codice,dimensioniMetriQuadri,padiglione,prezzoFinale)
        self.numeroPrese=numeroPrese

    @property
    def numeroPrese(self):
        return self._numeroPrese
    @numeroPrese.setter
    def numeroPrese(self,valore):
        if valore <0:
            raise ValueError("numero prese negativo")
        self._numeroPrese=valore


class StandPremium(Stand):
    def __init__(self,codice,dimensioniMetriQuadri,padiglione,prezzoFinale,posizione):
        super().__init__(codice,dimensioniMetriQuadri,padiglione,prezzoFinale)
        self.posizione=posizione

