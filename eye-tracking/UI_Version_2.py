import tkinter as tk
import time
import threading
from typing import List, Dict, Tuple, Any
import pygame
from gtts import gTTS
import os
import math
import re
import socket

### ---------- RegionReceiver ----------
class RegionReceiver:
    def __init__(self, callback=None):
        self.HOST = '0.0.0.0'
        self.PORT = 5051
        self.callback = callback

    def start(self):
        threading.Thread(target=self._server_thread, daemon=True).start()

    def _server_thread(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            print(f"[INFO] Listening on {self.HOST}:{self.PORT}")
            while True:
                conn, addr = s.accept()
                print(f"[INFO] Connection from {addr}")
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        with conn:
            buffer = ''
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print("[INFO] Client disconnected")
                        break
                    buffer += data.decode()
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        msg = line.strip()
                        print(f"[INFO] Received region: {msg}")
                        if self.callback:
                            self.callback(msg)
                except Exception as e:
                    print(f"[ERROR] Error while receiving: {e}")
                    break


### ---------- AAC_GUI ----------

class AAC_GUI():
    """
    This is the main OOP program for creating the interactive GUI.
    Revised version with 20-sector input system and state-dependent mapping.
    Commands:
    - 1-20: Ring sectors (mapping depends on current state)
    - 21: Top-left corner (NUM mode)
    - 22: Top-right corner (RETURN)
    - 23: Bottom-left corner (DELETE)
    - 24: Bottom-right corner (CONFIRM)
    - 25: Center circle (space/decimal point)
    """

    RIGHT: list[str] = ['a', 'e', 'i', 'o', 'u']
    TOP: list[str] = ["s", "t", "n", "r", "d", "l", "h"]
    LEFT: list[str] = ["c", "w", "m", "g", "y", "p", "f"]
    BOTTOM: list[str] = ["j", "b", "q", "k", "v", "z", "x"]

    # Configuration for selection mechanism
    SELECTION_THRESHOLD = 4  # Number of identical commands needed to confirm selection
    MAX_DISPLAY_CHARS = 7  # Maximum characters to display in center circle

    # Base color #3388ff with different opacity levels
    COLORS: Dict[str, str] = {
        "background": "#f8fafc",  # Very light blue-gray
        "border": "#3b82f6",  # Modern blue
        "text": "#1e293b",  # Dark blue-gray
        "ring": "#e2e8f0",  # Light gray
        "confirm": "#10b981",  # Green for confirm
        "cancel": "#ef4444",  # Red for cancel
        "side": "#f1f5f9"  # Very light blue
    }

    # Fallback colors for systems that don't support alpha channels in hex
    FALLBACK_COLORS: Dict[str, str] = {
        "highlight_0": "#e2e8f0",  # Light gray
        "highlight_1": "#dbeafe",  # Very light blue
        "highlight_2": "#bfdbfe",  # Light blue
        "highlight_3": "#93c5fd",  # Medium blue
        "highlight_4": "#3b82f6",  # Full blue
    }

    FONT: Dict[str, int] = {
        'small': ("Monaco", 10),
        'middle': ("Monaco", 12),
        'large': ("Monaco", 16)
    }

    STATES: list[str] = ['MAIN', 'RIGHT', 'TOP', 'LEFT', 'BOTTOM', 'NUM']

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.state = 'MAIN'  # Current panel shown on the screen
        self.current_text = ''
        self.volume = 100  # from 0 to 100

        # NEW: Sector-to-function mapping based on current state
        self.sector_mappings = {
            # MAIN Interface - sectors map to main sections
            "MAIN": {
                "TOP": [3, 4, 5, 6, 7],  # h l d r n t s
                "LEFT": [8, 9, 10, 11, 12, 13],  # c w m g y p f
                "BOTTOM": [14, 15, 16, 17, 18],  # j b q k v z x
                "RIGHT": [19, 20, 1, 2]  # u o i e a
            },
            # Individual vowel states
            "a": {0: [1, 2, 3, 4]},
            "e": {0: [5, 6, 7, 8]},
            "i": {0: [9, 10, 11, 12]},
            "o": {0: [13, 14, 15, 16]},
            "u": {0: [17, 18, 19, 20]},
            # Individual consonant states (TOP section)
            "s": {0: [1, 2, 3]},
            "t": {0: [4, 5, 6]},
            "n": {0: [7, 8, 9]},
            "r": {0: [10, 11]},
            "d": {0: [12, 13, 14, 15]},
            "l": {0: [16, 17]},
            "h": {0: [18, 19, 20]},
            # NUM Interface
            "NUM": {
                "1": [1],
                "2": [2, 3, 4],
                "3": [5, 6],
                "4": [7, 8],
                "5": [9, 10],
                "6": [11, 12],
                "7": [13, 14],
                "8": [15, 16],
                "9": [17, 18, 19],
                "0": [20]
            }
        }

        # NEW: Unified counter system for sectors and buttons
        self.counters = {
            # Main section counters (for MAIN state)
            "TOP": 0,
            "RIGHT": 0,
            "BOTTOM": 0,
            "LEFT": 0,
            # Corner button counters
            "NUM": 0,  # Command 21
            "RETURN": 0,  # Command 22
            "DELETE": 0,  # Command 23
            "CONFIRM": 0,  # Command 24
            "CENTER": 0,  # Command 25
            # Secondary selection counters (for character selection in secondary panels)
            "SECONDARY": {}  # Will be populated dynamically
        }

        # Initialize secondary counters for each character
        for section, chars in {"RIGHT": self.RIGHT, "TOP": self.TOP, "LEFT": self.LEFT, "BOTTOM": self.BOTTOM}.items():
            for i, char in enumerate(chars):
                self.counters["SECONDARY"][f"{section}_{i}"] = 0

        # For NUM state counters
        for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            self.counters["SECONDARY"][f"NUM_{num}"] = 0

        # Test for alpha channel support in tkinter
        try:
            self.root.winfo_rgb("#3388ff33")
            self.supports_alpha = True
        except:
            self.supports_alpha = False
            print("Warning: System doesn't support alpha channels in colors. Using fallback colors.")

        self.root.title("AAC Keyboard - 20 Sector System")
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg=self.COLORS["background"])
        self.canvas.pack()

        self.letters = {
            "RIGHT": self.RIGHT,
            "TOP": self.TOP,
            "LEFT": self.LEFT,
            "BOTTOM": self.BOTTOM
        }

        # Numbers without decimal point (moved to center)
        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.character_positions = {}
        self.section_ids = {}  # Store canvas IDs for main sections
        self.secondary_section_ids = {}  # Store canvas IDs for secondary sections
        self.corner_button_ids = {}  # Store canvas IDs for corner buttons
        self.center_circle_id = None  # Store canvas ID for center circle

        self.compute_character_positions()
        self.setup_UI()

        self.region_receiver = RegionReceiver(callback=self.process_command)
        self.region_receiver.start()

        # Start command input thread
        # self.command_thread = threading.Thread(target=self.command_listener, daemon=True)
        # self.command_thread.start()

    def show_calibration_point(self, position: str) -> None:
        """
        Show a yellow light point at the specified calibration position for 3 seconds
        position: "center", "top_mid", "left_mid", "bottom_mid", "right_mid"
        """
        # Define positions (these match the calibration positions)
        positions = {
            "center": (250, 250),  # Center of the 500x500 canvas
            "top_mid": (250, 100),  # Top middle
            "left_mid": (100, 250),  # Left middle
            "bottom_mid": (250, 400),  # Bottom middle
            "right_mid": (400, 250)  # Right middle
        }

        if position not in positions:
            print(f"[WARNING] Unknown calibration position: {position}")
            return

        x, y = positions[position]

        # Create yellow circle (light point)
        point_radius = 15  # Adjust size as needed
        point_id = self.canvas.create_oval(
            x - point_radius, y - point_radius,
            x + point_radius, y + point_radius,
            fill="yellow",
            outline="orange",
            width=3,
            tags="calibration_point"
        )

        print(f"[INFO] Showing yellow light at {position} for 3 seconds")

        # Remove the point after 3 seconds
        def remove_point():
            try:
                self.canvas.delete(point_id)
                print(f"[INFO] Removed yellow light from {position}")
            except:
                pass  # Point might already be deleted

        # Schedule removal after 3000ms (3 seconds)
        self.root.after(3000, remove_point)

    def get_highlight_color(self, counter: int) -> str:
        """Get the appropriate highlight color based on counter value and alpha channel support"""
        if counter == 0:
            return self.COLORS["ring"]  # No highlight

        if not self.supports_alpha:
            # Use fallback colors for systems without alpha support
            if counter >= self.SELECTION_THRESHOLD:
                return self.FALLBACK_COLORS["highlight_4"]
            else:
                return self.FALLBACK_COLORS[f"highlight_{counter}"]
        else:
            # Calculate opacity based on counter and threshold
            opacity_ratio = min(counter / self.SELECTION_THRESHOLD, 1.0)
            opacity_hex = format(int(opacity_ratio * 255), '02x')
            return f"#3388ff{opacity_hex}"

    def get_display_text(self) -> str:
        """Get the text to display in the center circle (last MAX_DISPLAY_CHARS characters)"""
        if len(self.current_text) <= self.MAX_DISPLAY_CHARS:
            return self.current_text
        else:
            return self.current_text[-self.MAX_DISPLAY_CHARS:]

    def get_center_circle_text(self) -> str:
        """Get the text to display in center circle based on current state"""
        if self.state == "NUM":
            return "."  # Decimal point in NUM mode
        else:
            return self.get_display_text()  # Normal text in other modes

    def compute_character_positions(self) -> None:
        """
        Precomputes positions for all characters and buttons.
        - MAIN mode: Clusters letters within 45-degree sectors radially.
        - Secondary mode: Letters distributed in equal segments around the full circle.
        - Special buttons (NUM, ⟲, ✔, X) use Cartesian coordinates.

        MODIFIED: Increased outer ring by 1/3 and inner ring by 1/5
        MODIFIED: Numbers are now 10 equally spaced (no decimal point)
        """
        center_x, center_y = 250, 250  # Center of the screen

        ### --- MAIN VIEW: Radial arrangement within sectors --- ###
        # Define sector centers and arrangements
        sector_info = {
            "TOP": {
                "center_angle": 90,  # degrees
                "center_radius": 100,  # Increased from 75 by 1/3
                "letters": self.TOP
            },
            "RIGHT": {
                "center_angle": 0,  # degrees
                "center_radius": 100,  # Increased from 75 by 1/3
                "letters": self.RIGHT
            },
            "BOTTOM": {
                "center_angle": 270,  # degrees
                "center_radius": 100,  # Increased from 75 by 1/3
                "letters": self.BOTTOM
            },
            "LEFT": {
                "center_angle": 180,  # degrees
                "center_radius": 100,  # Increased from 75 by 1/3
                "letters": self.LEFT
            }
        }

        # Position letters radially within each sector
        for section, info in sector_info.items():
            letters = info["letters"]
            center_angle = math.radians(info["center_angle"])
            center_radius = info["center_radius"]

            # Calculate center position of the sector
            sector_center_x = center_x + center_radius * math.cos(center_angle)
            sector_center_y = center_y - center_radius * math.sin(center_angle)

            # Arrange letters in a radial pattern around the sector center
            if section == "RIGHT":  # Vowels - arrange in a smaller, tighter pattern
                base_radius = 30
                angle_spread = 50  # degrees
            else:  # Consonants - arrange in a larger pattern
                base_radius = 30
                angle_spread = 50  # degrees

            # Calculate angles for each letter
            if len(letters) == 1:
                angles = [0]
            else:
                start_angle = info["center_angle"] - angle_spread / 2
                end_angle = info["center_angle"] + angle_spread / 2
                angles = [start_angle + i * angle_spread / (len(letters) - 1) for i in range(len(letters))]

            # Position each letter
            for i, char in enumerate(letters):
                if len(letters) == 1:
                    # Single letter - place at sector center
                    char_x = sector_center_x
                    char_y = sector_center_y
                else:
                    # Multiple letters - arrange radially
                    char_angle = math.radians(angles[i])
                    # Vary radius slightly for visual appeal
                    radius_variation = base_radius + (i % 2) * 5
                    char_x = center_x + (center_radius + radius_variation * 0.7) * math.cos(char_angle)
                    char_y = center_y - (center_radius + radius_variation * 0.7) * math.sin(char_angle)

                self.character_positions[(char, "MAIN")] = (char_x, char_y)

        ### --- SECONDARY VIEW: Full circle with equal segments --- ###
        ring_radius = 120  # Increased from 100 by 1/5
        for section, chars in self.letters.items():
            num_chars = len(chars)
            for i, char in enumerate(chars):
                # Calculate angle for arc segments - divide 360 degrees evenly
                start_angle = 360 * i / num_chars
                end_angle = 360 * (i + 1) / num_chars

                # Store the start and end angles for drawing arcs
                self.character_positions[(f"{char}_start", section)] = start_angle
                self.character_positions[(f"{char}_end", section)] = end_angle

                # Calculate angle for text position - in the middle of the segment
                text_angle = math.radians((start_angle + end_angle) / 2)

                # Store position for text - place it at 90% of the radius (moved 20% outward from 75%)
                self.character_positions[(char, section)] = (
                    center_x + (ring_radius * 0.9) * math.cos(text_angle),
                    center_y - (ring_radius * 0.9) * math.sin(text_angle)
                )

        ### --- NUMBERS: 10 Equally Spaced Positions in a Circle (MODIFIED) --- ###
        for i, num in enumerate(self.numbers):
            # Calculate angle for arc segments - 10 equal divisions
            start_angle = 360 * i / len(self.numbers)
            end_angle = 360 * (i + 1) / len(self.numbers)

            # Store the start and end angles for drawing arcs
            self.character_positions[(f"{num}_start", "NUM")] = start_angle
            self.character_positions[(f"{num}_end", "NUM")] = end_angle

            # Calculate angle for text position - in the middle of the segment
            text_angle = math.radians((start_angle + end_angle) / 2)

            # Store position for text - place it at 90% of the radius (moved 20% outward from 75%)
            self.character_positions[(num, "NUM")] = (
                center_x + (ring_radius * 0.9) * math.cos(text_angle),
                center_y - (ring_radius * 0.9) * math.sin(text_angle)
            )

        ### --- SPECIAL BUTTONS (NUM, ⟲, ✔, X) --- ###
        button_positions = {
            "NUM": (83, 83),  # Top-left
            "⟲": (417, 83),  # Top-right
            "✔": (417, 417),  # Bottom-right
            "X": (83, 417)  # Bottom-left
        }

        for button, pos in button_positions.items():
            self.character_positions[(button, "BUTTON")] = pos

    def setup_UI(self):
        """
        The four side buttons are at the lowest layer.
        On top of it is the ring, but it is in fact also a circle.
        On the topmost is the central circle for the text display.
        """
        self.create_side()
        self.create_ring()
        self.create_circle()

    def create_side(self):
        """Creates the four side buttons with explicitly defined positions and colors."""
        # Define explicit positions for each button
        num_x, num_y = self.character_positions[("NUM", "BUTTON")]
        return_x, return_y = self.character_positions[("⟲", "BUTTON")]
        confirm_x, confirm_y = self.character_positions[("✔", "BUTTON")]
        cancel_x, cancel_y = self.character_positions[("X", "BUTTON")]

        # Draw NUM button (21) - store ID for highlighting
        self.corner_button_ids["NUM_BG"] = self.canvas.create_rectangle(
            num_x - 167, num_y - 167, num_x + 167, num_y + 167,
            outline=self.COLORS["border"], fill=self.COLORS["side"], width=3, tags="side_button")
        self.canvas.create_text(num_x, num_y, text="NUM", fill=self.COLORS["text"],
                                font=self.FONT["middle"], tags="side_button")

        # Draw Return button (22) - store ID for highlighting
        self.corner_button_ids["RETURN_BG"] = self.canvas.create_rectangle(
            return_x - 167, return_y - 167, return_x + 167, return_y + 167,
            outline=self.COLORS["border"], fill=self.COLORS["side"], width=3, tags="side_button")
        self.canvas.create_text(return_x, return_y, text="⟲", fill=self.COLORS["text"],
                                font=self.FONT["middle"], tags="side_button")

        # Draw Confirm button (24) - store ID for highlighting
        self.corner_button_ids["CONFIRM_BG"] = self.canvas.create_rectangle(
            confirm_x - 167, confirm_y - 167, confirm_x + 167, confirm_y + 167,
            outline=self.COLORS["border"], fill=self.COLORS["side"], width=3, tags="side_button")
        self.canvas.create_text(confirm_x, confirm_y, text="✔", fill=self.COLORS["confirm"],
                                font=self.FONT["middle"], tags="side_button")

        # Draw Cancel/Delete button (23) - store ID for highlighting
        self.corner_button_ids["DELETE_BG"] = self.canvas.create_rectangle(
            cancel_x - 167, cancel_y - 167, cancel_x + 167, cancel_y + 167,
            outline=self.COLORS["border"], fill=self.COLORS["side"], width=3, tags="side_button")
        self.canvas.create_text(cancel_x, cancel_y, text="X", fill=self.COLORS["cancel"],
                                font=self.FONT["middle"], tags="side_button")

    def update_corner_button_highlighting(self):
        """Update the highlighting of corner buttons based on their counters"""
        # Update NUM button
        if "NUM_BG" in self.corner_button_ids:
            color = self.get_highlight_color(self.counters["NUM"])
            self.canvas.itemconfig(self.corner_button_ids["NUM_BG"], fill=color)

        # Update RETURN button
        if "RETURN_BG" in self.corner_button_ids:
            color = self.get_highlight_color(self.counters["RETURN"])
            self.canvas.itemconfig(self.corner_button_ids["RETURN_BG"], fill=color)

        # Update DELETE button
        if "DELETE_BG" in self.corner_button_ids:
            color = self.get_highlight_color(self.counters["DELETE"])
            self.canvas.itemconfig(self.corner_button_ids["DELETE_BG"], fill=color)

        # Update CONFIRM button
        if "CONFIRM_BG" in self.corner_button_ids:
            color = self.get_highlight_color(self.counters["CONFIRM"])
            self.canvas.itemconfig(self.corner_button_ids["CONFIRM_BG"], fill=color)

    def update_center_circle_highlighting(self):
        """Update the highlighting of center circle based on its counter"""
        if self.center_circle_id:
            color = self.get_highlight_color(self.counters["CENTER"])
            # If no highlighting, use background color, otherwise use highlight color
            if self.counters["CENTER"] == 0:
                color = self.COLORS["background"]
            self.canvas.itemconfig(self.center_circle_id, fill=color)

    def create_ring(self):
        """Draws the four-sectioned ring with arcs. Modified with larger outer ring."""
        # Create the outer ring with increased size (by 1/3)
        ring_size = 400  # Increased from 300
        offset = (500 - ring_size) // 2  # Center the ring
        self.canvas.create_oval(offset, offset, offset + ring_size, offset + ring_size,
                                outline=self.COLORS["border"],
                                fill=self.COLORS["background"], width=3, tags="outer_ring")

        # Create the four sections and store their IDs
        self.section_ids["TOP"] = self.canvas.create_arc(offset, offset, offset + ring_size, offset + ring_size,
                                                         start=45, extent=90,
                                                         outline=self.COLORS["border"],
                                                         fill=self.COLORS["ring"], width=3, tags="TOP")

        self.section_ids["RIGHT"] = self.canvas.create_arc(offset, offset, offset + ring_size, offset + ring_size,
                                                           start=315, extent=90,
                                                           outline=self.COLORS["border"],
                                                           fill=self.COLORS["ring"], width=3, tags="RIGHT")

        self.section_ids["BOTTOM"] = self.canvas.create_arc(offset, offset, offset + ring_size, offset + ring_size,
                                                            start=225, extent=90,
                                                            outline=self.COLORS["border"],
                                                            fill=self.COLORS["ring"], width=3, tags="BOTTOM")

        self.section_ids["LEFT"] = self.canvas.create_arc(offset, offset, offset + ring_size, offset + ring_size,
                                                          start=135, extent=90,
                                                          outline=self.COLORS["border"],
                                                          fill=self.COLORS["ring"], width=3, tags="LEFT")

        # Add letter indicators to MAIN view - now positioned radially
        for section, letters in self.letters.items():
            for char in letters:
                x, y = self.character_positions[(char, "MAIN")]
                self.canvas.create_text(x, y, text=char, fill=self.COLORS["text"],
                                        font=self.FONT["small"], tags="main_characters")

    def create_circle(self):
        """Draws the central text display circle with a border. Modified with larger inner circle."""
        # Increase inner circle size by 1/5 (from 100 to 120)
        circle_size = 120
        offset = (500 - circle_size) // 2
        self.center_circle_id = self.canvas.create_oval(offset, offset, offset + circle_size, offset + circle_size,
                                                        outline=self.COLORS["border"],
                                                        fill=self.COLORS["background"], width=3, tags="center_circle")
        # MODIFIED: Use new center circle text function
        self.canvas.create_text(250, 250, text=self.get_center_circle_text(), font=self.FONT["large"],
                                fill=self.COLORS["text"], tags="center_text")

    def reset_all_counters(self):
        """Reset all counters to 0"""
        for key in self.counters:
            if key == "SECONDARY":
                for sec_key in self.counters["SECONDARY"]:
                    self.counters["SECONDARY"][sec_key] = 0
            else:
                self.counters[key] = 0

    def process_sector_input(self, sector: int) -> None:
        """
        NEW: Process sector input (1-20) based on current state
        """
        if self.state == "MAIN":
            # Check which main section this sector belongs to
            mapping = self.sector_mappings["MAIN"]
            for section, sectors in mapping.items():
                if sector in sectors:
                    self.counters[section] += 1
                    if self.counters[section] >= self.SELECTION_THRESHOLD:
                        self.counters[section] = 0
                        self.reset_all_counters()
                        self.state = section
                        self.update_display(section)
                    else:
                        self.update_display("MAIN")
                    return

            # If sector doesn't match any mapping, dim current selection
            self.dim_current_selection()

        elif self.state in ["RIGHT", "TOP", "LEFT", "BOTTOM"]:
            # In secondary panel, check character-specific mappings
            section = self.state
            chars = self.letters[section]

            # Find which character this sector corresponds to
            for i, char in enumerate(chars):
                counter_key = f"{section}_{i}"

                # For individual character states, we need to check if we're in that state
                if char in self.sector_mappings and sector in self.sector_mappings[char][0]:
                    self.counters["SECONDARY"][counter_key] += 1
                    if self.counters["SECONDARY"][counter_key] >= self.SELECTION_THRESHOLD:
                        self.add_character(char)
                    else:
                        self.update_display(section)
                    return

            # If no match found, dim current selection
            self.dim_current_selection()

        elif self.state == "NUM":
            # In NUM panel, check number mappings
            mapping = self.sector_mappings["NUM"]
            for number, sectors in mapping.items():
                if sector in sectors:
                    counter_key = f"NUM_{number}"
                    self.counters["SECONDARY"][counter_key] += 1
                    if self.counters["SECONDARY"][counter_key] >= self.SELECTION_THRESHOLD:
                        self.add_number(number)
                    else:
                        self.update_display("NUM")
                    return

            # If sector doesn't match any mapping, dim current selection
            self.dim_current_selection()

    def process_button_input(self, button_code: int) -> None:
        """
        NEW: Process button input (21-25)
        21: NUM, 22: RETURN, 23: DELETE, 24: CONFIRM, 25: CENTER
        """
        if button_code == 21:  # NUM
            self.counters["NUM"] += 1
            if self.counters["NUM"] >= self.SELECTION_THRESHOLD:
                self.counters["NUM"] = 0
                self.reset_all_counters()
                self.update_display("NUM")
            else:
                self.update_corner_button_highlighting()

        elif button_code == 22:  # RETURN
            self.counters["RETURN"] += 1
            if self.counters["RETURN"] >= self.SELECTION_THRESHOLD:
                self.counters["RETURN"] = 0
                self.reset_all_counters()
                self.state = "MAIN"
                self.update_display("MAIN")
            else:
                self.update_corner_button_highlighting()

        elif button_code == 23:  # DELETE
            # Disable in secondary panels (except NUM)
            if self.state in ["TOP", "RIGHT", "BOTTOM", "LEFT"]:
                return

            self.counters["DELETE"] += 1
            if self.counters["DELETE"] >= self.SELECTION_THRESHOLD:
                self.counters["DELETE"] = 0
                if self.current_text:
                    self.current_text = self.current_text[:-1]
                    self.update_display(self.state)
                else:
                    self.tts("No")
            else:
                self.update_corner_button_highlighting()

        elif button_code == 24:  # CONFIRM
            # Disable in secondary panels (except NUM)
            if self.state in ["TOP", "RIGHT", "BOTTOM", "LEFT"]:
                return

            self.counters["CONFIRM"] += 1
            if self.counters["CONFIRM"] >= self.SELECTION_THRESHOLD:
                self.counters["CONFIRM"] = 0
                if self.current_text:
                    self.confirm_text()
                else:
                    self.tts("Yes")
            else:
                self.update_corner_button_highlighting()

        elif button_code == 25:  # CENTER
            self.counters["CENTER"] += 1
            if self.counters["CENTER"] >= self.SELECTION_THRESHOLD:
                self.counters["CENTER"] = 0
                if self.state == "NUM":
                    self.add_decimal_point()
                else:
                    self.add_space()
            else:
                self.update_center_circle_highlighting()

    def dim_current_selection(self):
        """Gradually dim the current selection"""
        if self.state == "MAIN":
            # Find highest main section counter and decrement
            max_counter = 0
            max_section = None
            for section in ["TOP", "RIGHT", "BOTTOM", "LEFT"]:
                if self.counters[section] > max_counter:
                    max_counter = self.counters[section]
                    max_section = section
            if max_section:
                self.counters[max_section] = max(0, self.counters[max_section] - 1)
                self.update_display("MAIN")

        elif self.state in ["TOP", "RIGHT", "BOTTOM", "LEFT"]:
            # Find highest secondary counter and decrement
            section = self.state
            max_counter = 0
            max_key = None
            for i in range(len(self.letters[section])):
                counter_key = f"{section}_{i}"
                if self.counters["SECONDARY"][counter_key] > max_counter:
                    max_counter = self.counters["SECONDARY"][counter_key]
                    max_key = counter_key
            if max_key:
                self.counters["SECONDARY"][max_key] = max(0, self.counters["SECONDARY"][max_key] - 1)
                self.update_display(section)

        elif self.state == "NUM":
            # Find highest number counter and decrement
            max_counter = 0
            max_key = None
            for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                counter_key = f"NUM_{num}"
                if self.counters["SECONDARY"][counter_key] > max_counter:
                    max_counter = self.counters["SECONDARY"][counter_key]
                    max_key = counter_key
            if max_key:
                self.counters["SECONDARY"][max_key] = max(0, self.counters["SECONDARY"][max_key] - 1)
                self.update_display("NUM")

    def update_display(self, option: str) -> None:
        """
        Updates the GUI based on the selected mode.
        Modes:
        - 'MAIN'  -> Shows four quadrants (default state).
        - 'RIGHT', 'TOP', 'LEFT', 'BOTTOM' -> Shows secondary panel with characters in a full circle.
        - 'NUM'   -> Displays numeric keypad in a full circle.

        Modified: Updated ring sizes and added larger offset calculations
        MODIFIED: Numbers now use 10 equal divisions instead of 11
        """
        # Clear only the ring and character elements, keep side buttons
        self.canvas.delete("ring")
        self.canvas.delete("characters")
        self.canvas.delete("labels")
        self.canvas.delete("secondary")
        self.canvas.delete("outer_ring")
        self.canvas.delete("main_labels")
        self.canvas.delete("main_characters")

        # Create outer ring FIRST with updated size
        ring_size = 400  # Increased from 300
        offset = (500 - ring_size) // 2
        self.canvas.create_oval(offset, offset, offset + ring_size, offset + ring_size,
                                outline=self.COLORS["border"],
                                fill=self.COLORS["background"], width=3, tags="outer_ring")

        # Update display based on current state
        if option == "MAIN":
            # Create the four main sections
            self.section_ids = {}  # Reset section IDs

            # Create TOP section
            counter_top = self.counters["TOP"]
            self.section_ids["TOP"] = self.canvas.create_arc(
                offset, offset, offset + ring_size, offset + ring_size, start=45, extent=90,
                outline=self.COLORS["border"],
                fill=self.get_highlight_color(counter_top),
                width=3, tags=("ring", "TOP")
            )

            # Create RIGHT section
            counter_right = self.counters["RIGHT"]
            self.section_ids["RIGHT"] = self.canvas.create_arc(
                offset, offset, offset + ring_size, offset + ring_size, start=315, extent=90,
                outline=self.COLORS["border"],
                fill=self.get_highlight_color(counter_right),
                width=3, tags=("ring", "RIGHT")
            )

            # Create BOTTOM section
            counter_bottom = self.counters["BOTTOM"]
            self.section_ids["BOTTOM"] = self.canvas.create_arc(
                offset, offset, offset + ring_size, offset + ring_size, start=225, extent=90,
                outline=self.COLORS["border"],
                fill=self.get_highlight_color(counter_bottom),
                width=3, tags=("ring", "BOTTOM")
            )

            # Create LEFT section
            counter_left = self.counters["LEFT"]
            self.section_ids["LEFT"] = self.canvas.create_arc(
                offset, offset, offset + ring_size, offset + ring_size, start=135, extent=90,
                outline=self.COLORS["border"],
                fill=self.get_highlight_color(counter_left),
                width=3, tags=("ring", "LEFT")
            )

            # Add letter indicators to MAIN view - positioned radially
            for section, letters in self.letters.items():
                for char in letters:
                    x, y = self.character_positions[(char, "MAIN")]
                    self.canvas.create_text(x, y, text=char, fill=self.COLORS["text"],
                                            font=self.FONT["small"], tags="main_characters")

        elif option == "NUM":
            # MODIFIED: Display numeric characters in circular layout with 10 equal divisions
            self.secondary_section_ids = {}

            # Create arcs for each number (now 10 instead of 11)
            for i, num in enumerate(self.numbers):
                start_angle = self.character_positions[(f"{num}_start", "NUM")]
                end_angle = self.character_positions[(f"{num}_end", "NUM")]
                extent = end_angle - start_angle

                # Get counter for highlighting
                counter_key = f"NUM_{num}"
                counter = self.counters["SECONDARY"][counter_key]

                # Create arc for this number
                self.secondary_section_ids[num] = self.canvas.create_arc(
                    offset, offset, offset + ring_size, offset + ring_size, start=start_angle, extent=extent,
                    outline=self.COLORS["border"], fill=self.get_highlight_color(counter),
                    width=3, tags=("ring", "secondary", f"num_{i}")
                )

                # Add number text - positioned at middle of segment
                x, y = self.character_positions[(num, "NUM")]
                self.canvas.create_text(x, y, text=num, fill=self.COLORS["text"],
                                        font=self.FONT["middle"], tags="characters")

        elif option in ["RIGHT", "TOP", "LEFT", "BOTTOM"]:
            # Show selected section characters in a full circle
            section = option
            chars = self.letters[section]
            self.secondary_section_ids = {}

            # Create arcs for each character
            for i, char in enumerate(chars):
                start_angle = self.character_positions[(f"{char}_start", section)]
                end_angle = self.character_positions[(f"{char}_end", section)]
                extent = end_angle - start_angle

                # Create arc for this character with appropriate highlighting
                counter_key = f"{section}_{i}"
                counter = self.counters["SECONDARY"][counter_key]
                fill_color = self.get_highlight_color(counter)

                self.secondary_section_ids[char] = self.canvas.create_arc(
                    offset, offset, offset + ring_size, offset + ring_size, start=start_angle, extent=extent,
                    outline=self.COLORS["border"], fill=fill_color,
                    width=3, tags=("ring", "secondary", f"char_{i}")
                )

                # Add ONLY the character text - positioned at middle of segment
                x, y = self.character_positions[(char, section)]
                self.canvas.create_text(x, y, text=char, fill=self.COLORS["text"],
                                        font=self.FONT["large"], tags="characters")

        # Update corner button highlighting
        self.update_corner_button_highlighting()

        # ALWAYS draw the center circle and text LAST to ensure it's on top
        self.canvas.delete("center_circle")
        self.canvas.delete("center_text")
        # Updated center circle size
        circle_size = 120  # Increased from 100
        circle_offset = (500 - circle_size) // 2
        self.center_circle_id = self.canvas.create_oval(circle_offset, circle_offset,
                                                        circle_offset + circle_size, circle_offset + circle_size,
                                                        outline=self.COLORS["border"],
                                                        fill=self.COLORS["background"], width=3, tags="center_circle")

        # Update center circle highlighting
        self.update_center_circle_highlighting()

        # MODIFIED: Display appropriate text based on mode
        self.canvas.create_text(250, 250, text=self.get_center_circle_text(), font=self.FONT["large"],
                                fill=self.COLORS["text"], tags="center_text")

        self.state = option  # Update the state of the interface

    def add_character(self, char: str) -> None:
        """Adds the selected letter to current_text"""
        self.current_text += char

        # Reset all counters
        self.reset_all_counters()

        # Return to main state
        self.state = "MAIN"
        self.update_display("MAIN")

    def add_number(self, num: str) -> None:
        """ADDED: Adds the selected number to current_text"""
        self.current_text += num

        # Reset all counters
        self.reset_all_counters()

        # Stay in NUM state (don't return to MAIN automatically)
        self.update_display("NUM")

    def add_space(self) -> None:
        """Adds a space to the current text"""
        self.current_text += ' '

        # Reset all counters
        self.reset_all_counters()

        # Update display to show new text
        self.update_display(self.state)

    def add_decimal_point(self) -> None:
        """ADDED: Adds a decimal point to the current text"""
        self.current_text += '.'

        # Reset all counters
        self.reset_all_counters()

        # Update display to show new text
        self.update_display(self.state)

    def confirm_text(self) -> None:
        """Convert current text to speech and clear"""
        if self.current_text:
            self.tts(self.current_text)
            self.current_text = ""

            # Reset all counters and return to main state
            self.reset_all_counters()

            self.state = "MAIN"
            self.update_display("MAIN")

    def command_listener(self):
        """Listen for commands from the terminal"""
        print("\nWelcome to AAC Keyboard - 20 Sector System")
        print(f"Selection threshold: {self.SELECTION_THRESHOLD} commands")
        print(f"Display limit: {self.MAX_DISPLAY_CHARS} characters")
        print("Commands:")
        print("1-20: Ring sectors (mapping depends on current state)")
        print("21: NUM mode (top-left corner)")
        print("22: Return to main panel (top-right corner)")
        print("23: Delete last character (bottom-left corner)")
        print("24: Confirm/text-to-speech (bottom-right corner)")
        print("25: Space/decimal point (center circle)")
        print("Type 'exit' to quit\n")
        # cmd = region

