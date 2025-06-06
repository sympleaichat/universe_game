# Universe Game MCP Server

An enhanced Conway's Game of Life simulation that runs as an MCP (Model Context Protocol) server for Claude Desktop. Watch cellular automata evolve with beautiful ASCII visualizations, pattern detection, and detailed analytics!

❗**This game uses a lot of tokens. Please be careful when increasing the number of turns.**:❗

## Features

- 🌌 **Conway's Game of Life Simulation**: Classic cellular automaton on a 20x20 grid
- 🎨 **Beautiful ASCII Visualizations**: Detailed displays every 10 turns with statistics
- 🔍 **Pattern Detection**: Automatically detects oscillators, still lifes, and gliders
- 📊 **Real-time Analytics**: Population tracking, birth/death statistics, stability analysis
- 🎮 **Interactive Controls**: Manual cell manipulation and pattern insertion
- 🚀 **Pre-built Patterns**: Add classic patterns like gliders, blinkers, blocks, and beacons

## Quick Start for Non-Technical Users

### Prerequisites

You'll need Python installed on your computer. Here's how to check and install:

#### Windows
1. Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
2. Type `python --version` and press Enter
3. If you see a version number (like `Python 3.11.0`), you're good to go!
4. If not, download Python from [python.org](https://www.python.org/downloads/) and install it
   - ⚠️ **Important**: Check "Add Python to PATH" during installation

#### Mac
1. Open Terminal (press `Cmd + Space`, type "Terminal", press Enter)
2. Type `python3 --version` and press Enter
3. If you see a version number, you're ready!
4. If not, install Python from [python.org](https://www.python.org/downloads/) or use Homebrew:
   ```bash
   brew install python
   ```

### Installation Steps

1. **Download the Game**
   - Download or clone this repository to your computer
   - Extract the files if downloaded as ZIP
   - Note the folder path (you'll need it later)

2. **Install Required Libraries**
   
   **Windows:**
   ```cmd
   pip install numpy
   ```
   
   **Mac:**
   ```bash
   pip3 install numpy
   ```

3. **Configure Claude Desktop**
   
   Find your Claude Desktop configuration file:
   
   **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   
   **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

   Open the file in a text editor and add the server configuration:

   **Windows Configuration:**
   ```json
   {
       "mcpServers": {
           "universe_game": {
               "command": "python",
               "args": ["C:\\path\\to\\your\\universe_game.py"],
               "env": {}
           }
       }
   }
   ```

   **Mac Configuration:**
   ```json
   {
       "mcpServers": {
           "universe_game": {
               "command": "python3",
               "args": ["/path/to/your/universe_game.py"],
               "env": {}
           }
       }
   }
   ```

   **Replace the path with your actual file location!**
   
   Example paths:
   - Windows: `"C:\\Users\\YourName\\Downloads\\universe_game\\universe_game.py"`
   - Mac: `"/Users/YourName/Downloads/universe_game/universe_game.py"`

4. **Restart Claude Desktop**
   - Close Claude Desktop completely
   - Reopen it
   - The Universe Game should now be available!

## How to Use

Once configured, you can interact with the Universe Game through Claude. Here are the available commands:

### Basic Commands

- **Start Evolution**: Ask Claude to "step the universe" or "advance the simulation"
- **Check Status**: Ask for "universe state" or "current status"
- **Reset Game**: Request to "reset the universe"

### Advanced Features

- **Manual Cell Control**: "Flip cell at position (5, 7)"
- **Add Patterns**: "Add a glider pattern" or "place a blinker at (10, 10)"
- **Get Analytics**: "Show universe analytics" for detailed statistics

### Example Conversations

```
You: "Let's start the universe game!"
Claude: [Initializes and shows the current state]

You: "Step the universe forward 5 times"
Claude: [Advances simulation and shows evolution]

You: "Add a glider pattern and let it run"
Claude: [Places glider and shows it moving across the grid]

You: "What patterns have been detected?"
Claude: [Shows analytics with detected oscillators, still lifes, etc.]
```

## Understanding the Display

The game shows a 20x20 grid where:
- `#` = Living cell
- `.` or ` ` = Dead cell

Every 10 turns, you'll see a detailed display with:
- 🌌 Universe grid with coordinates
- 📊 Population statistics
- 💫 Life intensity bar
- Pattern detection results

## Troubleshooting

### Common Issues

**"Command not found" error:**
- Windows: Make sure Python is installed and added to PATH
- Mac: Try using `python3` instead of `python` in the config

**"Module not found" error:**
- Install numpy: `pip install numpy` (Windows) or `pip3 install numpy` (Mac)

**"File not found" error:**
- Double-check the file path in your configuration
- Use forward slashes `/` on Mac, backslashes `\\` on Windows
- Make sure the file exists at the specified location

**Configuration not working:**
- Verify the JSON syntax is correct (use a JSON validator online)
- Restart Claude Desktop after making changes
- Check that the file path doesn't contain special characters

### Getting Help

If you encounter issues:
1. Check that Python and numpy are properly installed
2. Verify your file paths are correct
3. Ensure Claude Desktop was restarted after configuration
4. Try running the Python file directly to test: `python universe_game.py`

## Technical Details

### System Requirements
- Python 3.7+
- numpy library
- Claude Desktop application

### Architecture
- Built as an MCP (Model Context Protocol) server
- Implements Conway's Game of Life rules
- Features pattern detection algorithms
- Provides real-time statistics and visualization

### File Structure
```
universe_game/
├── universe_game.py          # Main MCP server
├── README.md                 # This file
└── examples/                 # Example patterns (optional)
```

## Contributing

Feel free to contribute improvements, bug fixes, or new features:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute according to your needs.

## Acknowledgments

- Based on John Conway's Game of Life
- Built for the Claude Desktop MCP ecosystem
- Inspired by cellular automata research and visualization

---
Claude Desktop https://claude.ai/download
