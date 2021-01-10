class Karta:
    def __init__(self, id_karty):
        self.__id = id_karty

    def __str__(self):
        return self.__id

    def getId(self):
        return self.__id
