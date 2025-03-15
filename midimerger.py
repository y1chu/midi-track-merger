import mido
import tkinter as tk
from tkinter import filedialog, messagebox
import os


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


class MidiMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Track Merger")
        self.root.geometry("400x250")
        self.center_window()

        # Set a default font
        self.default_font = ("Arial", 10)

        # Frame for input file selection
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        self.input_label = tk.Label(input_frame, text="Input MIDI File:", font=self.default_font)
        self.input_label.pack(side=tk.LEFT, padx=(0, 10))

        self.input_entry = tk.Entry(input_frame, width=30, font=self.default_font, justify='right')
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.input_button = tk.Button(input_frame, text="Browse", command=self.browse_input, font=self.default_font)
        self.input_button.pack(side=tk.LEFT, padx=(10, 0))

        # Label to show track count and selected file name (only file name is shown)
        self.track_label = tk.Label(root, text="Tracks: N/A", font=self.default_font)
        self.track_label.pack(pady=(0, 5))

        self.file_label = tk.Label(root, text="Selected File: ", font=self.default_font, anchor='e')
        self.file_label.pack(pady=(0, 10), padx=10, fill=tk.X)

        # Frame for output file selection
        output_frame = tk.Frame(root)
        output_frame.pack(pady=10, padx=10, fill=tk.X)

        self.output_label = tk.Label(output_frame, text="Output MIDI File:", font=self.default_font)
        self.output_label.pack(side=tk.LEFT, padx=(0, 10))

        self.output_entry = tk.Entry(output_frame, width=30, font=self.default_font)
        self.output_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.output_button = tk.Button(output_frame, text="Browse", command=self.browse_output, font=self.default_font)
        self.output_button.pack(side=tk.LEFT, padx=(10, 0))

        # Merge button
        self.merge_button = tk.Button(root, text="Merge Tracks", command=self.merge_tracks_action, font=self.default_font)
        self.merge_button.pack(pady=20)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"400x250+{x}+{y}")

    def browse_input(self):
        file_path = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid")])
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            # Show only the file name in the file label
            self.file_label.config(text=f"Selected File: {os.path.basename(file_path)}")
            try:
                midi = mido.MidiFile(file_path)
                self.track_label.config(text=f"Tracks: {len(midi.tracks)}")
            except Exception as e:
                self.track_label.config(text="Tracks: Error")
                messagebox.showerror("Error", f"Error reading MIDI file: {e}")

    def browse_output(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".mid", filetypes=[("MIDI Files", "*.mid")])
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def merge_tracks_action(self):
        input_file = self.input_entry.get()
        output_file = self.output_entry.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files.")
            return

        try:
            mid = mido.MidiFile(input_file)
            merged_mid = merge_tracks(mid)
            merged_mid.save(output_file)
            messagebox.showinfo("Success", f"Merged MIDI file saved to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MidiMergerApp(root)
    root.mainloop()