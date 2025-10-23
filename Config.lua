--[[
	Config.lua
	Configuration module for NPC Robot
	Contains all customizable settings for the robot behavior
]]

local Config = {}

-- Movement Settings
Config.WalkSpeed = 16 :: number -- Speed at which the robot walks
Config.MaxWanderDistance = 50 :: number -- Maximum distance to wander from spawn point
Config.PathUpdateInterval = 2 :: number -- How often to update path (seconds)
Config.StuckThreshold = 3 :: number -- Time before considering robot stuck (seconds)
Config.StuckCheckDistance = 2 :: number -- Minimum distance to move to not be stuck

-- Dialogue Settings
Config.MinDialogueInterval = 10 :: number -- Minimum time between phrases (seconds)
Config.MaxDialogueInterval = 30 :: number -- Maximum time between phrases (seconds)
Config.Phrases = {
	"Hello there! I'm a robot.",
	"Beep boop! Computing...",
	"Nice weather we're having!",
	"I love walking around here.",
	"My sensors are working perfectly.",
	"Analyzing environment...",
	"All systems operational!",
	"Just taking a stroll.",
	"Have you seen my charging station?",
	"Error 404: Coffee not found."
} :: {string}

-- Obstacle Detection Settings
Config.RaycastDistance = 8 :: number -- Distance to check for obstacles
Config.RaycastHeight = 2 :: number -- Height offset for raycasting
Config.ObstacleAvoidanceAngle = 90 :: number -- Angle to turn when avoiding obstacles

-- Fall Detection Settings
Config.FallDistanceThreshold = 50 :: number -- Distance below spawn to trigger respawn
Config.RespawnDelay = 3 :: number -- Delay before respawning (seconds)

-- Debug Settings
Config.DebugMode = false :: boolean -- Enable debug prints

return Config
