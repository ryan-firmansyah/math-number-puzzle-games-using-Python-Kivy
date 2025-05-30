from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from math import ceil, sqrt
import random
from kivy.core.audio import SoundLoader
from gamecomplete import GameCompleteScreen
from kivy.uix.screenmanager import Screen

class GameLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_manager = GameManager()
        self.start_new_level()
    
    def start_new_level(self):
        # Remove old playing area if exists
        if hasattr(self, 'current_playing_area'):
            self.remove_widget(self.current_playing_area)
            if hasattr(self, 'current_score_label'):
                self.remove_widget(self.current_score_label)
        
        # Create new playing area
        playing_area = self.game_manager.start_level()
        if playing_area:
            self.current_playing_area = playing_area
            self.current_score_label = playing_area.score_label
            self.add_widget(self.current_playing_area)
            self.add_widget(self.current_score_label)

class ScoreLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '20sp'
        self.color = (1, 1, 1, 1)
        self.update_score(0)

    def update_score(self, score):
        self.text = f'Score: {score}'

class LevelCompletePopup(Popup):
    def __init__(self, level, score, callback, **kwargs):
        super().__init__(**kwargs)
        self.title = ""  
        self.size_hint = (None, None)
        self.size = (300, 100)  
        self.auto_dismiss = True  
        self.background = ''  
        self.background_color = (0, 0, 0, 0)
        
        self.label = Label(
            text=f'Level {level} Complete',
            color=(1, 1, 1, 1),  
            font_size='24sp'
        )
        
        self.content = self.label
        
        # Automatically dismiss the popup after a delay and proceed to the next level
        Clock.schedule_once(lambda dt: self.finish_transition(callback), 2)

    def finish_transition(self, callback):
        self.dismiss()
        callback()

class NotifikasoPopup(Popup):
    def __init__(self, textnotif="", **kwargs):
        super().__init__(**kwargs)
        
        # Setup popup properties
        self.title = textnotif  
        self.size_hint = (None, None)
        self.size = (300, 100)  # Ukuran popup dalam pixels
        self.auto_dismiss = True  # Popup akan hilang saat di klik
        self.separator_height = 0
        self.background = ''  # Hapus background default
        self.background_color = (1, 1, 1, 0)  # Transparent
        
        # Buat label untuk teks
        # self.label = Label(
        #     text= textnotif,
        #     color=(1, 1, 1, 1),  # Warna teks putih
        #     font_size='14sp'
        # )
        
        # Set label sebagai konten popup
        # self.content = self.label
        
        # Jadwalkan popup untuk menghilang setelah 2 detik
        Clock.schedule_once(self.dismiss, 2)

