from sound.MultiTrackMusicPlayer import MultiTrackMusicPlayer
import pygame
import time

OFF = -1
AMBIENT = 0
STARTUP = 1
ON = 2
TIME_STOP = 3
ENDING = 4

STARTUP_TIME = 16


class TimeMachineSoundSystem(object):
    player = MultiTrackMusicPlayer()
    wasPlaying = False
    time_speed = 0
    is_running = False
    current_mode = OFF
    startup_time = 0

    def __init__(self):
        self.player.set_volume(0.4)
        self.__play_ambient()

    def __play_ambient(self):
        print("Playing ambient")
        # self.player.play_song('/home/admin/explorey/sound/TimeMachineAmbient.ogg', 1, channel=AMBIENT)

    def __play_time_startup(self):
        self.player.play_song('/home/admin/explorey/sound/TimeMachine-Startup.ogg', 1, channel=STARTUP)

    def __play_time_traveling(self):
        self.player.play_song('/home/admin/explorey/sound/TimeMachine-Running.ogg', 1, channel=ON)

    def __play_time_frozen(self):
        self.player.play_song('/home/admin/explorey/sound/TimeMachine-Frozen.ogg', 1, channel=TIME_STOP)

    def __play_time_ending(self):
        self.player.play_song('/home/admin/explorey/sound/TimeMachine-Shutdown.ogg', 1, channel=ENDING)

    def update_sounds(self, is_running, time_speed):
        if not is_running and self.current_mode != OFF:
            self.__play_ambient()
            self.player.stop_music(STARTUP)
            self.player.stop_music(ON)
            self.player.stop_music(TIME_STOP)
            self.current_mode = OFF

        if is_running and self.current_mode == OFF or self.current_mode == AMBIENT:
            self.__play_time_startup()
            self.startup_time = time.time()
            self.player.stop_music(AMBIENT)
        elif self.current_mode == STARTUP and time.time() > self.startup_time + STARTUP_TIME:
            self.__play_time_traveling()
            self.__play_time_frozen()
            self.current_mode = ON
        if self.current_mode == ON:
            velocity = abs(time_speed) / 1000
            if velocity < .3:
                ratio = velocity / .3
                self.player.set_volume(ON, ratio)
                self.player.set_volume(TIME_STOP, 1 - ratio)
            else:
                self.player.set_volume(ON, 1)
                self.player.set_volume(TIME_STOP, 0)






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
