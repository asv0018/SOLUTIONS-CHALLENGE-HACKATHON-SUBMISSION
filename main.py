from datetime import datetime
import re
from pygame import mixer
import os, sys
import glob
import pyrebase
import json
import requests
import calendar
import threading
import RPi.GPIO as GPIO
import LiquidCrystalDisplay_i2c
from time import *

lcd = LiquidCrystalDisplay_i2c.lcd()

GPIO_FOR_SNOOZE = 17
GPIO_FOR_PLAYPAUSE = 27

serial_num = "test"
pathOfConfig = "Resources/config.json"
all_alarm_minutes = []
all_alarm_hours = []
all_alarm_times = []
all_alarm_days = []
all_alarm_ids = []
all_alarm_everyday = []
all_alarm_days_selected = []
all_alarm_musics = []
all_alarm_snooze = []
all_alarm_plays = []
all_alarm_names = []
all_alarm_setters = []
downloaded_music_files = []

def send_data_to_google_sheets(data):
    response = requests.get("https://script.google.com/macros/s/AKfycbxMV3vdcKc9I6eBuzKlPiwrvN3mWdQjWSobAfykC9CxdzpQhF_rG6LhZ5cEd8lyzRE7/exec?label="+str(data))
    if response.status_code==200:
        print("SUCCESSFULLY SENT THE DATA TO GOOGLE SHEETS")
    else:
        print("NETWORK ISSUE")

def firebase_handler(response):
    global firebase, uid, data
    data = firebase.database().child("alarms_users").child(uid).get().val()
    json_file = open("Resources/firebase_database_data.json", "w")
    json_file.truncate(0)
    json_file.write(json.dumps(data, indent=4))
    json_file.close()
    try:
        refill_the_data_to_variables()
    except:
        print("still no data")

def refill_the_data_to_variables():
    all_alarm_minutes.clear()
    all_alarm_hours.clear()
    all_alarm_days.clear()
    all_alarm_times.clear()
    all_alarm_plays.clear()
    all_alarm_snooze.clear()
    all_alarm_setters.clear()
    all_alarm_everyday.clear()
    all_alarm_ids.clear()
    all_alarm_days_selected.clear()
    all_alarm_musics.clear()
    all_alarm_names.clear()
    json_file = open("Resources/firebase_database_data.json", "r")
    temp__data = json_file.read()
    temp_data = json.loads(temp__data)
    json_file.close()
    for i in temp_data:
        hours, minutes = "", ""
        play = False
        for j in temp_data[i]:
            if j== "name":
                temp_name_ = temp_data[i][j]
                all_alarm_names.append(temp_name_)
            if j == "setter":
                setter = temp_data[i][j]
                all_alarm_setters.append(setter)
            if j == "hours":
                hours = temp_data[i][j]
                all_alarm_hours.append(hours)
            if j == "minutes":
                minutes = temp_data[i][j]
                all_alarm_minutes.append(minutes)
            if j == "id":
                id = temp_data[i][j]
                all_alarm_ids.append(id)
            if j == "music":
                download_music = temp_data[i][j]
                if download_music == "https://firebasestorage.googleapis.com/v0/b/iot-alarm-cf8df.appspot.com/o/music_files%2Fdefault.mp3?alt=media&token=4d59a0ae-2b4b-459c-bd57-b5b5c7bdf47c":
                    download_music = "https://firebasestorage.googleapis.com/v0/b/iot-alarm-cf8df.appspot.com/o/music_files%2Fdefault.mp3?alt=media&token=b7bd161e-2398-445e-850b-80d9fb2e5a72"
                all_alarm_musics.append(download_music)
            if j == "play":
                play = temp_data[i][j]
                all_alarm_plays.append(play)
            if j == "snooze":
                snooze = temp_data[i][j]
                all_alarm_snooze.append(snooze)
            if j == "everytime":
                everytime = temp_data[i][j]
                all_alarm_everyday.append(everytime)
            if j == "days_selected":
                days_selected = temp_data[i][j]
                all_alarm_days_selected.append(days_selected)

        print("*************************")
        if len(str(hours)) < 2:
            hours = "0" + str(hours)
            #print(hours)
        else:
            hours = str(hours)
        if len(str(minutes)) < 2:
            minutes = "0" + str(minutes)
            #print(minutes)
        else:
            minutes = str(minutes)

        all_alarm_times.append(str(hours) + ":" + str(minutes))
    thread = threading.Thread(target=download_all_musics, args=("Resources/Downloads/Music", all_alarm_musics))
    thread.start()


