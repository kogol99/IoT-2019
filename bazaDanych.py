from datetime import datetime
from os import strerror
import os


class BazaDanych:
    def __init__(self):
        self.__plik_pracownikow = 'Pracownicy.txt'
        self.__plik_kart = 'Karty.txt'
        self.__plik_czytnikow = 'Czytniki.txt'
        self.__plik_sczytan = 'Sczytania.txt'

    def dodaj_pracownika(self, imie, nazwisko):
        if self.czy_pracownik_istnieje(imie, nazwisko):
            print("Nie dodano pracownika, podane dane widnieja juz w bazie danych")
            return False
        else:
            try:
                s = open(self.__plik_pracownikow, 'a')
                s.write(imie + ";" + nazwisko + "\n")
                s.close()
            except IOError as e:
                print("Blad dodaj_pracownika I/O:", strerror(e.errno))
            return True

    def czy_pracownik_istnieje(self, imie, nazwisko):
        try:
            for linia in open(self.__plik_pracownikow, 'r'):
                dane = linia.replace("\n", "")
                dane = dane.split(";")
                if dane[0] == imie and (dane[1] == nazwisko):
                    return True
            return False
        except IOError:
            return False

    def dodaj_karte(self, id_karty):
        if self.czy_karta_istnieje(id_karty):
            print("Nie dodano karty, podane dane widnieja juz w bazie danych")
        else:
            try:
                s = open(self.__plik_kart, 'a')
                s.write(str(id_karty) + "\n")
                s.close()
            except IOError as e:
                print("Blad dodaj_karte I/O:", strerror(e.errno))

    def czy_karta_istnieje(self, id_karty):
        try:
            for linia in open(self.__plik_kart, 'r+'):
                if linia == str(id_karty) + '\n':
                    return True
            return False
        except IOError:
            return False

    def dodaj_czytnik(self, id_czytnika):
        if self.czy_czytnik_istnieje(id_czytnika):
            print("Nie dodano czytnika, podane dane widnieja juz w bazie danych")
        else:
            try:
                s = open(self.__plik_czytnikow, 'a')
                s.write(str(id_czytnika) + "\n")
                s.close()
            except IOError as e:
                print("Blad dodaj_czytnik I/O:", strerror(e.errno))

    def czy_czytnik_istnieje(self, id_czytnika):
        try:
            for linia in open(self.__plik_czytnikow, 'r+'):
                if linia == str(id_czytnika) + '\n':
                    return True
            return False
        except IOError:
            return False

    def nowe_sczytanie(self, data, id_karty, id_czytnika):
        try:
            s = open(self.__plik_sczytan, 'a')
            s.write(str(data) + ";" + str(id_karty) + ";" + str(id_czytnika) + "\n")
            s.close()
        except IOError as e:
            print("Blad nowe_sczytanie I/O:", strerror(e.errno))

    def usun_pracownika(self, imie, nazwisko):
        try:
            nowy_plik = open('nowy_pracownicy.txt', 'w+t')
            czy_usuniety = False
            for linia in open(self.__plik_pracownikow, 'rt'):
                dane = linia.split(";")
                if dane[0] == imie and dane[1] == nazwisko + '\n' and not czy_usuniety:
                    czy_usuniety = True
                else:
                    nowy_plik.write(linia)
            os.remove(self.__plik_pracownikow)
            nowy_plik.close()
            os.rename('nowy_pracownicy.txt', self.__plik_pracownikow)
        except IOError as e:
            print("Blad usun_pracownika I/O:", strerror(e.errno))

    def usun_karte(self, id_karty):
        try:
            nowy_plik = open('nowy_karty.txt', 'w+t')
            czy_usuniety = False
            for linia in open(self.__plik_kart, 'rt'):
                if linia == str(id_karty) + '\n' and not czy_usuniety:
                    czy_usuniety = True
                else:
                    nowy_plik.write(linia)
            os.remove(self.__plik_kart)
            nowy_plik.close()
            os.rename('nowy_karty.txt', self.__plik_kart)
        except IOError as e:
            print("Blad usun_karte I/O:", strerror(e.errno))

    def usun_czytnik(self, id_czytnika):
        try:
            nowy_plik = open('nowy_czytniki.txt', 'w+t')
            czy_usuniety = False
            for linia in open(self.__plik_czytnikow, 'rt'):
                if linia == str(id_czytnika) + '\n' and not czy_usuniety:
                    czy_usuniety = True
                else:
                    nowy_plik.write(linia)
            os.remove(self.__plik_czytnikow)
            nowy_plik.close()
            os.rename('nowy_czytniki.txt', self.__plik_czytnikow)
        except IOError as e:
            print("Blad usun_czytnik I/O:", strerror(e.errno))

    def przypisz_karte(self, id_karty, imie, nazwisko):
        try:
            nowy_plik = open('nowy_pracownicy.txt', 'w+t')
            czy_dodane_do_os = False
            czy_wykonano_poprawnie = False
            for linia in open(self.__plik_pracownikow, 'rt'):
                dane = linia.replace("\n", "")
                dane = dane.split(";")
                if dane[0] == imie and dane[1] == nazwisko and not czy_dodane_do_os:
                    if len(dane) == 2:
                        nowy_plik.write(dane[0] + ";" + dane[1] + ";" + str(id_karty) + "\n")
                        czy_wykonano_poprawnie = True
                    elif not self.czy_karta_juz_przypisana(dane[2], id_karty):
                        dane[2] += "," + str(id_karty)
                        nowy_plik.write(dane[0] + ";" + dane[1] + ";" + dane[2] + "\n")
                        czy_wykonano_poprawnie = True
                    else:
                        nowy_plik.write(linia)
                    czy_dodane_do_os = True
                else:
                    nowy_plik.write(linia)
            os.remove(self.__plik_pracownikow)
            nowy_plik.close()
            os.rename('nowy_pracownicy.txt', self.__plik_pracownikow)
        except IOError as e:
            print("Blad usun_czytnik I/O:", strerror(e.errno))
            return False
        if czy_wykonano_poprawnie:
            return True
        else:
            return False

    def usuna_karte_pracownikowi(self, id_karty, imie, nazwisko):
        czy_byla_dodana = True
        try:
            nowy_plik = open('nowy_pracownicy.txt', 'w+t')
            czy_usunieta = False
            for linia in open(self.__plik_pracownikow, 'rt'):
                dane = linia.replace("\n", "")
                dane = dane.split(";")
                if dane[0] == imie and dane[1] == nazwisko and not czy_usunieta:
                    if len(dane) == 2:
                        czy_byla_dodana = False
                        nowy_plik.write(linia)
                    elif self.czy_karta_juz_przypisana(dane[2], id_karty):
                        nowa_lista_kart = self.usun_karte_z_listy(dane[2], id_karty)
                        if len(nowa_lista_kart) == 0:
                            nowy_plik.write(dane[0] + ";" + dane[1] + "\n")
                        else:
                            nowy_plik.write(dane[0] + ";" + dane[1] + ";" +
                                            str(nowa_lista_kart) + "\n")
                    else:
                        nowy_plik.write(linia)
                        czy_byla_dodana = False
                    czy_usunieta = True
                else:
                    nowy_plik.write(linia)
            os.remove(self.__plik_pracownikow)
            nowy_plik.close()
            os.rename('nowy_pracownicy.txt', self.__plik_pracownikow)
        except IOError as e:
            print("Blad usun_czytnik I/O:", strerror(e.errno))
            return False
        if czy_byla_dodana:
            return True
        else:
            return False

    def czy_karta_juz_przypisana(self, lista_kart, id_karty):
        karty = lista_kart.split(",")
        for i in range(len(karty)):
            if karty[i] == str(id_karty):
                print("Nie przypisano karty, poniewaz juz istnieje u tego pracownika " + str(id_karty))
                return True

    def usun_karte_z_listy(self, lista_kart, id_karty):
        z_przecinkiem_przed = "," + str(id_karty)
        z_przecinkiem_za =  str(id_karty) + ","
        lista_kart = lista_kart.replace(z_przecinkiem_przed,"")
        lista_kart = lista_kart.replace(z_przecinkiem_za,"")
        return lista_kart

    def get_id_czytnikow(self):
        lista_czytnikow = []
        try:
            for linia in open(self.__plik_czytnikow, 'r+'):
                lista_czytnikow.append(linia[:-1])
        except IOError:
            pass
        finally:
            return lista_czytnikow

    def get_id_kart(self):
        lista_kart = []
        try:
            for linia in open(self.__plik_kart, 'r+'):
                lista_kart.append(linia[:-1])
        except IOError:
            pass
        finally:
            return lista_kart

    def wygeneruj_raport(self):
        raport = open('raport.txt', 'w+t')
        raport.write(
            "Imie;Nazwisko;Wejscie o godzinie;Wejsc z karty; Wejscie na czytniku;"
            "Wyjscie o godzinie;Wyjscie z karty;Wyjscie na czytniku;Czas pracy\n")
        for pracownik in open(self.__plik_pracownikow, 'r+t'):
            dane_pracownika = pracownik.split(";")
            if len(dane_pracownika) == 2:
                raport.write(dane_pracownika[0] + ";" + dane_pracownika[1][:-1] + ";;;;;;;\n")
            else:
                lista_kart = dane_pracownika[2].replace("\n", "")
                lista_kart = lista_kart.split(",")
                lista_sczytan_pracownika = []
                for sczytanie in open(self.__plik_sczytan, 'r+t'):
                    dane_sczytania = sczytanie.split(";")
                    for i in range(len(lista_kart)):
                        if dane_sczytania[1] == lista_kart[i]:
                            lista_sczytan_pracownika.append(sczytanie)
                for i in range(0, len(lista_sczytan_pracownika), 2):
                    sczytanie1 = lista_sczytan_pracownika[i].split(";")
                    if i + 1 == len(lista_sczytan_pracownika):
                        raport.write(
                            dane_pracownika[0] + ";" + dane_pracownika[1] + ";" + sczytanie1[0] + ";" + sczytanie1[
                                1] + ";" + sczytanie1[2][:-1] + ";;;;\n")
                    else:
                        sczytanie2 = lista_sczytan_pracownika[i + 1].split(";")
                        koniec_pracy = datetime.fromisoformat(sczytanie2[0])
                        poczatek_pracy = datetime.fromisoformat(sczytanie1[0])
                        okres_pracy = koniec_pracy - poczatek_pracy
                        raport.write(
                            dane_pracownika[0] + ";" + dane_pracownika[1] + ";" + sczytanie1[0] + ";" + sczytanie1[
                                1] + ";" + sczytanie1[2][:-1] + ";" + sczytanie2[0] + ";" + sczytanie2[1] + ";" +
                            sczytanie2[
                                2][:-1] + ";" + str(okres_pracy) + "\n")

        raport.close()
