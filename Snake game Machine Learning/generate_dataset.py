import arcade
import pandas as pd
from Apple import Apple
from Snake import Snake

class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width= width, height= height, title="Super Snake")
        self.background_game = arcade.load_texture("images/Backgrande.png")
        self.flag = 0
        self.snake = Snake(self)
        self.Apple = Apple(self)
        self.dataset = []

    def on_draw(self): 
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background_game)
        
        self.snake.draw()
        self.Apple.draw()
        
        output = f"Score: {self.snake.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLUE, 20)
        
        if self.snake.center_x < 0 or self.snake.center_x > width or self.snake.center_y < 0 or self.snake.center_y > height:
            arcade.draw_text("GAME OVER", width//2, height//2, arcade.color.RED, 5 * 5, width=width, align='left')
            arcade.exit()
        
        arcade.finish_render()

    def on_update(self, delta_time:float):
        self.snake.move()

        # جمع آوری دیتا

        data = {"w0":None, "w1":None, "w2":None, "w3":None,
                "a0":None, "a1":None, "a2":None, "a3":None,
                "b0":None, "b1":None, "b2":None, "b3":None,
                "direction":None}

        # موقعیت سیب نسبت به سر مار

        if self.snake.center_x == self.Apple.center_x and self.snake.center_y < self.Apple.center_y:
            data["a0"] = 1
            data["a1"] = 0
            data["a2"] = 0
            data["a3"] = 0

        elif self.snake.center_x == self.Apple.center_x and self.snake.center_y > self.Apple.center_y:
            data["a0"] = 0
            data["a1"] = 0
            data["a2"] = 1
            data["a3"] = 0

        elif self.snake.center_x < self.Apple.center_x and self.snake.center_y == self.Apple.center_y:
            data["a0"] = 0
            data["a1"] = 1
            data["a2"] = 0
            data["a3"] = 0

        elif self.snake.center_x > self.Apple.center_x and self.snake.center_y == self.Apple.center_y:
            data["a0"] = 0
            data["a1"] = 0
            data["a2"] = 0
            data["a3"] = 1

        # فاصله سر مار تا دیوار ها

        data["w0"] = self.height - self.snake.center_y
        data["w1"] = self.width - self.snake.center_x
        data["w2"] = self.snake.center_y
        data["w3"] = self.snake.center_x

        # موقعیت سر مار نسبت به بدن خودش

        for part in self.snake.body:
            if self.snake.center_x == part["x"] and self.snake.center_y < part["y"]:
                data["b0"] = 1
                data["b1"] = 0
                data["b2"] = 0
                data["b3"] = 0
            
            elif self.snake.center_x == part["x"] and self.snake.center_y > part["y"]:
                data["b0"] = 0
                data["b1"] = 0
                data["b2"] = 1
                data["b3"] = 0
            
            elif self.snake.center_x < part["x"] and self.snake.center_y == part["y"]:
                data["b0"] = 0
                data["b1"] = 1
                data["b2"] = 0
                data["b3"] = 0
            
            elif self.snake.center_x > part["x"] and self.snake.center_y == part["y"]:
                data["b0"] = 0
                data["b1"] = 0
                data["b2"] = 0
                data["b3"] = 1

        self.dataset.append(data)

        if arcade.check_for_collision(self.snake, self.Apple):
            self.snake.eat(self.Apple)  
            self.Apple = Apple(self)
            
        if self.snake.center_y > self.Apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = -1
            data["direction"] = 2
        
        elif self.snake.center_y < self.Apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = 1
            data["direction"] = 0
        
        elif self.snake.center_x > self.Apple.center_x:
            self.snake.change_x = -1
            self.snake.change_y = 0
            data["direction"] = 3
        
        elif self.snake.center_x < self.Apple.center_x:
            self.snake.change_x = 1
            self.snake.change_y = 0
            data["direction"] = 1

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            df = pd.DataFrame(self.dataset)
            df.to_csv("dataset.csv", index=False)
            arcade.close_window()
            exit(0)

width = 800
height = 400

if __name__ == "__main__":
    game = Game(width, height)
    arcade.run()