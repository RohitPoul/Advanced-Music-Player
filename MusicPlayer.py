import tkinter as tk
from tkinter import ttk, filedialog
import pygame
import os
from mutagen import File
from mutagen.easyid3 import EasyID3
from PIL import Image, ImageTk
import requests
import io
import json
import threading
import time

class MusicPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Music Player")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Variables
        self.current_file = None
        self.playing = False
        self.current_time = 0
        self.song_length = 0
        self.volume = 0.5
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frames
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.middle_frame = ttk.Frame(self.root)
        self.middle_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Album art
        self.album_label = ttk.Label(self.middle_frame)
        self.album_label.pack(side=tk.LEFT, padx=10)
        
        # Metadata and lyrics frame
        self.info_frame = ttk.Frame(self.middle_frame)
        self.info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Metadata labels
        self.title_label = ttk.Label(self.info_frame, text="Title: ")
        self.title_label.pack(anchor=tk.W)
        
        self.artist_label = ttk.Label(self.info_frame, text="Artist: ")
        self.artist_label.pack(anchor=tk.W)
        
        self.album_label_text = ttk.Label(self.info_frame, text="Album: ")
        self.album_label_text.pack(anchor=tk.W)
        
        # Lyrics display
        self.lyrics_text = tk.Text(self.info_frame, height=10, width=40)
        self.lyrics_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Control buttons
        ttk.Button(self.bottom_frame, text="Open", command=self.open_file).pack(side=tk.LEFT, padx=5)
        self.play_button = ttk.Button(self.bottom_frame, text="Play", command=self.play_pause)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(self.bottom_frame, from_=0, to=100, 
                                    orient=tk.HORIZONTAL, variable=self.progress_var,
                                    command=self.seek)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Volume control
        self.volume_var = tk.DoubleVar(value=50)
        self.volume_scale = ttk.Scale(self.bottom_frame, from_=0, to=100,
                                    orient=tk.HORIZONTAL, variable=self.volume_var,
                                    command=self.set_volume)
        self.volume_scale.pack(side=tk.LEFT, padx=5)
        
        # Time labels
        self.time_label = ttk.Label(self.bottom_frame, text="0:00 / 0:00")
        self.time_label.pack(side=tk.LEFT, padx=5)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac")])
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        self.current_file = file_path
        
        # Load metadata
        try:
            audio = EasyID3(file_path)
            self.title_label.config(text=f"Title: {audio.get('title', ['Unknown'])[0]}")
            self.artist_label.config(text=f"Artist: {audio.get('artist', ['Unknown'])[0]}")
            self.album_label_text.config(text=f"Album: {audio.get('album', ['Unknown'])[0]}")
            
            # Try to load album art
            audio_file = File(file_path)
            if hasattr(audio_file, 'tags') and audio_file.tags:
                for tag in audio_file.tags:
                    if tag.startswith('APIC'):
                        artwork = audio_file.tags[tag].data
                        img = Image.open(io.BytesIO(artwork))
                        img = img.resize((200, 200), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.album_label.configure(image=photo)
                        self.album_label.image = photo
                        break
            
            # Fetch lyrics (example API call - you'll need to implement your preferred lyrics API)
            self.fetch_lyrics(audio.get('title', [''])[0], audio.get('artist', [''])[0])
            
        except Exception as e:
            print(f"Error loading metadata: {e}")
        
        # Load audio
        pygame.mixer.music.load(file_path)
        self.song_length = pygame.mixer.Sound(file_path).get_length()
        self.progress_bar.configure(to=self.song_length)
        self.update_time_label()
        
        # Start playing
        self.play_pause()
    
    def play_pause(self):
        if not self.current_file:
            return
            
        if self.playing:
            pygame.mixer.music.pause()
            self.play_button.config(text="Play")
        else:
            pygame.mixer.music.unpause() if pygame.mixer.music.get_pos() > 0 else pygame.mixer.music.play()
            self.play_button.config(text="Pause")
            threading.Thread(target=self.update_progress, daemon=True).start()
            
        self.playing = not self.playing
    
    def seek(self, value):
        if self.current_file and self.playing:
            pygame.mixer.music.set_pos(float(value))
    
    def set_volume(self, value):
        self.volume = float(value) / 100
        pygame.mixer.music.set_volume(self.volume)
    
    def update_progress(self):
        while self.playing:
            if pygame.mixer.music.get_busy():
                self.current_time = pygame.mixer.music.get_pos() / 1000
                self.progress_var.set(self.current_time)
                self.update_time_label()
            time.sleep(0.1)
    
    def update_time_label(self):
        current = time.strftime('%M:%S', time.gmtime(self.current_time))
        total = time.strftime('%M:%S', time.gmtime(self.song_length))
        self.time_label.config(text=f"{current} / {total}")
    
    def fetch_lyrics(self, title, artist):
        # This is a placeholder - you'll need to implement your preferred lyrics API
        # Example using a hypothetical API:
        try:
            # Replace with actual API endpoint and key
            api_url = f"https://www.stands4.com/services/v2/lyrics.php"
            response = requests.get(api_url)
            lyrics = response.json()['lyrics']
            lyrics = "🎵 Lyrics will appear here...\nImplement your preferred lyrics API"
            self.lyrics_text.delete(1.0, tk.END)
            self.lyrics_text.insert(tk.END, lyrics)
        except Exception as e:
            self.lyrics_text.delete(1.0, tk.END)
            self.lyrics_text.insert(tk.END, "Lyrics not found")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    player = MusicPlayer()
    player.run()