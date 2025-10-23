# Cipher-V1-RBot

An advanced autonomous Roblox NPC robot that demonstrates modern Lua scripting techniques and AI-like behavior. The robot walks around autonomously using PathfindingService, avoids obstacles with raycasting, and engages players with random dialogue.

## Features

- **Autonomous Movement**: Uses Roblox PathfindingService to navigate the environment intelligently
- **Obstacle Detection**: Implements raycasting to detect and avoid walls and obstacles
- **Dynamic Dialogue**: Randomly speaks phrases every 10-30 seconds using chat bubbles
- **Stuck Detection**: Automatically detects when stuck and changes direction
- **Fall Protection**: Respawns if the robot falls off the map
- **Modular Architecture**: Clean, maintainable code structure with separate modules
- **Type Safety**: Modern Roblox Lua with proper type annotations
- **Configurable**: Easy-to-modify settings for speed, phrases, and behavior

## File Structure

```
Cipher-V1-RBot/
├── Config.lua              # Configuration settings
├── ObstacleDetection.lua   # Raycasting and obstacle avoidance
├── DialogueSystem.lua      # Random chat bubble system
├── PathfindingModule.lua   # Pathfinding logic
├── MovementController.lua  # Movement and stuck detection
├── NPCRobot.lua           # Main orchestration script
└── README.md              # This file
```

## Setup Instructions

### 1. Create the NPC Character

In Roblox Studio:
1. Create a new humanoid character model in the Workspace
2. Name it "NPCRobot" (or customize the `CHARACTER_NAME` in NPCRobot.lua)
3. Ensure it has:
   - Humanoid component
   - HumanoidRootPart
   - Head (for chat bubbles)
   - Other body parts (arms, legs, torso)

### 2. Install the Scripts

1. In ServerScriptService, create a new Folder named "NPCRobotSystem"
2. Add all the Lua files to this folder:
   - Config.lua
   - ObstacleDetection.lua
   - DialogueSystem.lua
   - PathfindingModule.lua
   - MovementController.lua
   - NPCRobot.lua (this should be a Script, not a ModuleScript)

### 3. Configuration

Edit `Config.lua` to customize:
- **WalkSpeed**: How fast the robot moves
- **Phrases**: What the robot says
- **MaxWanderDistance**: How far from spawn point the robot can wander
- **DialogueIntervals**: Timing between phrases
- **DebugMode**: Enable/disable debug logging

### 4. Run the Game

Press Play in Roblox Studio. The robot should:
1. Start walking around autonomously
2. Avoid obstacles it encounters
3. Say random phrases every 10-30 seconds
4. Recover when stuck
5. Respawn if it falls

## Module Documentation

### Config.lua
Central configuration file containing all customizable settings:
- Movement parameters (speed, wander distance)
- Dialogue settings (phrases, timing)
- Obstacle detection settings (raycast distance, avoidance angles)
- Fall detection and respawn settings

### ObstacleDetection.lua
Handles raycasting for wall and obstacle detection:
- `CheckForObstacle()`: Checks if obstacle is in front
- `CheckAllDirections()`: Scans multiple directions
- `FindBestDirection()`: Determines optimal path when blocked

### DialogueSystem.lua
Manages the chat bubble system:
- Randomly selects phrases from config
- Displays chat bubbles at random intervals
- Uses Roblox ChatService for proper chat integration

### PathfindingModule.lua
Integrates with Roblox PathfindingService:
- `GetRandomDestination()`: Generates random waypoints
- `ComputePath()`: Calculates optimal path to destination
- `FollowPath()`: Executes movement along computed path

### MovementController.lua
Main movement logic and coordination:
- Orchestrates pathfinding and obstacle avoidance
- Detects when robot is stuck
- Changes direction when encountering problems
- Manages movement state and timing

### NPCRobot.lua
Primary orchestration script:
- Initializes all subsystems
- Monitors for falls and triggers respawn
- Manages overall robot lifecycle
- Entry point for the system

## Customization Examples

### Change Walking Speed
```lua
-- In Config.lua
Config.WalkSpeed = 20  -- Default is 16
```

### Add New Phrases
```lua
-- In Config.lua
Config.Phrases = {
    "Hello there!",
    "Nice day for a walk!",
    "Your custom phrase here",
    -- Add as many as you want
}
```

### Adjust Obstacle Detection
```lua
-- In Config.lua
Config.RaycastDistance = 12  -- Default is 8 (detects further)
Config.ObstacleAvoidanceAngle = 45  -- Default is 90 (sharper turns)
```

### Enable Debug Mode
```lua
-- In Config.lua
Config.DebugMode = true  -- See detailed logs in output
```

## Technical Details

### Type Safety
All modules use Roblox Luau type annotations for better code safety:
```lua
function PathfindingModule.new(character: Model): PathfindingModule
function ObstacleDetection.CheckForObstacle(humanoidRootPart: BasePart, direction: Vector3?): (boolean, Vector3?)
```

### Modern Roblox APIs
- Uses `task.spawn()` and `task.wait()` for better performance
- Implements `PathfindingService` with proper parameters
- Uses `RaycastParams` for efficient raycasting
- Integrates with `ChatService` for chat bubbles

### Performance Considerations
- Path updates every 2 seconds (configurable)
- Efficient raycasting with filtered params
- Proper cleanup of connections and threads
- Minimal garbage collection overhead

## Troubleshooting

**Robot doesn't move:**
- Check that the character has a Humanoid and HumanoidRootPart
- Ensure the character is not anchored
- Verify PathfindingService can generate paths in your map

**Robot falls through floor:**
- Make sure your floor has collision enabled
- Check that the spawn position is above solid ground

**No chat bubbles:**
- Verify the character has a Head part
- Check that Chat is enabled in game settings

**Robot gets stuck:**
- The stuck detection should handle this automatically
- If it persists, try adjusting `StuckThreshold` in Config.lua

## License

This is a demonstration project showing advanced Roblox scripting techniques.

## Credits

Created to demonstrate modern Roblox Lua scripting with:
- PathfindingService integration
- Raycasting for obstacle detection
- Modular code architecture
- Type-safe Luau implementation
