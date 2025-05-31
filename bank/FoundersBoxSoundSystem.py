from sound.MultiTrackMusicPlayer import MultiTrackMusicPlayer
import random

OFF = -1
BACKGROUND = 0
LEVER = 1
OPEN = 2

CHANNEL_MUSIC = 1
CHANNEL_LEVER = 2
CHANNEL_OPEN = 3

songs = [
    '/home/admin/explorey/sound/VaultAmbient.ogg',
    '/home/admin/explorey/sound/BoxLever.ogg',
    '/home/admin/explorey/sound/BoxUnlock.ogg',
]


class FoundersBoxSoundSystem(object):
    player = MultiTrackMusicPlayer(songs, devicename='bcm2835 Headphones, bcm2835 Headphones')

    def play_lever(self):
        if not self.player.is_still_playing(CHANNEL_LEVER):
            self.player.play_song(LEVER, 0.6, channel_num=CHANNEL_LEVER, loops=0)

    def play_open(self):
        self.player.stop_music(CHANNEL_OPEN)
        self.player.play_song(OPEN, 0.4, channel_num=CHANNEL_OPEN, loops=0)

    def play_background(self):
        self.player.stop_music(CHANNEL_MUSIC)
        self.player.play_song(BACKGROUND, 0.4, channel_num=CHANNEL_MUSIC, loops=-1)
