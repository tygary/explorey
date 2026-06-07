import logging

import pygame

logger = logging.getLogger(__name__)


BACKGROUND           = 0
GAME_START           = 1
PUZZLE_COMPLETE      = 2
CORRECT_CONNECTION   = 3
INCORRECT_CONNECTION = 4
OUT_OF_TIME          = 5
RESET                = 6
YOU_WIN              = 7

_NUM_CHANNELS = 8

_song_paths = [
    '/home/admin/explorey/sound/Babel-Background.ogg',
    '/home/admin/explorey/sound/Babel-GameStart.ogg',
    '/home/admin/explorey/sound/Babel-PuzzleComplete.ogg',
    '/home/admin/explorey/sound/Babel-CorrectConnection.ogg',
    '/home/admin/explorey/sound/Babel-IncorrectConnection.ogg',
    '/home/admin/explorey/sound/Babel-OutOfTime.ogg',
    '/home/admin/explorey/sound/Babel-Reset.ogg',
    '/home/admin/explorey/sound/Babel-YouWin.ogg',
]


class BabelSoundSystem:
    def __init__(self):
        self._enabled = False
        self._sounds = [None] * _NUM_CHANNELS
        self._channels = []
        self._background_playing = False

        try:
            pygame.mixer.init(buffer=1024, devicename='bcm2835 Headphones, bcm2835 Headphones')
            pygame.mixer.set_num_channels(_NUM_CHANNELS)
            self._channels = [pygame.mixer.Channel(i) for i in range(_NUM_CHANNELS)]
            self._enabled = True
        except Exception:
            logger.exception("Failed to initialize pygame mixer — audio disabled")
            return

        for i, path in enumerate(_song_paths):
            try:
                self._sounds[i] = pygame.mixer.Sound(path)
            except Exception:
                logger.warning("Could not load sound file %s — that sound will be skipped", path)

    def _play(self, index, volume, loops=-1):
        if not self._enabled:
            return
        sound = self._sounds[index]
        if sound is None:
            return
        try:
            ch = self._channels[index]
            ch.stop()
            ch.play(sound, loops=loops)
            ch.set_volume(volume)
        except Exception:
            logger.exception("Error playing sound index %d", index)

    def _stop(self, index):
        if not self._enabled:
            return
        try:
            self._channels[index].stop()
        except Exception:
            logger.exception("Error stopping sound index %d", index)

    def stop_all(self):
        for i in range(_NUM_CHANNELS):
            self._stop(i)
        self._background_playing = False

    def _ensure_background(self):
        if not self._background_playing:
            self._play(BACKGROUND, 0.5, loops=-1)
            self._background_playing = True

    def play_game_start(self):
        logger.info("Babel audio: Game Start")
        self.stop_all()
        self._play(GAME_START, 0.8, loops=0)
        self._ensure_background()

    def play_puzzle_complete(self):
        logger.info("Babel audio: Puzzle Complete")
        self._play(PUZZLE_COMPLETE, 0.8, loops=0)

    def play_correct_connection(self):
        logger.info("Babel audio: Correct Connection")
        self._play(CORRECT_CONNECTION, 0.8, loops=0)

    def play_incorrect_connection(self):
        logger.info("Babel audio: Incorrect Connection")
        self._play(INCORRECT_CONNECTION, 0.8, loops=0)

    def play_out_of_time(self):
        logger.info("Babel audio: Out of Time")
        self._play(OUT_OF_TIME, 1.0, loops=0)

    def play_reset(self):
        logger.info("Babel audio: Reset")
        self.stop_all()
        self._play(RESET, 0.8, loops=0)

    def play_you_win(self):
        logger.info("Babel audio: You Win")
        self.stop_all()
        self._play(YOU_WIN, 0.8, loops=0)
