import pygame
import multiprocessing


class MultiTrackMusicPlayer:
    songs = []
    channels = []

    def __init__(self, songs, num_channels=8, devicename='bcm2835 Headphones, bcm2835 Headphones'):
        pygame.mixer.init(buffer=1024, devicename=devicename)
        pygame.mixer.set_num_channels(num_channels)

        for song in songs:
            self.songs.append(pygame.mixer.Sound(song))

        for i in range(num_channels):
            self.channels.append(pygame.mixer.Channel(i))

    def play_song(self, song_index, volume, loops=-1, channel_num=0):
        channel = self.channels[channel_num]
        channel.stop()

        channel.play(self.songs[song_index], loops=loops)
        channel.set_volume(volume)

    def queue_song(self, song_index, channel_num=0):
        channel = self.channels[channel_num]
        channel.queue(self.songs[song_index])

    def play_temp_song(self, song_path, volume, pos=0.0, loops=0, channel_num=0):
        channel = self.channels[channel_num]
        sound = pygame.mixer.Sound(song_path)
        channel.play(sound, loops=loops)
        channel.set_volume(volume)

    def is_still_playing(self, channel_num=0):
        channel = self.channels[channel_num]
        try:
            print("Checking if music is still playing", channel.get_busy())
            return channel.get_busy() is True
            # return pygame.mixer.music.get_busy() == True
        except Exception as e:
            print("Error checking if music is still playing", e)
            return False

    def stop_music(self, channel=0):
        channel = self.channels[channel]
        channel.stop()

    def set_volume(self, channel, amount):
        channel = self.channels[channel].set_volume(amount)
