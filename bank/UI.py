import os
os.environ['KIVY_HOME'] = '/home/admin/.kivy'
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
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout

from bank.ATM import ATM
from bank.FormScanner import FormInfo
from bank.AccountPrinter import AccountPrinter

class Toast(Label):
    def __init__(self, text, duration=8.0, **kwargs):
        super().__init__(
            text=text,
            size_hint=(None, None),
            size=(500, 500),
            halign='center',
            valign='middle',
            font_size='20sp',  # Increased from 18sp
            color=(1, 1, 1, 1),
            text_size=(500, None),  # Enable text wrapping by setting text_size to match width
            **kwargs
        )
        self.opacity = 0.95
        self.padding = (10, 10)
        self.background_color = (0.2, 0.2, 0.2, 1)
        self.border_color = (1, 1, 1, 1)
        self.border_width = 2

        with self.canvas.before:
            Color(*self.background_color)
            self.bg = RoundedRectangle(radius=[12], size=self.size, pos=self.pos)

            Color(*self.border_color)
            
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 12), width=self.border_width)

        self.bind(pos=self.update_bg, size=self.update_bg)
        Clock.schedule_once(lambda dt: self.fade_out(), duration)
        
        # Make the toast clickable
        self.bind(on_touch_down=self.on_touch_down)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)
        self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 12)

    def fade_out(self):
        if self.parent:
            self.parent.remove_widget(self)
            
    def on_touch_down(self, touch, other=None):
        # Add a short delay before the Toast starts responding to touch events
        self.touch_enabled = False
        Clock.schedule_once(lambda dt: setattr(self, 'touch_enabled', True), 0.5)

        if not getattr(self, 'touch_enabled', True):
            # print("Toast touch disabled temporarily to avoid residual events.")
            return True

        # Log touch position and Toast bounds for debugging
        print(f"Touch position: {touch.pos}, Toast bounds: {self.pos}, {self.size}")
        if self.collide_point(*touch.pos):
            if self.parent:
                print("Toast clicked, removing it")
                self.parent.remove_widget(self)
            return True
        return super(Toast, self).on_touch_down(touch)

def show_toast(screen, message, duration=8.0):
    def create_toast_on_main_thread(*args):
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

            # Position toast at middle center of left area
            toast.pos_hint = {'center_x': 0.5, 'top': 0.65}
            left_area.add_widget(toast)

        except Exception as e:
            print("Could not show toast:", e)

    # Schedule creation on the main thread
    Clock.schedule_once(create_toast_on_main_thread)

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
            btn = Button(text=label, size_hint=(1, None), height=80, font_size='22sp')  # Increased font size
            if label == 'Deposit':
                btn.bind(on_press=self.go_to_deposit)
            elif label == 'Open Account':
                btn.bind(on_press=self.go_to_open_account)
            elif label == 'Withdraw':
                btn.bind(on_press=self.go_to_withdraw)
            elif label == 'Transfer':
                btn.bind(on_press=self.go_to_transfer)

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
    
    def go_to_transfer(self, instance):
        self.manager.current = 'transfer'


