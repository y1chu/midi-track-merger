import argparse
import mido


def merge_tracks(mid):
    new_track = mido.MidiTrack()
    events = []

    # Gather events with absolute timing from all tracks
    for track in mid.tracks:
        absolute_time = 0
        for msg in track:
            absolute_time += msg.time
            events.append((absolute_time, msg))
    
    # Sort events by absolute time
    events.sort(key=lambda x: x[0])
    
    # Recalculate delta times and add events to the new track
    last_time = 0
    for time, msg in events:
        msg.time = time - last_time
        new_track.append(msg)
        last_time = time
    
    # Replace all tracks with the single merged track
    mid.tracks = [new_track]
    return mid


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple MIDI tracks into a single track."
    )
    parser.add_argument("input", help="Path to the input MIDI file")
    parser.add_argument("output", help="Path to save the merged MIDI file")
    args = parser.parse_args()

    try:
        mid = mido.MidiFile(args.input)
    except Exception as e:
        print(f"Error loading MIDI file: {e}")
        return

    merged_mid = merge_tracks(mid)
    try:
        merged_mid.save(args.output)
        print(f"Merged MIDI file saved to {args.output}")
    except Exception as e:
        print(f"Error saving merged MIDI file: {e}")


if __name__ == "__main__":
    main()
