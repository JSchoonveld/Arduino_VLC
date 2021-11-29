#!/usr/bin/env python3
import time

import vlc
from pymata4 import pymata4

triggerPin = 11
echoPin = 12
LED_PIN = 13

board = pymata4.Pymata4()

video_started = False
video_paused = False

media_player = vlc.MediaPlayer()

media = vlc.Media('yourmovie.mp3')

media_player.set_media(media)


def the_callback(data):
    global video_started
    global video_paused
    global media_player

    print(data[2])

    if not video_started:
        if data[2] < 20:
            media_player.play()
            video_started = True

    elif video_started:
        if data[2] >= 30:
            media_player.set_pause(1)
            board.digital_write(LED_PIN, 1)
        elif data[2] < 30:
            media_player.set_pause(0)
            board.digital_write(LED_PIN, 0)
        elif data[2] < 100:
            media_player.get_fullscreen(1)


board.set_pin_mode_digital_output(LED_PIN)
board.set_pin_mode_sonar(triggerPin, echoPin, the_callback)

while True:
    try:
        time.sleep(2 / 1000000)
        board.sonar_read(triggerPin)
    except Exception:
        board.shutdown()
