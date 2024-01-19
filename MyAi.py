from MyBot import Bot
import pickle as pl
import pandas as pd

class BotAI(Bot):
    def __init__(self, number):
        super().__init__(number)
        self.ai = pl.load(open("model5x5.pkl", "rb"))
        
    
    def move(self, board):
        idx =self.ai.predict(self.config_predicted([*board.array.flatten()]))
        while board.array[idx//5][idx%5]:
            idx = self.ai.predict(self.config_predicted([*board.array.flatten()]))
        super().super().make_move(m=idx%5, n=idx//5)
        
        
    def config_predicted(self,lst):
    # Get the column names from the dataframe df
        columns = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,"m","n","k","idx"]
        new_df = pd.DataFrame(columns=columns)
        # Insert the data in lst as a row in the new dataframe
        new_row = pd.DataFrame([lst], columns=columns)
        new_df = pd.concat([new_df, new_row], ignore_index=True)
        return new_df
 
