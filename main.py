import pygame
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

    def draw(self):
        #pygame.draw.rect(WIN, self.color, pygame.Rect(x, y, self.width, self.height))
        label = font.render(self.text, self.text, WHITE)
        #?What ifit is an operational button?
        #WIN.blit(self.label, )
        if (self.intersection!=None):
            font_position = (
                ((self.intersection.p1.x+self.intersection.p2.x)/2)-(label.get_width()+self.width)/2,
                ((self.intersection.p1.y+self.intersection.p2.y)/2)-(max(label.get_height(), self.height))
            )
            rect_position = (
                font_position[0]+label.get_width(),
                (self.intersection.p1.y+self.intersection.p2.y)/2 - self.width/2
            )
        else:
            font_position = (
                (self.x+self.width/2-label.get_width()/2),
                (self.y+self.height/2-label.get_height()/2)
            )
            rect_position = (self.x, self.y)

        pygame.draw.rect(WIN, self.color, pygame.Rect(rect_position[0], rect_position[1], self.width, self.height))
        WIN.blit(label, font_position)

    def intersecting(self, x, y):
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
        return ((x**2+y**2)**0.5) <= radius_size

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
        for obj in self.objs:
            obj.draw()
        
        #Only separate component is the time label. 
        time_label = font.render(str(self.time), 1, WHITE)
        WIN.blit(time_label, (standard_button_width*5, 0))
        pygame.display.update()

    def main(self):
        run = True
        adding = False
        infecting = False
        connecting = False
        p1 = None
        backwarding = False
        forwarding = False
        while run:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if (pygame.mouse.get_pressed()[0]):
                intersecting = False
                x, y = pygame.mouse.get_pos()
                for obj in self.objs:
                    if (obj.intersecting(x, y)):
                        if (type(obj)==Button):
                            intersecting = True
                            if (obj.text=="add"):
                                adding = True
                                infecting = False
                                connecting = False
                                #Make sure no stored p1 data
                                p1 = None
                            elif (obj.text=="->" and not self.forwarding and not backwarding):
                                forwarding = True
                                self.forward()
                            elif (obj.text=="<-" and not self.forwarding and not backwarding):
                                backwarding = True
                                self.backward()
                            elif (obj.text=="infect"):
                                adding = False
                                infecting = True
                                connecting = False
                            elif (obj.text=="connect"):
                                adding = False
                                infecting = False
                                connecting = True
                        
                            elif (obj.text=="time"):
                                adding = False
                                connecting = False
                                infecting = False
                                if (y<=obj.y+obj.height/2):
                                    #*In the upper half -> add
                                    obj.intersection.time = min(10, obj.intersection.time+1)
                                else:
                                    obj.intersection.time = max(0, obj.intersection.time-1)

                        elif (type(obj)==Person):
                            if (connecting and p1!=None):
                                #*Creating a line. 
                                intersection = Intersection(p1, obj)
                                #!Since button location will be relative to the circle location, x and y don't really matter. 
                                button = Button(0, 0, self.change_button_width, self.change_button_height, 1, color, intersection)
                                connecting = False
                                p1 = None
                            elif (connecting):
                                p1 = obj
                            elif (infecting):
                                obj.color = RED
                            else:
                                #draggin
                                obj.x = x
                                obj.y = y


                #*After looking through all the objects
                if (not intersecting and adding):
                    self.objs.append(Person(x, y))
                    adding = False

        pygame.quit()

game = MainGame()
game.main()