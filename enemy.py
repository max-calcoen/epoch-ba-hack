import arcade
from projectile import Projectile

ENEMY_SCALING = 2

# Index of textures, first element faces left, second faces right
TEXTURE_LEFT = 1
TEXTURE_RIGHT = 0

class Enemy(arcade.Sprite):

    def __init__(self, tex_in, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.scale = ENEMY_SCALING
        self.textures = []

        # load right and left facing textures
        # right (original)
        texture = arcade.load_texture(tex_in)
        self.textures.append(texture)
        # left
        texture = arcade.load_texture(tex_in,
                                      flipped_horizontally=True)
        self.textures.append(texture)

        # by default, face left
        self.texture = texture

    def face_right(self):
      self.texture = self.textures[TEXTURE_RIGHT]
    def face_left(self):
      self.texture = self.textures[TEXTURE_LEFT]

    def face_player(self, player_x):
      if player_x > self.x:
        self.face_right()
      else:
        self.face_left()
    def throw_projectile(self):
      new_projectile = Projectile()
      