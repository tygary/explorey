from random import randint, randrange


def get_grb_color(color):
    return [color[1], color[0], color[2], color[3]]


class Colors(object):
    red = [250, 0, 0, 0]
    green = [0, 255, 0, 0]
    blue = [0, 0, 255, 0]

    orange = [255, 184, 3, 0]
    yellow = [230, 255, 4, 0]

    bright_white = [100, 100, 100, 200]
    soft_white = [20, 20, 20, 100]
    white = [255, 255, 255, 0]

    mid_green = [150, 250, 0, 50]
    light_green = [0, 80, 0, 100]

    light_blue = [0, 0, 155, 0]
    soft_blue = [2, 221, 255, 0]
    mixed_blue = [0, 50, 255, 100, 0]

    purple = [132, 2, 255, 0]
    pink = [255, 3, 191, 0]

    def get_random_color_weighted(self):
        all_colors = self.get_all_colors()
        index = randrange(len(all_colors))
        return all_colors[index]

    def get_all_colors(self):
        return [self.light_green, self.mid_green, self.green, self.mixed_blue, self.blue, self.red]


