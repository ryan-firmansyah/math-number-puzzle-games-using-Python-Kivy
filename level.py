from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Color, Rectangle, Line

from kivy.uix.behaviors import ButtonBehavior

class ImageButton(ButtonBehavior, Image):
    pass

class SquareButton(Button):
    def __init__(self, **kwargs):
        super(SquareButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Gray color for the outline
            self.rect = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)

        # Bind size and position changes to update the outline
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.rectangle = (self.x, self.y, self.width, self.height)

# Define the LevelScreen class
class LevelScreen(Screen):
    def __init__(self, **kwargs):
        super(LevelScreen, self).__init__(**kwargs)
        base_width = 450
        window_height = int(base_width * (16 / 9))
        Window.size = (base_width, window_height)
        self.create_layout()

    def create_layout(self):
        with self.canvas.before:
            Color(0.53, 0.81, 0.92, 1)  # RGBA values for sky blue color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Bind size and position changes to update the background
        self.bind(size=self.update_rect, pos=self.update_rect)
        # Root layout with a vertical BoxLayout
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add a back button and title at the top
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100)
        
        # Add back button with an image (you can use an image for the back button)
        back_button = ImageButton(source='images/back.png', size_hint= (None, None), size=(30, 30), pos_hint= {"x": 0.05, "top": 0.95})  # Add the correct image path
        title = Label(text="LEVEL", font_size='40sp', size_hint=(0.8, 1), pos_hint= {"center_x": 0.5, "center_y": 0.80})
        
        top_layout.add_widget(back_button)
        top_layout.add_widget(title)

        # Grid layout for levels (3x5 grid)
        grid = GridLayout(cols=3, rows=5, spacing=10, size_hint=(1, 0.8))

        # Level buttons 1 to 9
        for i in range(1, 2):
            btn = ImageButton(source='images/Group18.png')
            grid.add_widget(btn)

        # Locked levels (add images of locks)
        for _ in range(14):
            lock_icon = ImageButton(source='images/Group19.png')  # Replace 'lock_icon.png' with the path to your lock image
            grid.add_widget(lock_icon)

        # Add layouts to root
        root.add_widget(top_layout)
        root.add_widget(grid)

        # Add the layout to the screen
        self.add_widget(root)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

# Define the main application class
class LevelSelectionApp(App):
    def build(self):
        return LevelScreen()

if __name__ == "__main__":
    LevelSelectionApp().run()
