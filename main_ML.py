import tensorflow as tf
import pandas as pd
import arcade
from Apple import Apple
from Snake import Snake

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width= 800, height= 400, title="Super Snake")
        self.background_game = arcade.load_texture("images/Backgrande.png")
        self.flag = 0
        self.snake = Snake(self)
        self.Apple = Apple(self)
        self.model = tf.keras.models.load_model("snake_model.h5")

    def on_draw(self): 
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background_game)
        
        self.snake.draw()
        self.Apple.draw()
        
        output = f"Score: {self.snake.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLUE, 20)
        
        if self.snake.center_x < 0 or self.snake.center_x > self.width or self.snake.center_y < 0 or self.snake.center_y > self.height:
            arcade.draw_text('GAME OVER', self.width//2, self.height//2, arcade.color.RED, 5 * 5, width=self.width, align='left')
            arcade.exit()
        
        arcade.finish_render()

    def on_update(self, delta_time:float):
        self.snake.move() 
        
        data = {"ws":None, "hs":None, "wa":None, "ha":None,
                "a0":None, "a1":None, "a2":None, "a3":None}

        data["ws"] = self.snake.center_x
        data["hs"] = self.snake.center_y
        data["wa"] = self.Apple.center_x
        data["ha"] = self.Apple.center_y

        if self.snake.center_y < self.Apple.center_y:
            data['a0'] = 1  
            data['a1'] = 0  
            data['a2'] = 0
            data['a3'] = 0
        elif self.snake.center_y > self.Apple.center_y:    
            data['a0'] = 0
            data['a1'] = 0
            data['a2'] = 1
            data['a3'] = 0
        elif self.snake.center_x < self.Apple.center_x:
            data['a0'] = 0
            data['a1'] = 1
            data['a2'] = 0
            data['a3'] = 0
        elif self.snake.center_x > self.Apple.center_x:    
            data['a0'] = 0
            data['a1'] = 0
            data['a2'] = 0
            data['a3'] = 1

        data = pd.DataFrame(data, index=[1])
        data.fillna(0, inplace=True)
        data = data.values
        
        print(data)

        output = self.model.predict(data) 
        direction = output.argmax()
        print(direction)

        if direction == 0:
            self.snake.change_x = 0
            self.snake.change_y = 1
        elif direction == 1:
            self.snake.change_x = 1
            self.snake.change_y = 0
        elif direction == 2:
            self.snake.change_x = 0
            self.snake.change_y = -1
        elif direction == 3:
            self.snake.change_x = -1
            self.snake.change_y = 0

        if arcade.check_for_collision(self.snake, self.Apple):
            self.snake.eat(self.Apple)  
            self.Apple = Apple(self)

if __name__ == "__main__":
    game = Game()
    arcade.run()