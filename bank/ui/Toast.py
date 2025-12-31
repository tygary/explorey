from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Line

class Toast(Label):
    def __init__(self, text, duration=8.0, **kwargs):
        super().__init__(
            text=text,
            size_hint=(None, None),
            size=(500, 500),
            halign='center',
            valign='middle',
            font_size='20sp',  # Increased from 18sp
            color=(1, 1, 1, 1),
            text_size=(500, None),  # Enable text wrapping by setting text_size to match width
            **kwargs
        )
        self.opacity = 0.95
        self.padding = (10, 10)
        self.background_color = (0.2, 0.2, 0.2, 1)
        self.border_color = (1, 1, 1, 1)
        self.border_width = 2

        with self.canvas.before:
            Color(*self.background_color)
            self.bg = RoundedRectangle(radius=[12], size=self.size, pos=self.pos)

            Color(*self.border_color)
            
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 12), width=self.border_width)

        self.bind(pos=self.update_bg, size=self.update_bg)
        Clock.schedule_once(lambda dt: self.fade_out(), duration)
        
        # Make the toast clickable
        self.bind(on_touch_down=self.on_touch_down)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 12)

    def fade_out(self):
        if self.parent:
            self.parent.remove_widget(self)
            
    def on_touch_down(self, touch, other=None):
        # Add a short delay before the Toast starts responding to touch events
        self.touch_enabled = False
        Clock.schedule_once(lambda dt: setattr(self, 'touch_enabled', True), 0.5)

        if not getattr(self, 'touch_enabled', True):
            # print("Toast touch disabled temporarily to avoid residual events.")
            return True

        # Log touch position and Toast bounds for debugging
        print(f"Touch position: {touch.pos}, Toast bounds: {self.pos}, {self.size}")
        if self.collide_point(*touch.pos):
            if self.parent:
                print("Toast clicked, removing it")
                self.parent.remove_widget(self)
            return True
        return super(Toast, self).on_touch_down(touch)

def show_toast(screen, message, duration=8.0):
    def create_toast_on_main_thread(*args):
        toast = Toast(message, duration)

        # Try to add the toast to the left/main content area
        try:
            # Assume screen has BoxLayout with left and right children
            box = screen.children[0]  # Main layout
            left_area = box.children[1]  # Left side (index 1 because children is reversed)

            # Wrap left area in FloatLayout if it isn't already
            if not isinstance(left_area, FloatLayout):
                new_left = FloatLayout(size_hint=left_area.size_hint)
                for w in left_area.children[:]:
                    new_left.add_widget(w)
                box.remove_widget(left_area)
                box.add_widget(new_left, index=1)
                left_area = new_left

            # Position toast at middle center of left area
            toast.pos_hint = {'center_x': 0.5, 'top': 0.65}
            left_area.add_widget(toast)

        except Exception as e:
            print("Could not show toast:", e)

    # Schedule creation on the main thread
    Clock.schedule_once(create_toast_on_main_thread)
