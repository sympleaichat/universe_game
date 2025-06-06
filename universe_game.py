#!/usr/bin/env python3
"""
Enhanced Universe Game MCP Server with Visual Display
Conway's Game of Life with pattern detection, analytics, and visual ASCII display every 10 turns
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import random
from datetime import datetime

class PatternDetector:
    """Detect Interesting Patterns in the Life Game"""
    
    @staticmethod
    def detect_oscillators(grid: np.ndarray, history: List[np.ndarray]) -> List[Dict]:
        """Detects oscillator patterns"""
        if len(history) < 3:
            return []
        
        patterns = []
        # 2-period oscillator (blinker など)
        if np.array_equal(grid, history[-2]):
            patterns.append({"type": "2-period_oscillator", "period": 2})
        
        # 3-period oscillator
        if len(history) >= 3 and np.array_equal(grid, history[-3]):
            patterns.append({"type": "3-period_oscillator", "period": 3})
            
        return patterns
    
    @staticmethod
    def detect_still_lifes(grid: np.ndarray, prev_grid: np.ndarray) -> List[Dict]:
        """Detects stationary patterns"""
        if np.array_equal(grid, prev_grid):
            alive_cells = np.sum(grid)
            if alive_cells > 0:
                return [{"type": "still_life", "cells": int(alive_cells)}]
        return []
    
    @staticmethod
    def detect_gliders(grid: np.ndarray, history: List[np.ndarray]) -> List[Dict]:
        """Detect glider patterns (simplified version)"""
        if len(history) < 4:
            return []
        
        # Find characteristic 5-cell patterns of gliders
        glider_patterns = []
        rows, cols = grid.shape
        
        for i in range(rows - 2):
            for j in range(cols - 2):
                # Check for 5-cell patterns in a 3x3 area
                region = grid[i:i+3, j:j+3]
                if np.sum(region) == 5:
                    glider_patterns.append({
                        "type": "potential_glider",
                        "position": [int(i), int(j)],
                        "cells": 5
                    })
        
        return glider_patterns

class VisualDisplay:
    """Classes to manage visual display"""
    
    @staticmethod
    def create_detailed_ascii(universe: np.ndarray, turn: int, statistics: Dict) -> str:
        """Create detailed ASCII displays"""
        lines = []
        
        # Header
        lines.append("🌌 ═══════════════════════════════════════════════════════════════")
        lines.append(f"   UNIVERSE EVOLUTION - Turn {turn}")
        lines.append("═══════════════════════════════════════════════════════════════")
        lines.append("")
        
        # Grid display (top number)
        lines.append("    " + "".join([f"{i%10}" for i in range(20)]))
        lines.append("   ┌" + "─" * 20 + "┐")
        
        for i, row in enumerate(universe):
            line = f"{i:2}|"
            for cell in row:
                line += "#" if cell else "."
            line += "|"
            lines.append(line)
        
        lines.append("   └" + "─" * 20 + "┘")
        lines.append("")
        
        # Statistics
        alive = int(np.sum(universe))
        lines.append("📊 STATISTICS")
        lines.append(f"   Living Cells: {alive}")
        lines.append(f"   Population Peak: {statistics.get('max_alive', 0)}")
        lines.append(f"   Total Births: {statistics.get('total_births', 0)}")
        lines.append(f"   Total Deaths: {statistics.get('total_deaths', 0)}")
        lines.append(f"   Stable Generations: {statistics.get('generations_stable', 0)}")
        
        # Visual representation of life status
        lines.append("")
        lines.append("💫 LIFE INTENSITY")
        density = alive / 400  # 400 = 20x20
        bar_length = min(50, int(density * 50))
        bar = "#" * bar_length + ":" * (20 - bar_length) if bar_length < 20 else "#" * 20
        lines.append(f"   [{bar}] {density:.1%}")
        
        return "\n".join(lines)
    
    @staticmethod
    def create_compact_ascii(universe: np.ndarray, turn: int) -> str:
        """Create compact ASCII display"""
        lines = []
        lines.append(f"🌌 Turn {turn} | Living: {int(np.sum(universe))}")
        lines.append("┌" + "─" * 20 + "┐")
        
        for row in universe:
            line = "|"
            for cell in row:
                line += "#" if cell else " "
            line += "|"
            lines.append(line)
        
        lines.append("└" + "─" * 20 + "┘")
        return "\n".join(lines)

class UniverseGame:
    def __init__(self):
        self.GRID_SIZE = 20
        self.universe = np.random.choice([0, 1], size=(self.GRID_SIZE, self.GRID_SIZE))
        self.turn = 0
        self.max_turns = 20
        self.game_id = f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.history = []
        self.grid_history = []
        self.pattern_detector = PatternDetector()
        self.detected_patterns = []
        self.visual_display = VisualDisplay()
        self.display_frequency = 10  # by 10 turn
        self.statistics = {
            "max_alive": 0,
            "min_alive": 999,
            "total_births": 0,
            "total_deaths": 0,
            "generations_stable": 0
        }
        
    def update_universe(self):
        """Update universe according to life game rules"""
        old_grid = self.universe.copy()
        new_grid = np.zeros_like(self.universe)
        
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                neighbors = np.sum(self.universe[max(i-1,0):i+2, max(j-1,0):j+2]) - self.universe[i, j]
                if self.universe[i, j]:
                    new_grid[i, j] = 1 if neighbors in [2, 3] else 0
                else:
                    new_grid[i, j] = 1 if neighbors == 3 else 0
        
        # Statistics update
        old_alive = np.sum(old_grid)
        new_alive = np.sum(new_grid)
        
        if new_alive > old_alive:
            self.statistics["total_births"] += int(new_alive - old_alive)
        elif new_alive < old_alive:
            self.statistics["total_deaths"] += int(old_alive - new_alive)
        
        self.statistics["max_alive"] = max(self.statistics["max_alive"], int(new_alive))
        self.statistics["min_alive"] = min(self.statistics["min_alive"], int(new_alive))
        
        if np.array_equal(old_grid, new_grid):
            self.statistics["generations_stable"] += 1
        else:
            self.statistics["generations_stable"] = 0
        
        self.universe = new_grid
        self.grid_history.append(old_grid)
        
        # Pattern Detection
        self.detect_patterns()
    
    def detect_patterns(self):
        """Detect patterns in the current grid"""
        patterns = []
        
        if len(self.grid_history) > 0:
            prev_grid = self.grid_history[-1]
            
            # Static Patterns
            still_lifes = self.pattern_detector.detect_still_lifes(self.universe, prev_grid)
            patterns.extend(still_lifes)
            
            # Oscillators
            oscillators = self.pattern_detector.detect_oscillators(self.universe, self.grid_history)
            patterns.extend(oscillators)
            
            # Gliders
            gliders = self.pattern_detector.detect_gliders(self.universe, self.grid_history)
            patterns.extend(gliders)
        
        if patterns:
            self.detected_patterns.extend([{
                "turn": self.turn,
                "patterns": patterns
            }])
    
    def should_show_detailed_display(self) -> bool:
        """Determine if detailed display should be performed"""
        return (self.turn % self.display_frequency == 0) or (self.turn == 1)
    
    def get_ascii_display(self) -> str:
        """Generate string for ASCII display (conventional version)"""
        lines = []
        lines.append("+" + "-" * self.GRID_SIZE + "+")
        
        for row in self.universe:
            line = "|"
            for cell in row:
                line += "#" if cell else " "
            line += "|"
            lines.append(line)
        
        lines.append("+" + "-" * self.GRID_SIZE + "+")
        return "\n".join(lines)
    
    def get_visual_display(self) -> str:
        """Get visual display"""
        if self.should_show_detailed_display():
            return self.visual_display.create_detailed_ascii(
                self.universe, self.turn, self.statistics
            )
        else:
            return self.visual_display.create_compact_ascii(
                self.universe, self.turn
            )
    
    def get_summary(self) -> Dict[str, Any]:
        """Add detailed display for visual display timing"""
        alive_cells = int(np.sum(self.universe))
        
        summary = {
            "turn": self.turn,
            "alive_cells": alive_cells,
            # "ascii_display": self.get_ascii_display(),
            "recent_patterns": self.detected_patterns[-3:] if self.detected_patterns else [],
            # "statistics": {
            #     **self.statistics,
            #     "current_alive": alive_cells,
            #     "stability": "stable" if self.statistics["generations_stable"] > 5 else "evolving"
            # },
            # "interesting_events": self._get_interesting_events()
        }
        
        # Add detailed display for visual display timing
        if self.should_show_detailed_display():
            summary["visual_display"] = self.get_visual_display()
            summary["display_milestone"] = True
        
        return summary
    
    def _get_interesting_events(self) -> List[str]:
        """Summarize interesting events"""
        events = []
        alive = int(np.sum(self.universe))
        
        if alive == 0:
            events.append("Universe became extinct")
        elif alive == self.statistics["max_alive"]:
            events.append(f"Population peak reached: {alive} cells")
        elif self.statistics["generations_stable"] > 10:
            events.append(f"Stable for {self.statistics['generations_stable']} generations")
        
        if self.detected_patterns:
            recent_patterns = [p["patterns"] for p in self.detected_patterns[-5:]]
            pattern_types = set()
            for pattern_list in recent_patterns:
                for pattern in pattern_list:
                    pattern_types.add(pattern["type"])
            
            if pattern_types:
                events.append(f"Patterns detected: {', '.join(pattern_types)}")
        
        return events
    
    def flip_cell(self, x: int, y: int) -> str:
        """Invert specified cells"""
        if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE:
            old_state = self.universe[x, y]
            self.universe[x, y] = 1 - self.universe[x, y]
            return f"Cell at ({x}, {y}) flipped from {old_state} to {self.universe[x, y]}"
        return f"Invalid coordinates: ({x}, {y})"
    
    def add_pattern(self, pattern_name: str, x: int = 10, y: int = 10) -> str:
        """Add known patterns"""
        patterns = {
            "glider": [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
            "blinker": [(0, 0), (0, 1), (0, 2)],
            "block": [(0, 0), (0, 1), (1, 0), (1, 1)],
            "beacon": [(0, 0), (0, 1), (1, 0), (2, 3), (3, 2), (3, 3)]
        }
        
        if pattern_name not in patterns:
            return f"Unknown pattern: {pattern_name}"
        
        # Clear Grid
        self.universe.fill(0)
        
        # Place pattern
        for dx, dy in patterns[pattern_name]:
            if 0 <= x + dx < self.GRID_SIZE and 0 <= y + dy < self.GRID_SIZE:
                self.universe[x + dx, y + dy] = 1
        
        return f"Added {pattern_name} pattern at ({x}, {y})"
    
    def step(self) -> Dict[str, Any]:
        """Advance one step (abridged version)"""
        if self.turn >= self.max_turns:
            return {"status": "game_finished", "message": "Game has reached maximum turns"}
        
        # Update universe
        self.update_universe()
        self.turn += 1
        
        return self.get_summary()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            "game_id": self.game_id,
            "turn": self.turn,
            "max_turns": self.max_turns,
            "alive_cells": int(np.sum(self.universe)),
            "universe": self.universe.tolist(),
            "grid_size": self.GRID_SIZE,
            "statistics": self.statistics,
            "recent_patterns": self.detected_patterns[-5:] if self.detected_patterns else [],
            "visual_display": self.get_visual_display()
        }
    
    def reset(self) -> Dict[str, Any]:
        """Reset Game"""
        self.__init__()
        return {
            "status": "reset", 
            "message": "Game has been reset", 
            "summary": self.get_summary(),
            "visual_display": self.get_visual_display()
        }
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get detailed analysis information"""
        return {
            "game_id": self.game_id,
            "total_turns": self.turn,
            "statistics": self.statistics,
            "all_patterns": self.detected_patterns,
            "population_history": [int(np.sum(grid)) for grid in self.grid_history[-20:]],
            "visual_display": self.get_visual_display()
        }

