"""
Flet Music Player - Main Application

Central controller for the music player application.
Manages state, components, and user interactions.
"""

import flet as ft
import logging
from typing import List, Dict

# Import components
from core.file_scanner import MusicScanner
from core.audio_manager import AudioManager
from ui.library_view import LibraryView
from ui.player_bar import PlayerBar

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(page: ft.Page) -> None:
    """
    Main application entry point.
    
    Sets up the Flet page, initializes all components, and manages the app state.
    
    Args:
        page (ft.Page): The Flet page object.
    """
    
    # ============================================================================
    # PAGE CONFIGURATION
    # ============================================================================
    page.title = "🎵 Music Player"
    page.window_width = 450
    page.window_height = 900
    page.window_min_width = 350
    page.window_min_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.margin = 0
    page.bgcolor = "#0a0a0a"
    page.window_frameless = False
    
    # Set theme colors
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#1db954",
            secondary="#1db954",
            tertiary="#1db954"
        )
    )
    
    logger.info("Page configured with beautiful dark theme")
    
    # ============================================================================
    # STATE INITIALIZATION
    # ============================================================================
    state = {
        'songs': [],
        'current_song_index': 0,
    }
    
    # ============================================================================
    # COMPONENT INITIALIZATION
    # ============================================================================
    
    # Callback for audio position changes
    def on_position_changed(position_ms: int) -> None:
        """
        Handle audio position updates from AudioManager.
        
        Args:
            position_ms (int): Current position in milliseconds.
        """
        if state['songs'] and player_bar:
            song = state['songs'][state['current_song_index']]
            duration_str = song.get('duration', '00:00')
            try:
                parts = duration_str.split(':')
                if len(parts) == 2:
                    total_seconds = int(parts[0]) * 60 + int(parts[1])
                    total_ms = total_seconds * 1000
                    if total_ms > 0:
                        position_normalized = position_ms / total_ms * 100
                        player_bar.set_seek_position(min(100, position_normalized))
            except (ValueError, IndexError):
                pass
    
    # Initialize AudioManager
    audio_manager = AudioManager(page, on_position_changed)
    logger.info("AudioManager initialized")
    
    # Initialize PlayerBar
    player_bar = PlayerBar(
        on_play_pause_click=None,  # Will be assigned after definition
        on_next_click=None,
        on_prev_click=None,
        on_seek_change=None
    )
    logger.info("PlayerBar initialized")
    
    # Initialize LibraryView
    library_view = LibraryView(
        songs=[],
        on_song_click=None  # Will be assigned after definition
    )
    logger.info("LibraryView initialized")
    
    # Initialize FilePicker for directory selection
    def on_folder_selected(e) -> None:
        """
        Handle folder selection from FilePicker.
        
        Scans the selected directory for music files and updates the library.
        
        Args:
            e: The file picker result event.
        """
        if e.path:
            logger.info(f"Folder selected: {e.path}")
            try:
                scanner = MusicScanner()
                state['songs'] = scanner.scan_directory(e.path)
                logger.info(f"Found {len(state['songs'])} songs")
                
                # Update LibraryView with new songs
                library_view.songs = state['songs']
                library_view.content = library_view._build_listview()
                
                # Reset current song index
                state['current_song_index'] = 0
                
                # Load first song if available
                if state['songs']:
                    song = state['songs'][0]
                    player_bar.update_song_info(song['title'], song['artist'])
                    audio_manager.load_and_play(song['file_path'])
                    logger.info(f"Loaded first song: {song['title']}")
                
                page.update()
                
            except Exception as ex:
                logger.error(f"Error scanning directory: {ex}")
    
    file_picker = ft.FilePicker()
    file_picker.on_result = on_folder_selected
    page.overlay.append(file_picker)
    logger.info("FilePicker initialized and added to page overlay")
    
    # ============================================================================
    # CALLBACK IMPLEMENTATIONS
    # ============================================================================
    
    def on_song_click(song: Dict[str, str]) -> None:
        """
        Handle song selection from LibraryView.
        
        Args:
            song (Dict[str, str]): The selected song dictionary.
        """
        try:
            # Find song index
            state['current_song_index'] = state['songs'].index(song)
            
            # Update player bar
            player_bar.update_song_info(song['title'], song['artist'])
            player_bar.set_seek_position(0)
            
            # Load and play audio
            audio_manager.load_and_play(song['file_path'])
            
            logger.info(f"Playing: {song['title']} by {song['artist']}")
            page.update()
            
        except ValueError:
            logger.error(f"Song not found in list")
        except Exception as ex:
            logger.error(f"Error playing song: {ex}")
    
    def on_play_pause() -> None:
        """Handle play/pause button click."""
        try:
            is_playing = audio_manager.toggle_play_pause()
            player_bar.set_playing_state(is_playing)
            status = "Playing" if is_playing else "Paused"
            logger.info(f"{status}")
            page.update()
        except Exception as ex:
            logger.error(f"Error toggling play/pause: {ex}")
    
    def on_next() -> None:
        """Handle next button click."""
        try:
            if state['songs']:
                state['current_song_index'] = (state['current_song_index'] + 1) % len(state['songs'])
                song = state['songs'][state['current_song_index']]
                
                player_bar.update_song_info(song['title'], song['artist'])
                player_bar.set_seek_position(0)
                
                audio_manager.load_and_play(song['file_path'])
                
                logger.info(f"Skipped to next: {song['title']}")
                page.update()
        except Exception as ex:
            logger.error(f"Error skipping to next: {ex}")
    
    def on_prev() -> None:
        """Handle previous button click."""
        try:
            if state['songs']:
                state['current_song_index'] = (state['current_song_index'] - 1) % len(state['songs'])
                song = state['songs'][state['current_song_index']]
                
                player_bar.update_song_info(song['title'], song['artist'])
                player_bar.set_seek_position(0)
                
                audio_manager.load_and_play(song['file_path'])
                
                logger.info(f"Skipped to previous: {song['title']}")
                page.update()
        except Exception as ex:
            logger.error(f"Error skipping to previous: {ex}")
    
    def on_seek_change(position: float) -> None:
        """
        Handle seek slider change.
        
        Args:
            position (float): Seek position as percentage (0-100).
        """
        try:
            if state['songs']:
                song = state['songs'][state['current_song_index']]
                duration_str = song.get('duration', '00:00')
                
                parts = duration_str.split(':')
                if len(parts) == 2:
                    total_seconds = int(parts[0]) * 60 + int(parts[1])
                    position_ms = int((position / 100) * total_seconds * 1000)
                    audio_manager.seek(position_ms)
                    logger.info(f"Seeked to {position:.1f}%")
        except (ValueError, IndexError) as ex:
            logger.error(f"Error seeking: {ex}")
    
    # Assign callbacks to components
    player_bar.on_play_pause_click = on_play_pause
    player_bar.on_next_click = on_next
    player_bar.on_prev_click = on_prev
    player_bar.on_seek_change = on_seek_change
    
    library_view.on_song_click = on_song_click
    
    # ============================================================================
    # LAYOUT CREATION
    # ============================================================================
    
    # Create AppBar with folder picker button
    app_bar = ft.AppBar(
        title=ft.Row(
            controls=[
                ft.Icon("music", size=28, color="#1db954"),
                ft.Text("Music Player", size=24, weight="bold", color="#ffffff")
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#0a0a0a",
        toolbar_height=70,
        elevation=4,
        shadow_color="#1db95440",
        actions=[
            ft.Container(
                content=ft.IconButton(
                    "folder_open",
                    icon_color="#1db954",
                    icon_size=24,
                    tooltip="Select Music Folder",
                    on_click=lambda e: file_picker.get_directory_path()
                ),
                padding=8
            )
        ]
    )
    
    # Create main layout
    main_column = ft.Column(
        controls=[
            library_view,
            player_bar
        ],
        spacing=0,
        expand=True
    )
    
    # Add AppBar and main layout to page
    page.appbar = app_bar
    page.add(main_column)
    
    logger.info("Application UI built and ready")


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
