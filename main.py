import pygame
import math
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("COVID simulator")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

standard_button_width = 125
standard_button_height = 50
change_button_width = 25
change_button_height = 25
radius_size = 25
fps = 10
line_width = 5
one_second_wait_time = 1000
backtrack_show_time = 10000

font = pygame.font.SysFont('comicsans', 30)

class Button():
    def __init__(self, x, y, width, height, text, color, intersection=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.intersection = intersection
        self.line_color = WHITE

    def draw(self):
        #pygame.draw.rect(WIN, self.color, pygame.Rect(x, y, self.width, self.height))
        label = font.render(str(self.text), 1, WHITE)
        #?What ifit is an operational button?
        #WIN.blit(self.label, )
        if (self.intersection!=None):
            font_position = (
                ((self.intersection.p1.x+self.intersection.p2.x)/2)-(label.get_width()+self.width)/2,
                ((self.intersection.p1.y+self.intersection.p2.y)/2)-label.get_height()/2
            )
            
            rect_position = (
                font_position[0]+label.get_width(),
                (self.intersection.p1.y+self.intersection.p2.y)/2 - self.width/2
            )
            self.x = rect_position[0]
            self.y = rect_position[1]

            #!Have to draw the line if it is intersecting. 
            pygame.draw.line(WIN, self.line_color, (self.intersection.p1.x, self.intersection.p1.y), (self.intersection.p2.x, self.intersection.p2.y), line_width)
            pygame.draw.rect(WIN, GREEN, pygame.Rect(self.x, self.y, self.width, self.height/2))
            pygame.draw.rect(WIN, RED, pygame.Rect(self.x, self.y+self.height/2, self.width, self.height/2))
        else:
            font_position = (
                (self.x+self.width/2-label.get_width()/2),
                (self.y+self.height/2-label.get_height()/2)
            )

            pygame.draw.rect(WIN, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

        WIN.blit(label, font_position)

    def intersecting(self, x, y):
        #!Cannot let self.x and self.y be random points because we check intersection with them. 
        return (x>=self.x and x<=self.x+self.width and y>=self.y and y<=self.y+self.height)

class Intersection():
    def __init__(self, p1, p2):
        self.color = BLACK
        self.p1 = p1
        self.p2 = p2
        #self.time = 1
        #!The text property for Button already can be blitted
    #!Since only Button and Person objects are included in arr, must draw everything from Button. 

class Person():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = GREEN
    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), radius_size)

    def intersecting(self, x, y):
        #!Not calculating it correctly!
        return math.sqrt((x-self.x)**2+(y-self.y)**2) <= radius_size

