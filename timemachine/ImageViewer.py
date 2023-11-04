import pygame
from datetime import datetime

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024

END = datetime(2999, 12, 31, 23, 59, 59)
START = datetime(1000, 1, 1, 0, 0, 0)

IMAGES_BY_YEAR = [
 {
   "year": datetime(1000,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1000 - Big Castle.jpeg"
 },
 {
   "year": datetime(1010,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1010 - Castle.jpeg"
 },
 {
   "year": datetime(1033,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1033 - King Crowning.jpeg"
 },
 {
   "year": datetime(1096,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1096 - First Crusade.jpeg"
 },
 {
   "year": datetime(1113,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1113 - Khmer Empire.jpeg"
 },
 {
   "year": datetime(1147,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1147 - Second Crusade.jpeg"
 },
 {
   "year": datetime(1149,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1149 - Second Crusade 2.jpeg"
 },
 {
   "year": datetime(1202,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1201 - Fourth Crusade.jpeg"
 },
 {
   "year": datetime(1206,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1206 - Ghengis Khan.jpeg"
 },
 {
   "year": datetime(1229,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1229 - Khan dies.jpeg"
 },
 {
   "year": datetime(1232,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1232 - Chinese Rockets.jpeg"
 },
 {
   "year": datetime(1281,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1281.jpeg"
 },
 {
   "year": datetime(1298,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1298.jpeg"
 },
 {
   "year": datetime(1314,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1314 - European Famine.jpeg"
 },
 {
   "year": datetime(1337,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1337 - 100 Year War.jpeg"
 },
 {
   "year": datetime(1350,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1350 - Plague.jpeg"
 },
 {
   "year": datetime(1429,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1429 - Joan.jpeg"
 },
 {
   "year": datetime(1450,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1450 - print.jpeg"
 },
 {
   "year": datetime(1503,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1503 - Mona.jpeg"
 },
 {
   "year": datetime(1517,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1517 - Cortes.jpeg"
 },
 {
   "year": datetime(1542,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1542 - Musket.jpeg"
 },
 {
   "year": datetime(1547,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1547 - Ivan.jpeg"
 },
 {
   "year": datetime(1588,  7, 12, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1588 - Armada.jpeg"
 },
 {
   "year": datetime(1589,  7, 12, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1588.jpeg"
 },
 {
   "year": datetime(1592,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1592.jpeg"
 },
 {
   "year": datetime(1606,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1606.jpeg"
 },
 {
   "year": datetime(1620,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1620.jpeg"
 },
 {
   "year": datetime(1634,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1634.jpeg"
 },
 {
   "year": datetime(1642,  12, 13, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1642.jpeg"
 },
 {
   "year": datetime(1672,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1672.jpeg"
 },
 {
   "year": datetime(1769,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1769.jpeg"
 },
 {
   "year": datetime(1800,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1800.jpeg"
 },
 {
   "year": datetime(1808,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1808.jpeg"
 },
 {
   "year": datetime(1833,  11, 12, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1833.jpeg"
 },
 {
   "year": datetime(1853,  1, 24, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1853.jpeg"
 },
 {
   "year": datetime(1865,  4, 2, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1865.jpeg"
 },
 {
   "year": datetime(1869,  11, 17, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1869.jpeg"
 },
 {
   "year": datetime(1873,  5, 10, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1873.jpeg"
 },
 {
   "year": datetime(1890,  7, 29, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1890.jpeg"
 },
 {
   "year": datetime(1893,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1893.jpeg"
 },
 {
   "year": datetime(1913,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1913.jpeg"
 },
 {
   "year": datetime(1918,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1918.jpeg"
 },
 {
   "year": datetime(1921,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1921.jpeg"
 },
 {
   "year": datetime(1933,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1933 - Fireside chat.jpeg"
 },
 {
   "year": datetime(1934,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1934.jpeg"
 },
 {
   "year": datetime(1937,  7, 2, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1937 Earheart.jpeg"
 },
 {
   "year": datetime(1948,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1948.jpeg"
 },
 {
   "year": datetime(1952,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1952.jpeg"
 },
 {
   "year": datetime(1952,  11, 6, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1952-November.jpeg"
 },
 {
   "year": datetime(1956,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1956.jpeg"
 },
 {
   "year": datetime(1957,  10, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1957 Sputnik I.jpeg"
 },
 {
   "year": datetime(1958,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1958.jpeg"
 },
 {
   "year": datetime(1962,  10, 16, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1962.jpeg"
 },
 {
   "year": datetime(1968,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1968.jpeg"
 },
 {
   "year": datetime(1969,  7, 20, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1969-Moon Landing.jpeg"
 },
 {
   "year": datetime(1974,  8, 9, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1974.jpeg"
 },
 {
   "year": datetime(1980,  11, 4, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1980.jpeg"
 },
 {
   "year": datetime(1981,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1981.jpeg"
 },
 {
   "year": datetime(1983,  3, 23, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1983.jpeg"
 },
 {
   "year": datetime(1986,  1, 28, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1986.jpeg"
 },
 {
   "year": datetime(1987,  10, 19, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1987.jpeg"
 },
 {
   "year": datetime(1991,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1991.jpeg"
 },
 {
   "year": datetime(1993,  12, 8, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1993.jpeg"
 },
 {
   "year": datetime(1996,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1996.jpeg"
 },
 {
   "year": datetime(1998,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/1998.jpeg"
 },
 {
   "year": datetime(2001,  10, 8, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2001.jpeg"
 },
 {
   "year": datetime(2020,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2020.jpeg"
 },
 {
   "year": datetime(2090,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2090.jpeg"
 },
 {
   "year": datetime(2101,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2101.jpeg"
 },
 {
   "year": datetime(2116,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2116.jpeg"
 },
 {
   "year": datetime(2122,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2122.jpeg"
 },
 {
   "year": datetime(2200,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2200.jpeg"
 },
 {
   "year": datetime(2225,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2225.jpeg"
 },
 {
   "year": datetime(2295,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2295.jpeg"
 },
 {
   "year": datetime(2302,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2302.jpeg"
 },
 {
   "year": datetime(2433,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2433.jpeg"
 },
 {
   "year": datetime(2434,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2434.jpeg"
 },
 {
   "year": datetime(2496,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2496.jpeg"
 },
 {
   "year": datetime(2500,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2500.jpeg"
 },
 {
   "year": datetime(2555,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2555.jpeg"
 },
 {
   "year": datetime(2590,  9, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2590.jpeg"
 },
 {
   "year": datetime(2596,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2596 - Vampire war.jpeg"
 },
 {
   "year": datetime(2629,  12, 16, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2629.jpeg"
 },
 {
   "year": datetime(2665,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2665.jpeg"
 },
 {
   "year": datetime(2666,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2666.jpeg"
 },
 {
   "year": datetime(2672,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2672.jpeg"
 },
 {
   "year": datetime(2780,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2780.jpeg"
 },
 {
   "year": datetime(2782,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2782.jpeg"
 },
 {
   "year": datetime(2906,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2906.jpeg"
 },
 {
   "year": datetime(2912,  1, 1, 0, 0, 0),
    "filename": "/home/admin/explorey/images/2912.jpeg"
 }
]


class ImageViewer(object):
    current_date = END
    image = None
    font = None
    path = None
    screen = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Time Viewer')
        self.font = pygame.font.SysFont('arial', 48)

    def __update_image(self, image_path):
        # create a surface object, image is drawn on it.
        try:
            self.image = pygame.image.load(image_path).convert()
        except Exception as err:
            print(err)

    def render(self, datestring):
        # Using blit to copy content from one surface to other
        try:
            self.screen.blit(self.image, (0, 0))
        except Exception as err:
            print(err)
        # text = self.font.render(datestring, True, (0, 0, 0))
        # text_rect = text.get_rect()
        # text_rect.topleft = (20, 20)
        # self.screen.blit(text, text_rect)
        # paint screen one time
        pygame.display.flip()

    def update(self, date, datestring, active):
        if active:
            if self.current_date != date:

                min_distance = (END - START).total_seconds()
                path = IMAGES_BY_YEAR[0]["filename"]
                event_date = IMAGES_BY_YEAR[0]["year"]
                for index in range(0, len(IMAGES_BY_YEAR)):
                    current_event = IMAGES_BY_YEAR[index]
                    current_event_date = current_event["year"]
                    current_event_path = current_event["filename"]
                    event_distance = abs((current_event_date - date).total_seconds())
                    if event_distance < min_distance:
                        event_date = current_event
                        path = current_event_path
                        min_distance = event_distance



                # closest_year_index = 0
                # distance = END
                # for index in range(len(IMAGES_BY_YEAR)):
                #     image = IMAGES_BY_YEAR[index]
                #     if image['date'] <= date:
                #         closest_year_index = index
                # current_year = IMAGES_BY_YEAR[closest_year_index]

                if path != self.path or not self.image:
                    print(f"Changing image - year {event_date} - path: {path}")
                    self.current_date = date
                    self.path = path
                    self.__update_image(self.path)
                    self.render(datestring)
        else:
            self.screen.fill((0,0,0))
            pygame.display.flip()