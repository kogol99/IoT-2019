#!/usr/bin/env python3
from datetime import datetime

import paho.mqtt.client as mqtt
import tkinter.messagebox
import time

from system import System

MQTT_BROKER = "BROKER-NAME"
MQTT_PORT = 8883
MQTT_TLS_CRT = 'ca.crt'
USERNAME = 'USERNAME'
PASSWORD = 'PASS'

client = mqtt.Client()
window = tkinter.Tk()
system = System()


def aktualny_czas():
    aktualny_czas_sczytanie = datetime.now()
    aktualny_czas_format = aktualny_czas_sczytanie.strftime("%Y-%m-%dT%H:%M:%S")
    return aktualny_czas_format


def process_message(client, userdata, message):
    zdekodowana_wiadomosc = (str(message.payload.decode("utf-8"))).split(".")

    if zdekodowana_wiadomosc[0] != "Podłączenie terminala" and zdekodowana_wiadomosc[
        0] != "Terminal zakończył połączenie":
        system.nowe_sczytanie(aktualny_czas(), zdekodowana_wiadomosc[0], zdekodowana_wiadomosc[1])
        print(time.ctime() + ", " +
              zdekodowana_wiadomosc[0] + " użył terminala o id: " + zdekodowana_wiadomosc[1] + ". ")
    else:
        print(zdekodowana_wiadomosc[0] + " : " + zdekodowana_wiadomosc[1])


def wyswietl_liste_pracownikow():
    elementy_do_wyswietlenia = []
    lista_pracownikow = tkinter.Tk()
    lista_pracownikow.title("Lista praocwnikow")

    for pracownik in open('Pracownicy.txt', 'r+t'):
        dane = pracownik.replace("\n", "")
        dane = dane.split(";")
        if len(dane) == 2:
            elementy_do_wyswietlenia.append(tkinter.Label(lista_pracownikow, text=(
                    "Imie: %s, nazwisko: %s, brak przypisanych kart" % (dane[0], dane[1]))))
        else:
            elementy_do_wyswietlenia.append(tkinter.Label(lista_pracownikow, text=(
                    "Imie: %s, nazwisko: %s, przypisane karty: %s" % (dane[0], dane[1], dane[2]))))

    for label in elementy_do_wyswietlenia:
        label.pack(side="top")

    lista_pracownikow.mainloop()


def wyswietl_raport():
    raport = tkinter.Tk()
    raport.title("Raport")
    id_linii = 0

    for linia in open('Raport.txt', 'r+t'):
        id_linii += 1
        dane = linia.replace("\n", "")
        dane = dane.split(";")
        for i in range(len(dane)):
            tkinter.Label(raport, text=dane[i]).grid(row=id_linii, column=i)

    raport.mainloop()


