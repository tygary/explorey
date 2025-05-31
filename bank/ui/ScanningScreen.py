from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from bank.ui.Toast import show_toast


# Scanning Screen
class ScanningScreen(Screen):
    def __init__(self, scanning_message, start_scan, cancel_scan, on_finish_scan, form_type=None, **kwargs):
        super(ScanningScreen, self).__init__(**kwargs)
        self.form_type = form_type if form_type else self.name
        self.start_scan = start_scan
        self.cancel_scan = cancel_scan
        self.on_finish_scan = on_finish_scan
        self.scanning_message = scanning_message
        
        layout = BoxLayout(orientation='horizontal')

        # Left area with instruction text
        left_layout = FloatLayout(size_hint=(0.66, 1))
        label = Label(
            text=scanning_message,
            font_size='26sp',  # Increased from 24sp
            halign='center',
            valign='middle',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        left_layout.add_widget(label)

        # Right area with cancel button
        right_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.34, 1),
            padding=10,
        )
        right_layout.add_widget(Label(size_hint=(1, 0.9)))  # Spacer
        cancel_btn = Button(
            text='Cancel',
            size_hint=(1, 0.1)
        )
        cancel_btn.bind(on_press=self.go_back)
        right_layout.add_widget(cancel_btn)
        right_layout.add_widget(Label(size_hint=(1, 0.1)))  # Spacer

        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        self.add_widget(layout)

    def on_enter(self):
        # Start the scanning process when entering this screen
        self.start_scan(self.form_type, self.on_finish_scan, self.on_scan_fail)

    def on_scan_fail(self, message):
        # Handle scan failure
        show_toast(self, message)
        self.manager.current = 'dashboard'

    def go_back(self, instance=None):
        self.cancel_scan()
        self.manager.current = 'dashboard'
