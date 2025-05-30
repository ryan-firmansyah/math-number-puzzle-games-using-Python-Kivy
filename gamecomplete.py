from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.button import Button

class IButton(ButtonBehavior, Image):
    pass

class GameCompleteScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set window size
        base_width = 450
        window_height = int(base_width * (16 / 9))
        Window.size = (base_width, window_height)
        
        # Add background image
        self.background = Image(
            source="images/bg2.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.background)

        # Add back button
        self.back_button = IButton(
            source="icon_music/button_back.png",
            size_hint=(0.15, 0.15),
            pos_hint={"x": 0.05, "top": 0.95}
        )
        self.back_button.bind(on_press=self.on_button_back_click)
        self.add_widget(self.back_button)
    
        # Add play again button
        self.play_again_button = Button(
            text='Main Lagi',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        self.play_again_button.bind(on_press=self.on_play_again)
        self.add_widget(self.play_again_button)
    
    def on_button_back_click(self, instance):
        App.get_running_app().root.current = 'menu'

    def on_play_again(self, instance):
        # Reset game state and start over
        game_screen = App.get_running_app().root.get_screen('play')
        game_screen.reset_game()
        App.get_running_app().root.current = 'play'

class GameCompleteApp(App):
    def build(self):
        return GameCompleteScreen()

if __name__ == '__main__':
    GameCompleteApp().run()