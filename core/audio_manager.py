"""
Audio Manager Module for Music Player Application

This module provides audio playback functionality using pygame mixer.
Handles loading, playing, pausing, seeking, and state management of audio files.
"""

import logging
from typing import Callable, Optional
import pygame
import threading
import time

# Configure logging
logger = logging.getLogger(__name__)


class AudioManager:
    """
    Manages audio playback for the music player using pygame mixer.
    
    This implementation uses pygame's mixer module for robust audio playback support.
    """
    
    def __init__(
        self,
        page,
        on_position_changed: Callable[[int], None]
    ):
        """
        Initialize the AudioManager.

        Args:
            page: The Flet page object (not used but kept for compatibility).
            on_position_changed (Callable): Callback function triggered when playback position changes.
                Receives the position in milliseconds as an argument.
        
        Raises:
            ValueError: If initialization fails.
        """
        self.on_position_changed = on_position_changed
        self.current_file = None
        self.is_playing = False
        self.current_position_ms = 0
        self.total_duration_ms = 0
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            logger.info("AudioManager initialized with pygame mixer")
        except Exception as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")
            raise ValueError(f"Failed to initialize audio system: {e}")
        
        # Track position update thread
        self.position_thread = None
        self.should_update_position = False
    
    def _start_position_update_thread(self) -> None:
        """Start background thread to update playback position."""
        if self.position_thread is not None:
            return
        
        self.should_update_position = True
        self.position_thread = threading.Thread(target=self._update_position_loop, daemon=True)
        self.position_thread.start()
    
    def _stop_position_update_thread(self) -> None:
        """Stop the position update thread."""
        self.should_update_position = False
        if self.position_thread is not None:
            self.position_thread.join(timeout=1)
            self.position_thread = None
    
    def _update_position_loop(self) -> None:
        """Background thread that updates playback position."""
        while self.should_update_position and self.is_playing:
            try:
                if pygame.mixer.music.get_busy():
                    # Get position in milliseconds
                    position_ms = int(pygame.mixer.music.get_pos())
                    if position_ms >= 0:
                        self.current_position_ms = position_ms
                        self.on_position_changed(position_ms)
                else:
                    # Music finished
                    if self.is_playing:
                        self.is_playing = False
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error updating position: {e}")
                break
    
    def load_and_play(self, file_path: str) -> bool:
        """
        Load an audio file and automatically start playback.
        
        Args:
            file_path (str): The absolute path to the audio file to load and play.
        
        Returns:
            bool: True if file was loaded and playback started successfully, False otherwise.
        """
        try:
            # Stop any existing playback
            if self.is_playing:
                pygame.mixer.music.stop()
                self._stop_position_update_thread()
            
            # Load the new file
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            self.current_position_ms = 0
            
            # Extract duration using pygame
            try:
                sound = pygame.mixer.Sound(file_path)
                self.total_duration_ms = int(sound.get_length() * 1000)
            except:
                self.total_duration_ms = 0
            
            # Start playback
            pygame.mixer.music.play()
            self.is_playing = True
            self._start_position_update_thread()
            
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
                pygame.mixer.music.pause()
                self.is_playing = False
                self._stop_position_update_thread()
                logger.info(f"Paused: {self.current_file}")
            else:
                # Currently paused, so resume
                pygame.mixer.music.unpause()
                self.is_playing = True
                self._start_position_update_thread()
                logger.info(f"Resumed: {self.current_file}")
            
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
            pygame.mixer.music.play()
            self.is_playing = True
            self._start_position_update_thread()
            logger.info(f"Started playback: {self.current_file}")
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
            pygame.mixer.music.pause()
            self.is_playing = False
            self._stop_position_update_thread()
            logger.info(f"Paused: {self.current_file}")
        except Exception as e:
            logger.error(f"Error pausing audio: {e}")
    
    def stop(self) -> None:
        """
        Stop playback and release the current audio file.
        """
        try:
            if self.is_playing:
                pygame.mixer.music.stop()
                self.is_playing = False
                self._stop_position_update_thread()
            self.current_file = None
            self.current_position_ms = 0
            logger.info("Stopped playback")
        except Exception as e:
            logger.error(f"Error stopping audio: {e}")
    
    def seek(self, position_ms: int) -> None:
        """
        Seek to a specific position in the audio file.
        
        Args:
            position_ms (int): Position in milliseconds.
        """
        try:
            if self.current_file is None:
                logger.warning("No audio file loaded for seeking")
                return
            
            # Pygame mixer's set_pos is limited
            position_seconds = position_ms / 1000.0
            pygame.mixer.music.set_pos(position_seconds)
            self.current_position_ms = position_ms
            logger.info(f"Seeked to {position_ms}ms")
        except Exception as e:
            logger.error(f"Error seeking: {e}")
    
    def get_duration(self) -> int:
        """
        Get the total duration of the current audio file in milliseconds.
        
        Returns:
            int: Duration in milliseconds, or 0 if no file is loaded.
        """
        return self.total_duration_ms
    
    def get_position(self) -> int:
        """
        Get the current playback position in milliseconds.
        
        Returns:
            int: Current position in milliseconds.
        """
        return self.current_position_ms