def refill_the_data_to_variables_from_storage():
    all_alarm_minutes.clear()
    all_alarm_hours.clear()
    all_alarm_days.clear()
    all_alarm_times.clear()
    all_alarm_plays.clear()
    all_alarm_snooze.clear()
    all_alarm_setters.clear()
    all_alarm_everyday.clear()
    all_alarm_ids.clear()
    all_alarm_days_selected.clear()
    all_alarm_musics.clear()
    all_alarm_names.clear()
    json_file = open("Resources/firebase_database_data.json", "r")
    temp__data = json_file.read()
    temp_data = json.loads(temp__data)
    json_file.close()
    for i in temp_data:
        hours, minutes = "", ""
        play = False
        for j in temp_data[i]:
            if j == "name":
                temp_name__ = temp_data[i][j]
                all_alarm_names.append(temp_name__)
            if j == "setter":
                setter = temp_data[i][j]
                all_alarm_setters.append(setter)
            if j == "hours":
                hours = temp_data[i][j]
                all_alarm_hours.append(hours)
            if j == "minutes":
                minutes = temp_data[i][j]
                all_alarm_minutes.append(minutes)
            if j == "id":
                id = temp_data[i][j]
                all_alarm_ids.append(id)
            if j == "music":
                download_music = temp_data[i][j]
                if download_music == "https://firebasestorage.googleapis.com/v0/b/iot-alarm-cf8df.appspot.com/o/music_files%2Fdefault.mp3?alt=media&token=4d59a0ae-2b4b-459c-bd57-b5b5c7bdf47c":
                    download_music = "https://firebasestorage.googleapis.com/v0/b/iot-alarm-cf8df.appspot.com/o/music_files%2Fdefault.mp3?alt=media&token=b7bd161e-2398-445e-850b-80d9fb2e5a72"
                all_alarm_musics.append(download_music)
            if j == "play":
                play = temp_data[i][j]
                all_alarm_plays.append(play)
            if j == "snooze":
                snooze = temp_data[i][j]
                all_alarm_snooze.append(snooze)
            if j == "everytime":
                everytime = temp_data[i][j]
                all_alarm_everyday.append(everytime)
            if j == "days_selected":
                days_selected = temp_data[i][j]
                all_alarm_days_selected.append(days_selected)
        print("*************************")
        if len(str(hours)) < 2:
            hours = "0"+str(hours)
            #print(hours)
        else:
            hours = str(hours)
        if len(str(minutes)) < 2:
            minutes = "0"+str(minutes)
            #print(minutes)
        else:
            minutes = str(minutes)
        all_alarm_times.append(hours + ":" + minutes)


def load_all_songs():
    downloaded_music_files.clear()
    with open("Resources/Downloads/downloaded_music_paths.txt", "r") as file:
        downloaded_music_files.append(file.readline().rstrip("\n"))
    print(downloaded_music_files)


def delete_old_songs():
    delete_files = glob.glob('Resources/Downloads/Music/*')
    for file_to_be_deleted in delete_files:
        os.remove(file_to_be_deleted)
    print("All the old songs are deleted...")


def download_all_musics(path, all_alarms_url_path):
    paths = open("Resources/Downloads/downloaded_music_paths.txt", "w+")
    downloaded_music_files.clear()
    paths.truncate(0)
    for i in all_alarms_url_path:
        music_uri = requests.get(i)
        temp_index = all_alarm_musics.index(i)
        temp_name = all_alarm_ids[temp_index]
        temp_music_name = re.sub('[^A-Za-z0-9]+', "", temp_name)
        temp_path = r"{0}/{1}".format(path, temp_music_name)
        with open(temp_path + ".mp3", 'wb+') as music_file:
            music_file.write(music_uri.content)
        paths.write(temp_path + ".mp3" + "\n")
        downloaded_music_files.append(temp_path + ".mp3")
        print("adding/updating a music file")
    print("ALL MUSIC FILES ARE DOWNLOADED")
    print(downloaded_music_files)
    paths.close()


