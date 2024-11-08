from PixelControl import OverlayedPixelControl

RED = 0
GREEN = 1
BLUE = 2


class Routine(object):
    addresses = []
    pixels = None

    def __init__(self, pixels, addresses, should_override=False):
        if isinstance(pixels, OverlayedPixelControl):
            self.pixels = pixels.get_sub_pixels_for_routine(self, should_override)
        else:
            self.pixels = pixels
        self.addresses = addresses

    def update_addresses(self, addresses):
        removed_addresses = set(self.addresses).difference(addresses)
        if len(removed_addresses) > 0:
            for address in removed_addresses:
                self.pixels.setColor(address, [0, 0, 0])
        self.addresses = addresses

    def tick(self):
        print("tick")
