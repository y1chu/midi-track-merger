# MIDI Track Merger

MIDI Track Merger merges multiple tracks of a MIDI file into a single track. This tool is useful for simplifying MIDI files for playback, editing, or further processing.

## Features

- **Merge Tracks:** Combines all tracks in a MIDI file into one, preserving correct timing.
- **Track Count Display:** Automatically displays the number of tracks in the selected input file.

## Requirements

- Python 3.13.x
- [mido](https://github.com/mido/mido) library for MIDI processing

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/y1chu/midi-track-merger.git
   cd midi-track-merger
   ```

2. **Dependencies:**

   ```bash
   pip install mido
   ```

3. **Run the Application:**

   ```bash
   python midimerger.py
   ```