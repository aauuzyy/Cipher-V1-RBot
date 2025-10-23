--[[
	SETUP_GUIDE.lua
	Step-by-step setup guide for the NPC Robot
	
	This file provides detailed instructions for setting up the robot.
	Read through each section carefully.
]]

--[[
	===========================================
	STEP 1: CREATE YOUR NPC CHARACTER
	===========================================
	
	Option A: Use a Roblox Character Rig
	-------------------------------------
	1. In Roblox Studio, go to the Home tab
	2. Click on "Rig Builder" (in the Avatar section)
	3. Select "R15" or "R6" (R15 recommended)
	4. A character rig will appear in the Workspace
	5. Rename it to "NPCRobot"
	
	Option B: Create a Custom Character
	-----------------------------------
	1. Create a new Model in Workspace
	2. Name it "NPCRobot"
	3. Add these essential parts:
	   - HumanoidRootPart (BasePart)
	   - Head (BasePart)
	   - Humanoid (from Insert Object menu)
	4. Position the Head above the HumanoidRootPart
	5. Optionally add other body parts (torso, arms, legs)
	
	===========================================
	STEP 2: ORGANIZE THE SCRIPTS
	===========================================
	
	1. In ServerScriptService, create a new Folder
	2. Name it "NPCRobotSystem"
	3. Add these files as ModuleScripts:
	   - Config.lua (ModuleScript)
	   - ObstacleDetection.lua (ModuleScript)
	   - DialogueSystem.lua (ModuleScript)
	   - PathfindingModule.lua (ModuleScript)
	   - MovementController.lua (ModuleScript)
	4. Add NPCRobot.lua as a regular Script (NOT ModuleScript)
	
	Folder structure should look like:
	ServerScriptService
	└── NPCRobotSystem
	    ├── Config (ModuleScript)
	    ├── ObstacleDetection (ModuleScript)
	    ├── DialogueSystem (ModuleScript)
	    ├── PathfindingModule (ModuleScript)
	    ├── MovementController (ModuleScript)
	    └── NPCRobot (Script) ← This one is a Script!
	
	===========================================
	STEP 3: CONFIGURE THE CHARACTER NAME
	===========================================
	
	1. Open NPCRobot.lua (the Script, not ModuleScript)
	2. Find this line near the top:
	   local CHARACTER_NAME = "NPCRobot"
	3. If you named your character differently, change it here
	4. Example: local CHARACTER_NAME = "MyAwesomeBot"
	
	===========================================
	STEP 4: CUSTOMIZE SETTINGS (OPTIONAL)
	===========================================
	
	Open Config.lua and customize:
	
	-- Speed and Movement
	Config.WalkSpeed = 16  -- Make robot faster/slower
	Config.MaxWanderDistance = 50  -- How far robot can wander
	
	-- Dialogue
	Config.MinDialogueInterval = 10  -- Minimum seconds between phrases
	Config.MaxDialogueInterval = 30  -- Maximum seconds between phrases
	
	-- Add your own phrases
	Config.Phrases = {
	    "Hello there!",
	    "Add your custom phrases here!",
	}
	
	-- Debug (helpful for troubleshooting)
	Config.DebugMode = true  -- Shows detailed logs
	
	===========================================
	STEP 5: TEST THE ROBOT
	===========================================
	
	1. Make sure your NPC character is in the Workspace
	2. Make sure all scripts are in ServerScriptService
	3. Click the "Play" button in Roblox Studio
	4. Watch the Output window for any errors
	5. The robot should start:
	   - Walking around automatically
	   - Saying phrases in chat bubbles
	   - Avoiding obstacles
	   - Recovering when stuck
	
	===========================================
	TROUBLESHOOTING
	===========================================
	
	Problem: "Character not found" error
	Solution: Check that CHARACTER_NAME matches your character's exact name
	
	Problem: Robot doesn't move
	Solution: 
	- Verify character has Humanoid and HumanoidRootPart
	- Make sure character is not anchored
	- Check that your map has a floor with collision
	
	Problem: No chat bubbles appear
	Solution: Verify character has a "Head" part
	
	Problem: Script errors in Output
	Solution:
	- Enable Config.DebugMode = true for detailed logs
	- Check that all ModuleScripts are in the same folder
	- Verify require() paths are correct
	
	Problem: Robot falls through floor
	Solution: Ensure your floor/terrain has collision enabled
	
	===========================================
	ADVANCED CUSTOMIZATION
	===========================================
	
	Multiple Robots:
	- Duplicate your character in Workspace
	- Give each a unique name
	- Duplicate and modify NPCRobot.lua for each one
	- Change CHARACTER_NAME for each script
	
	Custom Behaviors:
	- Modify MovementController.lua for different movement patterns
	- Edit DialogueSystem.lua to trigger phrases on events
	- Adjust ObstacleDetection.lua for different avoidance strategies
	
	Integration:
	- Use the NPCRobot module in your own scripts
	- Create instances programmatically: NPCRobot.new(character)
	- Start/stop robots: robot:Start() and robot:Stop()
]]

print("=== NPC Robot Setup Guide ===")
print("This file contains detailed setup instructions.")
print("Open it in the script editor to read the full guide!")
print("============================")
