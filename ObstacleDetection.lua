--[[
	ObstacleDetection.lua
	Handles raycasting for obstacle detection and wall avoidance
]]

local Config = require(script.Parent.Config)

local ObstacleDetection = {}

--[[
	Checks if there's an obstacle in front of the robot
	@param humanoidRootPart - The HumanoidRootPart of the NPC
	@param direction - The direction to check (optional, defaults to LookVector)
	@return boolean - True if obstacle detected, false otherwise
	@return Vector3 - Normal of the hit surface (if any)
]]
function ObstacleDetection.CheckForObstacle(humanoidRootPart: BasePart, direction: Vector3?): (boolean, Vector3?)
	local checkDirection = direction or humanoidRootPart.CFrame.LookVector
	local startPosition = humanoidRootPart.Position + Vector3.new(0, Config.RaycastHeight, 0)
	local endPosition = startPosition + (checkDirection * Config.RaycastDistance)
	
	-- Create raycast params
	local raycastParams = RaycastParams.new()
	raycastParams.FilterType = Enum.RaycastFilterType.Exclude
	raycastParams.FilterDescendantsInstances = {humanoidRootPart.Parent}
	
	-- Perform raycast
	local raycastResult = workspace:Raycast(startPosition, checkDirection * Config.RaycastDistance, raycastParams)
	
	if raycastResult then
		if Config.DebugMode then
			print("[ObstacleDetection] Obstacle detected at distance:", (raycastResult.Position - startPosition).Magnitude)
		end
		return true, raycastResult.Normal
	end
	
	return false, nil
end

--[[
	Checks multiple directions around the robot for obstacles
	@param humanoidRootPart - The HumanoidRootPart of the NPC
	@return table - Table of directions and their obstacle status
]]
function ObstacleDetection.CheckAllDirections(humanoidRootPart: BasePart): {[string]: boolean}
	local directions = {
		forward = humanoidRootPart.CFrame.LookVector,
		left = -humanoidRootPart.CFrame.RightVector,
		right = humanoidRootPart.CFrame.RightVector,
	}
	
	local results = {}
	for name, direction in pairs(directions) do
		local hasObstacle, _ = ObstacleDetection.CheckForObstacle(humanoidRootPart, direction)
		results[name] = hasObstacle
	end
	
	return results
end

--[[
	Finds the best direction to move when obstacles are detected
	@param humanoidRootPart - The HumanoidRootPart of the NPC
	@return Vector3 - The best direction to move (or nil if all blocked)
]]
function ObstacleDetection.FindBestDirection(humanoidRootPart: BasePart): Vector3?
	local obstacles = ObstacleDetection.CheckAllDirections(humanoidRootPart)
	
	-- Prefer forward if clear
	if not obstacles.forward then
		return humanoidRootPart.CFrame.LookVector
	end
	
	-- Try left if clear
	if not obstacles.left then
		return -humanoidRootPart.CFrame.RightVector
	end
	
	-- Try right if clear
	if not obstacles.right then
		return humanoidRootPart.CFrame.RightVector
	end
	
	-- If all blocked, try backward
	return -humanoidRootPart.CFrame.LookVector
end

return ObstacleDetection
