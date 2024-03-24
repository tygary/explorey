RED = 0
GREEN = 1
BLUE = 2


class Routine(object):
    addresses = []
    pixels = None

    def __init__(self, pixels, addresses):
        self.pixels = pixels
        self.addresses = addresses

    def update_addresses(self, addresses):
        self.addresses = addresses

    def tick(self):
        print("tick")

