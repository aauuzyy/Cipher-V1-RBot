--[[
	QUICK_REFERENCE.lua
	
	Quick reference guide for common tasks and modifications.
	Perfect for when you need to make quick changes.
]]

--[[
	===========================================
	QUICK START (3 STEPS)
	===========================================
	
	1. Create an NPC character in Workspace named "NPCRobot"
	   (Use Insert > Rig Builder > R15)
	
	2. Put all .lua files in ServerScriptService > NPCRobotSystem
	   (Config, ObstacleDetection, DialogueSystem, PathfindingModule,
	    MovementController, NPCRobot)
	
	3. Press Play!
	
	===========================================
	COMMON MODIFICATIONS
	===========================================
	
	Make Robot Faster:
	─────────────────
	File: Config.lua
	Line: Config.WalkSpeed = 16
	Change to: Config.WalkSpeed = 25
	
	Make Robot Slower:
	─────────────────
	File: Config.lua
	Line: Config.WalkSpeed = 16
	Change to: Config.WalkSpeed = 8
	
	Add Custom Phrases:
	──────────────────
	File: Config.lua
	Line: Config.Phrases = { ... }
	Add your phrases to the table:
	Config.Phrases = {
	    "Hello there! I'm a robot.",
	    "Your custom phrase here!",
	    "Add as many as you want!",
	}
	
	Change Dialogue Frequency:
	─────────────────────────
	File: Config.lua
	More frequent (every 5-15 seconds):
	Config.MinDialogueInterval = 5
	Config.MaxDialogueInterval = 15
	
	Less frequent (every 30-60 seconds):
	Config.MinDialogueInterval = 30
	Config.MaxDialogueInterval = 60
	
	Increase Wander Range:
	─────────────────────
	File: Config.lua
	Line: Config.MaxWanderDistance = 50
	Change to: Config.MaxWanderDistance = 100
	
	Decrease Wander Range:
	─────────────────────
	File: Config.lua
	Line: Config.MaxWanderDistance = 50
	Change to: Config.MaxWanderDistance = 25
	
	Enable Debug Logging:
	────────────────────
	File: Config.lua
	Line: Config.DebugMode = false
	Change to: Config.DebugMode = true
	(Shows detailed logs in Output window)
	
	Change Character Name:
	─────────────────────
	File: NPCRobot.lua
	Line: local CHARACTER_NAME = "NPCRobot"
	Change to: local CHARACTER_NAME = "YourNPCName"
	
	Make Robot Jump More:
	────────────────────
	File: PathfindingModule.lua
	In PathfindingService:CreatePath():
	Change: AgentCanJump = true
	To: AgentCanJump = true, AgentCanClimb = true
	
	Adjust Obstacle Detection Range:
	───────────────────────────────
	File: Config.lua
	Line: Config.RaycastDistance = 8
	Change to: Config.RaycastDistance = 12 (detect further)
	Or: Config.RaycastDistance = 5 (detect closer)
	
	Change Stuck Recovery Time:
	──────────────────────────
	File: Config.lua
	Line: Config.StuckThreshold = 3
	Change to: Config.StuckThreshold = 5 (more patient)
	Or: Config.StuckThreshold = 1 (quicker recovery)
	
	Modify Respawn Delay:
	────────────────────
	File: Config.lua
	Line: Config.RespawnDelay = 3
	Change to: Config.RespawnDelay = 1 (faster)
	Or: Config.RespawnDelay = 5 (slower)
	
	===========================================
	TROUBLESHOOTING
	===========================================
	
	Robot Doesn't Move:
	──────────────────
	✓ Check: Character has Humanoid
	✓ Check: Character has HumanoidRootPart
	✓ Check: Character is not anchored
	✓ Check: Floor has collision enabled
	✓ Enable: Config.DebugMode = true
	✓ Look in Output for errors
	
	No Chat Bubbles:
	───────────────
	✓ Check: Character has "Head" part
	✓ Check: Chat is enabled in game settings
	✓ Enable: Config.DebugMode = true
	✓ Watch Output for dialogue messages
	
	Robot Falls Through Floor:
	─────────────────────────
	✓ Check: Floor has collision enabled
	✓ Check: Floor is not set to CanCollide = false
	✓ Check: Spawn position is above floor
	✓ Note: Robot will respawn if it falls
	
	"Character Not Found" Error:
	───────────────────────────
	✓ Check: Character name matches CHARACTER_NAME
	✓ Check: Character is in Workspace
	✓ Check: Spelling and capitalization
	✓ Update: CHARACTER_NAME in NPCRobot.lua
	
	Robot Gets Stuck:
	────────────────
	✓ This is normal - it should recover automatically
	✓ If it doesn't: Lower Config.StuckThreshold
	✓ If it's too sensitive: Raise Config.StuckThreshold
	✓ Check: ObstacleDetection is working (debug mode)
	
	Script Errors:
	─────────────
	✓ Check: All files are in same folder
	✓ Check: Config, ObstacleDetection, etc. are ModuleScripts
	✓ Check: NPCRobot is a Script (not ModuleScript)
	✓ Look: At line numbers in error messages
	✓ Enable: Config.DebugMode for more info
	
	===========================================
	ADVANCED CUSTOMIZATION
	===========================================
	
	Create Multiple Robots:
	──────────────────────
	1. Duplicate your character in Workspace
	2. Rename each: "Robot1", "Robot2", etc.
	3. Duplicate NPCRobot script for each
	4. Change CHARACTER_NAME in each script
	5. Press Play
	
	Custom Movement Pattern:
	───────────────────────
	File: PathfindingModule.lua
	Function: GetRandomDestination()
	
	Example - Move in circles:
	```lua
	function PathfindingModule:GetRandomDestination(): Vector3
	    self.angle = (self.angle or 0) + math.pi / 4
	    local radius = 20
	    local offset = Vector3.new(
	        math.cos(self.angle) * radius,
	        0,
	        math.sin(self.angle) * radius
	    )
	    return self.spawnPosition + offset
	end
	```
	
	Example - Patrol waypoints:
	```lua
	local waypoints = {
	    Vector3.new(10, 5, 10),
	    Vector3.new(20, 5, 20),
	    Vector3.new(30, 5, 10),
	}
	
	function PathfindingModule:GetRandomDestination(): Vector3
	    self.waypointIndex = (self.waypointIndex or 0) % #waypoints + 1
	    return waypoints[self.waypointIndex]
	end
	```
	
	Context-Aware Dialogue:
	──────────────────────
	File: DialogueSystem.lua
	Function: SayRandomPhrase()
	
	Example - Time-based phrases:
	```lua
	function DialogueSystem:SayRandomPhrase()
	    local hour = os.date("*t").hour
	    local phrase
	    
	    if hour < 12 then
	        phrase = "Good morning!"
	    elseif hour < 18 then
	        phrase = "Good afternoon!"
	    else
	        phrase = "Good evening!"
	    end
	    
	    ChatService:Chat(self.head, phrase, Enum.ChatColor.White)
	end
	```
	
	Player Detection:
	────────────────
	Add to MovementController.lua:
	
	```lua
	function MovementController:FindNearestPlayer(): Player?
	    local nearestPlayer = nil
	    local nearestDistance = math.huge
	    
	    for _, player in pairs(game.Players:GetPlayers()) do
	        local character = player.Character
	        if character then
	            local distance = (character.HumanoidRootPart.Position - 
	                            self.humanoidRootPart.Position).Magnitude
	            if distance < nearestDistance then
	                nearestDistance = distance
	                nearestPlayer = player
	            end
	        end
	    end
	    
	    return nearestPlayer
	end
	
	-- Use in MoveToRandomLocation():
	function MovementController:MoveToRandomLocation()
	    local player = self:FindNearestPlayer()
	    local destination
	    
	    if player and player.Character then
	        -- Move towards player if within 50 studs
	        local distance = (player.Character.HumanoidRootPart.Position - 
	                         self.humanoidRootPart.Position).Magnitude
	        if distance < 50 then
	            destination = player.Character.HumanoidRootPart.Position
	        else
	            destination = self.pathfinder:GetRandomDestination()
	        end
	    else
	        destination = self.pathfinder:GetRandomDestination()
	    end
	    
	    -- Rest of existing code...
	end
	```
	
	===========================================
	PERFORMANCE TUNING
	===========================================
	
	For Better Performance:
	──────────────────────
	✓ Increase: Config.PathUpdateInterval (slower updates)
	✓ Decrease: Config.RaycastDistance (shorter rays)
	✓ Limit: Number of robots in game
	✓ Use: Simpler character models
	
	For More Responsive Behavior:
	────────────────────────────
	✓ Decrease: Config.PathUpdateInterval (faster updates)
	✓ Increase: Config.RaycastDistance (earlier detection)
	✓ Decrease: Config.StuckThreshold (quicker recovery)
	
	===========================================
	USEFUL CODE SNIPPETS
	===========================================
	
	Stop All Robots:
	───────────────
	```lua
	for _, desc in pairs(game.ServerScriptService.NPCRobotSystem:GetDescendants()) do
	    if desc:IsA("Script") and desc.Name == "NPCRobot" then
	        -- Robots will stop when script is disabled
	        desc.Disabled = true
	    end
	end
	```
	
	Create Robot Programmatically:
	─────────────────────────────
	```lua
	local NPCRobot = require(game.ServerScriptService.NPCRobotSystem.NPCRobot)
	local character = workspace:FindFirstChild("NPCRobot")
	local robot = NPCRobot.new(character)
	robot:Start()
	```
	
	Change Phrases at Runtime:
	─────────────────────────
	```lua
	local Config = require(game.ServerScriptService.NPCRobotSystem.Config)
	Config.Phrases = {
	    "New phrase 1",
	    "New phrase 2",
	}
	```
	
	Monitor Robot Position:
	──────────────────────
	```lua
	local character = workspace:FindFirstChild("NPCRobot")
	local hrp = character.HumanoidRootPart
	
	while true do
	    print("Robot position:", hrp.Position)
	    task.wait(1)
	end
	```
	
	===========================================
	FILE CHECKLIST
	===========================================
	
	Required Files (All in same folder):
	☐ Config.lua (ModuleScript)
	☐ ObstacleDetection.lua (ModuleScript)
	☐ DialogueSystem.lua (ModuleScript)
	☐ PathfindingModule.lua (ModuleScript)
	☐ MovementController.lua (ModuleScript)
	☐ NPCRobot.lua (Script) ← Must be a Script!
	
	Optional Files:
	☐ SETUP_GUIDE.lua (Documentation)
	☐ TESTING_GUIDE.lua (Documentation)
	☐ ARCHITECTURE.lua (Documentation)
	☐ ExampleUsage.lua (Example code)
	
	===========================================
	RECOMMENDED SETTINGS
	===========================================
	
	For Casual Wandering:
	────────────────────
	Config.WalkSpeed = 12
	Config.MaxWanderDistance = 30
	Config.MinDialogueInterval = 15
	Config.MaxDialogueInterval = 45
	
	For Active Exploration:
	──────────────────────
	Config.WalkSpeed = 20
	Config.MaxWanderDistance = 100
	Config.PathUpdateInterval = 1
	Config.MinDialogueInterval = 5
	Config.MaxDialogueInterval = 15
	
	For Confined Space:
	──────────────────
	Config.WalkSpeed = 10
	Config.MaxWanderDistance = 20
	Config.RaycastDistance = 5
	Config.StuckThreshold = 2
	
	For Testing/Debug:
	─────────────────
	Config.DebugMode = true
	Config.MinDialogueInterval = 3
	Config.MaxDialogueInterval = 8
	Config.PathUpdateInterval = 1
	
	===========================================
	GETTING HELP
	===========================================
	
	1. Enable debug mode: Config.DebugMode = true
	2. Check Output window for error messages
	3. Review SETUP_GUIDE.lua for setup instructions
	4. Read TESTING_GUIDE.lua for testing procedures
	5. Check ARCHITECTURE.lua for technical details
	6. Look at ExampleUsage.lua for code examples
]]

print("=== NPC Robot Quick Reference ===")
print("Fast answers to common questions")
print("Open file for detailed quick reference")
print("================================")
