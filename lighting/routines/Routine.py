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
        removed_addresses = set(self.addresses).difference(addresses)
        for address in removed_addresses:
            self.pixels.setColor(address, [0, 0, 0])
        self.addresses = addresses

    def tick(self):
        print("tick")