def first_time_init(firebase):
    uid = firebase.database().child("iot_alarm").child(serial_num).child(serial_num)
    uid = uid.get().val()
    if uid is not None:
        stream = firebase.database().child("alarms_users").child(uid).stream(firebase_handler)
        data_file = open("Resources/firebase_database_data.json", "r")
        temp_data = data_file.read()
        data_file.close()
        return uid, stream
    else:
        print("OOPS! :< There is no account paired with this IoT Device")
        data_file = open("Resources/firebase_database_data.json", "r")
        temp_data = data_file.read()
        data_file.close()
        return None, None

def Thread_to_display_time_on_LCD():
    now = datetime.now()
    day_num = datetime.today().weekday()
    day = str(calendar.day_name[day_num])
    time = str(now.strftime("%H:%M:%S"))
    date = str(now.strftime("%d/%m/%Y"))
    global lcd
    
    lcd.lcd_display_string("Time : ",1,0)
    # Here you write te code to display time

def snooze_timer(testhour, testmin):
    i = testhour 
    j = testmin + 2
    if testmin < 50:
        testmin = testmin + 10
    elif testmin >= 50:
        if testmin == 50:
            testmin = 0
            testhour = testhour + 1
            if testhour == 24:
                testhour = 0
                
        else:
            diff_time = 60 - testmin
            min_to_set = 10 - diff_time
            testmin = min_to_set
            testhour = testhour + 1
            if testhour == 24:
                testhour = 0

    # Luciana zogbi youtube channel, i should see all the videos! she is pretty!!!!
    print("Finally after snooze for 10 minutes, the hours and minutes are as :")
    print("hours : {}\nmins : {}".format(testhour,testmin))
    print("******************8")

    return i, j

def mainLoopWhenNotConnectedToInternet():
    load_all_songs()
    try:
        refill_the_data_to_variables_from_storage()
    except:
        print("There is no data found in the account to play alarm")

    playing = False
    while not connected_to_internet:
        now = datetime.now()
        day_num = datetime.today().weekday()
        day = str(calendar.day_name[day_num])
        time = str(now.strftime("%H:%M"))
        print(time)
         #print("Downloaded music files:" + str(downloaded_music_files))
        #print(all_alarm_times)
        if time in all_alarm_times:
            index = all_alarm_times.index(time)
            if day in all_alarm_days_selected[index]:
                if all_alarm_plays[index]:
                    print("Alarm time now")
                    if not playing:
                        mixer.music.load(downloaded_music_files[index])
                        mixer.music.play(-1)
                        playing = True
                        if all_alarm_everyday[index] == False:
                            pass
                            # you cannot perform under following operations as, you are not reachable to the internet
                            #databases = firebase.database().child("alarms_users").child(uid).child(all_alarm_ids[index])
                            #databases.update({"play": False})

#################################################################################################
#                                  THE MAIN PROGRAM STARTS HERE                                 #
#################################################################################################


