# 🎵 Flet Music Player - Project Documentation

## Project Overview

A **modern, beautiful music player application** built with Flet (Python UI framework) and Pygame (audio engine). The app features a sleek dark theme with Spotify-inspired green accents, full audio playback capabilities, and intuitive file upload functionality.

**Status**: ✅ Fully Functional and Running
**Last Updated**: 2026-07-25

---

## 🎯 Core Features

### Audio Playback
- ✅ Full audio playback support using **Pygame 2.6.1** mixer
- ✅ Play/Pause/Next/Previous controls
- ✅ Seek functionality with time-based jumping
- ✅ Real-time position tracking and progress display
- ✅ Support for multiple formats: MP3, WAV, OGG, FLAC

### User Interface
- ✅ Modern dark theme (#0a0a0a) with green accents (#1db954)
- ✅ Beautiful card-based song library
- ✅ Large circular play button (60x60px with shadow effect)
- ✅ Album art display with icon placeholders
- ✅ Time display (current/total duration) with MM:SS formatting
- ✅ Responsive progress slider
- ✅ Professional header with upload buttons
- ✅ Empty state UI guidance

### File Management
- ✅ Individual audio file upload via file picker
- ✅ Folder scanning for batch music import
- ✅ Automatic metadata extraction (title, artist, duration)
- ✅ Error handling with snackbar notifications
- ✅ Support for multiple audio formats

---

## 📁 Project Structure

```
flet-mobile-app/
├── main.py                 # Main application entry point and orchestration
├── claude.md               # This documentation file
├── README.md               # User-facing documentation
│
├── core/                   # Core business logic
│   ├── __init__.py
│   ├── audio_manager.py    # Pygame-based audio engine (256 lines)
│   ├── file_scanner.py     # Metadata extraction and file discovery
│   └── constants.py        # (Optional) Configuration constants
│
├── ui/                     # User interface components
│   ├── __init__.py
│   ├── player_bar.py       # Player controls and display component
│   ├── library_view.py     # Song library grid/list component
│   └── styles.py           # (Optional) Centralized styling
│
├── assets/                 # Static assets (placeholder for images)
│
└── flet_env/               # Virtual environment
    ├── Scripts/
    ├── Lib/
    └── pyvenv.cfg
```

---

## 🔧 Technical Architecture

### Technology Stack
- **Framework**: Flet 0.86.2 (Python UI framework)
- **Audio Engine**: Pygame 2.6.1 (mixer-based playback)
- **Metadata**: TinyTag 2.2.1 (audio file metadata extraction)
- **Python**: 3.10.4
- **OS Support**: Windows, Linux, macOS (via Flet)

### Component Architecture

#### 1. **AudioManager** (`core/audio_manager.py`)
**Responsibility**: Handle all audio playback operations

**Key Methods**:
- `load_and_play(file_path)` - Load and start playing an audio file
- `toggle_play_pause()` - Toggle between play and pause states
- `play()` / `pause()` / `stop()` - Direct playback control
- `seek(position_ms)` - Jump to specific time in track
- `get_duration()` - Get total track duration in milliseconds
- `get_position()` - Get current playback position in milliseconds

**Implementation Details**:
- Uses pygame.mixer for audio playback
- Background thread for position updates (polls every 0.1s)
- Callback-based position change notifications
- Graceful error handling with comprehensive logging

**Audio Formats Supported**:
- MP3 (primary format)
- WAV
- OGG
- FLAC

#### 2. **PlayerBar** (`ui/player_bar.py`)
**Responsibility**: Render player controls and display current song info

**Key Features**:
- Large album art display (100x100px) with icon and shadow
- Song title and artist display (truncated with ellipsis)
- Seek slider with time indicators
- Control buttons (Previous, Play/Pause, Next)
- Time display (MM:SS format)
- Responsive layout that adapts to content

**Key Methods**:
- `update_song_info(title, artist)` - Update displayed metadata
- `set_playing_state(is_playing)` - Update play button state
- `set_seek_position_ms(current_ms, total_ms)` - Update progress display
- `set_seek_position(percent)` - Update seek slider position

**Styling**:
- Background: #0a0a0a (near black)
- Accents: #1db954 (Spotify green)
- Secondary: #1a1a1a (dark gray for cards)
- Text: #ffffff (white), #b0b0b0 (light gray)

#### 3. **LibraryView** (`ui/library_view.py`)
**Responsibility**: Display scrollable list of songs

**Key Features**:
- Card-based song tiles with album art icon
- Song title, artist, and duration display
- Hover effects for visual feedback
- Selection highlighting (green background on click)
- Empty state UI with helpful guidance
- Dynamic list updates

**Key Methods**:
- `_build_listview()` - Construct the scrollable song list
- `_create_song_tile(song, index)` - Create individual song card
- `update_songs(songs)` - Update list dynamically

**Tile Layout**:
```
[Album Art] [Title + Artist] [Duration]
```

#### 4. **FileScanner** (`core/file_scanner.py`)
**Responsibility**: Scan directories and extract audio metadata

**Key Methods**:
- `scan_directory(path)` - Recursively find all music files
- `_extract_metadata(file_path)` - Extract ID3 tags and fallbacks
- `_validate_directory(path)` - Validate and access directories

**Metadata Extraction**:
- Primary: ID3 tags from audio files
- Fallback: Filename if tags missing
- Duration calculation from audio stream

#### 5. **Main App** (`main.py`)
**Responsibility**: Orchestrate components and manage application state

**Key Responsibilities**:
- Page configuration (size, theme, colors)
- Component initialization
- Event handler setup
- State management
- UI layout construction

**State Object Structure**:
```python
state = {
    'songs': [],              # List of song dictionaries
    'current_song_index': -1, # Currently playing song index
    'music_folder': None      # Last selected music folder path
}
```

**Event Flow**:
1. User uploads file(s) → `on_files_selected()`
2. File validated & metadata extracted
3. Song added to state and library view
4. User clicks song → `on_song_click()`
5. Audio loaded via `audio_manager.load_and_play()`
6. Position updates via `on_position_changed()` callback
7. UI updates via `player_bar.set_seek_position_ms()`

---

## 🎨 UI/UX Design

### Color Scheme
- **Primary Background**: #0a0a0a (near-black for main background)
- **Secondary Background**: #1a1a1a (dark gray for cards)
- **Accent Color**: #1db954 (Spotify green for interactive elements)
- **Text Primary**: #ffffff (white for titles)
- **Text Secondary**: #b0b0b0 (light gray for metadata)
- **Hover State**: #242424 (slightly lighter gray)
- **Selected State**: #1db954 (green highlight)

### Layout
- **Window**: 500x950px (mobile-inspired aspect ratio)
- **Header**: Fixed, 12px padding with title and action buttons
- **Library**: Scrollable list with 8px spacing, fills available space
- **Player Bar**: Fixed bottom section with controls

### Component Dimensions
- **Album Art**: 100x100px with 16px border radius
- **Play Button**: 60x60px circular with shadow
- **Song Tile**: Full width with 12px internal padding, 12px border radius
- **Seek Slider**: Full width, active color #1db954

---

## 🚀 How to Run

### Prerequisites
```bash
# Python 3.10+
# Virtual environment: flet_env/
# Packages: flet, pygame, tinytag
```

### Starting the App
```bash
cd c:\Users\santh\Music\flet-mobile-app
flet_env\Scripts\python.exe main.py
```

### Building/Packaging
```bash
# For desktop distribution
flet build windows

# For web deployment
flet publish
```

---

## 📊 Data Structures

### Song Object
```python
song = {
    'file_path': str,      # Absolute path to audio file
    'file_name': str,      # Filename with extension
    'title': str,          # Song title (from ID3 or filename)
    'artist': str,         # Artist name (from ID3 or default)
    'duration': str        # Duration in MM:SS format
}
```

### Application State
```python
state = {
    'songs': List[Dict],   # Array of song objects
    'current_song_index': int,  # Current song index (-1 if none)
    'music_folder': Optional[str]  # Last opened folder
}
```

---

## 🔄 Event Flow Diagram

```
User Action → Event Handler → AudioManager/State Update → UI Update
    ↓                ↓                      ↓                  ↓
Upload File   on_files_selected    songs[] + metadata    library_view refresh
Click Song    on_song_click        load_and_play()       player_bar update
Play/Pause    on_play_pause        toggle_play_pause()   button state change
Next/Prev     on_next/on_prev      load_and_play(next)   metadata update
Seek          on_seek_change       seek(position_ms)     slider + time update
```

---

## 🐛 Error Handling

### Graceful Error Management
- ✅ Invalid file format detection with fallback
- ✅ Missing metadata handling with defaults
- ✅ Audio engine initialization failure with error logging
- ✅ File access permission errors caught and reported
- ✅ User feedback via snackbar notifications

### Logging
All events logged via Python's `logging` module:
```python
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

**Log Levels Used**:
- `INFO`: User actions, state changes, successful operations
- `WARNING`: Missing metadata, unavailable features
- `ERROR`: Failed operations, exceptions

---

## 📝 Code Conventions

### Naming
- **Functions**: `snake_case` (e.g., `load_and_play`)
- **Classes**: `PascalCase` (e.g., `AudioManager`)
- **Constants**: `UPPER_CASE` (e.g., `SUPPORTED_EXTENSIONS`)
- **Private Methods**: Leading underscore `_method_name`

### Documentation
- Module docstring at top of each file
- Class docstring explaining purpose
- Method docstrings with Args/Returns/Raises sections
- Inline comments for complex logic

### Error Handling
- Try/except with specific exception types
- Logging before returning/raising
- User-friendly error messages via snackbars
- Graceful degradation rather than crashes

---

## 🧪 Testing Considerations

### Manual Testing Checklist
- [ ] Upload single MP3 file
- [ ] Upload WAV file
- [ ] Scan folder with multiple formats
- [ ] Play song to completion
- [ ] Pause and resume playback
- [ ] Skip to next track
- [ ] Skip to previous track
- [ ] Use seek slider to jump around
- [ ] Verify time display accuracy
- [ ] Test with file without metadata
- [ ] Close app cleanly

### Known Limitations
- Pygame mixer seek precision limited (may be approximate)
- Large folder scans may pause UI briefly (should add progress indicator)
- No playlist support (loads all files into single list)
- No shuffle/repeat functionality

---

## 🔮 Future Enhancements

### Planned Features
1. **Playlist Management**
   - Create/save/load playlists
   - Reorder songs via drag-and-drop
   - Delete individual songs from library

2. **Enhanced UI**
   - Album art extraction from MP3 ID3 tags
   - Animated play button state change
   - Volume control slider
   - Search/filter functionality

3. **Audio Features**
   - Equalizer support
   - Crossfade between tracks
   - Repeat modes (all/one)
   - Shuffle functionality

4. **Persistence**
   - Save last played song and position
   - Remember music folders
   - Save user preferences
   - Recent files list

5. **Performance**
   - Lazy load large libraries
   - Add progress indicator for folder scanning
   - Cache album art
   - Optimize seek performance

---

## 🔧 Troubleshooting

### App Won't Start
**Issue**: `ModuleNotFoundError: No module named 'pygame'`
**Solution**: 
```bash
flet_env\Scripts\pip.exe install pygame
```

### No Audio Playing
**Issue**: Sound doesn't play
**Solution**:
- Check system volume
- Verify audio file format is supported
- Check file permissions
- Inspect logs for pygame errors

### UI Looks Broken
**Issue**: Elements overlap or disappear
**Solution**:
- Flet has known layout issues on some systems
- Try resizing window
- Restart the app
- Check for newer Flet version

### Slow Folder Scanning
**Issue**: App freezes when scanning large folder
**Solution**:
- Add loading indicator (planned feature)
- Pre-filter files to supported formats only
- Consider threading the scan operation

---

## 📚 Dependencies

### Core Dependencies
```
flet==0.86.2           # UI Framework
pygame==2.6.1          # Audio Engine
tinytag==2.2.1         # Metadata Extraction
python==3.10.4         # Language Runtime
```

### Optional
```
pillow==12.3.0         # Image handling (if adding album art)
watchdog==6.0.0        # File system watching (for auto-refresh)
```

---

## 📄 File Statistics

| File | Lines | Purpose |
|------|-------|---------|
| main.py | ~380 | App orchestration and event handling |
| core/audio_manager.py | ~256 | Pygame audio engine |
| ui/player_bar.py | ~280 | Player controls UI component |
| ui/library_view.py | ~200 | Song library display component |
| core/file_scanner.py | ~150 | File discovery and metadata extraction |

**Total**: ~1,266 lines of code

---

## 🎓 Learning Resources

### Key Concepts Used
1. **Event-Driven Architecture**: UI responds to user actions via callbacks
2. **Component-Based Design**: Reusable UI components with encapsulation
3. **Threading**: Background thread for position updates
4. **State Management**: Central state object for application data
5. **Error Handling**: Graceful degradation and user feedback

### Flet Documentation
- https://flet.dev/docs
- https://github.com/flet-dev/flet

### Pygame Audio
- https://www.pygame.org/docs/ref/mixer.html
- https://www.pygame.org/docs/ref/music.html

---

## 📞 Support & Maintenance

### Common Issues & Solutions

**Issue**: High CPU usage
- **Cause**: Position update thread polling too frequently
- **Solution**: Increase sleep interval in `_update_position_loop()` (currently 0.1s)

**Issue**: Memory leaks with many files
- **Cause**: Song objects not being garbage collected
- **Solution**: Implement proper cleanup in destructor

**Issue**: Seek doesn't work precisely
- **Cause**: Pygame mixer limitations
- **Solution**: Use alternative audio library (pydub/librosa) for better seek support

---

## 📋 Version History

### v1.0.0 (2026-07-25) - CURRENT
- ✅ Initial release with full audio playback
- ✅ Beautiful modern UI with Spotify-inspired design
- ✅ File upload and folder scanning
- ✅ Complete play controls (play/pause/next/prev)
- ✅ Seek functionality
- ✅ Metadata extraction
- ✅ Error handling with user notifications

---

**Last Updated**: July 25, 2026
**Status**: Production Ready ✅
**Maintainer**: Music Player Development Team
