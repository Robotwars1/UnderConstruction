import pgzrun
import os
import time

# Makes the game window appear centered on the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Sets window name
TITLE = "UnderConstruction"

# Sets window size
WIDTH = 1600
HEIGHT = 900

# -1 == factory
# 1 == city
area = -1

# Variable for knowing  which button has been pressed
sender = ''

# Bool for stopping movement during the transition animation between areas
Transitioning = False

# Dictionaries for resources
resources = {"Iron_Ore":0, "Copper_Ore":0, "Coal":0, "Clay":0, "Log":0, "Wheat":0, 
             "Pig":0, "Sand":0, "Iron_Ingot":0, "Steel_Ingot":0, "Copper_Ingot":0,
             "Brick":0, "Roof_Tiles":0, "Wood_Beam":0, "Wood_Plank":0, "Flour":0,
             "Bread":0, "Pork":0, "Copper_Wire":0, "Concrete":0}
resources_price = {"Iron_Ore":10, "Copper_Ore":10, "Coal":10, "Clay":10, "Log":10, 
                   "Wheat":10, "Pig":10, "Sand":10, "Iron_Ingot":0, "Steel_Ingot":0, 
                   "Copper_Ingot":0, "Brick":0, "Roof_Tiles":0, "Wood_Beam":0, 
                   "Wood_Plank":0, "Flour":0, "Bread":0, "Pork":0, "Copper_Wire":0, 
                   "Concrete":0}
buy_amount = {"Iron_Ore":'Click to edit', "Copper_Ore":'Click to edit', 
              "Coal":'Click to edit', "Clay":'Click to edit', 
              "Log":'Click to edit', "Wheat":'Click to edit', 
              "Pig":'Click to edit', "Sand":'Click to edit'}
buy_amount_per_second = {"Iron_Ore":False, "Copper_Ore":False, "Coal":False, 
                         "Clay":False, "Log":False, "Wheat":False, "Pig":False, 
                         "Sand":False}
money = 1000000

# Bool for only rendering TradingUI when trading
trading = False

# Bool for if currently changing the amount of a resource to buy
changing_buy_amount = False

# UI Elements
ResourceUI = Actor('resourceui')
ResourceUI.pos = (800, 827.5)

SwitchMap = Actor('to_city')
SwitchMap.pos = (80, 25)

