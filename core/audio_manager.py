"""
Audio Manager Module for Music Player Application

This module provides audio playback functionality using Flet's ft.Audio control.
Handles loading, playing, pausing, seeking, and state management of audio files.

Note: Since ft.Audio may not be available in all Flet versions, this module
provides a stub implementation that prevents crashes.
"""

import logging
from typing import Callable, Optional
import flet as ft

# Configure logging
logger = logging.getLogger(__name__)


class AudioManager:
    """
    Manages audio playback for the music player.
    
    This is a stub implementation that provides the interface for audio management
    without requiring ft.Audio (which may not be available in all Flet versions).
    """
    
    def __init__(
        self,
        page: ft.Page,
        on_position_changed: Callable[[int], None]
    ):
        """
        Initialize the AudioManager.
        
        Args:
            page (ft.Page): The Flet page object to attach the audio control to.
            on_position_changed (Callable): Callback function triggered when playback position changes.
                Receives the position in milliseconds as an argument.
        
        Raises:
            ValueError: If page is None or invalid.
        """
        if page is None:
            raise ValueError("page cannot be None")
        
        self.page = page
        self.on_position_changed = on_position_changed
        self.current_file = None
        self.is_playing = False
        
        # Try to initialize ft.Audio if available, otherwise use stub
        self.audio_control = None
        try:
            self.audio_control = ft.Audio(
                autoplay=False,
                volume=1.0,
                playback_rate=1.0,
                on_position_changed=self._handle_position_changed,
                on_state_changed=self._handle_state_changed
            )
            # Add audio control to page overlay (hidden from UI, manages audio)
            self.page.overlay.append(self.audio_control)
            logger.info("AudioManager initialized with ft.Audio support")
        except AttributeError:
            logger.warning("ft.Audio not available in this Flet version - using stub mode")
            logger.info("AudioManager initialized in stub mode (audio playback disabled)")
    
    def load_and_play(self, file_path: str) -> bool:
        """
        Load an audio file and automatically start playback.
        
        Args:
            file_path (str): The absolute path to the audio file to load and play.
        
        Returns:
            bool: True if file was loaded and playback started successfully, False otherwise.
        """
        try:
            if self.audio_control is None:
                logger.warning(f"Audio not available - simulating playback for: {file_path}")
                self.current_file = file_path
                self.is_playing = True
                logger.info(f"Loaded and started playback (simulated): {file_path}")
                return True
            
            # Set the audio source
            self.audio_control.src = file_path
            self.current_file = file_path
            self.page.update()
            
            # Start playback
            self.audio_control.play()
            self.is_playing = True
            
            logger.info(f"Loaded and started playback: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load and play audio file {file_path}: {e}")
            self.is_playing = False
            return False
    
    def toggle_play_pause(self) -> bool:
        """
        Toggle between play and pause states.
        
        If the audio is currently playing, it will be paused. If it's paused,
        playback will resume. If no file is loaded, this method does nothing.
        
        Returns:
            bool: True if currently playing after toggle, False if paused.
        """
        if self.current_file is None:
            logger.warning("No audio file loaded for play/pause toggle")
            return False
        
        try:
            if self.audio_control is None:
                # Stub mode - just toggle the flag
                self.is_playing = not self.is_playing
                logger.info(f"Play/Pause (simulated): {self.current_file}")
                return self.is_playing
            
            if self.is_playing:
                # Currently playing, so pause
                self.audio_control.pause()
                self.is_playing = False
                logger.info(f"Paused: {self.current_file}")
            else:
                # Currently paused, so resume
                self.audio_control.resume()
                self.is_playing = True
                logger.info(f"Resumed: {self.current_file}")
            
            self.page.update()
            return self.is_playing
            
        except Exception as e:
            logger.error(f"Error toggling play/pause: {e}")
            return self.is_playing
    
    def play(self) -> None:
        """
        Start playback of the currently loaded audio file.
        
        If already playing, this method does nothing. If no file is loaded,
        no action is taken.
        """
        if self.current_file is None:
            logger.warning("No audio file loaded for playback")
            return
        
        if self.is_playing:
            logger.debug("Audio already playing, ignoring play request")
            return
        
        try:
            if self.audio_control is None:
                self.is_playing = True
                logger.info(f"Started playback (simulated): {self.current_file}")
                return
            
            self.audio_control.play()
            self.is_playing = True
            logger.info(f"Started playback: {self.current_file}")
            self.page.update()
        except Exception as e:
            logger.error(f"Error starting playback: {e}")
    
    def pause(self) -> None:
        """
        Pause the currently playing audio.
        
        If not playing, this method does nothing.
        """
        if not self.is_playing:
            logger.debug("Audio not playing, ignoring pause request")
            return
        
        try:
            if self.audio_control is None:
                self.is_playing = False
                logger.info(f"Paused (simulated): {self.current_file}")
                return
            
            self.audio_control.pause()
            self.is_playing = False
            logger.info(f"Paused: {self.current_file}")
            self.page.update()
        except Exception as e:
            logger.error(f"Error pausing audio: {e}")
    
    def stop(self) -> None:
        """
        Stop playback and release the current audio file.
        """
        try:
            if self.audio_control is None:
                self.is_playing = False
                self.current_file = None
                logger.info("Audio stopped and released (simulated)")
                return
            
            if self.is_playing:
                self.audio_control.pause()
                self.is_playing = False
            
            self.audio_control.src = None
            self.current_file = None
            logger.info("Audio stopped and released")
            self.page.update()
        except Exception as e:
            logger.error(f"Error stopping audio: {e}")
    
    def seek(self, position_milliseconds: int) -> None:
        """
        Seek to a specific position in the audio file.
        
        Args:
            position_milliseconds (int): The position to seek to, in milliseconds.
        
        Raises:
            ValueError: If position_milliseconds is negative.
        """
        if position_milliseconds < 0:
            raise ValueError("Position cannot be negative")
        
        if self.current_file is None:
            logger.warning("No audio file loaded, cannot seek")
            return
        
        try:
            if self.audio_control is None:
                logger.debug(f"Seek (simulated) to {position_milliseconds}ms")
                return
            
            self.audio_control.seek(position_milliseconds)
            logger.debug(f"Seeked to {position_milliseconds}ms in {self.current_file}")
            self.page.update()
        except Exception as e:
            logger.error(f"Error seeking to position {position_milliseconds}ms: {e}")
    
    def set_volume(self, volume: float) -> None:
        """
        Set the playback volume.
        
        Args:
            volume (float): Volume level from 0.0 (mute) to 1.0 (maximum).
        
        Raises:
            ValueError: If volume is not between 0.0 and 1.0.
        """
        if not (0.0 <= volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")
        
        try:
            if self.audio_control is None:
                logger.debug(f"Volume set (simulated) to {volume}")
                return
            
            self.audio_control.volume = volume
            logger.debug(f"Volume set to {volume}")
            self.page.update()
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
    
    def get_current_position(self) -> int:
        """
        Get the current playback position.
        
        Returns:
            int: The current position in milliseconds, or 0 if no file is loaded.
        """
        if self.current_file is None:
            return 0
        
        try:
            if self.audio_control is None:
                return 0
            
            # Note: In some Flet versions, this might be in a different format
            # Adjust based on actual Flet behavior
            position = getattr(self.audio_control, 'current_position', 0)
            return int(position) if position else 0
        except Exception as e:
            logger.error(f"Error getting current position: {e}")
            return 0
    
    def _handle_position_changed(self, e: ft.ControlEvent) -> None:
        """
        Internal handler for position changed events from the audio control.
        
        Args:
            e (ft.ControlEvent): The control event containing position data.
        """
        try:
            position = int(e.data) if e.data else 0
            logger.debug(f"Position changed to {position}ms")
            self.on_position_changed(position)
        except Exception as ex:
            logger.error(f"Error in position changed handler: {ex}")
    
    def _handle_state_changed(self, e: ft.ControlEvent) -> None:
        """
        Internal handler for state changed events from the audio control.
        
        Handles state transitions such as when a song finishes playing.
        
        Args:
            e (ft.ControlEvent): The control event containing state data.
        """
        try:
            state = str(e.data).lower() if e.data else ""
            logger.info(f"Audio state changed to: {state}")
            
            # Handle state transitions
            if state == "completed":
                self.is_playing = False
                logger.info(f"Playback completed: {self.current_file}")
                # The main app should handle auto-play next track
            elif state == "playing":
                self.is_playing = True
                logger.debug("Playback started")
            elif state == "paused":
                self.is_playing = False
                logger.debug("Playback paused")
            
        except Exception as ex:
            logger.error(f"Error in state changed handler: {ex}")
    
    def cleanup(self) -> None:
        """
        Clean up audio resources and remove the audio control from the page overlay.
        
        Should be called when shutting down the application or destroying the AudioManager.
        """
        try:
            self.stop()
            if self.audio_control and self.audio_control in self.page.overlay:
                self.page.overlay.remove(self.audio_control)
            logger.info("AudioManager cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def load_and_play(self, file_path: str) -> bool:
        """
        Load an audio file and automatically start playback.
        
        Args:
            file_path (str): The absolute path to the audio file to load and play.
        
        Returns:
            bool: True if file was loaded and playback started successfully, False otherwise.
        
        Raises:
            FileNotFoundError: If the file path does not exist.
        """
        try:
            # Set the audio source
            self.audio_control.src = file_path
            self.current_file = file_path
            self.page.update()
            
            # Start playback
            self.audio_control.play()
            self.is_playing = True
            
            logger.info(f"Loaded and started playback: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load and play audio file {file_path}: {e}")
            self.is_playing = False
            return False
    
    def toggle_play_pause(self) -> bool:
        """
        Toggle between play and pause states.
        
        If the audio is currently playing, it will be paused. If it's paused,
        playback will resume. If no file is loaded, this method does nothing.
        
        Returns:
            bool: True if currently playing after toggle, False if paused.
        """
        if self.current_file is None:
            logger.warning("No audio file loaded for play/pause toggle")
            return False
        
        try:
            if self.is_playing:
                # Currently playing, so pause
                self.audio_control.pause()
                self.is_playing = False
                logger.info(f"Paused: {self.current_file}")
            else:
                # Currently paused, so resume
                self.audio_control.resume()
                self.is_playing = True
                logger.info(f"Resumed: {self.current_file}")
            
            self.page.update()
            return self.is_playing
            
        except Exception as e:
            logger.error(f"Error toggling play/pause: {e}")
            return self.is_playing
    
    def play(self) -> None:
        """
        Start playback of the currently loaded audio file.
        
        If already playing, this method does nothing. If no file is loaded,
        no action is taken.
        """
        if self.current_file is None:
            logger.warning("No audio file loaded for playback")
            return
        
        if self.is_playing:
            logger.debug("Audio already playing, ignoring play request")
            return
        
        try:
            self.audio_control.play()
            self.is_playing = True
            logger.info(f"Started playback: {self.current_file}")
            self.page.update()
        except Exception as e:
            logger.error(f"Error starting playback: {e}")
    
    def pause(self) -> None:
        """
        Pause the currently playing audio.
        
        If not playing, this method does nothing.
        """
        if not self.is_playing:
            logger.debug("Audio not playing, ignoring pause request")
            return
        
        try:
            self.audio_control.pause()
            self.is_playing = False
            logger.info(f"Paused: {self.current_file}")
            self.page.update()
        except Exception as e:
            logger.error(f"Error pausing audio: {e}")
    
    def stop(self) -> None:
        """
        Stop playback and release the current audio file.
        """
        try:
            if self.is_playing:
                self.audio_control.pause()
                self.is_playing = False
            
            self.audio_control.src = None
            self.current_file = None
            logger.info("Audio stopped and released")
            self.page.update()
        except Exception as e:
            logger.error(f"Error stopping audio: {e}")
    
    def seek(self, position_milliseconds: int) -> None:
        """
        Seek to a specific position in the audio file.
        
        Args:
            position_milliseconds (int): The position to seek to, in milliseconds.
        
        Raises:
            ValueError: If position_milliseconds is negative.
        """
        if position_milliseconds < 0:
            raise ValueError("Position cannot be negative")
        
        if self.current_file is None:
            logger.warning("No audio file loaded, cannot seek")
            return
        
        try:
            self.audio_control.seek(position_milliseconds)
            logger.debug(f"Seeked to {position_milliseconds}ms in {self.current_file}")
            self.page.update()
        except Exception as e:
            logger.error(f"Error seeking to position {position_milliseconds}ms: {e}")
    
    def set_volume(self, volume: float) -> None:
        """
        Set the playback volume.
        
        Args:
            volume (float): Volume level from 0.0 (mute) to 1.0 (maximum).
        
        Raises:
            ValueError: If volume is not between 0.0 and 1.0.
        """
        if not (0.0 <= volume <= 1.0):
            raise ValueError("Volume must be between 0.0 and 1.0")
        
        try:
            self.audio_control.volume = volume
            logger.debug(f"Volume set to {volume}")
            self.page.update()
        except Exception as e:
            logger.error(f"Error setting volume: {e}")
    
    def get_current_position(self) -> int:
        """
        Get the current playback position.
        
        Returns:
            int: The current position in milliseconds, or 0 if no file is loaded.
        """
        if self.current_file is None:
            return 0
        
        try:
            # Note: In some Flet versions, this might be in a different format
            # Adjust based on actual Flet behavior
            position = getattr(self.audio_control, 'current_position', 0)
            return int(position) if position else 0
        except Exception as e:
            logger.error(f"Error getting current position: {e}")
            return 0
    
    def _handle_position_changed(self, e: ft.ControlEvent) -> None:
        """
        Internal handler for position changed events from the audio control.
        
        Args:
            e (ft.ControlEvent): The control event containing position data.
        """
        try:
            position = int(e.data) if e.data else 0
            logger.debug(f"Position changed to {position}ms")
            self.on_position_changed(position)
        except Exception as ex:
            logger.error(f"Error in position changed handler: {ex}")
    
    def _handle_state_changed(self, e: ft.ControlEvent) -> None:
        """
        Internal handler for state changed events from the audio control.
        
        Handles state transitions such as when a song finishes playing.
        
        Args:
            e (ft.ControlEvent): The control event containing state data.
        """
        try:
            state = str(e.data).lower() if e.data else ""
            logger.info(f"Audio state changed to: {state}")
            
            # Handle state transitions
            if state == "completed":
                self.is_playing = False
                logger.info(f"Playback completed: {self.current_file}")
                # The main app should handle auto-play next track
            elif state == "playing":
                self.is_playing = True
                logger.debug("Playback started")
            elif state == "paused":
                self.is_playing = False
                logger.debug("Playback paused")
            
        except Exception as ex:
            logger.error(f"Error in state changed handler: {ex}")
    
    def cleanup(self) -> None:
        """
        Clean up audio resources and remove the audio control from the page overlay.
        
        Should be called when shutting down the application or destroying the AudioManager.
        """
        try:
            self.stop()
            if self.audio_control in self.page.overlay:
                self.page.overlay.remove(self.audio_control)
            logger.info("AudioManager cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
