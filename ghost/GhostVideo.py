import vlc
import os


class GhostVideo(object):
    def __init__(self):
        os.environ["XDG_RUNTIME_DIR"] = "/tmp/xdg"
        self.player = vlc.MediaPlayer("/home/admin/explorey/ghost/peppers_other_ghost.mp4")
        self.player.play()
        pass

    def play(self):
        self.player.stop()
        self.player.play()
        pass