import math

from lighting.routines.TimeRoutine import TimeRoutine


arrow_matrix = [
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

class ArrowGaugeRoutine(TimeRoutine):
    color = [255, 0, 0]
    percentage = 0
    prev_breakpoint = 0
    line_width = 5
    arrow_width = 7

    def __init__(self, pixels, addresses, group_cnt=8, color=[255, 0, 0]):
        super().__init__(pixels, addresses)
        self.color = color
        self.group_cnt = group_cnt

    def update_percentage(self, percentage):
        self.percentage = percentage

    def tick(self):
        num_pixels = len(self.addresses)
        num_pixel_groups = num_pixels // self.group_cnt
        num_pixel_groups_minus_width = num_pixel_groups - self.line_width
        start_group = math.floor(num_pixel_groups_minus_width * self.percentage)
        arrow_start_index = start_group - 1
        arrow_end_index = arrow_start_index + self.arrow_width
        
        # Ensure arrow doesn't go out of bounds
        if arrow_start_index < 0:
            arrow_start_index = 0
        if arrow_end_index > num_pixel_groups:
            arrow_end_index = num_pixel_groups
            
        # Clear all pixels first
        for pixel_index in range(num_pixels):
            self.pixels.setColor(self.addresses[pixel_index], [0, 0, 0])
        
        # Draw only the arrow where it should appear
        if arrow_start_index >= 0:
            for column in range(arrow_start_index, arrow_end_index):
                color_matrix_column = column - arrow_start_index
                
                # Skip if the column index is out of arrow_matrix bounds
                if color_matrix_column < 0 or color_matrix_column >= self.arrow_width:
                    continue
                    
                for row in range(self.group_cnt):
                    # Each column has group_cnt (8) pixels
                    # column is the column index, row is the position within the column (bottom to top)
                    pixel_index = column * self.group_cnt + row
                    
                    if pixel_index < num_pixels:
                        # Check if this pixel should be lit according to arrow_matrix
                        if row < len(arrow_matrix) and color_matrix_column < len(arrow_matrix[0]):
                            color_value = self.color if arrow_matrix[row][color_matrix_column] == 1 else [0, 0, 0]
                            self.pixels.setColor(self.addresses[pixel_index], color_value)


class GaugeRoutine(TimeRoutine):
    color = [255, 0, 0]
    percentage = 0
    prev_breakpoint = 0
    width = 5

    def __init__(self, pixels, addresses, group_cnt=8, color=[255, 0, 0]):
        super().__init__(pixels, addresses)
        self.color = color
        self.group_cnt = group_cnt

    def update_percentage(self, percentage):
        self.percentage = percentage

    def tick(self):
        num_pixels = len(self.addresses)
        num_pixel_groups = num_pixels // self.group_cnt
        num_pixel_groups_minus_width = num_pixel_groups - self.width
        start_group = math.floor(num_pixel_groups_minus_width * self.percentage)
        end_group = start_group + self.width
        for group_index in range(0, num_pixel_groups):
            color_value = self.color if group_index >= start_group and group_index < end_group else [0, 0, 0]
            for i in range(0, self.group_cnt):
                pixel_index = group_index * self.group_cnt + i
                if pixel_index < num_pixels:
                    self.pixels.setColor(self.addresses[pixel_index], color_value)
