from bazaDanych import BazaDanych
from random import randint


class System:
    def __init__(self):
        self.__lp_czytnika = 0
        self.__bazaDanych = BazaDanych()

    def dodaj_pracownika(self, imie, nazwisko):
        print("Dodaje pracownika")
        return self.__bazaDanych.dodaj_pracownika(imie, nazwisko)

    def dodaj_karte(self, id_karty):
        self.__bazaDanych.dodaj_karte(id_karty)

    def dodaj_czytnik(self, id_czytnika):
        self.__bazaDanych.dodaj_czytnik(id_czytnika)

    def nowe_sczytanie(self, data, id_karty, id_czytnika):
        self.__bazaDanych.nowe_sczytanie(data, id_karty, id_czytnika)

    def usun_pracownika(self, imie, nazwisko):
        self.__bazaDanych.usun_pracownika(imie, nazwisko)

    def usun_karte(self, id_karty):
        self.__bazaDanych.usun_karte(id_karty)

    def usun_czytnik(self, id_czytnika):
        self.__bazaDanych.usun_czytnik(id_czytnika)

    def przypisz_karte(self, id_karty, imie, nazwisko):
        return self.__bazaDanych.przypisz_karte(id_karty, imie, nazwisko)

    def usuna_karte_pracownikowi(self, id_karty, imie, nazwisko):
        return self.__bazaDanych.usuna_karte_pracownikowi(id_karty, imie, nazwisko)

    def wygeneruj_losowe_sczytanie(self, data):
        random_id = randint(300000000000, 399999999999)
        self.nowe_sczytanie(data, random_id, int(self.wybierz_czytnik()))

    def wygeneruj_prawdziwe_sczytanie(self, data):
        self.nowe_sczytanie(data, int(self.wybierz_karte()), int(self.wybierz_czytnik()))

    def wybierz_czytnik(self):
        lista_czytnikow = self.__bazaDanych.get_id_czytnikow()
        rand = randint(0, len(lista_czytnikow) - 1)
        return lista_czytnikow[rand]

    def wybierz_karte(self):
        lista_kart = self.__bazaDanych.get_id_kart()
        random_card = randint(0, len(lista_kart) - 1)
        return lista_kart[random_card]

    def wygeneruj_raport(self):
        self.__bazaDanych.wygeneruj_raport()