### ---------- receive ----------

    def process_command(self, cmd: str):
        """
        Process the received command for 20-sector system or calibration points
        """
        try:
            if cmd.lower() == 'exit':
                self.root.quit()
                return

            # Check if it's a calibration position command
            calibration_positions = ["center", "top_mid", "left_mid", "bottom_mid", "right_mid"]
            if cmd.lower() in calibration_positions:
                self.show_calibration_point(cmd.lower())
                return

            # Parse the command as number
            try:
                command_num = int(cmd)
            except ValueError:
                print(f"Invalid command: {cmd}. Please use numbers 1-25 or calibration positions")
                self.dim_current_selection()
                return

            # Process based on command range
            if 1 <= command_num <= 20:
                # Ring sector commands
                self.process_sector_input(command_num)
            elif 21 <= command_num <= 25:
                # Button commands
                self.process_button_input(command_num)
            else:
                print("Invalid command. Please use numbers 1-25")
                self.dim_current_selection()

        except Exception as e:
            print(f"Error in process_command: {e}")
    @staticmethod
    def tts(input_text: str) -> None:
        """Converts text to speech using gTTS and plays it with pygame."""
        print(f"Text-to-speech: '{input_text}'")
        file_path = "output.mp3"
        speech = gTTS(input_text, lang='en', tld='co.uk')
        speech.save(file_path)

        # Ensure pygame mixer is initialized before playing
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.quit()  # Close mixer to release file lock
        try:
            os.remove(file_path)
        except:
            pass  # Ignore if file can't be deleted


def main():
    root = tk.Tk()
    app = AAC_GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()