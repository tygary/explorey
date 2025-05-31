import os
os.environ['KIVY_HOME'] = '/home/admin/.kivy'
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout

from bank.ATM import ATM
from bank.FormScanner import FormInfo
from bank.AccountPrinter import AccountPrinter
from bank.ui.Toast import show_toast
from bank.ui.AmountConfirmationScreen import AmountConfirmationScreen
from bank.ui.DashboardScreen import DashboardScreen
from bank.ui.DepositScreen import DepositScreen
from bank.ui.ScanningScreen import ScanningScreen
from bank.ui.TellerSignup import TellerSignupScreen
from bank.ui.TopAccountsListScreen import TopAccountsListScreen
from bank.ui.EconomyOverviewScreen import EconomyOverviewScreen
from bank.ui.BankruptcyConfirmationScreen import BankruptcyConfirmationScreen

# Main App with ScreenManager
class UiApp(App):
    def __init__(self, atm: ATM, printer: AccountPrinter, start_scan, cancel_scan, start_deposit, cancel_deposit, dispense_beans, get_interest_rate, get_debt_interest_rate, get_exchange_rate, **kwargs):
        super(UiApp, self).__init__(**kwargs)
        self.start_scan = start_scan
        self.cancel_scan = cancel_scan
        self.start_deposit = start_deposit
        self.cancel_deposit = cancel_deposit
        self.dispense_beans = dispense_beans
        self.get_interest_rate = get_interest_rate
        self.get_debt_interest_rate = get_debt_interest_rate
        self.get_exchange_rate = get_exchange_rate
        self.atm = atm
        self.get_sign_on_bonus = atm.get_sign_on_bonus
        self.get_withdrawl_amount = atm.get_withdrawl_amount
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

        self.dashboard = DashboardScreen(name='dashboard', atm=self.atm)       
        self.deposit = ScanningScreen(name='deposit', scanning_message='Scan your deposit form now...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_deposit) 
        self.depositConfirm = AmountConfirmationScreen(name='deposit_confirm', action_text='Confirm Deposit')
        self.depositBeans = DepositScreen(name='deposit_beans', start_deposit=self.start_deposit, cancel_deposit=self.cancel_deposit, on_finish_deposit=self.on_complete_deposit)
        self.openAccount = ScanningScreen(name='open_account', scanning_message='Scan your new account form...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_open_account)
        self.withdraw = ScanningScreen(name='withdraw', scanning_message='Scan your account receipt now...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_withdrawl) 
        self.transfer = ScanningScreen(name='transfer', scanning_message='Scan your transfer form now...', start_scan=self.start_scan, cancel_scan=self.cancel_scan, on_finish_scan=self.on_finish_scanning_transfer)
        self.transferConfirm = AmountConfirmationScreen(name='transfer_confirm', action_text='Confirm Transfer')
        self.tellerSignup = TellerSignupScreen(
            on_agree=lambda _: self.change_screen('teller_signup_scanning'),
            on_cancel=lambda _: self.change_screen('dashboard'),
            name='teller_signup'
        )
        self.tellerSignupScanning = ScanningScreen(
            name='teller_signup_scanning',
            scanning_message='Scan your account details receipt now...',
            start_scan=self.start_scan,  # Use existing scanning logic
            cancel_scan=lambda _: self.change_screen('dashboard'),
            on_finish_scan=self.on_finish_teller_signup,
            form_type='withdraw'
        )
        self.tellerSigninScanning = ScanningScreen(
            name='teller_signin_scanning',
            scanning_message='Scan your account details receipt to sign in...',
            start_scan=self.start_scan,
            cancel_scan=lambda _: self.change_screen('dashboard'),
            on_finish_scan=self.on_finish_teller_signin,
            form_type='withdraw'
        )
        self.leaderboard = TopAccountsListScreen(
            get_accounts=self.atm.get_top_accounts,
            is_leaderboard=True,
            name='leaderboard'
        )
        self.bankruptcyRoll = TopAccountsListScreen(
            get_accounts=self.atm.get_bankruptcy_roll,
            is_leaderboard=False,
            name='bankruptcy_roll'
        )
        self.economyOverview = EconomyOverviewScreen(
            get_exchange_rate=self.get_exchange_rate,
            get_interest_rate=self.get_interest_rate,
            get_debt_interest_rate=self.get_debt_interest_rate,
            get_sign_on_bonus=self.get_sign_on_bonus,
            get_withdrawl_amount=self.get_withdrawl_amount,
            name='economy_overview'
        )
        self.bankruptcyScanning = ScanningScreen(
            name='bankruptcy_scanning',
            scanning_message='Scan your account details receipt now...',
            start_scan=self.start_scan,
            cancel_scan=lambda _: self.change_screen('dashboard'),
            on_finish_scan=self.on_finish_scanning_bankruptcy,
            form_type='withdraw'
        )
        self.bankruptcyConfirm = BankruptcyConfirmationScreen(name='bankruptcy_confirm', on_finalize_bankruptcy=self.on_bankruptcy_confirmed)

        self.manager.add_widget(self.dashboard)
        self.manager.add_widget(self.deposit)
        self.manager.add_widget(self.depositConfirm)
        self.manager.add_widget(self.depositBeans)
        self.manager.add_widget(self.openAccount)
        self.manager.add_widget(self.withdraw)
        self.manager.add_widget(self.transfer)
        self.manager.add_widget(self.transferConfirm)
        self.manager.add_widget(self.tellerSignup)
        self.manager.add_widget(self.tellerSignupScanning)
        self.manager.add_widget(self.tellerSigninScanning)
        self.manager.add_widget(self.leaderboard)
        self.manager.add_widget(self.bankruptcyRoll)
        self.manager.add_widget(self.economyOverview)
        self.manager.add_widget(self.bankruptcyScanning)
        self.manager.add_widget(self.bankruptcyConfirm)
        
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
        account, amount, beanbucks, exchange_rate = self.atm.deposit(form_info.to_account_number, amount)
        self.change_screen('dashboard')
        if not account:
            show_toast(self.dashboard, "Failed to deposit into account.  Account not found")
            return
        show_toast(self.dashboard, f"Deposited {amount} beans with exchange rate {exchange_rate} for {beanbucks} BeanBucks into account: {form_info.to_account_number}. New Balance: {account.balance}")

    def on_finish_scanning_withdrawl(self, form_info: FormInfo):
        account, amount, beanbucks, exchange_rate = self.atm.withdraw(form_info.from_account_number)
        self.change_screen('dashboard')
        if not account:
            show_toast(self.dashboard, "Failed to withdraw from account.  Account not found")
            return
        self.dispense_beans(amount)
        show_toast(self.dashboard, f"Withdrew {beanbucks} BeanBucks with exchange rate {exchange_rate} from account: {form_info.from_account_number}.  Dispensing {amount} Beans.  New Balance: {account.balance}")

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

    def on_agree_to_teller(self, _):
        self.change_screen('teller_signup_scanning')

    def on_finish_teller_signup(self, form_info):
        account = self.atm.get_account(form_info.from_account_number)
        if not account:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "Failed to sign up as a teller. Account not found.")
            return
        if account.is_teller:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "You are already a teller. Sign in instead.")
            return
        self.atm.make_teller(form_info.from_account_number)
        self.atm.set_current_teller(form_info.from_account_number)
        self.dashboard.update_teller_section()
        self.change_screen('dashboard')
        show_toast(self.dashboard, "You have successfully signed up as a teller.")

    def on_finish_teller_signin(self, form_info):
        account = self.atm.get_account(form_info.from_account_number)
        if account is None:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "Failed to sign in as a teller. Account not found.")
            return
        if not account.is_teller:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "This account is not a teller account. Sign up first.")
            return
        self.atm.set_current_teller(form_info.from_account_number)
        self.dashboard.update_teller_section()
        self.change_screen('dashboard')
        show_toast(self.dashboard, f"Signed in as teller: {form_info.from_account_number}")

    def on_finish_scanning_bankruptcy(self, form_info: FormInfo):
        account = self.atm.get_account(form_info.from_account_number)
        if not account:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "Failed to find account for bankruptcy.")
            return
        if account.balance > 0:
            self.change_screen('dashboard')
            show_toast(self.dashboard, "This account is not in debt.")
            return
        self.bankruptcyConfirm.set_account(account)
        self.change_screen('bankruptcy_confirm')
    
    def on_bankruptcy_confirmed(self, account):
        self.atm.pay_teller_based_on_amount(abs(account.balance * 2))
        account.balance = 1
        self.atm.update_account(account)
        
        self.change_screen('dashboard')
        show_toast(self.dashboard, f"Account {account.account_number} has filed for bankruptcy and now has 1 bean.")
        