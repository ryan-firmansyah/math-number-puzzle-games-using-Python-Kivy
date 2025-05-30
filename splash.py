from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.progressbar import ProgressBar
from kivy.uix.video import Video

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        base_width = 450
        window_height = int(base_width * (16 / 9))
        Window.size = (base_width, window_height)
        print(f"SplashScreen init - Window size: {Window.size}")

        self.background = Image(
            source="images/splash1.png", allow_stretch=True, keep_ratio=False
        )
        self.add_widget(self.background)

        # self.background = Video(
        #     source="video/splash.mp4",   
        #     state='play',  
        #     options={'eos': 'loop'},   
        #     allow_stretch=True,
        #     keep_ratio=False
        # )
        # self.background.size = Window.size
        # self.background.pos = self.pos
        # self.add_widget(self.background)

        # image = Image(
        #     source="images/judul.png",
        #     color=(1, 0.5, 0.5, 1),  # RGB + Alpha (Opacity)
        #     pos_hint={"center_x": 0.5, "center_y": 0.80}
        # )
        # self.add_widget(image)

        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint=(0.5, None),
            height=20,
            pos_hint={"center_x": 0.5, "y": 0.1},
        )
        self.add_widget(self.progress_bar)

        self.total_time = 5
        self.elapsed_time = 0
        self.sound = None
        Clock.schedule_interval(self.update_progress, 1 / 30)

    # def on_enter(self):
        
    #     self.sound = SoundLoader.load("music/splash.mp3")
    #     if self.sound:
    #         self.sound.play()

    def update_progress(self, dt):
        self.elapsed_time += dt
        progress = min(100, (self.elapsed_time / self.total_time) * 100)
        self.progress_bar.value = progress

    def on_leave(self):
        Clock.unschedule(self.update_progress)
        if self.sound:
            self.sound.stop()