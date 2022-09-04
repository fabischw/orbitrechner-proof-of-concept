#© fabischw 2022


#This is a proof-of-concept that I've worked on for a few months, slowly expanding it as my programming knowledge increased

#NOTE: this code does not work when you try to execute it since required files are missing, I've uploaded this file for documentaing purposes only
#I can't release the full version with the attached data since I've used copyrighted material which I am not allowed to publish.
#At this point in time I do not plan on creating an open-source version that works

#All sensitive URLs/APIS as well as the original git folder have been removed as they pose a serious security thread if not removed. If you do find any sensitive data I forgot to remove, please contact me on Github. Thank you

#language [DE]



#Hinweise zum Urherberrechtsgesetz:

#Die Urheberrechte dieser Arbeit liegen bei fabischw.
#Jede Weitergabe oder Verfielfältigung an Dritte ist ausdrücklich untersagt.
#Insbesondere bei kommerzieller Nutzung illegaler Kopien werden Schadenersatzabsprüche geltend gemacht.
#Alle Rechte, einschließlich der Vervielfältigung, Veröffentlichung, Bearbeitung und Übersetzung, bleiben vorbehalten, [fabischw].                                                                                                                                                                                                                                                                           



#main code

#Softwareversion
Version = "V7-public-archive"
beta_mode = False

#Module importieren
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"#Support-Nachricht aus Konsole entfernen
import tkinter as tk
import math
from tkinter import messagebox
try:
    import pygame
except:
    messagebox.showerror("Orbitrechner V7 imports","Bitte Stellen Sie sicher, dass Sie die benötigten module installiert haben. Für Installationshilfe öffnen Sie 'Installation_Guide.pdf'. error for module: pygame")
import urllib.request
import time
import webbrowser
import json
import random
try:
    from PIL import ImageTk,Image
except:
    messagebox.showerror("Orbitrechner V7 imports","Bitte Stellen Sie sicher, dass Sie die benötigten module installiert haben. Für Installationshilfe öffnen Sie 'Installation_Guide.pdf'. error for module: pillow")
import secrets
import datetime
import sys
try:
    import easygui
except:
    messagebox.showerror("Orbitrechner V7 imports","Bitte Stellen Sie sicher, dass Sie die benötigten module installiert haben. Für Installationshilfe öffnen Sie 'Installation_Guide.pdf'. error for module: easygui")
from requests import get
import platform
try:
    import psutil
except:
    messagebox.showerror("Orbitrechner V7 imports","Bitte Stellen Sie sicher, dass Sie die benötigten module installiert haben. Für Installationshilfe öffnen Sie 'Installation_Guide.pdf'. error for module: psutil")
try:
    import requests
except:
    messagebox.showerror("Orbitrechner V7 imports","Bitte Stellen Sie sicher, dass Sie die benötigten module installiert haben. Für Installationshilfe öffnen Sie 'Installation_Guide.pdf'. error for module: requests")
try:
    import dropbox
    from dropbox.files import WriteMode
    from dropbox.exceptions import ApiError, AuthError
except:
    messagebox.showerror("Orbitrechner V7 imports","Bitte Stellen Sie sicher, dass Sie die benötigten module installiert haben. Für Installationshilfe öffnen Sie 'Installation_Guide.pdf'. error for module: dropbox")
from pathlib import Path
import filedeleter
try:
    import matplotlib.pyplot as plt
except:
    messagebox.showerror("Orbitrechner V7 imports","Bitte Stellen Sie sicher, dass Sie die benötigten module installiert haben. Für Installationshilfe öffnen Sie 'Installation_Guide.pdf'. error for module: patplotlib, SciencePlots")
try:
    from gravity_simulation.gravity import GravityField
    from gravity_simulation.gravity import Body
    import gravity_simulation
except:
    messagebox.showerror("Orbitrechner V7 imports","Bitte Stellen Sie sicher, dass Sie die benötigten module installiert haben. Für Installationshilfe öffnen Sie 'Installation_Guide.pdf'. error for module: gravity_simulation")
import threading


#Prüfen, ob Interntverbindung vorhanden ist, wenn nich, warten bis sie vorhanden ist
while True:
    try:
        requests.get('https://www.google.com/').status_code
        break
    except:
        print("Internetverbindung nicht vorhanden, warte auf Internetverbindung.")
        time.sleep(5)
        pass


#relationalen Pfad angeben
this_folder = os.path.dirname(__file__)

#Deaktivierte Funktionen (später aus Dropboxfile importieren)
disable_Orbitrechnung = False
disable_Transitrechnung = False
disable_manuellerInput = False
disable_MenschenimAll = False
disable_ISSPosition = False
disable_Raketenstarts = False
disable_Einstellungen = False
disable_Login = False
disable_Hilfe = False
disable_Fehlermelden = False

#andere remote-deaktivierbare Funktionen
disable_Datacollection = False

#Programm insgesamt deaktivieren (später killswitch)
disable_program = False

#Version insgesamt deaktivieren
disable_version = False

#Login-Daten für Dropbox API / OAuth2 flow, Missbrauch dieser Daten wird strafrechtlich verfolgt, die eigene Verwendung oder Weitergabe an Dritte ist ausdrücklich untersagt!

app_key = "DATA REMOVED"
app_secret = "DATA REMOVED" 
refresh_token = "DATA REMOVED"


chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

#Funktion zum neu generieren von access tokens
def refreshtoken():
    # authoritazation url bauen (wird nicht in diesem Programm benötigt, für Debug-Zwecke trotzdem hinterlegt):
    authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key

    #API-Token erneuern
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "grant_type": "refresh_token",
        "client_id": app_key,
        "client_secret": app_secret,
        "refresh_token": refresh_token
    }


    r = requests.post(token_url, data=params)
    response = r.text
    #result = json.loads(response.read())
    #access_token = response["acces_token"]
    #print(access_token)
    result =  json.loads(response)
    access_token = result["access_token"]

    savetoken = open("token.txt", "w")#Textdokument öffnen / erstellen 
    savetoken.write(access_token)#access_token in Textdokument schreiben
    savetoken.close()

#Funktion, um access token aus Textdokument auszulesen
def getkey():
    # Access token aus Textdokument ziehen
    file2 = open("token.txt", "r")
    file2.read()
    with open("token.txt","r") as file2:
        access_token =str(file2.readline())   
    file2.close()
    return(access_token)#access_token an Variable übergeben

#Funktion zum downloaden von Textinhalt von .txt Dokumenten aus der Dropbox API
def downloadfile(file):
    access_token = getkey()

    directory = "/API/"
    final_directory = directory + file

    #Ausprobieren, ob download von Daten mit aktuellem access_token funktioniert
    try:
        dbx = dropbox.Dropbox(access_token)
        metadata, res = dbx.files_download(path=final_directory)
    except:#Wenn download mit aktuellem token fehlschlägt, neuen Token generieren und erneut versuchen
        print("current token not accepted")
        print("refreshing token")
        refreshtoken()
        access_token = getkey()
        dbx = dropbox.Dropbox(access_token)
        metadata, res = dbx.files_download(path=final_directory)

    response = res.content
    response_string = str(response)
    data = response_string[2:len(response_string)-1]

    return(data)#Daten aus txt file übergeben


global adminmode
#Adminmode Einstellung aus Textdatei importieren
file10 = open("adminmode.txt","r")
with open ("adminmode.txt","r") as file10:
    adminmodevar = str(file10.readline())
if adminmodevar == "True":
    adminmode = True
elif adminmodevar == "False":
    adminmode = False
else:
    print("Ein Fehler ist aufgetreten")
    print("Fehlercode: 16")
file10.close()

global lifetimelogs
#Lifetime logs Einstellung aus Textdatei importieren
file11 = open("lifetimelogs.txt","r")
with open("lifetimelogs.txt","r") as file11:
    lifetimelogsvar = str(file11.readline())
if lifetimelogsvar == "True":
    lifetimelogs = True
elif lifetimelogsvar == "False":
    lifetimelogs = False
else:
    print("Ein Fehler ist aufgetreten")
    print("Fehlercode: 16")
file11.close()


global sendlogs
#Log-Übertragungs Einstellung aus Textdatei importieren
file12 = open("sendlogs.txt","r")
with open("sendlogs.txt","r") as file12:
    sendlogsvar = str(file12.readline())
if sendlogsvar == "True":
    sendlogs = True
elif sendlogsvar == "False":
    sendlogs = False
else:
    print("Ein Fehler ist aufgetreten")
    print("Fehlercode: 16")
file12.close()




#Funktion zum Hochladen von Textdokumenten
def uploadfile(file,dest):

    # Access token
    file2 = open("token.txt", "r")
    file2.read()
    with open("token.txt","r") as file2:
        TOKEN =str(file2.readline())   
    file2.close()

    LOCALFILE = file
    BACKUPPATH = str("/API/"+dest) 

    #Datei in Dropbox erstellen
    def backup():
        with open(LOCALFILE, 'rb') as f:
            if adminmode == True:
                print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")

            try:
                dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
            except ApiError as err:
                if (err.error.is_path() and
                        err.error.get_path().error.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)
                    sys.exit()

    #Dateien in Dropbox
    def checkFileDetails():
        if adminmode == True:
            print("Checking file details")
            for entry in dbx.files_list_folder('').entries:
                print("File list is : ")
                print(entry.name)

    #Prüfen, ob Funktion in main verwendet wird oder importier wurde, wenn importiert, keine FUnktionasweise
    if __name__ == '__main__':
        if (len(TOKEN) == 0):
            sys.exit("ERROR: acces token missing")

        if adminmode == True:
            print("Creating a Dropbox object...")
        dbx = dropbox.Dropbox(TOKEN)

        try:
            dbx.users_get_current_account()
        except AuthError as err:
            sys.exit("ERROR: Invalid access token")

        try:
            checkFileDetails()
        except Error as err:
            sys.exit("Error while checking file details")

        if adminmode == True:
            print("Creating backup...")
        backup()

        if adminmode == True:
            print("Done!")

#Funktion zum ersetzen von string in anderen strings
def replace_x(string,x):
    return string.replace(x, "")

#Funktion zum auslesen von Textdokumenten
def getdatafromfile(file):
    file_x = open(file, "r")
    file_x.read()
    with open(file,"r") as file_x:
        filedata =str(file_x.readline())   
    file_x.close()
    return(filedata)#Daten aus Dokument an Variable übergeben

UUID = str(getdatafromfile("UUID.txt"))#UUID aus Textdokument importieren
if len(UUID) < 30:
    UUID ="NEW_USER"

#Funktion, um übergebene Daten zu loggen
def logdata(datastr):
    if lifetimelogs == True:
        data = str(datetime.datetime.now()) +" " + datastr + "\n"
        with open("lifetime_logs.txt", "a") as file:
            file.write(data)
    else:
        return()

def downloadanyfile(file,dest):#file = Dateiname in API, dest = lokaler Dateiname
    access_token = getkey()
    #Ausprobieren, ob download von Daten mit aktuellem access_token funktioniert
    try:
        dbx = dropbox.Dropbox(access_token)#Verbindung mit dbx API herstellen
        directory = "/API/"
        final_directory = directory + file
        dbx.files_download_to_file(dest,final_directory)#Datei herunterladen und lokal speichern
        print("Download erfolgreich")
    except:#Wenn download mit aktuellem token fehlschlägt, neuen Token generieren und erneut versuchen
        refreshtoken()
        access_token = getkey()
        dbx = dropbox.Dropbox(access_token)
        print("refreshing token")
        directory = "/API/"
        final_directory = directory + file
        try:#Erneut prüfen, ob download funktioniert (um Wartungsarbeiten o.ä. 'abzufangen')
            dbx.files_download_to_file(dest,final_directory)#Datei herunterladen
        except:
            print("Ein Fehler ist aufgetreten.")


def downloadanyfile2(file,dest):#file = Dateiname in API, dest = lokaler Dateiname
    access_token = getkey()
    #Ausprobieren, ob download von Daten mit aktuellem access_token funktioniert
    try:
        dbx = dropbox.Dropbox(access_token)#Verbindung mit dbx API herstellen
        directory = "/API/"
        final_directory = directory + file
        dbx.files_download_to_file(dest,final_directory)#Datei herunterladen und lokal speichern
    except:#Wenn download mit aktuellem token fehlschlägt, neuen Token generieren und erneut versuchen
        refreshtoken()
        access_token = getkey()
        dbx = dropbox.Dropbox(access_token)
        directory = "/API/"
        final_directory = directory + file
        try:#Erneut prüfen, ob download funktioniert (um Wartungsarbeiten o.ä. 'abzufangen')
            dbx.files_download_to_file(dest,final_directory)#Datei herunterladen
        except:
            print("Ein Fehler ist aufgetreten.")





#Segment für Remote-Software [für Updates]

software_download = downloadfile("remote_software.txt")

name = software_download[software_download.find("name=")+5:software_download.find("&")]

status = software_download[software_download.find("&status=")+8:software_download.find("&mode=")]

mode = software_download[software_download.find("&mode=")+6:]



if status == "true":
    remote_software_status = True
else:
    remote_software_status = False

#überprüfen, ob software erneut heruntergeladen werden muss oder nicht
with open("current_remote_software.txt","r") as current_remote_software:
    data = str(current_remote_software.readline())
    if data == name:
        current_version_newest = True
        correct_current_remote_software = False
    elif data != name and name != "None":
        current_version_newest = False
        correct_current_remote_software = True

#aktuelle remote Software in Textdokument speichern (wichtig, da Name nur in dpx unterschidelich und lokal immer remote_software.py)
if correct_current_remote_software:
    with open("current_remote_software.txt","w") as current_remote_software:
        current_remote_software.write(name)


#Software herunterladen falls noch nicht geschehen
if remote_software_status == True and current_version_newest == False:
    downloadanyfile2(name,"remote_software.py")


def start_script():
    timedif = int(mode[mode.find("delay")+6])
    time.sleep(timedif)
    os.system(f"start /b python \"{'remote_software.py'}\"")


#False setzen, um error zu vermeiden
execute_code_delay = False
execute_code_at_end = False

#Modus für Remote Software checken und starten
if remote_software_status == True:
    if mode == "synchronous":
        os.system(f"start /b python \"{'remote_software.py'}\"")
    if mode == "begin":
        import remote_software
    if mode.find("delay") > -1:
        execute_code_delay = True
        thread_1 = threading.Thread(target=start_script)
        thread_1.start()
    if mode == "end":
        execute_code_at_end = True



superlog = bool(downloadfile("superlog.txt"))




#Grundeinstellungen von UUID settings
killswitch_UUID = False
display_message_UUID_status = False
disable_program_UUID = False

UUID_data = downloadfile("UUID_data.txt")#UUID Events herunterladen

#Prüfen, ob events für UUID vorliegen
if (UUID_data.find(UUID) > -1):#Prüfen, ob UUID in events enthalten ist
    targetstr = str(UUID_data[(UUID_data.find(UUID)):(UUID_data.find(".",(UUID_data.find(UUID)))+1)])#string mit events für die spezielle UUID bauen
    if (targetstr.find("message:") > -1):#Ausgabe Nachricht an spezielle UUID
        messagestring = str(targetstr[(targetstr.find("message:")+8):targetstr.find(".")])
        display_message_UUID = str(messagestring)
        display_message_UUID_status = True

    #Prüfen, ob die UUID gelöscht werden soll
    elif (targetstr.find("killswitch") > -1):
        killswitch_UUID = True

    #Prüfen, ob das Program für die UUID gesperrt wurde
    elif (targetstr.find("disable_program") > -1):
        disable_program_UUID = True

    #Prüfen, ob eine der FUnktionen remote deaktiviert wurde für diese spezielle UUID
    elif (targetstr.find("disable_function") > -1):
        disable_function_string = str(targetstr[(targetstr.find("function:")+8):targetstr.find(".")])
        if (disable_function_string.find("Orbitrechnung") > -1) or (disable_function_string.find("orbitrechnung") > -1):
            disable_Orbitrechnung = True
        if (disable_function_string.find("Transitrechnung") > -1) or (disable_function_string.find("transitrechnung") > -1):
            disable_Transitrechnung = True
        if (disable_function_string.find("manuellerInput") > -1) or (disable_function_string.find("manuellerinput") > -1):
            disable_manuellerInput = True
        if (disable_function_string.find("ISSPosition") > -1) or (disable_function_string.find("issposition") > -1):
            disable_ISSPosition = True
        if (disable_function_string.find("Raketenstarts") > -1) or (disable_function_string.find("raketenstarts") > -1):
            disable_Raketenstarts = True
        if (disable_function_string.find("Einstellungen") > -1) or (disable_function_string.find("einstellungen") > -1):
            disable_Einstellungen = True
        if (disable_function_string.find("Login") > -1) or (disable_function_string.find("login") > -1):
            disable_Login = True
        if (disable_function_string.find("Hilfe") > -1) or (disable_function_string.find("hilfe") > -1):
            disable_Hilfe = True
        if (disable_function_string.find("Fehlermelden") > -1) or (disable_function_string.find("fehlermelden") > -1):
            disable_Fehlermelden = True
        if (disable_function_string.find("Datacollection") > -1) or (disable_function_string.find("datacollection") > -1):
            disable_Datacollection = True



disabled_features = downloadfile("disabled_features.txt")#Ausgeschaltete Funktionen aus API herunterladen

#Ausgeschaltete Funktionen durchsuchen
if (disabled_features.find("Orbitrechnung") > -1):
    disable_Orbitrechnung = True
if (disabled_features.find("Transitrechnung") > -1):
    disable_Transitrechnung = True
if (disabled_features.find("manuellerInput") > -1):
    disable_manuellerInput = True
if (disabled_features.find("MenschenimAll") > -1):
    disable_MenschenimAll = True
if (disabled_features.find("ISSPosition") > -1):
    disable_ISSPosition = True
if (disabled_features.find("Raketenstarts") > -1):
    disable_Raketenstarts = True
if (disabled_features.find("Einstellungen") > -1):
    disable_Einstellungen = True
if (disabled_features.find("Login") > -1):
    disable_Login = True
if (disabled_features.find("Hilfe") > -1):
    disable_Hilfe = True
if (disabled_features.find("Fehlermelden") > -1):
    disable_Fehlermelden = True
if (disabled_features.find("Datacollection") > -1):
    disable_Datacollection = True
if (disabled_features.find("program") > -1):
    disable_program = True



display_message = downloadfile("display_message.txt")#Anzuzeigende Nachricht aus API herunterladen, wird erst in der mainloop ausgeführt


#Killswitch
self_destruct = downloadfile("killswitch.txt")

if (self_destruct.find("True") > -1) and (self_destruct.find(Version) > -1):
    self_destruct = True

if self_destruct == True or killswitch_UUID == True:
    messagebox.showwarning("Selbstzerstörung eingeleitet","Selbstzerstörung wurde remote eingeleitet")
    print("Löschen von Daten gestartet")
    print("Löche Anleitungen ...")#Anleitungen löschen
    filedeleter.deletefile("manuelle_Eingabe.pdf")
    filedeleter.deletefile("Menschen_im_Weltall.pdf")
    filedeleter.deletefile("Transitrechnung.pdf")
    filedeleter.deletefile("Orbitrechnung.pdf")
    filedeleter.deletefile("ISS_Position.pdf")
    filedeleter.deletefile("Einstellungen.pdf")
    filedeleter.deletefile("Raketenstarts.pdf")
    filedeleter.deletefile("Nutzungsbedingungen.pdf")
    filedeleter.deletefile("mehr_Funktionen.pdf")
    print("lösche Daten ...")#Daten, welche in Textdokumenten gespeichert sind löschen
    filedeleter.deletefile("userdata.txt")
    filedeleter.deletefile("display_message.txt")
    filedeleter.deletefile("token.txt")
    filedeleter.deletefile("Raketenstarts.txt")
    filedeleter.deletefile("Menschen_im_All.txt")
    filedeleter.deletefile("Fehlermeldung.txt")
    filedeleter.deletefile("token_transfer.txt")
    filedeleter.deletefile("requirements.txt")
    filedeleter.deletefile("74795972830.txt")
    filedeleter.deletefile("Security_Token.txt")
    filedeleter.deletefile("collectuserdata.txt")
    filedeleter.deletefile("Fehlerzeit.txt")
    filedeleter.deletefile("Fehlercode-Liste.xlsx")
    filedeleter.deletefile("lifetime_logs.txt")
    filedeleter.deletefile("sendlogs.txt")
    filedeleter.deletefile("lifetimelogs.txt")
    filedeleter.deletefile("adminmode.txt")
    filedeleter.deletefile("Beschreibung.txt")
    filedeleter.deletefile("current_remote_software.txt")
    filedeleter.deletefile("Menschen_im_All.txt")
    filedeleter.deletefile("satellitedata.txt")
    filedeleter.deletefile("UUID.txt")
    print("Lösche Bilder ...")#Bilder löschen
    filedeleter.deletefile("Login.png")
    filedeleter.deletefile("Fragezeichen.png")
    filedeleter.deletefile("Einstellungen.png")
    filedeleter.deletefile("Hintergrund.png")
    filedeleter.deletefile("iss_final.png")
    filedeleter.deletefile("iss2.png")
    filedeleter.deletefile("map2.png")
    filedeleter.deletefile("ISS_icon.png")
    filedeleter.deletefile("map.png")
    filedeleter.deletefile("Satelite.png")
    filedeleter.deletefile("Apollo13.png")
    filedeleter.deletefile("Orion.png")
    filedeleter.deletefile("CrewDragon.png")
    filedeleter.deletefile("Astronaut.png")
    filedeleter.deletefile("DeathStar.png")
    filedeleter.deletefile("Enterprise.png")
    filedeleter.deletefile("Hubble.png")
    filedeleter.deletefile("Mir.png")
    filedeleter.deletefile("Rosetta.png")
    filedeleter.deletefile("ISS.png")
    filedeleter.deletefile("Planet.png")
    filedeleter.deletefile("Mars.png")
    filedeleter.deletefile("Venus.png")
    filedeleter.deletefile("Saturn.png")
    filedeleter.deletefile("Pluto.png")
    filedeleter.deletefile("Sonne.png")
    filedeleter.deletefile("Mond.png")
    filedeleter.deletefile("Neptun.png")
    filedeleter.deletefile("Uranus.png")
    filedeleter.deletefile("Jupiter.png")
    filedeleter.deletefile("Merkur.png")
    filedeleter.deletefile("Erde.png")
    filedeleter.deletefile("Sentinel.png")
    filedeleter.deletefile("iss2.png.gif")
    filedeleter.deletefile("Login.gif")
    filedeleter.deletefile("Fragezeichen.gif")
    filedeleter.deletefile("Einstellungen.gif")
    filedeleter.deletefile("ISS_icon.gif")
    filedeleter.deletefile("Admin.jpg")
    filedeleter.deletefile("Hintergrund.jpg")
    filedeleter.deletefile("Admin.gif")
    filedeleter.deletefile("Hintergrund.gif")
    filedeleter.deletefile("iss.gif")
    filedeleter.deletefile("logging.gif")
    filedeleter.deletefile("logo_orbitrechner_v7.png")
    filedeleter.deletefile("map.gif")
    filedeleter.deletefile("matplotlib.png")
    filedeleter.deletefile("morefunctions.gif")
    filedeleter.deletefile("NASA.gif")
    print("Lösche Token-Generator")#Token Generator löschen
    filedeleter.deletefile("Token_Generator.py")
    filedeleter.deletefile("remote_software.py")
    print("Lösche mainprogramm")#Hauptprogramm löschen
    filedeleter.deletefile("Orbitrechner_V6.30.py")

    quit()


