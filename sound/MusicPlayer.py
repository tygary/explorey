import pygame
import multiprocessing

class MusicPlayer:
    current_song = ''
    music_thread = None
    started = False
    volume = 1

    def __init__(self):
        self.__startup_mixer()

    def __startup_mixer(self):
        try:
            pygame.mixer.init(buffer=1024)
            self.started = True
            self.set_volume(self.volume)
        except Exception as err:
            print(f"Failed to start audio - {err}")

    def play_song(self, song, volume, pos=0.0, loops=-1):
        if not self.started:
            self.__startup_mixer()
        if self.started and (song != self.current_song or not self.is_still_playing()):
            self.stop_music()
            self.current_song = song
            #self.music_thread = multiprocessing.Process(target=self.__music_loop)
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.set_volume(volume)
            #pygame.mixer.music.set_pos(pos)
            pygame.mixer.music.play(loops=loops, start=pos)
            #self.music_thread.start()

    def is_still_playing(self):
        try:
            return pygame.mixer.music.get_busy() == True
        except:
            return False

    def stop_music(self):
        if self.started:
            #if self.music_thread is not None:
            #    self.music_thread.terminate()
            pygame.mixer.music.stop()
            pygame.mixer.music.rewind()

    def get_pos(self):
        return pygame.mixer.music.get_pos()

    def set_volume(self, amount):
        self.volume = amount
        if self.started:
            pygame.mixer.music.set_volume(amount)

    def __music_loop(self):

        pygame.mixer.stop()
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