# Scanning Screen
class ScanningScreen(Screen):
    def __init__(self, name, scanning_message, start_scan, cancel_scan, on_finish_scan, **kwargs):
        super(ScanningScreen, self).__init__(**kwargs)
        self.name = name
        self.start_scan = start_scan
        self.cancel_scan = cancel_scan
        self.on_finish_scan = on_finish_scan
        self.scanning_message = scanning_message
        
        layout = BoxLayout(orientation='horizontal')

        # Left area with instruction text
        left_layout = FloatLayout(size_hint=(0.66, 1))
        label = Label(
            text=scanning_message,
            font_size='26sp',  # Increased from 24sp
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
        right_layout.add_widget(Label(size_hint=(1, 0.1)))  # Spacer

        layout.add_widget(left_layout)
        layout.add_widget(right_layout)
        self.add_widget(layout)

    def on_enter(self):
        # Start the scanning process when entering this screen
        self.start_scan(self.name, self.on_finish_scan, self.on_scan_fail)

    def on_scan_fail(self, message):
        # Handle scan failure
        show_toast(self, message)
        self.manager.current = 'dashboard'

    def go_back(self, instance):
        self.cancel_scan()
        self.manager.current = 'dashboard'

# Scanning Screen
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


class AmountConfirmationScreen(Screen):
    def __init__(self, action_text, **kwargs):
        super(AmountConfirmationScreen, self).__init__(**kwargs)
        self.on_complete = lambda amount: None  # Placeholder for callback
        self.action_text = action_text

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
            font_size='26sp',  # Increased from 24sp
            size_hint=(1, None),
            height=60
        )
        left_layout.add_widget(self.amount_input)

        # confirmation button
        self.confirmation = Button(
            text=action_text,
            size_hint=(1, None),
            height=80,
            font_size='26sp'  # Increased font size
        )
        self.confirmation.bind(on_press=self.on_confirmation)
        left_layout.add_widget(self.confirmation)
        left_layout.add_widget(Label(size_hint=(1, 0.3)))  # Spacer

        # --- Right side (numeric keypad) ---
        right_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.34, 1),
            padding=10
        )
        
        # Create keypad with larger spacing
        keypad = GridLayout(
            cols=3,
            spacing=30,  # Increased spacing between buttons
            size_hint=(1, 0.8)
        )

        # Dictionary to store our buttons - we'll use this to implement press/release logic
        self.keypad_buttons = {}
        
        keys = ['1', '2', '3',
                '4', '5', '6',
                '7', '8', '9',
                '<', '0', '.']

        for key in keys:
            # Make buttons larger with more padding
            btn = Button(
                text=key,
                font_size='30sp',
                size_hint=(None, None),
                size=(80, 80),  # Fixed size buttons
                padding=(15, 15)
            )
            # Use direct on_release only - avoid on_press to prevent "bleed" to nearby buttons
            btn.bind(on_release=self.on_key_release)
            keypad.add_widget(btn)
            self.keypad_buttons[key] = btn

        # Spacer and add keypad
        right_layout.add_widget(Widget(size_hint=(1, 0.3)))  # top spacer
        right_layout.add_widget(keypad)
        right_layout.add_widget(Widget(size_hint=(1, 0.3)))  # bottom spacer

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

    def set_amount_image(self, path):
        """Call this to update the scanned image dynamically"""
        self.amount_img.source = path
        self.amount_img.reload()

    def on_key_release(self, instance):
        """Handle button release events only to avoid ghost presses"""
        key = instance.text
        print(f"Button {key} was released")
        if key == '<':  # backspace
            self.amount_input.text = self.amount_input.text[:-1]
        else:
            self.amount_input.text += key

    def on_confirmation(self, instance):
        amount = self.amount_input.text.strip()
        if not amount or not amount.isdigit() or float(amount) <= 0:
            show_toast(self, "Please enter a valid amount", 5)
            return
        print(f"{self.action_text}: {amount}")
        self.amount_input.text = ''
        if self.on_complete:
            self.on_complete(int(amount))
        # You can validate and trigger next actions here
    
    def go_back(self, instance):
        self.manager.current = 'dashboard'