class ImageButton(ButtonBehavior, RelativeLayout):
    number = NumericProperty(0)
    is_selected = BooleanProperty(False)
    current_frame = NumericProperty(0)

    def __init__(self, number, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.size_hint = (None, None)
        self.size = (60, 60)
        
        # List gambar untuk animasi
        self.frames = [
            'images/balon_merah1.png',    # Balon normal
            'images/balon_merah2.png',    # Balon retak pertama
            'images/balon_merah3.png',    # Balon retak kedua
            'images/balon_merah4.png',     # Balon pecah
            'images/balon_merah5.png'
        ]
        
        # Balon image
        self.image = Image(
            source=self.frames[0],
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.image)
        
        # Nomor balon
        self.label = Label(
            text=str(self.number),
            font_size='20sp',
            color=(1, 1, 1, 1),
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.label)
        self.bind(is_selected=self.update_appearance)

    def update_frame(self, frame_number):
        if 0 <= frame_number < len(self.frames):
            self.image.source = self.frames[frame_number]
            self.current_frame = frame_number

    def get_number(self):
        return self.number

    def update_appearance(self, instance, value):
        if value:
            self.image.color = (0.8, 0.8, 1, 1)
        else:
            self.image.color = (1, 1, 1, 1)

class PlayingArea(GridLayout):
    current_score = NumericProperty(0)  # Tambahkan ini di bagian atas kelas

    def __init__(self, level=1, total_score=0, **kwargs):
        super(PlayingArea, self).__init__(**kwargs)
        self.level = level
        self.total_score = total_score
        self.current_score = total_score
        self.balloon_count = 16 + (4 * (level - 1))
        
        # Menghitung jumlah kolom yang optimal
        self.cols = min(4, int(ceil(sqrt(self.balloon_count))))  # Maksimum 4 kolom
        self.rows = ceil(self.balloon_count / self.cols)
        
        # Set spacing dan padding
        self.spacing = [10, 10]  # Jarak antar balon
        
        # Hitung ukuran area permainan
        balloon_size = 60  # Ukuran setiap balon
        window_width = Window.width
        window_height = Window.height * 0.7  # 70% dari tinggi layar untuk area permainan
        
        # Hitung total lebar dan tinggi yang dibutuhkan
        total_width_needed = (self.cols * balloon_size) + ((self.cols - 1) * self.spacing[0])
        total_height_needed = (self.rows * balloon_size) + ((self.rows - 1) * self.spacing[1])
        
        # Hitung padding yang dibutuhkan untuk mempertahankan posisi tengah
        padding_x = (window_width - total_width_needed) / 2
        padding_y = (window_height - total_height_needed) / 2
        
        # Set padding untuk mempertahankan posisi tengah
        self.padding = [padding_x, padding_y, padding_x, padding_y]
        
        # Set ukuran layout
        self.size_hint = (None, None)
        self.size = (window_width, window_height)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        
        self.selected_balloon = None
        self.balloon_widgets = []
        
        # Score label
        self.score_label = ScoreLabel()
        self.score_label.pos_hint = {'top': 0.95, 'right': 0.98}
        self.score_label.update_score(self.total_score)

        # Load efek suara
        self.pop_sound = SoundLoader.load('music/balloon_pop3.mp3')
        if self.pop_sound:
            self.pop_sound.volume = 1.0
        
        self.setup_balloons()

    def setup_balloons(self):
        addition_of_10 = [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5)]
        balloon_numbers = []

        # Memastikan setidaknya setengah dari balon membentuk pasangan yang berjumlah 10
        pairs_needed = self.balloon_count // 2
        for _ in range(pairs_needed):
            pair = random.choice(addition_of_10)
            balloon_numbers.extend(pair)

        # Jika jumlah balon ganjil, tambahkan pasangan ekstra yang pasti valid
        if self.balloon_count % 2 != 0:
            extra_pair = random.choice(addition_of_10)
            balloon_numbers.extend(extra_pair)

        # Mengisi sisa balon dengan pasangan yang bisa dipasangkan
        while len(balloon_numbers) < self.balloon_count:
            remaining_pair = random.choice(addition_of_10)
            balloon_numbers.extend(remaining_pair)

        # Pastikan balon tidak lebih dari jumlah yang dibutuhkan
        balloon_numbers = balloon_numbers[:self.balloon_count]

        random.shuffle(balloon_numbers)

        for num in balloon_numbers:
            balloon = ImageButton(number=num)
            balloon.bind(on_press=self.on_balloon_press)
            self.add_widget(balloon)
            self.balloon_widgets.append(balloon)
    
    def play_pop_animation(self, balloon1, balloon2):
        def animate_balloon(balloon, dt):
            if balloon.current_frame < len(balloon.frames) - 1:
                balloon.current_frame += 1
                balloon.update_frame(balloon.current_frame)

                # Mainkan suara pada frame terakhir
                if balloon.current_frame == len(balloon.frames) - 1:
                    if self.pop_sound:
                        # Buat copy suara untuk memungkinkan overlap
                        pop = self.pop_sound.play()
                        if pop:
                            pop.volume = 1.0
            else:
                # Animasi selesai, hapus balon
                balloon.disabled = True
                balloon.opacity = 0
                if self.check_all_disabled():
                    self.show_level_complete()

        # Mulai animasi untuk kedua balon
        frame_duration = 0.05  # Durasi setiap frame (dalam detik)
        
        for frame in range(len(balloon1.frames)):
            Clock.schedule_once(
                lambda dt, b=balloon1: animate_balloon(b, dt),
                frame * frame_duration
            )
            Clock.schedule_once(
                lambda dt, b=balloon2: animate_balloon(b, dt),
                frame * frame_duration
            )

    def on_balloon_press(self, instance):
        if instance.disabled:
            return

        if self.selected_balloon is None:
            self.selected_balloon = instance
            self.highlight_balloon(instance)
        else:
            if self.selected_balloon == instance:
                self.unhighlight_balloon(instance)
                self.selected_balloon = None
            elif self.is_valid_second_balloon(instance):
                first_num = self.selected_balloon.get_number()
                second_num = instance.get_number()
                if first_num + second_num == 10:
                    self.unhighlight_balloon(self.selected_balloon)
                    self.play_pop_animation(self.selected_balloon, instance)
                    self.current_score += 1
                    self.total_score = self.current_score  # Update total_score
                    self.score_label.update_score(self.current_score)
                else:
                    print(f"Jumlah {first_num} + {second_num} tidak sama dengan 10")
                    popup = NotifikasoPopup(textnotif="Jumlah tidak sama dengan 10")  # Bisa diganti level sesuai kebutuhan
                    popup.open()
                    self.unhighlight_balloon(self.selected_balloon)
            else:
                print("Pilihan tidak valid. Coba pilih balon lain.")
                popup = NotifikasoPopup(textnotif="Pilihan tidak valid. Coba pilih balon lain.")  # Bisa diganti level sesuai kebutuhan
                popup.open()
                self.unhighlight_balloon(self.selected_balloon)
            
            self.selected_balloon = None

    def show_level_complete(self):
        popup = LevelCompletePopup(
            level=self.level,
            score=self.total_score,
            callback=self.on_level_complete
        )
        popup.open()

    def on_level_complete(self):
        if hasattr(self, 'on_level_finished'):
            self.on_level_finished(self.total_score)

    def is_valid_second_balloon(self, second_balloon):
        if self.selected_balloon is None or second_balloon.disabled:
            return False

        first_index = self.balloon_widgets.index(self.selected_balloon)
        second_index = self.balloon_widgets.index(second_balloon)
        
        if first_index == second_index:
            return False
        
        path = self.find_path(first_index, second_index)
        return path is not None

    def find_path(self, start, end):
        queue = [(start, [])]
        visited = set()
        
        while queue:
            current, path = queue.pop(0)
            if current == end:
                return path
            
            if current in visited:
                continue
            
            visited.add(current)
            
            for neighbor in self.get_valid_neighbors(current):
                if neighbor not in visited and (self.balloon_widgets[neighbor].disabled or neighbor == end):
                    new_path = path + [neighbor]
                    queue.append((neighbor, new_path))
        
        return None

    def get_valid_neighbors(self, index):
        row, col = divmod(index, self.cols)
        neighbors = []
        
        # Loop through potential neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            
            # Check if the new position is within the valid grid bounds
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                new_index = new_row * self.cols + new_col
                # Check that the new index is valid within balloon_widgets
                if 0 <= new_index < len(self.balloon_widgets):
                    neighbors.append(new_index)
        
        return neighbors
    
    def on_match_found(self):  # Atau metode yang menangani ketika pasangan benar ditemukan
        self.current_score += 10


    def remove_balloons(self, balloon1, balloon2):
        for balloon in [balloon1, balloon2]:
            balloon.disabled = True
            balloon.opacity = 0

    def disable_balloon(self, balloon):
        balloon.disabled = True

    def highlight_balloon(self, balloon):
        balloon.is_selected = True

    def unhighlight_balloon(self, balloon):
        balloon.is_selected = False

    def check_all_disabled(self):
        return all(balloon.disabled for balloon in self.balloon_widgets)
    

