import vlc


class GhostVideo(object):
    def __init__(self):
        self.player = vlc.MediaPlayer("/home/admin/explorey/ghost/ghost_pepper.mp4")
        self.player.play()

    def play(self):
        self.player.stop()
        self.player.play()