class Aplikacja:
    def __init__(self):
        window.geometry("500x660")
        window.title("System zarządzający czytnikami RFID")
        label = tkinter.Label(window, text="System zarządzający czytnikami RFID", font=("Sans-serif", 16, "italic"))
        dodaj_pracownika_podpis = tkinter.Label(window, text="Dodaj pracownika", font=("Sans-serif", 13), anchor='e')
        dodaj_pracownika_imie_podpis = tkinter.Label(window, text="Imię:")
        self.dodaj_pracownika_imie_pole = tkinter.Entry()
        dodaj_pracownika_nazwisko_podpis = tkinter.Label(window, text="Nazwisko:")
        self.dodaj_pracownika_nazwisko_pole = tkinter.Entry()
        dodaj_pracownika_przycisk = tkinter.Button(window, text="Dodaj pracownika", command=self.dodaj_pracownika)
        wyswietl_pracownikow_przycisk = tkinter.Button(window, text="Wyswietl liste pracownikow",
                                                       command=wyswietl_liste_pracownikow)

        przypisz_karte_podpis = tkinter.Label(window, text="Przypisz/Usuń kartę do pracownika", font=("Sans-serif", 13))
        przypisz_karte_imie_podpis = tkinter.Label(window, text="Imię:")
        self.przypisz_karte_imie_pole = tkinter.Entry()
        przypisz_karte_nazwisko_podpis = tkinter.Label(window, text="Nazwisko:")
        self.przypisz_karte_nazwisko_pole = tkinter.Entry()
        przypisz_karte_idkarty_podpis = tkinter.Label(window, text="ID Karty:")
        self.przypisz_karte_idkarty_pole = tkinter.Entry()
        przypisz_karte_przycisk = tkinter.Button(window, text="Przypisz kartę do pracownika",
                                                 command=self.przypisz_karte)
        usun_karte_pracownikowi_przycisk = tkinter.Button(window, text="Usun przypisanie karty do pracownika",
                                                          command=self.usuna_karte_pracownikowi)

        wylacz_system_przycisk = tkinter.Button(window, text="Wyłącz system", command=window.quit)
        wygeneruj_raport_przycisk = tkinter.Button(window, text="Wygeneruj raport", command=self.wygeneruj_raport)
        wyswietl_raport_przycisk = tkinter.Button(window, text="Wyswietl raport", command=wyswietl_raport)
        podziekuje_klientom_przycisk = tkinter.Button(window, text="Podziękuj czytnikom za dobrą pracę",
                                                      command=lambda: client.publish("server/name",
                                                                                     "Urządzenie główne dziękuje za "
                                                                                     "dobrą pracę"))
        label.pack(pady=(8, 15))
        dodaj_pracownika_podpis.pack()
        dodaj_pracownika_imie_podpis.pack()
        self.dodaj_pracownika_imie_pole.pack()
        dodaj_pracownika_nazwisko_podpis.pack()
        self.dodaj_pracownika_nazwisko_pole.pack()
        dodaj_pracownika_przycisk.pack(pady=(7, 20))

        przypisz_karte_podpis.pack(fill='both')
        przypisz_karte_imie_podpis.pack()
        self.przypisz_karte_imie_pole.pack()
        przypisz_karte_nazwisko_podpis.pack()
        self.przypisz_karte_nazwisko_pole.pack()
        przypisz_karte_idkarty_podpis.pack()
        self.przypisz_karte_idkarty_pole.pack()
        przypisz_karte_przycisk.pack(pady=(7, 3))
        usun_karte_pracownikowi_przycisk.pack(pady=(0, 20))

        wygeneruj_raport_przycisk.pack(pady=10)
        wyswietl_pracownikow_przycisk.pack(pady=(5, 5))
        wyswietl_raport_przycisk.pack(pady=(5, 20))
        podziekuje_klientom_przycisk.pack(pady=(5, 20))
        wylacz_system_przycisk.pack()

    def dodaj_pracownika(self):
        imie = str(self.dodaj_pracownika_imie_pole.get())
        nazwisko = str(self.dodaj_pracownika_nazwisko_pole.get())
        if imie == "" or nazwisko == "":
            czy_dodano = False
        else:
            czy_dodano = system.dodaj_pracownika(imie, nazwisko)
        if czy_dodano:
            tkinter.messagebox.showinfo('Informacja', 'Pracownik został dodany')
        else:
            tkinter.messagebox.showinfo('Informacja', 'Pracownik nie został dodany, sprawdź poprawność danych')

    def przypisz_karte(self):
        imie = str(self.przypisz_karte_imie_pole.get())
        nazwisko = str(self.przypisz_karte_nazwisko_pole.get())
        id_karty = str(self.przypisz_karte_idkarty_pole.get())
        if imie == "" or nazwisko == "" or id_karty == "":
            czy_przypisano = False
        else:
            czy_przypisano = system.przypisz_karte(id_karty, imie, nazwisko, )
        if czy_przypisano:
            tkinter.messagebox.showinfo('Informacja', 'Karta została przypisana do podanego pracownika')
        else:
            tkinter.messagebox.showinfo('Informacja', 'Karta nie została przypisana, sprawdź poprawność danych')

    def usuna_karte_pracownikowi(self):
        imie = str(self.przypisz_karte_imie_pole.get())
        nazwisko = str(self.przypisz_karte_nazwisko_pole.get())
        id_karty = str(self.przypisz_karte_idkarty_pole.get())
        if imie == "" or nazwisko == "" or id_karty == "":
            czy_usunieto = False
        else:
            czy_usunieto = system.usuna_karte_pracownikowi(id_karty, imie, nazwisko)
        if czy_usunieto:
            tkinter.messagebox.showinfo('Informacja', 'Karta została usunięta u podanego pracownika')
        else:
            tkinter.messagebox.showinfo('Informacja', 'Karta nie została usunięta, sprawdź poprawność danych')

    def wygeneruj_raport(self):
        system.wygeneruj_raport()
        tkinter.messagebox.showinfo('Informacja', 'Raport został zapisany do pliku raport.txt . '
                                                  'Możesz uzyć go bez przeszkód w programie Excel')


def polacz_z_broker():
    client.tls_set(MQTT_TLS_CRT)
    client.username_pw_set(username=USERNAME, password=PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("worker/name")


def rozlacz_z_broker():
    client.loop_stop()
    client.disconnect()


def uruchom_serwer():
    polacz_z_broker()
    Aplikacja()
    window.mainloop()
    rozlacz_z_broker()


if __name__ == "__main__":
    uruchom_serwer()
