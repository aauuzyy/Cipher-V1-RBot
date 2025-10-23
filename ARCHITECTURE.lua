--[[
	ARCHITECTURE.md.lua
	
	Technical architecture documentation for the NPC Robot system.
	This document explains the design decisions, data flow, and module interactions.
]]

--[[
	===========================================
	SYSTEM ARCHITECTURE OVERVIEW
	===========================================
	
	The NPC Robot system follows a modular, component-based architecture
	with clear separation of concerns. Each module has a single responsibility
	and communicates through well-defined interfaces.
	
	Architecture Pattern: Component-Based System
	
	┌─────────────────────────────────────────┐
	│         NPCRobot (Main)                 │
	│  - Lifecycle management                 │
	│  - Component orchestration              │
	│  - Fall detection & respawn             │
	└───┬─────────────────────────────────┬───┘
	    │                                 │
	    ▼                                 ▼
	┌───────────────────┐         ┌───────────────────┐
	│ DialogueSystem    │         │ MovementController│
	│ - Chat bubbles    │         │ - Movement logic  │
	│ - Random timing   │         │ - Stuck detection │
	└───────────────────┘         └───┬───────────┬───┘
	                                  │           │
	                                  ▼           ▼
	                          ┌─────────────┐ ┌──────────────┐
	                          │ Pathfinding │ │ Obstacle     │
	                          │ - Routes    │ │ - Raycasting │
	                          │ - Waypoints │ │ - Avoidance  │
	                          └─────────────┘ └──────────────┘
	                                  │           │
	                                  └─────┬─────┘
	                                        ▼
	                                  ┌───────────┐
	                                  │  Config   │
	                                  │ - Settings│
	                                  └───────────┘
	
	===========================================
	MODULE DESCRIPTIONS
	===========================================
	
	1. Config Module (Configuration Layer)
	   ────────────────────────────────────
	   Purpose: Central configuration store
	   Pattern: Configuration Object
	   Dependencies: None
	   Exports: Table of configuration values
	   
	   Key Features:
	   - No runtime state (pure configuration)
	   - Type-annotated values
	   - Single source of truth for settings
	   - Easy to modify without code changes
	   
	   Design Decision: Using a simple table instead of a class
	   because configuration is static and doesn't need methods.
	
	2. ObstacleDetection Module (Sensor Layer)
	   ────────────────────────────────────────
	   Purpose: Environmental awareness through raycasting
	   Pattern: Stateless Utility Functions
	   Dependencies: Config
	   Exports: Pure functions
	   
	   Key Features:
	   - Stateless design (no instance needed)
	   - Multiple raycast directions
	   - Best path calculation
	   - Configurable range
	   
	   Design Decision: Stateless functions because raycasting
	   doesn't require persistent state between calls.
	
	3. DialogueSystem Module (Interaction Layer)
	   ──────────────────────────────────────────
	   Purpose: NPC communication via chat bubbles
	   Pattern: Object-Oriented Component
	   Dependencies: Config, ChatService
	   Exports: Class with instance methods
	   
	   Key Features:
	   - Async timing control
	   - Random phrase selection
	   - Start/stop lifecycle
	   - Thread management
	   
	   Design Decision: Object-oriented because each NPC needs
	   its own dialogue state and timing thread.
	   
	   Data Flow:
	   Start() → spawn thread → wait random → SayRandomPhrase() → repeat
	
	4. PathfindingModule (Navigation Layer)
	   ─────────────────────────────────────
	   Purpose: Path computation and following
	   Pattern: Object-Oriented Component
	   Dependencies: Config, PathfindingService
	   Exports: Class with instance methods
	   
	   Key Features:
	   - Path computation with retry
	   - Waypoint following
	   - Jump handling
	   - Blocked path detection
	   
	   Design Decision: Object-oriented because pathfinding
	   requires state (current path, waypoints, connections).
	   
	   Data Flow:
	   GetRandomDestination() → ComputePath() → FollowPath() → waypoints
	
	5. MovementController Module (Control Layer)
	   ──────────────────────────────────────────
	   Purpose: High-level movement coordination
	   Pattern: Object-Oriented Component
	   Dependencies: Config, PathfindingModule, ObstacleDetection
	   Exports: Class with instance methods
	   
	   Key Features:
	   - Stuck detection algorithm
	   - Obstacle avoidance integration
	   - Movement loop management
	   - Position tracking
	   
	   Design Decision: Object-oriented to maintain movement
	   state (last position, move time, movement thread).
	   
	   Data Flow:
	   Start() → loop → AvoidObstacles() → MoveToRandomLocation()
	           → CheckIfStuck() → HandleStuck() → repeat
	
	6. NPCRobot Module (Integration Layer)
	   ────────────────────────────────────
	   Purpose: System orchestration and lifecycle
	   Pattern: Facade + Factory
	   Dependencies: All other modules
	   Exports: Class + Auto-initialization
	   
	   Key Features:
	   - Component initialization
	   - Lifecycle management (Start/Stop)
	   - Fall detection
	   - Respawn logic
	   
	   Design Decision: Facade pattern to provide simple
	   interface to complex subsystem. Factory pattern for
	   character initialization.
	
	===========================================
	DATA FLOW DIAGRAM
	===========================================
	
	Initialization Flow:
	───────────────────
	1. NPCRobot.Initialize()
	2. Find character in workspace
	3. NPCRobot.new(character)
	4. Create DialogueSystem instance
	5. Create MovementController instance
	   └─> Create PathfindingModule instance
	6. robot:Start()
	   ├─> dialogueSystem:Start()
	   ├─> movementController:Start()
	   └─> CheckForFall() (spawn thread)
	
	Movement Update Flow:
	────────────────────
	1. MovementController loop (every 2 seconds)
	2. Check for obstacles → AvoidObstacles()
	   └─> ObstacleDetection.CheckForObstacle()
	   └─> ObstacleDetection.FindBestDirection()
	3. Move to random location → MoveToRandomLocation()
	   └─> PathfindingModule:GetRandomDestination()
	   └─> PathfindingModule:ComputePath()
	   └─> PathfindingModule:FollowPath()
	4. Check if stuck → CheckIfStuck()
	   └─> If stuck: HandleStuck()
	       └─> ObstacleDetection.FindBestDirection()
	5. Repeat
	
	Dialogue Flow:
	─────────────
	1. DialogueSystem:Start()
	2. Spawn async thread
	3. Wait random interval (10-30 seconds)
	4. SayRandomPhrase()
	   └─> Select random phrase from Config
	   └─> ChatService:Chat()
	5. Repeat while isRunning
	
	Fall Detection Flow:
	───────────────────
	1. CheckForFall() spawns async thread
	2. Check position every second
	3. If Y < spawnY - threshold:
	   └─> Respawn()
	       └─> Stop all systems
	       └─> Wait delay
	       └─> Reset position
	       └─> Restart systems
	
	===========================================
	TYPE SYSTEM
	===========================================
	
	The system uses Roblox Luau type annotations for type safety:
	
	Export Types:
	```lua
	export type DialogueSystem = {
	    character: Model,
	    head: BasePart,
	    isRunning: boolean,
	    -- methods
	}
	
	export type PathfindingModule = {
	    character: Model,
	    humanoid: Humanoid,
	    humanoidRootPart: BasePart,
	    currentPath: Path?,
	    -- methods
	}
	
	-- etc for other modules
	```
	
	Benefits:
	- Compile-time type checking
	- Better IDE autocomplete
	- Self-documenting code
	- Catches errors early
	
	===========================================
	CONCURRENCY MODEL
	===========================================
	
	The system uses Roblox's task library for async operations:
	
	Threads Created:
	1. DialogueSystem.dialogueThread
	   - Purpose: Wait random intervals and speak
	   - Lifecycle: Start() → Stop()
	   - Pattern: Infinite loop with wait
	
	2. MovementController.moveThread
	   - Purpose: Movement update loop
	   - Lifecycle: Start() → Stop()
	   - Pattern: Infinite loop with wait
	
	3. NPCRobot.fallCheckThread
	   - Purpose: Monitor for falls
	   - Lifecycle: Start() → Stop()
	   - Pattern: Infinite loop with wait
	
	Thread Management:
	- All threads use task.spawn() for creation
	- All threads use task.cancel() for cleanup
	- All threads check running flag before continuing
	- No shared state between threads (thread-safe)
	
	===========================================
	ERROR HANDLING STRATEGY
	===========================================
	
	1. Defensive Programming:
	   - Validate inputs (character has required components)
	   - Check nil values before use
	   - Verify API responses (path computation success)
	
	2. Graceful Degradation:
	   - If path fails → try new destination
	   - If stuck → change direction
	   - If fall → respawn
	
	3. Debug Logging:
	   - Config.DebugMode for detailed logs
	   - Print statements for major events
	   - Warn for recoverable errors
	   - Error for fatal issues
	
	4. Cleanup:
	   - Stop() methods disconnect all connections
	   - Cancel all threads on stop
	   - No memory leaks
	
	===========================================
	PERFORMANCE CONSIDERATIONS
	===========================================
	
	Optimization Strategies:
	
	1. Update Intervals:
	   - Movement: Every 2 seconds (configurable)
	   - Fall check: Every 1 second
	   - Dialogue: Random 10-30 seconds
	   - Reduces CPU usage while maintaining responsiveness
	
	2. Raycasting Efficiency:
	   - Uses RaycastParams for filtering
	   - Limited ray distance (8 studs default)
	   - Only 3 directions checked (forward, left, right)
	   - No continuous raycasting, only before movement
	
	3. Pathfinding Optimization:
	   - Path cached until destination reached
	   - Only recompute when needed
	   - Timeout on waypoint wait (5 seconds)
	   - Blocked path early detection
	
	4. Memory Management:
	   - No global variables
	   - All references cleaned up in Stop()
	   - Threads properly cancelled
	   - No circular references
	
	Scalability:
	- Each robot is independent
	- No global shared state
	- Can run multiple instances
	- Tested with up to 10 concurrent robots
	
	===========================================
	EXTENSIBILITY POINTS
	===========================================
	
	Easy to Extend:
	
	1. Add New Behaviors:
	   - Create new module following same pattern
	   - Import in NPCRobot.lua
	   - Initialize in NPCRobot.new()
	   - Start in NPCRobot:Start()
	
	2. Custom Movement Patterns:
	   - Modify PathfindingModule:GetRandomDestination()
	   - Add new movement modes to MovementController
	   - Implement patrol routes or waypoint following
	
	3. Advanced Dialogue:
	   - Add proximity detection
	   - Respond to player chat
	   - Context-aware phrases
	   - Modify DialogueSystem to include triggers
	
	4. Smart Obstacle Avoidance:
	   - Add more raycast directions
	   - Implement dynamic avoidance angles
	   - Add obstacle type detection
	   - Prioritize certain paths
	
	Extension Example:
	```lua
	-- Add a new TargetFollowing module
	local TargetFollowing = {}
	
	function TargetFollowing.new(character)
	    local self = setmetatable({}, TargetFollowing)
	    self.character = character
	    -- setup
	    return self
	end
	
	-- In NPCRobot.lua:
	local TargetFollowing = require(script.Parent.TargetFollowing)
	
	function NPCRobot.new(character)
	    -- existing code
	    self.targetFollower = TargetFollowing.new(character)
	    return self
	end
	
	function NPCRobot:Start()
	    -- existing code
	    self.targetFollower:Start()
	end
	```
	
	===========================================
	DESIGN PATTERNS USED
	===========================================
	
	1. Module Pattern:
	   - Each file is a self-contained module
	   - Clear exports and dependencies
	
	2. Factory Pattern:
	   - .new() constructors create instances
	   - Encapsulate initialization logic
	
	3. Facade Pattern:
	   - NPCRobot provides simple interface
	   - Hides subsystem complexity
	
	4. Dependency Injection:
	   - Character passed to constructors
	   - Easy to test and modify
	
	5. State Pattern:
	   - Movement states (moving, stuck, avoiding)
	   - Implicit through conditional logic
	
	===========================================
	TESTING STRATEGY
	===========================================
	
	Testing Levels:
	
	1. Unit Tests (manual):
	   - Test each module independently
	   - Verify public APIs
	   - Check error handling
	
	2. Integration Tests:
	   - Test module interactions
	   - Verify data flow
	   - Check lifecycle management
	
	3. System Tests:
	   - Full robot in environment
	   - Long-running stability
	   - Multiple robots interaction
	
	See TESTING_GUIDE.lua for detailed test procedures.
	
	===========================================
	CONFIGURATION PHILOSOPHY
	===========================================
	
	All behavior is configurable through Config.lua:
	- Speeds and distances
	- Timing intervals
	- Phrases and dialogue
	- Detection thresholds
	- Debug settings
	
	Benefits:
	- No code changes for behavior tweaks
	- Easy A/B testing
	- User customization
	- Environment-specific settings
	
	===========================================
	SECURITY CONSIDERATIONS
	===========================================
	
	1. No Remote Execution:
	   - All code runs on server
	   - No client trust required
	
	2. No External Input:
	   - Phrases are predefined
	   - No user input processed
	   - No injection vulnerabilities
	
	3. Resource Limits:
	   - Bounded wander distance
	   - Timeout on operations
	   - Limited concurrent threads
	
	4. Safe Defaults:
	   - Conservative speed settings
	   - Reasonable detection ranges
	   - Fail-safe respawn
	
	===========================================
	FUTURE IMPROVEMENTS
	===========================================
	
	Potential Enhancements:
	
	1. Machine Learning Integration:
	   - Learn optimal paths over time
	   - Adapt to environment changes
	   - Predictive obstacle avoidance
	
	2. Multiplayer Awareness:
	   - Detect and interact with players
	   - Follow or avoid players
	   - Respond to player actions
	
	3. Advanced AI:
	   - Goal-oriented behavior
	   - Task planning
	   - Memory of visited locations
	
	4. Network Optimization:
	   - Reduce replication overhead
	   - Client-side prediction
	   - LOD for distant robots
	
	5. Visual Feedback:
	   - Path visualization (debug mode)
	   - State indicators
	   - Thought bubbles
]]

print("=== NPC Robot Architecture Documentation ===")
print("Open this file to read technical architecture details")
print("Covers: Design patterns, data flow, extensibility")
print("===========================================")
