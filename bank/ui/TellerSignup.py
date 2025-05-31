from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from bank.ui.ScanningScreen import ScanningScreen
from bank.ui.Toast import show_toast

class TellerSignupScreen(Screen):
    def __init__(self, on_agree, on_cancel, **kwargs):
        super(TellerSignupScreen, self).__init__(**kwargs)

        # Left side content
        left_layout = RelativeLayout(size_hint=(0.7, 1), pos_hint={'x': 0.1, 'y': 0})
        self.add_widget(left_layout)

        # Agreement text
        self.agreement_label = Label(
            text="Thank you for signing up to become a Teller!  We’re so excited to have you join the ACME team.  We like to think of ourselves as a family, well, because most of us are!  You’ll be joining the ranks of all of A.C.M. Ethelbert’s children.  If you stack your beans right, you might even be able to join the family.\nBecoming a Teller is an exciting opportunity.  You’ll be able to help our customers achieve all of their financial dreams.   In return, you’ll get paid for every interaction you assist with! \n\nBefore each ATM transaction you oversee, make sure you are signed in as the active teller and we will automatically pay your salary directly into your account.  You’ll be rich! \n\nTo finalize your enrollment, you must agree to the following terms:\n  * You vow to operate the ATM honestly and always enter the correct numbers\n  * You vow to prevent fraudulent activity by any means necessary\n  * You vow to physically project the bank with your life if it is under attack by bandits (We hear that a band raid may occur at 2pm on Saturday)\n  * You vow to assist customers to the best of your ability\nIf you agree to these terms, press the “I Agree” button below.",
            size_hint=(1, 0.8),
            pos_hint={'x': 0, 'y': 0.2},
            text_size=(400, None),
            width=400,
            halign="left",
            valign="middle"
        )
        self.agreement_label.bind(size=self.agreement_label.setter('text_size'))
        left_layout.add_widget(self.agreement_label)

        # I Agree button
        self.agree_button = Button(
            text="I Agree",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            on_press=on_agree
        )
        left_layout.add_widget(self.agree_button)

        # Right side content
        right_layout = RelativeLayout(size_hint=(0.3, 1), pos_hint={'x': 0.7, 'y': 0})
        self.add_widget(right_layout)

        # Cancel button
        self.cancel_button = Button(
            text="Cancel",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            on_press=on_cancel
        )
        right_layout.add_widget(self.cancel_button)
