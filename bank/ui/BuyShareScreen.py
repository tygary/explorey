from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

class BuyShareScreen(Screen):
    def __init__(self, on_finalize_purchase, **kwargs):
        super(BuyShareScreen, self).__init__(**kwargs)
        self.on_finalize_purchase = on_finalize_purchase
        # # Adjusted layout to horizontally center content and ensure proper vertical order
        # self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), width=400)
        # self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Updated left layout to center content and adjust spacing
        self.left_layout = RelativeLayout(size_hint=(0.7, 1), pos_hint={'x': 0.1, 'y': 0})
        self.add_widget(self.left_layout)

        self.instructions_label = Label(
            text="Shares of The Leech Mining Company are available for purchase at a price of 100 beans per share.  \n\nBy purchasing a share, you must have completed the shareholder agreement, located on a clipboard by the teller booth.  If you have already completed this agreement, then press Purchase below.",
            font_size="18sp",
            size_hint=(1, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            text_size=(400, None),
            width=400,
            halign="left",
            valign="middle"
        )
        self.instructions_label.bind(size=self.instructions_label.setter('text_size'))

        agree_button = Button(text="Purchase", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.05})
        agree_button.on_press = self.on_confirm

        # Add widgets in the correct order
        self.left_layout.add_widget(self.instructions_label)
        self.left_layout.add_widget(agree_button)

         # Right side layout
        right_layout = RelativeLayout(size_hint=(0.3, 1), pos_hint={'x': 0.7, 'y': 0})
        self.add_widget(right_layout)
        cancel_button = Button(text="Cancel", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.05}, on_press=self.cancel)
        right_layout.add_widget(cancel_button)
        

    def on_confirm(self, instance=None):
        self.on_finalize_purchase()

    def cancel(self, instance=None):
        self.manager.current = 'dashboard'