if __name__ == "__main__":
    iot_medicine_label = ""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_FOR_PLAYPAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GPIO_FOR_SNOOZE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    mixer.init()
    file = open(pathOfConfig,"r")
    config = json.load(file)
    file.close()
    firebase = pyrebase.initialize_app(config)
    connected_to_internet = False
    try:
        check_internet = requests.get("https://www.google.com/", timeout=2)
        print("IoT Alarm is connected to internet :)")
        connected_to_internet = True
    except:
        print("NO INTERNET! :< . DEVICE READS PREVIOUS DATA AND ALARMS ACCORDING TO IT")

    while True:
        if connected_to_internet:
            os.system("sudo timedatectl set-ntp True")
            print("updating the time is done")
            uid, stream = first_time_init(firebase)
            if uid is not None and stream is not None:
                print("STARTed IN MODE")
                load_all_songs()
                try:
                    refill_the_data_to_variables_from_storage()
                except:
                    print("There is no data found in the account to play alarm")

                is_snoozed = False
                snooze_time = ""
                playing = False
                previous_set_time = ""
                index = None
                pressed_stop = False
                pressed_snooze = False
                setter_name = ""
                tempmin, temphour = "",""
                while connected_to_internet:
                    now = datetime.now()
                    day_num = datetime.today().weekday()
                    day = str(calendar.day_name[day_num])
                    my_time = str(now.strftime("%H %M %S"))
                    time = str(now.strftime("%H:%M"))
                    date = str(now.strftime("%d/%m"))
                    print(time)
                    lcd.lcd_display_string(date+"   "+my_time, 1)
                    #print("Downloaded music files:" + str(downloaded_music_files))
                    #print(all_alarm_times)
                    if time in all_alarm_times:
                        index = all_alarm_times.index(time)
                        if day in all_alarm_days_selected[index]:
                            if all_alarm_plays[index]:
                                print("Alarm time now")
                                my_alarm_name = all_alarm_names[index]
                                iot_medicine_label = my_alarm_name
                                if not playing:
                                    my_alarm_name = all_alarm_names[index]
                                    lcd.lcd_display_string(my_alarm_name,2)
                                    previous_set_time = time
                                    mixer.music.load(downloaded_music_files[index])
                                    mixer.music.play(-1)
                                    playing = True
                                    tempmin = int(all_alarm_minutes[index])
                                    temphour = int(all_alarm_hours[index])
                                    #setter_name = all_alarm_setters[index]
                                    setter_name = "self"

                    if pressed_stop == True:
                        if previous_set_time != time:
                            # Now it shud moniter that the play gets turned off after  the time is changed
                            playing = False
                            pressed_stop = False
                            previous_set_time = ""

                        

                    if pressed_snooze == True:
                        # This will take care from restarting of the music after pressing the button
                        if time == snooze_time:
                            print("snooze time now +)(+")
                            mixer.music.load(downloaded_music_files[index])
                            mixer.music.play(-1)
                            playing = True
                            snooze_time = ""
                            
                    # I am planning to do some kind of interrupts stuffs here
                    if GPIO.input(GPIO_FOR_PLAYPAUSE)==False:
                        iot = threading.Thread(target = send_data_to_google_sheets, args=(iot_medicine_label,))
                        iot.start()
                        lcd.lcd_clear()
                        if pressed_stop == False:
                            if playing == True:
                                print("USER PRESSED TO STOP THE ALARM :)")
                                if all_alarm_everyday[index] == False:
                                    databases = firebase.database().child("alarms_users").child(uid).child(
                                        all_alarm_ids[index])
                                    databases.update({"play": False})
                                mixer.music.stop()
                                
                                iot_medicine_label = ""
                                is_snoozed = False
                                snooze_time = ""
                                pressed_stop = True
                                pressed_snooze = False


                    if GPIO.input(GPIO_FOR_SNOOZE)==False:
                        # If the person presses the snooze button then do these necessory actions
                        if pressed_stop == False:
                            if playing == True:
                                print("USER PRESSED TO SNOOZE THE ALARM :)")
                                # Here, I should do program in such a way that
                                if setter_name == "self":
                                    print("the time is {} & {}".format(tempmin,temphour))
                                    temphour, tempmin = snooze_timer(int(temphour),int(tempmin))
                                    temphour, tempmin = str(temphour), str(tempmin)
                                    if len(tempmin) < 2:
                                        tempmin = "0"+tempmin
                                        #print(tempmin)
                                    else:
                                        tempmin = tempmin
                                    if len(temphour) < 2:
                                        temphour = "0"+temphour
                                        #print(temphour)
                                    else:
                                        temphour = temphour

                                    is_snoozed = True
                                    mixer.music.stop()
                                    snooze_time = "{0}:{1}".format(temphour, tempmin)
                                    pressed_stop = True
                                    pressed_snooze = True 

                            




            else:
                print("OOPS, PLEASE PAIR YOUR DEVICE WITH THE ACCOUNT, RESTART THE DEVICE AND TRY AGAIN")
                keep_in_while_loop_until_restart = True
                while keep_in_while_loop_until_restart:
                    pass # NO PROGRAMME CAN BE WRITTEN HERE
        else:
            inner_condition = False
            try:
                refill_the_data_to_variables_from_storage()
                print("RETRIEVED PREVIOUSLY SAVED DATA")
                inner_condition = True
            except:
                print("OH YOU MIGHT SEEM TO BE A NEW USER :> YOU DONT HAVE ANY ALARMS IN YOUR ACCOUNT :)")
                print("Get me synced to internet!. Once you get internet")
                # Write a program in try except block to detect inteernet, if intreernt iss pressent then direclty kill the process and relaunch it. this can be done only in linucx environement
                while not inner_condition:
                    try:
                        test = requests.get("https://github.com")
                        print("finally, connected to internet network")
                        os.system("chmod +x restart_script.sh")
                        os.system("./restart_script.sh") # this will restart the main script ok!!!
                    except:
                        pass
            while not connected_to_internet:
                pass
                # This shall be taken care in linux environment
                mainLoopWhenNotConnectedToInternet()
