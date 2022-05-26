from lighting.GenericButtonController import GenericButtonController


MAX_POINTS = 1000


class WarGame(object):

	points = 0
	pixel_start = 0
	pixel_end = 0
	num_pixels = 0
	red_button_pin = 0
    blue_button_pin = 0

	buttons = None

	def __init__(self, pixels, pixel_start, pixel_end, red_button_pin, blue_button_pin):
        self.pixels = pixels
        self.pixel_start = pixel_start
        self.pixel_end = pixel_end
        self.num_pixels = pixel_end - pixel_start
        red_button_pin = red_button_pin
        blue_button_pin = blue_button_pin

        self.buttons = GenericButtonController()

       	self.buttons.add_event_detection(self.red_button_pin, self.on_red_button)
       	self.buttons.add_event_detection(self.blue_button_pin, self.on_blue_button)

    def on_red_button(self):
    	if points < MAX_POINTS:
    		points += 1
		self.render()

	def on_blue_button(self):
		if (points > (MAX_POINTS * -1)):
			points -= 1
		self.render()

	def render(self):
        print("render")
		


