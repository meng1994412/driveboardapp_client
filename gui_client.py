from graphics import *
import time
import socket

print("Open up the GUI to control the laser")

# create a graphics window
win = GraphWin("Laser Controller", 800, 600)
win.setBackground("white")
win.setCoords(0, 0, 800, 600)

# left block
left_rect = Rectangle(Point(50, 200), Point(230, 380))
left_rect.setFill("gray")
left_rect.setWidth(10)
left_rect.draw(win)

left_triangle = Polygon(Point(100, 290), Point(180, 330), Point(180, 250))
left_triangle.setFill("red")
left_triangle.setWidth(5)
left_triangle.draw(win)

# right block
right_rect = Rectangle(Point(450, 200), Point(630, 380))
right_rect.setFill("gray")
right_rect.setWidth(10)
right_rect.draw(win)

right_triangle = Polygon(Point(580, 290), Point(500, 330), Point(500, 250))
right_triangle.setFill("red")
right_triangle.setWidth(5)
right_triangle.draw(win)

# top block
top_rectangle = Rectangle(Point(250, 400), Point(430, 580))
top_rectangle.setFill("gray")
top_rectangle.setWidth(10)
top_rectangle.draw(win)

top_triangle = Polygon(Point(340, 530), Point(300, 450), Point(380, 450))
top_triangle.setFill("red")
top_triangle.setWidth(5)
top_triangle.draw(win)

# bottom block
bot_rectangle = Rectangle(Point(250, 10), Point(430, 190))
bot_rectangle.setFill("gray")
bot_rectangle.setWidth(10)
bot_rectangle.draw(win)

bot_triangle = Polygon(Point(340, 60), Point(300, 150), Point(380, 150))
bot_triangle.setFill("red")
bot_triangle.setWidth(5)
bot_triangle.draw(win)

# run block
run_rectangle = Rectangle(Point(640, 120), Point(780, 180))
run_rectangle.setFill("green")
run_rectangle.setWidth(10)
run_rectangle.draw(win)

run_txt = Text(Point(710, 150), "Run")
run_txt.setSize(20)
run_txt.setStyle("bold")
run_txt.draw(win)

# exit block
exit_rectangle = Rectangle(Point(640, 20), Point(780, 80))
exit_rectangle.setFill("yellow")
exit_rectangle.setWidth(10)
exit_rectangle.draw(win)

exit_txt = Text(Point(710, 50), "Exit")
exit_txt.setSize(20)
exit_txt.setStyle("bold")
exit_txt.draw(win)

# set up communication with server
# PORT
PORT = 65430

# create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
# ip_address = socket.gethostbyname(local_hostname)

# using ethernet address for connection
ip_address = "192.168.1.49"
# ip_address = "127.0.0.1"

# bind the socket to the port 65431
server_address = (ip_address, PORT)
s.connect(server_address)
print("connecting to {} ({}) with {}".format(local_hostname, local_fqdn, ip_address))


while True:
    # driveboard.relative()
    p = win.getMouse()
    if (p.getX() > 50 and p.getX() < 230) and (p.getY() > 200 and p.getY() < 380):
        print("move laser 10 to the left")
        decision = "left"

    elif (p.getX() > 450 and p.getX() < 630) and (p.getY() > 200 and p.getY() < 380):
        print("move laster 10 to the right")
        decision = "right"

    elif (p.getX() > 250 and p.getX() < 430) and (p.getY() > 400 and p.getY() < 580):
        print("move laser 10 to the top")
        decision = "top"

    elif (p.getX() > 250 and p.getX() < 430) and (p.getY() > 10 and p.getY() < 190):
        print("move laser 10 to the bottom")
        decision = "bot"

    elif (p.getX() > 640 and p.getX() < 780) and (p.getY() > 20 and p.getY() < 80):
        print("quit the GUI")
        decision = "quit"

    elif (p.getX() > 640 and p.getX() < 780) and (p.getY() > 120 and p.getY() < 180):
        print("print the path")
        decision = "run"

    # send data to server
    s.send(decision.encode("utf-8"))
    # wait for two seconds
    time.sleep(0.5)

    if decision == "quit":
        break

win.close()

# close connection
s.close()
