import tkinter as tk
import time
from typing import List
import pygame
from gtts import gTTS
import os
import math


class AAC_GUI():
    """
    This is the main OOP program for creating the interactive GUI.
    The idea is to instantiate the appropriate panel for view when certain buttons are clicked.
    And the main frame gets initiated first in the while loop.
    The pygame module is used for the future development to incorporate various visual designs we created ourselves.
    """

    RIGHT: list[str] = ['a', 'e', 'i', 'o', 'u']

    TOP: list[str] = ["s", "t", "n", "r", "d", "l", "h"]

    LEFT: list[str] = ["c", "w", "m", "g", "y", "p", "f"]

    BOTTOM: list[str] = ["j", "b", "q", "k", "v", "z", "x"]

    COLORS: {str:str} = {
        "background": "black",
        "border": "dark blue",
        "highlight": "yellow",
        "text": "white",
        "ring": "steel blue",
        "confirm": "green",
        "cancel": "red",
        "side": "dark gray"
    }

    FONT: {str: int} = {
        'small': 8,
        'middle': 12,
        'large': 16
    }

    STATES: list[str] = ['MAIN', 'RIGHT', 'TOP', 'LEFT', 'BOTTOM', 'NUM']

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.state= 'MAIN'  # Current panel shown on the screen, to be communicated to the display
        self.current_text= ''
        self.volume = 100  # from 0 to 100
        self.hover_time = {}  # Track hover start time
        self.root.title("AAC Keyboard")
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
        self.compute_character_positions()
        self.setup_UI()

    def compute_character_positions(self) -> None:
        """
        Precomputes positions for all characters and buttons.
        - MAIN mode: Clusters letters within 45-degree sectors.
        - HALF-CIRCLE mode: Two distinct views (left/right vs. top/bottom) with a 12.857° shift.            - Special buttons (NUM, ⟲, ✔, X) use Cartesian coordinates.
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
            "NUM": (100, 100),  # Left
            "⟲": (400, 100),  # Right
            "✔": (400, 400),  # Bottom
            "X": (100, 400)  # Top
        }

        for button, pos in button_positions.items():
            self.character_positions[(button, "BUTTON")] = pos

    def setup_UI(self):
        """
        The four side buttons are at the lowest layer.
        On top of it is the ring, but it is in fact also a circle.
        On the topmost is the central circle for the text display.
        The region being covered will not be selected, only what's on the surface.
        """
        self.create_side()
        self.create_ring()
        self.create_circle()

    def create_side(self):
        """Creates the four side buttons with explicitly defined positions and colors."""
        # Define explicit positions for each button
        num_x, num_y = self.character_positions["NUM", "BUTTON"]
        return_x, return_y = self.character_positions["⟲", "BUTTON"]
        confirm_x, confirm_y = self.character_positions["✔", "BUTTON"]
        cancel_x, cancel_y = self.character_positions["X", "BUTTON"]

        # Draw NUM button
        self.canvas.create_rectangle(num_x - 150, num_y - 150, num_x + 150, num_y + 150,
                                     outline=self.COLORS["border"], fill=self.COLORS["side"], width=3)
        self.canvas.create_text(num_x, num_y, text="NUM", fill=self.COLORS["text"],
                                font=("Arial", self.FONT["middle"]))

        # Draw Return button
        self.canvas.create_rectangle(return_x - 150, return_y - 150, return_x + 150, return_y + 150,
                                     outline=self.COLORS["border"], fill=self.COLORS["side"], width=3)
        self.canvas.create_text(return_x, return_y, text="⟲", fill=self.COLORS["text"],
                                font=("Arial", self.FONT["middle"]))

        # Draw Confirm button
        self.canvas.create_rectangle(confirm_x - 150, confirm_y - 150, confirm_x + 150, confirm_y + 150,
                                     outline=self.COLORS["border"], fill=self.COLORS["side"], width=3)
        self.canvas.create_text(confirm_x, confirm_y, text="✔", fill=self.COLORS["confirm"],
                                font=("Arial", self.FONT["middle"]))

        # Draw Cancel button
        self.canvas.create_rectangle(cancel_x - 150, cancel_y - 150, cancel_x + 150, cancel_y + 150,
                                     outline=self.COLORS["border"], fill=self.COLORS["side"], width=3)
        self.canvas.create_text(cancel_x, cancel_y, text="X", fill=self.COLORS["cancel"],
                                font=("Arial", self.FONT["middle"]))

    def create_ring(self):
        """Draws the four-sectioned ring with arcs."""
        self.canvas.create_oval(100, 100, 400, 400, outline=self.COLORS["border"],
                                fill=self.COLORS["background"], width=3)

        self.canvas.create_arc(100, 100, 400, 400, start=315, extent=90, outline=self.COLORS["border"],
                               fill=self.COLORS["ring"], width=3)
        self.canvas.create_arc(100, 100, 400, 400, start=45, extent=90, outline=self.COLORS["border"],
                               fill=self.COLORS["ring"], width=3)
        self.canvas.create_arc(100, 100, 400, 400, start=135, extent=90, outline=self.COLORS["border"],
                               fill=self.COLORS["ring"], width=3)
        self.canvas.create_arc(100, 100, 400, 400, start=225, extent=90, outline=self.COLORS["border"],
                               fill=self.COLORS["ring"], width=3)


        #self.canvas.create_line(250, 100, 250, 400, fill=self.COLORS["border"], width=3)  # Vertical divider
        #self.canvas.create_line(100, 250, 400, 250, fill=self.COLORS["border"], width=3)  # Horizontal divider

        for char, (x, y) in self.character_positions.items():
            if "MAIN" in char:
                self.canvas.create_text(x, y, text=char[0], fill=self.COLORS["text"], font=("Arial", self.FONT["middle"]))

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
        self.canvas.delete("characters")  # Clear current ring display

        match option:
            case "MAIN":
                # Reset to four-quadrant layout
                for quadrant, chars in self.letters.items():
                    for char in chars:
                        x, y = self.character_positions[char]
                        self.canvas.create_text(x, y, text=char,
                                                fill="white", font=("Arial", self.FONT["small"]), tags="characters")

            case "NUM":
                # Display numeric characters in circular layout
                for num in self.numbers:
                    x, y = self.character_positions[num]
                    self.canvas.create_text(x, y, text=num, fill="white",
                                            font=("Arial", self.FONT["middle"]), tags="characters")

            case "RIGHT" | "TOP" | "LEFT" | "BOTTOM":
                # Convert four quadrants into two half-circles
                lower_chars = self.letters[option]  # Lowercase letters in selected quadrant
                upper_chars = [c.upper() for c in lower_chars]  # Mirror uppercase letters in opposite side

                for i, char in enumerate(lower_chars):
                    x, y = self.character_positions[char]
                    self.canvas.create_text(x, y, text=char,
                                            fill="white", font=("Arial", self.FONT["large"]), tags="characters")

                for i, char in enumerate(upper_chars):
                    mirrored_x, mirrored_y = self.character_positions[
                        char.lower()]  # Use lowercase position for mirroring
                    self.canvas.create_text(mirrored_x, mirrored_y, text=char,
                                            fill="white", font=("Arial", self.FONT["large"]), tags="characters")

        self.state = option  # Update the state of the interface

    def select_option(self, option: str) -> None:
        """Handles selection of quadrants (LEFT, RIGHT, etc.) and updates state"""
        self.state = option
        self.update_display(option)

    def add_character(self, char: str) -> None:
        """Adds the selected letter to current_text"""
        self.current_text += char
        self.update_display(self.state)

    def confirm_text(self) -> None:
        self.tts(self.current_text)
        self.current_text = ""
        self.state = self.STATES[0]
        self.update_display(self.state)

    def adjust_volume(self, increment: int) -> None:
        """We ignore this function for now since it will be interfaced with the Pi hardware in the future"""
        pass

    def handle_side_buttons(self, button: str) -> None:
        """
        Handles side button clicks including Confirm, Cancel, Number Toggle, and Return.
        """
        match button:
            case "NUM":
                    self.update_display("NUM")
            case "⟲":
                self.state = "MAIN"  # Reset state to main panel
                self.update_display("MAIN")
            case "✔" | "X":
                self.handle_confirm_cancel(button)

    def handle_confirm_cancel(self, action: str) -> None:
        """
        Handles both Confirm ('✔') and Cancel ('X') button clicks.
        Determines whether to delete a character, say 'Yes'/'No', or play text-to-speech.
        """
        match action:
            case "✔":
                if not self.current_text:
                    self.current_text = "Yes"
                elif self.current_text[-1] == " ":
                    self.confirm_text()  # Speak and clear text
                    self.current_text = ""
                else:
                    self.current_text += " "  # Add space before confirming
            case "X":
                if not self.current_text:
                    self.current_text = "No"
                else:
                    self.current_text = self.current_text[:-1]  # Delete last char
        self.update_display(self.state)

    def on_clicked(self, event):
        """
        Substitute for the hover function, will be implemented with the IMU input in the future
        """
        pass

    def start_hover(self, option: str):
        """Gradually brightens the hovered option over 2 seconds. If fully highlighted, auto-selects the option."""
        self.hover_time[option] = time.time()

        def check_hover():
            elapsed = time.time() - self.hover_time.get(option, 0)
            if elapsed >= 2:
                self.select_option(option)
            else:
                brightness = int(255 * (elapsed / 2))
                self.canvas.itemconfig(option, fill=f"#{brightness:02x}{brightness:02x}00")
                self.root.after(100, check_hover)

        check_hover()

    def reset_hover(self, option: str):
        """If cursor leaves before 2 seconds, resets brightness"""
        if option in self.hover_time:
            del self.hover_time[option]
        self.canvas.itemconfig(option, fill=self.COLORS["text"])

    @staticmethod
    def tts(input_text: str) -> None:
        """Converts text to speech using gTTS and plays it with pygame."""
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
    AAC_GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
