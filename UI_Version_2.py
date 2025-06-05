import tkinter as tk
import time
import threading
from typing import List, Dict, Tuple
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
    - 1a, 1b, etc: Select specific letters in secondary panels
    """

    RIGHT: list[str] = ['a', 'e', 'i', 'o', 'u']

    TOP: list[str] = ["s", "t", "n", "r", "d", "l", "h"]

    LEFT: list[str] = ["c", "w", "m", "g", "y", "p", "f"]

    BOTTOM: list[str] = ["j", "b", "q", "k", "v", "z", "x"]

    COLORS: Dict[str, str] = {
        "background": "black",
        "border": "white",
        "text": "white",
        "highlight_1": "#3399ff33",  # Light blue with 20% opacity
        "highlight_2": "#3399ff66",  # Light blue with 40% opacity
        "highlight_3": "#3399ff99",  # Light blue with 60% opacity
        "highlight_4": "#3399ffcc",  # Light blue with 80% opacity
        "ring": "black",
        "confirm": "white",
        "cancel": "white",
        "side": "black"
    }

    FONT: Dict[str, int] = {
        'small': 8,
        'middle': 12,
        'large': 16
    }

    STATES: list[str] = ['MAIN', 'RIGHT', 'TOP', 'LEFT', 'BOTTOM', 'NUM']

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.state = 'MAIN'  # Current panel shown on the screen
        self.current_text = ''
        self.volume = 100  # from 0 to 100
        self.selection_counters = {
            "TOP": 0,
            "RIGHT": 0,
            "BOTTOM": 0,
            "LEFT": 0
        }
        
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
        self.compute_character_positions()
        self.setup_UI()
        
        # Start command input thread
        self.command_thread = threading.Thread(target=self.command_listener, daemon=True)
        self.command_thread.start()

    def compute_character_positions(self) -> None:
        """
        Precomputes positions for all characters and buttons.
        - MAIN mode: Clusters letters within 45-degree sectors.
        - HALF-CIRCLE mode: Two distinct views (left/right vs. top/bottom) with a 12.857° shift.
        - Special buttons (NUM, ⟲, ✔, X) use Cartesian coordinates.
        """
        center_x, center_y = 250, 250  # Center of the screen
        ring_radius = 100  # Distance from center for MAIN view
        half_radius = 100  # Slightly inner radius for HALF-CIRCLE mode

        ### --- MAIN VIEW: Cluster Letters in 45-degree Sectors --- ###
        sector_angles = {
            "RIGHT": (-22.5, 22.5),
            "TOP": (60, 120),
            "LEFT": (150, 210),
            "BOTTOM": (240, 300),
        }

        # Cluster letters inside 45-degree sectors
        for quadrant, chars in zip(sector_angles.keys(), [self.RIGHT, self.TOP, self.LEFT, self.BOTTOM]):
            start_angle, end_angle = sector_angles[quadrant]
            angle_step = (end_angle - start_angle) / len(chars)
            for i, char in enumerate(chars):
                angle = math.radians(start_angle + i * angle_step)
                self.character_positions[(char, "MAIN")] = (
                    center_x + ring_radius * math.cos(angle),
                    center_y - ring_radius * math.sin(angle)
                )

        ### --- HALF-CIRCLE VIEW: Two Variants for Even Spacing --- ###
        half_circle_divisions = 14
        shift_angle = 360 / (2 * half_circle_divisions)  # 12.857° shift

        for quadrant, chars in zip(["RIGHT", "TOP"], [self.RIGHT + self.LEFT, self.TOP + self.BOTTOM]):
            for i, char in enumerate(chars):
                base_angle = 180 - (i * (180 / half_circle_divisions))  # Base division
                if quadrant == "TOP":  # Shift for top/bottom alignment
                    base_angle += shift_angle
                angle = math.radians(base_angle)

                self.character_positions[(char, "HALF")] = (
                    center_x + half_radius * math.cos(angle),
                    center_y - half_radius * math.sin(angle)
                )

        ### --- NUMBERS: 11 Equally Spaced Positions in a Smaller Circle --- ###
        num_radius = 100
        for i, num in enumerate(self.numbers):
            angle = math.radians(360 * i / 11)
            self.character_positions[(num, "NUM")] = (
                center_x + num_radius * math.cos(angle),
                center_y - num_radius * math.sin(angle)
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

        # Draw NUM button (5)
        self.canvas.create_rectangle(num_x - 150, num_y - 150, num_x + 150, num_y + 150,
                                     outline=self.COLORS["border"], fill=self.COLORS["side"], width=3)
        self.canvas.create_text(num_x, num_y, text="NUM (5)", fill=self.COLORS["text"],
                                font=("Arial", self.FONT["middle"]))

        # Draw Return button (6)
        self.canvas.create_rectangle(return_x - 150, return_y - 150, return_x + 150, return_y + 150,
                                     outline=self.COLORS["border"], fill=self.COLORS["side"], width=3)
        self.canvas.create_text(return_x, return_y, text="⟲ (6)", fill=self.COLORS["text"],
                                font=("Arial", self.FONT["middle"]))

        # Draw Confirm button (8)
        self.canvas.create_rectangle(confirm_x - 150, confirm_y - 150, confirm_x + 150, confirm_y + 150,
                                     outline=self.COLORS["border"], fill=self.COLORS["side"], width=3)
        self.canvas.create_text(confirm_x, confirm_y, text="✔ (8)", fill=self.COLORS["confirm"],
                                font=("Arial", self.FONT["middle"]))

        # Draw Cancel/Delete button (7)
        self.canvas.create_rectangle(cancel_x - 150, cancel_y - 150, cancel_x + 150, cancel_y + 150,
                                     outline=self.COLORS["border"], fill=self.COLORS["side"], width=3)
        self.canvas.create_text(cancel_x, cancel_y, text="X (7)", fill=self.COLORS["cancel"],
                                font=("Arial", self.FONT["middle"]))

    def create_ring(self):
        """Draws the four-sectioned ring with arcs."""
        # Create the outer ring
        self.canvas.create_oval(100, 100, 400, 400, outline=self.COLORS["border"],
                                fill=self.COLORS["background"], width=3)

        # Create the four sections with their command numbers and store their IDs
        self.section_ids["TOP"] = self.canvas.create_arc(100, 100, 400, 400, start=45, extent=90, outline=self.COLORS["border"],
                                                       fill=self.COLORS["ring"], width=3, tags="TOP")
        self.canvas.create_text(250, 125, text="1", fill=self.COLORS["text"], font=("Arial", self.FONT["middle"]))
        
        self.section_ids["RIGHT"] = self.canvas.create_arc(100, 100, 400, 400, start=315, extent=90, outline=self.COLORS["border"],
                                                         fill=self.COLORS["ring"], width=3, tags="RIGHT")
        self.canvas.create_text(375, 250, text="2", fill=self.COLORS["text"], font=("Arial", self.FONT["middle"]))
        
        self.section_ids["BOTTOM"] = self.canvas.create_arc(100, 100, 400, 400, start=225, extent=90, outline=self.COLORS["border"],
                                                          fill=self.COLORS["ring"], width=3, tags="BOTTOM")
        self.canvas.create_text(250, 375, text="3", fill=self.COLORS["text"], font=("Arial", self.FONT["middle"]))
        
        self.section_ids["LEFT"] = self.canvas.create_arc(100, 100, 400, 400, start=135, extent=90, outline=self.COLORS["border"],
                                                        fill=self.COLORS["ring"], width=3, tags="LEFT")
        self.canvas.create_text(125, 250, text="4", fill=self.COLORS["text"], font=("Arial", self.FONT["middle"]))

        # Add letter indicators to MAIN view
        for section, letters in self.letters.items():
            letter_text = ", ".join(letters)
            if section == "TOP":
                self.canvas.create_text(250, 150, text=letter_text, fill=self.COLORS["text"], font=("Arial", self.FONT["small"]))
            elif section == "RIGHT":
                self.canvas.create_text(350, 250, text=letter_text, fill=self.COLORS["text"], font=("Arial", self.FONT["small"]))
            elif section == "BOTTOM":
                self.canvas.create_text(250, 350, text=letter_text, fill=self.COLORS["text"], font=("Arial", self.FONT["small"]))
            elif section == "LEFT":
                self.canvas.create_text(150, 250, text=letter_text, fill=self.COLORS["text"], font=("Arial", self.FONT["small"]))

    def create_circle(self):
        """Draws the central text display circle with a border."""
        self.canvas.create_oval(200, 200, 300, 300, outline=self.COLORS["border"],
                                fill=self.COLORS["background"], width=3)
        self.canvas.create_text(250, 250, text=self.current_text, font=("Arial", self.FONT["large"]),
                                fill=self.COLORS["text"], tags="text")

    def update_display(self, option: str) -> None:
        """
        Updates the GUI based on the selected mode.
        Modes:
        - 'MAIN'  -> Resets to four quadrants (default state).
        - 'RIGHT', 'TOP', 'LEFT', 'BOTTOM' -> Converts to two half-circles.
        - 'NUM'   -> Displays numeric keypad instead of letters.
        """
        # Reset all sections to default color
        for section in self.section_ids:
            self.canvas.itemconfig(self.section_ids[section], fill=self.COLORS["ring"])
        
        # Clear current character display
        self.canvas.delete("characters")
        
        # Update center text
        self.canvas.delete("text")
        self.canvas.create_text(250, 250, text=self.current_text, font=("Arial", self.FONT["large"]),
                                fill=self.COLORS["text"], tags="text")

        # Update display based on current state
        if option == "MAIN":
            # Reset to four-quadrant layout
            for section in self.section_ids:
                counter = self.selection_counters[section]
                if counter > 0:
                    highlight_color = self.COLORS[f"highlight_{counter}"]
                    self.canvas.itemconfig(self.section_ids[section], fill=highlight_color)
        
        elif option == "NUM":
            # Display numeric characters in circular layout
            for num in self.numbers:
                x, y = self.character_positions[(num, "NUM")]
                self.canvas.create_text(x, y, text=num, fill=self.COLORS["text"],
                                        font=("Arial", self.FONT["middle"]), tags="characters")
        
        elif option in ["RIGHT", "TOP", "LEFT", "BOTTOM"]:
            # Show selected section with secondary characters
            section = option
            chars = self.letters[section]
            
            # Display characters with subsection letters
            for i, char in enumerate(chars):
                x = 250 + 100 * math.cos(math.pi * (0.5 - i/(len(chars)-1)))
                y = 250 - 100 * math.sin(math.pi * (0.5 - i/(len(chars)-1)))
                
                self.canvas.create_text(x, y, text=f"{char} ({chr(97+i)})", fill=self.COLORS["text"],
                                        font=("Arial", self.FONT["large"]), tags="characters")
        
        self.state = option  # Update the state of the interface

    def select_option(self, option: str) -> None:
        """Handles selection of quadrants (LEFT, RIGHT, etc.) and updates state"""
        if option in self.selection_counters:
            # Increment the counter for this section
            self.selection_counters[option] += 1
            
            # If counter reaches 4, activate secondary panel
            if self.selection_counters[option] >= 4:
                self.selection_counters[option] = 0  # Reset counter
                self.state = option  # Activate secondary panel
                self.update_display(option)
            else:
                # Just update highlighting in MAIN state
                self.update_display("MAIN")
        else:
            self.state = option
            self.update_display(option)

    def add_character(self, char: str) -> None:
        """Adds the selected letter to current_text"""
        self.current_text += char
        self.state = "MAIN"  # Return to main state
        self.update_display("MAIN")

    def confirm_text(self) -> None:
        """Convert current text to speech and clear"""
        if self.current_text:
            self.tts(self.current_text)
            self.current_text = ""
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
            self.state = "MAIN"  # Reset state to main panel
            self.update_display("MAIN")
        elif button == "CONFIRM":
            self.confirm_text()
        elif button == "DELETE":
            if self.current_text:
                self.current_text = self.current_text[:-1]  # Delete last char
                self.update_display(self.state)

    def command_listener(self):
        """Listen for commands from the terminal"""
        print("\nWelcome to AAC Keyboard - Command Based")
        print("Commands:")
        print("1-4: Select main sections (top=1, right=2, bottom=3, left=4)")
        print("5: Switch to numbers/letters")
        print("6: Return to main panel")
        print("7: Delete last character")
        print("8: Confirm (text-to-speech)")
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
        if cmd.lower() == 'exit':
            self.root.quit()
            return
            
        # Check for main section commands (1-4)
        if cmd == '1':
            self.select_option("TOP")
        elif cmd == '2':
            self.select_option("RIGHT")
        elif cmd == '3':
            self.select_option("BOTTOM")
        elif cmd == '4':
            self.select_option("LEFT")
            
        # Check for corner commands (5-8)
        elif cmd == '5':
            self.handle_side_buttons("NUM")
        elif cmd == '6':
            self.handle_side_buttons("RETURN")
        elif cmd == '7':
            self.handle_side_buttons("DELETE")
        elif cmd == '8':
            self.handle_side_buttons("CONFIRM")
            
        # Check for secondary selection commands (e.g., 1a, 2b)
        elif re.match(r'^[1-4][a-g]$', cmd):
            section_num = int(cmd[0])
            char_index = ord(cmd[1]) - ord('a')
            
            # Map section number to section name
            section_map = {1: "TOP", 2: "RIGHT", 3: "BOTTOM", 4: "LEFT"}
            section = section_map.get(section_num)
            
            if section and self.state == section and char_index < len(self.letters[section]):
                # Add the selected character
                self.add_character(self.letters[section][char_index])
        else:
            print("Invalid command. Please use 1-8 or section+letter (e.g., 1a)")

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
        os.remove(file_path)


def main():
    root = tk.Tk()
    app = AAC_GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()