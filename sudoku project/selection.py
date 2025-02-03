
class SelectNumber:
    def __init__(self,pygame,font):
        self.pygame = pygame
        self.btn_w = 80 #button width
        self.btn_h = 80 #button height
        self.my_font = font
        self.selected_number = 0
        
        self.color_selected = (0,255,0)
        self.color_normal = (200,200,200)
        
        self.btn_position = [(950,50),(1050,50),(950,150),(1050,150),(950,250),(1050,250),(950,350),(1050,350),(1050,450)]
        
    def draw(self , pygame , surface):
        for index , pos in enumerate(self.btn_position):
            pygame.draw.rect(surface,self.color_normal,[pos[0],pos[1],self.btn_w,self.btn_h], width = 3 , border_radius = 10 )
            
            #checking for mouse hover
            if self.button_hover(pos):
                pygame.draw.rect(surface,self.color_selected,[pos[0],pos[1],self.btn_w,self.btn_h],width = 3 , border_radius = 10 )
                text_surface = self.my_font.render(str(index+1),False,(0,255,0))
            else:
                text_surface = self.my_font.render(str(index+1),False,self.color_normal)
                
            #check the number was selected , then draw a green
            if self.selected_number > 0 :
                if self.selected_number - 1 == index:
                    pygame.draw.rect(surface,self.color_selected,[pos[0],pos[1],self.btn_w,self.btn_h],width=3,border_radius=10)
                    text_surface = self.my_font.render(str(index+1),False,self.color_selected)
                    
            surface.blit(text_surface , (pos[0]+ 26,pos[1]+26))
    
    def button_clicked(self,mouse_x,mouse_y) -> None:
        for index,pos in enumerate(self.btn_position):
            if self.on_button(mouse_x,mouse_y,pos):
                self.selected_number = index + 1
    
    
    def button_hover(self,pos) -> bool | None :
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0],mouse_pos[1],pos):
            return True
    
            
    def on_button(self,mouse_x,mouse_y,pos) -> bool :
        return pos[0] < mouse_x < pos[0]+self.btn_w and pos[1]< mouse_y < pos[1]+self.btn_h        