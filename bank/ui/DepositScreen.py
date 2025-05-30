from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from kivy.uix.floatlayout import FloatLayout

from bank.FormScanner import FormInfo
from bank.ui.Toast import show_toast


class DepositScreen(Screen):
    def __init__(self, start_deposit, cancel_deposit, on_finish_deposit, **kwargs):
        super(DepositScreen, self).__init__(**kwargs)
        self.start_deposit = start_deposit
        self.cancel_deposit = cancel_deposit
        self.on_finish_deposit = on_finish_deposit
        self.amount = 0 # Will be set when the deposit is confirmed
        self.form_info = None  # Will be set when the deposit is confirmed
        self.is_waiting = False
        
        layout = BoxLayout(orientation='horizontal')

        # Left area with instruction text
        left_layout = FloatLayout(size_hint=(0.66, 1))
        label = Label(
            text=f"Place your beans in the deposit chute now...",
            font_size='26sp',  # Increased from 24sp
            halign='center',
            valign='middle',
            text_size=(None, None),
            size_hint=(0.9, 0.5),
            pos_hint={'center_x': 0.5, 'top': 0.9},
            shorten=False,
            markup=True
        )
        left_layout.add_widget(label)
        self.amount_label = Label(
            text="0 beans deposited",
            font_size='26sp',  # Increased from 24sp
            halign='center',
            valign='middle',
            text_size=(None, None),
            size_hint=(0.9, 0.3),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            shorten=False,
            markup=True
        )
        left_layout.add_widget(self.amount_label)

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

    def set_values(self, form_info: FormInfo, amount: int):
        """Call this to set the form info and amount for the deposit"""
        self.form_info = form_info
        self.amount = amount
        self.amount_label.text = f"0 / {self.amount} beans deposited"

    def on_enter(self):
        # Start the scanning process when entering this screen
        self.is_waiting = True
        self.start_deposit(self.on_beans_deposited, self.on_deposit_fail)

    def on_beans_deposited(self, total):
        self.amount_label.text = f"{total} / {self.amount} beans deposited"
        if abs(total - self.amount) < self.amount * .5 and self.is_waiting:
            self.is_waiting = False
            # If the amount is within 50% of the requested amount, proceed
            self.on_finish_deposit(self.form_info, self.amount)

    def on_deposit_fail(self, message):
        # Handle deposit failure
        show_toast(self, message)
        self.manager.current = 'dashboard'

    def go_back(self, instance):
        self.cancel_deposit()
        self.manager.current = 'dashboard'
