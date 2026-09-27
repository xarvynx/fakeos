#!/usr/bin/env python3
"""
visuals.py - Shared visual components for FakeOS
Colors, icons, animations, and UI utilities
"""

import time
import os
import sys

# ═══════════════════════════════════════════════════════════════
# COLOR & STYLE CONSTANTS (ANSI Escape Codes)
# ═══════════════════════════════════════════════════════════════

class C:
    # Reset
    R = '\033[0m'           # Reset all
    B = '\033[1m'           # Bold
    D = '\033[2m'           # Dim
    I = '\033[3m'           # Italic
    U = '\033[4m'           # Underline
    BL = '\033[5m'          # Blink
    RV = '\033[7m'          # Reverse
    
    # Foreground colors
    FG = {
        'black': '\033[30m', 'red': '\033[31m', 'green': '\033[32m',
        'yellow': '\033[33m', 'blue': '\033[34m', 'magenta': '\033[35m',
        'cyan': '\033[36m', 'white': '\033[37m',
        'bright_black': '\033[90m', 'bright_red': '\033[91m',
        'bright_green': '\033[92m', 'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m', 'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m', 'bright_white': '\033[97m',
    }
    
    # Background colors
    BG = {
        'black': '\033[40m', 'red': '\033[41m', 'green': '\033[42m',
        'yellow': '\033[43m', 'blue': '\033[44m', 'magenta': '\033[45m',
        'cyan': '\033[46m', 'white': '\033[47m',
    }


# Semantic color aliases
class S:
    # Status colors
    OK = C.FG['bright_green']
    WARN = C.FG['bright_yellow']
    ERR = C.FG['bright_red']
    INFO = C.FG['bright_cyan']
    DEBUG = C.FG['bright_black']
    
    # UI colors
    TITLE = C.FG['bright_magenta'] + C.B
    SUBTITLE = C.FG['bright_blue'] + C.B
    CMD = C.FG['bright_cyan'] + C.B
    ARG = C.FG['bright_yellow']
    PATH = C.FG['bright_blue']
    USER = C.FG['bright_green'] + C.B
    ROOT = C.FG['bright_red'] + C.B
    HOST = C.FG['bright_yellow'] + C.B
    PROMPT = C.FG['bright_magenta']
    DIM = C.FG['bright_black']
    
    # Box drawing
    BOX = C.FG['bright_black']
    ACCENT = C.FG['bright_cyan']


# ═══════════════════════════════════════════════════════════════
# NERD FONT ICONS
# ═══════════════════════════════════════════════════════════════

class ICON:
    # System
    OS = ''          # Linux logo
    KERNEL = ''      # Kernel
    BOOT = ''        # Power
    SHUTDOWN = ''    # Shutdown
    
    # User
    USER = ''        # User
    ROOT = ''        # Root (with different color)
    LOCK = ''        # Lock
    UNLOCK = ''      # Unlock
    KEY = ''         # Key
    
    # Filesystem
    DIR = ''         # Folder
    DIR_OPEN = ''    # Open folder
    FILE = ''        # File
    FILE_HIDDEN = '' # Hidden file
    SYMLINK = ''     # Symlink
    HOME = ''        # Home
    ROOT_DIR = ''    # Root filesystem
    
    # Actions
    SEARCH = ''      # Search
    ADD = ''         # Add
    REMOVE = ''      # Remove
    EDIT = ''        # Edit
    COPY = ''        # Copy
    MOVE = ''        # Move
    DELETE = ''      # Trash
    DOWNLOAD = ''    # Download
    UPLOAD = ''      # Upload
    
    # Status
    CHECK = ''       # Check
    CROSS = ''       # Cross
    WARNING = ''     # Warning
    INFO = ''        # Info
    QUESTION = ''    # Question
    LOADING = ''     # Loading
    SPINNER = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    
    # Apps
    TERMINAL = ''    # Terminal
    CALC = ''        # Calculator
    GAME = ''        # Game
    TODO = ''        # Clock/Task
    TIME = ''        # Time
    NEOFETCH = ''    # Neofetch
    HACK = ''        # Rocket/Hack
    MATH = ''        # Math
    SETTINGS = ''    # Settings
    
    # Arrow/Prompt
    ARROW = ''       # Right arrow
    ARROW2 = ''      # Right arrow 2
    PROMPT = '❯'      # Prompt
    PROMPT_ROOT = '❯' # Root prompt
    
    # Misc
    STAR = '★'        # Star
    SPARKLE = '✨'     # Sparkle
    GEAR = '⚙'        # Gear
    BOLT = '⚡'        # Bolt
    HEART = '♥'       # Heart


# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def colorize(text: str, fg: str = None, bg: str = None, bold: bool = False, dim: bool = False) -> str:
    """Apply ANSI colors to text."""
    result = ''
    if bold:
        result += C.B
    if dim:
        result += C.D
    if fg and fg in C.FG:
        result += C.FG[fg]
    if bg and bg in C.BG:
        result += C.BG[bg]
    result += text + C.R
    return result


def gradient(text: str, colors: list) -> str:
    """Apply gradient colors to text."""
    if not text:
        return ''
    result = ''
    step = len(text) / max(len(colors) - 1, 1)
    for i, ch in enumerate(text):
        idx = min(int(i / step), len(colors) - 1)
        result += C.FG.get(colors[idx], '') + ch
    return result + C.R


def typewriter(text: str, delay: float = 0.02, end: str = '\n'):
    """Print text with typewriter effect."""
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print(end, end='', flush=True)


def spinner_animation(message: str, duration: float = 1.5):
    """Show a spinning animation with message."""
    frames = ICON.SPINNER
    start = time.time()
    i = 0
    while time.time() - start < duration:
        frame = frames[i % len(frames)]
        print(f'\r{S.INFO}{frame} {message}{C.R}', end='', flush=True)
        time.sleep(0.08)
        i += 1
    print(f'\r{S.OK}{ICON.CHECK} {message}{C.R}')


def progress_bar(message: str, steps: int = 20, delay: float = 0.05):
    """Show a progress bar animation."""
    width = 30
    print(f'{S.INFO}{message}{C.R}')
    for i in range(steps + 1):
        filled = int(width * i / steps)
        bar = '█' * filled + '░' * (width - filled)
        percent = int(100 * i / steps)
        print(f'\r{S.DIM}[{S.ACCENT}{bar}{S.DIM}] {percent:3d}%{C.R}', end='', flush=True)
        time.sleep(delay)
    print(f'\r{S.OK}{ICON.CHECK} {message} [Done]{C.R}')


def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_box(title: str, content: list, width: int = 60, icon: str = ''):
    """Print a styled box with title and content."""
    title_str = f' {icon} {title} ' if icon else f' {title} '
    top = f'{S.BOX}╭{"─" * (width - 2)}╮{C.R}'
    mid = f'{S.BOX}│{C.R} {S.TITLE}{title_str:<{width - 4}}{C.R} {S.BOX}│{C.R}'
    sep = f'{S.BOX}├{"─" * (width - 2)}┤{C.R}'
    bottom = f'{S.BOX}╰{"─" * (width - 2)}╯{C.R}'
    
    print(top)
    print(mid)
    print(sep)
    for line in content:
        print(f'{S.BOX}│{C.R} {line:<{width - 4}} {S.BOX}│{C.R}')
    print(bottom)


def print_banner():
    """Print a simple FakeOS banner."""
    print(f'{S.TITLE}{ICON.OS} FakeOS v2.1.0{C.R}')
    print(f'{S.DIM}──────────────────────────────────────{C.R}')
    print()


# ═══════════════════════════════════════════════════════════════
# BOOT ANIMATION
# ═══════════════════════════════════════════════════════════════

def boot_animation(config_current_user='guest'):
    """Display the boot animation sequence."""
    clear_screen()
    
    print(f'{S.DIM}{"═" * 50}{C.R}')
    typewriter(f'{S.INFO}{ICON.BOOT} FakeOS Bootloader v2.1.0{C.R}', 0.01)
    time.sleep(0.2)
    
    boot_messages = [
        (f'{ICON.KERNEL} Initializing kernel...', 0.3),
        (f'{ICON.GEAR} Loading modules...', 0.2),
        (f'{ICON.DIR} Mounting filesystem...', 0.2),
        (f'{ICON.USER} Starting session...', 0.2),
        (f'{ICON.CHECK} Ready', 0.1),
    ]
    
    for msg, delay in boot_messages:
        spinner_animation(msg, delay)
    
    print()
    progress_bar('Finalizing', 10, 0.03)
    print()
    
    # Welcome banner
    print_banner()
    
    # Welcome message
    user_icon = ICON.ROOT if config_current_user == 'root' else ICON.USER
    user_color = S.ROOT if config_current_user == 'root' else S.USER
    print(f'{S.INFO}{ICON.INFO} Welcome, {user_color}{config_current_user}{S.INFO} {user_icon}{C.R}')
    print(f'{S.DIM}Type {S.CMD}help{S.DIM} for commands{C.R}')
    print()