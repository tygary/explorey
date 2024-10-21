from sound.MultiTrackMusicPlayer import MultiTrackMusicPlayer


OFF = -1
GAME_START = 0
ON_0 = 1
ON_1 = 2
ON_2 = 3
ON_3 = 4
RUNNING_OUT_OF_TIME = 5
ENERGY_GAIN = 6
ROUND_SUCCESS = 7
GAME_OVER = 8
YOU_WIN = 9
PENDING_SWITCHBOARD = 10


STARTUP_TIME = 10

songs = [
    '/home/admin/explorey/sound/Game-Startup.ogg',
    '/home/admin/explorey/sound/Game-Running-1.ogg',
    '/home/admin/explorey/sound/Game-Running-2.ogg',
    '/home/admin/explorey/sound/Game-Running-3.ogg',
    '/home/admin/explorey/sound/Game-Running-4.ogg',
    '/home/admin/explorey/sound/Game-OutOfTime.ogg',
    '/home/admin/explorey/sound/Game-EnergyGain.ogg',
    '/home/admin/explorey/sound/Game-RoundWin-2.ogg',
    '/home/admin/explorey/sound/Game-Over.ogg',
    '/home/admin/explorey/sound/Game-YouWin.ogg',
    '/home/admin/explorey/sound/Game-PendingSwitches.ogg',
]


class RatGameSoundSystem(object):
    player = MultiTrackMusicPlayer(songs, num_channels=11)

    is_playing_ambient = False
    is_playing_running_out_of_time = False
    is_playing_pending_switchboard = False

    # def __init__(self):
    #     self.play_ambient()

    def stop_all(self):
        # self.player.stop_music(AMBIENT)
        self.player.stop_music(GAME_START)
        self.player.stop_music(ON_0)
        self.player.stop_music(ON_1)
        self.player.stop_music(ON_2)
        self.player.stop_music(ON_3)
        self.player.stop_music(RUNNING_OUT_OF_TIME)
        self.player.stop_music(ENERGY_GAIN)
        self.player.stop_music(ROUND_SUCCESS)
        self.player.stop_music(GAME_OVER)
        self.player.stop_music(YOU_WIN)
        self.player.stop_music(PENDING_SWITCHBOARD)
        self.is_playing_ambient = False
        self.is_playing_running_out_of_time = False
        self.is_playing_pending_switchboard = False

    def play_ambient(self):
        if not self.is_playing_ambient:
            # self.player.play_song(AMBIENT, 1, channel=AMBIENT)
            self.is_playing_ambient = True

    def play_game_start(self):
        print("Playing Game Start")
        self.stop_all()
        self.player.play_song(GAME_START, 0.5, channel=GAME_START, loops=0)

    def play_running(self, round_num):
        print("Playing Running", round_num)
        self.stop_all()
        index = ON_0 + round_num
        self.player.play_song(index, 0.5, channel=index)

    def play_running_out_of_time(self):
        if not self.is_playing_running_out_of_time:
            print("Playing Running out of time")
            self.player.play_song(RUNNING_OUT_OF_TIME, 1, channel=RUNNING_OUT_OF_TIME)
            self.is_playing_running_out_of_time = True

    def stop_running_out_of_time(self):
        if self.is_playing_running_out_of_time:
            print("Stopping Running out of time")
            self.player.stop_music(RUNNING_OUT_OF_TIME)
            self.is_playing_running_out_of_time = False

    def play_pending_switchboard(self):
        if not self.is_playing_pending_switchboard:
            print("Playing pending switchboard")
            self.player.play_song(PENDING_SWITCHBOARD, 1, channel=PENDING_SWITCHBOARD)
            self.is_playing_pending_switchboard = True

    def stop_pending_switchboard(self):
        if self.is_playing_pending_switchboard:
            print("Stopping Pending Switchboard")
            self.player.stop_music(PENDING_SWITCHBOARD)
            self.is_playing_pending_switchboard = False

    def play_energy_gain(self):
        print("Playing Energy Gain")
        self.player.play_song(ENERGY_GAIN, 1, channel=ENERGY_GAIN, loops=0)

    def play_round_success(self):
        print("Playing Round Success")
        self.stop_all()
        self.player.play_song(ROUND_SUCCESS, 0.8, channel=ROUND_SUCCESS, loops=0)

    def play_game_over(self):
        print("Playing Game Over")
        self.stop_all()
        self.player.play_song(GAME_OVER, 0.8, channel=GAME_OVER, loops=0)

    def play_you_win(self):
        print("Playing You Win")
        self.stop_all()
        self.player.play_song(YOU_WIN, 0.8, channel=YOU_WIN, loops=0)


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
