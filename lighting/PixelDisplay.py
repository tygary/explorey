from lighting.lib.led_matrix import Matrix


class PixelDisplay(object):
    matrix = Matrix()

    def draw_text(self, text):
        self.matrix.reset()
        self.matrix.text(text, (0, 0), 8, (255, 0, 0))
        self.matrix.show()

