import arcade

class Snake(arcade.Sprite):
    def __init__(self, game):
        super().__init__()
        self.width = 16
        self.height = 16
        self.center_x =  game.width // 2 - 10 // 8 * 8
        self.center_y = game.height // 2 - 10 // 8 * 8
        self.color1 = arcade.color.KHAKI
        self.color2 = arcade.color.BROWN
        self.change_x = 1
        self.change_y = 0
        self.speed = 8
        self.score = 0
        self.body = []
        self.snake_score = 1

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, self.color1)
        for part in self.body:
            arcade.draw_rectangle_filled(part["x"], part["y"], self.width, self.height, self.color2)

    def move(self):
        self.body.append({"x":self.center_x,"y":self.center_y})
        if len(self.body)>self.score:
            self.body.pop(0)
        self.center_x += self.speed * self.change_x
        self.center_y += self.speed * self.change_y

    def eat(self, food):
        self.score += 1
        del food