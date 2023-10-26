import pygame
from datetime import datetime

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024

IMAGES_BY_YEAR = [
    {
        "date": datetime(1000, 1, 1, 0, 0, 0),
        "path": "/home/admin/explorey/images/1970.jpeg"
    },
    {
        "date": datetime(1980, 1, 1, 0, 0, 0),
        "path": "/home/admin/explorey/images/1970.jpeg"
    },
    {
        "date": datetime(1990, 1, 1, 0, 0, 0),
        "path": "/home/admin/explorey/images/1970.jpeg"
    },
    {
        "date": datetime(2000, 1, 1, 0, 0, 0),
        "path": "/home/admin/explorey/images/1970.jpeg"
    },

]


class ImageViewer(object):
    is_running = True
    current_date = None
    current_image_index = 0
    image = None
    font = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Time Viewer')
        self.font = pygame.font.SysFont('arial', 48)

    def __update_image(self, image_path):
        # create a surface object, image is drawn on it.
        self.image = pygame.image.load(image_path).convert()

    def render(self, datestring):
        # Using blit to copy content from one surface to other
        self.screen.blit(self.image, (0, 0))
        text = self.font.render(datestring, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.topleft = (20, 20)
        self.screen.blit(text, text_rect)
        # paint screen one time
        pygame.display.flip()

    def update(self, date, datestring):
        if self.is_running:
            if self.current_date != date:
                closest_year_index = 0
                for index in range(len(IMAGES_BY_YEAR)):
                    image = IMAGES_BY_YEAR[index]
                    if image['date'] <= date:
                        closest_year_index = index
                current_year = IMAGES_BY_YEAR[closest_year_index]
                self.current_date = date
                if current_year != IMAGES_BY_YEAR[self.current_image_index] or not self.image:
                    self.__update_image(current_year['path'])
                self.render(datestring)
            # iterate over the list of Event objects
            # that was returned by pygame.event.get() method.
            for i in pygame.event.get():
                # if event object type is QUIT
                # then quitting the pygame
                # and program both.
                if i.type == pygame.QUIT:
                    self.is_running = False