TradingUI = Actor('tradingui')
TradingUI.pos = (WIDTH//2, HEIGHT//2)

TradingUI_closebtn = Actor('tradingui_closebtn')
TradingUI_closebtn.pos = (TradingUI.x + TradingUI.width/2 - TradingUI_closebtn.width/2, TradingUI.y - TradingUI.height/2 + TradingUI_closebtn.height/2)

Checkbox1 = Actor('checkbox_empty')
Checkbox1.pos = (WIDTH//2 - 149.75, HEIGHT//2 - 71.25)

Checkbox2 = Actor('checkbox_empty')
Checkbox2.pos = (WIDTH//2 - 149.75, HEIGHT//2 - 23.75)

Checkbox3 = Actor('checkbox_empty')
Checkbox3.pos = (WIDTH//2 - 149.75, HEIGHT//2 + 23.75)

Checkbox4 = Actor('checkbox_empty')
Checkbox4.pos = (WIDTH//2 - 149.75, HEIGHT//2 + 71.25)

Checkbox5 = Actor('checkbox_empty')
Checkbox5.pos = (WIDTH//2 + 406.75, HEIGHT//2 - 71.25)

Checkbox6 = Actor('checkbox_empty')
Checkbox6.pos = (WIDTH//2 + 406.75, HEIGHT//2 - 23.75)

Checkbox7 = Actor('checkbox_empty')
Checkbox7.pos = (WIDTH//2 + 406.75, HEIGHT//2 + 23.75)

Checkbox8 = Actor('checkbox_empty')
Checkbox8.pos = (WIDTH//2 + 406.75, HEIGHT//2 + 71.25)

# Dictionary for checkbox actors
checkbox_list = {'Iron_Ore':Checkbox1, 'Copper_Ore':Checkbox2, 'Coal':Checkbox3, 
                 'Clay':Checkbox4, 'Log':Checkbox5, 'Wheat':Checkbox6, 
                 'Pig':Checkbox7, 'Sand':Checkbox8}

# Creates sprites behind the amount panels for recongizing clicks
Amount_Iron_Ore = Actor('amount_background')
Amount_Iron_Ore.pos = (WIDTH//2 - 330.5, HEIGHT//2 - 71.25)

Amount_Copper_Ore = Actor('amount_background')
Amount_Copper_Ore.pos = (WIDTH//2 - 330.5, HEIGHT//2 - 23.75)

Amount_Coal = Actor('amount_background')
Amount_Coal.pos = (WIDTH//2 - 330.5, HEIGHT//2 + 23.75)

Amount_Clay = Actor('amount_background')
Amount_Clay.pos = (WIDTH//2 - 330.5, HEIGHT//2 + 71.25)

Amount_Log = Actor('amount_background')
Amount_Log.pos = (WIDTH//2 + 226, HEIGHT//2 - 71.25)

Amount_Wheat = Actor('amount_background')
Amount_Wheat.pos = (WIDTH//2 + 226, HEIGHT//2 - 23.75)

Amount_Pig = Actor('amount_background')
Amount_Pig.pos = (WIDTH//2 + 226, HEIGHT//2 + 23.75)

Amount_Sand = Actor('amount_background')
Amount_Sand.pos = (WIDTH//2 + 226, HEIGHT//2 + 71.25)

# Other Sprites
Player = Actor('player')
Player.pos = (WIDTH//2, HEIGHT//2)

ViewBox = Actor('viewbox')
ViewBox.pos = (WIDTH//2, HEIGHT//2)

TransitionAnimation = Actor('transition_animation')
TransitionAnimation.pos = (WIDTH//2 + TransitionAnimation.width, HEIGHT//2)

#CollisionMap Sprites for limiting movement
CollisionMapUp = Actor('collisionmaphorizontal')
CollisionMapUp.pos = (WIDTH//2, HEIGHT//2 - 1150)

CollisionMapDown = Actor('collisionmaphorizontal')
CollisionMapDown.pos = (WIDTH//2, HEIGHT//2 + 1150)

CollisionMapLeft = Actor('collisionmapvertical')
CollisionMapLeft.pos = (WIDTH//2 - 2025, HEIGHT//2)

CollisionMapRight = Actor('collisionmapvertical')
CollisionMapRight.pos = (WIDTH//2 + 2025, HEIGHT//2)

# Factory Sprites
Factory = Actor('factory')
Factory.pos = (WIDTH//2, HEIGHT//2)

TradingPC = Actor('tradingpc')
TradingPC.pos = (Factory.x - 1600, Factory.y - 875)

# MetalFactory specific sprites
MetalFactory = Actor('basic_factory')
MetalFactory.pos = (WIDTH//2 + 500, HEIGHT//2 + 375)

MetalFactory_UpWall = Actor('basic_factory_horizontal_wall')
MetalFactory_UpWall.pos = (WIDTH//2 + 500, HEIGHT//2 - 337.5)

MetalFactory_DownWall = Actor('basic_factory_horizontal_wall')
MetalFactory_DownWall.pos = (WIDTH//2 + 500, HEIGHT//2 + 1087.5)

MetalFactory_LeftWall = Actor('basic_factory_vertical_wall')
MetalFactory_LeftWall.pos = (WIDTH//2 + 137.5, HEIGHT//2 + 375)

MetalFactory_RightWall = Actor('basic_factory_vertical_wall')
MetalFactory_RightWall.pos = (WIDTH//2 + 862.5, HEIGHT//2 + 375)

MetalFactory_Conveyor = Actor('metal_factory_conveyor')
MetalFactory_Conveyor.pos = (WIDTH//2 + 1187.5, HEIGHT//2 + 425)

MetalFactory_buyUI = Actor('buyui')
MetalFactory_buyUI.pos = (MetalFactory.x, MetalFactory.y)

MetalFactory_buyUI_buybtn = Actor('buyui_buybtn')
MetalFactory_buyUI_buybtn.pos = (MetalFactory_buyUI.x, MetalFactory_buyUI.y + 118.75)

MetalFactory_IronSmelter = Actor('metal_factory_smelter')
MetalFactory_IronSmelter.pos = (MetalFactory.x - 200, MetalFactory.y - 450)

MetalFactory_CopperSmelter = Actor('metal_factory_smelter')
MetalFactory_CopperSmelter.pos = (MetalFactory.x + 200, MetalFactory.y - 450)

MetalFactory_SteelSmelter = Actor('metal_factory_smelter')
MetalFactory_SteelSmelter.pos = (MetalFactory.x - 200, MetalFactory.y + 450)
MetalFactory_SteelSmelter.angle = 180 # Rotates the sprite 180 degrees

MetalFactory_BrickFurnace = Actor('metal_factory_smelter')
MetalFactory_BrickFurnace.pos = (MetalFactory.x + 200, MetalFactory.y + 450)
MetalFactory_BrickFurnace.angle = 180 # Rotates the sprite 180 degrees

MetalFactory_buyUI_text = 'Metal Factory'

# WoodFactory specific sprites
WoodFactory = Actor('basic_factory')
WoodFactory.pos = (WIDTH//2 - 550, HEIGHT//2 + 375)

WoodFactory_UpWall = Actor('basic_factory_horizontal_wall')
WoodFactory_UpWall.pos = (WoodFactory.x, WoodFactory.y - 712.5)

WoodFactory_DownWall = Actor('basic_factory_horizontal_wall')
WoodFactory_DownWall.pos = (WoodFactory.x, WoodFactory.y + 712.5)

WoodFactory_LeftWall = Actor('basic_factory_vertical_wall')
WoodFactory_LeftWall.pos = (WoodFactory.x - 362.5, WoodFactory.y)

WoodFactory_RightWall = Actor('basic_factory_vertical_wall')
WoodFactory_RightWall.pos = (WoodFactory.x + 362.5, WoodFactory.y)

WoodFactory_Conveyor = Actor('straight_conveyor')
WoodFactory_Conveyor.pos = (WIDTH//2 - 25, HEIGHT//2 + 337.5)

WoodFactory_buyUI = Actor('buyui')
WoodFactory_buyUI.pos = (WoodFactory.x, WoodFactory.y)

WoodFactory_buyUI_buybtn = Actor('buyui_buybtn')
WoodFactory_buyUI_buybtn.pos = (WoodFactory_buyUI.x, WoodFactory_buyUI.y + 118.75)

WoodFactory_BeamSaw = Actor('beam_saw')
WoodFactory_BeamSaw.pos = (WoodFactory.x, WoodFactory.y + 412.5)

WoodFactory_PlankSaw = Actor('plank_saw')
WoodFactory_PlankSaw.pos = (WoodFactory.x, WoodFactory.y - 587.5)

WoodFactory_buyUI_text = 'Wood Factory'

# Dictionary for seeing if a building should produce materials or not
MetalFactory_Producers = {MetalFactory_IronSmelter:False, MetalFactory_CopperSmelter:False, MetalFactory_SteelSmelter:False, MetalFactory_BrickFurnace:False}
WoodFactory_Producers = {WoodFactory_BeamSaw:False, WoodFactory_PlankSaw:False}

# Int for setting the MetalFactory_buyUI to correct state
# Stage 0 = Nothing built, Stage 1 = MetalFactory, Stage 2 = Conveyor, Stage 3 = Iron Smelter, Stage 4 = Copper Smelter, Stage 5 = Steel Smelter, Stage 6 = Brick Furnace
MetalFactory_Stage = 0

# Int for setting the WoodFactory_buyUI to correct state
# Stage 0 = Nothing built, Stage 1 = WoodFactory, Stage 2 = Conveyor
WoodFactory_Stage = 0

# List of sprites in factory map to make it easier to move around
Factory_Sprites = [Factory, TradingPC, CollisionMapUp, CollisionMapDown, CollisionMapLeft, CollisionMapRight, 
                   MetalFactory, MetalFactory_UpWall, MetalFactory_DownWall, MetalFactory_LeftWall, MetalFactory_RightWall, MetalFactory_buyUI, MetalFactory_buyUI_buybtn, MetalFactory_Conveyor,
                   MetalFactory_IronSmelter, MetalFactory_CopperSmelter, MetalFactory_SteelSmelter, MetalFactory_BrickFurnace,
                   WoodFactory, WoodFactory_UpWall, WoodFactory_DownWall, WoodFactory_LeftWall, WoodFactory_RightWall, WoodFactory_buyUI, WoodFactory_buyUI_buybtn, WoodFactory_Conveyor,
                   WoodFactory_BeamSaw, WoodFactory_PlankSaw]
# List of sprites in factory map that should be rendered and bool for if they should be rendered or not, sets them in order so things go above or below the player sprite as they should
Factory_Sprites_Render = {Factory:True, TradingPC:True, MetalFactory:False, MetalFactory_UpWall:False, MetalFactory_DownWall:False, MetalFactory_LeftWall:False, 
                          MetalFactory_RightWall:False, MetalFactory_buyUI:True, MetalFactory_IronSmelter:False, MetalFactory_CopperSmelter:False, MetalFactory_SteelSmelter:False, 
                          MetalFactory_BrickFurnace:False,
                          WoodFactory:False, WoodFactory_UpWall:False, WoodFactory_DownWall:False, WoodFactory_LeftWall:False, WoodFactory_RightWall:False, WoodFactory_buyUI:True,
                          WoodFactory_BeamSaw:False, WoodFactory_PlankSaw:False,
                          Player:True, MetalFactory_Conveyor:False, WoodFactory_Conveyor:False}

# City Sprites
City = Actor('city')
City.pos = (WIDTH//2, HEIGHT//2)

def draw():
    screen.clear()
    if area == -1:
        # Draw sprites in factory area
        for sprite in Factory_Sprites_Render:
            #If the sprite should be rendered and if they are visible on screen
            if Factory_Sprites_Render[sprite] and ViewBox.colliderect(sprite):
                sprite.draw()
            if sprite == MetalFactory_buyUI and Factory_Sprites_Render[MetalFactory_buyUI]:
                screen.draw.text(MetalFactory_buyUI_text, center=(MetalFactory_buyUI_buybtn.x, MetalFactory_buyUI_buybtn.y - 237.5), fontsize=40)
                #screen.draw.text() # First row resource
                #screen.draw.text() # Second row resource
                #screen.draw.text() # Third row resource
                #screen.draw.text() # Fourth row resource
                screen.draw.text('Buy', center=(MetalFactory_buyUI_buybtn.x, MetalFactory_buyUI_buybtn.y), fontsize=40) # Buy button
            if sprite == WoodFactory_buyUI and Factory_Sprites_Render[WoodFactory_buyUI]:
                screen.draw.text(WoodFactory_buyUI_text, center=(WoodFactory_buyUI_buybtn.x, WoodFactory_buyUI_buybtn.y - 237.5), fontsize=40)
                #screen.draw.text() # First row resource
                #screen.draw.text() # Second row resource
                #screen.draw.text() # Third row resource
                #screen.draw.text() # Fourth row resource
                screen.draw.text('Buy', center=(WoodFactory_buyUI_buybtn.x, WoodFactory_buyUI_buybtn.y), fontsize=40) # Buy button
    else:
        # Draw city area
        City.draw()
        Player.draw()
    # Draw UI elements
    SwitchMap.draw()
    ResourceUI.draw()
    # Draw TradingUI with close button and text
    if trading:
        TradingUI.draw()
        TradingUI_closebtn.draw()
        Checkbox1.draw()
        Checkbox2.draw()
        Checkbox3.draw()
        Checkbox4.draw()
        Checkbox5.draw()
        Checkbox6.draw()
        Checkbox7.draw()
        Checkbox8.draw()
        Amount_Iron_Ore.draw()
        # Amount text
        screen.draw.text(f'{buy_amount["Iron_Ore"]}', midleft=(325, 378.125), fontsize=40)
        screen.draw.text(f'{buy_amount["Copper_Ore"]}', midleft=(325, 425.625), fontsize=40)
        screen.draw.text(f'{buy_amount["Coal"]}', midleft=(325, 473.125), fontsize=40)
        screen.draw.text(f'{buy_amount["Clay"]}', midleft=(325, 520.625), fontsize=40)
        screen.draw.text(f'{buy_amount["Log"]}', midleft=(881.5, 378.125), fontsize=40)
        screen.draw.text(f'{buy_amount["Wheat"]}', midleft=(881.5, 425.625), fontsize=40)
        screen.draw.text(f'{buy_amount["Pig"]}', midleft=(881.5, 473.125), fontsize=40)
        screen.draw.text(f'{buy_amount["Sand"]}', midleft=(881.5, 520.625), fontsize=40)
        # Price text
        screen.draw.text(f'{resources_price["Iron_Ore"]}', midleft=(706.5, 378.125), fontsize=40)
        screen.draw.text(f'{resources_price["Copper_Ore"]}', midleft=(706.5, 425.625), fontsize=40)
        screen.draw.text(f'{resources_price["Coal"]}', midleft=(706.5, 473.125), fontsize=40)
        screen.draw.text(f'{resources_price["Clay"]}', midleft=(706.5, 520.625), fontsize=40)
        screen.draw.text(f'{resources_price["Log"]}', midleft=(1262.5, 378.125), fontsize=40)
        screen.draw.text(f'{resources_price["Wheat"]}', midleft=(1262.5, 425.625), fontsize=40)
        screen.draw.text(f'{resources_price["Pig"]}', midleft=(1262.5, 473.125), fontsize=40)
        screen.draw.text(f'{resources_price["Sand"]}', midleft=(1262.5, 520.625), fontsize=40)
    # Draw resource count in ResourceUI
    # Row 1
    screen.draw.text(f'{money}', midleft=(40, 779.75), fontsize=40)
    # Row 2
    screen.draw.text(f'{resources["Iron_Ore"]}', midleft=(50, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Copper_Ore"]}', midleft=(209.5, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Coal"]}', midleft=(369, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Clay"]}', midleft=(528.5, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Log"]}', midleft=(688, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Wheat"]}', midleft=(847.5, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Pig"]}', midleft=(1007, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Sand"]}', midleft=(1166.5, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Iron_Ingot"]}', midleft=(1326, 827.25), fontsize=40)
    screen.draw.text(f'{resources["Steel_Ingot"]}', midleft=(1485.5, 827.25), fontsize=40)
    # Row 3
    screen.draw.text(f'{resources["Copper_Ingot"]}', midleft=(50, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Brick"]}', midleft=(209.5, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Roof_Tiles"]}', midleft=(369, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Wood_Beam"]}', midleft=(528.5, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Wood_Plank"]}', midleft=(688, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Flour"]}', midleft=(847, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Bread"]}', midleft=(1007, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Pork"]}', midleft=(1166.5, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Copper_Wire"]}', midleft=(1326, 875.75), fontsize=40)
    screen.draw.text(f'{resources["Concrete"]}', midleft=(1485.5, 875.75), fontsize=40)
    # If transition animation is playing, draw the transition animation. Draws last to overlap / hide everything
    if Transitioning:
        TransitionAnimation.draw()

def update():
    # If in factory area
    if area == -1 and not Transitioning:
        if keyboard.w and not Player.colliderect(CollisionMapUp):
            for sprite in Factory_Sprites:
                sprite.y += 5
        if keyboard.s and not Player.colliderect(CollisionMapDown):
            for sprite in Factory_Sprites:
                sprite.y -= 5
        if keyboard.a and not Player.colliderect(CollisionMapLeft):
            for sprite in Factory_Sprites:
                sprite.x += 5
        if keyboard.d and not Player.colliderect(CollisionMapRight):
            for sprite in Factory_Sprites:
                sprite.x -= 5
    # If in city area
    elif area == 1 and not Transitioning:
        if keyboard.w:
            City.y += 5
        if keyboard.s:
            City.y -= 5
        if keyboard.a:
            City.x += 5
        if keyboard.d:
            City.x -= 5

# Checks where on screen you pressed
def on_mouse_down(pos):
    # If pressed on SwitchMap sprite then call the function for changing current area
    if SwitchMap.collidepoint(pos):
        change_area()
    global sender
    # If pressed on a checkbox in tradeUI, call the function to change appropriate stuff
    if Checkbox1.collidepoint(pos) and trading:
        sender = 'Iron_Ore'
        checkbox_pressed()
    elif Checkbox2.collidepoint(pos) and trading:
        sender = 'Copper_Ore'
        checkbox_pressed()
    elif Checkbox3.collidepoint(pos) and trading:
        sender = 'Coal'
        checkbox_pressed()
    elif Checkbox4.collidepoint(pos) and trading:
        sender = 'Clay'
        checkbox_pressed()
    elif Checkbox5.collidepoint(pos) and trading:
        sender = 'Log'
        checkbox_pressed()
    elif Checkbox6.collidepoint(pos) and trading:
        sender = 'Wheat'
        checkbox_pressed()
    elif Checkbox7.collidepoint(pos) and trading:
        sender = 'Pig'
        checkbox_pressed()
    elif Checkbox8.collidepoint(pos) and trading:
        sender = 'Sand'
        checkbox_pressed()
    # If pressed on an amount_background in tradeUI, call the function to change trade amount
    if Amount_Iron_Ore.collidepoint(pos) and trading:
        sender = 'Iron_Ore'
        amountback_pressed()
    elif Amount_Copper_Ore.collidepoint(pos) and trading:
        sender = 'Copper_Ore'
        amountback_pressed()
    elif Amount_Coal.collidepoint(pos) and trading:
        sender = 'Coal'
        amountback_pressed()
    elif Amount_Clay.collidepoint(pos) and trading:
        sender = 'Clay'
        amountback_pressed()
    elif Amount_Log.collidepoint(pos) and trading:
        sender = 'Log'
        amountback_pressed()
    elif Amount_Wheat.collidepoint(pos) and trading:
        sender = 'Wheat'
        amountback_pressed()
    elif Amount_Pig.collidepoint(pos) and trading:
        sender = 'Pig'
        amountback_pressed()
    elif Amount_Sand.collidepoint(pos) and trading:
        sender = 'Sand'
        amountback_pressed()
    # If pressed on the buy button on MetalFactory_buyUI, call the function to buy the correct building/item
    if MetalFactory_Stage < 6 and MetalFactory_buyUI_buybtn.collidepoint(pos):
        MetalFactory_build()
    elif WoodFactory_Stage < 4 and WoodFactory_buyUI_buybtn.collidepoint(pos):
        WoodFactory_build()
    # If pressed on TradingPC sprite then call the function to open tradeUI
    if TradingPC.collidepoint(pos):
        tradeui_open()
        return
    # If pressed on TradeUI_closebtn sprite then call the function to close tradeUI
    if TradingUI_closebtn.collidepoint(pos):
        tradeui_close()

# Starts the changing of current area, starts the first animation
def change_area():
    global Transitioning
    Transitioning = True
    animate(TransitionAnimation, pos=(WIDTH//2, HEIGHT//2), duration=2, tween='accel_decel', on_finished=change_area_2)

# Changes current area and starts the second animation
def change_area_2():
    global area
    area *= -1
    animate(TransitionAnimation, pos=(WIDTH//2 + TransitionAnimation.width, HEIGHT//2), duration=2, tween='accel_decel', on_finished=change_area_3)

# Changes SwitchMap text and sets bool to stop transitioning
def change_area_3():
    global SwithcMap
    global Transitioning
    if area == 1:
        SwithcMap = Actor('to_factory')
    else:
        SwitchMap = Actor('to_city')
    Transitioning = False

# Buys buildings / items, enables the bought buildings / items and makes sure they are rendered / drawn
def MetalFactory_build():
    global MetalFactory_Stage
    global MetalFactory_buyUI_text
    MetalFactory_Stage += 1
    if MetalFactory_Stage == 1:
        # Sets the bought building to be drawn
        Factory_Sprites_Render[MetalFactory] = True
        Factory_Sprites_Render[MetalFactory_UpWall] = True
        Factory_Sprites_Render[MetalFactory_DownWall] = True
        Factory_Sprites_Render[MetalFactory_LeftWall] = True
        Factory_Sprites_Render[MetalFactory_RightWall] = True
        MetalFactory_buyUI_text = 'Conveyor'
    elif MetalFactory_Stage == 2:
        # Sets the bought building to be drawn
        Factory_Sprites_Render[MetalFactory_Conveyor] = True
        MetalFactory_buyUI_text = 'Iron Smelter'
    elif MetalFactory_Stage == 3:
        Factory_Sprites_Render[MetalFactory_IronSmelter] = True
        MetalFactory_Producers[MetalFactory_IronSmelter] = True
        MetalFactory_buyUI_text = 'Copper Smelter'
    elif MetalFactory_Stage == 4:
        Factory_Sprites_Render[MetalFactory_CopperSmelter] = True
        MetalFactory_Producers[MetalFactory_CopperSmelter] = True
        MetalFactory_buyUI_text = 'Steel Smelter'
    elif MetalFactory_Stage == 5:
        Factory_Sprites_Render[MetalFactory_SteelSmelter] = True
        MetalFactory_Producers[MetalFactory_SteelSmelter] = True
        MetalFactory_buyUI_text = 'Brick Furnace'
    elif MetalFactory_Stage == 6:
        Factory_Sprites_Render[MetalFactory_BrickFurnace] = True
        MetalFactory_Producers[MetalFactory_BrickFurnace] = True
        Factory_Sprites_Render[MetalFactory_buyUI] = False

# Buys buildings / items, enables the bought buildings / items and makes sure they are rendered / drawn
def WoodFactory_build():
    global WoodFactory_Stage
    global WoodFactory_buyUI_text
    WoodFactory_Stage += 1
    if WoodFactory_Stage == 1:
        # Sets the bought building to be drawn
        Factory_Sprites_Render[WoodFactory] = True
        Factory_Sprites_Render[WoodFactory_UpWall] = True
        Factory_Sprites_Render[WoodFactory_DownWall] = True
        Factory_Sprites_Render[WoodFactory_LeftWall] = True
        Factory_Sprites_Render[WoodFactory_RightWall] = True
        WoodFactory_buyUI_text = 'Conveyor'
    elif WoodFactory_Stage == 2:
        # Sets the bought building to be drawn
        Factory_Sprites_Render[WoodFactory_Conveyor] = True
        WoodFactory_buyUI_text = 'Beam Saw'
    elif WoodFactory_Stage == 3:
        # Sets the bought building to be drawn
        Factory_Sprites_Render[WoodFactory_BeamSaw] = True
        WoodFactory_Producers[WoodFactory_BeamSaw] = True
        WoodFactory_buyUI_text = 'Plank Saw'
    elif WoodFactory_Stage == 4:
        # Sets the bought building to be drawn
        Factory_Sprites_Render[WoodFactory_PlankSaw] = True
        WoodFactory_Producers[WoodFactory_PlankSaw] = True
        Factory_Sprites_Render[WoodFactory_buyUI] = False

# Makes the tradeUI render when opened
def tradeui_open():
    global trading
    trading = True

# Makes the tradeUI not render when closed
def tradeui_close():
    global trading
    trading = False
    if changing_buy_amount:
        stop_trading()
    else:
        resource_buy()

# Changes the tradeUI checkbox sprite and 
# acompanying bool for if that resource should be bought per second
def checkbox_pressed():
    for checkbox in checkbox_list:
        if checkbox == sender:
            global buy_amount_per_second
            if checkbox_list[checkbox].image == 'checkbox_checkmark':
                checkbox_list[checkbox].image = 'checkbox_empty'
                buy_amount_per_second[checkbox] = False
            else:
                checkbox_list[checkbox].image = 'checkbox_checkmark'
                buy_amount_per_second[checkbox] = True

# Sets bool to allow changing of given material to buy
def amountback_pressed():
    global changing_buy_amount
    changing_buy_amount = True
    if buy_amount[sender] == 'Click to edit':
        buy_amount[sender] = ''

# Checks if a key is pressed
def on_key_down(key, unicode):
    if changing_buy_amount:
        buy_amount_change(key, unicode)

# Changes amount of a given material to buy
def buy_amount_change(key, unicode):
    global buy_amount
    # If the pressed key is enter, stop trading and remove non-numbers from the string
    if key == 13:
        global changing_buy_amount
        changing_buy_amount = False
        # Remove the non-numbers from the string
        for char in buy_amount[sender]:
            if char.isdigit() == False:
                buy_amount[sender] = buy_amount[sender].replace(f'{char}', '')
    # If the pressed key is backspace, remove the last char from string
    elif key == 8:
        buy_amount[sender] = buy_amount[sender][:-1]
    # If pressed key is not enter or backspace, add char to string
    else:   
        buy_amount[sender] += unicode

# If closed the tradeUi, stop trading and remove non-numbers from the string
def stop_trading():
    global buy_amount
    global changing_buy_amount
    changing_buy_amount = False
    # Remove the non-numbers from the string
    for char in buy_amount[sender]:
        if char.isdigit() == False:
            buy_amount[sender] = buy_amount[sender].replace(f'{char}', '')
    resource_buy()

# Buys the resources, when tradeUI is closed
def resource_buy():
    global resources
    global money
    for resource in buy_amount:
        # If buy amount of given resource is not set to per second and is a number
        if not buy_amount_per_second[resource] and buy_amount[resource].isdigit():
            # If you dont have enough money to buy resources, set buy amount to 0 
            if money < int(buy_amount[resource]) * int(resources_price[resource]):
                buy_amount[resource] = 'Click to edit'
            else:
                resources[resource] += int(buy_amount[resource])
                money -= int(buy_amount[resource]) * resources_price[resource]
                buy_amount[resource] = 'Click to edit'

# Buys the resources, per second
def resource_buy_per_second():
    global resources
    global money
    for resource in buy_amount_per_second:
        # If buy amount for given resource is set to per second and is a number and the tradeUI is closed
        if buy_amount_per_second[resource] and buy_amount[resource].isdigit():
            # If you dont have enough money to buy resources, set buy amount to 0 
            if money < int(buy_amount[resource]) * int(resources_price[resource]):
                buy_amount[resource] = 'Click to edit'
            else:
                resources[resource] += int(buy_amount[resource])
                money -= int(buy_amount[resource]) * resources_price[resource]
        else:
            buy_amount[resource] = 'Click to edit'

# Function that consumes and produces correct resources
def metalfactory_resource_produce():
    global resources
    for producer in MetalFactory_Producers:
        if MetalFactory_Producers[producer]: # If the producer is True, eg meant to produce material
            if producer == MetalFactory_IronSmelter and resources['Iron_Ore'] > 1:
                resources['Iron_Ore'] -= 1
                resources['Iron_Ingot'] += 1
            elif producer == MetalFactory_CopperSmelter and resources['Copper_Ore'] > 1:
                resources['Copper_Ore'] -= 1
                resources['Copper_Ingot'] += 1
            elif producer == MetalFactory_SteelSmelter and resources['Iron_Ore'] > 2 and resources['Coal'] > 1:
                resources['Iron_Ore'] -= 2
                resources['Coal'] -= 1
                resources['Steel_Ingot'] += 1
            elif producer == MetalFactory_BrickFurnace and resources['Clay'] > 1:
                resources['Clay'] -= 1
                resources['Brick'] += 1

# Function that consumes and produces correct resources
def woodfactory_resource_produce():
    global resources
    for producer in WoodFactory_Producers:
        if WoodFactory_Producers[producer]: # If the producer is True, eg meant to produce material
            if producer == WoodFactory_BeamSaw and resources['Log'] > 1:
                resources['Log'] -= 1
                resources['Wood_Beam'] += 2
            elif producer == WoodFactory_PlankSaw and resources['Wood_Beam'] > 1:
                resources['Wood_Beam'] -= 1
                resources['Wood_Plank'] += 4

# Schedules the resource_buy function to be called every second
clock.schedule_interval(resource_buy_per_second, 1)

# Schedules the metalfactory_resource_production to be called every second
clock.schedule_interval(metalfactory_resource_produce, 1)

# Schedules the woodfactory_resource_produce to be called every second
clock.schedule_interval(woodfactory_resoruce_produce, 1)

# Runs the game
pgzrun.go()