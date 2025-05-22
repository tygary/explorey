from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock


# Main Dashboard Screen
class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='horizontal')

        # Left area with logo
        left_layout = FloatLayout(size_hint=(0.66, 1))
        logo = Image(
            source='logo_placeholder.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True,
        )
        left_layout.add_widget(logo)

        # Right area with buttons
        right_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.34, 1),
            padding=10,
            spacing=15
        )
        button_labels = ['Withdraw', 'Deposit', 'Transfer', 'Become a Teller']
        for label in button_labels:
            btn = Button(text=label, size_hint=(1, None), height=80)
            if label == 'Withdraw':
                btn.bind(on_press=self.go_to_withdraw)
            right_layout.add_widget(btn)

        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        self.add_widget(layout)

    def go_to_withdraw(self, instance):
        self.manager.current = 'withdraw'


# Withdraw Screen
class WithdrawScreen(Screen):
    def __init__(self, **kwargs):
        super(WithdrawScreen, self).__init__(**kwargs)
        self.document_scanned_cb = None
        layout = BoxLayout(orientation='horizontal')

        # Left area with instruction text
        left_layout = FloatLayout(size_hint=(0.66, 1))
        label = Label(
            text='Scan your account number now',
            font_size='24sp',
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

        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        self.add_widget(layout)

    def set_document_scanned_callback(self, callback):
        self.document_scanned_cb = callback

    

    def go_back(self, instance):
        self.manager.current = 'dashboard'


# Main App with ScreenManager
class UiApp(App):
    def build(self):
        self.manager = ScreenManager(transition=FadeTransition())
        self.manager.add_widget(DashboardScreen(name='dashboard'))
        self.manager.add_widget(WithdrawScreen(name='withdraw'))
        return self.manager

    

class ATMUI(object): 
    def __init__(self):
        self.app = UiApp()
        self.app.run()

    def get_app(self):
        return App.get_running_app()

    def change_screen(self, screen_name):
        def switch_screen(dt):
            self.get_app.manager.current = screen_name
        Clock.schedule_once(switch_screen)
    
    
