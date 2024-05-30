from sound.MultiTrackMusicPlayer import MultiTrackMusicPlayer
import pygame
import time
import random





OFF = -1
AMBIENT = 0
GAME_START = 1
ON = 2
RUNNING_OUT_OF_TIME = 3
ENERGY_GAIN = 4
ROUND_SUCCESS = 5
GAME_OVER = 6
YOU_WIN = 7


STARTUP_TIME = 10

songs = [
    '/home/admin/explorey/sound/CaveAmbient.ogg',
    '/home/admin/explorey/sound/TimeMachine-Startup.ogg',
    '/home/admin/explorey/sound/TimeMachine-Running.ogg',
    '/home/admin/explorey/sound/TimeMachine-Frozen.ogg',
    '/home/admin/explorey/sound/exploreysounds-bowlung.ogg',
    '/home/admin/explorey/sound/TimeMachine-Shutdown.ogg',
    '/home/admin/explorey/sound/explorey-space-pasture.ogg',
    '/home/admin/explorey/sound/exploreysounds-bowlung.ogg',
]


class RatGameSoundSystem(object):
    player = MultiTrackMusicPlayer(songs)

    is_playing_ambient = False
    is_playing_running_out_of_time = False

    def __init__(self):
        self.play_ambient()

    def stop_all(self):
        self.player.stop_music(AMBIENT)
        self.player.stop_music(GAME_START)
        self.player.stop_music(ON)
        self.player.stop_music(RUNNING_OUT_OF_TIME)
        self.player.stop_music(ENERGY_GAIN)
        self.player.stop_music(ROUND_SUCCESS)
        self.player.stop_music(GAME_OVER)
        self.player.stop_music(YOU_WIN)
        self.is_playing_ambient = False
        self.is_playing_running_out_of_time = False

    def play_ambient(self):
        if not self.is_playing_ambient:
            self.player.play_song(AMBIENT, 1, channel=AMBIENT)
            self.is_playing_ambient = True

    def play_game_start(self):
        self.stop_all()
        self.player.play_song(GAME_START, 1, channel=GAME_START, loops=0)

    def play_running(self):
        self.player.play_song(ON, 1, channel=ON)

    def play_running_out_of_time(self):
        if not self.is_playing_running_out_of_time:
            self.player.play_song(RUNNING_OUT_OF_TIME, 1, channel=RUNNING_OUT_OF_TIME)
            self.is_playing_running_out_of_time = True

    def stop_running_out_of_time(self):
        if self.is_playing_running_out_of_time:
            self.player.stop_music(RUNNING_OUT_OF_TIME)
            self.is_playing_running_out_of_time = False

    def play_energy_gain(self):
        self.player.play_song(ENERGY_GAIN, 1, channel=ENERGY_GAIN, loops=0)

    def play_round_success(self):
        self.stop_all()
        self.player.play_song(ROUND_SUCCESS, 1, channel=ROUND_SUCCESS, loops=0)

    def play_game_over(self):
        self.stop_all()
        self.player.play_song(GAME_OVER, 1, channel=GAME_OVER, loops=0)

    def play_you_win(self):
        self.stop_all()
        self.player.play_song(YOU_WIN, 1, channel=YOU_WIN, loops=0)


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
