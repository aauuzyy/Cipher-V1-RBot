--[[
	NPCRobot.lua
	Main script that orchestrates all NPC robot components
	
	SETUP INSTRUCTIONS:
	1. Place this script and all module scripts (Config, ObstacleDetection, DialogueSystem, 
	   PathfindingModule, MovementController) in the same location (e.g., ServerScriptService)
	2. Create an NPC character model in the workspace with:
	   - Humanoid
	   - HumanoidRootPart
	   - Head (for chat bubbles)
	   - Other body parts as needed
	3. Set the CHARACTER_NAME variable below to match your NPC's name
	4. Run the script from a Script (not LocalScript) in ServerScriptService
]]

local Config = require(script.Parent.Config)
local DialogueSystem = require(script.Parent.DialogueSystem)
local MovementController = require(script.Parent.MovementController)

-- CONFIGURATION: Set this to your NPC character's name in the workspace
local CHARACTER_NAME = "NPCRobot"

local NPCRobot = {}
NPCRobot.__index = NPCRobot

export type NPCRobot = {
	character: Model,
	humanoid: Humanoid,
	humanoidRootPart: BasePart,
	dialogueSystem: any,
	movementController: any,
	spawnPosition: Vector3,
	fallCheckThread: thread?,
	isActive: boolean,
	new: (character: Model) -> NPCRobot,
	Start: (self: NPCRobot) -> (),
	Stop: (self: NPCRobot) -> (),
	CheckForFall: (self: NPCRobot) -> (),
	Respawn: (self: NPCRobot) -> ()
}

--[[
	Creates a new NPCRobot instance
	@param character - The NPC character model
	@return NPCRobot instance
]]
function NPCRobot.new(character: Model): NPCRobot
	local self = setmetatable({}, NPCRobot)
	
	-- Validate character
	local humanoid = character:FindFirstChildOfClass("Humanoid")
	local humanoidRootPart = character:FindFirstChild("HumanoidRootPart")
	
	if not humanoid or not humanoidRootPart then
		error("[NPCRobot] Character must have a Humanoid and HumanoidRootPart")
	end
	
	self.character = character
	self.humanoid = humanoid :: Humanoid
	self.humanoidRootPart = humanoidRootPart :: BasePart
	self.spawnPosition = humanoidRootPart.Position
	self.isActive = false
	
	-- Initialize systems
	self.dialogueSystem = DialogueSystem.new(character)
	self.movementController = MovementController.new(character)
	
	if Config.DebugMode then
		print("[NPCRobot] Initialized for", character.Name)
	end
	
	return self
end

--[[
	Starts all robot systems
]]
function NPCRobot:Start()
	if self.isActive then
		return
	end
	
	self.isActive = true
	
	-- Start dialogue system
	self.dialogueSystem:Start()
	
	-- Start movement controller
	self.movementController:Start()
	
	-- Start fall detection
	self:CheckForFall()
	
	print("[NPCRobot]", self.character.Name, "is now active!")
end

--[[
	Stops all robot systems
]]
function NPCRobot:Stop()
	if not self.isActive then
		return
	end
	
	self.isActive = false
	
	-- Stop dialogue system
	self.dialogueSystem:Stop()
	
	-- Stop movement controller
	self.movementController:Stop()
	
	-- Stop fall detection
	if self.fallCheckThread then
		task.cancel(self.fallCheckThread)
		self.fallCheckThread = nil
	end
	
	print("[NPCRobot]", self.character.Name, "has been stopped.")
end

--[[
	Continuously checks if the robot has fallen
]]
function NPCRobot:CheckForFall()
	self.fallCheckThread = task.spawn(function()
		while self.isActive do
			task.wait(1) -- Check every second
			
			-- Check if robot fell below spawn position
			local currentY = self.humanoidRootPart.Position.Y
			local spawnY = self.spawnPosition.Y
			
			if currentY < spawnY - Config.FallDistanceThreshold then
				if Config.DebugMode then
					warn("[NPCRobot] Robot has fallen! Respawning...")
				end
				
				self:Respawn()
			end
		end
	end)
end

--[[
	Respawns the robot at its spawn position
]]
function NPCRobot:Respawn()
	-- Stop systems temporarily
	local wasActive = self.isActive
	self:Stop()
	
	-- Wait before respawning
	task.wait(Config.RespawnDelay)
	
	-- Reset position
	if self.humanoidRootPart and self.humanoidRootPart.Parent then
		self.humanoidRootPart.CFrame = CFrame.new(self.spawnPosition)
		
		-- Reset humanoid health if needed
		if self.humanoid.Health <= 0 then
			self.humanoid.Health = self.humanoid.MaxHealth
		end
		
		if Config.DebugMode then
			print("[NPCRobot] Respawned at", self.spawnPosition)
		end
		
		-- Restart systems if it was active
		if wasActive then
			self:Start()
		end
	end
end

-- Main initialization code
local function Initialize()
	-- Wait for workspace to load
	task.wait(1)
	
	-- Find the character in workspace
	local character = workspace:FindFirstChild(CHARACTER_NAME)
	
	if not character then
		warn("[NPCRobot] Character '" .. CHARACTER_NAME .. "' not found in workspace!")
		warn("[NPCRobot] Please create an NPC character with this name or update CHARACTER_NAME variable")
		return
	end
	
	-- Create and start the robot
	local robot = NPCRobot.new(character)
	robot:Start()
	
	-- Handle character removal
	character.AncestryChanged:Connect(function(_, parent)
		if not parent then
			robot:Stop()
		end
	end)
end

-- Run initialization
Initialize()

return NPCRobot
