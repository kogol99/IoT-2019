class Sczytanie:
    def __init__(self, karta, czytnik, data):
        self.__karta = karta
        self.__czytnik = czytnik
        self.__data = data

    def __str__(self):
        return '= ZCZYTANIE = karta' + self.__karta + ', czytnik' + self.__czytnik + ', data ' + self.__data