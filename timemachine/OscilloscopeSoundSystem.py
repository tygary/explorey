from sound.MusicPlayer import MusicPlayer
import time


MUSIC = [
    '/home/admin/explorey/sound/osc_spirals.wav'
]


class OscilloscopeSoundSystem(object):
    player = MusicPlayer()
    wasPlaying = False
    ambient_pos = 0.0
    time_speed = 0
    is_running = False

    def __init__(self):
        self.player.set_volume(0.4)
        self.__play_ambient()

    def __play_ambient(self):
        # self.player.play_song(MUSIC[0], 1)
        self.player.stop_music()

    def __play_time_frozen(self):
        self.player.play_song('/home/admin/explorey/sound/TimeFrozen.ogg', 1)

    def __play_time_traveling(self):
        self.player.play_song(MUSIC[0], 1)

    def update_sounds(self, active):
        if not self.is_running and not active:
            return

        if not self.is_running and active:
            self.__play_time_traveling()

        if self.is_running and not active:
            self.player.stop_music()







