from random import sample
from selection import SelectNumber
from copy import deepcopy # deepcopy which is used to copy the data like list of list [][]....without any references
#GRID NUMBERS
sub_grid_size = 3
full_grid = sub_grid_size * sub_grid_size  


def create_line_coordinates(cell_size : int)->list[list[tuple]]:
   "create the x,y coordinate for drwaing the grid lines"
   points = [] 
   for y in range(1,10):
       #horizontal lines
       temp = []
       temp.append((0,y*cell_size)) #x,y points [(0,100),(0,200),(0,300)......] this example when the cell_size is 100
       temp.append((675,y*cell_size))#x,y points [(800,100),(800,200),(800,300)..........] """to calcuate the pixel gris 9 x cell_size(7) = 675"
       points.append(temp)
       
   for x in range(1,10):
        #vertical line
        temp =[]
        temp.append((x*cell_size,0)) #x,y points [(100,0),(200,0),(300,0)]
        temp.append((x*cell_size,675)) #x,y points [(100,800),(200,800),(300,800).....]
        points.append(temp) 
   print(points)            
   return points  

def pattern(row_num,col_num):
    return (sub_grid_size * (row_num % sub_grid_size) + row_num // sub_grid_size + col_num) % full_grid

def shuffle(sam):
    return sample(sam, len(sam))

def create_grid(sub_grid):
    "create the 9x9 grid filled with random number"
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1,full_grid+1))
    return [[nums[pattern(r,c)] for c in cols] for r in rows]
    
def remove_numbers(grid):
    num_of_cell = full_grid * full_grid
    empties = num_of_cell * 3 // 6 # 7 is ideal - higher this number means easiers game
    for i in sample(range(num_of_cell) , empties):# it will loop n number of time corresponds to empties and values will be selected from the num_of_cell
        grid[i // full_grid][i % full_grid] = 0
    


class Grid:
    def __init__(self, pygame, font):
      self.cell_size = 75
      self.num_x_offset = 35
      self.num_y_offset = 12
      self.line_coordinates = create_line_coordinates(self.cell_size)
      self.grid = create_grid(sub_grid_size) 
      self.__text_grid =  deepcopy(self.grid)#create a copy before removing numbers
      
      remove_numbers(self.grid)
      self.occupied_cell_coordinates = self.pre_occupied_cells()
      #print(self.occupied_cell_coordinates)
      
      self.selection = SelectNumber(pygame,font)
      
      
      self.game_font = font
      
      self.win = False
      
    def check_grid(self):
        #check if all the cells in the main grid nd the test gird are equal ..... the purpose is check whether the match is finished
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__text_grid[y][x]:
                    return False
        return True  
    
    def restart(self):
        self.grid = create_grid(sub_grid_size) 
        self.__text_grid =  deepcopy(self.grid)#create a copy before removing numbers
      
        remove_numbers(self.grid)
        self.occupied_cell_coordinates = self.pre_occupied_cells()
        self.win = False
    
          
    def get_mouse_click(self,x,y) -> None :
          if x <=650:
              grid_x,grid_y = x // 75 , y // 75
              #print(grid_x , grid_y)
              if not self.is_cell_preoccupied(grid_x , grid_y):
                  self.set_cell(grid_x , grid_y, self.selection.selected_number)
          self.selection.button_clicked(x,y)  
          if self.check_grid():
              print("you won the match")
              self.win = True      
     
    def is_cell_preoccupied(self,x,y) -> bool:
        "check whether the cell is empty or filled"
        for cell in self.occupied_cell_coordinates:
            if x == cell[1] and y == cell[0]:
                return True
        return False       
          
      
      
    def pre_occupied_cells(self):
        """Gather the y,x coordinates for all preoccupied/initialized cells."""  
        occupied_cells_coordinates = []
        for y in range(len(self.grid)):
            for x in range (len(self.grid[y])):
               if self.get_cell(x,y) !=0:
                   occupied_cells_coordinates.append((y,x)) # row y and col x in tuple
        return occupied_cells_coordinates           
                    
  
    def __draw_lines(self,pg,surface) -> None: # we are making this as private by using "__"
        for index,line in enumerate(self.line_coordinates):
              #   print("the index is",index)
              #   print("the line is",line)
              if index == 2 or index == 5 or index == 11 or index == 14 :
                  pg.draw.line(surface , (250,200,0) , line[0],line[1])
              else:
                  pg.draw.line(surface,(0,50,0),line[0],line[1])
                  
    def __draw_numbers(self,surface) -> None : # we are making this as private by using "__"
        """Drwa the grid number"""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x,y) != 0:
                    if (y,x) in self.occupied_cell_coordinates:
                        text_surface = self.game_font.render(str(self.get_cell(x,y)),False,(0,200,250)) # The render() method in this context converts a string (or number) into a visual text surface for display in a Pygame application.
                    
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x,y)),False,(0,255,0))
                        
                    if  self.get_cell(x,y) != self.__text_grid[y][x] :
                        text_surface = self.game_font.render(str(self.get_cell(x,y)) , False ,(255,0,0))       
                
                    surface.blit(text_surface , (x* self.cell_size + self.num_x_offset , y* self.cell_size + self.num_y_offset)) # here we can dislpay the number
                
    def draw_all(self,pg,surface):
        self.__draw_lines(pg,surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg ,surface)
        
        
                    
    def get_cell(self,x,y)  ->int :
        """get a cell value at y,x coordinate ."""         
        return self.grid[y][x]
    
    def set_cell(self,x,y,value) -> None:
        "set a cell value at y,x coordinate"
        self.grid[y][x] = value
        
                      
    
    def show(self):
        for cell in self.grid:
            print(cell)    
            
    def fill_all(self,surface) -> None :
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
              if self.get_cell(x, y) == 0 or self.get_cell(x, y) != 0 :  # Check if the cell is empty
                 self.set_cell(x, y, self.__text_grid[y][x])  # Fill the cell with the correct value

                
    #  def fill_all(self,surface) -> None :
    #     for y in range(len(self.grid)):
    #         for x in range(len(self.grid[y])):
    #             if self.get_cell(x,y):
    #                 text_surface = self.game_font.render(str(self.get_cell(x,y)),False,(0,255,200))
    #                 surface.blit(text_surface, (x* self.cell_size + self.num_x_offset , y* self.cell_size + self.num_y_offset))             
                  
# if __name__ == "__main__":
#     grid = Grid()
#     grid.show()   
#     #grid.fill_all(self,surface)                   
            