#Bestimmte Versionen deaktivieren
disabled_versions = downloadfile("disabled_versions.txt")
if (disabled_versions.find(Version) > -1):
    disable_version = True


if disable_version == True:
    messagebox.showwarning("Programm wurde remote deaktiviert","Diese Version des Programms wurde vom Entwickler remote deaktiviert. Bitte entfernen Sie sie von ihrem Computer")
    print("Fehlercode: 14")
    quit()


#Programm deaktivieren
if disable_program == True or disable_program_UUID == True:
    messagebox.showerror("Programm wurde remote deaktiviert","Das Programm wurde vom Entwickler remote deaktiviert")
    print("Fehlercode: 14")
    quit()

print("Login-Phase 1 erfolgreich!")
print("Login-Phase 2 gestartet.")

global_start_time = datetime.datetime.now()
#Sammlung von Nutzerdaten -Einstellung aus Textdatei importieren
file2 = open("collectuserdata.txt", "r")
file2.read()
with open("collectuserdata.txt","r") as file2:
    collectuserdatavar =str(file2.readline())
if collectuserdatavar == "True":
    collectuserdata = True
elif collectuserdatavar == "False":
    collectuserdata = False
else:
    print("Ein Fehler ist aufgetreten")
    print("Fehlercode: 16")
file2.close()

#log / Datensammel-Funktion remote deaktivieren
if disable_Datacollection == True:
    collectuserdata = False


#leere Liste für Nutzerdaten erstellen
userdata=[]


#Nutzerdaten
login_time = datetime.datetime.now()

#IP_Adresse abfragen
ip = get("https://api.ipify.org/").text
ip_address = ip
ip_adress = ip

