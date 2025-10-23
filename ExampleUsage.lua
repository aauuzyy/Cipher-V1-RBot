--[[
	ExampleUsage.lua
	
	This script demonstrates how to use the NPC Robot system programmatically.
	You can use this as a reference for creating multiple robots or integrating
	the robot system into your own game.
	
	USAGE:
	1. Place this script in ServerScriptService
	2. Ensure all NPC Robot modules are in ServerScriptService.NPCRobotSystem
	3. Create NPC character models in Workspace (or use the auto-create function)
	4. Run the game
]]

-- Import the NPC Robot system
local NPCRobotSystem = game:GetService("ServerScriptService"):WaitForChild("NPCRobotSystem")
local NPCRobotModule = require(NPCRobotSystem:WaitForChild("NPCRobot"))
local Config = require(NPCRobotSystem:WaitForChild("Config"))

-- Example 1: Create a robot for an existing character
local function CreateRobotForCharacter(characterName: string)
	local character = workspace:WaitForChild(characterName, 10)
	
	if not character then
		warn("Character", characterName, "not found in workspace")
		return nil
	end
	
	local robot = NPCRobotModule.new(character)
	robot:Start()
	
	print("Robot created for", characterName)
	return robot
end

-- Example 2: Create multiple robots
local function CreateMultipleRobots()
	local robots = {}
	
	-- List of character names in your workspace
	local characterNames = {
		"NPCRobot1",
		"NPCRobot2",
		"NPCRobot3",
	}
	
	for _, name in ipairs(characterNames) do
		local character = workspace:FindFirstChild(name)
		if character then
			local robot = NPCRobotModule.new(character)
			robot:Start()
			table.insert(robots, robot)
			print("Started robot:", name)
		else
			warn("Character not found:", name)
		end
	end
	
	return robots
end

-- Example 3: Create a simple NPC character programmatically
local function CreateSimpleNPC(name: string, position: Vector3): Model
	local npc = Instance.new("Model")
	npc.Name = name
	
	-- Create HumanoidRootPart
	local hrp = Instance.new("Part")
	hrp.Name = "HumanoidRootPart"
	hrp.Size = Vector3.new(2, 2, 1)
	hrp.Position = position
	hrp.Anchored = false
	hrp.CanCollide = true
	hrp.Transparency = 1 -- Invisible
	hrp.Parent = npc
	
	-- Create Head
	local head = Instance.new("Part")
	head.Name = "Head"
	head.Size = Vector3.new(2, 1, 1)
	head.Position = position + Vector3.new(0, 2, 0)
	head.Anchored = false
	head.CanCollide = true
	head.BrickColor = BrickColor.new("Bright blue")
	head.Parent = npc
	
	-- Create Torso (optional, for visibility)
	local torso = Instance.new("Part")
	torso.Name = "Torso"
	torso.Size = Vector3.new(2, 2, 1)
	torso.Position = position + Vector3.new(0, 0.5, 0)
	torso.Anchored = false
	torso.CanCollide = true
	torso.BrickColor = BrickColor.new("Bright red")
	torso.Parent = npc
	
	-- Create Humanoid
	local humanoid = Instance.new("Humanoid")
	humanoid.Parent = npc
	
	-- Weld head and torso to HumanoidRootPart
	local headWeld = Instance.new("WeldConstraint")
	headWeld.Part0 = hrp
	headWeld.Part1 = head
	headWeld.Parent = hrp
	
	local torsoWeld = Instance.new("WeldConstraint")
	torsoWeld.Part0 = hrp
	torsoWeld.Part1 = torso
	torsoWeld.Parent = hrp
	
	-- Add to workspace
	npc.Parent = workspace
	
	return npc
end

-- Example 4: Advanced - Create and manage a robot with custom settings
local function CreateCustomRobot()
	-- Create a simple NPC
	local npc = CreateSimpleNPC("CustomRobot", Vector3.new(0, 5, 0))
	
	-- Wait a moment for physics to settle
	task.wait(0.5)
	
	-- Create robot with custom behavior
	local robot = NPCRobotModule.new(npc)
	
	-- You can access and modify robot properties before starting
	-- Note: Config is shared across all robots
	-- For individual robot settings, you'd need to modify the modules
	
	robot:Start()
	
	-- Stop the robot after 30 seconds (example)
	task.delay(30, function()
		robot:Stop()
		print("Custom robot stopped after 30 seconds")
	end)
	
	-- Restart after 35 seconds
	task.delay(35, function()
		robot:Start()
		print("Custom robot restarted")
	end)
	
	return robot
end

-- Example 5: React to robot events
local function MonitorRobot(robot)
	local character = robot.character
	
	-- Monitor when robot's humanoid dies
	robot.humanoid.Died:Connect(function()
		print(character.Name, "has died!")
		-- Auto-respawn after 5 seconds
		task.wait(5)
		robot:Respawn()
	end)
	
	-- Monitor when robot is removed from workspace
	character.AncestryChanged:Connect(function(_, parent)
		if not parent then
			print(character.Name, "was removed from workspace")
			robot:Stop()
		end
	end)
end

-- ============================================
-- MAIN EXECUTION
-- ============================================

-- Choose which example to run:

-- Option 1: Use existing character
-- local myRobot = CreateRobotForCharacter("NPCRobot")

-- Option 2: Create multiple robots
-- local allRobots = CreateMultipleRobots()

-- Option 3: Create a simple robot programmatically
local simpleRobot = CreateCustomRobot()
if simpleRobot then
	MonitorRobot(simpleRobot)
end

-- Option 4: Create several robots at different positions
task.wait(1) -- Wait a moment
for i = 1, 3 do
	local spawnPos = Vector3.new(i * 10, 5, 0)
	local npc = CreateSimpleNPC("Robot" .. i, spawnPos)
	task.wait(0.5)
	
	local robot = NPCRobotModule.new(npc)
	robot:Start()
	print("Started Robot" .. i)
end

print("=== Example Usage Script Complete ===")
print("Check the Output for robot status messages")
print("Enable Config.DebugMode for detailed logs")
