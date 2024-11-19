from sound.MultiTrackMusicPlayer import MultiTrackMusicPlayer
import random

OFF = -1
READY = 0
STARTUP = 1
BACKGROUND = 2
ENDING = 3
HIT_0 = 4
HIT_1 = 5
HIT_2 = 6
HIT_3 = 7
HIT_4 = 8
HIT_5 = 9
HIT_6 = 10
HIT_7 = 11
COUNTDOWN = 12

STARTUP_TIME = 10

CHANNEL_MUSIC = 1
CHANNEL_SOUNDS_A1 = 2
CHANNEL_SOUNDS_A2 = 3
CHANNEL_SOUNDS_B1 = 4
CHANNEL_SOUNDS_B2 = 5

CHANNEL_STARTUP = 6

songs = [
    '/home/admin/explorey/sound/Scale-ready.ogg',
    '/home/admin/explorey/sound/Scale-startup.ogg',
    '/home/admin/explorey/sound/Scale-background.ogg',
    '/home/admin/explorey/sound/Scale-ending.ogg',
    '/home/admin/explorey/sound/Scale-hit-0.ogg',
    '/home/admin/explorey/sound/Scale-hit-1.ogg',
    '/home/admin/explorey/sound/Scale-hit-2.ogg',
    '/home/admin/explorey/sound/Scale-hit-3.ogg',
    '/home/admin/explorey/sound/Scale-hit-4.ogg',
    '/home/admin/explorey/sound/Scale-hit-5.ogg',
    '/home/admin/explorey/sound/Scale-hit-6.ogg',
    '/home/admin/explorey/sound/Scale-hit-7.ogg',
    '/home/admin/explorey/sound/GhostScale-countdown.ogg',
]


class GhostScaleSoundSystem(object):
    player = MultiTrackMusicPlayer(songs, devicename='bcm2835 Headphones, bcm2835 Headphones')
    wasPlaying = False
    time_speed = 0
    is_running = False
    is_playing_countdown = False
    current_mode = OFF
    startup_time = 0
    A1 = False
    B1 = False

    def play_ready(self):
        self.player.stop_music(CHANNEL_MUSIC)
        self.player.play_song(READY, 0.6, channel_num=CHANNEL_MUSIC, loops=0)

    def play_startup(self):
        self.player.play_song(STARTUP, 0.4, channel_num=CHANNEL_STARTUP, loops=0)

    def play_countdown(self):
        print("Playing Countdown")
        self.player.play_song(COUNTDOWN, 1.0, channel_num=CHANNEL_MUSIC, loops=0)

    def play_background(self):
        self.player.stop_music(CHANNEL_MUSIC)
        self.player.play_song(BACKGROUND, 0.4, channel_num=CHANNEL_MUSIC, loops=-1)

    def play_ending(self):
        self.player.stop_music(CHANNEL_MUSIC)
        self.player.stop_music(CHANNEL_SOUNDS_A1)
        self.player.stop_music(CHANNEL_SOUNDS_A2)
        self.player.stop_music(CHANNEL_SOUNDS_B1)
        self.player.stop_music(CHANNEL_SOUNDS_B2)
        self.player.play_song(ENDING, 0.6, channel_num=CHANNEL_MUSIC, loops=0)

    def play_hit(self, left=True):
        if left:
            if self.A1:
                channel = CHANNEL_SOUNDS_A2
            else:
                channel = CHANNEL_SOUNDS_A1
            self.player.stop_music(channel)
            self.player.play_song(random.randint(HIT_0, HIT_3), 0.5, channel_num=channel, loops=0)
            self.player.channels[channel].set_volume(1.0, 0.0)
        else:
            if self.B1:
                channel = CHANNEL_SOUNDS_B2
            else:
                channel = CHANNEL_SOUNDS_B1
            self.player.stop_music(channel)
            self.player.play_song(random.randint(HIT_4, HIT_7), 0.5, channel_num=channel, loops=0)
            self.player.channels[channel].set_volume(0.0, 1.0)
