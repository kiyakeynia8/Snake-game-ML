import arcade
from Apple import Apple
from Snake import Snake

class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width= width, height= height, title="Super Snake")
        self.background_game = arcade.load_texture("images/Backgrande.png")
        self.flag = 0
        self.snake = Snake(self)
        self.Apple = Apple(self)

    def on_draw(self): 
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background_game)
        
        self.snake.draw()
        self.Apple.draw()
        
        output = f"Score: {self.snake.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLUE, 20)
        
        if self.snake.center_x < 0 or self.snake.center_x > width or self.snake.center_y < 0 or self.snake.center_y > height:
            arcade.draw_text('GAME OVER', width//2, height//2, arcade.color.RED, 5 * 5, width=width, align='left')
            arcade.exit()
        
        arcade.finish_render()

    def on_update(self, delta_time:float):
        self.snake.move() 
        
        if arcade.check_for_collision(self.snake, self.Apple):
            self.snake.eat(self.Apple)  
            self.Apple = Apple(self)
            
        if self.snake.center_y > self.Apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = -1
        
        elif self.snake.center_y < self.Apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = 1
        
        elif self.snake.center_x > self.Apple.center_x:
            self.snake.change_x = -1
            self.snake.change_y = 0
        
        elif self.snake.center_x < self.Apple.center_x:
            self.snake.change_x = 1
            self.snake.change_y = 0

    def on_key_release(self, symbol, modifiers):
        pass

width = 800
height = 400

if __name__ == "__main__":
    game = Game(width, height)
    arcade.run()