import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame


class Levers(object):
    joystick = None
    on_lever_change = None
    on_button_press = None
    done = False
    levers = [0, 0, 0]
    lever_tolerance = 0.00

    def __init__(self, on_lever_change=None, on_button_press=None):
        pygame.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
        self.on_lever_change = on_lever_change
        self.on_button_press = on_button_press

    def update(self):
        if self.done is True:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if self.on_button_press:
                    self.on_button_press(event.button, True)
                    print(f"Button {event.button} pressed")

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")
                if self.on_button_press:
                    self.on_button_press(event.button, False)
                    print(f"Button {event.button} released")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                self.joystick = pygame.joystick.Joystick(event.device_index)
                print(f"Joystick {self.joystick.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                print(f"Joystick {event.instance_id} disconnected")

            if self.joystick:
                for axis_id in range(self.joystick.get_numaxes()):
                    value = self.joystick.get_axis(axis_id)
                    if value != self.levers[axis_id] and abs(self.levers[axis_id] - value) > self.lever_tolerance:
                        # print(f"Lever {axis_id} change from {self.levers[axis_id]} to {value}")
                        self.levers[axis_id] = value
                        if self.on_lever_change:
                            self.on_lever_change(axis_id, value)


