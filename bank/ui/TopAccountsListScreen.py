from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen

class TopAccountsListScreen(Screen):
    def __init__(self, accounts, is_leaderboard=True, **kwargs):
        super(TopAccountsListScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title based on the flag
        title_text = "Leaderboard" if is_leaderboard else "Bankruptcy Roll"
        title_label = Label(text=title_text, font_size="20sp", size_hint=(1, None), height=50)
        layout.add_widget(title_label)

        # Scrollable list of accounts
        scroll_view = ScrollView()
        account_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        account_list.bind(minimum_height=account_list.setter('height'))

        for account in accounts[:20]:  # Top 20 accounts
            account_item = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
            account_image = Image(source=account.name_file_path, size_hint=(None, None), size=(200, 50))
            account_balance = Label(text=f"${account.balance:.2f}", size_hint=(0.4, 1), font_size="16sp")
            account_item.add_widget(account_image)
            account_item.add_widget(account_balance)
            account_list.add_widget(account_item)

        scroll_view.add_widget(account_list)
        layout.add_widget(scroll_view)

        # Back button
        back_btn = Button(text="Back", size_hint=(None, None), size=(100, 50), pos_hint={'x': 0, 'y': 0})
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'dashboard'
