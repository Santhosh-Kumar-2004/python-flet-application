"""
LibraryView Component - Modern card-based music library display
"""

from typing import List, Dict, Callable, Optional
import flet as ft


class LibraryView(ft.Container):
    """
    Beautiful modern library view with card-based design.
    
    Features:
    - Responsive card tiles with album art
    - Smooth hover effects
    - Song selection highlighting
    - Dynamic song list updates
    """
    
    def __init__(
        self,
        songs: List[Dict[str, str]],
        on_song_click: Callable[[Dict[str, str]], None]
    ):
        """
        Initialize LibraryView with songs and callback.
        
        Args:
            songs (List[Dict[str, str]]): List of song dictionaries
            on_song_click (Callable): Callback when song is clicked
        """
        super().__init__()
        
        self.songs = songs
        self.on_song_click = on_song_click
        self.selected_index = None
        self.tiles = []
        
        self.expand = True
        self.bgcolor = "#0a0a0a"
        
        self.content = self._build_listview()
    
    def _build_listview(self) -> ft.ListView:
        """
        Build scrollable list of song tiles.
        
        Returns:
            ft.ListView: Scrollable list container
        """
        self.tiles = []
        
        # Check if there are songs
        if not self.songs:
            empty_state = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon("music_note", size=64, color="#1db954"),
                        ft.Text(
                            "No Songs Yet",
                            size=20,
                            weight="w900",
                            color="#ffffff"
                        ),
                        ft.Text(
                            "Click the upload button to add music files",
                            size=14,
                            color="#b0b0b0"
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12
                ),
                alignment=ft.Alignment.CENTER,
                expand=True
            )
            
            list_view = ft.ListView(
                expand=True,
                controls=[empty_state]
            )
        else:
            list_view = ft.ListView(
                expand=True,
                spacing=8,
                padding=12
            )
            
            for idx, song in enumerate(self.songs):
                tile = self._create_song_tile(song, idx)
                self.tiles.append(tile)
                list_view.controls.append(tile)
        
        return list_view
    
    def _create_song_tile(self, song: Dict[str, str], index: int) -> ft.Container:
        """
        Create a beautiful card-based song tile.
        
        Args:
            song (Dict[str, str]): Song metadata
            index (int): Song index
            
        Returns:
            ft.Container: Styled song tile
        """
        title = song.get("title", "Unknown Title")
        artist = song.get("artist", "Unknown Artist")
        duration = song.get("duration", "0:00")
        
        # Album art placeholder with gradient background
        album_art = ft.Container(
            content=ft.Icon("album", size=32, color="#1db954"),
            width=60,
            height=60,
            bgcolor="#1a1a1a",
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            shadow=ft.BoxShadow(blur_radius=4, color="#1db95420")
        )
        
        # Song info column
        song_info = ft.Column(
            controls=[
                ft.Text(
                    title,
                    size=14,
                    weight="w600",
                    color="#ffffff",
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=1
                ),
                ft.Text(
                    artist,
                    size=12,
                    color="#b0b0b0",
                    overflow=ft.TextOverflow.ELLIPSIS,
                    max_lines=1
                )
            ],
            spacing=3,
            expand=True,
            tight=True
        )
        
        # Duration badge
        duration_badge = ft.Container(
            content=ft.Text(duration, size=11, color="#1db954", weight="600"),
            padding=8,
            bgcolor="#1db95420",
            border_radius=6
        )
        
        # Main content row
        content_row = ft.Row(
            controls=[album_art, song_info, duration_badge],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        
        # Create tile container with better styling
        tile = ft.Container(
            content=content_row,
            bgcolor="#1a1a1a",
            border_radius=12,
            padding=12,
            on_hover=lambda e: self._handle_hover(e, tile, index),
            on_click=lambda _: self._handle_click(song, index, tile),
            shadow=ft.BoxShadow(blur_radius=2, color="#00000020")
        )
        
        return tile
    
    def _handle_hover(self, e, tile: ft.Container, index: int) -> None:
        """Handle hover effect on tile."""
        if e.data == "true":
            if self.selected_index != index:
                tile.bgcolor = "#242424"
        else:
            if self.selected_index != index:
                tile.bgcolor = "#1a1a1a"
        tile.update()
    
    def _handle_click(self, song: Dict[str, str], index: int, tile: ft.Container) -> None:
        """Handle tile click - update selection and trigger callback."""
        # Reset previous selection
        if self.selected_index is not None and self.selected_index < len(self.tiles):
            old_tile = self.tiles[self.selected_index]
            old_tile.bgcolor = "#1a1a1a"
            old_tile.update()
        
        # Highlight new selection
        tile.bgcolor = "#1db954"
        self.selected_index = index
        tile.update()
        
        # Call callback
        if self.on_song_click:
            self.on_song_click(song)
    
    def update_songs(self, songs: List[Dict[str, str]]) -> None:
        """
        Update songs dynamically.
        
        Args:
            songs (List[Dict[str, str]]): New song list
        """
        self.songs = songs
        self.selected_index = None
        self.content = self._build_listview()
        self.update()
