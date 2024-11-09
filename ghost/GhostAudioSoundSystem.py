from sound.MultiTrackMusicPlayer import MultiTrackMusicPlayer


CHANNEL_AMBIENT = 0
CHANNEL_VOICE = 1
CHANNEL_FX = 2
CHANNEL_OUT_OF_TIME = 3
CHANNEL_FX_2 = 4

OFF = -1
INTRO_SCAN = 0
ENGAGE_NUMINSITY = 1
INITIATE_FLUX = 2
INCREASE_AURARAL = 3
DECREASE_AURARAL = 4
ACTIVATE_CHRONOMETER = 5
DEACTIVATE_CHRONOMETER = 6
INCREASE_INSULATION = 7
DECREASE_INSULATION = 8
MAGNETIZE_MATRIX = 9
INCREASE_ACCELERATOR = 10
DETERMINE_ACCELERATOR = 11
GAME_OVER = 12
YOU_WIN = 13
PUT_BACK_HEADPHONES = 14

AMBIENT = 15
STARTUP = 16
OUT_OF_TIME = 17
OBJECTIVE_COMPLETED = 18
SPIN_DOWN = 19
GAME_BACKGROUND = 20
MACHINE_SUCCESS = 21
STORY_INTRO_SOUNDS = 22

STARTUP_TIME = 10

songs = [
    '/home/admin/explorey/sound/GhostAudio-intro_scan.ogg',
    '/home/admin/explorey/sound/GhostAudio-engage_numinosity.ogg',
    '/home/admin/explorey/sound/GhostAudio-initiate_flux.ogg',
    '/home/admin/explorey/sound/GhostAudio-increase_auraral.ogg',
    '/home/admin/explorey/sound/GhostAudio-decrease_auraral.ogg',
    '/home/admin/explorey/sound/GhostAudio-activate_chronometer.ogg',
    '/home/admin/explorey/sound/GhostAudio-deactivate_chronometer.ogg',
    '/home/admin/explorey/sound/GhostAudio-increase_insulation.ogg',
    '/home/admin/explorey/sound/GhostAudio-decrease_insulation.ogg',
    '/home/admin/explorey/sound/GhostAudio-magnetize_matrix.ogg',
    '/home/admin/explorey/sound/GhostAudio-increase_accelerator.ogg',
    '/home/admin/explorey/sound/GhostAudio-determine_accelerator.ogg',
    '/home/admin/explorey/sound/GhostAudio-game_over.ogg',
    '/home/admin/explorey/sound/GhostAudio-you_win.ogg',
    '/home/admin/explorey/sound/GhostAudio-put_back_headphones.ogg',

    '/home/admin/explorey/sound/GhostAudio-ambient.ogg',
    '/home/admin/explorey/sound/GhostAudio-startup.ogg',
    '/home/admin/explorey/sound/Game-OutOfTime.ogg',
    '/home/admin/explorey/sound/GhostAudio-objective_completed.ogg',
    '/home/admin/explorey/sound/GhostAudio-spin_down.ogg',
    '/home/admin/explorey/sound/GhostAudio-game_background.ogg',
    '/home/admin/explorey/sound/GhostAudio-machine_success.ogg',
    '/home/admin/explorey/sound/GhostAudio-story_intro_sounds.ogg',
    '/home/admin/explorey/sound/GhostAudio-scanning.ogg',
]


