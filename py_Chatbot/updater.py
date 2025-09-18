import subprocess
import sys
import os
import pygame
import pygame.freetype
import math
import threading
import time
import ctypes

# --- Config ---
APP_NAME = "Project: lockchat - updater"
FONT_PATH = os.path.join("src", "fonts", "DejaVuSans.ttf")
if not os.path.isfile(FONT_PATH):
    print("Font missing: src/fonts/DejaVuSans.ttf")
    sys.exit(1)

# --- Pygame setup ---
pygame.init()
pygame.freetype.init()

WIDTH, HEIGHT = 360, 470
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption(APP_NAME)
font = pygame.freetype.Font(FONT_PATH, 18)

# --- Rounded corners (Windows only) ---
try:
    hwnd = pygame.display.get_wm_info()['window']
    ctypes.windll.user32.SetWindowRgn(hwnd,
        ctypes.windll.gdi32.CreateRoundRectRgn(0, 0, WIDTH, HEIGHT, 15, 15),
        True)
except Exception as e:
    print("Rounded window not supported on this OS.")

# --- Update logic ---
def run_checks_and_fixes(done_flag):
    # Add checks right there also this is beta.
    time.sleep(8)
    done_flag["done"] = True

# --- Main updater animation ---
def show_startup(screen):
    logo_path = os.path.join("src", "icons", "lockchatpng.png")
    logo = None
    if os.path.isfile(logo_path):
        logo = pygame.image.load(logo_path).convert_alpha()
        logo = pygame.transform.smoothscale(logo, (80, 80))

    phase = "checking"
    start_time = pygame.time.get_ticks()
    done_flag = {"done": False}

    # Start update check in background
    threading.Thread(target=run_checks_and_fixes, args=(done_flag,), daemon=True).start()

    running = True
    t = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed = pygame.time.get_ticks() - start_time
        screen.fill((30, 33, 36))

        # Bounce animation
        if logo:
            bounce_offset = int(math.sin(t * 0.08) * 8)  # bounce
            logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60 + bounce_offset))
            screen.blit(logo, logo_rect)

        # Text
        if phase == "checking":
            text_surface, _ = font.render("Checking for updates...", (220, 220, 220))
        else:
            text_surface, _ = font.render("Starting...", (220, 220, 220))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(text_surface, text_rect)

        # Phase handling
        if phase == "checking" and done_flag["done"]:
            phase = "starting"
            start_time = pygame.time.get_ticks()  # reset timer

        if phase == "starting" and elapsed > 1000:  # show Starting... 1s
            running = False

        pygame.display.flip()
        pygame.time.delay(7)
        t += 1

# --- Main ---
if __name__ == "__main__":
    show_startup(screen)
    pygame.quit()
    # Launch main.py if exists
    main_path = "main.py"
    if os.path.isfile(main_path):
        subprocess.run([sys.executable, main_path])
