class Pracownik:
    def __init__(self, imie, nazwisko):
        self.__imie = imie
        self.__nazwisko = nazwisko
        self.__lista_kart = []

    def __str__(self):
        return self.__id

    def dodajKarte(self, karta):
        self.__lista_kart.append(karta)

    def getId(self):
        return self.__id

    def getImie(self):
        return  self.__imie

    def getNazwisko(self):
        return self.__nazwisko