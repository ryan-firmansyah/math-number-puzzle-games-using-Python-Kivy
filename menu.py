from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader 
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.screenmanager import Screen

Builder.load_file('menu.kv')

class ImageButton(ButtonBehavior, Image):
    # Buat button animasi
    def on_press(self):
        # if self.source == "icon_music/music_on.png" or "icon_music/music_off.png":
        if self.source == "icon_music/music_on.png" or self.source == "icon_music/music_off.png":
            anim = Animation(size_hint=(0.115, 0.115), duration=0.2) 
        else:
            anim = Animation(size_hint=(0.35, 0.35), duration=0.2)
        
        anim.start(self)

    def on_release(self):
        # 
        if self.source == "icon_music/music_on.png" or self.source == "icon_music/music_off.png":
            anim = Animation(size_hint=(0.1, 0.1), duration=0.2)  
        else:
            anim = Animation(size_hint=(0.3, 0.3), duration=0.2)  
        anim.start(self)

class MenuScreen(Screen):
    current_frame = 0
    frames = [] 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        base_width = 450
        window_height = int(base_width * (16 / 9))
        Window.size = (base_width, window_height)
        
        # with self.canvas.before:
        #     self.bg = Rectangle(source="images/home1.png", pos=self.pos, size=Window.size)
        
        for i in range(1, 149):  # Misalnya ada 4 frame
            self.frames.append(f"images/bggif/frame_{i}.png")

        with self.canvas.before:
            self.bg = Rectangle(source=self.frames[0], 
                            pos=self.pos, 
                            size=Window.size)
            
        Clock.schedule_interval(self.update_background, 0.1)

        Window.bind(size=self._update_bg_size)
        self.bind(pos=self._update_bg_size, size=self._update_bg_size)

        self.button_click_sound = SoundLoader.load('music/btn-click.mp3')

    def update_background(self, dt):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.bg.source = self.frames[self.current_frame]

    def _update_bg_size(self, *args):
        if hasattr(self, 'bg'):
            self.bg.size = Window.size
            self.bg.pos = self.pos

    def on_button_music_click(self):
        print("music button clicked")
        if self.button_click_sound:
            self.button_click_sound.play()
            
        App.get_running_app().toggle_music()
        
        # Update ikon tombol musik
        if App.get_running_app().sound_on:
            self.ids.music_button.source = 'icon_music/music_on.png'
        else:
            self.ids.music_button.source = 'icon_music/music_off.png'
            
    def on_button_play_click(self):
        print("Play Button Pressed")
        if self.button_click_sound:
            self.button_click_sound.play()
        # Pastikan screen manager ada dan screen 'play' terdaftar
        if hasattr(self, 'manager') and self.manager is not None:
            if 'play' in self.manager.screen_names:
                self.manager.current = 'play'
            else:
                print("Error: Screen 'play' tidak ditemukan")
        else:
            print("Error: Screen manager tidak ditemukan")