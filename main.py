from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from splash import SplashScreen
from menu import MenuScreen
from play import PlayingScreen
from kivy.core.audio import SoundLoader

class MathAppScreenManager(ScreenManager):
    pass

class TheMathApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load background music and set looping
        self.sound = SoundLoader.load('music/splash.mp3')
        self.sound_on = True
        if self.sound:
            self.sound.loop = True
            self.sound.play()

    def build(self):
        base_width = 450
        window_height = int(base_width * (16 / 9))
        Window.size = (base_width, window_height)
        
        # Buat screen manager
        sm = MathAppScreenManager()
        
        # Tambahkan semua screen
        splash_screen = SplashScreen(name='splash')
        menu_screen = MenuScreen(name='menu')
        playing_screen = PlayingScreen(name='play')
        
        # Pastikan semua screen ditambahkan ke manager
        sm.add_widget(splash_screen)
        sm.add_widget(menu_screen)
        sm.add_widget(playing_screen)
        
        # Set screen awal
        sm.current = 'splash'
        
        # Schedule perpindahan ke menu screen
        Clock.schedule_once(lambda dt: setattr(sm, 'current', 'menu'), 5)
        
        return sm
    
    def toggle_music(self):
        if self.sound_on:
            self.sound.stop()
            self.sound_on = False
        else:
            self.sound.play()
            self.sound_on = True

if __name__ == '__main__':
    TheMathApp().run()