import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle, Line

from bank.ATM import ATM
from bank.FormScanner import FormInfo
from bank.AccountPrinter import AccountPrinter

class Toast(Label):
    def __init__(self, text, duration=2.0, **kwargs):
        super().__init__(
            text=text,
            size_hint=(None, None),
            size=(500, 50),
            halign='center',
            valign='middle',
            font_size='18sp',
            color=(1, 1, 1, 1),
            **kwargs
        )
        self.opacity = 0.95
        self.padding = (10, 10)
        self.background_color = (0.1, 0.1, 0.1, 0.75)
        self.border_color = (1, 1, 1, 1)
        self.border_width = 2

        with self.canvas.before:
            Color(*self.background_color)
            self.bg = RoundedRectangle(radius=[12], size=self.size, pos=self.pos)

            Color(*self.border_color)
            
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 12), width=self.border_width)

        self.bind(pos=self.update_bg, size=self.update_bg)

        Clock.schedule_once(lambda dt: self.fade_out(), duration)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 12)

    def fade_out(self):
        if self.parent:
            self.parent.remove_widget(self)

def show_toast(screen, message, duration=2.0):
    toast = Toast(message, duration)

    # Try to add the toast to the left/main content area
    try:
        # Assume screen has BoxLayout with left and right children
        box = screen.children[0]  # Main layout
        left_area = box.children[1]  # Left side (index 1 because children is reversed)

        # Wrap left area in FloatLayout if it isn't already
        if not isinstance(left_area, FloatLayout):
            new_left = FloatLayout(size_hint=left_area.size_hint)
            for w in left_area.children[:]:
                new_left.add_widget(w)
            box.remove_widget(left_area)
            box.add_widget(new_left, index=1)
            left_area = new_left

        # Position toast at top center of left area
        toast.pos_hint = {'center_x': 0.5, 'top': 0.98}
        left_area.add_widget(toast)

    except Exception as e:
        print("Could not show toast:", e)

# Main Dashboard Screen
class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
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
        right_layout.add_widget(Widget(size_hint_y=1))
        button_labels = ['Open Account', 'Withdraw', 'Deposit', 'Transfer', 'Become a Teller']
        for label in button_labels:
            btn = Button(text=label, size_hint=(1, None), height=80)
            if label == 'Deposit':
                btn.bind(on_press=self.go_to_deposit)
            elif label == 'Open Account':
                btn.bind(on_press=self.go_to_open_account)
            elif label == 'Withdraw':
                btn.bind(on_press=self.go_to_withdraw)
            right_layout.add_widget(btn)
        right_layout.add_widget(Widget(size_hint_y=1))

        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        self.add_widget(layout)

    def go_to_deposit(self, instance):
        self.manager.current = 'deposit'

    def go_to_open_account(self, instance):
        self.manager.current = 'open_account'

    def go_to_withdraw(self, instance):
        self.manager.current = 'withdraw'


# Scanning Screen
class ScanningScreen(Screen):
    def __init__(self, scanning_message, start_scan, cancel_scan, on_finish_scan, **kwargs):
        super(ScanningScreen, self).__init__(**kwargs)
        self.start_scan = start_scan
        self.cancel_scan = cancel_scan
        self.on_finish_scan = on_finish_scan
        self.scanning_message = scanning_message
        
        layout = BoxLayout(orientation='horizontal')

        # Left area with instruction text
        left_layout = FloatLayout(size_hint=(0.66, 1))
        label = Label(
            text=scanning_message,
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

    def on_enter(self):
        # Start the scanning process when entering this screen
        self.start_scan(self.name, self.on_finish_scan, self.on_scan_fail)

    def on_scan_fail(self, message):
        # Handle scan failure
        show_toast(self, message, 2)
        self.manager.current = 'dashboard'

    def go_back(self, instance):
        self.cancel_scan()
        self.manager.current = 'dashboard'


class AmountConfirmationScreen(Screen):
    def __init__(self, action_text, **kwargs):
        super(AmountConfirmationScreen, self).__init__(**kwargs)
        self.on_complete = lambda amount: None  # Placeholder for callback

        layout = BoxLayout(orientation='horizontal')

        # --- Left side (main area) ---
        left_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.66, 1),
            padding=20,
            spacing=20
        )

        # Scanned amount image
        self.amount_img = Image(
            source='',
            size_hint=(1, 0.6),
            allow_stretch=True,
            keep_ratio=True
        )
        left_layout.add_widget(self.amount_img)

        # Number input field
        self.amount_input = TextInput(
            hint_text='Enter amount to confirm',
            multiline=False,
            input_filter='float',
            font_size='24sp',
            size_hint=(1, None),
            height=60
        )
        left_layout.add_widget(self.amount_input)

        # confirmation button
        self.confirmation = Button(
            text=action_text,
            size_hint=(1, None),
            height=80
        )
        self.confirmation.bind(on_press=self.on_confirmation)
        left_layout.add_widget(self.confirmation)

        # --- Right side (optional) ---
        right_layout = BoxLayout(size_hint=(0.34, 1))
        
        # --- Right side (numeric keypad) ---
        right_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.34, 1),
            padding=10
        )

        keypad = GridLayout(
            cols=3,
            spacing=10,
            size_hint=(1, 0.8)
        )

        keys = ['1', '2', '3',
                '4', '5', '6',
                '7', '8', '9',
                '<', '0', '.']

        for key in keys:
            btn = Button(text=key, font_size='24sp')
            btn.bind(on_press=self.keypad_press)
            keypad.add_widget(btn)

        # Spacer and add keypad
        right_layout.add_widget(Widget(size_hint=(1, 0.1)))  # top spacer
        right_layout.add_widget(keypad)
        right_layout.add_widget(Widget(size_hint=(1, 0.1)))  # bottom spacer

        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        self.add_widget(layout)

    def set_amount_image(self, path):
        """Call this to update the scanned image dynamically"""
        self.amount_img.source = path
        self.amount_img.reload()

    def keypad_press(self, instance):
        key = instance.text
        if key == '<':  # backspace
            self.amount_input.text = self.amount_input.text[:-1]
        else:
            self.amount_input.text += key

    def on_confirmation(self, instance):
        amount = self.amount_input.text.strip()
        if not amount or not amount.isdigit() or float(amount) <= 0:
            show_toast(self, "Please enter a valid amount", 2)
            return
        print(f"Withdrawing: {amount}")
        if self.on_complete:
            self.on_complete(amount)
        # You can validate and trigger next actions here

