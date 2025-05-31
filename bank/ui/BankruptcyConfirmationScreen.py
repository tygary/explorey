from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

class BankruptcyConfirmationScreen(Screen):
    def __init__(self, on_finalize_bankruptcy, **kwargs):
        super(BankruptcyConfirmationScreen, self).__init__(**kwargs)
        self.on_finalize_bankruptcy = on_finalize_bankruptcy
        # # Adjusted layout to horizontally center content and ensure proper vertical order
        # self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), width=400)
        # self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Updated left layout to center content and adjust spacing
        self.left_layout = RelativeLayout(size_hint=(0.7, 1), pos_hint={'x': 0.1, 'y': 0})
        self.add_widget(self.left_layout)

        # Adjusted widgets to ensure proper vertical order
        self.account_image = Image(size_hint=(1, 0.1), width=400, allow_stretch=True, keep_ratio=True, pos_hint={'center_x': 0.5, 'center_y': 0.8})
        self.beans_owed_label = Label(font_size="18sp", size_hint=(1, 0.05), pos_hint={'center_x': 0.5, 'center_y': 0.7}, halign='center', valign='middle')
        self.instructions_label = Label(
            text="It has come to our attention that you have decided to file for bankruptcy.   While it is unfortunate you have been unable to repay your debts, ACME Bank is very understanding that sometimes people are very bad with money and this does not make them bad people.\n\nIn order to qualify for bankruptcy, you must have completed the bankruptcy form.\n\nDo you swear that you have done one or more of the following:\n\n  * Attempted to work off your debt as a teller\n  * Announced loudly to everyone in the bank that you are bad with beans and apologize\n  * Visited the spank bank and received your corporate punishment by a teller\n\nIf so, then you may file for bankruptcy.  \n\nBy filing for bankruptcy, do you agree to the following:\n\n  * Your debt will be wiped away and replaced by a single bean in your account\n  * You vow to be better with money and not go into debt\n  * You understand that by going into debt a second time that ACME Bank reserves the right to foreclose on any belongings, property, clothes, nicknames, beers in your cooler, or artistic credits you may own.\n\nPress the button below to continue.",
            font_size="18sp",
            size_hint=(1, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            text_size=(400, None),
            width=400,
            halign="left",
            valign="middle"
        )
        self.instructions_label.bind(size=self.instructions_label.setter('text_size'))

        agree_button = Button(text="I Agree to File for Bankruptcy", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.05})
        agree_button.on_press = self.on_confirm

        # Add widgets in the correct order
        self.left_layout.add_widget(self.account_image)
        self.left_layout.add_widget(self.beans_owed_label)
        self.left_layout.add_widget(self.instructions_label)
        self.left_layout.add_widget(agree_button)

         # Right side layout
        right_layout = RelativeLayout(size_hint=(0.3, 1), pos_hint={'x': 0.7, 'y': 0})
        self.add_widget(right_layout)
        cancel_button = Button(text="Cancel", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'y': 0.05}, on_press=self.cancel)
        right_layout.add_widget(cancel_button)
        

    def on_confirm(self, instance=None):
        self.on_finalize_bankruptcy(self.account)

    def set_account(self, account):
        self.account = account
        self.account_image.source = account.name_file_path
        self.beans_owed_label.text = f"Beans Owed: {-1 * account.balance}"

    def cancel(self, instance=None):
        self.manager.current = 'dashboard'
