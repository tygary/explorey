from sound.MusicPlayer import MusicPlayer
import time
import random

AMBIENT = '/home/admin/explorey/sound/osc_ambient.wav'

MUSIC = [
    '/home/admin/explorey/sound/osc_asteroids.wav'
    '/home/admin/explorey/sound/osc_blocks.wav'
    '/home/admin/explorey/sound/osc_circles.wav'
    '/home/admin/explorey/sound/osc_deconstruct.wav'
    '/home/admin/explorey/sound/osc_dots.wav'
    '/home/admin/explorey/sound/osc_lines.wav'
    '/home/admin/explorey/sound/osc_planets.wav'
    '/home/admin/explorey/sound/osc_reconstruct.wav'
    '/home/admin/explorey/sound/osc_shrooms.wav'
    '/home/admin/explorey/sound/osc_spirals.wav'
]


class OscilloscopeSoundSystem(object):
    player = MusicPlayer()
    wasPlaying = False
    ambient_pos = 0.0
    time_speed = 0
    is_running = False
    ambient_playing = False

    def __init__(self):
        self.player.set_volume(0.4)
        self.__play_ambient()

    def __play_ambient(self):
        self.player.play_song(AMBIENT, 1)
        self.is_running = False
        self.ambient_playing = True

    def __play_time_traveling(self):
        choice = random.choice(MUSIC)
        self.player.play_song(choice, 1)
        self.is_running = True
        self.ambient_playing = False

    def update_sounds(self, active):
        if active and not self.is_running:
            self.__play_time_traveling()
        elif not active and not self.ambient_playing:
            self.__play_ambient()