# Main App with ScreenManager
class UiApp(App):
    def __init__(self, atm: ATM, printer: AccountPrinter, start_scan, cancel_scan, start_deposit, cancel_deposit, dispense_beans, get_interest_rate, get_exchange_rate, **kwargs):
        super(UiApp, self).__init__(**kwargs)
        self.start_scan = start_scan
        self.cancel_scan = cancel_scan
        self.start_deposit = start_deposit
        self.cancel_deposit = cancel_deposit
        self.dispense_beans = dispense_beans
        self.get_interest_rate = get_interest_rate
        self.get_exchange_rate = get_exchange_rate
        self.atm = atm
        self.printer = printer
        
        # Set window to maximized to cover entire screen
        Window.maximize()
        
        # Configure window to be borderless (no decorations)
        Window.borderless = True
        
    def build(self):
        # Create the screen manager
        self.manager = ScreenManager(transition=NoTransition())

        # Create the main container that will hold our bounded content
        main_container = FloatLayout()
        
        # Create a layout that will constrain our content to the specific coordinates
        # Note: Calculations are based on a maximized window covering the full screen
        # We'll position the content using relative coordinates
        content_layout = RelativeLayout(
            # Set size to exactly the dimensions we want
            size_hint=(None, None),
            size=(1000, 1200),  # Width and height
            # Position it at the desired coordinates
            pos=(0, 200)
        )
        
        # Add background color to the constrained area (optional)
        with content_layout.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # background
            RoundedRectangle(size=content_layout.size, pos=(0, 0))

        self.dashboard = DashboardScreen(name='dashboard')       
        self.deposit = ScanningScreen(name='deposit', scanning_message='Scan your deposit form now...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_deposit) 
        self.depositConfirm = AmountConfirmationScreen(name='deposit_confirm', action_text='Confirm Deposit')
        self.depositBeans = DepositScreen(name='deposit_beans', start_deposit=self.start_deposit, cancel_deposit=self.cancel_deposit, on_finish_deposit=self.on_complete_deposit)
        self.openAccount = ScanningScreen(name='open_account', scanning_message='Scan your new account form...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_open_account)
        self.withdraw = ScanningScreen(name='withdraw', scanning_message='Scan your account receipt now...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_withdrawl) 
        self.transfer = ScanningScreen(name='transfer', scanning_message='Scan your transfer form now...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_transfer)
        self.transferConfirm = AmountConfirmationScreen(name='transfer_confirm', action_text='Confirm Transfer')

        self.manager.add_widget(self.dashboard)
        self.manager.add_widget(self.deposit)
        self.manager.add_widget(self.depositConfirm)
        self.manager.add_widget(self.depositBeans)
        self.manager.add_widget(self.openAccount)
        self.manager.add_widget(self.withdraw)
        self.manager.add_widget(self.transfer)
        self.manager.add_widget(self.transferConfirm)
        
        # Add the screen manager to the content layout
        content_layout.add_widget(self.manager)
        
        # Add the content layout to the main container
        main_container.add_widget(content_layout)
        
        # Create a black background for the entire window
        with main_container.canvas.before:
            Color(0, 0, 0, 1)  # Black background for the rest of the window
            Rectangle(size=Window.size, pos=(0, 0))
        
        return main_container

    def start(self, update_callback=None):
        if update_callback:
            self.update_callback = update_callback
            Clock.schedule_interval(lambda dt: update_callback(), 0.1)
        self.run()

    def change_screen(self, screen_name):
        def switch_screen(dt):
            self.manager.current = screen_name
        Clock.schedule_once(switch_screen)

    def on_finish_scanning_open_account(self, form_info: FormInfo):
        account_number = self.atm.create_account(form_info.name_file_path)
        account = self.atm.get_account(account_number)
        if not account:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "Failed to create account")
            return
        account_balance = account.balance
        self.printer.printAccount(account_number, account_balance, account.name_file_path)
        self.change_screen('dashboard')
        show_toast(self.dashboard, f"Account created, get receipt below.")

    
    def on_finish_scanning_deposit(self, form_info: FormInfo):
        def on_amount_confirmation(amount):
            # Handle the amount confirmation
            print(f"Confirmed deposit of {amount} from account number: {form_info.to_account_number}")
            self.depositBeans.set_values(form_info, amount)
            self.change_screen('deposit_beans')
        account = self.atm.get_account(form_info.to_account_number)
        if not account:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "Failed to deposit into account.  Account not found")
            return
        self.depositConfirm.set_amount_image(form_info.amount_file_path)
        self.depositConfirm.on_complete = on_amount_confirmation
        self.change_screen('deposit_confirm')
    
    def on_complete_deposit(self, form_info: FormInfo, amount):
        # Handle the completion of the deposit process
        account = self.atm.deposit(form_info.to_account_number, amount)
        self.change_screen('dashboard')
        if not account:
            show_toast(self.dashboard, "Failed to deposit into account.  Account not found")
            return
        show_toast(self.dashboard, f"Deposited {amount} beans into account: {form_info.to_account_number}. Balance: {account.balance}")

    def on_finish_scanning_withdrawl(self, form_info: FormInfo):
        account, amount = self.atm.withdraw(form_info.from_account_number)
        self.change_screen('dashboard')
        if not account:
            show_toast(self.dashboard, "Failed to withdraw from account.  Account not found")
            return
        self.dispense_beans(amount)
        show_toast(self.dashboard, f"Withdrew {amount} beans from account: {form_info.from_account_number}.  Balance: {account.balance}")

    def on_finish_scanning_transfer(self, form_info: FormInfo):
        def on_amount_confirmation(amount):
            # Handle the amount confirmation
            print(f"Confirmed transfer of {amount} from account number: {form_info.from_account_number} to {form_info.to_account_number}")
            from_acc = self.atm.get_account(form_info.from_account_number)
            to_acc = self.atm.get_account(form_info.to_account_number)
            if not from_acc or not to_acc:
                self.change_screen('dashboard')
                show_toast(self.dashboard, "Failed to transfer, Account not found")
                return
            if from_acc.balance < amount:
                self.change_screen('dashboard')
                show_toast(self.dashboard, f"Insufficient funds in account {form_info.from_account_number}\nfor transfer of {amount} beans.")
                return
            self.atm.transfer(form_info.from_account_number, form_info.to_account_number, amount)
            self.change_screen('dashboard')
            show_toast(self.dashboard, f"Transferred {amount} beans\nFrom account: {form_info.from_account_number} (balance {from_acc.balance})\n To account: {form_info.to_account_number} (Balance: {to_acc.balance})")
            
            
        from_account = self.atm.get_account(form_info.from_account_number)
        if not from_account:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "Failed to find account to transfer from.")
            
            return
        to_account = self.atm.get_account(form_info.to_account_number)
        if not to_account:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "Failed to find account to transfer to.")
            return
        self.transferConfirm.set_amount_image(form_info.amount_file_path)
        self.transferConfirm.on_complete = on_amount_confirmation
        self.change_screen('transfer_confirm')
