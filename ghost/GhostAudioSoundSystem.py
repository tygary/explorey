import threading
from sound.MultiTrackMusicPlayer import MultiTrackMusicPlayer


CHANNEL_AMBIENT = 0
CHANNEL_VOICE = 1
CHANNEL_FX = 2
CHANNEL_OUT_OF_TIME = 3
CHANNEL_FX_2 = 4
# Objective sound channels (for simultaneous playback)
CHANNEL_OBJECTIVE_1 = 5
CHANNEL_OBJECTIVE_2 = 6
CHANNEL_OBJECTIVE_3 = 7
CHANNEL_OBJECTIVE_4 = 8
CHANNEL_OBJECTIVE_5 = 9

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
MACHINE_SCANNING = 23

STARTUP_TIME = 10

songs = [
    '/home/admin/explorey/sound/GhostAudio-IntroNew.ogg',
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

    next_event_callbacks = None
    
    # Channel management for objective sounds (class constant)
    objective_channels = [CHANNEL_OBJECTIVE_1, CHANNEL_OBJECTIVE_2, CHANNEL_OBJECTIVE_3, CHANNEL_OBJECTIVE_4, CHANNEL_OBJECTIVE_5]
    
    def __init__(self):
        """Initialize the sound system and reset available channels."""
        self.available_objective_channels = self.objective_channels.copy()
        self.objective_sound_delay_counter = 0  # Track delay for staggered playback
    
    def _get_available_objective_channel(self):
        """Get an available channel for objective sounds. Returns None if all channels are in use."""
        # Clean up finished channels
        self._cleanup_finished_channels()
        
        if len(self.available_objective_channels) > 0:
            return self.available_objective_channels.pop(0)
        return None
    
    def _release_objective_channel(self, channel):
        """Release a channel back to the available pool."""
        if channel is not None and channel not in self.available_objective_channels:
            self.available_objective_channels.append(channel)
    
    def _cleanup_finished_channels(self):
        """Check all objective channels and release any that have finished playing."""
        finished_channels = []
        for channel in self.objective_channels:
            if channel not in self.available_objective_channels:
                if not self.player.is_still_playing(channel):
                    finished_channels.append(channel)
        
        for channel in finished_channels:
            self._release_objective_channel(channel)
    
    def stop_all_objective_sounds(self):
        """Stop all objective sounds and release their channels."""
        for channel in self.objective_channels:
            self.player.stop_music(channel)
        self.available_objective_channels = self.objective_channels.copy()
        self.objective_sound_delay_counter = 0  # Reset delay counter for new batch

    def stop_all(self):
        self.player.stop_music(CHANNEL_AMBIENT)
        self.player.stop_music(CHANNEL_VOICE)
        self.player.stop_music(CHANNEL_FX)
        self.player.stop_music(CHANNEL_OUT_OF_TIME)
        self.is_playing_ambient = False
        self.is_playing_running_out_of_time = False
        self.is_playing_pending_switchboard = False
        self.stop_all_objective_sounds()

    # ----------------------------

    def play_intro_scan(self):
        print("Playing Intro Scan")
        self.player.stop_music(CHANNEL_VOICE)
        self.player.play_song(INTRO_SCAN, 1, channel_num=CHANNEL_VOICE, loops=0)
        self.player.queue_song(ENGAGE_NUMINSITY, channel_num=CHANNEL_VOICE)
    
    def _play_objective_sound_with_delay(self, song_index, delay_seconds):
        """Internal method to play an objective sound after a delay."""
        def play_delayed():
            channel = self._get_available_objective_channel()
            if channel is not None:
                self.player.play_song(song_index, 1, channel_num=channel, loops=0)
            else:
                print(f"No available channels for song {song_index}")
        
        if delay_seconds > 0:
            timer = threading.Timer(delay_seconds, play_delayed)
            timer.start()
        else:
            play_delayed()

    def play_engage_numinsity(self):
        """Play Engage Numinsity on an available objective channel with staggered delay."""
        print("Playing Engage Numinsity")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(ENGAGE_NUMINSITY, delay)

    def play_initiate_flux(self):
        """Play Initiate Flux on an available objective channel with staggered delay."""
        print("Playing Initiate Flux")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(INITIATE_FLUX, delay)
    
    def play_increase_auraral(self):
        """Play Increase Auraral on an available objective channel with staggered delay."""
        print("Playing Increase Auraral")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(INCREASE_AURARAL, delay)
    
    def play_decrease_auraral(self):
        """Play Decrease Auraral on an available objective channel with staggered delay."""
        print("Playing Decrease Auraral")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(DECREASE_AURARAL, delay)
    
    def play_activate_chronometer(self):
        """Play Activate Chronometer on an available objective channel with staggered delay."""
        print("Playing Activate Chronometer")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(ACTIVATE_CHRONOMETER, delay)
    
    def play_deactivate_chronometer(self):
        """Play Deactivate Chronometer on an available objective channel with staggered delay."""
        print("Playing Deactivate Chronometer")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(DEACTIVATE_CHRONOMETER, delay)
    
    def play_increase_insulation(self):
        """Play Increase Insulation on an available objective channel with staggered delay."""
        print("Playing Increase Insulation")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(INCREASE_INSULATION, delay)

    def play_decrease_insulation(self):
        """Play Decrease Insulation on an available objective channel with staggered delay."""
        print("Playing Decrease Insulation")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(DECREASE_INSULATION, delay)

    def play_magnetize_matrix(self):
        """Play Magnetize Matrix on an available objective channel with staggered delay."""
        print("Playing Magnetize Matrix")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(MAGNETIZE_MATRIX, delay)

    def play_increase_accelerator(self):
        """Play Increase Accelerator on an available objective channel with staggered delay."""
        print("Playing Increase Accelerator")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(INCREASE_ACCELERATOR, delay)

    def play_determine_accelerator(self):
        """Play Determine Accelerator on an available objective channel with staggered delay."""
        print("Playing Determine Accelerator")
        delay = self.objective_sound_delay_counter * 1.0  # 1 second per sound
        self.objective_sound_delay_counter += 1
        self._play_objective_sound_with_delay(DETERMINE_ACCELERATOR, delay)

    def play_game_over(self):
        print("Playing Game Over")
        self.stop_all()
        self.player.play_song(GAME_OVER, 1, channel_num=CHANNEL_VOICE, loops=0)
        self.player.play_song(SPIN_DOWN, 0.5, channel_num=CHANNEL_FX, loops=0)

    def play_you_win(self):
        print("Playing You Win")
        self.stop_all()
        self.player.play_song(YOU_WIN, 1, channel_num=CHANNEL_VOICE, loops=0)
        self.player.play_song(MACHINE_SUCCESS, 0.5, channel_num=CHANNEL_FX, loops=0)

    def play_put_back_headphones(self):
        print("Playing Put Back Headphones")
        self.stop_all()
        self.player.play_song(PUT_BACK_HEADPHONES, 1, channel_num=CHANNEL_VOICE, loops=0)

    # ----------------------------

    def play_ambient(self):
        if not self.is_playing_ambient:
            # self.player.play_song(AMBIENT, 1, channel=AMBIENT)
            self.is_playing_ambient = True
            self.player.play_song(AMBIENT, 0.3, channel_num=CHANNEL_AMBIENT, loops=-1)

    def play_game_backround(self):
        if not self.is_playing_game_background:
            print("Playing game background")
            self.stop_all()
            self.player.play_song(GAME_BACKGROUND, 0.3, channel_num=CHANNEL_AMBIENT, loops=-1)
            self.is_playing_game_background = True

    def play_running_out_of_time(self):
        if not self.is_playing_running_out_of_time:
            print("Playing Running out of time")
            self.player.play_song(OUT_OF_TIME, 1.0, channel_num=CHANNEL_OUT_OF_TIME, loops=-1)
            self.is_playing_running_out_of_time = True

    def stop_running_out_of_time(self):
        if self.is_playing_running_out_of_time:
            print("Stopping Running out of time")
            self.player.stop_music(CHANNEL_OUT_OF_TIME)
            self.is_playing_running_out_of_time = False

    def play_objective_completed(self):
        print("Playing Objective Completed")
        self.player.play_song(OBJECTIVE_COMPLETED, 0.5, channel_num=CHANNEL_FX, loops=0)

    def play_spin_down(self):
        print("Playing Spin Down")
        self.player.play_song(SPIN_DOWN, 0.3, channel_num=CHANNEL_FX_2, loops=0)

    def play_startup(self):
        print("Playing Startup")
        self.player.play_song(STARTUP, 0.3, channel_num=CHANNEL_FX_2, loops=0)

    def play_scanning(self):
        print("Playing Scanning")
        self.player.play_song(MACHINE_SCANNING, 0.3, channel_num=CHANNEL_FX_2, loops=0)

    def play_story_intro_sounds(self):
        print("Playing Story Intro Sounds")
        self.stop_all()
        self.player.play_song(STORY_INTRO_SOUNDS, 0.3, channel_num=CHANNEL_VOICE, loops=0)

    def play_ghost_story(self, rfid):
        print("Playing Ghost Story")
        self.stop_all()
        story = GHOST_STORIES_BY_RFID.get(rfid)
        if story is None:
            print("No story found for RFID", rfid)
            return
        self.player.play_temp_song(story, 1, channel_num=CHANNEL_VOICE, loops=0)

    def set_next_event_callbacks(self, callbacks):
        print("Setting audio next event callback")
        self.next_event_callbacks = callbacks

    def is_still_playing(self, channel_num):
        return self.player.is_still_playing(channel_num)

    def tick(self):
        if self.next_event_callbacks is not None and len(self.next_event_callbacks) > 0 and not self.player.is_still_playing(CHANNEL_VOICE):
            print("Calling audio next event callbacks", self.next_event_callbacks)
            self.next_event_callback = self.next_event_callbacks.pop(0)
            try:
                self.next_event_callback()
            except Exception as e:
                print("Error calling next event callback", e)
            if (len(self.next_event_callbacks) == 0):
                self.next_event_callbacks = None


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

GHOST_STORIES_BY_RFID = {
    "test": '/home/admin/explorey/sound/GhostAudio-story_1.ogg',
    "4b541366080104e0": '/home/admin/explorey/sound/GhostAudio-story_2.ogg',
    "234c1366080104e0": '/home/admin/explorey/sound/GhostAudio-story_3.ogg',
    "d3401366080104e0": '/home/admin/explorey/sound/GhostAudio-story_4.ogg',
    "6d351366080104e0": '/home/admin/explorey/sound/GhostAudio-story_5.ogg',
    "e92e1366080104e0": '/home/admin/explorey/sound/GhostAudio-story_6.ogg',
    "f9251366080104e0": '/home/admin/explorey/sound/GhostAudio-story_7.ogg',
    "b31f1366080104e0": '/home/admin/explorey/sound/GhostAudio-story_8.ogg',
    "9f451366080104e0": '/home/admin/explorey/sound/GhostAudio-story_9.ogg',
    "b0371366080104e0": '/home/admin/explorey/sound/GhostAudio-story_10.ogg',
    "d12a1366080104e0": '/home/admin/explorey/sound/GhostAudio-story_11.ogg',
    "df861366080104e0": '/home/admin/explorey/sound/GhostAudio-story_13.ogg',
    "7da31366080104e0": '/home/admin/explorey/sound/GhostAudio-story_14.ogg',
    "3961366080104": '/home/admin/explorey/sound/GhostAudio-story_15.ogg',
    "f1891366080104e0": '/home/admin/explorey/sound/GhostAudio-story_16.ogg',
    "51b81366080104e0": '/home/admin/explorey/sound/GhostAudio-story_17.ogg',
    "f17e1366080104e0": '/home/admin/explorey/sound/GhostAudio-story_18.ogg',
    "16f81366080104e0": '/home/admin/explorey/sound/GhostAudio-story_20.ogg',
    "503b1566080104e0": '/home/admin/explorey/sound/GhostAudio-story_21.ogg',
    "e0661366080104e0": '/home/admin/explorey/sound/GhostAudio-story_22.ogg',
    "2a5e1366080104e0": '/home/admin/explorey/sound/GhostAudio-story_23.ogg',
    "1eb11466080104e0": '/home/admin/explorey/sound/GhostAudio-story_24.ogg',
    "36c81466080104e0": '/home/admin/explorey/sound/GhostAudio-story_25.ogg',
    "bebc1466080104e0": '/home/admin/explorey/sound/GhostAudio-story_25.ogg',
    "0dd31466080104e0": '/home/admin/explorey/sound/GhostAudio-story_25.ogg',
    "d1e81466080104e0": '/home/admin/explorey/sound/GhostAudio-story_26.ogg',
    "e2de1466080104e0": '/home/admin/explorey/sound/GhostAudio-story_28.ogg',
    "9bee1466080104e0": '/home/admin/explorey/sound/GhostAudio-story_30.ogg',
    "82421466080104": '/home/admin/explorey/sound/GhostAudio-story_31.ogg',
    "1a351466080104e0": '/home/admin/explorey/sound/GhostAudio-story_32.ogg',
    "a61a1566080104e0": '/home/admin/explorey/sound/GhostAudio-story_33.ogg',
    "9d291466080104e0": '/home/admin/explorey/sound/GhostAudio-story_34.ogg',
    "1ed81366080104e0": '/home/admin/explorey/sound/GhostAudio-story_35.ogg',
    "c0ed1366080104e0": '/home/admin/explorey/sound/GhostAudio-story_35.ogg',
    "d8f91366080104e0": '/home/admin/explorey/sound/GhostAudio-story_35.ogg',
    "e4e21366080104e0": '/home/admin/explorey/sound/GhostAudio-story_35.ogg',
    "28051466080104e0": '/home/admin/explorey/sound/GhostAudio-story_35.ogg',
    "02dd1466080104e0": '/home/admin/explorey/sound/GhostAudio-story_36.ogg',
    "94f41466080104e0": '/home/admin/explorey/sound/GhostAudio-story_36.ogg',
    "58031466080104e0": '/home/admin/explorey/sound/GhostAudio-story_36.ogg',
    "38d11466080104e0": '/home/admin/explorey/sound/GhostAudio-story_36.ogg',
    "780d1566080104e0": '/home/admin/explorey/sound/GhostAudio-story_37.ogg',
    "dc251566080104e0": '/home/admin/explorey/sound/GhostAudio-story_39.ogg',
    "85511566080104e0": '/home/admin/explorey/sound/GhostAudio-story_40.ogg',
    "622d1566080104e0": '/home/admin/explorey/sound/GhostAudio-story_41.ogg',
    "553b1566080104e0": '/home/admin/explorey/sound/GhostAudio-story_42.ogg',
    "3efe1466080104e0": '/home/admin/explorey/sound/GhostAudio-story_43.ogg',
    "3a221566080104e0": '/home/admin/explorey/sound/GhostAudio-44.ogg',
    "d2331466080104e0": '/home/admin/explorey/sound/GhostAudio-45.ogg',
    "4d281466080104e0": '/home/admin/explorey/sound/GhostAudio-46.ogg',
    "c61c1466080104e0": '/home/admin/explorey/sound/GhostAudio-47.ogg',
    "fe161566080104e0": '/home/admin/explorey/sound/GhostAudio-48.ogg',
    "ad0b1566080104e0": '/home/admin/explorey/sound/GhostAudio-49.ogg',
}