class GameManager:
    def __init__(self):
        self.current_level = 1
        self.max_level = 10
        self.total_score = 0
        self.playing_area = None
        self.game_layout = None

    def start_level(self):
        if self.current_level <= self.max_level:
            self.playing_area = PlayingArea(level=self.current_level, total_score=self.total_score)
            self.playing_area.on_level_finished = self.on_level_complete
            print(f"Level {self.current_level} dimulai!")
            print(f"Jumlah balon: {self.playing_area.balloon_count}")
            return self.playing_area
        else:
            self.go_to_game_complete()
            return None

    # def show_game_complete(self):
    #     popup = GameCompletePopup(total_score=self.total_score)
    #     popup.open()

    def go_to_game_complete(self):
        # Instead of showing popup, navigate to GameCompleteScreen
        app = App.get_running_app()
        game_complete_screen = GameCompleteScreen()
        
        # You might want to pass the total score to the GameCompleteScreen
        game_complete_screen.total_score = self.total_score
        
        # Add the screen to the screen manager if it's not already added
        if 'game_complete' not in app.root.screen_manager.screen_names:
            app.root.screen_manager.add_widget(
                Screen(name='game_complete', children=[game_complete_screen])
            )
        
        # Switch to the game complete screen
        app.root.current = 'game_complete'

    def on_level_complete(self, score):
        self.total_score = score
        if self.current_level < self.max_level:
            self.current_level += 1
            if hasattr(self, 'game_layout') and self.game_layout:
                Clock.schedule_once(lambda dt: self.game_layout.start_new_level(), 0.5)
        else:
            self.go_to_game_complete()

