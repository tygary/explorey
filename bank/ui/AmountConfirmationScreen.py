from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


from bank.ui.Toast import show_toast


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