"""
File Scanner Module for Music Player Application

This module provides functionality to scan directories for music files
and extract metadata from audio files.
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional
from tinytag import TinyTag, TinyTagException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MusicScanner:
    """
    A robust scanner for discovering and extracting metadata from music files.
    
    This class provides functionality to recursively scan directories for MP3 files
    and extract their metadata using the TinyTag library with fallback mechanisms
    for missing or corrupted tags.
    """
    
    # Supported audio file extensions
    SUPPORTED_EXTENSIONS = {'.mp3'}
    
    def __init__(self):
        """Initialize the MusicScanner instance."""
        logger.info("MusicScanner initialized")
    
    def scan_directory(self, directory_path: str) -> List[Dict[str, str]]:
        """
        Scan a directory for music files and extract metadata.
        
        This method recursively searches the given directory for MP3 files
        and extracts their metadata using TinyTag with fallback mechanisms
        for missing or corrupted tags.
        
        Args:
            directory_path (str): The path to the directory to scan.
        
        Returns:
            List[Dict[str, str]]: A list of dictionaries containing music file metadata.
                Each dictionary contains:
                - file_path (str): Absolute path to the audio file
                - file_name (str): Name of the file without extension
                - title (str): Title of the song (from metadata or filename)
                - artist (str): Artist name (from metadata or "Unknown Artist")
                - duration (str): Duration in MM:SS format
        
        Raises:
            ValueError: If the directory path is invalid or inaccessible.
        """
        music_files = []
        
        # Validate directory path
        dir_path = self._validate_directory(directory_path)
        if dir_path is None:
            return music_files
        
        logger.info(f"Starting scan of directory: {directory_path}")
        
        try:
            # Recursively find all MP3 files in the directory
            mp3_files = list(dir_path.rglob('*.mp3'))
            logger.info(f"Found {len(mp3_files)} MP3 file(s)")
            
            for file_path in mp3_files:
                try:
                    music_data = self._extract_metadata(file_path)
                    if music_data:
                        music_files.append(music_data)
                except Exception as e:
                    logger.warning(f"Error processing file {file_path}: {e}")
                    continue
            
            logger.info(f"Successfully scanned {len(music_files)} file(s)")
            return music_files
            
        except PermissionError as e:
            logger.error(f"Permission denied when scanning directory: {e}")
            raise ValueError(f"Permission denied: Cannot access {directory_path}")
        except Exception as e:
            logger.error(f"Unexpected error during directory scan: {e}")
            raise ValueError(f"Error scanning directory: {str(e)}")
    
    def _validate_directory(self, directory_path: str) -> Optional[Path]:
        """
        Validate that the given directory path exists and is accessible.
        
        Args:
            directory_path (str): The path to validate.
        
        Returns:
            Optional[Path]: A Path object if valid, None otherwise.
        """
        try:
            path = Path(directory_path).resolve()
            
            if not path.exists():
                logger.error(f"Directory does not exist: {directory_path}")
                return None
            
            if not path.is_dir():
                logger.error(f"Path is not a directory: {directory_path}")
                return None
            
            # Check if directory is readable
            if not path.resolve().exists():
                logger.error(f"Directory path is not accessible: {directory_path}")
                return None
            
            return path
            
        except (OSError, ValueError) as e:
            logger.error(f"Invalid directory path: {directory_path} - {e}")
            return None
    
    def _extract_metadata(self, file_path: Path) -> Optional[Dict[str, str]]:
        """
        Extract metadata from a single audio file.
        
        Attempts to extract metadata using TinyTag. If metadata is missing or
        extraction fails, uses fallback values (filename for title,
        "Unknown Artist" for artist).
        
        Args:
            file_path (Path): Path object of the audio file.
        
        Returns:
            Optional[Dict[str, str]]: Dictionary containing file metadata, or None if processing fails.
        """
        try:
            # Extract metadata using TinyTag
            tag = TinyTag.get(str(file_path), tags=True, duration=True)
            
            # Extract values with fallbacks
            title = self._get_safe_title(tag, file_path)
            artist = self._get_safe_artist(tag)
            duration = self._format_duration(tag.duration)
            
            return {
                'file_path': str(file_path.resolve()),
                'file_name': file_path.stem,
                'title': title,
                'artist': artist,
                'duration': duration
            }
            
        except TinyTagException as e:
            logger.warning(f"TinyTag error for {file_path}: {e}")
            # Fallback: use filename as title
            return {
                'file_path': str(file_path.resolve()),
                'file_name': file_path.stem,
                'title': file_path.stem,
                'artist': 'Unknown Artist',
                'duration': '00:00'
            }
        except Exception as e:
            logger.error(f"Unexpected error extracting metadata from {file_path}: {e}")
            return None
    
    def _get_safe_title(self, tag: TinyTag, file_path: Path) -> str:
        """
        Safely extract title from metadata with fallback to filename.
        
        Args:
            tag (TinyTag): TinyTag object containing metadata.
            file_path (Path): Path object of the audio file (for fallback).
        
        Returns:
            str: The title string or filename if not available.
        """
        if tag.title and tag.title.strip():
            return tag.title.strip()
        logger.debug(f"No title found for {file_path}, using filename")
        return file_path.stem
    
    def _get_safe_artist(self, tag: TinyTag) -> str:
        """
        Safely extract artist from metadata with fallback.
        
        Args:
            tag (TinyTag): TinyTag object containing metadata.
        
        Returns:
            str: The artist name or "Unknown Artist" if not available.
        """
        if tag.artist and tag.artist.strip():
            return tag.artist.strip()
        logger.debug("No artist found in metadata")
        return 'Unknown Artist'
    
    def _format_duration(self, duration: Optional[float]) -> str:
        """
        Format duration from seconds to MM:SS format.
        
        Args:
            duration (Optional[float]): Duration in seconds, or None.
        
        Returns:
            str: Formatted duration string in MM:SS format.
        """
        if duration is None:
            return '00:00'
        
        try:
            total_seconds = int(duration)
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes:02d}:{seconds:02d}"
        except (ValueError, TypeError):
            logger.warning(f"Invalid duration value: {duration}")
            return '00:00'
