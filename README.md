# EXP_IIA
This is the second assignment for experimental robotics that develop the first assigment of EXPLAB to integrate it in a simulation with Gazebo.

 <p align="center">
 
  <img src="images/Schermata 2023-03-04 alle 23.47.35.png" width="1000" title="hover text">
</p>


## 1) -Brief Introduction:

In this README we find we explain the work done in the second assignment of Experimental robotics, where starting from the first assignment that we specially modified, we then created a robot with a manipulator and added it into the Gazebo simulator.

From our professor provided us with the assigment2 package to start with, which contains:

the definition of a custom message and a custom service               
1)- a simulation environment representing the "house" to be monitored             
2)- a node that implements a service: it requests the id (marker) detected by the robot and responds with information about the corresponding room (room name, center coordinates, links to other rooms)            
3)- a launch file, which starts Gazebo with the simulation environment and the service node (assignment.launch).


Our tasks will be as follows:

1)- Be spawned at the initial location x = -6.0, y = 11.0                           
2)- Construct the "semantic" map of the environment by detecting, without moving the robot's base, all seven markers around it, calling up the provided service node. Try to "scan" the environment completely, possibly exploring different solutions related to the robot model.                                  
3)- Start the patrolling algorithm by relying on the autonomous navigation strategies (mapping/planning) and the information collected and stored in the ontology during the previous phase.                                                                
4)- When a room is reached, perform a full scan of the room (by rotating the base or camera).

#### What we did for this assigment:

we created a model of the robot (starting from an already made one that we then specially modified) we equipped the robot with a manipulator consisting of a continuous joint,three revolute joints,two prismatic joints; where the end-effector contained the camera, plus we added a laserscan at the head of the robot all this in the .xarco file, we added the controllers of the dei joint and the pluin of the camera and laser in the .gazeo file.


In the second step we wrote the codes of the My_map node, which as its main function is to construct the ontology map using armor; to do this it performs the following steps:

1) We defined a joint_move() function,which moves the joints so that the camera is positioned in front of the marchers.                             
        1.1) In order to detect the marchers we downloaded the aruco_ros pkg then modified the marcher_publisher.cpp file by having it publish the results on the /marcher_id channel ; this node takes as arg the output of the camera that was in the /robot/camera1/image_raw channel              
        
2) We then defined the function marker_detect(), which uses the channel data /marker_id to get the information from the server marcher_detect.cpp which associates information with each id ident we store the information in the array Room[].         
  
3) Then we use this information (array Room[]) communicate with armo to build the ontology map which we then save as Assignment.owl


In the second step, we took the state machine from the first assignment and then modified it so that it could be integrated into the new architecture; specifically, we asked armor for the x and y data properties to know the coordinates of the rooms, which we will then use to send the robot there using the move_base node.
Then we added a part where the robot rotates to scan the room.  

## 2) -Software Architecture, Temporal Diagrams and State Diagrams:

### Software Architecture:

The following diagram shows the software architecture of our assignment and how the various modules communicate with each other.

<p align="center">
 
  <img src="images/Schermata 2023-03-04 alle 23.35.35.png" width="700" title="hover text">
</p>

Let us now describe the communication channels between the various modules:

|1| - This channel describes the communication between My_map.py and aruco where ever map reads the id_marchers from /marcher_id. 

|2||3| - This channel sends the request to the marcher_server by sending the 'marcher ID and then receives the information regarding the room through channel 3.                                                                               
|4| - Through the armor commands My_map builds the ontology.

|5| - On this communication channel queries are made to armor on data properties such as: "visitedAt", "x" , "y", and object properties such as "IsIn", "URGENT".

|6| - On this are done replacements of data in armor such as "visitedAt" and "IsIn".

|7||8| - The state machine asks move_base to move the robot to the coordinates indicated with through /move_base_simple/goal, and waits until it receives feedback through channel 8.

