import customtkinter as ctk
import tkinter as tk
import os, json, importlib, threading, time
from pathlib import Path
import logging
import math
import re

# --- Setup Logging ---
# Set up a basic logger to help with debugging and to report errors.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Constants ---
WINDOW_TITLE = "Modern Chatbot"
SETTINGS_FILE = Path("src/settings.json")
# Define default settings in a single place for clarity.
DEFAULT_SETTINGS = {
    "theme": "light",
    "text_size": 14,
    "version": "beta",
    "layout": "Medium"
}

# Define colors for the thinking state
THINKING_LABEL_COLOR = "#B0B0B0"
STOP_BUTTON_COLOR = "#FF5555"

# --- Settings Management Class ---
# Encapsulate settings logic within a class for better organization.
class AppSettings:
    """Manages application settings, including loading, saving, and state."""
    
    def __init__(self):
        # Use a dictionary to hold the current settings state.
        self.settings = DEFAULT_SETTINGS.copy()
        self.load_settings()
        self.apply_initial_settings()

    def load_settings(self):
        """Loads settings from a JSON file. Handles file not found or decode errors."""
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    # Update settings with loaded data, using defaults for any missing keys.
                    self.settings.update(data)
                    logging.info("Settings loaded successfully.")
        except json.JSONDecodeError:
            logging.error(f"Error decoding settings file at {SETTINGS_FILE}. Using default settings.")
        except IOError as e:
            logging.error(f"IOError: Could not read settings file. {e}")

    def save_settings(self):
        """Saves current settings to a JSON file."""
        try:
            SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=4)
            logging.info("Settings saved successfully.")
        except IOError as e:
            logging.error(f"IOError: Could not save settings file. {e}")

    def apply_initial_settings(self):
        """Applies theme and color settings on startup."""
        ctk.set_appearance_mode(self.settings.get("theme", DEFAULT_SETTINGS["theme"]))
        ctk.set_default_color_theme("blue")
        
    def get(self, key):
        """A simple getter for settings values."""
        return self.settings.get(key)
        
    def set(self, key, value):
        """A simple setter for settings values."""
        self.settings[key] = value

# --- Chatbot Logic ---
# Function to get the chatbot's response by importing a language file.
def get_chatbot_response(user_input: str, version_type: str) -> str:
    """Simulates a chatbot response based on the version type."""
    
    try:
        # Determine the language file to import
        if version_type == "beta":
            lang_module = importlib.import_module("src.langs.en")
        else: # Assumed 'Pre-beta'
            lang_module = importlib.import_module("src.langs.enTest")

        # Check for special symbols first, as requested by the user
        if re.search(r"[#\$%&\^]", user_input):
            return lang_module.get_reply("$code")
            
        return lang_module.get_reply(user_input)

    except ImportError:
        logging.error(f"Language file not found for version: {version_type}. Check src/langs directory.")
        return "Sorry, a required language file is missing."
    except Exception as e:
        logging.error(f"Error generating chatbot response: {e}")
        return "Sorry, something went wrong while processing your request."

