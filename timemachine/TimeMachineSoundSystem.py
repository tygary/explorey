from sound.MultiTrackMusicPlayer import MultiTrackMusicPlayer
import pygame
import time

OFF = -1
AMBIENT = 0
STARTUP = 1
ON = 2
TIME_STOP = 3
ENDING = 4
FULL_SPEED = 5

STARTUP_TIME = 10

songs = [
    '/home/admin/explorey/sound/TimeMachine-AmbienceLoud.ogg',
    '/home/admin/explorey/sound/TimeMachine-StartupShort.ogg',
    '/home/admin/explorey/sound/TimeMachine-Running.ogg',
    '/home/admin/explorey/sound/TimeMachine-Frozen.ogg',
    '/home/admin/explorey/sound/TimeMachine-Shutdown.ogg',
    '/home/admin/explorey/sound/TimeMachine-FullSpeed.ogg'
]


class TimeMachineSoundSystem(object):
    player = MultiTrackMusicPlayer(songs)
    wasPlaying = False
    time_speed = 0
    is_running = False
    current_mode = OFF
    startup_time = 0

    def __init__(self):
        self.__play_ambient()

    def __play_ambient(self):
        self.player.play_song(AMBIENT, 1, channel=AMBIENT)

    def __play_time_startup(self):
        self.player.play_song(STARTUP, 1, channel=STARTUP, loops=0)

    def __play_time_traveling(self):
        self.player.play_song(ON, 1, channel=ON)

    def __play_time_frozen(self):
        self.player.play_song(TIME_STOP, 1, channel=TIME_STOP)

    def __play_time_ending(self):
        self.player.play_song(ENDING, 1, channel=ENDING, loops=0)

    def __play_full_speed(self):
        self.player.play_song(FULL_SPEED, 1, channel=FULL_SPEED)

    def update_sounds(self, is_running, time_speed):
        if not is_running and self.current_mode != OFF:
            if self.current_mode == ON:
                self.__play_time_ending()
            self.__play_ambient()
            self.player.stop_music(STARTUP)
            self.player.stop_music(ON)
            self.player.stop_music(TIME_STOP)
            self.player.stop_music(FULL_SPEED)
            self.current_mode = OFF

        if is_running and self.current_mode == OFF or self.current_mode == AMBIENT:
            self.__play_time_startup()
            self.startup_time = time.time()
            self.player.stop_music(AMBIENT)
            self.current_mode = STARTUP
        elif self.current_mode == STARTUP and time.time() > self.startup_time + STARTUP_TIME:
            self.__play_time_traveling()
            self.__play_time_frozen()
            self.__play_full_speed()
            self.current_mode = ON
        if self.current_mode == ON:
            velocity = abs(time_speed) / 1000
            if velocity < .4:
                ratio = velocity / .4
                self.player.set_volume(ON, 0.5 + ratio/2)
                self.player.set_volume(TIME_STOP, (1 - ratio) * 0.8 + 0.2)
                self.player.set_volume(FULL_SPEED, 0.2)
            elif velocity > 0.6:
                ratio = (velocity - 0.6) / .4
                self.player.set_volume(ON, 1)
                self.player.set_volume(TIME_STOP, 0.2)
                self.player.set_volume(FULL_SPEED, 0.4 * ratio + 0.2)
            else:
                self.player.set_volume(ON, 1)
                self.player.set_volume(TIME_STOP, 0.2)
                self.player.set_volume(FULL_SPEED, 0.2)






    # def play_bat_journey(self):
    #     self.player.play_song('/home/admin/explorey/sound/BatAudioJourney.ogg', 1, loops=0)

#     def handle_change(self, values):
#         try:
#             print 'Triggered currentValues={}'.format(values)
#             play = False
#             for i in range(4):
#                 if values[i] == 0:
#                     play = True
#
#             if not self.wasPlaying:
#                 self.ambient_pos = self.player.get_pos()
#
#             if play:
#                 volume = 0.99
#                 self.wasPlaying = True
#                 if values[0] == 0:
#                         self.player.play_song('/home/pi/bluechz/sound/Success! - Blue Sky.ogg', volume)
#                 elif values[1] == 0:
#                         self.player.play_song('/home/pi/bluechz/sound/Failure 3 - Escape Velocity.ogg', volume)
#                 elif values[2] == 0:
#                         self.player.play_song('/home/pi/bluechz/sound/Failure 1 - Time Warp.ogg', volume)
#                 elif values[3] == 0:
#                         self.player.play_song('/home/pi/bluechz/sound/Intro Spiel.ogg', volume)
#             else:
#                 self.player.stop_music()
#                 self.player.play_song('/home/pi/bluechz/sound/LabAmbient.ogg', 0.35, loops=10)
#                 self.wasPlaying = False
#         except RuntimeError:
#             print 'got an error!'

# time.sleep(5)


# control = MusicControlSystem()

# while True:
#     control.leverController.check_for_new_switch_values()
#     continue
