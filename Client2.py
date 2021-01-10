from random import randint
from tkinter import messagebox

import paho.mqtt.client as mqtt
import tkinter

ID_TERMINALA = "T1"
MQTT_BROKER = "BROKER-NAME"
MQTT_PORT = 8883
MQTT_TLS_CRT = 'ca.crt'
USERNAME = 'USERNAME'
PASSWORD = 'PASS'

client = mqtt.Client()
window = tkinter.Tk()


def poinformuj_serwer(informacja):
    client.publish("worker/name", informacja + "." + ID_TERMINALA, )


def stworz_glowne_okno():
    window.geometry("400x320")
    window.title("Czytnik kart RFID")

    tkinter.Label(window, text="Wybierz symulacje sczytania karty:",
                  font=("Sans-serif", 14, "italic")).pack(pady=20)
    tkinter.Button(window, text="325643567864",
                   command=lambda: poinformuj_serwer("325643567864")).pack(pady=3)
    tkinter.Button(window, text="324685456443",
                   command=lambda: poinformuj_serwer("324685456443")).pack(pady=3)
    tkinter.Button(window, text="345678754653",
                   command=lambda: poinformuj_serwer("345678754653")).pack(pady=3)
    tkinter.Button(window, text="375689657564",
                   command=lambda: poinformuj_serwer("375689657564")).pack(pady=3)
    tkinter.Button(window, text="Losowe ID Karty",
                   command=lambda: poinformuj_serwer(str(randint(300000000000, 399999999999)))).pack(pady=3)

    tkinter.Button(window, text="Wyłącz czytnik", command=window.quit).pack(pady=20)


def polacz_z_broker():
    client.tls_set(MQTT_TLS_CRT)
    client.username_pw_set(username=USERNAME, password=PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT)
    poinformuj_serwer("Client połączył się")
    client.on_message = process_message
    client.loop_start()
    client.subscribe("server/name")


def rozlacz_z_broker():
    poinformuj_serwer("Client zakończył połączenie")
    client.disconnect()


def uruchom_czytnik():
    polacz_z_broker()
    stworz_glowne_okno()
    window.mainloop()
    rozlacz_z_broker()


def process_message(client, userdata, message):
    message_decoded = (str(message.payload.decode("utf-8")))
    messagebox.showinfo("Message from the Server", message_decoded)


if __name__ == "__main__":
    uruchom_czytnik()
