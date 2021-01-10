class Czytnik:
    def __init__(self, id_czytnika):
        self.__id = id_czytnika

    def __str__(self):
        return self.__id

    def getId(self):
        return self.__id