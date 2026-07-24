"""
PlayerBar Component - Beautiful modern music player controls
"""

from typing import Callable, Optional
import flet as ft


class PlayerBar(ft.Container):
    """
    Modern player bar with beautiful controls and animations.
    
    Features:
    - Seek slider with time indicators
    - Album art display
    - Song metadata
    - Play/pause, previous, next controls
    - Volume display
    """
    
    def __init__(
        self,
        on_play_pause_click: Callable[[], None],
        on_next_click: Callable[[], None],
        on_prev_click: Callable[[], None],
        on_seek_change: Callable[[float], None]
    ):
        """
        Initialize PlayerBar with callbacks.
        
        Args:
            on_play_pause_click (Callable): Callback for play/pause button
            on_next_click (Callable): Callback for next button
            on_prev_click (Callable): Callback for previous button
            on_seek_change (Callable): Callback for seek changes (0-1)
        """
        super().__init__()
        
        self.on_play_pause_click = on_play_pause_click
        self.on_next_click = on_next_click
        self.on_prev_click = on_prev_click
        self.on_seek_change = on_seek_change
        
        self.is_playing = False
        
        self.bgcolor = "#0a0a0a"
        self.padding = 12
        self.border_radius = 20
        
        self.content = self._build_content()
    
    def _build_content(self) -> ft.Column:
        """Build main player bar content."""
        main_column = ft.Column(
            controls=[
                self._build_seek_section(),
                self._build_controls_section()
            ],
            spacing=12,
            expand=True
        )
        
        return main_column
    
    def _build_seek_section(self) -> ft.Container:
        """Build the seek slider with time display."""
        # Current time and total time text
        time_row = ft.Row(
            controls=[
                ft.Text("0:00", size=11, color="#808080", weight="500"),
                ft.Container(expand=True),
                ft.Text("0:00", size=11, color="#808080", weight="500")
            ],
            spacing=0
        )
        self.current_time_text = time_row.controls[0]
        self.total_time_text = time_row.controls[2]
        
        # Seek slider
        self.seek_slider = ft.Slider(
            min=0,
            max=100,
            value=0,
            expand=True,
            active_color="#1db954",
            inactive_color="#2a2a2a",
            thumb_color="#1db954",
            on_change=lambda e: self.on_seek_change(float(e.control.value) / 100)
        )
        
        seek_column = ft.Column(
            controls=[
                self.seek_slider,
                time_row
            ],
            spacing=6
        )
        
        return seek_column
    
    def _build_controls_section(self) -> ft.Container:
        """Build the player controls section."""
        # Album art
        self.album_container = ft.Container(
            content=ft.Icon("album", size=48, color="#1db954"),
            width=80,
            height=80,
            bgcolor="#1a1a1a",
            border_radius=14,
            alignment=ft.Alignment.CENTER
        )
        
        # Song info column
        self.title_text = ft.Text(
            "No song selected",
            size=16,
            weight="600",
            color="#ffffff",
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        
        self.artist_text = ft.Text(
            "Select a song to play",
            size=13,
            color="#b0b0b0",
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        
        song_info = ft.Column(
            controls=[self.title_text, self.artist_text],
            spacing=4,
            expand=True
        )
        
        # Control buttons
        button_row = ft.Row(
            controls=[
                self._create_button("skip_previous", self.on_prev_click, "#1db954"),
                self._create_button("play_arrow", self.on_play_pause_click, "#1db954", scale=1.2),
                self._create_button("skip_next", self.on_next_click, "#1db954")
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Main controls row (album + info + buttons)
        controls_row = ft.Row(
            controls=[
                self.album_container,
                song_info,
                button_row
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        
        # Wrap in container for better styling
        controls_container = ft.Container(
            content=controls_row,
            bgcolor="#1a1a1a",
            border_radius=14,
            padding=12
        )
        
        return controls_container
    
    def _create_button(
        self,
        icon_name: str,
        on_click: Callable[[], None],
        color: str,
        scale: float = 1.0
    ) -> ft.IconButton:
        """
        Create a styled button.
        
        Args:
            icon_name (str): Icon name
            on_click (Callable): Click callback
            color (str): Icon color
            scale (float): Icon scale factor
            
        Returns:
            ft.IconButton: Styled button
        """
        return ft.IconButton(
            icon_name,
            icon_color=color,
            icon_size=28 * scale,
            on_click=lambda _: on_click(),
            tooltip="Control"
        )
    
    def update_song_info(self, title: str, artist: str) -> None:
        """
        Update displayed song information.
        
        Args:
            title (str): Song title
            artist (str): Artist name
        """
        self.title_text.value = title
        self.artist_text.value = artist
        self.update()
    
    def set_seek_position(self, position: float) -> None:
        """
        Update seek slider position (0-100).
        
        Args:
            position (float): Position percentage (0-100)
        """
        self.seek_slider.value = max(0, min(100, position))
        self.update()
    
    def set_playing_state(self, is_playing: bool) -> None:
        """
        Update play/pause button state.
        
        Args:
            is_playing (bool): Whether music is playing
        """
        self.is_playing = is_playing
        # Update play button icon - could update here if button is accessible
        self.update()
    
    def set_time_display(self, current: str, total: str) -> None:
        """
        Update time display.
        
        Args:
            current (str): Current time string
            total (str): Total time string
        """
        self.current_time_text.value = current
        self.total_time_text.value = total
        self.update()