# --- Settings Popup ---
class SettingsPopup(ctk.CTkToplevel):
    """A popup window for managing application settings."""

    def __init__(self, parent: ctk.CTk, settings: AppSettings):
        super().__init__(parent)
        self.parent = parent
        self.settings = settings
        self.title("Settings")
        self.geometry("300x400")
        self.resizable(False, False)

        # Ensure the popup is modal and stays on top
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the settings popup."""
        # Theme Section
        ctk.CTkLabel(self, text="Theme:").pack(padx=10, pady=(10, 0), anchor="w")
        self.theme_options = ["light", "dark", "system"]
        self.theme_menu = ctk.CTkOptionMenu(self, values=self.theme_options,
                                            command=self.set_theme)
        self.theme_menu.pack(padx=10, pady=5, fill="x")
        self.theme_menu.set(self.settings.get("theme"))

        # Text Size Section
        ctk.CTkLabel(self, text="Text Size:").pack(padx=10, pady=(10, 0), anchor="w")
        self.text_size_frame = ctk.CTkFrame(self)
        self.text_size_frame.pack(padx=10, pady=5, fill="x")
        self.text_size_frame.grid_columnconfigure(0, weight=1)

        self.text_size_entry = ctk.CTkEntry(self.text_size_frame)
        self.text_size_entry.insert(0, str(self.settings.get("text_size")))
        self.text_size_entry.grid(row=0, column=0, sticky="ew")

        self.apply_font_btn = ctk.CTkButton(self.text_size_frame, text="Apply", command=self.set_text_size)
        self.apply_font_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Version Section
        ctk.CTkLabel(self, text="Bot Version:").pack(padx=10, pady=(10, 0), anchor="w")
        self.version_options = ["beta", "Pre-beta"]
        self.version_menu = ctk.CTkOptionMenu(self, values=self.version_options, command=self.set_version)
        self.version_menu.pack(padx=10, pady=5, fill="x")
        self.version_menu.set(self.settings.get("version"))

        # Layout Section
        ctk.CTkLabel(self, text="Layout:").pack(padx=10, pady=(10, 0), anchor="w")
        self.layout_options = ["Medium", "Compact", "Modern"]
        self.layout_menu = ctk.CTkOptionMenu(self, values=self.layout_options, command=self.set_layout)
        self.layout_menu.pack(padx=10, pady=5, fill="x")
        self.layout_menu.set(self.settings.get("layout"))

    def set_theme(self, choice):
        """Updates the application theme and saves the setting."""
        ctk.set_appearance_mode(choice)
        self.settings.set("theme", choice)

    def set_text_size(self):
        """Updates the font size, handling invalid input."""
        try:
            size = int(self.text_size_entry.get())
            if 8 <= size <= 24:
                self.settings.set("text_size", size)
                self.parent.update_fonts(size)
            else:
                logging.warning("Text size must be between 8 and 24.")
        except ValueError:
            logging.error("Invalid text size. Please enter a number.")
    
    def set_version(self, choice):
        """Updates the chatbot version setting."""
        self.settings.set("version", choice)

    def set_layout(self, choice):
        """Updates the application layout."""
        self.settings.set("layout", choice)
        self.parent.apply_layout(choice)
        
    def on_closing(self):
        """Saves settings before closing the application."""
        self.destroy()

# --- Main App ---
class ModernChatApp(ctk.CTk):
    """Main application window for the modern chatbot."""
    
    def __init__(self, settings: AppSettings):
        super().__init__()
        self.settings = settings
        self.is_thinking = False
        self.stop_event = threading.Event()
        
        # Window setup
        self.title(WINDOW_TITLE)
        self.geometry("1280x800")
        self.minsize(800, 600)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configure grid layout to be responsive
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.settings_btn = ctk.CTkButton(self.sidebar_frame, text="⚙ Settings", command=self.open_settings)
        self.settings_btn.pack(side="bottom", padx=10, pady=10)

        # --- Chat Frame (now a scrollable frame) ---
        self.chat_frame = ctk.CTkFrame(self, corner_radius=0)
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_display_frame = ctk.CTkScrollableFrame(self.chat_frame, corner_radius=0)
        self.chat_display_frame.grid(row=0, column=0, sticky="nsew")

        # --- Input Frame ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=1, sticky="sew", padx=20, pady=20)
        self.input_frame.grid_columnconfigure(0, weight=1)

        # Bot status label
        self.status_label = ctk.CTkLabel(self.input_frame, text="", fg_color="transparent", text_color=THINKING_LABEL_COLOR)
        self.status_label.grid(row=0, column=0, sticky="w", padx=5)

        self.input_entry = ctk.CTkEntry(self.input_frame, font=("Arial", self.settings.get("text_size")))
        self.input_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(5, 0))
        self.input_entry.bind("<Return>", self.send_message)

        self.send_btn = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_btn.grid(row=1, column=1, pady=(5, 0))

        self.apply_layout(self.settings.get("layout"))

    def send_message(self, event=None):
        """Handles sending a message and displaying the response."""
        user_msg = self.input_entry.get().strip()
        if not user_msg:
            return
            
        self.input_entry.delete(0, "end")
        
        # Display user message
        self.insert_message(f"User: {user_msg}", "user")
        
        self.is_thinking = True
        self.stop_event.clear()
        self.set_thinking_ui(True)
        
        threading.Thread(target=self.get_bot_response_async, args=(user_msg,), daemon=True).start()

    def get_bot_response_async(self, user_msg):
        """Worker thread for getting the chatbot's response."""
        try:
            thinking_time = math.sin(len(user_msg)) * 2 / 1.2
            thinking_time = max(0.05, thinking_time)
            
            start_time = time.time()
            while time.time() - start_time < thinking_time:
                if self.stop_event.is_set():
                    self.after(0, self.handle_stopped_response)
                    return
                time.sleep(0.05)
            
            bot_reply = get_chatbot_response(user_msg, self.settings.get("version"))
            self.after(0, self.handle_bot_response, bot_reply)
        except Exception as e:
            logging.error(f"Error in bot response thread: {e}")
            self.after(0, self.handle_bot_response, "An error occurred.")
            
    def handle_bot_response(self, bot_reply):
        """Handles the bot's response after thinking is complete."""
        if not self.stop_event.is_set():
            # Check for the special "$code" format and extract the message.
            if bot_reply.startswith("Here's your provided testrun code:"):
                self.insert_message(f"Bot: {bot_reply}", "bot")
            else:
                self.insert_message(f"Bot: {bot_reply}", "bot")
            
            self.set_thinking_ui(False)

    def handle_stopped_response(self):
        """Handles the UI update when the response is stopped by the user."""
        self.insert_message("The response has stopped.", "bot")
        self.set_thinking_ui(False)

    def insert_message(self, text, sender):
        """
        Inserts a message into the chat display. Handles special formatting for
        bot messages containing code blocks.
        """
        # A simple regex to find all backtick-enclosed content.
        code_snippets = re.findall(r'`(.*?)`', text)
        
        # If there's a code snippet in a bot reply, handle it specially.
        if sender == "bot" and code_snippets:
            # Split the text by the backticks to get the parts
            parts = re.split(r'`(.*?)`', text, flags=re.DOTALL)
            
            # Create a frame for the message content
            message_frame = ctk.CTkFrame(self.chat_display_frame, fg_color="transparent")
            message_frame.pack(fill="x", pady=5)
            
            # Loop through the parts and add them to the frame
            for i, part in enumerate(parts):
                if i % 2 == 0:  # This is a normal text part
                    if part.strip(): # Avoid empty labels
                        text_label = ctk.CTkLabel(message_frame, text=part.strip(), font=("Arial", self.settings.get("text_size")), justify="left", wraplength=1000)
                        text_label.pack(fill="x", anchor="w", padx=10)
                else:  # This is a code snippet
                    # Get the current theme to set the code block color
                    current_theme = ctk.get_appearance_mode()
                    if current_theme == "Dark":
                        code_frame_color = "#404040"
                    else:
                        code_frame_color = "#F0F0F0"

                    code_frame = ctk.CTkFrame(message_frame, corner_radius=10, fg_color=code_frame_color)
                    code_frame.pack(fill="x", padx=15, pady=(5, 5))
                    
                    code_label = ctk.CTkLabel(code_frame, text=part, font=("Courier New", self.settings.get("text_size")), justify="left")
                    code_label.pack(fill="both", expand=True, padx=5, pady=5)
        else: # Standard message without a code block
            message_label = ctk.CTkLabel(self.chat_display_frame, text=text, font=("Arial", self.settings.get("text_size")), justify="left")
            message_label.pack(fill="x", pady=5, padx=10, anchor="w")
        
        # Scroll to the bottom
        self.chat_display_frame._parent_canvas.yview_moveto(1.0)

    def set_thinking_ui(self, is_thinking):
        """Updates the UI elements based on the thinking state."""
        self.is_thinking = is_thinking
        if is_thinking:
            self.status_label.configure(text="The bot is thinking...")
            self.send_btn.configure(text="Stop thinking", command=self.stop_thinking)
            self.input_entry.configure(state="disabled")
        else:
            self.status_label.configure(text="")
            self.send_btn.configure(text="Send", command=self.send_message)
            self.input_entry.configure(state="normal")

    def stop_thinking(self):
        """Sets the event to stop the bot's thinking process."""
        self.stop_event.set()

    def open_settings(self):
        """Opens the settings popup window."""
        SettingsPopup(self, self.settings)

    def update_fonts(self, size: int):
        """Updates the font size of the main UI elements."""
        # Need to update all labels in the chat display frame
        for widget in self.chat_display_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.configure(font=("Arial", size))
            elif isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkLabel):
                        child.configure(font=("Courier New", size))
        self.input_entry.configure(font=("Arial", size))

    def apply_layout(self, layout: str):
        """Applies layout settings to the UI."""
        font_size = self.settings.get("text_size")
        if layout == "Medium":
            pad, fsize = 10, font_size
        elif layout == "Compact":
            pad, fsize = 4, max(10, font_size - 2)
        elif layout == "Modern":
            pad, fsize = 15, font_size + 2
        else:
            pad, fsize = 10, font_size

        self.chat_frame.grid(padx=pad, pady=pad)
        self.input_frame.grid(padx=pad, pady=pad)
        self.update_fonts(fsize)
        
    def on_closing(self):
        """Saves settings before closing the application."""
        self.settings.save_settings()
        self.destroy()

# --- Run App ---
if __name__ == "__main__":
    app_settings = AppSettings()
    app = ModernChatApp(settings=app_settings)
    app.mainloop()
