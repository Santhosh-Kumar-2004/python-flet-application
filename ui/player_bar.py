"""
PlayerBar Component - Modern, feature-rich music player controls
"""

from typing import Callable, Optional
import flet as ft


class PlayerBar(ft.Container):
    """
    Beautiful modern player bar with premium controls and smooth animations.
    
    Features:
    - High-quality seek slider with time indicators
    - Large album art display
    - Song metadata display
    - Large, responsive play/pause button
    - Previous and next track controls
    - Smooth animations and hover effects
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
            on_seek_change (Callable): Callback for seek changes (0-100%)
        """
        super().__init__()
        
        self.on_play_pause_click = on_play_pause_click
        self.on_next_click = on_next_click
        self.on_prev_click = on_prev_click
        self.on_seek_change = on_seek_change
        
        self.is_playing = False
        self.current_duration_ms = 0
        
        self.bgcolor = "#0a0a0a"
        self.padding = 0
        self.border_radius = 0
        self.shadow = ft.BoxShadow(blur_radius=10, color="#00000040")
        
        # Build the content
        self.content = self._build_content()
    
    def _build_content(self) -> ft.Column:
        """Build main player bar content."""
        main_column = ft.Column(
            controls=[
                self._build_seek_section(),
                self._build_player_section()
            ],
            spacing=0,
            expand=True
        )
        return main_column
    
    def _build_seek_section(self) -> ft.Container:
        """Build the seek slider with beautiful time display."""
        # Current time text
        self.current_time_text = ft.Text(
            "0:00",
            size=11,
            color="#808080",
            weight="500"
        )
        
        # Total time text
        self.total_time_text = ft.Text(
            "0:00",
            size=11,
            color="#808080",
            weight="500"
        )
        
        # Time row with spacer
        time_row = ft.Row(
            controls=[
                self.current_time_text,
                ft.Container(expand=True),
                self.total_time_text
            ],
            spacing=0
        )
        
        # Seek slider with modern styling
        self.seek_slider = ft.Slider(
            min=0,
            max=100,
            value=0,
            expand=True,
            active_color="#1db954",
            inactive_color="#2a2a2a",
            thumb_color="#1db954",
            on_change=lambda e: self._handle_seek_change(e)
        )
        
        seek_column = ft.Column(
            controls=[
                self.seek_slider,
                time_row
            ],
            spacing=4,
            tight=True
        )
        
        seek_container = ft.Container(
            content=seek_column,
            bgcolor="#1a1a1a",
            padding=16,
            border_radius=0
        )
        
        return seek_container
    
    def _handle_seek_change(self, e) -> None:
        """Handle seek slider change."""
        if self.on_seek_change:
            self.on_seek_change(float(e.control.value))
    
    def _build_player_section(self) -> ft.Container:
        """Build the main player controls section."""
        # Album art - larger and more prominent
        self.album_container = ft.Container(
            content=ft.Icon("album", size=52, color="#1db954"),
            width=100,
            height=100,
            bgcolor="#1a1a1a",
            border_radius=16,
            alignment=ft.Alignment.CENTER,
            shadow=ft.BoxShadow(blur_radius=8, color="#1db95440")
        )
        
        # Song title
        self.title_text = ft.Text(
            "🎵 No song selected",
            size=18,
            weight="w900",
            color="#ffffff",
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        
        # Artist name
        self.artist_text = ft.Text(
            "Upload or open a music folder to start",
            size=13,
            color="#b0b0b0",
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        
        # Song info column
        song_info = ft.Column(
            controls=[self.title_text, self.artist_text],
            spacing=4,
            expand=True,
            tight=True
        )
        
        # Album and info row
        album_info_row = ft.Row(
            controls=[self.album_container, song_info],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        
        # Control buttons - play button is large
        control_buttons = ft.Row(
            controls=[
                self._create_button("skip_previous", self.on_prev_click, size=28),
                self._create_large_button("play_arrow", self.on_play_pause_click),
                self._create_button("skip_next", self.on_next_click, size=28)
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # Main player column
        player_column = ft.Column(
            controls=[
                album_info_row,
                ft.Container(height=16),
                control_buttons
            ],
            spacing=0,
            expand=False,
            tight=True
        )
        
        player_container = ft.Container(
            content=player_column,
            bgcolor="#0a0a0a",
            padding=16,
            border_radius=0,
            expand=True
        )
        
        return player_container
    
    def _create_button(
        self,
        icon_name: str,
        on_click: Callable,
        size: int = 24
    ) -> ft.Container:
        """
        Create a standard control button.
        
        Args:
            icon_name (str): Name of the icon
            on_click (Callable): Click callback
            size (int): Icon size
        
        Returns:
            ft.Container: Styled button container
        """
        return ft.Container(
            content=ft.IconButton(
                icon_name,
                icon_color="#1db954",
                icon_size=size,
                on_click=lambda e: on_click() if on_click else None
            ),
            padding=0
        )
    
    def _create_large_button(
        self,
        icon_name: str,
        on_click: Callable
    ) -> ft.Container:
        """
        Create a large play/pause button.
        
        Args:
            icon_name (str): Name of the icon
            on_click (Callable): Click callback
        
        Returns:
            ft.Container: Large styled button container
        """
        return ft.Container(
            content=ft.IconButton(
                icon_name,
                icon_color="#ffffff",
                icon_size=36,
                on_click=lambda e: on_click() if on_click else None,
                style=ft.ButtonStyle(
                    bgcolor="#1db954",
                    overlay_color="#1db954dd"
                )
            ),
            padding=0,
            bgcolor="#1db954",
            border_radius=50,
            width=60,
            height=60,
            alignment=ft.Alignment.CENTER,
            shadow=ft.BoxShadow(blur_radius=8, color="#1db95460")
        )
    
    def update_song_info(self, title: str, artist: str) -> None:
        """
        Update the song title and artist display.
        
        Args:
            title (str): Song title
            artist (str): Artist name
        """
        self.title_text.value = title
        self.artist_text.value = artist
    
    def set_playing_state(self, is_playing: bool) -> None:
        """
        Update the play button based on playing state.
        
        Args:
            is_playing (bool): Whether music is playing
        """
        self.is_playing = is_playing
        # Update will be called by parent
    
    def set_seek_position(self, percent: float) -> None:
        """
        Set the seek slider position.
        
        Args:
            percent (float): Position as percentage (0-100)
        """
        self.seek_slider.value = min(100, max(0, percent))
    
    def set_seek_position_ms(self, current_ms: int, total_ms: int) -> None:
        """
        Set seek position and update time display based on milliseconds.
        
        Args:
            current_ms (int): Current position in milliseconds
            total_ms (int): Total duration in milliseconds
        """
        self.current_duration_ms = total_ms
        
        # Update current time display
        current_seconds = current_ms // 1000
        current_minutes = current_seconds // 60
        current_secs = current_seconds % 60
        self.current_time_text.value = f"{current_minutes}:{current_secs:02d}"
        
        # Update total time display
        if total_ms > 0:
            total_seconds = total_ms // 1000
            total_minutes = total_seconds // 60
            total_secs = total_seconds % 60
            self.total_time_text.value = f"{total_minutes}:{total_secs:02d}"
            
            # Update slider position
            percent = (current_ms / total_ms) * 100
            self.seek_slider.value = min(100, max(0, percent))
