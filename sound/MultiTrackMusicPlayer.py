import pygame
import multiprocessing


class MultiTrackMusicPlayer:

    def __init__(self):
        pygame.mixer.init(buffer=1024)

    def play_song(self, song, volume, pos=0.0, loops=-1, channel=0):
        self.stop_music(channel=channel)

        music = pygame.mixer.Channel(channel)

        music.play(pygame.mixer.sound(song), loops=loops, start=pos)
        music.set_volume(volume)

    def is_still_playing(self):
        try:
            return pygame.mixer.music.get_busy() == True
        except:
            return False

    def stop_music(self, channel=0):
        pygame.mixer.Channel(channel).stop()

    def set_volume(self, channel, amount):
        pygame.mixer.Channel(channel).set_volume(amount)
