import random
import string
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.colorpicker import ColorPicker
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard

# Set default window size for mobile and lock orientation to portrait
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')  # Prevent window resizing
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background for hacker theme

class GeneratorApp(App):
    theme = {
        'background': (0.1, 0.1, 0.1, 1),
        'text': (0, 1, 0, 1),  # Green text for hacker theme
        'button': (0.2, 0.2, 0.2, 1),
        'button_text': (0, 1, 0, 1),
        'input': (0.15, 0.15, 0.15, 1),
        'input_text': (0, 1, 0, 1)
    }
    
    def build(self):
        self.title = "Random Credential Generator"
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(text="Random Credential Generator", 
                      font_size=24, 
                      size_hint=(1, 0.1),
                      color=self.theme['text'])
        self.root.add_widget(header)
        
        # Main content area
        content = GridLayout(cols=1, spacing=10, size_hint=(1, 0.8))
        
        # Name input
        name_layout = BoxLayout(orientation='vertical', spacing=5)
        name_layout.add_widget(Label(text="Name/Keyword for Username:", 
                                    color=self.theme['text']))
        self.name_input = TextInput(multiline=False, 
                                  background_color=self.theme['input'],
                                  foreground_color=self.theme['input_text'])
        name_layout.add_widget(self.name_input)
        content.add_widget(name_layout)
        
        # Username options
        username_options = BoxLayout(orientation='vertical', spacing=5)
        username_options.add_widget(Label(text="Username Options:", 
                                        color=self.theme['text']))
        
        # Username complexity
        username_complexity = GridLayout(cols=2, spacing=5)
        username_complexity.add_widget(Label(text="Complexity:", 
                                           color=self.theme['text']))
        self.username_complex_spinner = Spinner(
            text='Mix Characters',
            values=('Lower Case Only', 'Upper Case Only', 'Numbers Only', 
                   'Lower + Upper', 'Lower + Numbers', 'Upper + Numbers', 'Mix Characters'),
            background_color=self.theme['button'],
            color=self.theme['button_text']
        )
        username_complexity.add_widget(self.username_complex_spinner)
        username_options.add_widget(username_complexity)
        
        # Username length
        username_length = GridLayout(cols=2, spacing=5)
        username_length.add_widget(Label(text="Length (6-20):", 
                                       color=self.theme['text']))
        self.username_length_slider = Slider(min=6, max=20, value=10, step=1)
        self.username_length_label = Label(text="10", 
                                         color=self.theme['text'])
        self.username_length_slider.bind(value=self.update_username_length)
        username_length.add_widget(self.username_length_slider)
        username_length.add_widget(self.username_length_label)
        username_options.add_widget(username_length)
        
        content.add_widget(username_options)
        
        # Password options
        password_options = BoxLayout(orientation='vertical', spacing=5)
        password_options.add_widget(Label(text="Password Options:", 
                                        color=self.theme['text']))
        
        # Password complexity
        password_complexity = GridLayout(cols=2, spacing=5)
        password_complexity.add_widget(Label(text="Complexity:", 
                                           color=self.theme['text']))
        self.password_complex_spinner = Spinner(
            text='Mix Characters',
            values=('Lower Case Only', 'Upper Case Only', 'Numbers Only', 
                   'Lower + Upper', 'Lower + Numbers', 'Upper + Numbers', 'Mix Characters'),
            background_color=self.theme['button'],
            color=self.theme['button_text']
        )
        password_complexity.add_widget(self.password_complex_spinner)
        password_options.add_widget(password_complexity)
        
        # Password length
        password_length = GridLayout(cols=2, spacing=5)
        password_length.add_widget(Label(text="Length (8-32):", 
                                       color=self.theme['text']))
        self.password_length_slider = Slider(min=8, max=32, value=12, step=1)
        self.password_length_label = Label(text="12", 
                                          color=self.theme['text'])
        self.password_length_slider.bind(value=self.update_password_length)
        password_length.add_widget(self.password_length_slider)
        password_length.add_widget(self.password_length_label)
        password_options.add_widget(password_length)
        
        content.add_widget(password_options)
        
        self.root.add_widget(content)
        
        # Buttons at the bottom
        button_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.1))
        
        generate_btn = Button(text="Generate", 
                            background_color=self.theme['button'],
                            color=self.theme['button_text'])
        generate_btn.bind(on_press=self.generate_credentials)
        button_layout.add_widget(generate_btn)
        
        theme_btn = Button(text="Customize Theme", 
                         background_color=self.theme['button'],
                         color=self.theme['button_text'])
        theme_btn.bind(on_press=self.show_theme_customizer)
        button_layout.add_widget(theme_btn)
        
        self.root.add_widget(button_layout)
        
        # Results display with copy buttons
        self.result_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.25))
        
        # Username result with copy button
        username_box = BoxLayout(size_hint_y=None, height=40)
        self.username_result = Label(text="Username: ", 
                                   color=self.theme['text'],
                                   halign='left',
                                   size_hint=(0.7, 1))
        username_copy_btn = Button(text="Copy",
                                 size_hint=(0.3, 1),
                                 background_color=self.theme['button'],
                                 color=self.theme['button_text'])
        username_copy_btn.bind(on_press=lambda x: self.copy_to_clipboard(self.username_result.text.replace("Username: ", "")))
        username_box.add_widget(self.username_result)
        username_box.add_widget(username_copy_btn)
        
        # Password result with copy button
        password_box = BoxLayout(size_hint_y=None, height=40)
        self.password_result = Label(text="Password: ", 
                                   color=self.theme['text'],
                                   halign='left',
                                   size_hint=(0.7, 1))
        password_copy_btn = Button(text="Copy",
                                 size_hint=(0.3, 1),
                                 background_color=self.theme['button'],
                                 color=self.theme['button_text'])
        password_copy_btn.bind(on_press=lambda x: self.copy_to_clipboard(self.password_result.text.replace("Password: ", "")))
        password_box.add_widget(self.password_result)
        password_box.add_widget(password_copy_btn)
        
        self.result_layout.add_widget(username_box)
        self.result_layout.add_widget(password_box)
        self.root.add_widget(self.result_layout)
        
        return self.root
    
    def update_username_length(self, instance, value):
        self.username_length_label.text = str(int(value))
    
    def update_password_length(self, instance, value):
        self.password_length_label.text = str(int(value))
    
    def generate_credentials(self, instance):
        # Generate username
        name = self.name_input.text.strip()
        username_length = int(self.username_length_slider.value)
        username_complexity = self.username_complex_spinner.text
        
        username = self.generate_string(name, username_length, username_complexity)
        
        # Generate password
        password_length = int(self.password_length_slider.value)
        password_complexity = self.password_complex_spinner.text
        
        password = self.generate_string("", password_length, password_complexity)
        
        # Display results
        self.username_result.text = f"Username: {username}"
        self.password_result.text = f"Password: {password}"
    
    def generate_string(self, base, length, complexity):
        chars = ""
        
        if "Lower" in complexity:
            chars += string.ascii_lowercase
        if "Upper" in complexity:
            chars += string.ascii_uppercase
        if "Numbers" in complexity:
            chars += string.digits
        
        # If no complexity selected (shouldn't happen), default to mix
        if not chars:
            chars = string.ascii_letters + string.digits
        
        # If we have a base, use it as part of the result
        result = base
        
        # Fill remaining length with random characters
        remaining_length = length - len(result)
        if remaining_length > 0:
            result += ''.join(random.choice(chars) for _ in range(remaining_length))
        
        # If result is longer than requested (due to base), truncate
        if len(result) > length:
            result = result[:length]
        
        # Shuffle the characters (except the base if we want to keep it at start)
        if base:
            # Only shuffle the part after the base
            base_part = result[:len(base)]
            random_part = list(result[len(base):])
            random.shuffle(random_part)
            result = base_part + ''.join(random_part)
        else:
            result = list(result)
            random.shuffle(result)
            result = ''.join(result)
        
        return result
    
    def show_theme_customizer(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        color_picker = ColorPicker()
        content.add_widget(color_picker)
        
        buttons = BoxLayout(spacing=10, size_hint=(1, 0.1))
        
        cancel_btn = Button(text="Cancel")
        cancel_btn.bind(on_press=lambda x: self.popup.dismiss())
        buttons.add_widget(cancel_btn)
        
        apply_btn = Button(text="Apply")
        apply_btn.bind(on_press=lambda x: self.apply_theme(color_picker.color))
        apply_btn.bind(on_press=lambda x: self.popup.dismiss())
        buttons.add_widget(apply_btn)
        
        reset_btn = Button(text="Reset to Default")
        reset_btn.bind(on_press=lambda x: self.reset_theme())
        reset_btn.bind(on_press=lambda x: self.popup.dismiss())
        buttons.add_widget(reset_btn)
        
        content.add_widget(buttons)
        
        self.popup = Popup(title="Customize Theme", 
                     content=content,
                     size_hint=(0.9, 0.9))
        self.popup.open()
    
    def apply_theme(self, color):
        # Create a darker version for backgrounds
        bg_color = (max(0, color[0] * 0.2), max(0, color[1] * 0.2), max(0, color[2] * 0.2), 1)
        input_color = (max(0, color[0] * 0.3), max(0, color[1] * 0.3), max(0, color[2] * 0.3), 1)
        button_color = (max(0, color[0] * 0.4), max(0, color[1] * 0.4), max(0, color[2] * 0.4), 1)
        
        self.theme = {
            'background': bg_color,
            'text': color,
            'button': button_color,
            'button_text': color,
            'input': input_color,
            'input_text': color
        }
        
        self.update_theme()
    
    def reset_theme(self):
        self.theme = {
            'background': (0.1, 0.1, 0.1, 1),
            'text': (0, 1, 0, 1),  # Green text for hacker theme
            'button': (0.2, 0.2, 0.2, 1),
            'button_text': (0, 1, 0, 1),
            'input': (0.15, 0.15, 0.15, 1),
            'input_text': (0, 1, 0, 1)
        }
        self.update_theme()
    
    def update_theme(self):
        Window.clearcolor = self.theme['background']
        
        # Update all widgets with new colors
        for widget in self.root.walk():
            if isinstance(widget, Label):
                widget.color = self.theme['text']
            elif isinstance(widget, Button):
                widget.background_color = self.theme['button']
                widget.color = self.theme['button_text']
            elif isinstance(widget, TextInput):
                widget.background_color = self.theme['input']
                widget.foreground_color = self.theme['input_text']
            elif isinstance(widget, Spinner):
                widget.background_color = self.theme['button']
                widget.color = self.theme['button_text']
    
    def copy_to_clipboard(self, text):
        Clipboard.copy(text)
        self.show_copy_notification()
    
    def show_copy_notification(self):
        content = Label(text="Copied to clipboard!", color=(0, 1, 0, 1))
        popup = Popup(title="",
                     content=content,
                     size_hint=(0.5, 0.1),
                     auto_dismiss=True)
        popup.open()

if __name__ == '__main__':
    GeneratorApp().run()