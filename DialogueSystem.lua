--[[
	DialogueSystem.lua
	Manages random dialogue with chat bubbles
]]

local Config = require(script.Parent.Config)
local ChatService = game:GetService("Chat")

local DialogueSystem = {}
DialogueSystem.__index = DialogueSystem

export type DialogueSystem = {
	character: Model,
	head: BasePart,
	isRunning: boolean,
	dialogueThread: thread?,
	new: (character: Model) -> DialogueSystem,
	Start: (self: DialogueSystem) -> (),
	Stop: (self: DialogueSystem) -> (),
	SayRandomPhrase: (self: DialogueSystem) -> ()
}

--[[
	Creates a new DialogueSystem instance
	@param character - The NPC character model
	@return DialogueSystem instance
]]
function DialogueSystem.new(character: Model): DialogueSystem
	local self = setmetatable({}, DialogueSystem)
	self.character = character
	self.head = character:FindFirstChild("Head") :: BasePart
	self.isRunning = false
	self.dialogueThread = nil
	return self
end

--[[
	Starts the dialogue system with random intervals
]]
function DialogueSystem:Start()
	if self.isRunning then
		return
	end
	
	self.isRunning = true
	
	self.dialogueThread = task.spawn(function()
		while self.isRunning do
			-- Wait random interval between min and max
			local waitTime = math.random(Config.MinDialogueInterval, Config.MaxDialogueInterval)
			task.wait(waitTime)
			
			if self.isRunning then
				self:SayRandomPhrase()
			end
		end
	end)
	
	if Config.DebugMode then
		print("[DialogueSystem] Started for", self.character.Name)
	end
end

--[[
	Stops the dialogue system
]]
function DialogueSystem:Stop()
	self.isRunning = false
	if self.dialogueThread then
		task.cancel(self.dialogueThread)
		self.dialogueThread = nil
	end
	
	if Config.DebugMode then
		print("[DialogueSystem] Stopped for", self.character.Name)
	end
end

--[[
	Says a random phrase from the config
]]
function DialogueSystem:SayRandomPhrase()
	if not self.head or #Config.Phrases == 0 then
		return
	end
	
	local randomIndex = math.random(1, #Config.Phrases)
	local phrase = Config.Phrases[randomIndex]
	
	-- Use ChatService to display chat bubble
	ChatService:Chat(self.head, phrase, Enum.ChatColor.White)
	
	if Config.DebugMode then
		print("[DialogueSystem]", self.character.Name, "says:", phrase)
	end
end

return DialogueSystem
