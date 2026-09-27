## FakeOS
> A terminal-based fake operating system built in Python.

## Features
- CLI Interface
- Guest and Root Accounts (with password protection)
- Todo Application (persistent)
- Game (Guessr)
- Calculator
- **AI Math Solver (OpenRouter API)**
- Built-in Tools
- Filesystem (ZFS.py - fully implemented)

## Installation
```bash
git clone https://github.com/xarvynx/fakeos.git
cd fakeos
python3 core.py
```

## Commands
### Filesystem
- `pwd` - Print working directory
- `ls [path]` - List directory contents
- `cd [path]` - Change directory
- `mkdir <name>` - Create directory
- `touch <name> [content]` - Create file
- `write <name> <content>` - Write file (overwrites)
- `cat <name>` - Read file
- `rm <name>` - Remove file or empty directory
- `tree [path]` - Show directory tree
- `echo <text>` - Print text
- `echo <text> > file` - Write text to file (overwrite)
- `echo <text> >> file` - Append text to file

### System
- `whoami` - Show current user
- `su` - Switch to root (requires password)
- `clear` - Clear screen
- `time` - Show current time
- `neofetch` - Show system info
- `help` - Show this help
- `exit` - Shutdown FakeOS

### Apps
- `calc` - Basic calculator
- `guessr` - Number guessing game
- `todo` - To-Do list app (persistent)
- `math` / `solve` - AI-powered math solver (textbook format, requires OpenRouter API key)

### Math Solver Usage
```bash
guest@fakeos> math
🔑 OpenRouter API Key Required
Get one at: https://openrouter.ai/keys
Enter your OpenRouter API key: sk-or-v1-...
✅ Key saved securely (gitignored)

📐 Math Question: integrate x^2 * sin(x) from 0 to pi
🤔 Thinking...

**Given**: Evaluate ∫₀^π x² sin(x) dx
**Formula**: Integration by parts...
**Step 1**: ...
**Final Answer**: ▓▓▓ π² - 4 ▓▓▓
```

### Fun commands (doesn't affect host PC)
- `rm -rf /` - Fake system wipe (root only)
- `hacknasa` - Fake NASA hack

## Modules
- `core.py` - Main entry point, command dispatch
- `games.py` - Games (guessr)
- `utils.py` - Utilities (calc, rm_)
- `tools.py` - Tools (neofetch, hacknasa, time, todo, clear)
- `ZFS.py` - Virtual filesystem with JSON persistence
- `config.py` - Configuration (current user, password)
- `math_tool.py` - AI math solver using OpenRouter API

## Requirements
- Python 3.x
- Linux / Windows / macOS

## License
- MIT License