from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

class BankruptcyConfirmationScreen(Screen):
    def __init__(self, on_finalize_bankruptcy, **kwargs):
        super(BankruptcyConfirmationScreen, self).__init__(**kwargs)
        self.on_finalize_bankruptcy = on_finalize_bankruptcy
        # Adjusted layout to horizontally center content and ensure proper vertical order
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), width=400)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Updated left layout to center content and adjust spacing
        self.left_layout = BoxLayout(orientation='vertical', size_hint=(1, None), padding=10, spacing=20)

        # Adjusted widgets to ensure proper vertical order
        self.account_image = Image(size_hint=(1, None), height=200, allow_stretch=True, keep_ratio=True)
        self.beans_owed_label = Label(font_size="18sp", size_hint=(1, None), height=50)
        self.instructions_label = Label(
            text="It has come to our attention that you have decided to file for bankruptcy.   While it is unfortunate you have been unable to repay your debts, ACME Bank is very understanding that sometimes people are very bad with money and this does not make them bad people.\n\nIn order to qualify for bankruptcy, you must have completed the bankruptcy form.\n\nDo you swear that you have done one or more of the following:\n\n  * Attempted to work off your debt as a teller\n  * Announced loudly to everyone in the bank that you are bad with beans and apologize\n  * Visited the spank bank and received your corporate punishment by a teller\n\nIf so, then you may file for bankruptcy.  \n\nBy filing for bankruptcy, do you agree to the following:\n\n  * Your debt will be wiped away and replaced by a single bean in your account\n  * You vow to be better with money and not go into debt\n  * You understand that by going into debt a second time that ACME Bank reserves the right to foreclose on any belongings, property, clothes, nicknames, beers in your cooler, or artistic credits you may own.\n\nPress the button below to continue.",
            font_size="16sp",
            size_hint=(1, None),
            text_size=(400, None),
            halign="left",
            valign="middle"
        )

        agree_button = Button(text="I Agree to File for Bankruptcy", size_hint=(1, None), height=50, pos_hint={'center_x': 0.5})
        agree_button.on_press = self.on_confirm

        # Add widgets in the correct order
        self.left_layout.add_widget(self.account_image)
        self.left_layout.add_widget(self.beans_owed_label)
        self.left_layout.add_widget(self.instructions_label)
        self.left_layout.add_widget(Widget(size_hint_y=0.2))
        self.left_layout.add_widget(agree_button)

        self.layout.add_widget(self.left_layout)
        self.add_widget(self.layout)

    def on_confirm(self):
        self.on_finalize_bankruptcy(self.account)

    def set_account(self, account):
        self.account = account
        self.account_image.source = account.name_file_path
        self.beans_owed_label.text = f"Beans Owed: {-1 * account.balance}"

    def cancel(self, instance):
        self.manager.current = 'dashboard'
