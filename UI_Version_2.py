import tkinter as tk
import time
import threading
from typing import List, Dict, Tuple, Any
import pygame
from gtts import gTTS
import os
import math
import re


class AAC_GUI():
    """
    This is the main OOP program for creating the interactive GUI.
    Revised version that accepts terminal commands instead of hover selection.
    Commands:
    - 1, 2, 3, 4: Select main sections (top, right, bottom, left)
    - 5, 6, 7, 8: Corner controls (mode switch, return, delete, confirm)
    - 9: Center circle (space key)
    - 1a, 1b, etc: Select specific letters in secondary panels
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
        "highlight_0": "#e2e8f0",     # Light gray
        "highlight_1": "#dbeafe",     # Very light blue
        "highlight_2": "#bfdbfe",     # Light blue
        "highlight_3": "#93c5fd",     # Medium blue
        "highlight_4": "#3b82f6",     # Full blue
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

        # Main section selection counters
        self.selection_counters = {
            "TOP": 0,
            "RIGHT": 0,
            "BOTTOM": 0,
            "LEFT": 0
        }

        # Corner button selection counters
        self.corner_counters = {
            "NUM": 0,  # Button 5
            "RETURN": 0,  # Button 6
            "DELETE": 0,  # Button 7
            "CONFIRM": 0  # Button 8
        }

        # Center circle (space key) counter
        self.center_counter = 0  # Button 9

        # Secondary selection counters (for each letter in each section)
        self.secondary_counters = {
            "TOP": [0] * len(self.TOP),
            "RIGHT": [0] * len(self.RIGHT),
            "BOTTOM": [0] * len(self.BOTTOM),
            "LEFT": [0] * len(self.LEFT)
        }

        # Current active secondary section (if any)
        self.active_secondary = None
        self.active_secondary_index = -1

        # Test for alpha channel support in tkinter
        try:
            self.root.winfo_rgb("#3388ff33")
            self.supports_alpha = True
        except:
            self.supports_alpha = False
            print("Warning: System doesn't support alpha channels in colors. Using fallback colors.")

        self.root.title("AAC Keyboard - Command Based")
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg=self.COLORS["background"])
        self.canvas.pack()

        self.letters = {
            "RIGHT": self.RIGHT,
            "TOP": self.TOP,
            "LEFT": self.LEFT,
            "BOTTOM": self.BOTTOM
        }

        self.numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
        self.character_positions = {}
        self.section_ids = {}  # Store canvas IDs for main sections
        self.secondary_section_ids = {}  # Store canvas IDs for secondary sections
        self.corner_button_ids = {}  # Store canvas IDs for corner buttons
        self.center_circle_id = None  # Store canvas ID for center circle

        self.compute_character_positions()
        self.setup_UI()

        # Start command input thread
        self.command_thread = threading.Thread(target=self.command_listener, daemon=True)
        self.command_thread.start()

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

    def compute_character_positions(self) -> None:
        """
        Precomputes positions for all characters and buttons.
        - MAIN mode: Clusters letters within 45-degree sectors radially.
        - Secondary mode: Letters distributed in equal segments around the full circle.
        - Special buttons (NUM, ⟲, ✔, X) use Cartesian coordinates.
        """
        center_x, center_y = 250, 250  # Center of the screen

        ### --- MAIN VIEW: Radial arrangement within sectors --- ###
        # Define sector centers and arrangements
        sector_info = {
            "TOP": {
                "center_angle": 90,  # degrees
                "center_radius": 75,
                "letters": self.TOP
            },
            "RIGHT": {
                "center_angle": 0,  # degrees
                "center_radius": 75,
                "letters": self.RIGHT
            },
            "BOTTOM": {
                "center_angle": 270,  # degrees
                "center_radius": 75,
                "letters": self.BOTTOM
            },
            "LEFT": {
                "center_angle": 180,  # degrees
                "center_radius": 75,
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
        ring_radius = 100
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

        ### --- NUMBERS: 11 Equally Spaced Positions in a Circle --- ###
        for i, num in enumerate(self.numbers):
            # Calculate angle for arc segments
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
            "NUM": (100, 100),  # Top-left
            "⟲": (400, 100),  # Top-right
            "✔": (400, 400),  # Bottom-right
            "X": (100, 400)  # Bottom-left
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

        # Draw NUM button (5) - store ID for highlighting
        self.corner_button_ids["NUM_BG"] = self.canvas.create_rectangle(
            num_x - 150, num_y - 150, num_x + 150, num_y + 150,
            outline=self.COLORS["border"], fill=self.COLORS["side"], width=3, tags="side_button")
        self.canvas.create_text(num_x, num_y, text="NUM", fill=self.COLORS["text"],
                                font=self.FONT["middle"], tags="side_button")

        # Draw Return button (6) - store ID for highlighting
        self.corner_button_ids["RETURN_BG"] = self.canvas.create_rectangle(
            return_x - 150, return_y - 150, return_x + 150, return_y + 150,
            outline=self.COLORS["border"], fill=self.COLORS["side"], width=3, tags="side_button")
        self.canvas.create_text(return_x, return_y, text="⟲", fill=self.COLORS["text"],
                                font=self.FONT["middle"], tags="side_button")

        # Draw Confirm button (8) - store ID for highlighting
        self.corner_button_ids["CONFIRM_BG"] = self.canvas.create_rectangle(
            confirm_x - 150, confirm_y - 150, confirm_x + 150, confirm_y + 150,
            outline=self.COLORS["border"], fill=self.COLORS["side"], width=3, tags="side_button")
        self.canvas.create_text(confirm_x, confirm_y, text="✔", fill=self.COLORS["confirm"],
                                font=self.FONT["middle"], tags="side_button")

        # Draw Cancel/Delete button (7) - store ID for highlighting
        self.corner_button_ids["DELETE_BG"] = self.canvas.create_rectangle(
            cancel_x - 150, cancel_y - 150, cancel_x + 150, cancel_y + 150,
            outline=self.COLORS["border"], fill=self.COLORS["side"], width=3, tags="side_button")
        self.canvas.create_text(cancel_x, cancel_y, text="X", fill=self.COLORS["cancel"],
                                font=self.FONT["middle"], tags="side_button")

    def update_corner_button_highlighting(self):
        """Update the highlighting of corner buttons based on their counters"""
        # Update NUM button
        if "NUM_BG" in self.corner_button_ids:
            color = self.get_highlight_color(self.corner_counters["NUM"])
            self.canvas.itemconfig(self.corner_button_ids["NUM_BG"], fill=color)

        # Update RETURN button
        if "RETURN_BG" in self.corner_button_ids:
            color = self.get_highlight_color(self.corner_counters["RETURN"])
            self.canvas.itemconfig(self.corner_button_ids["RETURN_BG"], fill=color)

        # Update DELETE button
        if "DELETE_BG" in self.corner_button_ids:
            color = self.get_highlight_color(self.corner_counters["DELETE"])
            self.canvas.itemconfig(self.corner_button_ids["DELETE_BG"], fill=color)

        # Update CONFIRM button
        if "CONFIRM_BG" in self.corner_button_ids:
            color = self.get_highlight_color(self.corner_counters["CONFIRM"])
            self.canvas.itemconfig(self.corner_button_ids["CONFIRM_BG"], fill=color)

    def update_center_circle_highlighting(self):
        """Update the highlighting of center circle based on its counter"""
        if self.center_circle_id:
            color = self.get_highlight_color(self.center_counter)
            # If no highlighting, use background color, otherwise use highlight color
            if self.center_counter == 0:
                color = self.COLORS["background"]
            self.canvas.itemconfig(self.center_circle_id, fill=color)

    def create_ring(self):
        """Draws the four-sectioned ring with arcs."""
        # Create the outer ring
        self.canvas.create_oval(100, 100, 400, 400, outline=self.COLORS["border"],
                                fill=self.COLORS["background"], width=3, tags="outer_ring")

        # Create the four sections with their command numbers and store their IDs
        self.section_ids["TOP"] = self.canvas.create_arc(100, 100, 400, 400, start=45, extent=90,
                                                         outline=self.COLORS["border"],
                                                         fill=self.COLORS["ring"], width=3, tags="TOP")

        self.section_ids["RIGHT"] = self.canvas.create_arc(100, 100, 400, 400, start=315, extent=90,
                                                           outline=self.COLORS["border"],
                                                           fill=self.COLORS["ring"], width=3, tags="RIGHT")

        self.section_ids["BOTTOM"] = self.canvas.create_arc(100, 100, 400, 400, start=225, extent=90,
                                                            outline=self.COLORS["border"],
                                                            fill=self.COLORS["ring"], width=3, tags="BOTTOM")

        self.section_ids["LEFT"] = self.canvas.create_arc(100, 100, 400, 400, start=135, extent=90,
                                                          outline=self.COLORS["border"],
                                                          fill=self.COLORS["ring"], width=3, tags="LEFT")

        # Add letter indicators to MAIN view - now positioned radially
        for section, letters in self.letters.items():
            for char in letters:
                x, y = self.character_positions[(char, "MAIN")]
                self.canvas.create_text(x, y, text=char, fill=self.COLORS["text"],
                                        font=self.FONT["small"], tags="main_characters")

    def create_circle(self):
        """Draws the central text display circle with a border."""
        self.center_circle_id = self.canvas.create_oval(200, 200, 300, 300, outline=self.COLORS["border"],
                                                        fill=self.COLORS["background"], width=3, tags="center_circle")
        self.canvas.create_text(250, 250, text=self.get_display_text(), font=self.FONT["large"],
                                fill=self.COLORS["text"], tags="center_text")

    def dim_current_selection(self):
        """Gradually dim the current selection in secondary panels"""
        if self.state in ["TOP", "RIGHT", "BOTTOM", "LEFT"]:
            # Find the highest counter in the current secondary panel
            section = self.state
            max_counter = max(self.secondary_counters[section])
            if max_counter > 0:
                # Find the index with the highest counter and decrement it
                for i, counter in enumerate(self.secondary_counters[section]):
                    if counter == max_counter:
                        self.secondary_counters[section][i] = max(0, counter - 1)
                        break
                # Update the display to show the dimming
                self.update_display(self.state)

    def update_display(self, option: str) -> None:
        """
        Updates the GUI based on the selected mode.
        Modes:
        - 'MAIN'  -> Shows four quadrants (default state).
        - 'RIGHT', 'TOP', 'LEFT', 'BOTTOM' -> Shows secondary panel with characters in a full circle.
        - 'NUM'   -> Displays numeric keypad in a full circle.
        """
        # Clear only the ring and character elements, keep side buttons
        self.canvas.delete("ring")
        self.canvas.delete("characters")
        self.canvas.delete("labels")
        self.canvas.delete("secondary")
        self.canvas.delete("outer_ring")
        self.canvas.delete("main_labels")
        self.canvas.delete("main_characters")

        # Create outer ring FIRST
        self.canvas.create_oval(100, 100, 400, 400, outline=self.COLORS["border"],
                                fill=self.COLORS["background"], width=3, tags="outer_ring")

        # Update display based on current state
        if option == "MAIN":
            # Create the four main sections
            self.section_ids = {}  # Reset section IDs

            # Create TOP section
            counter_top = self.selection_counters["TOP"]
            self.section_ids["TOP"] = self.canvas.create_arc(
                100, 100, 400, 400, start=45, extent=90,
                outline=self.COLORS["border"],
                fill=self.get_highlight_color(counter_top),
                width=3, tags=("ring", "TOP")
            )

            # Create RIGHT section
            counter_right = self.selection_counters["RIGHT"]
            self.section_ids["RIGHT"] = self.canvas.create_arc(
                100, 100, 400, 400, start=315, extent=90,
                outline=self.COLORS["border"],
                fill=self.get_highlight_color(counter_right),
                width=3, tags=("ring", "RIGHT")
            )

            # Create BOTTOM section
            counter_bottom = self.selection_counters["BOTTOM"]
            self.section_ids["BOTTOM"] = self.canvas.create_arc(
                100, 100, 400, 400, start=225, extent=90,
                outline=self.COLORS["border"],
                fill=self.get_highlight_color(counter_bottom),
                width=3, tags=("ring", "BOTTOM")
            )

            # Create LEFT section
            counter_left = self.selection_counters["LEFT"]
            self.section_ids["LEFT"] = self.canvas.create_arc(
                100, 100, 400, 400, start=135, extent=90,
                outline=self.COLORS["border"],
                fill=self.get_highlight_color(counter_left),
                width=3, tags=("ring", "LEFT")
            )

            # Add letter indicators to MAIN view - positioned radially
            for section, letters in self.letters.items():
                for char in letters:
                    x, y = self.character_positions[(char, "MAIN")]
                    self.canvas.create_text(x, y, text=char, fill=self.COLORS["text"],
                                            font= self.FONT["small"], tags="main_characters")

        elif option == "NUM":
            # Display numeric characters in circular layout with full 360-degree arcs
            self.secondary_section_ids = {}

            # Create arcs for each number
            for i, num in enumerate(self.numbers):
                start_angle = self.character_positions[(f"{num}_start", "NUM")]
                end_angle = self.character_positions[(f"{num}_end", "NUM")]
                extent = end_angle - start_angle

                # Create arc for this number
                self.secondary_section_ids[num] = self.canvas.create_arc(
                    100, 100, 400, 400, start=start_angle, extent=extent,
                    outline=self.COLORS["border"], fill=self.COLORS["ring"],
                    width=3, tags=("ring", "secondary", f"num_{i}")
                )

                # Add number text - positioned at middle of segment
                x, y = self.character_positions[(num, "NUM")]
                self.canvas.create_text(x, y, text=num, fill=self.COLORS["text"],
                                        font= self.FONT["middle"], tags="characters")

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
                counter = self.secondary_counters[section][i]
                fill_color = self.get_highlight_color(counter)

                self.secondary_section_ids[char] = self.canvas.create_arc(
                    100, 100, 400, 400, start=start_angle, extent=extent,
                    outline=self.COLORS["border"], fill=fill_color,
                    width=3, tags=("ring", "secondary", f"char_{i}")
                )

                # Add ONLY the character text - positioned at middle of segment
                x, y = self.character_positions[(char, section)]
                self.canvas.create_text(x, y, text=char, fill=self.COLORS["text"],
                                        font= self.FONT["large"], tags="characters")

        # Update corner button highlighting
        self.update_corner_button_highlighting()

        # ALWAYS draw the center circle and text LAST to ensure it's on top
        self.canvas.delete("center_circle")
        self.canvas.delete("center_text")
        self.center_circle_id = self.canvas.create_oval(200, 200, 300, 300, outline=self.COLORS["border"],
                                                        fill=self.COLORS["background"], width=3, tags="center_circle")

        # Update center circle highlighting
        self.update_center_circle_highlighting()

        # Display truncated text
        self.canvas.create_text(250, 250, text=self.get_display_text(), font= self.FONT["large"],
                                fill=self.COLORS["text"], tags="center_text")

        self.state = option  # Update the state of the interface
        self.active_secondary = None  # Reset active secondary selection
        self.active_secondary_index = -1

    def select_option(self, option: str) -> None:
        """Handles selection of quadrants (LEFT, RIGHT, etc.) and updates state"""
        if option in self.selection_counters:
            # Increment the counter for this section
            self.selection_counters[option] += 1

            # If counter reaches threshold, activate secondary panel
            if self.selection_counters[option] >= self.SELECTION_THRESHOLD:
                self.selection_counters[option] = 0  # Reset counter
                self.state = option  # Activate secondary panel
                self.update_display(option)
            else:
                # Just update highlighting in MAIN state
                self.update_display("MAIN")
        else:
            self.state = option
            self.update_display(option)

    def select_corner_button(self, button: str) -> None:
        """Handles selection of corner buttons with gradual lighting"""
        if button in self.corner_counters:
            # Increment the counter for this corner button
            self.corner_counters[button] += 1

            # If counter reaches threshold, execute the button action
            if self.corner_counters[button] >= self.SELECTION_THRESHOLD:
                self.corner_counters[button] = 0  # Reset counter
                self.handle_side_buttons(button)
            else:
                # Just update highlighting
                self.update_corner_button_highlighting()

    def select_center_circle(self) -> None:
        """Handles selection of center circle (space key) with gradual lighting"""
        # Increment the counter for center circle
        self.center_counter += 1

        # If counter reaches threshold, add space
        if self.center_counter >= self.SELECTION_THRESHOLD:
            self.center_counter = 0  # Reset counter
            self.add_space()
        else:
            # Just update highlighting
            self.update_center_circle_highlighting()

    def add_space(self) -> None:
        """Adds a space to the current text"""
        self.current_text += ' '

        # Reset all selection counters
        for section in self.selection_counters:
            self.selection_counters[section] = 0

        for section in self.secondary_counters:
            for i in range(len(self.secondary_counters[section])):
                self.secondary_counters[section][i] = 0

        for corner in self.corner_counters:
            self.corner_counters[corner] = 0

        self.center_counter = 0

        # Update display to show new text
        self.update_display(self.state)

    def select_secondary_option(self, section: str, index: int) -> None:
        """Handles selection of secondary options and updates state"""
        if section in self.secondary_counters and 0 <= index < len(self.secondary_counters[section]):
            # Store the active secondary section and index
            self.active_secondary = section
            self.active_secondary_index = index

            # Increment the counter for this secondary option
            self.secondary_counters[section][index] += 1

            # If counter reaches threshold, select this character
            if self.secondary_counters[section][index] >= self.SELECTION_THRESHOLD:
                # Add the character to current text
                char = self.letters[section][index]
                self.add_character(char)

                # Reset counter
                self.secondary_counters[section][index] = 0

                # Return to main panel
                self.active_secondary = None
                self.active_secondary_index = -1
            else:
                # Just update the display to show highlighting
                self.update_display(section)
        else:
            print(f"Invalid secondary option: {section}, index {index}")

    def add_character(self, char: str) -> None:
        """Adds the selected letter to current_text"""
        self.current_text += char

        # Reset all selection counters
        for section in self.selection_counters:
            self.selection_counters[section] = 0

        for section in self.secondary_counters:
            for i in range(len(self.secondary_counters[section])):
                self.secondary_counters[section][i] = 0

        for corner in self.corner_counters:
            self.corner_counters[corner] = 0

        self.center_counter = 0

        # Return to main state
        self.state = "MAIN"
        self.update_display("MAIN")

    def confirm_text(self) -> None:
        """Convert current text to speech and clear"""
        if self.current_text:
            self.tts(self.current_text)
            self.current_text = ""

            # Reset all counters and return to main state
            for section in self.selection_counters:
                self.selection_counters[section] = 0

            for section in self.secondary_counters:
                for i in range(len(self.secondary_counters[section])):
                    self.secondary_counters[section][i] = 0

            for corner in self.corner_counters:
                self.corner_counters[corner] = 0

            self.center_counter = 0

            self.state = "MAIN"
            self.update_display("MAIN")

    def handle_side_buttons(self, button: str) -> None:
        """
        Handles side button clicks including Confirm, Cancel, Number Toggle, and Return.
        """
        if button == "NUM":
            self.update_display("NUM")
        elif button == "RETURN":
            # Reset all selection counters
            for section in self.selection_counters:
                self.selection_counters[section] = 0

            for section in self.secondary_counters:
                for i in range(len(self.secondary_counters[section])):
                    self.secondary_counters[section][i] = 0

            for corner in self.corner_counters:
                self.corner_counters[corner] = 0

            self.center_counter = 0

            self.state = "MAIN"  # Reset state to main panel
            self.update_display("MAIN")
        elif button == "CONFIRM":
            if self.current_text != "":
                self.confirm_text()
            else:
                self.tts("Yes")
        elif button == "DELETE":
            if self.current_text:
                self.current_text = self.current_text[:-1]  # Delete last char
                self.update_display(self.state)
            else:
                self.tts("No")  # When empty, output "No"

    def command_listener(self):
        """Listen for commands from the terminal"""
        print("\nWelcome to AAC Keyboard - Command Based")
        print(f"Selection threshold: {self.SELECTION_THRESHOLD} commands")
        print(f"Display limit: {self.MAX_DISPLAY_CHARS} characters")
        print("Commands:")
        print("1-4: Select main sections (top=1, right=2, bottom=3, left=4)")
        print("5: Switch to numbers/letters")
        print("6: Return to main panel")
        print("7: Delete last character")
        print("8: Confirm (text-to-speech)")
        print("9: Space key (center circle)")
        print("1a-1g, 2a-2g, etc: Select specific letters in secondary panels")
        print("Type 'exit' to quit\n")

        while True:
            try:
                cmd = input("Enter command: ")

                # Process the command on the main thread
                self.root.after(0, lambda: self.process_command(cmd))

                if cmd.lower() == 'exit':
                    break
            except Exception as e:
                print(f"Error processing command: {e}")

    def process_command(self, cmd: str):
        """Process the received command and update UI accordingly"""
        try:
            if cmd.lower() == 'exit':
                self.root.quit()
                return

            # Check for main section commands (1-4)
            if cmd == '1':
                if self.state == "MAIN":
                    self.select_option("TOP")
                elif self.state in ["RIGHT", "BOTTOM", "LEFT", "NUM"]:
                    self.dim_current_selection()
            elif cmd == '2':
                if self.state == "MAIN":
                    self.select_option("RIGHT")
                elif self.state in ["TOP", "BOTTOM", "LEFT", "NUM"]:
                    self.dim_current_selection()
            elif cmd == '3':
                if self.state == "MAIN":
                    self.select_option("BOTTOM")
                elif self.state in ["TOP", "RIGHT", "LEFT", "NUM"]:
                    self.dim_current_selection()
            elif cmd == '4':
                if self.state == "MAIN":
                    self.select_option("LEFT")
                elif self.state in ["TOP", "RIGHT", "BOTTOM", "NUM"]:
                    self.dim_current_selection()

            # Check for corner commands (5-8)
            elif cmd == '5':
                self.select_corner_button("NUM")
            elif cmd == '6':
                self.select_corner_button("RETURN")
            elif cmd == '7':
                self.select_corner_button("DELETE")
            elif cmd == '8':
                self.select_corner_button("CONFIRM")

            # Check for center circle command (9) - space key
            elif cmd == '9':
                self.select_center_circle()

            # Check for secondary selection commands (e.g., 1a, 2b)
            elif re.match(r'^[1-4][a-g]$', cmd):
                section_num = int(cmd[0])
                char_index = ord(cmd[1]) - ord('a')

                # Map section number to section name
                section_map = {1: "TOP", 2: "RIGHT", 3: "BOTTOM", 4: "LEFT"}
                section = section_map.get(section_num)

                if section and self.state == section and char_index < len(self.letters[section]):
                    # We're in the correct secondary panel, so select this character
                    self.select_secondary_option(section, char_index)
                else:
                    # Wrong panel or invalid character, dim current selection
                    self.dim_current_selection()
            else:
                print("Invalid command. Please use 1-9 or section+letter (e.g., 1a)")
                if self.state in ["TOP", "RIGHT", "BOTTOM", "LEFT", "NUM"]:
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
