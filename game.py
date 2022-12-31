import arcade
from player import Player
from screen import Screen

# SCREEN CONSTANTS 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Hypersomnia"
# ======================================

# OBJECT CONSTANTS
TILE_SCALING = 0.5
PLAYER_SPEED = 8.0
PLAYER_JUMP_SPEED = 20.0
GRAVITY = 1.0
BLOCK_SIZE = 32
# ======================================



# LEVELS / SCREENS

tmp = list(range(0, SCREEN_WIDTH, BLOCK_SIZE))
floor = []
for i in tmp:
    floor.append([i, BLOCK_SIZE])
tempf = [*floor]
tempf.pop(7)
tempf.pop(7)
tempf.pop(7)
tempf.pop(7)
tempf.pop(10)
tempf.pop(10)
tempf.pop(10)
tempf.pop(10)
tempf.pop(15)
tempf.pop(15)
tempf.pop(15)
tempf.pop(15)
screens = [
    Screen([*floor, [256, 64], [512, 64], [768, 64]]),
    Screen([*tempf]),
    Screen([*floor]) # include an enemy here
]

s = arcade.Sound("./assets/sounds/theme.wav")

class MainMenu(arcade.View):
    def on_show_view(self):
        arcade.set_background_color((255, 255, 255))
        return
        arcade.set_background_color("assets/blocks/background.png")

    def on_draw(self):
        self.clear()
        font = "04b_19"
        arcade.draw_text("HYPERSOMNIA", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10, (44, 44, 44), font_size=100, font_name=font, anchor_x="center", anchor_y="baseline")
        arcade.draw_text("CLICK TO BEGIN", SCREEN_WIDTH / 2, SCREEN_HEIGHT/2 - 40, (40, 40, 40), font_size=30, font_name=font, anchor_x="center", anchor_y="baseline")
    def on_mouse_press(self, x, y, _button, _modifiers):
        sound = arcade.Sound("./assets/sounds/gui.wav")
        sound.play(volume=0.5)
        sp = arcade.Sound("./assets/sounds/theme.wav")
        sp.play(loop=True, volume=0.1)
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

class MyGame(arcade.View):

    def __init__(self):

        # set up the window
        super().__init__()
        self.scene = None
        self.player_sprite = None
        self.background = None
        self.physics_engine = None
        self.level = 0
        self.facing_left = False


    def setup(self):
        self.clear()
        # create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.blocks_list = arcade.SpriteList(use_spatial_hash=True)

        # initialize Scene and sprite lists
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("Background")
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("blocks", use_spatial_hash=True)

        #backhground
        self.final_background = arcade.Sprite("assets/blocks/FinalBackground.png")
        self.final_background.center_x = SCREEN_HEIGHT / 2 + 250
        self.final_background.center_y = SCREEN_HEIGHT / 2
        self.scene.add_sprite("Background", self.final_background)

        self.scene.add_sprite_list("proj")

        # set up the player
        self.player_sprite = Player("assets/sprites/player.png")
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        
        # CREATING SCENE

        # place blocks down
        current_screen = screens[self.level]
        for coordinate in current_screen.coordinate_map:
            block = arcade.Sprite(
                "assets/blocks/block.png", TILE_SCALING
            )
            block.position = coordinate
            self.scene.add_sprite("Blocks", block)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Blocks"]
        )

    # render
    def on_draw(self):
        self.clear()
        # draw sprites
        self.scene.draw(
            pixelated=True
        )



    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            so = arcade.Sound("./assets/sounds/jump.wav")
            arcade.play_sound(so)
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
            self.player_sprite.face_left()
            self.facing_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED
            self.player_sprite.face_right()
            self.facing_left = True
        elif key == arcade.key.F:
            so = arcade.Sound("./assets/sounds/throw.wav")
            arcade.play_sound(so)
            # fire projectile
            proj = arcade.Sprite("./assets/sprites/projectile_a.png", scale=1.5)
            proj.change_angle = -10
            if self.facing_left:
                proj.change_x = 10
            else:
                proj.change_x = -10
            proj.center_x = self.player_sprite.center_x
            proj.center_y = self.player_sprite.center_y
            self.scene.add_sprite("proj", proj)
            

    def on_key_release(self, key, modifiers):
        # called when the user releases a key.

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        # movement and game logic
        try:
            self.scene.update(["proj"])
            if self.scene.proj >= SCREEN_WIDTH - 32:
                self.scene.remove_sprite_list_by_name("proj")
        except:
            True
        # check if the player has hit the bottom, and send them back to the beginning of the screen
        if self.player_sprite.center_y < 0:
            self.player_sprite.center_x = 50
            self.player_sprite.center_y = 700
        
        
        # move the player with the physics engine
        self.physics_engine.update()
        
        #check right wall
        if self.player_sprite.center_x >= SCREEN_WIDTH - 32:
            # send to left side of screen
            temp = self.player_sprite.center_y
            self.level += 1
            #CHANGE THE LEVEL
            self.setup()

            self.player_sprite.center_y = temp
            self.player_sprite.center_x = 0

def main():
    # Main function
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