# Global game instances
game = UniverseGame()

class MCPServer:
    def __init__(self):
        self.tools = {
            "step_universe": {
                "name": "step_universe",
                "description": "Execute one step of the universe simulation (returns summary with visual display every 10 turns)",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "get_universe_state": {
                "name": "get_universe_state", 
                "description": "Get current state of the universe game with visual display",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "reset_universe": {
                "name": "reset_universe",
                "description": "Reset the universe game to initial state",
                "inputSchema": {
                    "type": "object", 
                    "properties": {},
                    "required": []
                }
            },
            "flip_cell": {
                "name": "flip_cell",
                "description": "Manually flip a specific cell in the universe",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "x": {"type": "integer", "description": "X coordinate (0-19)"},
                        "y": {"type": "integer", "description": "Y coordinate (0-19)"}
                    },
                    "required": ["x", "y"]
                }
            },
            "add_pattern": {
                "name": "add_pattern",
                "description": "Add a known Conway's Game of Life pattern",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string", 
                            "enum": ["glider", "blinker", "block", "beacon"],
                            "description": "Pattern to add"
                        },
                        "x": {"type": "integer", "description": "X coordinate (default: 10)", "default": 10},
                        "y": {"type": "integer", "description": "Y coordinate (default: 10)", "default": 10}
                    },
                    "required": ["pattern"]
                }
            },
            "get_analytics": {
                "name": "get_analytics",
                "description": "Get detailed analytics and pattern history with visual display",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process messages"""
        method = message.get("method")
        message_id = message.get("id", "unknown")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "universe_game_visual",
                        "version": "2.1.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0", 
                "id": message_id,
                "result": {"tools": list(self.tools.values())}
            }
        
        elif method == "tools/call":
            params = message.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            try:
                if tool_name == "step_universe":
                    result = game.step()
                elif tool_name == "get_universe_state":
                    result = game.get_state()
                elif tool_name == "reset_universe":
                    result = game.reset()
                elif tool_name == "flip_cell":
                    x = arguments.get("x")
                    y = arguments.get("y")
                    if x is None or y is None:
                        result = {"error": "Missing x or y coordinate"}
                    else:
                        flip_result = game.flip_cell(int(x), int(y))
                        result = {
                            "message": flip_result, 
                            # "ascii_display": game.get_ascii_display(),
                            "visual_display": game.get_visual_display(),
                            "summary": game.get_summary()
                        }
                elif tool_name == "add_pattern":
                    pattern = arguments.get("pattern")
                    x = arguments.get("x", 10)
                    y = arguments.get("y", 10)
                    if not pattern:
                        result = {"error": "Missing pattern name"}
                    else:
                        add_result = game.add_pattern(pattern, int(x), int(y))
                        result = {
                            "message": add_result,
                            # "ascii_display": game.get_ascii_display(),
                            "visual_display": game.get_visual_display(), 
                            "summary": game.get_summary()
                        }
                elif tool_name == "get_analytics":
                    result = game.get_analytics()
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                
                return {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }

def read_stdin():
    """Read one line from standard input"""
    return sys.stdin.readline()

async def main():
    """Main loop"""
    server = MCPServer()
    print("Enhanced Universe Game MCP Server with Visual Display starting...", file=sys.stderr, flush=True)
    
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, read_stdin)
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
                
            message = json.loads(line)
            response = await server.handle_message(message)
            
            print(json.dumps(response, ensure_ascii=False), flush=True)
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}", file=sys.stderr, flush=True)
            continue
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr, flush=True)
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}"
                }
            }
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())