import pygame
import multiprocessing


class MultiTrackMusicPlayer:
    songs = []

    def __init__(self, songs):
        pygame.mixer.init(buffer=1024)

        for index in range(0, len(songs)):
            self.songs[index] = pygame.mixer.Sound(songs[index])

    def play_song(self, song_index, volume, pos=0.0, loops=-1, channel=0):
        print(f"Playing - {song_index} - channel {channel}")
        self.stop_music(channel=channel)

        music = pygame.mixer.Channel(channel)

        music.play(self.songs[song_index], loops=loops)
        music.set_volume(volume)

    def is_still_playing(self):
        try:
            return pygame.mixer.music.get_busy() == True
        except:
            return False

    def stop_music(self, channel=0):
        print(f"Stopping -  channel {channel}")
        pygame.mixer.Channel(channel).stop()

    def set_volume(self, channel, amount):
        print(f"Set Vol - {amount} - channel {channel}")
        pygame.mixer.Channel(channel).set_volume(amount)
