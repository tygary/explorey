from sound.MusicPlayer import MusicPlayer
import time

class MusicControlSystem(object):

    player = MusicPlayer()
    wasPlaying = False
    ambient_pos = 0.0

    def __init__(self):
        self.player.set_volume(0.4)

    def play_space(self):
        self.player.play_song('/home/admin/explorey/sound/explorey-space-pasture.ogg', 1)

    def play_bowling(self):
        self.player.play_song('/home/admin/explorey/sound/exploreysounds-bowlung.ogg', 1)

    def play_cave_ambient(self):
        self.player.play_song('/home/admin/explorey/sound/CaveAmbient.ogg', 1)

    def play_bats_ambient(self):
        self.player.play_song('/home/admin/explorey/sound/CaveBackground.ogg', 1)

    def play_bat_journey(self):
        self.player.play_song('/home/admin/explorey/sound/BatAudioJourney.ogg', 1, loops=0)

#     def handle_change(self, values):
#         try:
#             print 'Triggered currentValues={}'.format(values)
#             play = False
#             for i in range(4):
#                 if values[i] == 0:
#                     play = True
#
#             if not self.wasPlaying:
#                 self.ambient_pos = self.player.get_pos()
#
#             if play:
#                 volume = 0.99
#                 self.wasPlaying = True
#                 if values[0] == 0:
#                         self.player.play_song('/home/pi/bluechz/sound/Success! - Blue Sky.ogg', volume)
#                 elif values[1] == 0:
#                         self.player.play_song('/home/pi/bluechz/sound/Failure 3 - Escape Velocity.ogg', volume)
#                 elif values[2] == 0:
#                         self.player.play_song('/home/pi/bluechz/sound/Failure 1 - Time Warp.ogg', volume)
#                 elif values[3] == 0:
#                         self.player.play_song('/home/pi/bluechz/sound/Intro Spiel.ogg', volume)
#             else:
#                 self.player.stop_music()
#                 self.player.play_song('/home/pi/bluechz/sound/LabAmbient.ogg', 0.35, loops=10)
#                 self.wasPlaying = False
#         except RuntimeError:
#             print 'got an error!'

# time.sleep(5)


# control = MusicControlSystem()

# while True:
#     control.leverController.check_for_new_switch_values()
#     continue