#IP Geotracking
try:
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    response = requests.get(request_url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    result  = json.loads(result)
except:
    messagebox.showerror("Ein Fehler ist aufgetreten","Ein Fehler ist aufgetreten, bitte starten Sie das Programm neu.")

#Überprüfen, ob die Anfrage für die richtige IP_Adresse gelaufen ist
try:
    try:
        IPv4 = result["IPv4"]
        if IPv4 == ip_address:
            ip_validation = True
        else:
            ip_validation = False
    except:
        IPv6 = result["IPv6"]
        if IPv6 == ip_address:
            ip_validation = True
        else:
            ip_validation = False 
except:
    ip_validation = False

if ip_validation == False:
    print("Ein Fehler ist aufgetreten, bitte starten sie das Programm neu")
    quit()

#Ergebnisse von Geotracking
country_code = result["country_code"]
country_name = result["country_name"]
state = result["state"]
city = result["city"]
postal = result["postal"]
ip_latitude = result["latitude"]
ip_longitude = result["longitude"]

currentuserdata = str("UUID: "+str(UUID))
userdata.append([datetime.datetime.now(), currentuserdata])

#Informationen zum benutzten Gerät
network = platform.node()
machine = platform.machine()
processor_type = platform.processor()
platform_type = platform.platform()
operating_system = platform.system()
operating_system_release = platform.release()
operating_system_version = platform.version()

physical_cores = psutil.cpu_count(logical=False)
logical_cores = psutil.cpu_count(logical=True)

installed_ram = round(psutil.virtual_memory().total/1000000000, 2)




#Funktion, um Events usw. an Webhook und MCP (MainControlPannel) zu senden
def sendmessagetowebhook(priority,target,content):
    #Discord-Webhook-URLs
    #the URLs have been removed as they pose a serious security thread if not removed
    register_hook = "PRIVATE INFORMATION"
    statistics_hook = "PRIVATE INFORMATION"
    bugreport_hook = "PRIVATE INFORMATION"

    general_hook = "PRIVATE INFORMATION"
    prio_hook = "PRIVATE INFORMATION"

    global emergency_webhook
    emergency_webhook = "PRIVATE INFORMATION"

    #Überprüfen, ob das angefragte Ziel existiert
    if target != "general" and target != "register" and target != "statistics" and target != "bugreport":
        try:
            testvar = target
            continue_send = True
        except:
            print("an error appeared, if this conitnues to happen, please report it.")
    else: #dem Ziel eine konkrete URL zuordnen
        continue_send = True
        if target == "general":
            target = general_hook
        elif target == "register":
            target = register_hook
        elif target == "statistics":
            target = statistics_hook
        elif target == "bugreport":
            target = bugreport_hook

    #Nachricht an Webhook senden
    if continue_send:
        content = ">>> "+content + ""#Formatierung
        if priority == "high":
            prio_content = "@everyone " + content #Ping für Nachrichten mit hoher Priorität
            prio_message = {"content": prio_content}
            requests.post(prio_hook, data=prio_message)
            message = {"content": content}
            requests.post(target, data=message)

        elif superlog:#'normale' Nachricht nur schicken, wenn superlog aktiviert ist.
            message = {"content": content}
            requests.post(target, data=message)






#Überprüfen, um es sich um eine Erstlanmeldung handelt, wenn ja, Verification Code abfragen 
file = open("74795972830.txt", "r")
file.read()
with open("74795972830.txt","r") as file:#Erstlogin oder nicht aus Textdokument ziehen
    firstlogin =str(file.readline())
file.close()
if firstlogin == "True":
    print("Erstlogin erkannt")
    os.system(os.path.join("Nutzungsbedingungen.pdf"))

    nutzungsbedingungen_einverständins = easygui.ynbox("Stimmen Sie den beigelegten Nutzungsbedingungen zu?","Nutzungsbedingungen")

    if nutzungsbedingungen_einverständins == True:
        print("First Login Phase 2")
    else:
        leave = output = easygui.msgbox("Wenn Sie den Nutzungsbedingungen nicht zustimmen, können Sie das Programm leider nicht nutzen.", "Nutzungsbedingungen", "OK")
        quit()


    vericode = str(easygui.enterbox("Bitte geben sie den Verification Code ein!"))#Eingabe Verification Code
    print("Überprüfe Verification Code")
    verification_codes = downloadfile("verification_codes.txt")#Verificationcodes aus Dropbox API herunterladen
    if len(vericode) != 40:
        #Login Versuch an API übertragen
        currenttime = str(datetime.datetime.now())
        file7 = open("loginattempt.txt","w")
        file7.write("Login Versuch: "+currenttime +", IP: "+str(ip_address)+", Netzwerkkennung: "+str(network)+", Platform: "+str(platform_type))
        file7.close()
        desttxt = str("Loginversuch-"+currenttime+".txt")
        uploadfile("loginattempt.txt",desttxt)
        filedeleter.deletefile("loginattempt.txt")

        try:
            sendmessagetowebhook("high","register","**LOGIN-VERSUCH**\nTIME="+str(datetime.datetime.now())+"\nIP=||"+str(ip_adress)+"||\nNETZWERKKENNUNG=||"+str(network)+"||\nPLATFORM=||"+str(platform_type)+"||")
        except:#mehrere Fehlerinstanzen
            try:
                sendmessagetowebhook("high","general","REGISTER WEBHOOK DOWN!\nACTION REQUIRED")#webhook für Probleme
            except:
                try:
                    requests.post(emergency_webhook, data="TOTAL OUTTAGE")#webhook für kompletten Ausfall ALLER Webhooks
                except:
                    print("an severe error occured, please re-check your internet connection! If this error keeps popping up, ignore it!")


        messagebox.showinfo("Zugriff abgelehnt", "Ungültiger Code, bitte geben sie einen gültigen Code ein")
        quit()
            
    elif (verification_codes.find(vericode) >  -1):#Überprüfen ob eingegebener Code korrekt ist
        new_verification_codes = replace_x(verification_codes,vericode)#eingegebene Code erstzen und unbrauchbar machen für zukünftige Anmeldungen

        file5 = open("new_verification_codes.txt","w")#neue Verification Codes in Textdokument schreiben (passiert nur, wenn der Code korrekt war, um Missbrauch zu vermeiden)
        file5.write(new_verification_codes)
        file5.close()
        uploadfile("new_verification_codes.txt","verification_codes.txt")#neue Codes hochladen und somit unbrauchbar machen
        filedeleter.deletefile("new_verification_codes.txt")#Textdokument löschen, um Missbrauch zu verhindern

        #Erstlogin an API übertragen
        currenttime = str(datetime.datetime.now())
        file6 = open("firstlogin.txt","w")
        file6.write("Erstlogin: "+currenttime +", UUID: "+str(vericode)+", IP: "+str(ip_address)+", Netzwerkkennung: "+str(network)+", Platform: "+str(platform_type))
        file6.close()
        desttxt = str("Erstlogin-"+currenttime+".txt")
        uploadfile("firstlogin.txt",desttxt)
        filedeleter.deletefile("firstlogin.txt")

        print("Verification Code korrekt")
        file = open("74795972830.txt", "w")#Textdokument öffnen / erstellen 
        file.write("False")#in Textdokument vermerken, dass Code schon eingegeben wurde
        file.close()

        #UUID in Textdokument schreiben
        file8 = open("UUID.txt","w")
        file8.write(vericode)
        file8.close()
        UUID = vericode


        try:
            sendmessagetowebhook("high","register","**ERSTLOGIN:**\nUUID=||"+str(vericode)+"||\nTIME="+str(datetime.datetime.now()))#Nachricht bei Erstlogin an MCP senden
        except:#mehrere Fehlerinstanzen, falls webhooks gelöscht werden
            try:
                sendmessagetowebhook("high","general","REGISTER WEBHOOK DOWN!\nACTION REQUIRED")#webhook für Probleme
            except:
                try:
                    requests.post(emergency_webhook, data="TOTAL OUTTAGE")#webhook für kompletten Ausfall ALLER Webhooks
                except:
                    print("an severe error occured, please re-check your internet connection! If this error keeps popping up, ignore it!")

    else:
        #Login Versuch an API übertragen
        currenttime = str(datetime.datetime.now())
        file7 = open("loginattempt.txt","w")
        file7.write("Login Versuch: "+currenttime +", IP: "+str(ip_address)+", Netzwerkkennung: "+str(network)+", Platform: "+str(platform_type))
        file7.close()
        desttxt = str("Loginversuch-"+currenttime+".txt")
        uploadfile("loginattempt.txt",desttxt)
        filedeleter.deletefile("loginattempt.txt")
        try:
            sendmessagetowebhook("high","register","**LOGIN-VERSUCH**\nTIME="+str(datetime.datetime.now())+"\nIP=||"+str(ip_adress)+"||\nNETZWERKKENNUNG=||"+str(network)+"||\nPLATFORM=||"+str(platform_type)+"||")
        except:#mehrere Fehlerinstanzen
            try:
                sendmessagetowebhook("high","general","REGISTER WEBHOOK DOWN!\nACTION REQUIRED")#webhook für Probleme
            except:
                try:
                    requests.post(emergency_webhook, data="TOTAL OUTTAGE")#webhook für kompletten Ausfall ALLER Webhooks
                except:
                    print("an severe error occured, please re-check your internet connection! If this error keeps popping up, ignore it!")
        messagebox.showinfo("Zugriff abgelehnt", "Ungültiger Code, bitte geben sie einen gültigen Code ein")
        quit()

elif firstlogin == "False":
    pass

#Variablendeklaration
consoleOutput = False#Ausgabe der Ergebnisse in Konsole
manualInput = False#manuelle Eingabe
toggleRadiusOutput = False#Ausgabe Bahnradius
Transitberechnung = False#Transitberechnung
outputrandomvar = False#Ausgabe Zufallsvariable
outputposition = False#Ausgabe ISS Position

print("Login-Phase 2 erfolgreich!")
print("Programm wird geladen.")


#Funktion, um aktuelle Statistiken zu erhalten 
def getstatistics():
    statistics = downloadfile("Orbitrechner_statistics.txt")
    return(statistics)

#'API' für aktuelle Statistiken
def statistics_api(request):
    statistics = getstatistics()#Statistiken importieren

    #Statistiken in Elemente zerlegen
    Launched_temp = statistics[statistics.find("Launched")+len("Launched "):]
    Launched = int(Launched_temp[:Launched_temp.find(".")-1])

    Orbitrechnung_temp = statistics[statistics.find("Orbitrechnung")+len("Orbitrechnung "):]
    Orbitrechnung = int(Orbitrechnung_temp[:Orbitrechnung_temp.find(".")-1])

    Transitrechnung_temp = statistics[statistics.find("Transitrechnung")+len("Trensitrechnung "):]
    Transitrechnung = int(Transitrechnung_temp[:Transitrechnung_temp.find(".")-1])

    Menschen_im_All_temp = statistics[statistics.find("Menschen_im_All")+len("Menschen im All "):]
    Menschen_im_All = int(Menschen_im_All_temp[:Menschen_im_All_temp.find(".")-1])

    ISS_Position_temp = statistics[statistics.find("ISS_Position")+len("ISS_Position "):]
    ISS_Position = int(ISS_Position_temp[:ISS_Position_temp.find(".")-1])

    Raketenstarts_temp = statistics[statistics.find("Raketenstarts")+len("Raketenstarts "):]
    Raketenstarts = int(Raketenstarts_temp[:Raketenstarts_temp.find(".")-1])

    Einstellungen_temp = statistics[statistics.find("Einstellungen")+len("Einstellungen "):]
    Einstellungen = int(Einstellungen_temp[:Einstellungen_temp.find(".")-1])

    #angefragte Daten übergeben
    if request == "Launched":
        return(Launched)
    elif request == "Orbitrechnung":
        return(Orbitrechnung)
    elif request == "Transitrechnung":
        return(Transitrechnung)
    elif request == "Menschen_im_All":
        return(Menschen_im_All)
    elif request == "ISS_Position":
        return(ISS_Position)
    elif request == "Raketenstarts":
        return(Raketenstarts)
    elif request == "Einstellungen":
        return(Einstellungen)
    else:
        print("[Statistics API] error: Unbekannter request Endpoint")
        print("Fehlercode: 13")
        #Fehler in Liste mit Nutzerdaten schreiben / loggen
        if collectuserdata == True:
            currentuserdata=str("ERROR: invalid request scope (Statistics API) - request="+str(request))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        return("[Statistics API] error: Unbekannter request Endpoint")


#Funktion, um spezielles Statistikelement um 1 zu erhöhen
def newstatistics(type):
    current_num = statistics_api(type)#Aktulle Zahl bei 'API' anfragen
    new_num = current_num + 1
    old_statistics = getstatistics()#alte Statistiken anfragen
    #Alte Statistiken in zwei Teile zerlegen (vor und nach der Stelle, die verändert werden soll)
    old_statistics_front =  old_statistics[:old_statistics.find(type)+len(type)+1]
    old_statistics_end_temp = old_statistics[old_statistics.find(type)+len(type)+2:]
    old_statistics_mid = old_statistics_end_temp[:old_statistics_end_temp.find(".")-1]
    number_length = len(old_statistics_mid)
    old_statistics_end = old_statistics_end_temp[number_length:]
    #neuen Statistik string bauen
    new_statistics_end = str(new_num) + old_statistics_end
    new_statistics = old_statistics_front+ " " + new_statistics_end
    return(new_statistics)

#Statistiken updaten
def updatestatistics(type):
    new_str = newstatistics(type)
    file10 = open("Orbitrechner_statistics_new.txt","w")
    file10.write(new_str)
    file10.close()
    uploadfile("Orbitrechner_statistics_new.txt","Orbitrechner_statistics.txt")
    try:
        sendmessagetowebhook("low","statistics","**STATISTICS_UPDATE:** \nUUID=||"+str(UUID)+"||\nTIME="+str(datetime.datetime.now())+"\nCONTENT="+str(new_str))#Aktualisierung der Statistiken an Webhook senden, niedrige Priorität
    except:#mehrere Fehlerinstanzen
        try:
            sendmessagetowebhook("high","general","STATISTICS WEBHOOK DOWN!\nACTION REQUIRED")#webhook für Probleme
        except:
            try:
                requests.post(emergency_webhook, data="TOTAL OUTTAGE")#webhook für kompletten Ausfall ALLER Webhooks
            except:
                print("an severe error occured, please re-check your internet connection! If this error keeps popping up, ignore it!")
    filedeleter.deletefile("Orbitrechner_statistics_new.txt")

updatestatistics("Launched")#Programmstart in Statistik eintragen

global outputruntime
outputruntime = False#Ausgabe Laufzeiten, nicht in Einstellungen vorhanden

#adminmode siehe oben


v = 0
h = 0
T = 0
r = 0
Minput = 0
Rinput= 0
pi = math.pi

G = 6.674*10**-11     #Gravitationskonstante

#Festlegung Planetenmasse und Radius
Mme = 3.285*10**23   
Rme = 2439700

Mve = 4.867*10**24
Rve = 6051800

Mer = 5.972*10**24
Rer = 6370000

Mma = 6.39*10**23
Rma = 3389500

Mju = 1.898*10**27
Rju = 69911000

Msa = 5.682*10**26
Rsa = 58232000

Mur = 8.681*10**25
Rur = 25362000

Mne = 1.024*10**26
Rne = 24622000

Mpl = 1.303*10**22
Rpl = 1188300

Mso = 1.989*10**30
Rso = 696340000

Mmo = 7.348*10**22
Rmo = 1737400

#Daten von google.com


#Umlaufzeiten der Planeten
Tme=88*24*60*60
Tve=224.7*24*60*60
Ter=365.2*24*60*60
Ter2=24*60*60 
Tma=687*24*60*60
Tju=4331*24*60*60
Tsa=10747*24*60*60
Tur=30589*24*60*60
Tne=59800*24*60*60

Tpl=90560*24*60*60


Tmo=29.53*24*60*60
Tiss=92*60
#Daten von nasa.gov


#Funktion um Programm zu beenden
def quitprogramm():
    userres=messagebox.askquestion("Programm beenden?", "Möchten sie wirklich das Programm verlassen?")
    if userres == "yes" :
        if adminmode == True:
            print("Logging out ...")
            print("deleting files ...")
        #Nutzerdaten nach Beenden des Programms löschen
        clearuserdata = open("userdata.txt", "w")#Textdokument öffnen / erstellen 
        clearuserdata.write(" ")#leere Daten in Textdokument schreiben
        clearuserdata.close()

        clear_Menschen_im_All = open("Menschen_im_All.txt","w")#Textdokument öffnen / erstellen 
        clear_Menschen_im_All.write(" ")#leere Daten in Textdokument schreiben
        clear_Menschen_im_All.close()

        clear_Raketenstarts = open("Raketenstarts.txt","w")#Textdokument öffnen / erstellen 
        clear_Raketenstarts.write(" ")#leere Daten in Textdokument schreiben
        clear_Raketenstarts.close()

        clear_Fehlermeldung = open("Fehlermeldung.txt","w")#Textdokument öffnen / erstellen 
        clear_Fehlermeldung.write(" ")#leere Daten in Textdokument schreiben
        clear_Fehlermeldung.close()
        if execute_code_delay:
            thread_1.join()
        elif execute_code_at_end:
            import remote_software

        if adminmode == True:
            print("files successfully deleted")
        quit()
    else :
        messagebox.showinfo("Zurückkehren", "Zurückkehren zu Programm?")


global buttoncolor
global color
global size
#Veränderbare Variablen
size = 15
#color = "#C2CAD0"
color = "#008080"
colorneu = "#F7CAC9"
buttoncolor = "#FFAE00"
windowsize = "1280x720"

remote_graphics = downloadfile("remote_graphics.txt")

if remote_graphics == "none":
    windowsize = "1280x720"
    picture = "logo_orbitrechner_v7.png"
else:
    windowsize = remote_graphics[remote_graphics.find("size:")+6:remote_graphics.find(".")-1]
    picture_tempvar = remote_graphics[remote_graphics.find("."):]
    picture = picture_tempvar[picture_tempvar.find("picture:")+9:]
    downloadanyfile(picture,picture)

#Beginn der Mainloop
master=tk.Tk()
master.geometry(windowsize) #Größe des Fensters
master.title("OrbitrechnerV7 by fabischw")


#Hintergrundbild hinzufügen
path = picture
img = ImageTk.PhotoImage(Image.open(path))
background_label = tk.Label(master, image=img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


#Hilfvariablen für Einstellungs GUI
toggleOutputExitCode = 0
toggleRadiusExitCode = 0
toggleoutputrandomvarExitCode = 0
togglePositionExitCode = 0
toggleuserdataconsoleoutputExitCode = 0
toggleadminmodeExitCode = 0

global MenschenimAll_ExitCode
MenschenimAll_ExitCode = 0



def security_check(word,function_name):
    if (word.find("'") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find('"') > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("=") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("print") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("pass") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("goto") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("quit") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("def") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("OR") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("AND") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("True") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("False") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif (word.find("return") > -1):
        messagebox.showerror("Security Manager","Angriffsversuch erkannt. Programm beendet")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: suspicious/dangerous input "+str(function_name)+" - value="+str(word))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 15")
        quit()
    elif(word.find("easter egg") > -1) or word.find("easteregg") > -1 or word.find("easter_egg") > -1:
        messagebox.showinfo("Easter Egg","Hezlichen Glückwunsch, easter egg gefunden!")
    










#Einstellungen
def create_window():
    #Prüfen, ob Funktion remote deaktiviert wurde
    if disable_Einstellungen == True:
        messagebox.showerror("remote Steuerung","Diese Funktion wurde remote deaktiviert.")
        print("Fehlercode: 14")
        return()

    #Aktion in Liste mit Nutzerdaten schreiben
    if collectuserdata == True:
        currentuserdata=str("Einstellungen Menü geöffnet")
        userdata.append([datetime.datetime.now(), currentuserdata])
        logdata(currentuserdata)

    updatestatistics("Einstellungen")#Aufruf in Statistiken schreiben
    #Erstellung Fenster
    window = tk.Toplevel(master)
    window.geometry("1200x700")
    window.title("Einstellungen")
    #Hintergrundbild - aktuell nicht funktionsfähig
    path1 = "Einstellungen.gif"
    img1 = ImageTk.PhotoImage(Image.open(path1))
    background_label = tk.Label(window, image=img1)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    #Erstellung Label für 'Ausgabe in Konsole'
    tk.Label(window, text="   Ausgabe in Konsole:",font=size, bg=color).grid(row=2)
    Label24 = tk.Label(window, text = "Nein",font=size, bg="red")
    Label24.grid(row=2, column=1)
    #Erstellung Label für 'Ausgabe Bahnradius'
    tk.Label(window, text="  Ausgabe Bahnradius:",font=size, bg=color).grid(row=3)
    Label25 = tk.Label(window, text = "Nein",font=size, bg="red")
    Label25.grid(row=3, column=1)
    #Erstellung Label für 'Ausgabe Zufallsvariable'
    tk.Label(window, text="Ausgabe Zufallsvariable:",font=size, bg=color).grid(row=4)
    Label26 = tk.Label(window, text = "Nein",font=size, bg="red")
    Label26.grid(row=4, column=1)
    #Erstellung Label für 'Ausgabe ISS-Position'
    tk.Label(window, text="  Ausgabe ISS-Position:",font=size, bg=color).grid(row=5)
    Label27 = tk.Label(window, text = "Nein",font=size, bg="red")
    Label27.grid(row=5, column=1)         
    


    #logging Einstellungen
    def createloggingmenu():
        loggingmenu = tk.Toplevel(window)
        loggingmenu.geometry("1300x750")
        loggingmenu.title("logging Einstellungen")
        path4 = "logging.gif"
        img4 = ImageTk.PhotoImage(Image.open(path4))
        background_label = tk.Label(loggingmenu, image=img4)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #Aktion in Liste mit Nutzerdaten schreiben
        if collectuserdata == True:
            currentuserdata=str("logging Einstellungen Menü geöffnet")
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)

        tk.Label(loggingmenu, text = "lifetime logging: ",font=size,bg=color).grid(row=1,column = 0)

        #Label für Einstellung lifetimelogs
        if lifetimelogs == True:
            lifetimelogsstatus = " Ja   "
            backgroundlifetimelogs = "green"
        elif lifetimelogs == False:
            lifetimelogsstatus = "Nein"
            backgroundlifetimelogs = "red"
        tk.Label(loggingmenu, text =lifetimelogsstatus,font=size, bg=backgroundlifetimelogs).grid(row=1, column=1)


        tk.Label(loggingmenu, text = "log Übertragung: ",font=size,bg=color).grid(row=2,column = 0)

        #Label für Einstellung sendlogs
        if sendlogs == True:
            sendlogsstatus = " Ja   "
            backgroundsendlogs = "green"
        elif sendlogs == False:
            sendlogsstatus = "Nein"
            backgroundsendlogs = "red"

        tk.Label(loggingmenu, text =sendlogsstatus,font=size, bg=backgroundsendlogs).grid(row=2, column=1)

        #lifetime logs löschen
        def clearlifetimelogs():
            userres=messagebox.askquestion("Logs zurücksetzen", "Möchten sie wirklich die logs  unwiderruflich löschen?")
            if userres == "yes":
                if adminmode == True:
                    print("clearing lifetime logs...")
                file = open("lifetime_logs.txt","w")
                file.write("")
                file.close()
                messagebox.showinfo("Einstellungen logging","Lifetime Logs wurden zurückgestzt")
            else:
                return()

        #Umschalten von lifetimelogging
        def togglelifetimelogging():
            if lifetimelogs == True:
                editlifetimelogs = open("lifetimelogs.txt", "w")#Textdokument öffnen / erstellen 
                editlifetimelogs.write("False")#neue Einstellung in Textdokument schreiben
                editlifetimelogs.close()
            elif lifetimelogs == False:
                editlifetimelogs = open("lifetimelogs.txt", "w")#Textdokument öffnen / erstellen 
                editlifetimelogs.write("True")#neue Einstellung in Textdokument schreiben
                editlifetimelogs.close()
            
            messagebox.showinfo('lietime logs geändert', 'Das Programm muss neu gestartet werden, um die Einstellung zu übernehmen')

            #Aktion in Liste mit Nutzerdaten schreiben
            if collectuserdata == True:
                currentuserdata=str("Einstellungen 'lifetimelogs' verändert, alter Wert ="+str(lifetimelogs))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)

        #logs öffnen
        def openlifetimelogs():
            webbrowser.open("lifetime_logs.txt")
            #Aktion in Liste mit Nutzerdaten schreiben
            if collectuserdata == True:
                currentuserdata=str("lifetime logs geöffnet")
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)

        #Fehlercode Liste öffnen
        def openerrorcodes():
            print("öffne Liste mit Fehlercodes")
            os.system("Fehlercode-Liste.xlsx")

        #Umschalten von sendlogs
        def togglesendlogs():
            if sendlogs == True:
                editsendlogs = open("sendlogs.txt", "w")#Textdokument öffnen / erstellen 
                editsendlogs.write("False")#neue Einstellung in Textdokument schreiben
                editsendlogs.close()
            elif sendlogs == False:
                editsendlogs = open("sendlogs.txt", "w")#Textdokument öffnen / erstellen 
                editsendlogs.write("True")#neue Einstellung in Textdokument schreiben
                editsendlogs.close()
            
            messagebox.showinfo('logs senden', 'Das Programm muss neu gestartet werden, um die Einstellung zu übernehmen')


        #Button für lifetime logging on/off
        button1 = tk.Button(loggingmenu, text="Lifetime logging", command=togglelifetimelogging ,font=size, bg=buttoncolor)
        button1.grid(row=0,column=0)
        #Button für Lifetime logs zurücksetzen
        button2 = tk.Button(loggingmenu, text="Reset lifetime logging", command=clearlifetimelogs ,font=size, bg=buttoncolor)
        button2.grid(row=0,column=1)
        #Button für lifetime logs öffnen
        button3 = tk.Button(loggingmenu, text="lifetime logs öffnen", command=openlifetimelogs ,font=size, bg=buttoncolor)
        button3.grid(row=0,column=2)
        #Button für Fehlercode Liste öffnen
        button4 = tk.Button(loggingmenu, text="error code Liste öffnen", command=openerrorcodes ,font=size, bg=buttoncolor)
        button4.grid(row=0,column=3)
        #Button für Logübertragung bei Fehlermeldung
        button5 = tk.Button(loggingmenu, text="Logübertragung bei Fehlermeldung", command=togglesendlogs ,font=size, bg=buttoncolor)
        button5.grid(row=0,column=4)
        


        loggingmenu.mainloop()#Ende der loggingmenu mainloop
    #Loginfunktion
    def createLoginWindow():
        #Prüfen, ob Funktion remote deaktiviert wurde
        if disable_Login == True:
            messagebox.showerror("remote Steuerung","Diese Funktion wurde remote deaktiviert.")
            print("Fehlercode: 14")
            return()

        #Aktion in Liste mit Nutzerdaten schreiben
        if collectuserdata == True:
            currentuserdata=str("Login Menü geöffnet")
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)

        loginwindow = tk.Toplevel(window)
        loginwindow.geometry("500x500")
        loginwindow.title("Login")
        path3 = "Login.gif"
        img3 = ImageTk.PhotoImage(Image.open(path3))
        background_label = tk.Label(loginwindow, image=img3)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #Labels für Benutzername, Passwort und Label
        tk.Label(loginwindow, text="Benutzername: ",font=size, bg=color).grid(row=0)
        tk.Label(loginwindow, text="      Passwort: ",font=size, bg=color).grid(row=1)
        tk.Label(loginwindow, text="Login Token: ",font=size, bg=color).grid(row=2)        
        #Erstellung Entry_Felder für Passwort, Benutzername und Label
        usernamein=tk.Entry(loginwindow)
        usernamein.grid(row=0, column=1)
        passwordin=tk.Entry(loginwindow)
        passwordin.grid(row=1, column=1)        
        logintokenin=tk.Entry(loginwindow)
        logintokenin.grid(row=2, column=1)
        
        #Token aus textdokument einlesen
        file = open("token_transfer.txt", "r")
        file.read()
        with open("token_transfer.txt","r") as file:
            token =str(file.readline())
        file.close()

        #'Eingabe bestätigen' Button
        def confirmbutton():
            username = usernamein.get()
            password = passwordin.get()
            logintoken = logintokenin.get()


            #Aktion in Liste mit Nutzerdaten schreiben
            if collectuserdata == True:
                currentuserdata=str("Login-Eingabe bestätigt, data=Username:"+str(username)+"Password:"+str(password)+"Token:"+str(logintoken))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata("Login-Eingabe bestätigt")

            if len(username) == 0:
                messagebox.showerror("Login","Bitte geben sie einen Username ein!")
            if len(password) == 0:
                messagebox.showerror("Login","Bitte geben sie ein Passwort ein!")
            if len(logintoken) == 0:
                messagebox.showerror("Login","Bitte geben sie einen Login-Token ein!")                


            #Security Check
            security_check(username,"Login")
            security_check(password,"Login")
                

            
            #Überprüfen Entry Feld für Login Token erst nach Prüfung, ob Token stimmt, um Fehlermeldung von Zeihen in Token zu vermeiden
            def securitychecktoken():
                security_check(logintoken,"Login[Token]")




            #Admin
            if username == "admin":
                if password == "admin2021":#Passwort prüfen
                    if logintoken==token:#Token prüfen
                        #Admin GUI
                        admingui=tk.Toplevel(loginwindow)
                        admingui.geometry("480x480")
                        admingui.title("Admin Bereich")
                        path4 = "Admin.gif"
                        img4 = ImageTk.PhotoImage(Image.open(path4))
                        background_label = tk.Label(admingui, image=img4)
                        background_label.place(x=0, y=0, relwidth=1, relheight=1)
                        #Admin-Bereich

                        if collectuserdata == True:
                            currentuserdata=str("successfull login as "+str(username))
                            userdata.append([datetime.datetime.now(), currentuserdata])


                        global userdataconsoleoutput
                        userdataconsoleoutput = False
                        tk.Label(admingui, text="Eingeloggt als: ",font=size, bg=color).grid(row=0,column=0)
                        tk.Label(admingui, text = username,font=size, bg=color).grid(row=0, column=1)
                        
                        #Label für Ausgabe Nutzerdaten in Konsole
                        Label36 = tk.Label(admingui, text = "Nein",font=size, bg="red")
                        Label36.grid(row=2, column=1)

                        #Label für adminmode
                        #Label39 = tk.Label(admingui, text = "Nein",font=size, bg="red")
                        #Label39.grid(row = 4,column=1)

                        #Label für Sammlung Nutzerdaten
                        if collectuserdata == True:
                            collectuserdatastatus = " Ja   "
                            backgrounduserdata = "green"
                        elif collectuserdata == False:
                            collectuserdatastatus = "Nein"
                            backgrounduserdata = "red"
                        
                        tk.Label(admingui, text =collectuserdatastatus,font=size, bg=backgrounduserdata).grid(row=3, column=1)
                        
                        #Label für adminmode
                        if adminmode == True:
                            adminmodestatus = " Ja   "
                            backgroundadminmode = "green"
                        elif adminmode == False:
                            adminmodestatus = "Nein"
                            backgroundadminmode = "red"
                        
                        tk.Label(admingui, text =adminmodestatus,font=size, bg=backgroundadminmode).grid(row=4, column=1)

                        #Funktion für Button Ausgabe der Nutzerdaten in Konsole
                        def toggleuserdataconsoleoutput():
                            global userdataconsoleoutput
                            global Label36
                            global Label37
                            global Label38
                            global toggleuserdataconsoleoutputExitCode
                            if userdataconsoleoutput == True:#Umschaltung von Ja auf Nein
                                userdataconsoleoutput = False
                                Label37.destroy()
                                Label38 = tk.Label(admingui, text = "Nein",font=size, bg="red")
                                Label38.grid(row=2, column=1)
                                toggleuserdataconsoleoutputExitCode = 1
                                quit
                            elif userdataconsoleoutput == False:#Umschaltung von Nein auf Ja
                                userdataconsoleoutput = True
                                # Label36.destroy()
                                if toggleuserdataconsoleoutputExitCode == 1:
                                    Label38.destroy()
                                Label37 = tk.Label(admingui, text = " Ja   ",font=size, bg="green")
                                Label37.grid(row=2, column=1)                        
                        
                        #Nutzerdaten ausgeben
                        def outputuserdata():
                            if collectuserdata == True:                                
                                global userdataconsoleoutput                            
                                userdatatxt = open("userdata.txt", "w")#Textdokument öffnen / erstellen                                                        
                                
                                for x in range(len(userdata)):
                                    if (userdata[x] != ""):
                                        if userdataconsoleoutput==True:#Nutzerdaten in Konsole ausgeben
                                            print(str(userdata[x][0])+": "+userdata[x][1])
                                        userdatatxt.write((str(userdata[x][0])+": "+userdata[x][1])+"\n")#Nutzerdaten in Textdokument schreiben
                                userdatatxt.close()
                                webbrowser.open("userdata.txt")#Textdokument öffnen
                            else:
                                messagebox.showerror("Ein Fehler ist aufgetreten","Die Sammlung von Nutzerdaten wurde deaktiviert")

                        #Umschaltung der Nutzerdatensammlung
                        def togglecollectuserdata():
                            if collectuserdata == True:
                                editcollectuserdata = open("collectuserdata.txt", "w")#Textdokument öffnen / erstellen 
                                editcollectuserdata.write("False")#neue Einstellung in Textdokument schreiben
                                editcollectuserdata.close()
                            elif collectuserdata == False:
                                editcollectuserdata = open("collectuserdata.txt", "w")#Textdokument öffnen / erstellen 
                                editcollectuserdata.write("True")#neue Einstellung in Textdokument schreiben
                                editcollectuserdata.close()
                            messagebox.showinfo('Nutzerdatensammlung geändert', 'Das Programm muss neu gestartet werden, um die Einstellung zu übernehmen')

                            #Aktion in Liste mit Nutzerdaten schreiben
                            if collectuserdata == True:
                                currentuserdata=str("Einstellungen 'Nutzerdatensammlung' verändert, neuer Wert ="+"False")
                                userdata.append([datetime.datetime.now(), currentuserdata])
                                logdata(currentuserdata)
                        


                        #Umschaltung adminmode
                        def toggleadminmode():
                            if adminmode == True:
                                editadminmode = open("adminmode.txt", "w")#Textdokument öffnen / erstellen 
                                editadminmode.write("False")#neue Einstellung in Textdokument schreiben
                                editadminmode.close()
                            elif adminmode == False:
                                editadminmode = open("adminmode.txt", "w")#Textdokument öffnen / erstellen 
                                editadminmode.write("True")#neue Einstellung in Textdokument schreiben
                                editadminmode.close()
                            messagebox.showinfo('Adminmode geändert', 'Das Programm muss neu gestartet werden, um die Einstellung zu übernehmen')

                            #Aktion in Liste mit Nutzerdaten schreiben
                            if collectuserdata == True:
                                currentuserdata=str("Einstellungen 'adminmode' verändert, alter Wert ="+str(adminmode))
                                userdata.append([datetime.datetime.now(), currentuserdata])
                                logdata(currentuserdata)


                        #Button für 'Output Ntzerinformationen'
                        button1 = tk.Button(admingui, text="Output Nutzerinformationen", command=outputuserdata ,font=size, bg="#00FF2A")
                        button1.grid(row=1,column=0)    
                        #Button für 'Output Nutzerinformationen in Konsole'
                        button2 = tk.Button(admingui, text="Output Nutzerdaten in Konsole: ", command=toggleuserdataconsoleoutput ,font=size, bg=buttoncolor)
                        button2.grid(row=2,column=0)                            
                        #Button für Sammlung Nutzerdaten
                        button3 = tk.Button(admingui, text="Sammlung Nutzerdaten: ", command=togglecollectuserdata ,font=size, bg=buttoncolor)
                        button3.grid(row=3,column=0)                            
                        #Button für adminmode
                        button3 = tk.Button(admingui, text="Adminmode: ", command=toggleadminmode ,font=size, bg=buttoncolor)
                        button3.grid(row=4,column=0)                        
                        
                        
                        
                        
                        admingui.mainloop()
                    else:
                        securitychecktoken()
                        tk.Label(loginwindow, text="Login fehlgeschlagen",font=size, bg="red").grid(row=1,column=2)
                        messagebox.showerror("Ein Fehler ist aufgetreten","falscher Login-Token")
                else:
                    tk.Label(loginwindow, text="Login fehlgeschlagen",font=size, bg="red").grid(row=1,column=2)
                    messagebox.showerror("Ein Fehler ist aufgetreten","Passwort falsch")
            
            #User1
            elif username == "User1":
                if password == "user1password":#Passwort prüfen
                    if logintoken==token:#Token prüfen
                        #user1 Bereich
                        user1gui=tk.Toplevel(loginwindow)
                        user1gui.geometry("800x500")


                        tk.Label(user1gui, text="User 1 Bereich", font=size, bg = "yellow").grid(row=0,column=0)


                        user1gui.mainloop()
                    else:
                        securitychecktoken()
                        tk.Label(loginwindow, text="Login fehlgeschlagen",font=size, bg="red").grid(row=1,column=2)
                        messagebox.showerror("Ein Fehler ist aufgetreten","falscher Login-Token")
                else:
                    tk.Label(loginwindow, text="Login fehlgeschlagen",font=size, bg="red").grid(row=1,column=2)
                    messagebox.showerror("Ein Fehler ist aufgetreten","Passwort falsch")

        #Account erstellen
        if beta_mode:            
            def createaccount():
                print("not functional yet")

            
        #Button für Eingabe bestätigen    
        button1 = tk.Button(loginwindow, text="Eingabe bestätigen", command=confirmbutton ,font=size, bg="#00FF2A")
        button1.grid(row=0,column=3)    
        #Button für Account erstellen
        if beta_mode:
            button2 = tk.Button(loginwindow, text="Account erstellen",command=createaccount,font=size,bg=buttoncolor)
            button2.grid(row=1,column=3)

        loginwindow.mainloop()
    
    

    #Button für Ausgabe in Konsole
    def toggleOutput():
        global consoleOutput
        global color
        global colorneu
        global Label28
        global Label29
        global toggleOutputExitCode
        #Umschalten von Ja auf Nein
        if consoleOutput == True:
            consoleOutput = False
            Label28.destroy()
            Label29 = tk.Label(window, text = "Nein",font=size, bg="red")
            Label29.grid(row=2, column=1)
            toggleOutputExitCode = 1
            quit#Schleife verlassen
        #Umschalten von Nein auf Ja
        elif consoleOutput == False:
            consoleOutput = True
            Label24.destroy()
            if toggleOutputExitCode == 1:
                Label29.destroy()
            Label28 = tk.Label(window, text = " Ja   ",font=size, bg="green")
            Label28.grid(row=2, column=1)            
        
        #Änderung der Einstellung in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("toggleOutput verändert, neuer Zustand: " + str(consoleOutput))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        
    #Button für Bahnradius-Ausgabe
    def toggleRadius():
        global toggleRadiusOutput
        global Label30
        global Label31
        global toggleRadiusExitCode
        #Umschaltung von Ja auf Nein
        if toggleRadiusOutput == True:
            toggleRadiusOutput = False
            Label30.destroy()
            Label31 = tk.Label(window, text = "Nein",font=size, bg="red")
            Label31.grid(row=3, column=1)
            toggleRadiusExitCode = 1
            quit
        #Umschaltung von Nein auf Ja
        elif toggleRadiusOutput == False:
            toggleRadiusOutput = True
            Label25.destroy()
            if toggleRadiusExitCode == 1:
                Label31.destroy()
            Label30 = tk.Label(window, text = " Ja   ",font=size, bg="green")
            Label30.grid(row=3, column=1)
        #Änderung der Einstellung in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("toggleRadius verändert, neuer Zustand: " + str(toggleRadiusOutput))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
    
    #Ausgabe Zufallsvariable
    def toggleoutputrandomvar():
        global outputrandomvar
        global Label32
        global Label33
        global toggleoutputrandomvarExitCode
        #Umschaltung von Ja auf Nein
        if outputrandomvar == True:
            outputrandomvar = False
            Label32.destroy()
            Label33 = tk.Label(window, text = "Nein",font=size, bg="red")
            Label33.grid(row=4, column=1)
            toggleoutputrandomvarExitCode = 1
            quit
        #Umschaltung von Nein auf Ja
        elif outputrandomvar == False:
            outputrandomvar = True
            Label26.destroy()
            if toggleoutputrandomvarExitCode == 1:
                Label33.destroy()
            Label32 = tk.Label(window, text = " Ja   ",font=size, bg="green")
            Label32.grid(row=4, column=1)
        
        #Änderung der Einstellung in Nutzerdaten Liste schreiben
        if collectuserdata == True:            
            currentuserdata=str("Outpout Randomvar verändert, neuer Zustand: " + str(outputrandomvar))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
    
    #Ausgabe Position            
    def togglePosition():
        global outputposition
        global Label34
        global Label35
        global togglePositionExitCode
        #Umschaltung von Ja auf Nein
        if outputposition == True:
            outputposition = False
            Label34.destroy()
            Label35 = tk.Label(window, text = "Nein",font=size, bg="red")
            Label35.grid(row=5, column=1)
            togglePositionExitCode = 1
            quit
        #Umschaltung von Nein auf Ja
        elif outputposition == False:
            outputposition = True
            Label27.destroy()
            if togglePositionExitCode == 1:
                Label35.destroy()
            Label34 = tk.Label(window, text = " Ja   ",font=size, bg="green")
            Label34.grid(row=5, column=1)
        
        #Änderung der Einstellung in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("Positionsoutput verändert, neuer Zustand: " + str(outputposition))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
    #Hilfe GUI
    def hilfe():
        #Prüfen, on Funktion rempte deaktiviert wurde
        if disable_Hilfe == True:
            messagebox.showerror("remote Steuerung","Diese Funktion wurde remote deaktiviert.")
            print("Fehlercode: 14")
            return()

        #Aktion in Liste mit Nutzerdaten schreiben
        if collectuserdata == True:
            currentuserdata=str("Hilfe Menü geöffnet")
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        
        #Hilfe Fenster erstellen
        helpgui=tk.Toplevel(window)
        helpgui.geometry("400x400")
        helpgui.title("Hilfe")
        path2 = "Fragezeichen.gif"
        img2 = ImageTk.PhotoImage(Image.open(path2))
        background_label = tk.Label(helpgui, image=img2)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #Dropdown-Menü für Hilfe erstellen
        options = tk.StringVar(master)
        options.set("Option wählen") 
        helptypein =tk.OptionMenu(helpgui, options, "Orbitberechnung", "Transitberechnung","manuelle Eingabe","ISS-Tracker","Menschen im All","Raketenstarts", "Einstellungen","mehr Funktionen","Nutzungsbedingungen")
        helptypein.grid(row=0,column=0)
        helptypein.config(bg="#FF6F61")
        
        
        def gethelptype():
            helptype=(options.get())#ausgewählte Option auslesen

            #Aktion in Liste mit Nutzerdaten schreiben
            if collectuserdata == True:
                currentuserdata=str("Eingabe Hilfe bestätigt, Typ="+str(helptype))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)

            if helptype == "Option wählen":
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte wählen sie eine Option!")
            else:
                if helptype == "Orbitberechnung":
                    os.system(os.path.join("Orbitrechnung.pdf"))#PDF mit Anleitung für Orbitberechnung öffnen
                elif helptype == "Transitberechnung":
                    os.system(os.path.join("Transitrechnung.pdf"))#PDF mit Anleitung für Transitberechnung öffnen
                elif helptype == "manuelle Eingabe":
                    os.system(os.path.join("manuelle_Eingabe.pdf"))#PDF mit Anleitung für manuelle Eingabe öffnen
                elif helptype == "ISS-Tracker":
                    os.system(os.path.join("ISS_Position.pdf"))#PDF mit Anleitung für ISS-Position öffnen
                elif helptype == "Menschen im All":
                    os.system(os.path.join("Menschen_im_Weltall.pdf"))#PDF mit Anleitung für Menschen im Weltall öffnen
                elif helptype == "Einstellungen":
                    os.system(os.path.join("Einstellungen.pdf"))#PDF mit Anleitung für Einstellungen öffnen   
                elif helptype == "Raketenstarts":
                    os.system(os.path.join("Raketenstarts.pdf"))#PDF mit Anleitung für Raketenstarts öffnen   
                elif helptype == "Nutzungsbedingungen":
                    os.system(os.path.join("Nutzungsbedingungen.pdf"))#PDF mit Nutzungsbedingungen öffnen
                elif helptype == "mehr Funktionen":
                    os.system(os.path.join("mehr_Funktionen.pdf"))#PDF mit Anleitung für mehr Funktionen öffnen

        
        #Button für Bestätigung der Auswahl    
        button = tk.Button(helpgui, text=" Auswahl bestätigen ", command=gethelptype,font=size, bg="#00FF2A")
        button.grid(row=0, column=1)
        helpgui.mainloop()


    #Funkion zum Melden von Fehlern
    def fehlermelden():
        #Prüfen, ob Funktion remote deaktiviert wurde
        if disable_Fehlermelden == True:
            messagebox.showerror("remote Steuerung","Diese Funktion wurde remote deaktiviert.")
            print("Fehlercode: 14")
            return()
        #Aktion in Liste mit Nutzerdaten schreiben
        if collectuserdata == True:
            currentuserdata=str("Fehler melden Bereich geöffnet")
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        fehlerwindow = tk.Toplevel(window)
        fehlerwindow.geometry("500x500")
        fehlerwindow.title("Fehler melden")
        #path4 = "Login.gif"
        #img4 = ImageTk.PhotoImage(Image.open(path3))
        #background_label = tk.Label(loginwindow, image=img3)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)

        def openfehlertxt():
            messagebox.showinfo("Fehler melden","Bitte speichern sie das Dokument nach der Eingabe ab!")
            file2 = open("Fehlermeldung.txt", "w")
            file2.close()
            webbrowser.open("Fehlermeldung.txt")

        def sendfehlermeldung():

            #Zeit der letzten Fehlermeldung importieren
            file7 = open("Fehlerzeit.txt", "r")
            file7.read()
            with open("Fehlerzeit.txt","r") as file7:
                fehler_last_time = str(file7.readline())
            file7.close()

            #Zeitdifferenz errechnen (erst string aus txt Dokument in datetime Objekt umwandeln)
            starttime_in = fehler_last_time
            starttime_raw = starttime_in[0:len(starttime_in)-7]
            starttime = datetime.datetime.strptime(starttime_raw, "%Y-%m-%d %H:%M:%S")
            currenttime = datetime.datetime.now()
            delta_t = str(currenttime - starttime)

            delta_t = delta_t[delta_t.find(",")+1:len(delta_t)] #Tage usw. aus sting entfernen
            #Zeitdifferenz in Sekunden umrechnen
            hours = int(delta_t[0:delta_t.find(":")])
            minutes = int(delta_t[(delta_t.find(":")+1):(delta_t.find(":")+3)])
            minutes_total = minutes + hours * 60
            seconds = int(delta_t[(delta_t.find(":")+4):(delta_t.find("."))])
            seconds_total = seconds + minutes * 60

            timedifference = 900 #Anzahl Sekunden, wie lange es dauert, bis eine neue Fehlermeldung abgegeben werden darf

            waittime = timedifference - seconds_total
            #Umrechnung der Zeit
            T =waittime
            divmodT = str(divmod(T, 60))
            Minuten = int(divmodT[(divmodT.find("(")+1):divmodT.find(",")])
            Sekunden = int(divmodT[(divmodT.find(",")+2):divmodT.find(")")])

            if seconds_total < timedifference:
                waitstring = "Bitte warten sie noch "+str(Minuten)+" Minuten, " +str(Sekunden)+" Sekunden "+"bis Sie eine neue Fehlermeldung absenden"
                messagebox.showerror("Cooldown",waitstring)
                return()


            

            #Login Daten für OAuth2 (Web-Autorisierungsserver) flow,
            #Missbrauch dieser Daten wird strafrechtlich verfolgt; die eigene Verwendung oder Weitergabe an Dritte ist ausdrücklich untersagt!
            app_key = "ca245ceyx9r4s6q"
            app_secret = "ts6r2dr46d4k44k" 
            refresh_token = "N9fClzC10jIAAAAAAAAAAd5HWGhUGQkOeHQF2KxnVpDwVU2G9PiIMZr8OYFccqyF"

            def uploadfile(file,dest):
                #Prüfen, wann die letzt Meldung abgesetzt wurde und ob eine neue gesendet werden darf

                # Access token
                file2 = open("token.txt", "r")
                file2.read()
                with open("token.txt","r") as file2:
                    TOKEN =str(file2.readline())   
                file2.close()

                LOCALFILE = file
                BACKUPPATH = str("/API/"+dest)

                #Dokument in dropbox erstellen, evntl Datei überschreiben
                def backup():
                    with open(LOCALFILE, 'rb') as f:

                        if adminmode == True:
                            print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")

                        try:
                            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
                        except ApiError as err:
                            if (err.error.is_path() and
                                    err.error.get_path().error.is_insufficient_space()):
                                sys.exit("ERROR: Cannot back up; insufficient space.")
                            elif err.user_message_text:
                                print(err.user_message_text)
                                sys.exit()
                            else:
                                print(err)
                                sys.exit()

                def checkFileDetails():
                    if adminmode == True:
                        print("Checking file details")
                        for entry in dbx.files_list_folder('').entries:
                            print("File list is : ")
                            print(entry.name)

                if __name__ == '__main__':
                    if (len(TOKEN) == 0):
                        sys.exit("ERROR: missing access token")

                    if adminmode == True:
                        print("Creating a Dropbox object...")
                    dbx = dropbox.Dropbox(TOKEN)

                    try:
                        dbx.users_get_current_account()
                    except AuthError as err:
                        sys.exit("ERROR: Invalid access token")

                    try:
                        checkFileDetails()
                    except Error as err:
                        sys.exit("Error while checking file details")

                    if adminmode == True:
                        print("Creating backup...")
                    backup()

                    if adminmode == True:
                        print("Done!")
            
            def refreshtoken():
                # authoritazation url bauen (wird nicht in diesem Programm benötigt, für Debug-Zwecke trotzdem hinterlegt):
                authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key

                


                #API-Token erneuern
                token_url = "https://api.dropboxapi.com/oauth2/token"
                params = {
                    "grant_type": "refresh_token",
                    "client_id": app_key,
                    "client_secret": app_secret,
                    "refresh_token": refresh_token
                }


                r = requests.post(token_url, data=params)
                response = r.text
                #result = json.loads(response.read())
                #access_token = response["acces_token"]
                #print(access_token)
                result =  json.loads(response)
                access_token = result["access_token"]

                savetoken = open("token.txt", "w")#Textdokument öffnen / erstellen 
                savetoken.write(access_token)#access_token in Textdokument schreiben
                savetoken.close()
            

            #Vom Nutzer eingegebene Fehlermeldung erstellen
            currenttime = str(datetime.datetime.now())
            desttxt = str("Fehlermeldung"+currenttime+"_UUID="+str(UUID)+".txt")    
            userdatatxt = open("userdata.txt", "w")#Textdokument öffnen / erstellen                                                        

            if sendlogs == True:
                #Logs in Textdokument schreiben (um Fehler replizieren zu können)                    
                for x in range(len(userdata)):
                    if (userdata[x] != ""):
                        userdatatxt.write((str(userdata[x][0])+": "+userdata[x][1])+"\n")#Nutzerdaten in Textdokument schreiben
                userdatatxt.close()

            destlogs = str("log-"+currenttime+"_UUID="+str(UUID)+".txt")
            


            #Funktion um zu überprüfen, ob das Dokument zu groß ist
            def checkfordatacap():
                file = open("Fehlermeldung.txt")
                data = file.readlines()
                i= 0
                for x in data:
                    i = i+1
                    if len(x) > 50:
                        return(True)

                    if i >= 40:
                        return(True)
                return(False)

            #session logs überprüfen, um spam / DoS zu verhindern

            def checkfordatacap2():
                file = open("userdata.txt")
                data = file.readlines()
                i= 0
                for x in data:
                    i = i+1
                    if len(x) > 80:
                        return(True)

                    if i >= 70:
                        return(True)
                return(False)



            #Bei zu großem Dokument nicht senden, Fehler loggen, User informueren
            datacap = checkfordatacap()
            if datacap == True:
                messagebox.showerror("Ein Fehler ist aufgetreten","Ihre Nachricht ist zu lange. Bitte schreiben Sir mir eine E-Mail, falls die Nachricht nicht kürzer sein kann")
                if collectuserdata == True:
                    currentuserdata=str("Fehlermeldung zu groß zur Übertragung")
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                    return()

            datacap_session_logs = checkfordatacap2()
            if datacap_session_logs == True:
                messagebox.showerror("Ein Fehler ist aufgetreten","Ein Fehler ist aufgetreten. Bitte starten SIe das Programm neu und versuchen Sie es erneut")
                if collectuserdata == True:
                    currentuserdata=str("session logs zu groß zur Übertragung")
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                    return()


            #Testen ob Hochladen funktioniert, wenn nicht Token neu generieren
            if datacap == False and datacap_session_logs == False:
                print("Fehlermeldung wird übertragen...")
                try:
                    uploadfile("Fehlermeldung.txt",desttxt)
                    if sendlogs == True:
                        uploadfile("userdata.txt",destlogs)
                    print("Upload erfolgreich")
                except:
                    print("an error occured")
                    print("refreshing token...")
                    refreshtoken()
                    uploadfile("Fehlermeldung.txt",desttxt)
                    if sendlogs == True:
                        uploadfile("userdata.txt",destlogs)
                    print("Upload erfolgreich")
                

                file9 = open("Fehlermeldung.txt","r")
                with open("Fehlermeldung.txt","r") as file9:
                    content =str(file9.readline())   
                file9.close()

                #Event loggen
                if collectuserdata == True:
                    currentuserdata=str("Fehlermeldung wurde übertragen, content = "+str(content))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                

                try:
                    sendmessagetowebhook("low","bugreport","**BUGREPORT:**\nUUID=||"+str(UUID)+"||\nTIME="+str(datetime.datetime.now()))
                except:#mehrere Fehlerinstanzen
                    try:
                        sendmessagetowebhook("high","general","BUGREPORT WEBHOOK DOWN!\nACTION REQUIRED")#webhook für Probleme
                    except:
                        try:
                            requests.post(emergency_webhook, data="TOTAL OUTTAGE")#webhook für kompletten Ausfall ALLER Webhooks
                        except:
                            print("an severe error occured, please re-check your internet connection! If this error keeps popping up, ignore it!")


                #Zeit, wann Fehlermeldung abgeschickt wurde in txt Dokument schreiben
                file6 = open("Fehlerzeit.txt","w")
                file6.write(str(datetime.datetime.now()))
                file6.close()

        #Texteingabe Buttton
        button13 = tk.Button(fehlerwindow,text="Für Texteingabe hier klicken",command=openfehlertxt,font=size, bg = buttoncolor)
        button13.grid(row=0,column=0)
        #'Meldung übertragen'-Button
        button14 = tk.Button(fehlerwindow,text="Meldung übertragen",command=sendfehlermeldung,font=size, bg = buttoncolor)
        button14.grid(row=0,column=1)
    
        fehlerwindow.mainloop()

        
    
    #'Ausgabe in Konsole'-Button
    button = tk.Button(window, text=" Ausgabe in Konsole ", command=toggleOutput,font=size, bg=buttoncolor)
    button.grid(row=0, column=0)
    #'Ausgabe Bahnradius'-Button
    button1 = tk.Button(window, text=" Ausgabe Bahnradius ", command=toggleRadius, font=size, bg=buttoncolor)
    button1.grid(row=0,column=1)
    #'Ausgabe Zufallsvariable(Bedeutung in Anhang)
    button2 = tk.Button(window, text=" Ausgabe Zufallsvariable ", command=toggleoutputrandomvar, font=size, bg=buttoncolor)
    button2.grid(row=0,column=2)
    #'Ausgabe geographische Position"-Button
    button2 = tk.Button(window, text=" Ausgabe ISS-Position ", command=togglePosition, font=size, bg=buttoncolor)
    button2.grid(row=0,column=3)
    #'Fehler melden'-Button
    button12 = tk.Button(window, text="Fehler melden",command=fehlermelden,font=size, bg=buttoncolor)
    button12.grid(row=0,column=4)
    #'logging Einstellungen'
    button6 = tk.Button(window, text=" logging Einstellungen ", command=createloggingmenu, font=size, bg=buttoncolor)
    button6.grid(row=0,column=5)
    #'Login' Button
    button3 = tk.Button(window, text=" Login ", command=createLoginWindow, font=size, bg="#7FCDCD")
    button3.grid(row=0,column=6)
    #'Hilfe' Button
    button4 = tk.Button(window, text=" Hilfe ", command=hilfe, font=size, bg="#00FF2A")
    button4.grid(row=0,column=7)
    #'Quit' Button
    button5 = tk.Button(window, text=" Quit ", command=quitprogramm, font=size, bg="red")
    button5.grid(row=0,column=8)    
    
    window.mainloop()#Einstellungs GUI mainloop


    
