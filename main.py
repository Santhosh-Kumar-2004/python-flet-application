"""
Flet Music Player - Modern Audio Player Application

A beautiful, feature-rich music player with intuitive UI and full audio support.
"""

import flet as ft
import logging
import os
from typing import List, Dict
from pathlib import Path

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
    page.window_width = 500
    page.window_height = 950
    page.window_min_width = 350
    page.window_min_height = 600
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.margin = 0
    page.bgcolor = "#0a0a0a"
    
    # Set modern theme with Spotify-inspired colors
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary="#1db954",
            secondary="#1db954",
            tertiary="#1db954"
        )
    )
    
    logger.info("Page configured with dark modern theme")
    
    # ============================================================================
    # STATE INITIALIZATION
    # ============================================================================
    state = {
        'songs': [],
        'current_song_index': -1,
        'music_folder': None,
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
        if state['current_song_index'] >= 0 and state['songs']:
            try:
                player_bar.set_seek_position_ms(position_ms, audio_manager.get_duration())
            except Exception as e:
                logger.error(f"Error updating position: {e}")
    
    # Initialize AudioManager
    audio_manager = AudioManager(page, on_position_changed)
    logger.info("AudioManager initialized with pygame")
    
    # Initialize PlayerBar
    player_bar = PlayerBar(
        on_play_pause_click=None,
        on_next_click=None,
        on_prev_click=None,
        on_seek_change=None
    )
    logger.info("PlayerBar initialized")
    
    # Initialize LibraryView
    library_view = LibraryView(
        songs=[],
        on_song_click=None
    )
    logger.info("LibraryView initialized")
    
    # ============================================================================
    # FILE PICKER SETUP
    # ============================================================================
    
    # For uploading individual files
    def on_files_selected(e) -> None:
        """
        Handle file selection from file picker.
        Supports uploading individual audio files or folders.
        
        Args:
            e: The file picker result event.
        """
        if e.files:
            logger.info(f"Files selected: {len(e.files)} file(s)")
            try:
                for file_info in e.files:
                    file_path = file_info.path
                    
                    # If it's a directory, scan it
                    if os.path.isdir(file_path):
                        scanner = MusicScanner()
                        new_songs = scanner.scan_directory(file_path)
                        state['songs'].extend(new_songs)
                        state['music_folder'] = file_path
                        logger.info(f"Added {len(new_songs)} songs from folder")
                    # If it's a file, try to add it
                    elif os.path.isfile(file_path):
                        if file_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                            # Extract metadata
                            file_name = os.path.basename(file_path)
                            name_without_ext = os.path.splitext(file_name)[0]
                            
                            song_data = {
                                'file_path': file_path,
                                'file_name': file_name,
                                'title': name_without_ext,
                                'artist': 'Unknown Artist',
                                'duration': '0:00'
                            }
                            
                            # Try to get metadata
                            try:
                                from tinytag import TinyTag
                                tag = TinyTag.get(file_path)
                                if tag.title:
                                    song_data['title'] = tag.title
                                if tag.artist:
                                    song_data['artist'] = tag.artist
                                if tag.duration:
                                    minutes = int(tag.duration // 60)
                                    seconds = int(tag.duration % 60)
                                    song_data['duration'] = f"{minutes}:{seconds:02d}"
                            except:
                                pass
                            
                            state['songs'].append(song_data)
                            logger.info(f"Added song: {song_data['title']}")
                
                # Update library view
                if state['songs']:
                    library_view.songs = state['songs']
                    library_view.content = library_view._build_listview()
                    
                    # If no song is playing, load the first one
                    if state['current_song_index'] < 0 and state['songs']:
                        state['current_song_index'] = 0
                        song = state['songs'][0]
                        player_bar.update_song_info(song['title'], song['artist'])
                        audio_manager.load_and_play(song['file_path'])
                        player_bar.set_playing_state(True)
                        logger.info(f"Auto-playing first song: {song['title']}")
                    
                    page.update()
                    
            except Exception as ex:
                logger.error(f"Error processing files: {ex}")
                show_error_snackbar(f"Error: {str(ex)}")
    
    file_picker = ft.FilePicker()
    file_picker.on_result = on_files_selected
    page.overlay.append(file_picker)
    logger.info("FilePicker initialized and added to page overlay")
    
    # ============================================================================
    # CALLBACK IMPLEMENTATIONS
    # ============================================================================
    
    def show_error_snackbar(message: str) -> None:
        """Show an error message using snackbar."""
        snack = ft.SnackBar(ft.Text(message, color="#ff6b6b"))
        page.overlay.append(snack)
        snack.open = True
        page.update()
    
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
            if audio_manager.load_and_play(song['file_path']):
                player_bar.set_playing_state(True)
                logger.info(f"Playing: {song['title']} by {song['artist']}")
            else:
                show_error_snackbar(f"Failed to play: {song['title']}")
            
            page.update()
            
        except ValueError:
            logger.error(f"Song not found in list")
            show_error_snackbar("Song not found")
        except Exception as ex:
            logger.error(f"Error playing song: {ex}")
            show_error_snackbar(f"Error playing song: {str(ex)}")
    
    def on_play_pause() -> None:
        """Handle play/pause button click."""
        try:
            if not state['songs'] or state['current_song_index'] < 0:
                show_error_snackbar("No song selected. Please upload or select a song.")
                return
            
            is_playing = audio_manager.toggle_play_pause()
            player_bar.set_playing_state(is_playing)
            status = "Playing" if is_playing else "Paused"
            logger.info(f"{status}")
            page.update()
        except Exception as ex:
            logger.error(f"Error toggling play/pause: {ex}")
            show_error_snackbar(f"Error: {str(ex)}")
    
    def on_next() -> None:
        """Handle next button click."""
        try:
            if state['songs']:
                state['current_song_index'] = (state['current_song_index'] + 1) % len(state['songs'])
                song = state['songs'][state['current_song_index']]
                
                player_bar.update_song_info(song['title'], song['artist'])
                player_bar.set_seek_position(0)
                
                if audio_manager.load_and_play(song['file_path']):
                    player_bar.set_playing_state(True)
                    logger.info(f"Skipped to next: {song['title']}")
                else:
                    show_error_snackbar("Failed to play next song")
                
                page.update()
        except Exception as ex:
            logger.error(f"Error skipping to next: {ex}")
            show_error_snackbar(f"Error: {str(ex)}")
    
    def on_prev() -> None:
        """Handle previous button click."""
        try:
            if state['songs']:
                state['current_song_index'] = (state['current_song_index'] - 1) % len(state['songs'])
                song = state['songs'][state['current_song_index']]
                
                player_bar.update_song_info(song['title'], song['artist'])
                player_bar.set_seek_position(0)
                
                if audio_manager.load_and_play(song['file_path']):
                    player_bar.set_playing_state(True)
                    logger.info(f"Skipped to previous: {song['title']}")
                else:
                    show_error_snackbar("Failed to play previous song")
                
                page.update()
        except Exception as ex:
            logger.error(f"Error skipping to previous: {ex}")
            show_error_snackbar(f"Error: {str(ex)}")
    
    def on_seek_change(position_percent: float) -> None:
        """
        Handle seek slider change.
        
        Args:
            position_percent (float): Seek position as percentage (0-100).
        """
        try:
            if state['songs'] and state['current_song_index'] >= 0:
                total_ms = audio_manager.get_duration()
                if total_ms > 0:
                    position_ms = int((position_percent / 100) * total_ms)
                    audio_manager.seek(position_ms)
                    logger.info(f"Seeked to {position_percent:.1f}%")
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
    
    # Create modern header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon("music", size=28, color="#1db954"),
                        ft.Text("Music Player", size=22, weight="w900", color="#ffffff")
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.IconButton(
                        "file_upload",
                        icon_color="#1db954",
                        icon_size=24,
                        tooltip="Upload Audio Files",
                        on_click=lambda e: file_picker.pick_files(
                            allowed_extensions=["mp3", "wav", "ogg", "flac"]
                        )
                    ),
                    padding=8
                ),
                ft.Container(
                    content=ft.IconButton(
                        "folder_open",
                        icon_color="#1db954",
                        icon_size=24,
                        tooltip="Open Folder",
                        on_click=lambda e: file_picker.get_directory_path()
                    ),
                    padding=8
                )
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#1a1a1a",
        padding=12,
        border_radius=0,
        shadow=ft.BoxShadow(blur_radius=8, color="#00000030"),
    )
    
    # Create main layout
    main_column = ft.Column(
        controls=[
            header,
            library_view,
            player_bar
        ],
        spacing=0,
        expand=True
    )
    
    # Add main layout to page
    page.add(main_column)
    
    logger.info("UI built successfully")


if __name__ == "__main__":
    ft.app(target=main)
