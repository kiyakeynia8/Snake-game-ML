import random
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
        self.apple = Apple(self)
        self.dataset = []

    def on_draw(self): 
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background_game)
        
        self.snake.draw()
        self.apple.draw()
        
        output = f"Score: {self.snake.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLUE, 20)
        
        if self.snake.center_x < 0 or self.snake.center_x > width or self.snake.center_y < 0 or self.snake.center_y > height:
            arcade.draw_text("GAME OVER", width//2, height//2, arcade.color.RED, 5 * 5, width=width, align='left')
            arcade.exit()
        
        arcade.finish_render()

    def on_update(self, delta_time:float):
        self.snake.move()

        data = {"ws":None, "hs":None, "wa":None, "ha":None,
                "a0":None, "a1":None, "a2":None, "a3":None,
                "direction":None}

        data["ws"] = self.snake.center_x
        data["hs"] = self.snake.center_y
        data["wa"] = self.apple.center_x
        data["ha"] = self.apple.center_y

        if self.snake.center_y < self.apple.center_y:
            data['a0'] = 1  
            data['a1'] = 0  
            data['a2'] = 0
            data['a3'] = 0
        elif self.snake.center_y > self.apple.center_y:    
            data['a0'] = 0
            data['a1'] = 0
            data['a2'] = 1
            data['a3'] = 0
        elif self.snake.center_x < self.apple.center_x:
            data['a0'] = 0
            data['a1'] = 1
            data['a2'] = 0
            data['a3'] = 0
        elif self.snake.center_x > self.apple.center_x:    
            data['a0'] = 0
            data['a1'] = 0
            data['a2'] = 0
            data['a3'] = 1

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat(self.apple)  
            self.apple = Apple(self)
            
        if self.snake.center_y > self.apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = -1
            data["direction"] = 2        
        elif self.snake.center_y < self.apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = 1
            data["direction"] = 0        
        elif self.snake.center_x > self.apple.center_x:
            self.snake.change_x = -1
            self.snake.change_y = 0
            data["direction"] = 3        
        elif self.snake.center_x < self.apple.center_x:
            self.snake.change_x = 1
            self.snake.change_y = 0
            data["direction"] = 1

        if len(self.dataset) < 3:
            self.dataset.append(data)

        elif self.dataset[-1]["direction"] != data["direction"] or random.random() < 0.05:
                self.dataset.append(data)

        print(len(self.dataset))

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