# Main App with ScreenManager
class UiApp(App):
    def __init__(self, atm: ATM, printer: AccountPrinter, start_scan, cancel_scan, **kwargs):
        super(UiApp, self).__init__(**kwargs)
        self.start_scan = start_scan
        self.cancel_scan = cancel_scan
        self.atm = atm
        self.printer = printer

    def start(self, update_callback=None):
        if update_callback:
            self.update_callback = update_callback
            Clock.schedule_interval(lambda dt: update_callback(), 0.1)
        self.run()

    def change_screen(self, screen_name):
        def switch_screen(dt):
            self.manager.current = screen_name
        Clock.schedule_once(switch_screen)

    def build(self):
        self.manager = ScreenManager(transition=NoTransition())

        self.dashboard = DashboardScreen(name='dashboard')       
        self.deposit = ScanningScreen(name='deposit', scanning_message='Scan your deposit form now...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_deposit) 
        self.depositConfirm = AmountConfirmationScreen(name='deposit_confirm', action_text='Withdraw')
        self.openAccount = ScanningScreen(name='open_account', scanning_message='Scan your new account form...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_open_account)
        self.withdraw = ScanningScreen(name='withdraw', scanning_message='Scan your account receipt now...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_withdrawl) 

        self.manager.add_widget(self.dashboard)
        self.manager.add_widget(self.deposit)
        self.manager.add_widget(self.depositConfirm)
        self.manager.add_widget(self.openAccount)
        self.manager.add_widget(self.withdraw)
        return self.manager

    def on_finish_scanning_open_account(self, form_info: FormInfo):
        account_number = self.atm.create_account(form_info.name_file_path)
        account = self.atm.get_account(account_number)
        if not account:
            show_toast(self.openAccount, "Failed to create account", 2)
            return
        account_balance = account.balance
        self.printer.printAccount(account_number, account_balance)
        self.change_screen('dashboard')
        show_toast(self.dashboard, f"Account created, get receipt below.", 2)

    
    def on_finish_scanning_deposit(self, form_info: FormInfo):
        def on_amount_confirmation(amount):
            # Handle the amount confirmation
            print(f"Confirmed deposit of {amount} from account number: {form_info.to_account_number}")
            self.on_complete_deposit(form_info, amount)
        self.depositConfirm.set_amount_image(form_info.amount_file_path)
        self.depositConfirm.on_complete = on_amount_confirmation
        self.change_screen('deposit_confirm')
        
    
    def on_complete_deposit(self, form_info: FormInfo, amount):
        # Handle the completion of the deposit process
        self.atm.deposit(form_info.to_account_number, amount)
        self.change_screen('dashboard')
        show_toast(self.dashboard, f"Deposited {amount} beans into account: {form_info.to_account_number}", 2)

    def on_finish_scanning_withdrawl(self, form_info: FormInfo):
        amount = self.atm.withdraw(form_info.from_account_number)
        self.change_screen('dashboard')
        show_toast(self.dashboard, f"Withdrew {amount} beans from account: {form_info.to_account_number}", 2)


