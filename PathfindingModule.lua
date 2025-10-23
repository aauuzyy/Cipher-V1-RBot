--[[
	PathfindingModule.lua
	Handles pathfinding using Roblox PathfindingService
]]

local Config = require(script.Parent.Config)
local PathfindingService = game:GetService("PathfindingService")

local PathfindingModule = {}
PathfindingModule.__index = PathfindingModule

export type PathfindingModule = {
	character: Model,
	humanoid: Humanoid,
	humanoidRootPart: BasePart,
	spawnPosition: Vector3,
	currentPath: Path?,
	pathConnection: RBXScriptConnection?,
	new: (character: Model) -> PathfindingModule,
	GetRandomDestination: (self: PathfindingModule) -> Vector3,
	ComputePath: (self: PathfindingModule, destination: Vector3) -> boolean,
	FollowPath: (self: PathfindingModule) -> (),
	StopPath: (self: PathfindingModule) -> ()
}

--[[
	Creates a new PathfindingModule instance
	@param character - The NPC character model
	@return PathfindingModule instance
]]
function PathfindingModule.new(character: Model): PathfindingModule
	local self = setmetatable({}, PathfindingModule)
	self.character = character
	self.humanoid = character:FindFirstChildOfClass("Humanoid") :: Humanoid
	self.humanoidRootPart = character:FindFirstChild("HumanoidRootPart") :: BasePart
	self.spawnPosition = self.humanoidRootPart.Position
	self.currentPath = nil
	self.pathConnection = nil
	return self
end

--[[
	Gets a random destination within the wander distance
	@return Vector3 - Random destination position
]]
function PathfindingModule:GetRandomDestination(): Vector3
	local randomAngle = math.random() * math.pi * 2
	local randomDistance = math.random(10, Config.MaxWanderDistance)
	
	local offset = Vector3.new(
		math.cos(randomAngle) * randomDistance,
		0,
		math.sin(randomAngle) * randomDistance
	)
	
	return self.spawnPosition + offset
end

--[[
	Computes a path to the destination
	@param destination - Target position
	@return boolean - True if path was successfully computed
]]
function PathfindingModule:ComputePath(destination: Vector3): boolean
	-- Create a new path
	self.currentPath = PathfindingService:CreatePath({
		AgentRadius = 2,
		AgentHeight = 5,
		AgentCanJump = true,
		WaypointSpacing = 4,
		Costs = {
			Water = 20
		}
	})
	
	-- Compute the path
	local success, errorMessage = pcall(function()
		self.currentPath:ComputeAsync(self.humanoidRootPart.Position, destination)
	end)
	
	if not success then
		if Config.DebugMode then
			warn("[PathfindingModule] Path computation failed:", errorMessage)
		end
		return false
	end
	
	if self.currentPath.Status == Enum.PathStatus.Success then
		return true
	else
		if Config.DebugMode then
			warn("[PathfindingModule] Path status:", self.currentPath.Status)
		end
		return false
	end
end

--[[
	Follows the computed path
]]
function PathfindingModule:FollowPath()
	if not self.currentPath then
		return
	end
	
	local waypoints = self.currentPath:GetWaypoints()
	
	if #waypoints == 0 then
		return
	end
	
	-- Disconnect previous blocked connection if exists
	if self.pathConnection then
		self.pathConnection:Disconnect()
		self.pathConnection = nil
	end
	
	-- Handle blocked paths
	self.pathConnection = self.currentPath.Blocked:Connect(function(blockedWaypointIndex)
		if blockedWaypointIndex >= 1 then
			if Config.DebugMode then
				print("[PathfindingModule] Path blocked at waypoint", blockedWaypointIndex)
			end
			-- Path is blocked, will need to recompute
			self:StopPath()
		end
	end)
	
	-- Move through waypoints
	for i, waypoint in ipairs(waypoints) do
		if i > 1 then -- Skip the first waypoint (current position)
			-- Handle jump action
			if waypoint.Action == Enum.PathWaypointAction.Jump then
				self.humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
			end
			
			-- Move to waypoint
			self.humanoid:MoveTo(waypoint.Position)
			
			-- Wait for humanoid to reach waypoint or timeout
			local timeout = 5
			local reached = self.humanoid.MoveToFinished:Wait(timeout)
			
			if not reached then
				if Config.DebugMode then
					print("[PathfindingModule] Failed to reach waypoint", i)
				end
				break
			end
		end
	end
	
	if Config.DebugMode then
		print("[PathfindingModule] Reached destination")
	end
end

--[[
	Stops the current path following
]]
function PathfindingModule:StopPath()
	if self.pathConnection then
		self.pathConnection:Disconnect()
		self.pathConnection = nil
	end
	
	self.currentPath = nil
end

return PathfindingModule
