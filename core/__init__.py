"""
Core Components Package

This package contains core functionality for the music player.
"""

from .file_scanner import MusicScanner
from .audio_manager import AudioManager

__all__ = ['MusicScanner', 'AudioManager']
