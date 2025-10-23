--[[
	TESTING_GUIDE.lua
	
	This guide explains how to test and verify each component of the NPC Robot system.
	Since this is Roblox Lua code, it needs to be tested within Roblox Studio.
]]

--[[
	===========================================
	TESTING OVERVIEW
	===========================================
	
	The NPC Robot system consists of several interconnected modules:
	
	1. Config.lua - Configuration settings
	2. ObstacleDetection.lua - Raycasting for walls/obstacles
	3. DialogueSystem.lua - Random chat bubbles
	4. PathfindingModule.lua - PathfindingService integration
	5. MovementController.lua - Movement coordination
	6. NPCRobot.lua - Main orchestration
	
	Each module should be tested individually and then integrated.
	
	===========================================
	UNIT TESTING APPROACH
	===========================================
	
	Since Roblox doesn't have built-in unit testing, we'll use
	manual verification and debug output.
	
	Enable Debug Mode:
	In Config.lua, set:
	Config.DebugMode = true
	
	This will print detailed logs to the Output window.
	
	===========================================
	TEST 1: Configuration Module
	===========================================
	
	Purpose: Verify all settings are correctly defined
	
	Test Script:
	```lua
	local Config = require(script.Parent.Config)
	
	-- Test 1: All required fields exist
	assert(Config.WalkSpeed, "WalkSpeed missing")
	assert(Config.Phrases, "Phrases missing")
	assert(Config.MaxWanderDistance, "MaxWanderDistance missing")
	print("✓ Config has all required fields")
	
	-- Test 2: Values are correct type
	assert(type(Config.WalkSpeed) == "number", "WalkSpeed should be number")
	assert(type(Config.Phrases) == "table", "Phrases should be table")
	print("✓ Config values have correct types")
	
	-- Test 3: Phrases are not empty
	assert(#Config.Phrases > 0, "Phrases should not be empty")
	print("✓ Config has phrases defined")
	
	print("=== Config Module Tests PASSED ===")
	```
	
	Expected Output:
	✓ Config has all required fields
	✓ Config values have correct types
	✓ Config has phrases defined
	=== Config Module Tests PASSED ===
	
	===========================================
	TEST 2: Obstacle Detection Module
	===========================================
	
	Purpose: Verify raycasting detects obstacles
	
	Test Setup:
	1. Create a test NPC in workspace
	2. Place a wall part 5 studs in front of it
	3. Run this test script
	
	Test Script:
	```lua
	local ObstacleDetection = require(script.Parent.ObstacleDetection)
	local Config = require(script.Parent.Config)
	
	Config.DebugMode = true
	
	local character = workspace:FindFirstChild("TestNPC")
	local hrp = character:FindFirstChild("HumanoidRootPart")
	
	-- Test 1: Detect obstacle in front
	local hasObstacle, normal = ObstacleDetection.CheckForObstacle(hrp)
	assert(hasObstacle == true, "Should detect obstacle in front")
	print("✓ Obstacle detection working")
	
	-- Test 2: Check all directions
	local directions = ObstacleDetection.CheckAllDirections(hrp)
	assert(directions.forward ~= nil, "Should check forward")
	assert(directions.left ~= nil, "Should check left")
	assert(directions.right ~= nil, "Should check right")
	print("✓ Multi-direction check working")
	
	-- Test 3: Find best direction
	local bestDir = ObstacleDetection.FindBestDirection(hrp)
	assert(bestDir ~= nil, "Should find a valid direction")
	print("✓ Best direction finder working")
	
	print("=== Obstacle Detection Tests PASSED ===")
	```
	
	Expected Behavior:
	- Raycast should detect wall in front
	- Should suggest turning left or right
	- Debug output should show detected obstacles
	
	===========================================
	TEST 3: Dialogue System Module
	===========================================
	
	Purpose: Verify chat bubbles appear at random intervals
	
	Test Setup:
	1. Create a test NPC with a Head part
	2. Run this test script
	
	Test Script:
	```lua
	local DialogueSystem = require(script.Parent.DialogueSystem)
	local Config = require(script.Parent.Config)
	
	-- Temporarily set short intervals for testing
	Config.MinDialogueInterval = 2
	Config.MaxDialogueInterval = 5
	Config.DebugMode = true
	
	local character = workspace:FindFirstChild("TestNPC")
	local dialogue = DialogueSystem.new(character)
	
	-- Test 1: Create instance
	assert(dialogue.character == character, "Character should be set")
	assert(dialogue.head, "Head should be found")
	print("✓ DialogueSystem instance created")
	
	-- Test 2: Say a phrase manually
	dialogue:SayRandomPhrase()
	print("✓ Manual phrase spoken (check for chat bubble)")
	
	-- Test 3: Start automatic dialogue
	dialogue:Start()
	assert(dialogue.isRunning == true, "Should be running")
	print("✓ Dialogue system started")
	print("  Waiting for automatic phrases (watch for chat bubbles)...")
	
	-- Wait and observe
	task.wait(15)
	
	-- Test 4: Stop dialogue
	dialogue:Stop()
	assert(dialogue.isRunning == false, "Should be stopped")
	print("✓ Dialogue system stopped")
	
	print("=== Dialogue System Tests PASSED ===")
	```
	
	Expected Behavior:
	- Chat bubble should appear above NPC's head
	- Multiple bubbles should appear at 2-5 second intervals
	- System should stop when Stop() is called
	
	===========================================
	TEST 4: Pathfinding Module
	===========================================
	
	Purpose: Verify pathfinding works correctly
	
	Test Setup:
	1. Create a baseplate or terrain
	2. Place test NPC on the baseplate
	3. Run this test script
	
	Test Script:
	```lua
	local PathfindingModule = require(script.Parent.PathfindingModule)
	local Config = require(script.Parent.Config)
	
	Config.DebugMode = true
	
	local character = workspace:FindFirstChild("TestNPC")
	local pathfinder = PathfindingModule.new(character)
	
	-- Test 1: Create instance
	assert(pathfinder.character == character, "Character should be set")
	assert(pathfinder.humanoid, "Humanoid should be found")
	assert(pathfinder.spawnPosition, "Spawn position should be recorded")
	print("✓ PathfindingModule instance created")
	
	-- Test 2: Get random destination
	local dest = pathfinder:GetRandomDestination()
	assert(dest, "Should return a destination")
	assert(typeof(dest) == "Vector3", "Destination should be Vector3")
	print("✓ Random destination generated:", dest)
	
	-- Test 3: Compute path
	local success = pathfinder:ComputePath(dest)
	if success then
		print("✓ Path computed successfully")
	else
		print("⚠ Path computation failed (may be ok if destination unreachable)")
	end
	
	-- Test 4: Follow path
	if success then
		pathfinder:FollowPath()
		print("✓ Following path (watch NPC move)")
	end
	
	print("=== Pathfinding Module Tests PASSED ===")
	```
	
	Expected Behavior:
	- Path should be computed to random destination
	- NPC should move along the computed path
	- Should handle obstacles and jumps
	
	===========================================
	TEST 5: Movement Controller Module
	===========================================
	
	Purpose: Verify movement coordination and stuck detection
	
	Test Setup:
	1. Create test NPC on baseplate
	2. Optionally add some obstacles
	3. Run this test script
	
	Test Script:
	```lua
	local MovementController = require(script.Parent.MovementController)
	local Config = require(script.Parent.Config)
	
	Config.DebugMode = true
	
	local character = workspace:FindFirstChild("TestNPC")
	local controller = MovementController.new(character)
	
	-- Test 1: Create instance
	assert(controller.character == character, "Character should be set")
	assert(controller.pathfinder, "Pathfinder should be initialized")
	print("✓ MovementController instance created")
	
	-- Test 2: Start movement
	controller:Start()
	assert(controller.isMoving == true, "Should be moving")
	print("✓ Movement started (watch NPC wander)")
	
	-- Test 3: Let it run for a while
	print("  Observing movement for 30 seconds...")
	task.wait(30)
	
	-- Test 4: Check if stuck detection works
	-- (Manually place NPC in a corner to test this)
	print("  If NPC gets stuck, it should change direction")
	
	-- Test 5: Stop movement
	task.wait(5)
	controller:Stop()
	assert(controller.isMoving == false, "Should be stopped")
	print("✓ Movement stopped")
	
	print("=== Movement Controller Tests PASSED ===")
	```
	
	Expected Behavior:
	- NPC should wander randomly
	- Should avoid obstacles
	- Should recover when stuck
	- Should respect walk speed setting
	
	===========================================
	TEST 6: Complete NPC Robot Integration
	===========================================
	
	Purpose: Verify all systems work together
	
	Test Setup:
	1. Follow SETUP_GUIDE.lua instructions
	2. Create NPC named "NPCRobot"
	3. Place all scripts in ServerScriptService
	4. Press Play
	
	What to Observe:
	
	1. Movement (within 30 seconds):
	   ✓ Robot starts walking
	   ✓ Robot wanders around spawn area
	   ✓ Robot doesn't walk in straight line only
	
	2. Obstacle Avoidance (place wall in path):
	   ✓ Robot detects wall before collision
	   ✓ Robot turns to avoid wall
	   ✓ Robot continues moving after avoidance
	
	3. Dialogue (within 30 seconds):
	   ✓ Chat bubble appears above robot's head
	   ✓ Different phrases appear at random
	   ✓ Bubbles appear every 10-30 seconds
	
	4. Stuck Recovery (corner robot):
	   ✓ Robot detects it's stuck
	   ✓ Robot changes direction
	   ✓ Robot escapes stuck position
	
	5. Fall Protection (push robot off edge):
	   ✓ Robot detects fall
	   ✓ Robot respawns at start position
	   ✓ Robot resumes normal behavior
	
	6. Performance:
	   ✓ No lag or frame drops
	   ✓ No error messages in Output
	   ✓ Smooth movement and pathfinding
	
	===========================================
	TROUBLESHOOTING TESTS
	===========================================
	
	If tests fail, check:
	
	1. Module Loading Issues:
	   - All scripts in same folder?
	   - Correct script types (Script vs ModuleScript)?
	   - No circular dependencies?
	
	2. Character Issues:
	   - Has Humanoid component?
	   - Has HumanoidRootPart?
	   - Has Head part?
	   - Not anchored?
	
	3. Pathfinding Issues:
	   - Baseplate has collision?
	   - Destination is reachable?
	   - No navigation mesh errors?
	
	4. Raycasting Issues:
	   - RaycastDistance sufficient?
	   - Filter params correct?
	   - Height offset appropriate?
	
	===========================================
	PERFORMANCE TESTING
	===========================================
	
	Test with Multiple Robots:
	```lua
	for i = 1, 10 do
		-- Create 10 robots
		local npc = CreateSimpleNPC("Robot" .. i, Vector3.new(i*5, 5, 0))
		local robot = NPCRobot.new(npc)
		robot:Start()
	end
	```
	
	Monitor:
	- FPS (should stay above 30)
	- Memory usage (check in Studio)
	- No excessive warnings in Output
	
	===========================================
	EDGE CASES TO TEST
	===========================================
	
	1. Empty workspace (no floor):
	   - Should fall and respawn
	
	2. Very small enclosed space:
	   - Should still move within space
	   - Stuck detection should work
	
	3. Character dies:
	   - Should handle gracefully
	   - Can respawn if needed
	
	4. Character removed from workspace:
	   - Should cleanup properly
	   - No memory leaks
	
	5. Dialogue with empty phrases:
	   - Should handle gracefully
	   - No errors
	
	===========================================
	SUCCESS CRITERIA
	===========================================
	
	All tests pass when:
	✓ No errors in Output window
	✓ Robot moves smoothly and naturally
	✓ Obstacles are avoided consistently
	✓ Dialogue appears at appropriate intervals
	✓ Stuck situations are resolved automatically
	✓ Falls are detected and handled
	✓ System can run for 5+ minutes without issues
	✓ Multiple robots can coexist without conflicts
]]

print("=== NPC Robot Testing Guide ===")
print("Open this file to read comprehensive testing instructions")
print("Enable Config.DebugMode = true for detailed test output")
print("===============================")