#Erstellung der Labels
Label1 = tk.Label(master, text="                        Planet:",font=size, bg=color)
Label1.grid(row=0)
Label2 = tk.Label(master, text="     Höhe/Umlaufdauer:",font=size, bg=color)
Label2.grid(row=1)
#Erstellung der Entry-Felder für Planet und gegebene Größe 
str_out=tk.StringVar(master)
str_out.set("Output")
options = tk.StringVar(master)
options.set("Planet auswählen") 
#Dropbox für Planeten
PlanetInput =tk.OptionMenu(master, options, "Merkur","Venus", "Erde", "Mars","Jupiter","Saturn","Uranus","Neptun","Pluto","Mond","Sonne")
PlanetInput.grid(row=0,column=1)
PlanetInput.config(bg="#FF6F61")




def output():
    str_out.set(options.get())
    planet=(options.get())
numberin=tk.Entry(master)
numberin.grid(row=1, column=1)
#Erstellung Label für 'Manueller Input'
Label3=tk.Label(master, text="          Manueller Input:",font=size, bg=color)
Label3.grid(row=6)
Label4=tk.Label(master, text = "Nein",font=size, bg="red")
Label4.grid(row=6, column=1)
#Erstellung Label für 'Transitberechnung'
Label5=tk.Label(master, text="   Transitberechnung:",font=size, bg=color)
Label5.grid(row=7)
Label6=tk.Label(master, text = "Nein",font=size, bg="red")
Label6.grid(row=7, column=1)

#Hifsvariablen für buttonPress
TransitrechnungExecutionExitCode = 0 
OrbitrechnungExecutionExitCode = 0
RadiusOutputExecutionExitCode = 0

