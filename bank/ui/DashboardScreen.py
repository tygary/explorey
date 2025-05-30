from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, RoundedRectangle


class DashboardScreen(Screen):
    def __init__(self, atm=None, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.atm = atm
        layout = BoxLayout(orientation='horizontal')

        # Left area with logo
        left_layout = FloatLayout(size_hint=(0.66, 1))
        logo = Image(
            source='/home/admin/explorey/images/bank_logo.png',
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
        right_layout.add_widget(Widget(size_hint_y=0.2))
        # Teller section with background and border
        self.teller_section = RelativeLayout(size_hint_y=None, height=100)
        with self.teller_section.canvas.before:
            Color(0.3, 0.3, 0.3, 1)  # Light gray background
            self.teller_bg = RoundedRectangle(radius=[10], pos=self.teller_section.pos, size=self.teller_section.size)
            Color(0.7, 0.7, 0.7, 1)  # Gray border
            self.teller_border = RoundedRectangle(radius=[10], pos=self.teller_section.pos, size=self.teller_section.size, width=2)
        def update_bg(*args):
            self.teller_bg.pos = self.teller_section.pos
            self.teller_bg.size = self.teller_section.size
            self.teller_border.pos = self.teller_section.pos
            self.teller_border.size = self.teller_section.size
        self.teller_section.bind(pos=update_bg, size=update_bg)

        right_layout.add_widget(self.teller_section)
        right_layout.add_widget(Widget(size_hint_y=0.1))
        button_labels = ['Open Account', 'Withdraw', 'Deposit', 'Transfer', 'Become a Teller']
        for label in button_labels:
            btn = Button(text=label, size_hint=(1, None), height=80, font_size='22sp')  # Increased font size
            if label == 'Deposit':
                btn.bind(on_press=self.go_to_deposit)
            elif label == 'Open Account':
                btn.bind(on_press=self.go_to_open_account)
            elif label == 'Withdraw':
                btn.bind(on_press=self.go_to_withdraw)
            elif label == 'Transfer':
                btn.bind(on_press=self.go_to_transfer)
            elif label == 'Become a Teller':
                btn.bind(on_press=self.go_to_become_teller)

            right_layout.add_widget(btn)
        right_layout.add_widget(Widget(size_hint_y=1))

        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        self.add_widget(layout)
        self.update_teller_section()

    def update_teller_section(self):
        self.teller_section.clear_widgets()
        teller = self.atm.get_current_teller() if self.atm else None
        # Add a background and border to the teller section
        self.teller_section.canvas.before.clear()
        from kivy.graphics import Color, RoundedRectangle
        with self.teller_section.canvas.before:
            Color(0.93, 0.93, 0.93, 1)  # Light gray background
            RoundedRectangle(pos=self.teller_section.pos, size=self.teller_section.size, radius=[10])
            Color(0.7, 0.7, 0.7, 1)  # Gray border
            RoundedRectangle(pos=self.teller_section.pos, size=self.teller_section.size, radius=[10], width=2)
        def update_bg(*args):
            for instr in self.teller_section.canvas.before.children:
                if isinstance(instr, RoundedRectangle):
                    instr.pos = self.teller_section.pos
                    instr.size = self.teller_section.size
        self.teller_section.bind(pos=update_bg, size=update_bg)
        # ...existing code for adding widgets...
        if teller:
            self.teller_section.add_widget(Button(text=f"Current Teller: {teller.account_number}", size_hint_y=None, height=20, background_color=(0,0,0,0), color=(1,1,1,1)))
            self.teller_section.add_widget(Image(source=teller.name_file_path, size_hint_y=None, height=40, allow_stretch=True, keep_ratio=True))
        sign_in_btn = Button(text="Replace Active Teller", size_hint_y=None, height=20, font_size='18sp')
        sign_in_btn.bind(on_press=self.go_to_teller_signin)
        self.teller_section.add_widget(sign_in_btn)

    def go_to_deposit(self, instance):
        self.manager.current = 'deposit'

    def go_to_open_account(self, instance):
        self.manager.current = 'open_account'

    def go_to_withdraw(self, instance):
        self.manager.current = 'withdraw'
    
    def go_to_transfer(self, instance):
        self.manager.current = 'transfer'

    def go_to_teller_signin(self, instance):
        self.manager.current = 'teller_signin_scanning'

    def go_to_become_teller(self, instance):
        self.manager.current = 'teller_signup'
