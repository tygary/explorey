from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

class TopAccountsListScreen(Screen):
    def __init__(self, get_accounts, is_leaderboard=True, **kwargs):
        super(TopAccountsListScreen, self).__init__(**kwargs)
        self.get_accounts = get_accounts
        self.is_leaderboard = is_leaderboard
        self.layout = BoxLayout(orientation='vertical', padding=100, spacing=10)

        # Title based on the flag
        title_text = "Highrollers" if is_leaderboard else "Wanted Debtors"
        title_label = Label(text=title_text, font_size="20sp", size_hint=(1, None), height=50)
        self.layout.add_widget(title_label)

        # Scrollable list of accounts
        self.scroll_view = ScrollView()
        self.account_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.account_list.bind(minimum_height=self.account_list.setter('height'))
        self.scroll_view.add_widget(self.account_list)
        self.layout.add_widget(self.scroll_view)

        # Back button
        back_btn = Button(text="Back", size_hint=(None, None), size=(100, 50), pos_hint={'x': 0.85, 'y': 0.05})
        back_btn.bind(on_press=self.go_back)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def refresh_accounts(self, *args):
        accounts = self.get_accounts()
        self.account_list.clear_widgets()

        for account in accounts[:20]:  # Top 20 accounts
            account_item = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)

            # Load the image to get its native size
            core_image = CoreImage(account.name_file_path)
            native_width, native_height = core_image.size

            # Scale the image to twice its native size
            account_image = Image(source=account.name_file_path, size_hint=(None, None), size=(native_width * 2, native_height * 2))
            account_balance = Label(text=f"${account.balance:.2f}", size_hint=(0.4, 1), font_size="16sp")
            account_item.add_widget(account_image)
            account_item.add_widget(account_balance)
            self.account_list.add_widget(account_item)

    def go_back(self, instance):
        self.manager.current = 'dashboard'

    def on_enter(self):
        # Schedule periodic refresh
        self.refresh_event = Clock.schedule_interval(self.refresh_accounts, 10)
        self.refresh_accounts()

    def on_leave(self):
        # Unschedule the refresh when leaving the screen
        Clock.unschedule(self.refresh_event)
