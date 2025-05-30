from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import Rectangle
from papan import PlayingArea, GameManager
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, BooleanProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader 
from kivy.app import App
from kivy.uix.screenmanager import Screen

Builder.load_file('play.kv')

class IButton(ButtonBehavior, Image):
    def on_press(self): 
        anim = Animation(size_hint=(.65, .65), duration=0.2) + Animation(size_hint=(.6, .6), duration=0.2)
        anim.start(self)

class PlayingScreen(Screen):
    current_level = NumericProperty(1)
    total_score = NumericProperty(0)
    game_manager = ObjectProperty(None, allownone=True)
    playing_area = ObjectProperty(None, allownone=True)  
    is_active = BooleanProperty(False)

    def update_score(self, new_score):
        self.total_score = new_score

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="images/bg1.png", pos=self.pos, size=Window.size)
        Window.bind(size=self._update_bg_size)
        self.bind(pos=self._update_bg_size, size=self._update_bg_size)
        
        self.game_manager = GameManager()

        self.button_click_sound = SoundLoader.load('music/btn-click.mp3')

    def _update_bg_size(self, *args):
        self.bg.size = Window.size
        self.bg.pos = self.pos

    def start_game(self, dt=None):
        print("Starting game...")
        self.is_active = True
        self.start_level(self.current_level)

    def start_level(self, level):
        print(f"Starting level {level}")  
        self.current_level = level
        
        if hasattr(self.ids, 'game_container'):
            if self.playing_area and self.playing_area in self.ids.game_container.children:
                self.ids.game_container.remove_widget(self.playing_area)
            
            if self.is_active:
                self.playing_area = PlayingArea(level=level, total_score=self.total_score)
                # Bind the score update method
                self.playing_area.bind(current_score=self.on_score_update)
                self.playing_area.on_level_finished = self.on_level_finished
                self.ids.game_container.add_widget(self.playing_area)
                print("Playing area added to container")
        else:
            print("Error: game_container not found in ids")

    def on_score_update(self, instance, value):
        """Called whenever the score changes in PlayingArea"""
        self.total_score = value
    
    def on_level_finished(self, score):
        if not self.is_active:
            return
        self.total_score = score
        if self.current_level < self.game_manager.max_level:
            Clock.schedule_once(lambda dt: self.start_next_level(), 0.5)
        else:
            self.game_manager.show_game_complete()

    def start_next_level(self):
        if not self.is_active:
            return
        self.current_level += 1
        self.start_level(self.current_level)

    def reset_game(self):
        self.current_level = 1
        self.total_score = 0
        self.is_active = False
        
        if hasattr(self.ids, 'game_container') and self.playing_area:
            if self.playing_area in self.ids.game_container.children:
                self.ids.game_container.remove_widget(self.playing_area)
        self.playing_area = None

    def on_enter(self):
        self.is_active = True
        if not self.playing_area:
            self.start_game()

    def on_leave(self):
        self.is_active = False
        if hasattr(self.ids, 'game_container') and self.playing_area:
            if self.playing_area in self.ids.game_container.children:
                self.ids.game_container.remove_widget(self.playing_area)
            self.playing_area = None

    def button_music_click(self):
        print("music button clicked")
        if self.button_click_sound:
            self.button_click_sound.play()
        
        App.get_running_app().toggle_music()
        
        if App.get_running_app().sound_on:
            self.ids.music_button.source = 'icon_music/music_on.png'
        else:
            self.ids.music_button.source = 'icon_music/music_off.png'
        
            
    def on_button_back_click(self):
        if self.button_click_sound:
            self.button_click_sound.play()
            
        Clock.schedule_once(self.change_screen_to_menu, 0.4)     
    
    def change_screen_to_menu(self,dt):
        self.manager.current = 'menu'
        self.reset_game()