#Buttonprozedur
def buttonPress():
    global manualInput
    global MenschenimAll_ExitCode
    if MenschenimAll_ExitCode == 1:
        button12.destroy()
        AstronautInput.destroy()
        MenschenimAll_ExitCode = 0    
    #Daten aus Input-Feldern importieren
    number = numberin.get()
    planet=(options.get())
    
    if len(number) > 15:
        messagebox.showerror("Ein Fehler ist aufgetreten","Eingabe zu lang ")
        if collectuserdata == True:
            currentuserdata=str("ERROR: invalid value (to long) (Transitrechner/Orbitrechner) - value="+str(number))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        return()

    if str(planet) == "Planet auswählen" and manualInput == False:
        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte wählen sie einen Planeten aus ")
        return()
    
    begin_time = datetime.datetime.now()
    
    
    
    #Variablendeklaration für Button
    v = 0
    h = 0
    T = 0
    r = 0
    Minuten = 0
    Sekunden = 0
    Stunden = 0
    Kilometer = 0
    Meter = 0
    kmh = 0
    
    #Farbendeklaration für pygame
    white = (255, 255, 255)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    grey = (200, 200, 200)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    colorn = "blue"
    textcolor = white
    #globale Variablen 
    global Transitberechnung
    global planetzwei
    global outputrandomvar
    global consoleOutput
    
    #Labels und Hilfvariablen
    global TransitrechnungExecutionExitCode
    global OrbitrechnungExecutionExitCode
    global RadiusOutputExecutionExitCode
    global Label13
    global Label14
    global Label15
    global Label16
    global Label17
    global Label18
    global Label19
    global Label20
    global Label21
    global Label22
    global Label23
    
    #Transitberechnung
    if Transitberechnung == True:

        updatestatistics("Transitrechnung")
        if OrbitrechnungExecutionExitCode == 1:
            Label16.destroy()
            Label17.destroy()
            Label18.destroy()
            Label19.destroy()
            Label20.destroy()
            Label21.destroy()
        if RadiusOutputExecutionExitCode == 1:
            Label22.destroy()
            Label23.destroy()
            
        Jahre = 0
        Tage = 0
        Stunden = 0
        Minuten = 0    
        Sekunden = 0
        
        planet2=planetzwei.get()#Planet aus Input-Feld importieren
        #Planet1
        planet = (options.get())
        #planet=input("Planet 1:")
        if planet == "Merkur" or planet == "merkur" or planet =="Mercury" or planet == "mercury":
            T1=Tme
            picture1 = pygame.image.load("Merkur.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Venus" or planet== "venus":
            T1=Tve
            picture1 = pygame.image.load("Venus.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Erde" or planet== "erde" or planet== "Earth" or planet== "earth":
            T1=Ter
            picture1 = pygame.image.load("Erde.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Mars" or planet== "mars" :
            T1=Tma
            picture1 = pygame.image.load("Mars.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Jupiter" or planet== "jupiter" :
            T1=Tju
            picture1 = pygame.image.load("Jupiters.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Saturn" or planet== "saturn" :
            T1=Tsa
            picture1 = pygame.image.load("Saturn.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Uranus" or planet== "uranus" :
            T1=Tur
            picture1 = pygame.image.load("Uranus.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Neptun" or planet== "neptun" or planet== "Neptune" or planet== "neptune" :
            T1=Tne
            picture1 = pygame.image.load("Neptun.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Pluto" or planet== "pluto":
            T1=Tpl
            picture1 = pygame.image.load("Pluto.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet == "Mond" or planet== "mond" or planet== "Moon" or planet== "moon" :
            T1=Tmo
            picture1 = pygame.image.load("Mond.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        elif planet =="ISS" or planet == "iss":
            T1=Tiss
            picture1 = pygame.image.load("ISS.png")
            picture1 = pygame.transform.scale(picture1,(50,50))
        else:
            #Fehler in Liste mit Nutzerdaten schreiben / loggen
            if collectuserdata == True:
                currentuserdata=str("ERROR: invalid value (Transitrechner,planet1) - value="+str(planet2))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)

        #Planet2
        #planet2=input("Planet 2:")
        planet2=planetzwei.get()
        security_check(planet2,"Transitrechner")



        if planet2 == "Merkur" or planet2 == "merkur" or planet2 =="Mercury" or planet2 == "mercury":
            T2=Tme
            picture2 = pygame.image.load("Merkur.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Venus" or planet2== "venus" :
            T2=Tve
            picture2 = pygame.image.load("Venus.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Erde" or planet2== "erde" or planet2== "Earth" or planet2== "earth":
            T2=Ter
            picture2 = pygame.image.load("Erde.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Mars" or planet2== "mars" :
            T2=Tma
            picture2 = pygame.image.load("Mars.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Jupiter" or planet2== "jupiter" :
            T2=Tju
            picture2 = pygame.image.load("Jupiter.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Saturn" or planet2== "saturn" :
            T2=Tsa
            picture2 = pygame.image.load("Saturn.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Uranus" or planet2== "uranus" :
            T2=Tur
            picture2 = pygame.image.load("Uranus.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Neptun" or planet2== "neptun" or planet2== "Neptune" or planet2== "neptune" :
            T2=Tne
            picture2 = pygame.image.load("Neptun.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Pluto" or planet2== "pluto":
            T2=Tpl
            picture2 = pygame.image.load("Pluto.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 == "Mond" or planet2== "mond" or planet2== "Moon" or planet2== "moon" :
            T2=Tmo
            picture2 = pygame.image.load("Mond.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        elif planet2 =="ISS" or planet2 == "iss":
            T2=Tiss
            picture2 = pygame.image.load("ISS.png")
            picture2 = pygame.transform.scale(picture2,(50,50))
        else:
            messagebox.showerror("Ein Fehler ist aufgetreten", "Bitte geben sie einen zulässigen Himmelskörper ein!")
            #Fehler in Nutzerdaten Liste schreiben
            if collectuserdata == True:
                currentuserdata=str("ERROR: invalid value (Transitrechner,planet2) - value="+str(planet2))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)
            print("Fehlercode: 9")
            return()

        Erde_Mittelpunkt = False
        #herausfinden ob es sich um einen Transit eines Objektes und einem Punkt auf der Erde handelt
        if T2==Tiss or T1==Tiss or T2==Tmo or T1==Tmo:
            picture = pygame.image.load("Erde.png")
            picture = pygame.transform.scale(picture,(100,100))
            Erde_Mittelpunkt = True

            if T1 == Ter:
                T1 = Ter2
            elif T2 == Ter:
                T2 = Ter2
        else:
            picture = pygame.image.load("Sonne.png")
            picture = pygame.transform.scale(picture,(100,100))

        if T1 < T2:
            deltaT=(((2*pi)/T1)-((2*pi)/T2))
        if T1 > T2:
            deltaT=(((2*pi)/T2)-((2*pi)/T1))
        if T1 == T2:
            messagebox.showerror("Ein Fehler ist aufgetreten","Ein Fehler ist aufgetreten")
            print("Fehlercode: 7")
            #Fehler in Nutzerdaten Liste schreiben
            if collectuserdata == True:
                currentuserdata=str("ERROR: Transitrechner: value1 = value2")
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)

        t=((2*pi)/deltaT)#
        T = round(t)

        if (T/60) < 60:        
            temp = str(divmod(T, 60))
            Minuten = int(temp[1:temp.find(",")])
            Sekunden = int(round(int(temp[(temp.find(",")+1):(temp.find(")"))])))
        elif (T/60) >= 60:
            temp = str(divmod(T, 60))
            minuten1 = int(temp[1:temp.find(",")])
            Sekunden = int(int(round(float(temp[(temp.find(",")+1):(temp.find(")"))]))))
            temp2 = str(divmod(minuten1, 60))
            Stunden = int(temp2[1:temp2.find(",")])
            Minuten = int(round(int(temp2[(temp2.find(",")+1):(temp2.find(")"))])))
        if Stunden >= 24:
            temp = str(divmod(Stunden, 24))
            Tage = int(temp[1:temp.find(",")])
            Stunden = int(round(int(temp[(temp.find(",")+1):(temp.find(")"))])))
        if Tage >= 365:
            temp=str(divmod(Tage, 365))
            Jahre = int(temp[1:temp.find(",")])
            Tage = int(round(int(temp[(temp.find(",")+1):(temp.find(")"))])))
        #print("Tage: " + str(Tage) + " Stunden: " + str(Stunden) +" Minuten: " + str(Minuten) + " Sekunden: " + str(Sekunden))
        tk.Label(master, text="Ergebnis:", font=size,bg = color).grid(row=11)
        Label13 = tk.Label(master, text="Zeit bis zum Transit: ",font=size, bg= color)
        Label13.grid(row=12,column=0)
        Label14 = tk.Label(master, text="Jahre: "+str(Jahre)+" Tage: " + str(Tage),font=size, bg = color)
        Label14.grid(row=12,column=1)
        Label15 = tk.Label(master, text=" Stunden: " + str(Stunden) +" Minuten: " + str(Minuten) + " Sekunden: " +str(Sekunden),font=size, bg = color)
        Label15.grid(row=12,column=2)
        
        TransitrechnungExecutionExitCode = 1
        
        if consoleOutput == True:
            print("Jahre: "+str(Jahre)+" Tage: " + str(Tage) + " Stunden: " + str(Stunden) +" Minuten: " + str(Minuten) + " Sekunden: " +str(Sekunden))
        messagebox.showinfo("Berechnung fertig","Die Berechnung wurde erfolgreich beendet")        #Benachrichtigung, dass die Berechnung erflogreich beendet wurde
        
        if T2 < T1:
            tempvarpicture = picture1
            picture1 = picture2
            picture2 = tempvarpicture
        starttime_animation_transitrechnung = datetime.datetime.now()
        pygame.init()
        screen = pygame.display.set_mode((900, 800))

        white = (255, 255, 255)
        blue = (0, 0, 255)
        yellow = (255, 255, 0)
        grey = (200, 200, 200)
        black = (0, 0, 0)
        red = (255, 0, 0)

        sun_radius = 50
        center = (350, 350)
        font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf",20)
        pygame.display.set_caption('Transitrechner-Visualiziation')


        earth_orbit = random.randint(1,200) / 100
        venus_orbit = random.randint(1,200) / 100

        clock = pygame.time.Clock()

        running = True
        global contact
        contact = False

        global i
        i = 0
        global z
        z = 0
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if contact == False:
                
                if i == 0:
                    earth_x = math.cos(earth_orbit) * 300 + 350
                    earth_y = -math.sin(earth_orbit) * 300 + 350
                    earth_orbit += .002
                    i = 1
                elif i == 1:
                    i = 0
                screen.fill(black)

                venus_x = math.cos(venus_orbit) * 200 + 350
                venus_y = -math.sin(venus_orbit) * 200 + 350
                venus_orbit += .002
                    
                pygame.draw.circle(screen, white, center, 200, 2)
                pygame.draw.circle(screen, white, center, 300, 2)
                
                #pygame.draw.circle(screen,red, (int(venus_x),int(venus_y)),15)
                screen.blit(picture1,(int(venus_x-25),int(venus_y-25)))
                #pygame.draw.circle(screen, yellow, center, sun_radius)
                #pygame.draw.circle(screen, blue, (int(earth_x), int(earth_y)), 15)
                if Erde_Mittelpunkt == False:
                    screen.blit(picture2,(int(earth_x-25),int(earth_y-25)))
                        
                x_distance = max(earth_x,venus_x)-min(earth_x,venus_x)
                
                y_distance = max(earth_y,venus_y)-min(earth_y,venus_y)

                delta_y = (earth_y+venus_y) / 2
                
                abstand = math.sqrt(x_distance**2+y_distance**2)
                screen.blit(picture,(300,300))
            screen.blit(font.render("Zeit bis zum nächsten Transit:",False,white),(580,600))
            screen.blit(font.render(str("Jahre: "+str(Jahre)+" Tage: "+str(Tage)+" Stunden: "+str(Stunden)),False,white),(580,640))
            screen.blit(font.render(str("Minuten: "+str(Minuten)+" Sekunden: "+str(Sekunden)),False,white),(580,680))
            
            if abstand < 100.0002:
                #print("contact")
                if z < 750:
                    contact = True
                else:
                    contact = False
                    
                #pygame.draw.line(screen, white, center, (earth_x, earth_y))
                #print("Erde: "+"X: "+str(earth_x)+" Y: "+str(earth_y))
                earth_x_rounded = round(earth_x)
                earth_y_rounded = earth_y -2
                #print("Gerundet: "+"X: "+str(earth_x_rounded)+" Y: "+str(earth_y_rounded))
                pygame.draw.line(screen, white, center, (earth_x_rounded, earth_y_rounded)) 
                z = z +1
                #rprint(z)
            else:
                z = 0
            pygame.display.flip()

            clock.tick(500)

        pygame.quit()
        endtime_animation_transitrechnung = datetime.datetime.now()
        runtime = endtime_animation_transitrechnung - starttime_animation_transitrechnung
        if collectuserdata == True:
            currentuserdata=str("Transitrechnung wurde durchgeführt"+"; Laufzeit gesamt: "+str(runtime))
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)

    else:
        if TransitrechnungExecutionExitCode == 1:
            Label13.destroy()
            Label14.destroy()
            Label15.destroy()
        if RadiusOutputExecutionExitCode == 1:
            Label22.destroy()
            Label23.destroy()
        
        updatestatistics("Orbitrechnung")

        global Minput
        global Rinput
        global toggleRadiusOutput
        if manualInput == True:
            Min=Minput.get()
            Rin=Rinput.get()

            #Testen, ob die manuelle Eingabe in float umgewandelt werden kann
            try:
                testvar_min = float(Min)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner,manual Input, Min) - value="+str(Min))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()

            #Testen, ob die manuelle Eingabe in float umgewandelt werden kann
            try:
                testvar_rin = float(Rin)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner,manual Input, Rin) - value="+str(Rin))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()

            
            #Security-Check
            security_check(Min,"Orbitrechner")
            security_check(Rin,"Orbitrechner")




                
    #M und r für Planet festlegen        
        if manualInput == False:
            if planet == "Merkur":    
                M=Mme
                r=Rme
                colorn = red
                textcolor = black
                picture = pygame.image.load("Merkur.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Venus":
                M=Mve
                r=Rve
                colorn = yellow
                textcolor = black
                picture = pygame.image.load("Venus.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Erde":
                M=Mer
                r=Rer
                colorn = blue
                textcolor = white
                picture = pygame.image.load("Erde.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Mars":
                M=Mma
                r=Rma
                colorn = red
                textcolor = black
                picture = pygame.image.load("Mars.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Jupiter":
                M=Mju
                r=Rju
                colorn = yellow
                textcolor = black
                picture = pygame.image.load("Jupiter.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Saturn":
                M=Msa
                r=Rsa
                colorn = yellow
                textcolor = black
                picture = pygame.image.load("Saturn.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Uranus":
                M=Mur
                r=Rur
                colorn = green
                textcolor = black
                picture = pygame.image.load("Uranus.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Neptun":
                M=Mne
                r=Rne
                colorn = blue
                textcolor = white
                picture = pygame.image.load("Neptun.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Pluto":
                M=Mpl
                r=Rpl
                colorn = green
                textcolor = black
                picture = pygame.image.load("Pluto.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Mond":
                M=Mmo
                r=Rmo
                colorn = grey
                textcolor = black
                picture = pygame.image.load("Mond.png")
                picture = pygame.transform.scale(picture,(100,100))
            elif planet == "Sonne":
                M=Mso
                r=Rso
                colorn=yellow
                textcolor = black
                picture = pygame.image.load("Sonne.png")
                picture = pygame.transform.scale(picture,(100,100))
        else:
            if manualInput == False:    #Manueller Input
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen zulässigen Himmelskörper ein!")#Fehlermeldung, bei keinem / unzulässigem Himmelskörper
                print("Fehlercode: 4") 
                return()
            elif manualInput == True:
                M=int(Min)
                r=int(Rin)
                picture = pygame.image.load("Planet.png")#Standardbild für Planet bei manuellem Input
                picture = pygame.transform.scale(picture,(100,100))

    #Einheiten erkennen und umrechnen
        #Anti-Exploit-Sektion
        security_check(number,"Orbitrechner")
        word = number



        if (word.find("km") > -1):
            try: 
                h=float(float(word[:word.find("km")] + (word[word.find("km")+2:]))*1000)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Höhe"
        elif (word.find("min") > -1):
            try:
                T=float(float(word[:word.find("min")] + (word[word.find("min")+3:]))*60)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Zeit"
        elif (word.find("dm") > -1):
            try:
                h=float(float(word[:word.find("dm")] + (word[word.find("dm")+2:]))/10)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Höhe"
        elif (word.find("cm") > -1):
            try:
                h=float(float(word[:word.find("cm")] + (word[word.find("cm")+2:]))/100)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Höhe"
        elif (word.find("mm") > -1):
            try:
                h=float(float(word[:word.find("mm")] + (word[word.find("mm")+2:]))/1000)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Höhe"
        elif (word.find("h") > -1):
            try:
                T=float(float(word[:word.find("h")] + (word[word.find("h")+1:]))*60*60)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Zeit"
        elif (word.find("s") > -1):
            try:
                T=float(word[:word.find("s")] + (word[word.find("s")+1:]))
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Zeit"
        elif (word.find("m") > -1):
            try:
                h=float(word[:word.find("m")] + (word[word.find("m")+1:]))
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Höhe"
        elif (word.find("d") > -1):
            try:
                T=float(float(word[:word.find("d")] + (word[word.find("d")+1:]))*24*60*60)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Zeit"
        elif (word.find("a") > -1):
            try:
                T=float(float(word[:word.find("a")] + (word[word.find("a")+1:]))*365*24*60*60)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                return()
            Eingabe = "Zeit"
        
        else:
            messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie eine zulässige Einheit ein !")#Fehlermeldung bei unzulässiger Einheit
            #Fehler in Nutzerdaten Liste schreiben
            if collectuserdata == True:
                currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)
            print("Fehlercode: 1")
            return()


        if r > 0:
            Rges =float(h + float(r))       #Berechnung des Bahnradius
        if v <= 0 and h <= 0 and T <= 0:    #Prüfung der Werte (Vermeidung von negativem Input)
            messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen zulässigen Wert ein!")#Fehlermeldung bei negativem Input
            #Fehler in Nutzerdaten Liste schreiben
            if collectuserdata == True:
                currentuserdata=str("ERROR: invalid value (Orbitrechner) - value="+str(word))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)
            print("Fehlercode: 3")
            return()

        else:
            if Eingabe == "Zeit" :          #Rechnung für Zeit gegeben
                h = float((((G*M*(T*T))/(4*pi*pi))**(1/3))- (r))
                v = float(((G*M)/Rges)**(1/2))
            elif Eingabe == "Höhe" :        #Rechnung für Höhe gegebn
                T = float(((((Rges**3)*4*(pi**2))/(G*M))**(1/2)))
                v = float(((G*M)/Rges)**(1/2))
            else:
                messagebox.showerror("Ein Fehler ist aufgetreten", "Ein Fehler ist aufgetreten")#Fehlermeldung, wenn weder Höhe noch Zeit eingegeben wurden  
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid calculation (Orbitrechner), Eingabe="+str(Eingabe))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                print("Fehlercode: 2") 
            
            if T < 0 or v < 0 or r < 0:
                messagebox.showerror("Ein Fehler ist aufgetreten", "Ein Fehler ist aufgetreten")#Fehlermeldng, wenn negative Werte eingegeben wurden oder als Ergebnisse ermittelt werden
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid result (Orbitrechner) - value="+str(T))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 10")
                print("Fehlercode: 5")
                return()
            #Umrechnung der Ergebnisse
            
            #Runden der Werte, um die Umrechnung zu vereinfachen
            T = round(T)
            h = round(h)
            v = round(v)
            #Umrechnung der Zeit
            if (T/60) < 60:        
                temp = str(divmod(T, 60))
                Minuten = int(temp[1:temp.find(",")])
                Sekunden = int(round(int(temp[(temp.find(",")+1):(temp.find(")"))])))
            elif (T/60) >= 60:
                temp = str(divmod(T, 60))
                minuten1 = int(temp[1:temp.find(",")])
                Sekunden = int(int(round(float(temp[(temp.find(",")+1):(temp.find(")"))]))))
                temp2 = str(divmod(minuten1, 60))
                Stunden = int(temp2[1:temp2.find(",")])
                Minuten = int(round(int(temp2[(temp2.find(",")+1):(temp2.find(")"))])))
            
            #Umrechnen der Höhe
            temph = str(divmod(h, 1000))
            Kilometer = int(temph[1:temph.find(",")])
            Meter = int(round(int(temph[(temph.find(",")+1):(temph.find(")"))])))    
            
            #Umrechnen der Geschwindigkeit
            tempv = v*(11/3)
            kmh = round(tempv)
            ms = round(v)
            
            if Transitberechnung == False:
                calctime = (datetime.datetime.now() - begin_time)
            
            #Ausgabe Ergebnis in Konsole
            if consoleOutput == True:        
                print("Stunden: " + str(Stunden) + " Minuten: " + str(Minuten) + " Sekunden: " + str(Sekunden)) #Ausgabe für Konsole
                print("Kilometer: " + str(Kilometer) + " Meter: " + str(Meter))
                print("km/h: " + str(kmh))
                if toggleRadiusOutput == True:
                    print("Radius: " + str(r))
            #Ausgabe Ergebnis durch Label
            tk.Label(master, text=" ").grid(row=12)
            Label16 = tk.Label(master, text="Umlaufdauer:", font=size,bg = color)
            Label16.grid(row=12)
            Label17 = tk.Label(master, text="Höhe:", font=size,bg = color)
            Label17.grid(row=13)
            Label18 = tk.Label(master, text="Geschwindigkeit:", font=size,bg = color)
            Label18.grid(row=14)
            tk.Label(master, text="Ergebnis:", font=size,bg = color).grid(row=11)
            Label19 = tk.Label(master, text="Stunden: " + str(Stunden) + " Minuten: " + str(Minuten) + " Sekunden: " + str(Sekunden),font=size,bg = color)
            Label19.grid(row=12,column=1)
            Label20 = tk.Label(master, text="Kilometer: " + str(Kilometer) + " Meter: " + str(Meter),font=size,bg = color)
            Label20.grid(row=13,column=1)
            Label21 = tk.Label(master, text ="km/h: " + str(kmh) + " (in m/s: " + str(ms)+ "  ) ", font=size,bg = color)
            Label21.grid(row=14,column=1)
            
            OrbitrechnungExecutionExitCode = 1
            
            #Ausgabe Bahnradius
            if toggleRadiusOutput == True:#Ausgabe Bahnradius
                Label22 = tk.Label(master, text= str(r) + " Meter", font=size,bg=color)
                Label22.grid(row=15,column=1)
                Label23 = tk.Label(master, text="Bahnradius:" ,font=size,bg=color)
                Label23.grid(row=15)
                RadiusOutputExecutionExitCode = 1
            elif toggleRadiusOutput == False:#Bahnradius-Ausgabe von möglichen vorherigen Berechnungen mit Einstelung aktiviert, überschreiben
                if color == "#C2CAD0":#nur überschreiben, wenn Hintergrundfarbe nicht im Quellcode verändert wurde
                    tk.Label(master, text="                                 ", font=size).grid(row=15,column=1)
                    tk.Label(master, text="                                 " ,font=size).grid(row=15)
            messagebox.showinfo("Berechnung fertig","Die Berechnung wurde erfolgreich beendet")        #Benachrichtigung, dass die Berechnung erflogreich beendet wurde
            #Ausgabe Hinweis wenn Höhe negativ
            if h <= 0:
                messagebox.showinfo("Hinweis","Hinweis: Diese Bahn ist parktisch nicht möglich, da sie innerhalb des Himmelskörpers verlaufen müsste")
            
            
            pygame.init()#Pygame loop Start
            screen = pygame.display.set_mode((800, 800))
            pygame.display.set_caption('Orbitrechner-Visualiziation')
            #Farbendeklaration
            white = (255, 255, 255)
            blue = (0, 0, 255)
            yellow = (255, 255, 0)
            grey = (200, 200, 200)
            black = (0, 0, 0)
            red = (255, 0, 0)
            green = (0, 255, 0)

            Text = planet

            #Variabledeklaration
            rn = 50
            center = (300, 300)
            orbit = 0
            orbit_x = 50
            orbit_y = 350

            font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf",15)

            clock = pygame.time.Clock()
            running = True
            randomvar = random.randint(0,1000)#Zahl zwischen 0 und 1000 per Zufall auswählen
            if outputrandomvar == True:
                print(randomvar)#Zufallszahl ausgeben
            
            
            
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                
                #Planetenposition erneuern
                orbit_x = math.cos(orbit) * 250 + 300
                orbit_y = -math.sin(orbit) * 250 + 300
                #Orbit anpassen
                orbit =orbit + 0.002
                screen.fill(black)
                pygame.draw.circle(screen, white, center, 250, 2)
                pygame.draw.line(screen, white, center, (300, 50))
                # Planet erstellen
                screen.blit(picture,(250,250))                
                screen.blit(font.render((str(h)+"m"), False, white),(310, 150))
                #Zufällige Bilder für Himmelskörper, die den Planet umkreisen
                if randomvar >= 900 and randomvar <=1000:#ISS
                    picture2 = pygame.image.load("ISS.png")
                    picture2 = pygame.transform.scale(picture2,(68,40))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=800 and randomvar <900:#Rosetta
                    picture2 = pygame.image.load("Rosetta.png")
                    picture2 = pygame.transform.scale(picture2,(57,27))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=700 and randomvar <800:#Mond
                    picture2 = pygame.image.load("Mond.png")
                    picture2 = pygame.transform.scale(picture2,(50,50))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=600 and randomvar <700:#Mir
                    picture2 = pygame.image.load("Mir.png")
                    picture2 = pygame.transform.scale(picture2,(70,40))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=500 and randomvar <600:#Hubble
                    picture2 = pygame.image.load("Hubble.png")
                    picture2 = pygame.transform.scale(picture2,(77,56))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+26, orbit_y+26))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+26, orbit_y+46))
                elif randomvar >=60 and randomvar <100:#Sentinel
                    picture2 = pygame.image.load("Sentinel.png")
                    picture2 = pygame.transform.scale(picture2,(70,39))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=0 and randomvar <10:#Enterprise
                    picture2 = pygame.image.load("Enterprise.png")
                    picture2 = pygame.transform.scale(picture2,(76,44))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+27, orbit_y+27))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+27, orbit_y+47))
                elif randomvar >=10 and randomvar <20:#Todesstern
                    picture2 = pygame.image.load("DeathStar.png")
                    picture2 = pygame.transform.scale(picture2,(78,60))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=400 and randomvar <500:#Apollo13
                    picture2 = pygame.image.load("Apollo13.png")
                    picture2 = pygame.transform.scale(picture2,(70,70))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=300 and randomvar <400:#CrewDragon
                    picture2 = pygame.image.load("CrewDragon.png")
                    picture2 = pygame.transform.scale(picture2,(80,50))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=200 and randomvar <300:#Orion
                    picture2 = pygame.image.load("Orion.png")
                    picture2 = pygame.transform.scale(picture2,(76,44))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=100 and randomvar <200:
                    picture2 = pygame.image.load("Satelite.png")
                    picture2 = pygame.transform.scale(picture2,(70,42))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))
                elif randomvar >=20 and randomvar <60:#Astronaut
                    picture2 = pygame.image.load("Astronaut.png")
                    picture2 = pygame.transform.scale(picture2,(72,54))
                    screen.blit(picture2,(int(orbit_x-34), int(orbit_y-20)))
                    screen.blit(font.render((str(v)+"m/s"), False, white),(orbit_x+20, orbit_y+20))
                    screen.blit(font.render((str(T)+"s"), False, white),(orbit_x+20, orbit_y+40))

                
                
                
                pygame.display.flip()
                clock.tick(60)

            pygame.quit()#Pygame loop Ende
            
    runtime = (datetime.datetime.now() - begin_time)
    if Transitberechnung == False:
        timedifference = runtime - calctime
    elif Transitberechnung == True:
        calctime = "null"
        timedifference = "null"
    if outputruntime == True:
        print("Zeit für Berechnung: " + str(calctime))
        print("Laufzeit Programm + Animation: " + str(runtime))
        print("Zeitdifferenz: " + str(timedifference))
    #Daten der Berechnung in Nutzerdaten Liste schreiben
    if collectuserdata == True:
        currentuserdata = str("Berechnung gestartet: "+ "Planet: "+ str(planet)+"; gegebene Größe: "+str(number)+"; manueller Input: "+str(manualInput)+"; Transitrechnung: "+str(Transitberechnung)+"; Output in Konsole: "+str(consoleOutput)+"; Ausgabe Zufallsvariable: "+str(outputrandomvar)+"; Laufzeit Berechnung: "+str(calctime)+"; Laufzeit Animation: "+str(timedifference)+"; Laufzeit gesamt: "+str(runtime))
        userdata.append([datetime.datetime.now(), currentuserdata])
        logdata(currentuserdata)
    #Ende Prozedur 'Berechne' Button

manualInputExitCode = 0

#Button für manuellen Input
def togglemanualInput():
    #Prüfen, ob Funktion remote deaktiviert wurde
    if disable_manuellerInput == True:
        messagebox.showerror("remote Steuerung","Diese Funktion wurde remote deaktiviert.")
        print("Fehlercode: 14")
        return()
    global manualInput
    global Minput
    global Rinput
    global Label7
    global Label8
    global Label9
    global Label10
    global Label4
    global manualInputExitCode
    #Umschaltung von Ja auf Nein
    if manualInput == True:
        manualInput = False
        Label7.destroy()
        Label8=tk.Label(master, text = "Nein",font=size, bg="red")
        Label8.grid(row=6, column=1) 
        ExitCodemanualInput = 1
        Rinput.destroy()
        Minput.destroy()
        Label9.destroy()
        Label10.destroy()
        manualInputExitCode =1  
    #Umschaltung von Nein auf Ja
    elif manualInput == False:
        manualInput = True
        #Label4.destroy()
        Label7=tk.Label(master, text = "  Ja  ",font=size, bg="green")
        Label7.grid(row=6, column=1)
        Label9 = tk.Label(master,text="Masse(kg)",font=size,bg=color)
        Label9.grid(row=0,column=2)
        Label10 = tk.Label(master, text="Radius(m)",font=size,bg=color)
        Label10.grid(row=1,column=2)
        Minput=tk.Entry(master)
        Minput.grid(row=0, column=3)
        Rinput=tk.Entry(master)
        Rinput.grid(row=1, column=3)
        Label4.destroy()
        if manualInputExitCode == 1:
            Label8.destroy()
    
    #Änderung der Einstellung in Nutzerdaten Liste schreiben
    if collectuserdata == True:
        currentuserdata=str("Manual Input verändert, neuer Zustand: " + str(manualInput))
        userdata.append([datetime.datetime.now(), currentuserdata])
        logdata(currentuserdata)

TransitrechnungExitCode = 0 

#Transitberechnung
def Transitrechnung():
    #Prüfen, ob Funktion remote deaktiviert wurde
    if disable_Transitrechnung == True:
        messagebox.showerror("remote Steuerung","Diese Funktion wurde remote deaktiviert.")
        print("Fehlercode: 14")
        return()
    global Transitberechnung
    global planetzwei
    global Label11
    global TransitrechnungExitCode
    global Label6
    global Label12
    #Umschaltung von Ja auf Nein 
    if Transitberechnung == True:
        Transitberechnung = False
        Label12 = tk.Label(master, text = "Nein",font=size, bg="red")
        Label12.grid(row=7, column=1)
        Label11.destroy()
        planetzwei.destroy()
        TransitrechnungExitCode = 1
    #Umschaltung von Nein auf Ja     
    elif Transitberechnung == False:
        Transitberechnung = True
        tk.Label(master, text = " Ja   ",font=size, bg="green").grid(row=7, column=1)
        Label11 = tk.Label(master, text="Planet 2: ",font=size,bg=color)
        Label11.grid(row=6,column=2)
        planetzwei=tk.Entry(master)
        planetzwei.grid(row=6, column=3)
        Label6.destroy()
        if TransitrechnungExitCode == 1:
            Label12.destroy()

    #Änderung der Einstellung in Nutzerdaten Liste schreiben
    if collectuserdata == True:
        currentuserdata=str("Transitrechnung aktiviert / deaktiviert, neuer Zustand:" + str(Transitberechnung))
        userdata.append([datetime.datetime.now(), currentuserdata])
        logdata(currentuserdata)
        
#Menschen im All
def MenschenimAll():
    #Prüfen, ob Funktion remote deaktiviert wurde
    if disable_MenschenimAll == True:
        messagebox.showerror("remote Steuerung","Diese Funktion wurde rempote deaktiviert.")
        print("Fehlercode: 14")
        return()
    updatestatistics("Menschen_im_All")
    #Setup für Dropbox
    options = tk.StringVar(master)
    options.set("Astronaut wählen")

    url = "http://api.open-notify.org/astros.json"
    try:
        response = urllib.request.urlopen(url)
        result = json.loads(response.read())
    except:
        messagebox.showerror("Ein Fehler ist aufgetreten.","Ein Fehler ist aufgetreten und die Verbindung wurde unterbrochen")
        #Fehler in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("ERROR: network error (MenschenimAll)")
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 21")
        return()


    file = open("Menchen_im_All.txt", "w")#Textdokument öffnen / erstellen
    file.write("Aktuell sind "+str(result["number"])+" Menschen im All: \n\n")
    astronaut_count = result["number"]
    #Menschen im All aus API importieren
    people = result["people"]
    for p in people:
        file.write(p['name']  +": "+ p['craft'] + "\n")#Menschen im All in Textdokument schreiben(Konsole nicht unbedingt vorhanden und Label keine konsistente Option)
    file.close()
    webbrowser.open("Menchen_im_All.txt")#Textdokument öffnen
    if result["number"] < 0:
        messagebox.showerror("Ein Fehler ist aufgetreten", "Ein Fehler ist aufgetreten")
        print("Fehlercode: 8")
    
    global consoleOutput
    if consoleOutput == True:
        print("Aktuell sind "+str(result["number"])+" Menschen im All: \n")
        for p in people:
            print(p['name']  +": "+ p['craft'])


    astronaut_list = people

    global AstronautInput

    #für die Anzahl Astronauten 1-20 die Dropbox erstellen, uneleganten Lösung aber mir ist keine bessere bekannt, da man keine Liste an die Funtion OptionMenu übergeben kann
    if astronaut_count <= 0:#Wenn Astronautenzahl 0 oder weniger ist, Fehlermeldung ausgeben
        messagebox.showerror("Ein Fehler ist aufgetreten","Ein Fehler ist aufgetreten")
        AstronautInput =tk.OptionMenu(master, options,"Ein Fehler ist aufgetreten" )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")        
    
    
    elif astronaut_count == 1:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")       

    elif astronaut_count == 2:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")     

    elif astronaut_count == 3:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 4:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 5:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 6:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 7:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 8:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 9:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 10:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 11:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 12:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 13:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 14:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        element14 = astronaut_list[13]
        astronaut14 = str(element14["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13,astronaut14 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 15:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        element14 = astronaut_list[13]
        astronaut14 = str(element14["name"])
        element15 = astronaut_list[14]
        astronaut15 = str(element15["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13,astronaut14,astronaut15 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 16:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        element14 = astronaut_list[13]
        astronaut14 = str(element14["name"])
        element15 = astronaut_list[14]
        astronaut15 = str(element15["name"])
        element16 = astronaut_list[15]
        astronaut16 = str(element16["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13,astronaut14,astronaut15,astronaut16 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 17:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        element14 = astronaut_list[13]
        astronaut14 = str(element14["name"])
        element15 = astronaut_list[14]
        astronaut15 = str(element15["name"])
        element16 = astronaut_list[15]
        astronaut16 = str(element16["name"])
        element17 = astronaut_list[16]
        astronaut17 = str(element17["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13,astronaut14,astronaut15,astronaut16,astronaut17 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 18:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        element14 = astronaut_list[13]
        astronaut14 = str(element14["name"])
        element15 = astronaut_list[14]
        astronaut15 = str(element15["name"])
        element16 = astronaut_list[15]
        astronaut16 = str(element16["name"])
        element17 = astronaut_list[16]
        astronaut17 = str(element17["name"])
        element18 = astronaut_list[17]
        astronaut18 = str(element18["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13,astronaut14,astronaut15,astronaut16,astronaut17,astronaut18 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 19:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        element14 = astronaut_list[13]
        astronaut14 = str(element14["name"])
        element15 = astronaut_list[14]
        astronaut15 = str(element15["name"])
        element16 = astronaut_list[15]
        astronaut16 = str(element16["name"])
        element17 = astronaut_list[16]
        astronaut17 = str(element17["name"])
        element18 = astronaut_list[17]
        astronaut18 = str(element18["name"])
        element19 = astronaut_list[18]
        astronaut19 = str(element19["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13,astronaut14,astronaut15,astronaut16,astronaut17,astronaut18,astronaut19 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count == 20:
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        element14 = astronaut_list[13]
        astronaut14 = str(element14["name"])
        element15 = astronaut_list[14]
        astronaut15 = str(element15["name"])
        element16 = astronaut_list[15]
        astronaut16 = str(element16["name"])
        element17 = astronaut_list[16]
        astronaut17 = str(element17["name"])
        element18 = astronaut_list[17]
        astronaut18 = str(element18["name"])
        element19 = astronaut_list[18]
        astronaut19 = str(element19["name"])
        element20 = astronaut_list[19]
        astronaut20 = str(element20["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13,astronaut14,astronaut15,astronaut16,astronaut17,astronaut18,astronaut19,astronaut20 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")

    elif astronaut_count > 20:
        messagebox.showinfo("Info","Es können aus technischen Gründen nur die ersten 20 Astronauten angezeigt werden.")
        element1 = astronaut_list[0]
        astronaut1 = str(element1["name"])
        element2 = astronaut_list[1]
        astronaut2 = str(element2["name"])
        element3 = astronaut_list[2]
        astronaut3 = str(element3["name"])
        element4 = astronaut_list[3]
        astronaut4 = str(element4["name"])
        element5 = astronaut_list[4]
        astronaut5 = str(element5["name"])
        element6 = astronaut_list[5]
        astronaut6 = str(element6["name"])
        element7 = astronaut_list[6]
        astronaut7 = str(element7["name"])
        element8 = astronaut_list[7]
        astronaut8 = str(element8["name"])
        element9 = astronaut_list[8]
        astronaut9 = str(element9["name"])
        element10 = astronaut_list[9]
        astronaut10 = str(element10["name"])
        element11 = astronaut_list[10]
        astronaut11 = str(element11["name"])
        element12 = astronaut_list[11]
        astronaut12 = str(element12["name"])
        element13 = astronaut_list[12]
        astronaut13 = str(element13["name"])
        element14 = astronaut_list[13]
        astronaut14 = str(element14["name"])
        element15 = astronaut_list[14]
        astronaut15 = str(element15["name"])
        element16 = astronaut_list[15]
        astronaut16 = str(element16["name"])
        element17 = astronaut_list[16]
        astronaut17 = str(element17["name"])
        element18 = astronaut_list[17]
        astronaut18 = str(element18["name"])
        element19 = astronaut_list[18]
        astronaut19 = str(element19["name"])
        element20 = astronaut_list[19]
        astronaut20 = str(element20["name"])
        AstronautInput =tk.OptionMenu(master, options,astronaut1, astronaut2, astronaut3,astronaut4,astronaut5,astronaut6,astronaut7,astronaut8,astronaut9,astronaut10,astronaut11,astronaut12,astronaut13,astronaut14,astronaut15,astronaut16,astronaut17,astronaut18,astronaut19,astronaut20 )
        AstronautInput.grid(row=7,column=4)
        AstronautInput.config(bg="#FF6F61")


    #Funktion zum ersetzen der Leerzeichen durch _
    def replace_spaces(string):
        return string.replace(" ", "_")

    #Wikipediaseite öffnen
    def openwikipage():
        astronaut_choice = (options.get())
        if astronaut_choice == "Astronaut wählen":#überprüfen, ob überhaupt eine Option ausgewählt wurde
            messagebox.showerror("Ein Fehler ist aufgetreten","Bitte wählen sie einen Astronaut aus.")
            print("Fehlercode: 11")
            return()
        else:
            request_choice = replace_spaces(astronaut_choice)

            chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

            #Versuchen, ob deutsche Seite existiert, wenn nicht englischsprachige öffnen (aktuell nicht funktionsfähig)
            try:
                language = "de"
                finished_url = str("https://"+language+".wikipedia.org/wiki/"+request_choice)
                webbrowser.get(chrome_path).open_new(finished_url)
                
            except:
                messagebox.showinfo("Chrome nicht installiert","Es wurde keine Chrome Installation gefunden. Link wird in Standardbrowser geöffnet...")
                language = "de"
                finished_url = str("https://"+language+".wikipedia.org/wiki/"+request_choice)
                webbrowser.open(finished_url)
                
            if collectuserdata == True:
                currentuserdata = str("Wikipedia Seite wurde aufgerufen für:"+str(request_choice))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)


    #Button für die Bestätigung der Dropdown-Menü Eingabe
    global button12
    button12 = tk.Button(text="Wikipedia-Seite öffnen",command=openwikipage,font=size,bg = buttoncolor)
    button12.grid(row=6,column=4)
    global MenschenimAll_ExitCode
    MenschenimAll_ExitCode = 1
    if collectuserdata == True:
        currentuserdata=str("Menschen im All aktiviert")
        userdata.append([datetime.datetime.now(), currentuserdata])
        logdata(currentuserdata)

#ISS-Position
def isslocation():
    #Prüfen, ob Funktion remote deaktiviert wurde
    if disable_ISSPosition == True:
        messagebox.showerror("remote Steuerung","Diese Funktion wurde remote deaktiviert.")
        print("Fehlercode: 14")
        return()
    updatestatistics("ISS_Position")
    global MenschenimAll_ExitCode
    if MenschenimAll_ExitCode == 1:
        button12.destroy()
        AstronautInput.destroy()
        MenschenimAll_ExitCode = 0
    begin_time = datetime.datetime.now()
    #Höhe und Breite der Karte
    height= 700
    width=1300
    global outputposition
    #Karte der Erde laden
    picture = pygame.image.load("map2.png")
    picture = pygame.transform.scale(picture,(width,height))
    #Bild der ISS laden
    iss = pygame.image.load("iss_final.png")
    iss = pygame.transform.scale(iss,(40,40))
        
    pygame.init()#Pygame loop Start
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('ISS-Tracker')
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf",15)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        
        screen.blit(picture,(0,0))
        #Position der ISS von API importieren
        url = "http://api.open-notify.org/iss-now.json"
        try:
            response = urllib.request.urlopen(url)
            result = json.loads(response.read())
        except:
            messagebox.showerror("Ein Fehler ist aufgetreten.","Ein Fehler ist aufgetreten und die Verbindung wurde unterbrochen")
            #Fehler in Nutzerdaten Liste schreiben
            if collectuserdata == True:
                currentuserdata=str("ERROR: network error (ISS Position)")
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)
            print("Fehlercode: 22")
            return()


        #Ergebnis filtern       
        location = result["iss_position"]
        lat = location['latitude']
        lon = location['longitude']
        lat = float(lat)
        lon = float(lon)
        #Position zu Konsole ausgeben
        if outputposition == True:
            print("Breite: " +str(lat))
            print("Länge: " + str(lon))
            print("-----------------")        
        #Umrechnung der Länge und Breite in Pixel
        latneu = ((((lat+90)/180)*height)*(-1))+height
        lonneu= ((lon+180)/360)*width
        #ISS auf Karte anzeigen
        screen.blit(iss,(lonneu-20,latneu-20))
        
        clock.tick(5)
        pygame.display.flip()

    pygame.quit()#Pygame loop Ende
    runtime = (datetime.datetime.now() - begin_time)
    if outputruntime == True:
        print("Laufzeit: " + str(runtime))
    #Aktion in Nutzerdaten Liste schreiben
    if collectuserdata == True:
        currentuserdata=str("ISS-Position wurde ausgeführt"+"; Laufzeit gesamt: "+str(runtime))
        userdata.append([datetime.datetime.now(), currentuserdata])
        logdata(currentuserdata)
            
#Raketenstarts
def rocketlaunches():
    #Prüfen, ob Funktion remote deaktiviert wurde
    if disable_Raketenstarts == True:
        messagebox.showerror("remote Steuerung","Diese Funktion wurde remote deaktiviert.")
        print("Fehlercode: 14")
        return()
    updatestatistics("Raketenstarts")
    global MenschenimAll_ExitCode
    if MenschenimAll_ExitCode == 1:
        button12.destroy()
        AstronautInput.destroy()
        MenschenimAll_ExitCode = 0
    #Data by RocketLaunch.Live
    launches = 5 
    url = str("https://fdo.rocketlaunch.live/json/launches/next/"+str(launches))

    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    resultnew = result["result"]
    i = 1

    if len(resultnew) < 0:
        #Fehler in Liste mit Nutzerdaten schreiben / loggen
        if collectuserdata == True:
            currentuserdata=str("ERROR: bad result - result list empty (Raketenstarts) ")
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)
        print("Fehlercode: 12")


    #Antwort (als Liste) mit loop durchsuchen
    for x in resultnew:
            #erster Start
            if i == 1:
                launch_id_1 = x["id"]
                name_1 = x["name"]
                provider_1 = x["provider"]
                provider_name_1 = provider_1["name"]
                vehicle_1 = x["vehicle"]
                vehicle_name_1 = vehicle_1["name"]
                pad_1 = x["pad"]
                location_1 = pad_1["location"]
                location_name_1 = location_1["name"]
                launch_description_1 = x["launch_description"]
                win_open_1 = x["win_open"]
                quicktext1 = str(x["quicktext"])
                link1 = quicktext1[(quicktext1.find("https")):(quicktext1.find("for")-1)]

            #zweiter Start    
            elif i == 2:
                launch_id_2 = x["id"]
                name_2 = x["name"]
                provider_2 = x["provider"]
                provider_name_2 = provider_2["name"]
                vehicle_2 = x["vehicle"]
                vehicle_name_2 = vehicle_2["name"]
                pad_2 = x["pad"]
                location_2 = pad_2["location"]
                location_name_2 = location_2["name"]
                launch_description_2 = x["launch_description"]
                win_open_2 = x["win_open"]
                quicktext2 = str(x["quicktext"])
                link2 = quicktext2[(quicktext2.find("https")):(quicktext2.find("for")-1)]

            #dritter Start    
            elif i == 3:
                launch_id_3 = x["id"]
                name_3 = x["name"]
                provider_3 = x["provider"]
                provider_name_3 = provider_3["name"]
                vehicle_3 = x["vehicle"]
                vehicle_name_3 = vehicle_3["name"]
                pad_3 = x["pad"]
                location_3 = pad_3["location"]
                location_name_3 = location_3["name"]
                launch_description_3 = x["launch_description"]
                win_open_3 = x["win_open"]
                quicktext3 = str(x["quicktext"])
                link3 = quicktext3[(quicktext3.find("https")):(quicktext3.find("for")-1)]

            #vierter Start    
            elif i == 4:
                launch_id_4 = x["id"]
                name_4 = x["name"]
                provider_4 = x["provider"]
                provider_name_4 = provider_4["name"]
                vehicle_4 = x["vehicle"]
                vehicle_name_4 = vehicle_4["name"]
                pad_4 = x["pad"]
                location_4 = pad_4["location"]
                location_name_4 = location_4["name"]
                launch_description_4 = x["launch_description"]
                win_open_4 = x["win_open"]
                quicktext4 = str(x["quicktext"])
                link4 = quicktext4[(quicktext4.find("https")):(quicktext4.find("for")-1)]

            #fünfter Start
            elif i == 5:
                launch_id_5 = x["id"]
                name_5 = x["name"]
                provider_5 = x["provider"]
                provider_name_5 = provider_5["name"]
                vehicle_5 = x["vehicle"]
                vehicle_name_5 = vehicle_5["name"]
                pad_5 = x["pad"]
                location_5 = pad_5["location"]
                location_name_5 = location_5["name"]
                launch_description_5 = x["launch_description"]
                win_open_5 = x["win_open"]
                quicktext5 = str(x["quicktext"])
                link5 = quicktext5[(quicktext5.find("https")):(quicktext5.find("for")-1)]

            i = i+1
    i = 1
    
    #Ergebnisse in ein Textdokument schreiben
    file = open("Raketenstarts.txt","w")
    file.write("Die nächsten 5 Raketenstarts: \n")
    file.write("(Daten von RocketLaunch.Live) \n\n")
    
    #erster Start
    file.write("Start 1 \n")
    file.write("Name der Mission: " + str(name_1) + "\n")
    file.write("Zeitfenster: "+str(win_open_1)+"\n")
    file.write("Provider: "+str(provider_name_1)+"\n")
    file.write("Rakete: "+str(vehicle_name_1)+"\n")
    file.write("Startort: "+str(location_name_1)+"\n")
    file.write("Beschreibung: "+str(launch_description_1)+"\n")
    file.write("Link zu Live Übertragung / mehr Infos: "+str(link1)+"\n\n")
    file.write("---------------------------------------------------------------------------------------------------------------------------------------------------- \n\n")
    
    #zweiter Start
    file.write("Start 2 \n")
    file.write("Name der Mission: " + str(name_2) + "\n")
    file.write("Zeitfenster: "+str(win_open_2)+"\n")
    file.write("Provider: "+str(provider_name_2)+"\n")
    file.write("Rakete: "+str(vehicle_name_2)+"\n")
    file.write("Startort: "+str(location_name_2)+"\n")
    file.write("Beschreibung: "+str(launch_description_2)+"\n")
    file.write("Link zu Live Übertragung / mehr Infos: "+str(link2)+"\n\n")    
    file.write("---------------------------------------------------------------------------------------------------------------------------------------------------- \n\n")
    
    #dritter Start
    file.write("Start 3 \n")
    file.write("Name der Mission: " + str(name_3) + "\n")
    file.write("Zeitfenster: "+str(win_open_3)+"\n")
    file.write("Provider: "+str(provider_name_3)+"\n")
    file.write("Rakete: "+str(vehicle_name_3)+"\n")
    file.write("Startort: "+str(location_name_3)+"\n")
    file.write("Beschreibung: "+str(launch_description_3)+"\n") 
    file.write("Link zu Live Übertragung / mehr Infos: "+str(link3)+"\n\n")
    file.write("---------------------------------------------------------------------------------------------------------------------------------------------------- \n\n")
    
    #vierter Start
    file.write("Start 4 \n")
    file.write("Name der Mission: " + str(name_4) + "\n")
    file.write("Zeitfenster: "+str(win_open_4)+"\n")
    file.write("Provider: "+str(provider_name_4)+"\n")
    file.write("Rakete: "+str(vehicle_name_4)+"\n")
    file.write("Startort: "+str(location_name_4)+"\n")
    file.write("Beschreibung: "+str(launch_description_4)+"\n")
    file.write("Link zu Live Übertragung / mehr Infos: "+str(link4)+"\n\n")    
    file.write("---------------------------------------------------------------------------------------------------------------------------------------------------- \n\n")
    
    #fünfter Start
    file.write("Start 5 \n")
    file.write("Name der Mission: " + str(name_5) + "\n")
    file.write("Zeitfenster: "+str(win_open_5)+"\n")
    file.write("Provider: "+str(provider_name_5)+"\n")
    file.write("Rakete: "+str(vehicle_name_5)+"\n")
    file.write("Startort: "+str(location_name_5)+"\n")
    file.write("Beschreibung: "+str(launch_description_5)+"\n")    
    file.write("Link zu Live Übertragung / mehr Infos: "+str(link5)+"\n")


    
    file.close()
    webbrowser.open("Raketenstarts.txt")#Textdokument öffnen

    #Ausgabe in Konsole
    global consoleOutput
    if consoleOutput == True:
        print("\n\n")
        print("Die nächsten 5 Raketenstarts: ")
        print("(Daten von RocketLaunch.Live) \n")
        
        #erster Start
        print("Start 1 ")
        print("Name der Mission: " + str(name_1))
        print("Zeitfenster: "+str(win_open_1))
        print("Provider: "+str(provider_name_1))
        print("Rakete: "+str(vehicle_name_1))
        print("Startort: "+str(location_name_1))
        print("Beschreibung: "+str(launch_description_1))
        print("Link zu Live Übertragung / mehr Infos: "+str(link1)+"\n")
        print("---------------------------------------------------------------------------------------------------------------------------------------------------- \n")
        
        #zweiter Start
        print("Start 2 ")
        print("Name der Mission: " + str(name_2))
        print("Zeitfenster: "+str(win_open_2))
        print("Provider: "+str(provider_name_2))
        print("Rakete: "+str(vehicle_name_2))
        print("Startort: "+str(location_name_2))
        print("Beschreibung: "+str(launch_description_2))
        print("Link zu Live Übertragung / mehr Infos: "+str(link2)+"\n")    
        print("---------------------------------------------------------------------------------------------------------------------------------------------------- \n")
        
        #dritter Start
        print("Start 3 ")
        print("Name der Mission: " + str(name_3))
        print("Zeitfenster: "+str(win_open_3))
        print("Provider: "+str(provider_name_3))
        print("Rakete: "+str(vehicle_name_3))
        print("Startort: "+str(location_name_3))
        print("Beschreibung: "+str(launch_description_3)) 
        print("Link zu Live Übertragung / mehr Infos: "+str(link3)+"\n")
        print("---------------------------------------------------------------------------------------------------------------------------------------------------- \n")
        
        #vierter Start
        print("Start 4 ")
        print("Name der Mission: " + str(name_4))
        print("Zeitfenster: "+str(win_open_4))
        print("Provider: "+str(provider_name_4))
        print("Rakete: "+str(vehicle_name_4))
        print("Startort: "+str(location_name_4))
        print("Beschreibung: "+str(launch_description_4))
        print("Link zu Live Übertragung / mehr Infos: "+str(link4)+"\n")    
        print("---------------------------------------------------------------------------------------------------------------------------------------------------- \n")
        
        #fünfter Start
        print("Start 5 ")
        print("Name der Mission: " + str(name_5))
        print("Zeitfenster: "+str(win_open_5))
        print("Provider: "+str(provider_name_5))
        print("Rakete: "+str(vehicle_name_5))
        print("Startort: "+str(location_name_5))
        print("Beschreibung: "+str(launch_description_5))    
        print("Link zu Live Übertragung / mehr Infos: "+str(link5))




    #Aktion in Nutzerdaten Liste schreiben
    if collectuserdata == True:
        currentuserdata=str("Raketenstarts wurde ausgeführt")
        userdata.append([datetime.datetime.now(), currentuserdata])
        logdata(currentuserdata)
    
#mehr FUnktionen GUI
def morefunctions():
    morefunctions = tk.Toplevel(master)
    morefunctions.geometry("1200x700")
    morefunctions.title("weitere Funktionen")
    #Hintergrundbild 
    path1 = "morefunctions.gif"
    img1 = ImageTk.PhotoImage(Image.open(path1))
    background_label = tk.Label(morefunctions, image=img1)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


    if collectuserdata == True:
        currentuserdata=str("Mehr Funktionen GUI wurde geöffnet")
        userdata.append([datetime.datetime.now(), currentuserdata])
        logdata(currentuserdata)


    #GUI für NASA API Funktionen
    def startnasaapigui():
        nasaapigui = tk.Toplevel(master)
        nasaapigui.geometry("1200x700")
        nasaapigui.title("NASA API")
        #Hintergrundbild 
        path1 = "NASA.gif"
        img1 = ImageTk.PhotoImage(Image.open(path1))
        background_label = tk.Label(nasaapigui, image=img1)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #Erstellung Label für 'Breite'
        Label2=tk.Label(nasaapigui, text=" Breite: ",font=size, bg=color)
        Label2.grid(row=1,column=0)

        #Entry field für latitude
        lat_in=tk.Entry(nasaapigui)
        lat_in.grid(row=2, column=0)


        #Erstellung Label für 'Länge'
        Label1=tk.Label(nasaapigui, text=" Länge: ",font=size, bg=color)
        Label1.grid(row=3,column=0)

        #Entry field für longitude
        lon_in=tk.Entry(nasaapigui)
        lon_in.grid(row=4, column=0)


        #Erstellung Label für 'Datum'
        Label1=tk.Label(nasaapigui, text=" Datum(Jahr-Tag-Monat): ",font=size, bg=color)
        Label1.grid(row=5,column=0)

        #Entry field für date
        date_in=tk.Entry(nasaapigui)
        date_in.grid(row=6, column=0)



        #Erstellung Label für 'Ausdehnung'
        Label1=tk.Label(nasaapigui, text=" Ausdehnung(Grad): ",font=size, bg=color)
        Label1.grid(row=7,column=0)

        #Entry field für dim
        dim_in=tk.Entry(nasaapigui)
        dim_in.grid(row=8, column=0)



        #Aktion loggen
        if collectuserdata == True:
            currentuserdata=str("NASA API GUI wurde gestartet.")
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)

        zeilentrennung = True

        #Funktion zum öffnen und anzeigen von Astronomy Picture of the Day:
        def getAPOD():

            if collectuserdata == True:
                currentuserdata=str("Astronomy Picture of the Day wurde gestartet.")
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)

            key = "UTAfuhvvHGt2rgCAmuwdxJ9BAqtP3jncO5EZ5xy4"#NASA API key
            url = "https://api.nasa.gov/planetary/apod?api_key=" + key #URL bauen

            try:
                response = urllib.request.urlopen(url)
            except urllib.error.HTTPError: 
                print("Ein Fehler ist aufgetreten, bitte versuchen Sie es erneut.")
                print("Fehlercode: 17")
                messagebox.showerror("Ein Fehler ist aufgetreten","Ein Fehler ist aufgetreten, bitte versuchen Sie es erneut.")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: NETWORK ERROR (getAPOD)")
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                return()


            result = json.loads(response.read())


            explanation = result["explanation"]
            title = result["title"]
            picture_url = result["url"]



            #Titel und Beschreibung in Textdokument schreiben
            with open("Beschreibung.txt","w") as description:
                description.write(title+"\n\n")

                if zeilentrennung == True:#harte Zeilentrennung
                    segments = round((len(explanation)/71))#Prüfen, Wie viele Zeilen es werden müssen
                    for i in range(0,segments):#Zeile für Zeile in Textdokument schreiben
                        description.write((explanation[i*71:(i+1)*71]+"\n"))

                    description.write(explanation[segments*71:])#Rest in Dokument schreiben
                elif zeilentrennung == False:
                    description.write(explanation)

            #Metadaten in jpg file schreiben
            with open("APOD.jpg", "wb") as file:
                try:
                    response = requests.get(picture_url)
                except:
                    print("Ein Fehler ist aufgetreten, bitte versuchen Sie es erneut.")
                    print("Fehlercode: 18")
                    messagebox.showerror("Ein Fehler ist aufgetreten","Ein Fehler ist aufgetreten, bitte versuchen Sie es erneut.")
                    #Fehler in Nutzerdaten Liste schreiben
                    if collectuserdata == True:
                        currentuserdata=str("ERROR: NETWORK ERROR (getAPOD)")
                        userdata.append([datetime.datetime.now(), currentuserdata])
                        logdata(currentuserdata)
                    return()
                file.write(response.content)

            print("Bild erfolgreich heruntergeladen.")

            os.system(os.path.join("APOD.jpg"))
            webbrowser.open("Beschreibung.txt")




        def getspaceobjects():

            if collectuserdata == True:
                currentuserdata=str("TLE Daten für Sateliten wurde gestartet.")
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)

            url = "https://tle.ivanstanojevic.me/api/tle/"

            try:
                request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})#Header auf Mozilla setzen, request wird ansonsten automatisch abgelehnt (Anfrage als menschlche Anfrage ausgeben)
                response = urllib.request.urlopen(request).read()
            except:
                messagebox.showerror("Ein Fehler ist aufgetreten.","Ein Fehler ist aufgetreten und die Verbindung wurde unterbrochen")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: network error (2 line TLE data)")
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 23")
                return()

            result_json = response.decode('utf8').replace("'", '"')#Antowrt in json umwandeln, Original ist byre Objekt

            result = json.loads(result_json)

            elements= result["member"]

            names = []#Liste für die Namen
            ids = [] #Liste für die IDs

            combined_data = []#Liste für kombinierte Daten

            for x in elements:
                #print(x["name"])
                names.append(x["name"])
                ids.append(x["satelliteId"])
                combined_data.append("Name: "+str(x["name"]) + " ID: "+str(x["satelliteId"]) + " line1: "+str(x["line1"])+" line2: "+str(x["line2"]))

            with open("satellitedata.txt","w") as file:
                file.write("2 Line Daten für LEO Sateliten: \n\n")
                for x in combined_data:
                    file.write(x+"\n")
            
            webbrowser.open("satellitedata.txt")


        def getpospicture(lon,lat,date,dim):#lon = Breite, lat = Länge, date = Zeitpunkt, dim = Größe des Bildes in Grad
            key = "UTAfuhvvHGt2rgCAmuwdxJ9BAqtP3jncO5EZ5xy4"#NASA API key

            url = "https://api.nasa.gov/planetary/earth/imagery?lon="+str(lon)+"&lat="+str(lat)+"&date="+str(date)+"&dim="+str(dim)+"&api_key="+str(key)


            #Metadaten in jpg file schreiben
            with open("location_image.jpg", "wb") as file:
                try:
                    response = requests.get(url)
                except:
                    print("Ein Fehler ist aufgetreten, bitte versuchen Sie es erneut.")
                    messagebox.showerror("Ein Fehler ist aufgetreten","Ein Fahler ist aufgetreten und das Bild konnte nicht geladen werden")
                    #Fehler in Nutzerdaten Liste schreiben
                    if collectuserdata == True:
                        currentuserdata=str("ERROR: network error (Satellitenbilder) - response="+str(response.content))
                        userdata.append([datetime.datetime.now(), currentuserdata])
                        logdata(currentuserdata)
                    print("Fehlercode: 20")
                    return()
                file.write(response.content)

            #Prüfen, ob die metadaten länger als 500 sind, wenn nicht ist höchstwahrscheinlich ein Fehler aufgetreten und die angefragten Daten sind nicht verfügbar
            if len(response.content) < 500:
                print("Ein Fehler ist aufgetreten.")
                messagebox.showerror("Ein Fehler ist aufgetreten","Ein Fahler ist aufgetreten und das Bild konnte nicht geladen werden")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: network error (Satellitenbilder) - response="+str(response.content))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 20")
                return()

            else:
                print("Bild erfolgreich heruntergeladen.")

            os.system(os.path.join("location_image.jpg"))


        def getpictureforpos():
            #Daten aus Input-Feldern importieren
            lon_in2 = lon_in.get()
            lat_in2 = lat_in.get()
            date_in2 = date_in.get()
            dim_in2 = dim_in.get()

            if collectuserdata == True:
                currentuserdata=str("Satellitenbild abgerufen, lon="+str(lon_in2)+" ,lat="+str(lat_in2)+" ,date="+str(date_in2)+" ,dim="+str(dim_in2))
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)


            #Security-Checks

            word6 = lon_in2
            security_check(lon_in2,"Satellitenbilder")
            security_check(lat_in2,"Satellitenbilder")
            security_check(date_in2,"Satellitenbilder")
            security_check(dim_in2,"Satellitenbilder")






            #Prüfen, ob Eingabewerte in float umgewandelt werden können
            try:
                lon = float(lon_in2)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein!")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Satellite Pictures) - value="+str(lon_in2))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 19")
                return()

            #Prüfen, ob Eingabewerte in float umgewandelt werden können
            try:
                lat = float(lat_in2)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein!")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Satellite Pictures) - value="+str(lat_in2))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 19")
                return()

            #Prüfen, ob Eingabewerte in float umgewandelt werden können
            try:
                dim = float(dim_in2)
            except ValueError:
                messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben sie einen zulässigen Wert ein!")
                #Fehler in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("ERROR: invalid value (Satellite Pictures) - value="+str(dim_in2))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)
                print("Fehlercode: 19")
                return()

            date = date_in2
            getpospicture(lon,lat,date,dim)



        #'NASA Astronomy Picture of the Day'-Button
        button = tk.Button(nasaapigui, text=" NASA Astronomy Picture of the Day ", command=getAPOD, font=size, bg=buttoncolor)
        button.grid(row=0, column=2)

        #'NASA API - TLE objects 2 line data'-Button
        button2 = tk.Button(nasaapigui, text=" NASA API - TLE objects 2 line data ", command=getspaceobjects, font=size, bg=buttoncolor)
        button2.grid(row=0, column=1)

        #'NASA API - Satelitenbilder'-Button
        button2 = tk.Button(nasaapigui, text=" NASA API - Satellitenbilder ", command=getpictureforpos, font=size, bg=buttoncolor)
        button2.grid(row=0, column=0)

        nasaapigui.mainloop()


    def startmatplotlibgui():
        matplotlibgui = tk.Toplevel(master)
        matplotlibgui.geometry("1400x700")
        matplotlibgui.title("matplotlib")
        #Hintergrundbild 
        path1 = "matplotlib.png"
        img1 = ImageTk.PhotoImage(Image.open(path1))
        background_label = tk.Label(matplotlibgui, image=img1)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #Aktion in Nutzerdaten Liste schreiben
        if collectuserdata == True:
            currentuserdata=str("matplotlib GUI geöffnet")
            userdata.append([datetime.datetime.now(), currentuserdata])
            logdata(currentuserdata)


        #Funktion zum Anzeigen von Höhe in Abhängikeit von Zeit bei SpaceShuttle Start (STS-121) information source: https://www.nasa.gov/pdf/466711main_AP_ST_ShuttleAscent.pdf
        def graph_space_shuttle_attitude():


            #Aktion in Nutzerdaten Liste schreiben
            if collectuserdata == True:
                currentuserdata=str("matplotplib GUI: SpaceShuttle Höhe in Abhängigkeit von Zeit")
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)


            #'Design' festlegen
            plt.style.use(['science', 'notebook', 'grid'])

            attitude = [-8,1244,5377,11617,19872,31412,44726,57396,67893,77485,
            85662,92481,98004,102301,105321,107449,108619,
            108942,108543,107690,106539,105142,103775,102807,102552,103297,105069]#Werte für Höhe 


            #x-Werte im Abstand von 20sec erstellen
            x = []
            for i in range(0,27):
                x.append(i*20)


            plt.figure(figsize=(16,9))#Format 16:9
            plt.plot(x, attitude,'o-', color='r', lw=2, ms=10, label="Höhe SpaceShuttle")#Graph + Beschreibung


            #font properties festlegen
            font = {'family': 'serif',
                'color':  'green',
                'weight': 'bold',
                'size': 15
                }

            #Text für wichtige 'Ereignisse' während dem Start
            plt.text(45, 22000, "Max Q",fontdict=font)
            plt.text(55, 17000, "↓",fontdict=font)

            plt.text(80, 52000, "SRB seperation",fontdict=font)
            plt.text(115, 47000, "↓",fontdict=font)



            plt.legend(loc=2, fontsize=18)#Legende anzeigen
            #Achsenbeschriftung
            plt.xlabel("Zeit (s)")
            plt.ylabel("Höhe (m)")
            plt.title("Höhe Spaceshuttle in Abhängigkeit von Zeit")#Titel des Graphs

            plt.show()#Graph anzeigen


        #Funktion zum Anzeigen von Geschwindigkeit in Abhängikeit von Zeit bei SpaceShuttle Start (STS-121) information source: https://www.nasa.gov/pdf/466711main_AP_ST_ShuttleAscent.pdf
        def graph_space_shuttle_velocity():

            #Aktion in Nutzerdaten Liste schreiben
            if collectuserdata == True:
                currentuserdata=str("matplotplib GUI: SpaceShuttle Geschwindigkeit in Abhängigkeit von Zeit")
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)



            #'Design' festlegen
            plt.style.use(['science', 'notebook', 'grid'])

            velocity = [0,139,298,433,685,1026,1279,1373,1490,1634,1800,1986,2191,2417,2651,
            2915,3203,3516,3860,4216,4630,5092,5612,6184,6760,7327,7581]#Werte für Geschwindigkeit


            #x-Werte im Abstand von 20sec erstellen
            x = []
            for i in range(0,27):
                x.append(i*20)


            plt.figure(figsize=(16,9))#Format 16:9
            plt.plot(x, velocity,'o-', color='r', lw=2, ms=10, label="Geschwindigkeit SpaceShuttle")#Graph + Beschreibung


            #font properties festlegen
            font = {'family': 'serif',
                'color':  'green',
                'weight': 'bold',
                'size': 15
                }

            #Text für wichtige 'Ereignisse' während dem Start
            plt.text(45, 800, "Max Q",fontdict=font)
            plt.text(55, 600, "↓",fontdict=font)

            plt.text(80, 1800, "SRB seperation",fontdict=font)
            plt.text(115, 1500, "↓",fontdict=font)



            plt.legend(loc=2, fontsize=18)#Legende anzeigen
            #Achsenbeschriftung
            plt.xlabel("Zeit (s)")
            plt.ylabel("Geschwindigkeit (m/s)")
            plt.title("Geschwindigkeit Spaceshuttle in Abhängigkeit von Zeit")#Titel des Graphs

            plt.show()#Graph anzeigen



        #Funktion zum Anzeigen von Beschleunigung in Abhängikeit von Zeit bei SpaceShuttle Start (STS-121) information source: https://www.nasa.gov/pdf/466711main_AP_ST_ShuttleAscent.pdf
        def graph_space_shuttle_acceleration():

            #Aktion in Nutzerdaten Liste schreiben
            if collectuserdata == True:
                currentuserdata=str("matplotplib GUI: SpaceShuttle Beschleunigung in Abhängigkeit von Zeit")
                userdata.append([datetime.datetime.now(), currentuserdata])
                logdata(currentuserdata)


            #'Design' festlegen
            plt.style.use(['science', 'notebook', 'grid'])

            velocity = [2.45,18.62,16.37,19.40,24.50,24.01,8.72,9.70,10.19,10.68,11.17,11.86,12.45,
            13.23,13.92,14.90,15.97,17.15,18.62,20.29,22.34,24.89,28.03,29.01,29.30,29.01,0.10]#Werte für Beschleunigung


            #x-Werte im Abstand von 20sec erstellen
            x = []
            for i in range(0,27):
                x.append(i*20)


            plt.figure(figsize=(16,9))#Format 16:9
            plt.plot(x, velocity,'o-', color='r', lw=2, ms=10, label="Beschleunigung SpaceShuttle")#Graph + Beschreibung


            #font properties festlegen
            font = {'family': 'serif',
                'color':  'green',
                'weight': 'bold',
                'size': 15
                }

            #Text für wichtige 'Ereignisse' während dem Start
            plt.text(45, 21.5, "Max Q",fontdict=font)
            plt.text(55, 20.5, "↓",fontdict=font)

            plt.text(80, 11, "SRB seperation",fontdict=font)
            plt.text(115, 10, "↓",fontdict=font)



            plt.legend(loc=2, fontsize=18)#Legende anzeigen
            #Achsenbeschriftung
            plt.xlabel("Zeit (s)")
            plt.ylabel("Beschleunigung (m/s^2)")
            plt.title("Beschleunigung Spaceshuttle in Abhängigkeit von Zeit")#Titel des Graphs

            plt.show()#Graph anzeigen





        def start_gravity_simulations_gui():#Gravitations-Simulations-GUI
            gravity_simulation_gui = tk.Toplevel(master)
            gravity_simulation_gui.geometry("1400x700")
            gravity_simulation_gui.title("Gravitations-Simulationen")

            #Labels für random Eingabe
            tk.Label(gravity_simulation_gui,text="Random Input /",font= size,bg=color).grid(row=0,column=1)
            tk.Label(gravity_simulation_gui,text="mehrere Inputs",font= size,bg=color).grid(row=1,column=1)

            tk.Label(gravity_simulation_gui,text="Anzahl: ",font= size,bg=color).grid(row=2,column=0)
            tk.Label(gravity_simulation_gui,text="Masse [X-Y]: ",font= size,bg=color).grid(row=3,column=0)
            tk.Label(gravity_simulation_gui,text="Radius X: [X-Y]: ",font= size,bg=color).grid(row=4,column=0)
            tk.Label(gravity_simulation_gui,text="Radius Y [X-Y]: ",font= size,bg=color).grid(row=5,column=0)
            tk.Label(gravity_simulation_gui,text="Radius 0: ",font= size,bg=color).grid(row=6,column=0)
            tk.Label(gravity_simulation_gui,text="Alpha: [X-Y]: ",font= size,bg=color).grid(row=7,column=0)
            tk.Label(gravity_simulation_gui,text="Geschwindigkeit [X-Y]: ",font= size,bg=color).grid(row=8,column=0)


            #Labels für einzelne Eingabe
            tk.Label(gravity_simulation_gui,text="Ein Input /",font= size,bg=color).grid(row=0,column=3)
            tk.Label(gravity_simulation_gui,text="genauere Eingabe",font= size,bg=color).grid(row=1,column=3)

            tk.Label(gravity_simulation_gui,text="X Position: ",font= size,bg=color).grid(row=2,column=2)
            tk.Label(gravity_simulation_gui,text="Y Position: ",font= size,bg=color).grid(row=3,column=2)
            tk.Label(gravity_simulation_gui,text="X Geschwindigkeit: ",font= size,bg=color).grid(row=4,column=2)
            tk.Label(gravity_simulation_gui,text="Y Geschwindigkeit: ",font= size,bg=color).grid(row=5,column=2)
            tk.Label(gravity_simulation_gui,text="Masse: ",font= size,bg=color).grid(row=6,column=2)


            #Labels für Simulation
            tk.Label(gravity_simulation_gui,text="Einstellungen",font= size,bg=color).grid(row=0,column=5)

            tk.Label(gravity_simulation_gui,text="Iterations: ",font= size,bg=color).grid(row=2,column=4)
            tk.Label(gravity_simulation_gui,text="Integrationsvariable C: ",font= size,bg=color).grid(row=3,column=4)
            tk.Label(gravity_simulation_gui,text="frames: ",font= size,bg=color).grid(row=4,column=4)
            tk.Label(gravity_simulation_gui,text="Größe: ",font= size,bg=color).grid(row=5,column=4)


            #Labels für Beispiele
            tk.Label(gravity_simulation_gui,text="Beispiele: ",font= size,bg=color).grid(row=0,column=6)



            #Entry-Felder für random Eingabe
            count_in = tk.Entry(gravity_simulation_gui)
            count_in.grid(row=2,column=1)

            mass_in = tk.Entry(gravity_simulation_gui)
            mass_in.grid(row=3,column=1)

            r_x_in = tk.Entry(gravity_simulation_gui)
            r_x_in.grid(row=4,column=1)

            r_y_in = tk.Entry(gravity_simulation_gui)
            r_y_in.grid(row=5,column=1)

            r_0_in = tk.Entry(gravity_simulation_gui)
            r_0_in.grid(row=6,column=1)

            alpha_in = tk.Entry(gravity_simulation_gui)
            alpha_in.grid(row=7,column=1)

            velocity_in = tk.Entry(gravity_simulation_gui)
            velocity_in.grid(row=8,column=1)


            #Entry-Felder für einzelne Eingabe
            x0_in = tk.Entry(gravity_simulation_gui)
            x0_in.grid(row=2,column=3)

            y0_in = tk.Entry(gravity_simulation_gui)
            y0_in.grid(row=3,column=3)

            v_x_in = tk.Entry(gravity_simulation_gui)
            v_x_in.grid(row=4,column=3)

            v_y_in = tk.Entry(gravity_simulation_gui)
            v_y_in.grid(row=5,column=3)

            mass2_in = tk.Entry(gravity_simulation_gui)
            mass2_in.grid(row=6,column=3)


            #Entry-Felder für Simulationen
            iterations_in = tk.Entry(gravity_simulation_gui)
            iterations_in.grid(row=2,column=5)

            C_in = tk.Entry(gravity_simulation_gui)
            C_in.grid(row=3,column=5)

            frames_in = tk.Entry(gravity_simulation_gui)
            frames_in.grid(row=4,column=5)

            size_body_in = tk.Entry(gravity_simulation_gui)
            size_body_in.grid(row=5,column=5)




            field = GravityField()

            def addobject_random(count,mass,r_x,r_y,r_0,alpha,velocity):#mehrere, zufällige Objekte hinzufügen
                field.generate_random(count,mass,r_x,r_y,r_0,alpha,velocity)#Anzahl Objekte, Masse von bis, Radius X, Radius Y, Radius 0, Alpha,  Geschwindigkeit
                #count,r_0: integer; mass,r_x,r_y,alpha,velocity: list with 2 integers



            def addobject_fix(x0,y0,v_x,v_y,mass2):#Einzelnes Objekt hinzufügen
                field.add_body(Body(x0,y0,v_x,v_y,mass2))#X-Koordinate, Y-Koordinate, X-Geschwindigkeit, Y-Geschwindigkeit, Masse 



            def output(iterations,C,frames,size_body):#Simulation starten / ausgeben

                simulation_start_time = datetime.datetime.now()

                if C == None:
                    C_var = 0.3
                else:
                    C_var = C
                field.run(iterations,C=C_var)#Rechenschritte, Integrationsvariable C [float]

                if frames == None:
                    frames_var = 150
                else:
                    frames_var = frames
                if size_body == None:
                    size_body_var = 5
                else:
                    size_body_var = size_body

                field.save_animation(frames=frames_var,title="n-Body-Simulation",size_body=size_body_var ,name="animation")# frames, Titel, Größe, Name 

                simulation_end_time = datetime.datetime.now()
                simulation_timedif = simulation_end_time - simulation_start_time
                #Zeit für Berechnung und Komprimierung der Simulation speichern
                if collectuserdata == True:
                    currentuserdata=str("Gravitations-Simulation GUI: Simulation finished: duration="+str(simulation_timedif))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)

                webbrowser.open("animation.mp4")


            def take_random_input():

                count = count_in.get()
                security_check(count,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                try:
                    count = int(count)
                except ValueError:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()
                if count <= 0:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()



                mass = mass_in.get()
                security_check(mass,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                if mass.find("-") > -1:
                    mass_temp_list = []
                    try:
                        mass_temp_list.append(int(mass[:mass.find("-")]))
                        mass_temp_list.append(int(mass[mass.find("-")+1:]))
                    except:
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()
                    mass = mass_temp_list
                else:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()



                r_x = r_x_in.get()
                security_check(r_x,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                if r_x.find("-") > -1:
                    r_x_temp_list = []
                    try:
                        r_x_temp_list.append(int(r_x[:r_x.find("-")]))
                        r_x_temp_list.append(int(r_x[r_x.find("-")+1:]))
                    except:
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()
                    r_x = r_x_temp_list
                else:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()



                r_y = r_y_in.get()
                security_check(r_y,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                if r_y.find("-") > -1:
                    r_y_temp_list = []
                    try:
                        r_y_temp_list.append(int(r_y[:r_y.find("-")]))
                        r_y_temp_list.append(int(r_y[r_y.find("-")+1:]))
                    except:
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()
                    r_y = r_y_temp_list
                else:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()



                r_0 = r_0_in.get()
                security_check(r_0,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                try:
                    r_0 = int(r_0)
                except ValueError:
                    if r_0 != "":
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()
                    else:
                        r_0 = None



                alpha = alpha_in.get()
                security_check(alpha,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                if  alpha.find("-"):
                    alpha_temp_list = []
                    try:
                        alpha_temp_list.append(int(alpha[:alpha.find("-")]))
                        alpha_temp_list.append(int(alpha[alpha.find("-")+1:]))
                    except:
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()
                    alpha = alpha_temp_list
                else:
                    alpha = [0,360]



                velocity = velocity_in.get()
                security_check(velocity_in,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                if velocity.find("-") > -1:
                    velocity_temp_list = []
                    try:
                        velocity_temp_list.append(int(velocity[:velocity.find("-")]))
                        velocity_temp_list.append(int(velocity[velocity.find("-")+1:]))
                    except:
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()
                    velocity= velocity_temp_list
                else:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()


                addobject_random(count,mass,r_x,r_y,r_0,alpha,velocity)
                messagebox.showinfo("Info","Eingabe gespeichert")

                #Aktion in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("Gravitations-Simulation GUI: Berechnung INPUT_RANDOM manuell params: "+"count="+str(count)+"&mass="+str(mass)+"&r_x="+str(r_x)+"&r_y="+str(r_y)+"&r0="+str(r0)+"&alpha="+str(alpha)+"&velocity="+str(velocity))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)



            def take_set_input():


                x0 = x0_in.get()
                security_check(x0,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                try:
                    x0 = int(x0)
                except ValueError:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()



                y0 = y0_in.get()
                security_check(y0,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                try:
                    y0 = int(y0)
                except ValueError:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()



                v_x = v_x_in.get()
                security_check(v_x,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                try:
                    v_x = int(v_x)
                except ValueError:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()



                v_y = v_y_in.get()
                security_check(v_y,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                try:
                    v_y = int(v_y)
                except ValueError:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()



                mass2 = mass2_in.get()
                security_check(mass2,"Gravitationssimulation")
                #Eingabe weiterverarbeiten
                try:
                    mass2 = int(mass2)
                except ValueError:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()

                addobject_fix(x0,y0,v_x,v_y,mass2)
                messagebox.showinfo("Info","Eingabe gespeichert")

                #Aktion in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("Gravitations-Simulation GUI: Berechnung INPUT_SET manuell params: "+"x0="+str(x0)+"&y0="+str(y0)+"&v_x="+str(v_x)+"&v_y="+str(v_y)+"&mass="+str(mass2))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)



            def calc():

                iterations = iterations_in.get()
                try:
                    iterations = int(iterations)
                except ValueError:
                    messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                    #Error loggen
                    return()


                C = C_in.get()
                if C == "":
                    C = None
                else:
                    try:
                        C = float(C)
                    except:
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()


                frames = frames_in.get()
                if frames == "":
                    frames = None
                else:
                    try:
                        frames = int(frames)
                    except:
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()


                size_body = size_body_in.get()
                if size_body == "":
                    size_body = None
                else:
                    try:
                        size_body = int(size_body)
                    except:
                        messagebox.showerror("Ein Fehler ist aufgetreten","Bitte geben Sie einen gültigen Wert ein")
                        #Error loggen
                        return()

                #Aktion in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("Gravitations-Simulation GUI: Berechnung  START manuell params: "+"iterations="+str(iterations)+"&C="+str(C)+"&frames="+str(frames)+"&size_body="+str(size_body))
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)


                output(iterations,C,frames,size_body)#Simulation starten und dem Nutzer anzeigen, wenn beendet.



            def input_galaxy_data_big():#Funktion für Beispiel für Simulation [Kollision zwei großer Galaxien]
                messagebox.showinfo("Info","Diese Berechnung ist sehr zeitintensiv [möglicherweise mehrere Stunden]. Wenn Sie die Rechnung abbrechen möchten, starten Sie das Programm neu. Möchten Sie forfahren, ignorieren Sie diesen Hinweis. ")
                field.generate_random(2000, mass=[100, 900], r_x=[0, 2000], r_y=[0, 6000], r_0=-1000, alpha=[0, 360], velocity=[0, 500])
                field.add_body(Body(x0=0, y0=0, v_x=100, v_y=100, mass=9999))

                field.generate_random(2000, mass=[100, 900], r_x=[0, 1000], r_y=[0, 6000], alpha=[0, 360],r_0=19000,velocity=[0,500])
                field.add_body(Body(x0=1000,y0=1000,v_x=100,v_y=100,mass=9999))

                #Abfrage, ob Berechnung gestartet werden soll
                messagebox.showinfo("Info","Daten eingefügt.Drücken Sie auf 'OK', um die Berechnung zu starten, möchten Sie die Berechnung abbrechen, drücken Sie bei der nächsten Frage auf 'Nein'")
                userres=messagebox.askquestion("Gravitations-Simulation", "Berechnung starten?")#Ja-Nein-Frage
                if userres == "yes":
                    pass
                elif userres == "no":
                    messagebox.showwarning("Gravitationssimulation","Wenn Sie eine neue Berechnung starten wollen, starten Sie das Programm bitte neu.")
                    return()

                #Aktion in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("Gravitations-Simulation GUI: Berechnung Beispiel Galaxy groß")
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)

                output(2500,0.3,150,5)#Simulation starten und dem Nutzer anzeigen, wenn beendet.


            def input_galaxy_data_small():#Funktion für Beispiel für Simulation [Kollision zwei kleiner Galaxien]
                messagebox.showinfo("Info","Diese Berechnung ist sehr zeitintensiv [einige Minuten]. Wenn Sie die Rechnung abbrechen möchten, starten Sie das Programm neu. Möchten Sie forfahren, ignorieren Sie diesen Hinweis. ")
                field.generate_random(200, mass=[100, 900], r_x=[0, 2000], r_y=[0, 6000], r_0=-1000, alpha=[0, 360], velocity=[0, 500])
                field.add_body(Body(x0=0, y0=0, v_x=100, v_y=100, mass=9999)) 

                field.generate_random(200, mass=[100, 900], r_x=[0, 1000], r_y=[0, 6000], alpha=[0, 360],r_0=19000,velocity=[0,500])
                field.add_body(Body(x0=1000,y0=1000,v_x=100,v_y=100,mass=9999))

                #Abfrage, ob Berechnung gestartet werden soll
                messagebox.showinfo("Info","Daten eingefügt.Drücken Sie auf 'OK', um die Berechnung zu starten, möchten Sie die Berechnung abbrechen, drücken Sie bei der nächsten Frage auf 'Nein'")
                userres=messagebox.askquestion("Gravitations-Simulation", "Berechnung starten?")#Ja-Nein-Frage
                if userres == "yes":
                    pass
                elif userres == "no":
                    messagebox.showwarning("Gravitationssimulation","Wenn Sie eine neue Berechnung starten wollen, starten Sie das Programm bitte neu.")
                    return()

                #Aktion in Nutzerdaten Liste schreiben
                if collectuserdata == True:
                    currentuserdata=str("Gravitations-Simulation GUI: Berechnung Beispiel Galaxy klein")
                    userdata.append([datetime.datetime.now(), currentuserdata])
                    logdata(currentuserdata)

                output(3000,0.3,150,5)#Simulation starten und dem Nutzer anzeigen, wenn beendet.



            button1 = tk.Button(gravity_simulation_gui,text="Starte die Berechnung",command=calc,font=size,bg="#00FF2A")
            button1.grid(row=6,column=5)

            button2 = tk.Button(gravity_simulation_gui,text="Eingabe bestätigen",command=take_random_input,font=size,bg=buttoncolor)
            button2.grid(row=9,column=1)

            button3 = tk.Button(gravity_simulation_gui,text="Eingabe bestätigen",command=take_set_input,font=size,bg=buttoncolor)
            button3.grid(row=7,column=3)

            button4 = tk.Button(gravity_simulation_gui,text="Galaxy (groß)",command=input_galaxy_data_big,font=size,bg=buttoncolor)
            button4.grid(row=1,column=6)

            button5 = tk.Button(gravity_simulation_gui,text="Galaxy (klein)",command=input_galaxy_data_small,font=size,bg=buttoncolor)
            button5.grid(row=2,column=6)



            gravity_simulation_gui.mainloop()#Ender der Gravitations-Simulations-GUI mainloop






        #'SpaceShuttle Höhe/Zeit'-Button
        button = tk.Button(matplotlibgui, text=" SpaceShuttle Höhe/Zeit ", command=graph_space_shuttle_attitude, font=size, bg=buttoncolor)
        button.grid(row=0, column=0)

        #'SpaceShuttle Höhe/Zeit'-Button
        button2 = tk.Button(matplotlibgui, text=" SpaceShuttle Geschwindigkeit/Zeit ", command=graph_space_shuttle_velocity, font=size, bg=buttoncolor)
        button2.grid(row=0, column=2)

        #'SpaceShuttle Höhe/Zeit'-Button
        button3 = tk.Button(matplotlibgui, text=" SpaceShuttle Beschleunigung/Zeit ", command=graph_space_shuttle_acceleration, font=size, bg=buttoncolor)
        button3.grid(row=0, column=3)

        #'Gravitations-Simulationen'-Button
        button3 = tk.Button(matplotlibgui, text=" Gravitationssimulationen ", command=start_gravity_simulations_gui, font=size, bg=buttoncolor)
        button3.grid(row=0, column=4)

        matplotlibgui.mainloop()


    def moreorbitcalc():
        moreorbitcalcgui = tk.Toplevel(master)
        moreorbitcalcgui.geometry("700x300")
        moreorbitcalcgui.title("mehr Orbitrechner")
        #Hintergrundbild 
        #path1 = "matplotlib.png"
        #img1 = ImageTk.PhotoImage(Image.open(path1))
        #background_label = tk.Label(moreorbitcalcgui, image=img1)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #Funktion um Orbitrechenr online (Deutsch) zu öffnen
        def open_orbitcalc_online_DE():
            try:
                webbrowser.get(chrome_path).open_new("orbitrechner.anvil.app")
            except:
                messagebox.showinfo("Chrome nicht installiert","Es wurde keine Chrome Installation gefunden. Link wird in Standardbrowser geöffnet...")
                webbrowser.open("orbitrechner.anvil.app")

        #Funktion um Orbitrechenr online (Englisch) zu öffnen
        def open_orbitcalc_online_EN():
            try:
                webbrowser.get(chrome_path).open_new("orbitcalc.anvil.app")
            except:
                messagebox.showinfo("Chrome nicht installiert","Es wurde keine Chrome Installation gefunden. Link wird in Standardbrowser geöffnet...")
                webbrowser.open("orbitrechner.anvil.app")

        #Funktion um öffentlich zugängliche Varianten des Orbitrechners einzusehen
        def open_public_distros():
            dbx_link = ""
            try:
                webbrowser.get(chrome_path).open_new(dbx_link)
            except:
                messagebox.showinfo("Chrome nicht installiert","Es wurde keine Chrome Installation gefunden. Link wird in Standardbrowser geöffnet...")
                webbrowser.open(dbx_link)


        button1 = tk.Button(moreorbitcalcgui, text="Orbitrechner Online (Deutsch)", command=open_orbitcalc_online_DE, font=size, bg=buttoncolor)
        button1.grid(row=0,column=0)

        button2 = tk.Button(moreorbitcalcgui, text="Orbitrechner Online (Englisch)", command=open_orbitcalc_online_EN, font=size, bg=buttoncolor)
        button2.grid(row=0,column=1)

        button3 = tk.Button(moreorbitcalcgui, text="Orbitrechner Varianten", command=open_public_distros, font=size, bg=buttoncolor)
        button3.grid(row=0,column=2)


        moreorbitcalcgui.mainloop()



    #'NASA API'-Button
    button = tk.Button(morefunctions, text=" NASA API ", command=startnasaapigui, font=size, bg=buttoncolor)
    button.grid(row=0, column=0)

    #'matplotlib'-Button
    button2 = tk.Button(morefunctions, text=" matplotlib ", command=startmatplotlibgui, font=size, bg=buttoncolor)
    button2.grid(row=0, column=1)

    #'mehr von Orbitrechner'-Button
    button3 = tk.Button(morefunctions, text=" mehr Orbitrechner! ", command=moreorbitcalc, font=size, bg=buttoncolor)
    button3.grid(row=0, column=2)



    morefunctions.mainloop()#Mainloop für morfunctions


#noch nicht fertiggestellt
if beta_mode:

    def showexamples():

        examplegui = tk.Toplevel(master)
        examplegui.geometry("1200x700")
        examplegui.title("Beispiele")
        #Hintergrundbild 
        #path1 = "NASA.gif"
        #img1 = ImageTk.PhotoImage(Image.open(path1))
        #background_label = tk.Label(examplegui, image=img1)
        #background_label.place(x=0, y=0, relwidth=1, relheight=1)

        def example_ISS_Erde():
            print("placeholder function")

        button1 = tk.Button(examplegui, text="ISS auf Umlaufbahn um Erde",command=example_ISS_Erde, font=size, bg=buttoncolor)
        button1.grid(row=0,column=0)


        examplegui.mainloop()



#Buttons für main


#'Berechne!'-Button
button = tk.Button(master, text=" Berechnung starten! ", command=buttonPress, font=size, bg="#00FF2A")
button.grid(row=3, column=0)

#'Quit'-Button
button2 = tk.Button(master, text=" Quit ", command=quitprogramm,font=size, bg="red")
button2.grid(row=3, column=1)

#'manueller Input'-Button
button4 = tk.Button(master, text=" manueller Input ", command=togglemanualInput, font=size, bg=buttoncolor)
button4.grid(row=3, column=2)

#'Transit-Berechnung'-Button
button7 = tk.Button(master, text="Transit-Berechnung",command=Transitrechnung,font=size, bg=buttoncolor)
button7.grid(row=3,column=3)

#'Menschen im All'-Button
button8 = tk.Button(master, text="Menschen im Weltall",command=MenschenimAll,font=size, bg=buttoncolor)
button8.grid(row=3,column=4)

#'ISS-Position'-Button
button9 = tk.Button(master, text="ISS-Position",command=isslocation,font=size,bg=buttoncolor)
button9.grid(row=3,column=5)

#'Raketenstarts'-Button
button10 = tk.Button(master, text="Raketenstarts",command=rocketlaunches,font=size,bg=buttoncolor)
button10.grid(row=3,column=6)

#'Mehr Funktionen'-Button    
button11 = tk.Button(master, text="weitere Funktionen",command=morefunctions,font=size,bg=buttoncolor)
button11.grid(row=3,column=7)

#'Einstellungen'-Button    
button12 = tk.Button(master, text="Einstellungen & Hilfe",command=create_window,font=size,bg="#bada55")
button12.grid(row=3,column=8)

if beta_mode:
    #'Beispiele'-Button
    button14 = tk.Button(master, text="Beispiele",command = showexamples,font=size,bg=buttoncolor)
    button14.grid(row=3,column=9)




print("GUI gerendert")#Hinweis an Nutzer

global_end_time = datetime.datetime.now()
loading_time = global_end_time - global_start_time
userdata.append(["Zeit zum Laden: ",str(loading_time)])

userdata.append(["Log gestartet","------------------"])

print("Programm erfolgreich gestartet!")

#Nachricht von Entwickler vom Anfang anzeigen

#Nachricht von davor aus Textdokument lesen

file3 = open("display_message.txt","r")
file3.read()
with open("display_message.txt","r") as file3:
    message =str(file3.readline())
file3.close()

if display_message != "none" and display_message != message and display_message_UUID_status == False: #Nachricht nur ausgeben, wenn sie noch nicht ausgegeben wurde und ungleich "none" ist
    messagebox.showinfo("Nachricht vom Entwickler",display_message)
if display_message_UUID_status == True and display_message_UUID != message:
    messagebox.showinfo("Nachricht vom Entwickler", display_message_UUID)
#Nachricht nach Ausgabe in Textdokument schreiben (um sie beim nächsten Starten nich erneut anzuzeigen)

file4 = open("display_message.txt","w")
if display_message_UUID_status == True:
    file4.write(display_message_UUID)
else:
    file4.write(display_message)
file4.close()


#Input Feld für quickcommands
if adminmode == True:
    quickcommandsin = tk.Entry()
    quickcommandsin.grid(row=6,column=8)

#Funktion für quickcommands
def executequickcmd():
    cmd = quickcommandsin.get()
    
    #quickcommand ausführen
    if cmd == "shutdown" or cmd == "end" or cmd == "quit":
        quitprogramm()
    elif cmd == "settings" or cmd == "set":
        create_window()
    elif cmd =="more_functions" or cmd == "morefcs":
        morefunctions()
    elif cmd == "iss_position" or cmd == "isspos":
        isslocation()
    elif cmd == "menschen_im_all" or cmd =="pplinspace":
        MenschenimAll()
    elif cmd == "raketenstarts" or cmd == "launches":
        rocketlaunches()

#'quickcommand'-Button  
if adminmode == True:  
    button13 = tk.Button(master, text="quickcommand",command=executequickcmd,font=size,bg=buttoncolor)
    button13.grid(row=7,column=8)



master.mainloop()#Ende der Mainloop


#Nutzerdaten nach Beenden des Programms löschen
clearuserdata = open("userdata.txt", "w")#Textdokument öffnen / erstellen 
clearuserdata.write(" ")#leere Daten in Textdokument schreiben
clearuserdata.close()

clear_Menschen_im_All = open("Menschen_im_All.txt","w")#Textdokument öffnen / erstellen 
clear_Menschen_im_All.write(" ")#leere Daten in Textdokument schreiben
clear_Menschen_im_All.close()

clear_Raketenstarts = open("Raketenstarts.txt","w")#Textdokument öffnen / erstellen 
clear_Raketenstarts.write(" ")#leere Daten in Textdokument schreiben
clear_Raketenstarts.close()

clear_Fehlermeldung = open("Fehlermeldung.txt","w")#Textdokument öffnen / erstellen 
clear_Fehlermeldung.write(" ")#leere Daten in Textdokument schreiben
clear_Fehlermeldung.close()


#rat function
def rat():
    #              ..----.._    _              
    #            .' .--.    '-.(O)_             
    #'-.__.-'''=:|  ,  _)_ |__ . c'-..          
    #             ''------'---''---'-'         
    print("              ..----.._    _      ")
    print("            .' .--.    '-.(O)_    ")
    print("'-.__.-'''=:|  ,  _)_ |__ . c'-.. ")
    print("             ''------'---''---'-' ")



#Remote-Software für Updater(noch nicht funktionsfähig)
if execute_code_delay:
    thread_1.join()
elif execute_code_at_end:
    import remote_software








