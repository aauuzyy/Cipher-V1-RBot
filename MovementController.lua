--[[
	MovementController.lua
	Main movement logic with stuck detection and direction changes
]]

local Config = require(script.Parent.Config)
local ObstacleDetection = require(script.Parent.ObstacleDetection)
local PathfindingModule = require(script.Parent.PathfindingModule)

local MovementController = {}
MovementController.__index = MovementController

export type MovementController = {
	character: Model,
	humanoid: Humanoid,
	humanoidRootPart: BasePart,
	pathfinder: any,
	lastPosition: Vector3,
	lastMoveTime: number,
	isMoving: boolean,
	moveThread: thread?,
	new: (character: Model) -> MovementController,
	Start: (self: MovementController) -> (),
	Stop: (self: MovementController) -> (),
	MoveToRandomLocation: (self: MovementController) -> (),
	CheckIfStuck: (self: MovementController) -> boolean,
	HandleStuck: (self: MovementController) -> (),
	AvoidObstacles: (self: MovementController) -> ()
}

--[[
	Creates a new MovementController instance
	@param character - The NPC character model
	@return MovementController instance
]]
function MovementController.new(character: Model): MovementController
	local self = setmetatable({}, MovementController)
	self.character = character
	self.humanoid = character:FindFirstChildOfClass("Humanoid") :: Humanoid
	self.humanoidRootPart = character:FindFirstChild("HumanoidRootPart") :: BasePart
	self.pathfinder = PathfindingModule.new(character)
	self.lastPosition = self.humanoidRootPart.Position
	self.lastMoveTime = tick()
	self.isMoving = false
	self.moveThread = nil
	
	-- Set walk speed
	self.humanoid.WalkSpeed = Config.WalkSpeed
	
	return self
end

--[[
	Starts the movement controller
]]
function MovementController:Start()
	if self.isMoving then
		return
	end
	
	self.isMoving = true
	
	self.moveThread = task.spawn(function()
		while self.isMoving do
			-- Check for obstacles before moving
			self:AvoidObstacles()
			
			-- Move to random location
			self:MoveToRandomLocation()
			
			-- Check if stuck
			if self:CheckIfStuck() then
				self:HandleStuck()
			end
			
			-- Wait before next movement
			task.wait(Config.PathUpdateInterval)
		end
	end)
	
	if Config.DebugMode then
		print("[MovementController] Started for", self.character.Name)
	end
end

--[[
	Stops the movement controller
]]
function MovementController:Stop()
	self.isMoving = false
	if self.moveThread then
		task.cancel(self.moveThread)
		self.moveThread = nil
	end
	
	self.pathfinder:StopPath()
	
	if Config.DebugMode then
		print("[MovementController] Stopped for", self.character.Name)
	end
end

--[[
	Moves to a random location within wander distance
]]
function MovementController:MoveToRandomLocation()
	local destination = self.pathfinder:GetRandomDestination()
	
	if Config.DebugMode then
		print("[MovementController] Moving to:", destination)
	end
	
	-- Store position before movement
	self.lastPosition = self.humanoidRootPart.Position
	self.lastMoveTime = tick()
	
	-- Compute and follow path
	if self.pathfinder:ComputePath(destination) then
		self.pathfinder:FollowPath()
	else
		if Config.DebugMode then
			warn("[MovementController] Failed to compute path, choosing new destination")
		end
	end
end

--[[
	Checks if the robot is stuck
	@return boolean - True if stuck, false otherwise
]]
function MovementController:CheckIfStuck(): boolean
	local currentTime = tick()
	local timeSinceLastMove = currentTime - self.lastMoveTime
	
	-- Only check if enough time has passed
	if timeSinceLastMove < Config.StuckThreshold then
		return false
	end
	
	-- Check distance moved
	local distanceMoved = (self.humanoidRootPart.Position - self.lastPosition).Magnitude
	
	if distanceMoved < Config.StuckCheckDistance then
		if Config.DebugMode then
			print("[MovementController] Robot is stuck! Distance moved:", distanceMoved)
		end
		return true
	end
	
	return false
end

--[[
	Handles stuck situation by changing direction
]]
function MovementController:HandleStuck()
	if Config.DebugMode then
		print("[MovementController] Handling stuck situation")
	end
	
	-- Stop current path
	self.pathfinder:StopPath()
	
	-- Find best direction without obstacles
	local bestDirection = ObstacleDetection.FindBestDirection(self.humanoidRootPart)
	
	if bestDirection then
		-- Turn to face the new direction
		local newCFrame = CFrame.lookAt(
			self.humanoidRootPart.Position,
			self.humanoidRootPart.Position + bestDirection
		)
		self.humanoidRootPart.CFrame = newCFrame
		
		-- Move in that direction
		local moveDistance = 10
		local newPosition = self.humanoidRootPart.Position + (bestDirection * moveDistance)
		self.humanoid:MoveTo(newPosition)
		
		-- Wait a bit for the movement
		task.wait(2)
		
		-- Update last position
		self.lastPosition = self.humanoidRootPart.Position
		self.lastMoveTime = tick()
	else
		-- All directions blocked, rotate randomly
		local randomAngle = math.random() * math.pi * 2
		self.humanoidRootPart.CFrame = self.humanoidRootPart.CFrame * CFrame.Angles(0, randomAngle, 0)
		
		if Config.DebugMode then
			print("[MovementController] All directions blocked, rotating randomly")
		end
	end
end

--[[
	Checks for obstacles and adjusts direction if needed
]]
function MovementController:AvoidObstacles()
	local hasObstacle, normal = ObstacleDetection.CheckForObstacle(self.humanoidRootPart)
	
	if hasObstacle then
		if Config.DebugMode then
			print("[MovementController] Obstacle detected, avoiding...")
		end
		
		-- Find best direction
		local bestDirection = ObstacleDetection.FindBestDirection(self.humanoidRootPart)
		
		if bestDirection then
			-- Turn away from obstacle
			local turnAngle = math.rad(Config.ObstacleAvoidanceAngle)
			self.humanoidRootPart.CFrame = self.humanoidRootPart.CFrame * CFrame.Angles(0, turnAngle, 0)
		end
	end
end

return MovementController
