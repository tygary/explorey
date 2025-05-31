from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock

class EconomyOverviewScreen(Screen):
    def __init__(self, get_exchange_rate, get_interest_rate, get_debt_interest_rate, get_sign_on_bonus, **kwargs):
        super(EconomyOverviewScreen, self).__init__(**kwargs)
        self.get_exchange_rate = get_exchange_rate
        self.get_interest_rate = get_interest_rate
        self.get_debt_interest_rate = get_debt_interest_rate
        self.get_sign_on_bonus = get_sign_on_bonus

        width = 700

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Spacer to push content down
        layout.add_widget(Widget(size_hint_y=1))

        # Display exchange rate
        self.exchange_rate_label = Label(
            text=f"Current BeanBucks to Bean Exchange Rate: {self.get_exchange_rate()} BeanBucks = 1 Bean",
            font_size="22sp",
            size_hint=(1, None),
            height=50,
            width=width
        )
        self.exchange_rate_label.halign = 'left'
        self.exchange_rate_label.valign = 'top'
        self.exchange_rate_label.text_size = self.exchange_rate_label.size
        layout.add_widget(self.exchange_rate_label)

        # Display interest rate
        self.interest_rate_label = Label(
            text=f"Current Interest Rate: {self.get_interest_rate() * 100:.2f}%\n(Applied to positive balances compounding every 10 minutes)",
            font_size="22sp",
            size_hint=(1, None),
            height=70,
            width=width
        )
        self.interest_rate_label.halign = 'left'
        self.interest_rate_label.valign = 'top'
        self.interest_rate_label.text_size = self.interest_rate_label.size
        layout.add_widget(self.interest_rate_label)

        # Display debt interest rate
        self.debt_interest_rate_label = Label(
            text=f"Current Debt Interest Rate: {self.get_debt_interest_rate() * 100:.2f}%\n(Applied to negative balances compounding every 10 minutes)",
            font_size="22sp",
            size_hint=(1, None),
            height=70,
            width=width
        )
        self.debt_interest_rate_label.halign = 'left'
        self.debt_interest_rate_label.valign = 'top'
        self.debt_interest_rate_label.text_size = self.debt_interest_rate_label.size
        layout.add_widget(self.debt_interest_rate_label)

        # Display current sign-on bonus
        self.sign_on_bonus_label = Label(
            text=f"Current Sign-on Bonus: {self.get_sign_on_bonus()} Beans",
            font_size="22sp",
            size_hint=(1, None),
            height=50,
            width=width
        )
        self.sign_on_bonus_label.halign = 'left'
        self.sign_on_bonus_label.valign = 'top'
        self.sign_on_bonus_label.text_size = self.sign_on_bonus_label.size
        layout.add_widget(self.sign_on_bonus_label)
        # Spacer to push content up
        layout.add_widget(Widget(size_hint_y=1))
        # Back button
        back_btn = Button(
            text="Back",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'right': 1, 'bottom': 1}
        )
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def update_rates(self, dt=None):
        # Update exchange rate
        self.exchange_rate_label.text = f"Current BeanBucks to Bean Exchange Rate: {self.get_exchange_rate()} BeanBucks = 1 Bean"

        # Update interest rate
        self.interest_rate_label.text = f"Current Interest Rate: {self.get_interest_rate() * 100:.2f}%\n(Applied to positive balances compounding every 10 minutes)"

        # Update debt interest rate
        self.debt_interest_rate_label.text = f"Current Debt Interest Rate: {self.get_debt_interest_rate() * 100:.2f}%\n(Applied to negative balances compounding every 10 minutes)"

        # Update sign-on bonus
        self.sign_on_bonus_label.text = f"Current Sign-on Bonus: {self.get_sign_on_bonus()} Beans"
    
    def on_enter(self):
        # Schedule periodic updates for the rates
        self.update_event = Clock.schedule_interval(self.update_rates, 5)
        self.update_rates()

    def on_leave(self):
        # Unschedule updates when leaving the screen
        Clock.unschedule(self.update_event)

    def go_back(self, instance):
        self.manager.current = 'dashboard'
