-- LIBS
local Instance = require("src/libs/Instance")
local LogManager = require("src/libs/Debug/LogManager")

local Color = require("src/classes/Color")
local Vector2 = require("src/classes/Vector2")

-- MODULE
local module = {}

local drawId = 0
local Objectpool = {}
module.ScreenSize = Vector2(1280, 1024)

-- METHODS
function module.add(obj, zIndex)
    assert(obj, "Argument #1 missing (Expected object, got nil)")
    assert(obj.draw, "Object doesn't have a draw function. Only add drawable object to the renderer.")
    zIndex = zIndex or 0
    obj.drawId = drawId
    drawId = drawId + 1

    table.insert(Objectpool, {obj = obj, zIndex = zIndex})
    table.sort(Objectpool, function(a, b)
        return a.zIndex < b.zIndex
    end)

    return true
end

function module.rem(obj)
    if not obj.drawId then return end
    for i,v in pairs(Objectpool) do
        if v.obj.drawId == obj.drawId then
            return table.remove(Objectpool, i)
        end
    end
end

function module.changeScreen(newScreen)
    if module.CurrentScreen then
        module.rem(module.CurrentScreen)
        module.CurrentScreen.cleanup()
    end
    
    module.CurrentScreen = newScreen
    module.CurrentScreen.open()
    module.add(module.CurrentScreen)
end

-- EVENTS
function module.update(dt)
    for _,v in pairs(Objectpool) do
        if v.obj.update2 then
            v.obj.update2(dt)
        end
    end
end

function love.draw()
    local time = love.timer.getTime()

    for _,v in pairs(Objectpool) do
        v.obj:draw(time)
    end
    
    love.graphics.setColor(1, 1, 1, .1)
    love.graphics.print("ATS 2022 ©", module.ScreenSize.X - 80, module.ScreenSize.Y - 20)

    module.BackgroundColor:applyBackground()
    LogManager.draw()
end

return module