|9||10| - Move_base commands the robot with channel /cmd_vel and receives a map information through channel 10 and then corrects the trajectory.

|11| - Gazebo sends information to on the obstacles collected by the laser through /scan.

|12| - Aruco receives information from the camera in gazebo from channel /robot/camera1/image_raw which it then uses to detect the markers.

### Temporal Diagrams:

<p align="center">
 
  <img src="images/Schermata 2023-03-04 alle 21.48.48.png" width="750" title="hover text">
</p>

The time diagram is very important in this project to understand how the assigment works, because it shows how communication occurs between the various nodes in real time and how they should be synchronized.

We can explain the time diagram in two steps:

1) Starting from gazebo which is the simulator, starts the build map node which changes the camera position in front of the marchers , also starts the marcher_server node gives the map the infoorformations about the rooms; after that the my_map communicates with armor to build the ontology map after that the my_map node finishes its work.

2) In the second phase, the state machine starts, which loads the ontology saved in Assigment.owl and moves to the planning state and then moves to go_room, where it communicates with move_base to move the robot, then move-base commands the robot simultaneously with the map it receives from slam_mapping; it continues this way executing all states.
### State Diagrams:



<p align="center">
 
  <img src="images/Schermata 2023-03-04 alle 23.37.11.png" width="950" title="hover text">
</p>

This diagram shows the schematic of the finite state machine, the states it is composed of, and how the transition from one state to another takes place.

The finite state machine consists of a Planner Action state (which decides what state to go to), you exit the state with 'go_R1'(to go to room R1), 'go_R2'(to go to room R2), 'go_R3'(to go to room R3), 'go_R4'(to go to room R4)and with 'Urgent'(to go to Urgency), you enter the state with 'go_plan'; in the Robot_Move_to_Rx state you exit with 'go_plan' and enter with 'go_Rx'(Rx represents the individual rooms R1,R2,R3,R4); nthe URGENCY state you exit with 'go_plan and enter with 'Urgent'.

## 3) -Installation and Running procedure:

### - Installation procedure:

For this installation procedure we have taken into account that you already have ROS installed with your work space, you must have  already installed in your workspace the following package:

1)- armor link: https://github.com/EmaroLab/armor.git                                       
    1.1)- armor_py_api : https://github.com/CarmineD8/armor_py_api.git
  
2)- SMACh and SMACH viwer, with the following command:

```console
# INSTALLATION
# - eventually install smach with 
#          $ sudo apt-get install ros-noetic-executive-smach*
# - create ROS package in your workspace:
#          $ catkin_create_pkg smach_tutorial std_msgs rospy
# - move this file to the 'smach_tutorial/scr' folder and give running permissions to it with
#          $ chmod +x state_machine.py
# - run the 'roscore' and then you can run the state machine with
#          $ rosrun smach_tutorial state_machine.py
# - eventually install the visualiser using
#          $ sudo apt-get install ros-kinetic-smach-viewer
# - run the visualiser with
#          $ rosrun smach_viewer smach_viewer.py
```
3)- move_base link: https://wiki.ros.org/move_base

4)- slam_gmapping link: https://github.com/CarmineD8/slam_gmapping.git

After that, younmust clone this repositori in you workspace and build it, with the catkin_make command.
in this repository you found the following repository(pkg):

##### 1)- assigment2:
this repository contein the script My_map.py to build the map, the SM_assigment2.y tat is the state machine , the launch, param file ecc...

##### 2)- aruco_ros: (!!!NOTE: BE CAREFUL this package you cannot download elsewhere because it contains the marcher_publisher.py file that has been specially modified.)

### - Running procedure:

for the installation procedure execute this command in the terminal :

```console
roslaunch assignment2 assignment.launch
```
and in another terminal execute this command (we are chose this procedure bucause you can notified about the progression of the state machine)

```console
rosrun assignment2 SM_assigment2.py
```

## 4) -Video about assigment:
this video show how the state machine work and the simulation of the robot.

#### link:



