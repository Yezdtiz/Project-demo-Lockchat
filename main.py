import pygame
import os
import importlib
import pygame.freetype 
import json

# --- Initialization ---
pygame.init()
pygame.freetype.init()
wintitle = "Project: lockchat - demo"
winicon_path = os.path.join("src", "icons", "lockchatpng.png")
if os.path.isfile(winicon_path):
    winicon = pygame.image.load(winicon_path)
    pygame.display.set_icon(winicon)

# Initial and minimum window sizes
initial_width = 1280
initial_height = 800
min_width = 800
min_height = 600

# Create the screen and set the window title and resizable flag
screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
pygame.display.set_caption(wintitle)

# --- Check for 'src', 'langs', and 'fonts' folders and files ---
if not os.path.isdir("src/langs"):
    print("Error: The 'src/langs' directory was not found. Please check your folder structure.")
    pygame.quit()
    exit()

if not os.path.isdir("src/fonts"):
    print("Error: The 'src/fonts' directory was not found. Please create it and add a font file.")
    pygame.quit()
    exit()

font_path = os.path.join("src", "fonts", "DejaVuSans.ttf")
if not os.path.isfile(font_path):
    print("Error: DejaVuSans.ttf was not found in the 'src/fonts' directory. Please download it and place it there.")
    pygame.quit()
    exit()

# --- Theme Definitions ---
light_theme = {
    "background": (240, 242, 245),
    "chat_bg": (255, 255, 255),
    "text_color": (30, 30, 30),
    "sidebar_color": (245, 247, 250),
    "accent_color": (162, 210, 228),
    "accent_hover": (160, 205, 210),
    "shadow_color": (0, 0, 0, 80),
    "outline_color": (162, 210, 228)
}

dark_theme = {
    "background": (30, 33, 36),
    "chat_bg": (47, 50, 56),
    "text_color": (220, 220, 220),
    "sidebar_color": (20, 23, 26),
    "accent_color": (0, 101, 137),
    "accent_hover": (14, 123, 162),
    "shadow_color": (0, 0, 0, 150),
    "outline_color": (0, 101, 137)
}

# --- Settings and UI state ---
settings_file = "src/settings.json"
current_theme_name = "light"
font_size = 24
text_sizes = [20, 24, 26, 30, 32]  # Add 20 to the list
settings_visible = False
dragging_slider = False
current_theme = light_theme

# --- UI Color Variables (Dynamic based on theme) ---
BACKGROUND_COLOR = current_theme["background"]
CHAT_BACKGROUND = current_theme["chat_bg"]
TEXT_COLOR = current_theme["text_color"]
SIDEBAR_COLOR = current_theme["sidebar_color"]
ACCENT_COLOR = current_theme["accent_color"]
ACCENT_HOVER = current_theme["accent_hover"]
SHADOW_COLOR = current_theme["shadow_color"]
OUTLINE_COLOR = current_theme["outline_color"]

# --- Fonts ---
text_font = pygame.freetype.Font(font_path, font_size)
ui_font = pygame.freetype.Font(font_path, 16)

# --- UI Outline Settings ---
outline_thickness = 2
outline_color = (88, 101, 242)

# --- Functions to manage settings ---
def set_theme(theme_name):
    """Sets the UI colors based on the chosen theme."""
    global current_theme, BACKGROUND_COLOR, CHAT_BACKGROUND, TEXT_COLOR, SIDEBAR_COLOR, ACCENT_COLOR, ACCENT_HOVER, SHADOW_COLOR, current_theme_name, OUTLINE_COLOR
    
    current_theme_name = theme_name
    if theme_name == "dark":
        current_theme = dark_theme
    else:
        current_theme = light_theme
    
    BACKGROUND_COLOR = current_theme["background"]
    CHAT_BACKGROUND = current_theme["chat_bg"]
    TEXT_COLOR = current_theme["text_color"]
    SIDEBAR_COLOR = current_theme["sidebar_color"]
    ACCENT_COLOR = current_theme["accent_color"]
    ACCENT_HOVER = current_theme["accent_hover"]
    SHADOW_COLOR = current_theme["shadow_color"]
    OUTLINE_COLOR = current_theme["outline_color"]

def set_text_size(size):
    """Sets the font size and recreates the font object."""
    global font_size, text_font
    font_size = size
    text_font = pygame.freetype.Font(font_path, font_size)

def set_language(lang_code):
    """Sets the language for chatbot replies."""
    global current_lang
    current_lang = lang_code

def set_version(version_type):
    """Sets the chatbot version and updates the language code."""
    global current_version_type, current_lang
    current_version_type = version_type
    # Map version type to a specific language file
    if current_version_type == "beta":
        current_lang = "en"
    elif current_version_type == "pre-beta":
        current_lang = "enTest"
    
def save_settings():
    """Saves the current settings to a JSON file."""
    settings_data = {
        "theme": current_theme_name,
        "text_size": font_size,
        "version": current_version_type  # Save the new setting
    }
    with open(settings_file, "w") as f:
        json.dump(settings_data, f)

def load_settings():
    """Loads settings from a JSON file if it exists."""
    global current_theme_name, font_size, current_version_type
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings_data = json.load(f)
                current_theme_name = settings_data.get("theme", "light")
                font_size = settings_data.get("text_size", 24)
                current_version_type = settings_data.get("version", "beta") # Load new setting
                set_theme(current_theme_name)
                set_text_size(font_size)
                set_version(current_version_type) # Apply the version setting
        except json.JSONDecodeError:
            print("Error loading settings.json. Using default settings.")
    else:
        set_theme("light")
        set_text_size(24)
        set_version("beta") # Default to beta if no file exists

# New variable for the version type
current_version_type = "beta"
current_lang = "en"

# Load settings at the start
load_settings()

# --- Key Repeat Settings ---
pygame.key.set_repeat(500, 50) 

# --- UI Element Dimensions and Dynamic Variables ---
# Proportional sizing variables
sidebar_width_ratio_collapsed = 0.05
sidebar_width_ratio_expanded = 0.2
sidebar_animation_speed = 30 # Adjusted for a better feel without dt
chat_area_padding = 20

# Initial values
current_sidebar_width = initial_width * sidebar_width_ratio_collapsed

# Chat and input variables
chat_history = []
input_text = ""
scroll_offset = 0 # Variable to control chat history scrolling
scroll_speed = 50 # Speed of scrolling
message_spacing = 15 # Space between messages
group_spacing = 30 # Space between user/bot groups

# Scrollbar variables
dragging_scrollbar = False
scrollbar_handle_rect = None
scroll_y_start = 0

# Cursor blink variables
cursor_visible = True
cursor_blink_rate = 500
last_cursor_toggle = pygame.time.get_ticks()

# Settings Popup Animation variables
popup_width = 400
popup_height = 300
popup_animation_speed = 0.25
popup_scale = 0.0
popup_opacity = 0
popup_target_scale = 0.0

# --- Helper function for chatbot replies ---
def get_chatbot_response(user_input):
    """Loads language-specific replies and finds a matching response."""
    # This logic has been simplified since lang switching is handled by settings now
    
    try:
        # Import the language module based on the current_lang variable
        lang_module = importlib.import_module(f"src.langs.{current_lang}")
        response = lang_module.get_reply(user_input)
        return response
    except ImportError:
        # This error is handled here because it's a global issue, not language-specific
        return f"Sorry, the language file for '{current_lang}' was not found. Please make sure the file exists in the 'src/langs' folder."

def draw_outline(surface, rect, color, thickness):
    """Draws a rounded rectangle outline."""
    pygame.draw.rect(surface, color, rect, thickness, border_radius=10)

def draw_settings_popup():
    """Draws the settings popup with themes, text size, and close button."""
    screen_width, screen_height = screen.get_size()
    
    # Animate pop-up scale and opacity
    global popup_scale, popup_opacity
    if settings_visible:
        popup_scale = min(1.0, popup_scale + popup_animation_speed)
        popup_opacity = min(255, popup_opacity + 25)
    else:
        popup_scale = max(0.0, popup_scale - popup_animation_speed)
        popup_opacity = max(0, popup_opacity - 25)
        
    if popup_scale <= 0 and not settings_visible:
        return None, None, None, None, None, None

    # Calculate animated popup size and position
    current_popup_width = popup_width * popup_scale
    current_popup_height = popup_height * popup_scale
    popup_x = (screen_width - current_popup_width) / 2
    popup_y = (screen_height - current_popup_height) / 2
    
    # Main popup rectangle
    popup_rect = pygame.Rect(popup_x, popup_y, current_popup_width, current_popup_height)
    pygame.draw.rect(screen, CHAT_BACKGROUND, popup_rect, border_radius=15)
    draw_outline(screen, popup_rect, OUTLINE_COLOR, outline_thickness)


    if popup_scale < 1.0:
        return None, None, None, None, None, None # Don't draw contents until fully scaled

    # --- Draw Pop-up Contents (only when fully scaled) ---
    
    # Title "Settings" centered
    settings_title_surface, _ = text_font.render("Settings", TEXT_COLOR, size=24)
    settings_title_rect = settings_title_surface.get_rect(center=(popup_rect.centerx, popup_y + 40))
    screen.blit(settings_title_surface, settings_title_rect)

    # Close button (cross)
    close_button_rect = pygame.Rect(popup_x + popup_width - 35, popup_y + 10, 25, 25)
    ui_font.render_to(screen, close_button_rect, "X", TEXT_COLOR, size=24)

    # Theme section
    item_spacing = 20
    ui_padding = 30
    theme_y = popup_y + 80
    theme_title_surface, _ = ui_font.render("Theme:", TEXT_COLOR)
    screen.blit(theme_title_surface, (popup_x + ui_padding, theme_y))

    theme_buttons = {
        "system": pygame.Rect(popup_x + 100, theme_y, 80, 30),
        "dark": pygame.Rect(popup_x + 190, theme_y, 80, 30),
        "light": pygame.Rect(popup_x + 280, theme_y, 80, 30)
    }

    for name, rect in theme_buttons.items():
        color = ACCENT_COLOR if name == current_theme_name else SIDEBAR_COLOR
        text_color = CHAT_BACKGROUND if name == current_theme_name else TEXT_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=5)
        button_text, _ = ui_font.render(name.capitalize(), text_color, size=16)
        button_text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, button_text_rect)

    # Version section
    version_y = theme_y + 30 + item_spacing
    version_title_surface, _ = ui_font.render("Version:", TEXT_COLOR)
    screen.blit(version_title_surface, (popup_x + ui_padding, version_y))

    version_buttons = {
        "beta": pygame.Rect(popup_x + 100, version_y, 80, 30),
        "pre-beta": pygame.Rect(popup_x + 190, version_y, 100, 30)
    }

    for name, rect in version_buttons.items():
        color = ACCENT_COLOR if name == current_version_type else SIDEBAR_COLOR
        text_color = CHAT_BACKGROUND if name == current_version_type else TEXT_COLOR
        pygame.draw.rect(screen, color, rect, border_radius=5)
        button_text, _ = ui_font.render(name.capitalize(), text_color, size=16)
        button_text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, button_text_rect)

    # Text size section
    text_size_y = version_y + 30 + item_spacing
    text_size_title_surface, _ = ui_font.render("Text Size:", TEXT_COLOR)
    screen.blit(text_size_title_surface, (popup_x + ui_padding, text_size_y))

    # Slider background line
    slider_line_rect = pygame.Rect(popup_x + 120, text_size_y + 15, 200, 5)
    pygame.draw.line(screen, TEXT_COLOR, slider_line_rect.midleft, slider_line_rect.midright, 2)
    
    # Calculate slider handle position
    size_index = text_sizes.index(font_size)
    slider_x = slider_line_rect.left + size_index * (slider_line_rect.width / (len(text_sizes) - 1))
    
    # Slider handle
    slider_handle_rect = pygame.Rect(0, 0, 15, 15)
    slider_handle_rect.center = (slider_x, slider_line_rect.centery)
    pygame.draw.circle(screen, ACCENT_COLOR, slider_handle_rect.center, 8)
    
    # Text size labels
    for i, size in enumerate(text_sizes):
        label_x = slider_line_rect.left + i * (slider_line_rect.width / (len(text_sizes) - 1))
        label_text, _ = ui_font.render(str(size), TEXT_COLOR, size=12)
        label_rect = label_text.get_rect(center=(label_x, slider_line_rect.bottom + 10))
        screen.blit(label_text, label_rect)
        
    return close_button_rect, theme_buttons, version_buttons, slider_handle_rect, slider_line_rect

# --- Main Game Loop ---
clock = pygame.time.Clock() 
running = True
while running:
    clock.tick(60) # Capping the frame rate at 60 FPS
    current_time = pygame.time.get_ticks()
    screen_width, screen_height = screen.get_size()
    
    # Calculate UI element dimensions based on current window size
    sidebar_width_collapsed = screen_width * sidebar_width_ratio_collapsed
    sidebar_width_expanded = screen_width * sidebar_width_ratio_expanded
    
    sidebar_rect = pygame.Rect(0, 0, current_sidebar_width, screen_height)
    settings_button_rect = pygame.Rect(0, screen_height - 60, current_sidebar_width, 60)
    chat_area_rect = pygame.Rect(current_sidebar_width + chat_area_padding, chat_area_padding, screen_width - current_sidebar_width - (2 * chat_area_padding), screen_height - 100 - (2 * chat_area_padding))
    input_box_rect = pygame.Rect(current_sidebar_width + chat_area_padding, screen_height - 60 - chat_area_padding, screen_width - current_sidebar_width - (2 * chat_area_padding), 40)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_settings()
            running = False

        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = max(event.w, min_width), max(event.h, min_height)
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            current_sidebar_width = min(current_sidebar_width, screen_width * sidebar_width_ratio_expanded)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if settings_visible and popup_scale >= 1.0:
                    close_button_rect, theme_buttons, version_buttons, slider_handle_rect, slider_line_rect = draw_settings_popup()
                    
                    if close_button_rect and close_button_rect.collidepoint(mouse_pos):
                        settings_visible = False
                    
                    if theme_buttons:
                        for name, rect in theme_buttons.items():
                            if rect.collidepoint(mouse_pos):
                                set_theme(name)

                    if version_buttons:
                        for name, rect in version_buttons.items():
                            if rect.collidepoint(mouse_pos):
                                set_version(name)
                    
                    if slider_handle_rect and slider_handle_rect.collidepoint(mouse_pos):
                        dragging_slider = True
                
                elif settings_button_rect.collidepoint(mouse_pos):
                    settings_visible = True
                
                # Handle mouse down on scrollbar
                if scrollbar_handle_rect and scrollbar_handle_rect.collidepoint(mouse_pos):
                    dragging_scrollbar = True
                    # Store the starting position of the mouse relative to the handle
                    scroll_y_start = mouse_pos[1] - scrollbar_handle_rect.y

            # Handle scrolling with the mouse wheel
            if chat_area_rect.collidepoint(event.pos):
                if event.button == 4: # Scroll up
                    scroll_offset -= scroll_speed
                elif event.button == 5: # Scroll down
                    scroll_offset += scroll_speed

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_slider = False
                # Stop dragging the scrollbar
                dragging_scrollbar = False

        if event.type == pygame.MOUSEMOTION:
            if dragging_slider and settings_visible:
                mouse_x, mouse_y = event.pos
                _, _, _, _, slider_line_rect = draw_settings_popup()
                
                if slider_line_rect:
                    clamped_x = max(slider_line_rect.left, min(mouse_x, slider_line_rect.right))
                    
                    closest_size = None
                    min_dist = float('inf')
                    for i, size in enumerate(text_sizes):
                        snap_x = slider_line_rect.left + i * (slider_line_rect.width / (len(text_sizes) - 1))
                        dist = abs(clamped_x - snap_x)
                        if dist < min_dist:
                            min_dist = dist
                            closest_size = size
                    
                    if closest_size and closest_size != font_size:
                        set_text_size(closest_size)
            
            # Handle dragging the scrollbar
            if dragging_scrollbar:
                mouse_y = event.pos[1]
                # Calculate the new top position of the scrollbar handle
                new_handle_y = mouse_y - scroll_y_start
                
                # Clamp the new handle position within the chat area
                clamped_handle_y = max(chat_area_rect.top, min(new_handle_y, chat_area_rect.bottom - scrollbar_handle_rect.height))
                
                # Calculate the new scroll offset based on the handle's position
                scrollbar_range = chat_area_rect.height - scrollbar_handle_rect.height
                if scrollbar_range > 0:
                    scroll_ratio = (clamped_handle_y - chat_area_rect.top) / scrollbar_range
                    chat_content_height = 0
                    for speaker, text in chat_history:
                        _, text_rect = text_font.render(f"{speaker}: {text}")
                        chat_content_height += text_rect.height + message_spacing
                        if speaker == "Bot":
                            chat_content_height += group_spacing
                    
                    max_scroll = max(0, chat_content_height - chat_area_rect.height + 20)
                    scroll_offset = max_scroll * scroll_ratio
                    

        if not settings_visible or (settings_visible and popup_scale < 1.0):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                    try:
                        import pyperclip
                        input_text += pyperclip.paste()
                    except (ImportError, pygame.error):
                        print("To enable paste, please install the 'pyperclip' library.")
                elif event.key == pygame.K_RETURN:
                    if input_text:
                        chat_history.append(("User", input_text))
                        bot_response = get_chatbot_response(input_text)
                        chat_history.append(("Bot", bot_response))
                        
                        input_text = ""
                        # Scroll to the bottom on new message
                        chat_content_height = 0
                        for speaker, text in chat_history:
                            _, text_rect = text_font.render(f"{speaker}: {text}")
                            chat_content_height += text_rect.height + message_spacing
                            if speaker == "Bot":
                                chat_content_height += group_spacing
                        
                        max_scroll = max(0, chat_content_height - chat_area_rect.height + 20)
                        scroll_offset = max_scroll

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif not (event.mod & pygame.KMOD_CTRL):
                    input_text += event.unicode
    
    # --- Update UI State based on current window size ---
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Animate sidebar
    if sidebar_rect.collidepoint(mouse_x, mouse_y):
        if current_sidebar_width < sidebar_width_expanded:
            current_sidebar_width += sidebar_animation_speed
    else:
        if current_sidebar_width > sidebar_width_collapsed:
            current_sidebar_width -= sidebar_animation_speed
    
    if input_box_rect.collidepoint(mouse_x, mouse_y) and not settings_visible:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    if current_time - last_cursor_toggle > cursor_blink_rate:
        cursor_visible = not cursor_visible
        last_cursor_toggle = current_time

    # --- Drawing the UI ---
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(screen, SIDEBAR_COLOR, sidebar_rect)
    draw_outline(screen, sidebar_rect, OUTLINE_COLOR, outline_thickness)
    
    button_color = ACCENT_HOVER if settings_button_rect.collidepoint(mouse_x, mouse_y) else ACCENT_COLOR
    pygame.draw.rect(screen, button_color, settings_button_rect)
    
    # Apply outline on hover
    if settings_button_rect.collidepoint(mouse_x, mouse_y):
        draw_outline(screen, settings_button_rect, OUTLINE_COLOR, outline_thickness)
    
    if current_sidebar_width > sidebar_width_collapsed + sidebar_animation_speed:
        settings_text_surface, _ = text_font.render("Settings", CHAT_BACKGROUND)
        settings_text_rect = settings_text_surface.get_rect(center=settings_button_rect.center)
        screen.blit(settings_text_surface, settings_text_rect)
    else:
        settings_text_surface, _ = text_font.render("⚙", CHAT_BACKGROUND, size=24)
        settings_text_rect = settings_text_surface.get_rect(center=settings_button_rect.center)
        screen.blit(settings_text_surface, settings_text_rect)
        
    pygame.draw.rect(screen, CHAT_BACKGROUND, chat_area_rect, border_radius=10)
    # Apply outline to chat area
    draw_outline(screen, chat_area_rect, OUTLINE_COLOR, outline_thickness)

    # Drawing the chat history with a scrollable view
    chat_content_height = 0
    # First pass to calculate total content height
    for speaker, text in chat_history:
        _, text_rect = text_font.render(f"{speaker}: {text}")
        chat_content_height += text_rect.height + message_spacing
        if speaker == "Bot":
            chat_content_height += group_spacing

    # Clamp the scroll offset to prevent scrolling past the content
    max_scroll = max(0, chat_content_height - chat_area_rect.height + 20)
    scroll_offset = max(0, min(scroll_offset, max_scroll))

    # Create a sub-surface for the chat area to manage clipping
    chat_surface = pygame.Surface(chat_area_rect.size, pygame.SRCALPHA)
    y_offset = -scroll_offset + 10 # Start with the scroll offset applied

    for speaker, text in chat_history:
        text_surface, text_rect = text_font.render(f"{speaker}: {text}", TEXT_COLOR)
        
        # Only draw if the message is within the visible area
        if y_offset + text_rect.height >= 0 and y_offset <= chat_area_rect.height:
            chat_surface.blit(text_surface, (10, y_offset))
            
        y_offset += text_rect.height + message_spacing
        if speaker == "Bot":
            y_offset += group_spacing

    screen.blit(chat_surface, (chat_area_rect.x, chat_area_rect.y))
    
    # Draw a scrollbar if the content overflows
    scrollbar_handle_rect = None # Reset handle rect each frame
    if chat_content_height > chat_area_rect.height:
        scrollbar_width = 10
        scrollbar_x = chat_area_rect.right - scrollbar_width - 5
        
        # Calculate scrollbar handle height and position
        scrollbar_height_ratio = chat_area_rect.height / chat_content_height
        scrollbar_handle_height = chat_area_rect.height * scrollbar_height_ratio
        
        # Clamp handle height to a minimum for usability
        min_handle_height = 20
        scrollbar_handle_height = max(min_handle_height, scrollbar_handle_height)
        
        scrollbar_y_ratio = scroll_offset / max_scroll if max_scroll > 0 else 0
        scrollbar_handle_y = chat_area_rect.top + (chat_area_rect.height - scrollbar_handle_height) * scrollbar_y_ratio
        
        scrollbar_handle_rect = pygame.Rect(scrollbar_x, scrollbar_handle_y, scrollbar_width, scrollbar_handle_height)
        pygame.draw.rect(screen, ACCENT_COLOR, scrollbar_handle_rect, border_radius=5)
    
    pygame.draw.rect(screen, CHAT_BACKGROUND, input_box_rect, border_radius=10)
    # Apply outline to input box
    draw_outline(screen, input_box_rect, OUTLINE_COLOR, outline_thickness)
    
    input_text_surface, input_text_rect = text_font.render(input_text, TEXT_COLOR)
    screen.blit(input_text_surface, (input_box_rect.x + 10, input_box_rect.y + 10))

    if cursor_visible and input_box_rect.collidepoint(mouse_x, mouse_y) and not settings_visible:
        cursor_pos_x = input_box_rect.x + 10 + input_text_rect.width
        cursor_rect = pygame.Rect(cursor_pos_x, input_box_rect.y + 10, 2, input_text_rect.height)
        pygame.draw.rect(screen, TEXT_COLOR, cursor_rect)
    

    draw_settings_popup()

    pygame.display.flip()

pygame.quit()