class GhostAudioSoundSystem(object):
    player = MultiTrackMusicPlayer(songs, num_channels=11)

    is_playing_ambient = False
    is_playing_running_out_of_time = False
    is_playing_game_background = False

    next_event_callback = None

    def stop_all(self):
        self.player.stop_music(CHANNEL_AMBIENT)
        self.player.stop_music(CHANNEL_VOICE)
        self.player.stop_music(CHANNEL_FX)
        self.player.stop_music(CHANNEL_OUT_OF_TIME)
        self.is_playing_ambient = False
        self.is_playing_running_out_of_time = False
        self.is_playing_pending_switchboard = False

    # ----------------------------

    def play_intro_scan(self):
        print("Playing Intro Scan")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(INTRO_SCAN, 1, channel_num=CHANNEL_VOICE, loops=0)
        self.player.queue_song(ENGAGE_NUMINSITY, 1, channel_num=CHANNEL_VOICE, loops=0)
    
    def play_engage_numinsity(self):
        print("Playing Engage Numinsity")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(ENGAGE_NUMINSITY, 1, channel_num=CHANNEL_VOICE, loops=0)

    def play_initiate_flux(self):
        print("Playing Initiate Flux")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(INITIATE_FLUX, 1, channel_num=CHANNEL_VOICE, loops=0)
    
    def play_increase_auraral(self):
        print("Playing Increase Auraral")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(INCREASE_AURARAL, 1, channel_num=CHANNEL_VOICE, loops=0)
    
    def play_decrease_auraral(self):
        print("Playing Decrease Auraral")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(DECREASE_AURARAL, 1, channel_num=CHANNEL_VOICE, loops=0)
    
    def play_activate_chronometer(self):
        print("Playing Activate Chronometer")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(ACTIVATE_CHRONOMETER, 1, channel_num=CHANNEL_VOICE, loops=0)
    
    def play_deactivate_chronometer(self):
        print("Playing Deactivate Chronometer")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(DEACTIVATE_CHRONOMETER, 1, channel_num=CHANNEL_VOICE, loops=0)
    
    def play_increase_insulation(self):
        print("Playing Increase Insulation")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(INCREASE_INSULATION, 1, channel_num=CHANNEL_VOICE, loops=0)

    def play_decrease_insulation(self):
        print("Playing Decrease Insulation")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(DECREASE_INSULATION, 1, channel_num=CHANNEL_VOICE, loops=0)

    def play_magnetize_matrix(self):
        print("Playing Magnetize Matrix")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(MAGNETIZE_MATRIX, 1, channel_num=CHANNEL_VOICE, loops=0)

    def play_increase_accelerator(self):
        print("Playing Increase Accelerator")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(INCREASE_ACCELERATOR, 1, channel_num=CHANNEL_VOICE, loops=0)

    def play_determine_accelerator(self):
        print("Playing Determine Accelerator")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(DETERMINE_ACCELERATOR, 1, channel_num=CHANNEL_VOICE, loops=0)

    def play_game_over(self):
        print("Playing Game Over")
        self.stop_all()
        self.player.play_song(GAME_OVER, 1, channel_num=CHANNEL_VOICE, loops=0)
        self.player.play_song(SPIN_DOWN, 1, channel_num=CHANNEL_FX, loops=0)

    def play_you_win(self):
        print("Playing You Win")
        self.stop_all()
        self.player.play_song(YOU_WIN, 1, channel_num=CHANNEL_VOICE, loops=0)
        self.player.play_song(MACHINE_SUCCESS, 1, channel_num=CHANNEL_FX, loops=0)

    def queue_put_back_headphones(self):
        print("Playing Put Back Headphones")
        self.stop_all()
        self.player.play_song(PUT_BACK_HEADPHONES, 1, channel_num=CHANNEL_VOICE, loops=0)

    # ----------------------------

    def play_ambient(self):
        if not self.is_playing_ambient:
            # self.player.play_song(AMBIENT, 1, channel=AMBIENT)
            self.is_playing_ambient = True
            self.player.play_song(AMBIENT, 0.5, channel_num=CHANNEL_AMBIENT, loops=-1)

    def play_game_backround(self):
        if not self.is_playing_game_background:
            print("Playing game background")
            self.stop_all()
            self.player.play_song(GAME_BACKGROUND, 0.5, channel_num=AMBIENT, loops=-1)
            self.is_playing_game_background = True

    def play_running_out_of_time(self):
        if not self.is_playing_running_out_of_time:
            print("Playing Running out of time")
            self.player.play_song(OUT_OF_TIME, 1, channel_num=CHANNEL_OUT_OF_TIME, loops=-1)
            self.is_playing_running_out_of_time = True

    def stop_running_out_of_time(self):
        if self.is_playing_running_out_of_time:
            print("Stopping Running out of time")
            self.player.stop_music(CHANNEL_OUT_OF_TIME)
            self.is_playing_running_out_of_time = False

    def play_objective_completed(self):
        print("Playing Objective Completed")
        self.player.play_song(OBJECTIVE_COMPLETED, 1, channel_num=CHANNEL_FX, loops=0)

    def play_spin_down(self):
        print("Playing Spin Down")
        self.player.play_song(SPIN_DOWN, 1, channel_num=CHANNEL_FX_2, loops=0)

    def play_startup(self):
        print("Playing Startup")
        self.player.play_song(STARTUP, 1, channel_num=CHANNEL_FX_2, loops=0)

    def play_scanning(self):
        print("Playing Scanning")
        self.player.play_song(INTRO_SCAN, 1, channel_num=CHANNEL_FX_2, loops=0)

    def queue_ghost_story(self, rfid):
        # story = GHOST_STORIES_BY_RFID[rfid]
        self.player.queue_song(STORY_INTRO_SOUNDS, 1, channel_num=CHANNEL_VOICE, loops=0)
        # self.player.queue_temp_song(story, 1, channel=CHANNEL_VOICE, loops=0)
        self.player.queue_song(PUT_BACK_HEADPHONES, channel=CHANNEL_VOICE, loops=0)

    def set_next_event_callback(self, callback):
        self.next_event_callback = callback

    def is_still_playing(self, channel_num):
        return self.player.is_still_playing(channel_num)

    def tick(self):
        if self.next_event_callback is not None and not self.player.is_still_playing():
            self.next_event_callback()
            self.next_event_callback = None


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

GHOST_STORIES_BY_RFID = {}
