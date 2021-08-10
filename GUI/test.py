import pygame as pg


def main():
    pg.init()

    screen=pg.display.set_mode((1280,720))
    running = True
    while running:
        for event in pg.event.get():
            # only do something if the event is of type QUIT
            if event.type == pg.QUIT:
                # change the value to False, to exit the main loop
                running=False

    pass

#if __name__=="__main__":
    # call the main function
  #  main()
  #pass