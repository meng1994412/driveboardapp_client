# driveboardapp development for lasersaur laser cut machine
#### Chenyang Meng
## Introduction
The [driveboardapp](https://github.com/nortd/driveboardapp) is the software that controls the laser cut machine at MSR lab. We want to implement a camera to help user to localize the position for laser to cut in the future. Thus, the goal of the project is to control the laser cutter from backend at client computer and visualize the where and what to cut from the camera mounted on the laser cutter.

## Language/Packages Used:
* Python 2.7 (beaglebone computer) / 3.5 (client computer)
* [socket](https://docs.python.org/3/library/socket.html)
* [OpenCV](https://docs.opencv.org/3.4.4/) 3.4.4
* [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Approaches
There are two repositories for the project. The first one is [driveboardapp](https://github.com/meng1994412/driveboardapp), including the original driveboardapp software plus some development scripts (each script will be explained in details in the following steps) for the project. All codes in this repository will run on the beaglebone machine on the laser cut machine. The second one is this repository named [driveboardapp_client](https://github.com/meng1994412/driveboardapp_client), which contains the documentation of the project for future purpose.

### step 1
The first step is to understand the original software and control the laser cutter on the beaglebone. `driveboard.py` ([check here](https://github.com/meng1994412/driveboardapp/blob/master/backend/driveboard.py)) contains all the functions used for controlling the laser cutter from backend. The relevant functions for moving laser cutter are `feedrate(val)`, `intensity(val)`, `relative()`, `absolute()`, `move(x, y, z)`, `air_on()`, `air_off()`.

The `test_move.py` ([check here](https://github.com/meng1994412/driveboardapp/blob/master/backend/test_move.py)) achieves the initial approach to control the laser cutter from backend on the beaglebone. The script contains the path of the lasersaur logo. Every time we want to control the laser cutter, we firstly need to build up connection using `driveboard.connect()`. We need to set laser cutter to either absolute coordinate system (`driveboard.absolute()`) or relative coordinate system (`driveboard.relative()`). In this step, we use absolute coordinate system. We will use relative coordinate system when implementing user interface control on the cutter. If we want to move the cutter without laser on, we need to define the seekrate value (`driveboard.feedrate(seekrate)`) and make sure the intensity is 0.0 (`driveboard.intensity(0.0)`). After moving the cutter (`driveboard.move(x, y, z)`) to somewhere, we need to use `time.sleep(0.1)` to provide some time for the beaglebone to execute the movement and 0.1s is a pretty quick and robust value. If we want to move the cutter with laser on, we need to define feedrate value instead (`driveboard.feedrate(feedrate)`), which will make the cutter move slower. And we can change the intensity to any value between 0 and 100 (larger the value, more power the laser has). We also have to make sure the airflow is on (`air_on()`). We need to remember close the connection (`driveboard.close()`) after the job is done.

In order to access to [driveboardapp](https://github.com/meng1994412/driveboardapp) on beaglebone, we can use the SSH command line (remember to connect to MSR lab wifi first).

```
ssh root@lasersaur.local
```

After SSH into the beaglebone machine, we need to stop the ongoing driveboardapp first (every time laser cut machine is turned on, the driveboardapp will automatically start) by using the following command line to run our development script from backend.

```
sudo service driveboardapp.sh stop
```

Then we can run our initial approach script (python 2.7 on beaglebone) by using following command.

```
python test_move.py
```

### step 2
The second step is build up a communication between between beaglebone and client computer so that we can send path data from client computer to the server (beaglebone machine). There are two development scripts named `comm_server.py` ([check here](https://github.com/meng1994412/driveboardapp/blob/master/backend/comm_server.py)) and `comm_client.py` ([check here](https://github.com/meng1994412/driveboardapp_client/blob/master/comm_client.py)). We create a TCP/IP socket, set a port and an ethernet IP address (the address on beaglebone), bind the socket to the port, and finally send/receive **string** data. The **string** data is a string of list contains the [x, y] coordinates we want the cutter to move. The original data is stored in the `data.py` and is converted into string at the beginning of the `comm_client.py`.

In `comm_server.py` ([check here](https://github.com/meng1994412/driveboardapp/blob/master/backend/comm_server.py)), we also need to build up connection with driveboard, set some initial seekrate, intensity value, and make sure the airflow is on. Every time we receive **string** data from the client, we change string data back to list data and call the `control_move(path)` function from `test_comm_move.py` ([chech here](https://github.com/meng1994412/driveboardapp/blob/master/backend/test_comm_move.py)). The `control_move(path)` function takes path data as the argument and executes the laser cutting.

Remember to run the `comm_server.py` on beaglebone first and then run the `comm_client.py` on the client computer to start the communication by using the following command lines.

```
python comm_server.py
```  

```
python comm_client.py
```

### step 3
The next step is to build a graphic user interface, which can allow user to move the laser cutter in four direction (top, bottom, right, left) 10 units each time. A communication between beaglebone and client computer is built so that we can use the user interface on client computer to move the laser cutter controlled by beaglebone. Figure 1 below shows a simple interface we created. The four direction (top, bottom, left, right) buttons controls the laser cutter. The "Exit" button will quit the interface and close the client communication. The "Run" button will execute the laser cutting job.

<img src="https://github.com/meng1994412/driveboardapp_client/blob/master/GUI.png" width="600">

Figure 1. Simple GUI for controlling the laser cutter.

In the `gui_client.py` ([check here](https://github.com/meng1994412/driveboardapp_client/blob/master/gui_client.py)), the GUI is built by using `graphics.py` module ([check here](https://github.com/meng1994412/driveboardapp_client/blob/master/graphics.py)). Each decision that whether move laser cutter to any direction, quit, or run is sent to the `gui_server.py` as a string type. The `gui_server.py` ([check here](https://github.com/meng1994412/driveboardapp/blob/master/backend/gui_server.py))sends the decision to `control(decision)` function from `gui_control.py`. If any direction button is clicked, the laser cutter will move 10 units from previous position to that direction (set to `driveboard.relative()` mode ([check here](https://github.com/meng1994412/driveboardapp/blob/master/backend/gui_server.py#L40))).Be cautious that right is positive x-axis, and bottom is positive y-axis. If "Exit" button is clicked, the laser cutter will change relative mode (`driveboard.relative()`) back to absolute mode (`driveboard.absolute()`) and move back to the original position. If "Run" button is clicked, the laser cutter will change to absolute mode (`driveboard.absolute()`) and execute the laser cutting job.

Remember to run the `gui_server.py` on beaglebone first and then run the `gui_client.py` on the client computer to start the communication by using the following command lines.

```
python gui_server.py
```  

```
python gui_client.py
```

### two development scripts might be useful in the future
There is a development script named `svg_transform.py` ([check here](https://github.com/meng1994412/driveboardapp_client/blob/master/svg_transform.py)). Since the driveboardapp software web interface will accept SVG file as input and execute the laser cutting job based on that SVG file. This script can take the SVG file and make translation, rotation, or scaling on the shape in the SVG file.

The other development script named `barcode_scanner.py` ([check here](https://github.com/meng1994412/driveboardapp_client/blob/master/barcode_scanner.py))is used for reading a QRcode by camera if we want to put a QRcode picture on the wood board to identify the location to execute the laser cutting job in the future. There is also a `barcode.csv` file which will record the time when camera finds the QRcode.

## What's next
For the future plan, we want to mount the camera on the laser cutter (temporarily by using tape or rubber band) with positive offset on x and y axis so that camera can view the area we might want to execute the laser cutting job. We want to make the camera face vertically to the wood board to simplify the situation at first. We measure the distance from camera to the wood board at z = 0 as reference. We also put a square tag on the wood board and measure the dimension of the tag. If we turn on the video stream, we will find a scaling factor of the tag between the measured dimension and dimension in the video stream. With that scaling factor, we can draw the shape about to cut in the video stream to help user visualize it. This might be a good starting point. After this, we can implement a resize handler to visualize the resizing shape about to cut on the video stream.

There are also some other next-steps, but which are less important for now. They are:
* build a single communication which can send/receive multiple types of data.
* build a input box on GUI so that we can define the distance for each move.
* build a solid model to mount camera on the laser cutter