class MainGame():
    def __init__(self):

        add = Button(0, 0, standard_button_width, standard_button_height, "add", GREEN)
        forward = Button(standard_button_width, 0, standard_button_width, standard_button_height, "->", RED)
        backward = Button(standard_button_width*2, 0, standard_button_width, standard_button_height, "<-", GREEN)
        infect = Button(standard_button_width*3, 0, standard_button_width, standard_button_height, "infect", RED)
        connect = Button(standard_button_width*4, 0, standard_button_width, standard_button_height, "connect", GREEN)
        self.objs = [add, forward, backward, infect, connect]
        self.time = 0

    def draw(self):
        WIN.fill(BLACK)
        #*Blit the black screen first
        time_label = font.render(str(self.time), 1, WHITE)
        WIN.blit(time_label, (standard_button_width*5, 0))
        for obj in self.objs:
            obj.draw()
        
        #Only separate component is the time label. 
        
        
        pygame.display.update()

    def forward(self):
        self.time = 0
        while self.time<10:
            pygame.time.wait(one_second_wait_time)
            self.time+=1
            #*Can increase to 10 here. 
            
            for obj in self.objs:
                #*Compare it to the time that has passed. 
                if (type(obj)==Button and type(obj.text)==int and obj.text==self.time):
                    if (obj.intersection.p1.color==RED or obj.intersection.p2.color==RED):
                        obj.intersection.p1.color=RED
                        obj.intersection.p2.color=RED
                        obj.line_color = RED
                    else:
                        obj.intersection.p1.color=GREEN
                        obj.intersection.p2.color=GREEN
                        obj.line_color = GREEN
                
                #*Reset the color if it is an interaction not happening at that time. 
                elif (type(obj)==Button and type(obj.text)==int):
                    obj.line_color = WHITE
            self.draw()

    def backward(self):
        #PURPLE -> must have had the virus at time 0. 
        #BLUE -> could have had the virus at time 0. 

        

        #*Display the results for 10 seconds. 
        pygame.time.wait(backtrack_show_time)


    def main(self):
        run = True
        adding = False
        infecting = False
        connecting = False
        p1 = None
        backwarding = False
        forwarding = False
        can_click = True #*A cooldown for the mouse
        #!Don't need clock if using delay
        #self.clock = pygame.time.Clock()
        self.forwarding_time = 0
        while run:
            #self.clock.tick(fps)
            #print(len(self.objs))
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if (pygame.mouse.get_pressed()[0]):
                intersecting = False
                x, y = pygame.mouse.get_pos()
                for obj in self.objs:
                    if (obj.intersecting(x, y)):
                        #print("intersecting")
                        if (type(obj)==Button):
                            intersecting = True
                            if (obj.text=="add"):
                                adding = True
                                infecting = False
                                connecting = False
                                #Make sure no stored p1 data
                                p1 = None
                            elif (obj.text=="->"):
                                #!We want forward to continuously run so just ditch this method and call draw from the forward method itself. 
                                #forwarding = True
                                self.forward()
                                
                            elif (obj.text=="<-"):
                                #backwarding = True
                                self.backward()
                            elif (obj.text=="infect"):
                                adding = False
                                infecting = True
                                connecting = False
                            elif (obj.text=="connect"):
                                adding = False
                                infecting = False
                                connecting = True

                            #!Check whether the type of text in an integer. 
                            elif (type(obj.text)==int):
                                #print("changing")
                                #!Probably want to implement the cursor logic so it doesn't decrease like crazy. 
                                adding = False
                                connecting = False
                                infecting = False
                                if (can_click):
                                    if (y<=obj.y+obj.height/2):
                                        #*In the upper half -> add
                                        #print("increased")
                                        obj.text = min(10, obj.text+1)
                                    else:
                                        obj.text = max(1, obj.text-1)
                            

                        elif (type(obj)==Person):
                            #print("person")
                            if (connecting and p1!=None and obj!=p1):
                                #!Multiple clicks per click so it becomes confusing. 
                                #*I can use the logic of has to click away. 
                                #*Or check that p1 is different from obj
                                #*Creating a line. 
                                intersection = Intersection(p1, obj)
                                #!Since button location will be relative to the circle location, x and y don't really matter. 
                                button = Button(0, 0, change_button_width, change_button_height, 1, WHITE, intersection)
                                #!Initially pass the text as 1. 
                                self.objs.append(button)
                                connecting = False
                                p1 = None
                            elif (connecting):
                                #print("initialized p1")

                                p1 = obj
                            elif (infecting):
                                #*Cannot move after infecting
                                if (obj.color==RED):
                                    obj.color=GREEN
                                else:
                                    obj.color=RED
                                #obj.color = RED
                                infecting = False
                            else:
                                #dragging
                                #!But it seems like it keeps creating new objects. 

                                obj.x = x
                                obj.y = y


                #*After looking through all the objects
                if (not intersecting and adding and not forwarding and not backwarding):
                    self.objs.append(Person(x, y))
                    #print("added")
                    adding = False

                can_click = False #*Since we just clicked. 
            else:
                can_click = True

        pygame.quit()

    

game = MainGame()
game.main()