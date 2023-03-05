#!/usr/bin/env python3

## @file SMachine_ASSIGNMENT.py
# @brief In this node are executing the state machine for the assignmet, 
# - It is composed in 6 state that are the 4 room,
# - a planner action and a urgency room
#
# @section author: 
# - CREATED by Bouazza EL Moutaouakil on 24/11/22
# @section version: 
# - version(1.0)

##  LIBRARI
# we are declared the librari tha we are need
# to do assignment 
import roslib
import rospy
import smach
import smach_ros
import time
from os.path import dirname, realpath
from armor_api.armor_client import ArmorClient
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Twist

## CLIENT SET-UP
# we are seting the path where we will save the ontologi,
# and we are creating the armor client 
# @param client define the client that talk with armor

path = dirname(realpath(__file__))
path = path + "/topological_map/"
print("WE MUST WAIT UNTIL THE MAP IS BUILD")
print("Wait... ONTOLOGICAL MAP COSTRUTION IN PROGRESS ........")
rospy.sleep(65) 
client = ArmorClient("My_client", "My_reference")
client.utils.load_ref_from_file(path + "Assignment.owl", "http://bnc/exp-rob-lab/2022-23",True,"PELLET", False )  # initializing with buffered manipulation and reasoning
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


## Plan_action Function
# this function simulate the planner of the robot
# and essentially call the transition of the state,
# on base of the value of the visitedAt data properti 
# of the room thath are defined in the room
# but before to do that, chek if there is some room in URGENCY mode
 

def Motion_in_Room(x,y):

     client_move = actionlib.SimpleActionClient('move_base',MoveBaseAction)
     client_move.wait_for_server()

     goal = MoveBaseGoal()
     goal.target_pose.header.frame_id = "map"
     goal.target_pose.header.stamp = rospy.Time.now()
     goal.target_pose.pose.position.x = x
     goal.target_pose.pose.position.y = y
     goal.target_pose.pose.orientation.w = 1.0
     
     client_move.send_goal(goal)
     wait = client_move.wait_for_result()
     
     if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
        return False
     else:
        return client_move.get_result()

def Plan_action():
     rospy.loginfo("PLAN ACTION")
     ## Ask to armore how many room are in urgency mode
     C = client.call('QUERY','IND','CLASS',['URGENT'])
     client.utils.apply_buffered_changes()
     client.utils.sync_buffered_reasoner()
     
     ## if there is more than 1 room (E is a URGENCY ROOM) go to Urgent state 
     if len(C.queried_objects) > 1 :
     	print("ROBOT MUST GO TO CHARGE")
     	return 'Urgent'
     
     ## if not ask to armor the data of visitedAt of the room
     A=['','','','' ]
     B=client.query.dataprop_b2_ind("visitedAt", "R1")
     client.utils.sync_buffered_reasoner()
     A[0] = int((B[0].split('"'))[1])
     B=client.query.dataprop_b2_ind("visitedAt", "R2")
     client.utils.sync_buffered_reasoner()
     A[1] = int((B[0].split('"'))[1])
     B=client.query.dataprop_b2_ind("visitedAt", "R3")
     client.utils.sync_buffered_reasoner()
     A[2] = int((B[0].split('"'))[1])
     B=client.query.dataprop_b2_ind("visitedAt", "R4")
     client.utils.sync_buffered_reasoner()
     A[3] = int((B[0].split('"'))[1])
     
     ## @param index take the index of  max value of this data
     index=(A.index(max(A))) +1
    
     ## in base of the index go to the room 
     if index == 1 :
     	return 'go_R1'
     if index == 2 :
     	return 'go_R2'
     if index == 3 :
     	return 'go_R3'
     if index == 4 :
     	return 'go_R4'
     ## @return Plan_Action() if there isn't any index recall the function
     # it is a step to avoid some bug during the execution 
     # of the function it coud be entered in one of the if  
     return Plan_action()
    
    


## @section RObot_Move_R1:
# - define the class that implies the motion of robot in room R1

class Robot_Move_R1(smach.State):
    def __init__(self):
        ## set the outcome to the other state ( in go to planner)
        smach.State.__init__(self, 
                             outcomes=['go_plan'],
                             )
                             
        
    def execute(self, userdata):
        
        
        ## ask to armor in wich room is robot and extractthe info
        B = client.query.objectprop_b2_ind("IsIn", "Robot1")
        
        
        B = (((B[0].split('#'))[1]).split('>'))[0]
        B=str(B)
        print("robot is in ", B)
        my_vel= Twist()
        
        
        ## move the robot to R1 
        Px=client.query.dataprop_b2_ind("x", "R1")
        Px = float(((Px[0].split('"'))[1]))
        Py=client.query.dataprop_b2_ind("y", "R1")
        Py = float(((Py[0].split('"'))[1]))
        print("X:",Px,"Y:",Py)
        res= Motion_in_Room(Px,Py)
        if res:
                rospy.loginfo("ROBOT MOVE TO R1")
        else:
               rospy.logerr("Move base not available to move the robot")
               exit(0) 
        
        
        client.call('REPLACE','OBJECTPROP','IND',["IsIn","Robot1", 'R1' , B ])
        client.utils.sync_buffered_reasoner()
        client.utils.apply_buffered_changes()
        
        ## stay it for some time (1 second)
        rospy.loginfo("SCAN OF THE ROOM BY ROTATING THE ROBOT")
        
        my_vel.angular.z=2.5
        pub.publish(my_vel)
        rate = rospy.Rate(0.2) # 0.2 Hz
        rate.sleep()
        my_vel.angular.z=0
        pub.publish(my_vel)
        
        
        ## ask to armor the value of visitedAt of R1
        A = client.query.dataprop_b2_ind("visitedAt", "R1")
        client.utils.sync_buffered_reasoner()
        
        ## @param A contain the value of visitedAt of R1 
        ## @param Anew contain the new value of visited of R1
        A = ((A[0].split('"'))[1])
        Anew = str(int(A) -1)
         
        ## change the value visitedAt of room R1 
        client.call('REPLACE','DATAPROP','IND',["visitedAt","R1","Long", Anew , A ])
        client.utils.sync_buffered_reasoner()
        
        
        
        ##inform user
        rospy.loginfo('Executing state robotMOve TO ROOM R1 ' )
        
        
        ## #return 'go_plan' to come back to planer
        return 'go_plan'
        

## @section RObot_Move_R2:
# - define the class that implies the motion of robot in room R2
class Robot_Move_R2(smach.State):
    def __init__(self):
        ## set the outcome to the other state ( in go to planner)
        smach.State.__init__(self, 
                             outcomes=['go_plan'],
                             )
                             
        
    def execute(self, userdata):
        
        ## ask to armor in wich room is robot and extractthe info
        B = client.query.objectprop_b2_ind("IsIn", "Robot1")
        B = (((B[0].split('#'))[1]).split('>'))[0]
        B=str(B)
        print("robot is in ", B)
        
        my_vel= Twist()
        
        
        ## move the robot to R2 
        Px=client.query.dataprop_b2_ind("x", "R2")
        Px = float(((Px[0].split('"'))[1]))
        Py=client.query.dataprop_b2_ind("y", "R2")
        Py = float(((Py[0].split('"'))[1]))
        print("X:",Px,"Y:",Py)
        res= Motion_in_Room(Px,Py)
        if res:
                rospy.loginfo("ROBOT MOVE TO R2")
        else:
               rospy.logerr("Move base not available to move the robot")
               exit(0) 
        
        client.call('REPLACE','OBJECTPROP','IND',["IsIn","Robot1", 'R2' , B ])
        client.utils.sync_buffered_reasoner()
        client.utils.apply_buffered_changes()
        
        ## stay it for some time (1 second)
        rospy.loginfo("SCAN OF THE ROOM BY ROTATION OF THE ROBOT")
       
        my_vel.angular.z=2.5
        pub.publish(my_vel)
        rate = rospy.Rate(0.2) # 0.2 Hz
        rate.sleep()
        my_vel.angular.z=0
        pub.publish(my_vel)
        
        
        ## ask to armor the value of visitedAt of R2
        A = client.query.dataprop_b2_ind("visitedAt", "R2")
        client.utils.sync_buffered_reasoner()
        
        ## @param A contain the value of visitedAt of R2 
        ## @param Anew contain the new value of visited of R2
        A = ((A[0].split('"'))[1])
        Anew = str(int(A) -1)
         
        ## change the value visitedAt of room R2
        client.call('REPLACE','DATAPROP','IND',["visitedAt","R2","Long", Anew , A ])
        client.utils.sync_buffered_reasoner()
        
        
        
        
        ## inform user
        rospy.loginfo('Executing state robotMOve TO ROOM R2 ' )
        
        
        ## return 'go_plan' to come back to planer
        return 'go_plan'
        

## @section RObot_Move_R3:
# - define the class that implies the motion of robot in room R3
class Robot_Move_R3(smach.State):
    def __init__(self):
        ## set the outcome to the other state ( in go to planner)
        smach.State.__init__(self, 
                             outcomes=['go_plan'],
                             )
                             
        
    def execute(self, userdata):
        
        
        ## ask to armor in wich room is robot and extractthe info
        B = client.query.objectprop_b2_ind("IsIn", "Robot1")
        B = (((B[0].split('#'))[1]).split('>'))[0]
        B = str(B)
        print("robot is in ", B)
        
        my_vel= Twist()
        
        
        
        ## move the robot to R3 
        Px=client.query.dataprop_b2_ind("x", "R3")
        Px = float(((Px[0].split('"'))[1]))
        Py=client.query.dataprop_b2_ind("y", "R3")
        Py = float(((Py[0].split('"'))[1]))
        print("X:",Px,"Y:",Py)
        res= Motion_in_Room(Px,Py)
        if res:
                rospy.loginfo("ROBOT MOVE TO R3")
        else:
               rospy.logerr("Move base not available to move the robot")
               exit(0) 
        
        client.call('REPLACE','OBJECTPROP','IND',["IsIn","Robot1", 'R3' , B ])
        client.utils.sync_buffered_reasoner()
        client.utils.apply_buffered_changes()
        
        ## stay it for some time (1 second)
        rospy.loginfo("SCAN OF THE ROOM BY ROTATION OF THE ROBOT")
        
        my_vel.angular.z=2.5
        pub.publish(my_vel)
        rate = rospy.Rate(0.2) # 0.2 Hz
        rate.sleep()
        my_vel.angular.z=0
        pub.publish(my_vel)
        
        
        ## ask to armor the value of visitedAt of R3
        A = client.query.dataprop_b2_ind("visitedAt", "R3")
        client.utils.sync_buffered_reasoner()
        
        ## @param A contain the value of visitedAt of R3
        ## @param Anew contain the new value of visited of R3
        A = ((A[0].split('"'))[1])
        Anew = str(int(A) -1)
         
        ## change the value visitedAt of room R3
        client.call('REPLACE','DATAPROP','IND',["visitedAt","R3","Long", Anew , A ])
        client.utils.sync_buffered_reasoner()
        
        
        ## inform user
        rospy.loginfo('Executing state robotMOve TO ROOM R3 ' )
        
        
        ## return 'go_plan' to come back to planer
        return 'go_plan'
 
## @section RObot_Move_R4:
# - define the class that implies the motion of robot in room R4       
class Robot_Move_R4(smach.State):
    def __init__(self):
        ## set the outcome to the other state ( in go to planner)
        smach.State.__init__(self, 
                             outcomes=['go_plan'],
                             )
                             
        
    def execute(self, userdata):
        
        ## ask to armor in wich room is robot and extractthe info
        B = client.query.objectprop_b2_ind("IsIn", "Robot1")
        B = (((B[0].split('#'))[1]).split('>'))[0]
        B = str(B)
        print("robot is in ", B)
        my_vel= Twist()
        
        
        
        
        ## move the robot to R4 
        Px=client.query.dataprop_b2_ind("x", "R4")
        Px = float(((Px[0].split('"'))[1]))
        Py=client.query.dataprop_b2_ind("y", "R4")
        Py = float(((Py[0].split('"'))[1]))
        print("X:",Px,"Y:",Py)
        res= Motion_in_Room(Px,Py)
        if res:
                rospy.loginfo("ROBOT MOVE TO R4")
        else:
               rospy.logerr("Move base not available to move the robot")
               exit(0) 
        
        client.call('REPLACE','OBJECTPROP','IND',["IsIn","Robot1", 'R4' , B ])
        client.utils.sync_buffered_reasoner()
        client.utils.apply_buffered_changes()
        
        ## stay it for some time (1 second)
        rospy.loginfo("SCAN OF THE ROOM BY ROTATION OF THE ROBOT")
       
        my_vel.angular.z=2.5
        pub.publish(my_vel)
        rate = rospy.Rate(0.2) # 0.2 Hz
        rate.sleep()
        my_vel.angular.z=0
        pub.publish(my_vel)
        
        
        ## ask to armor the value of visitedAt of R4
        A = client.query.dataprop_b2_ind("visitedAt", "R4")
        client.utils.sync_buffered_reasoner()
        
        ## @param A contain the value of visitedAt of R4 
        ## @param Anew contain the new value of visited of R4
        A = ((A[0].split('"'))[1])
        Anew = str(int(A) -1)
         
        ## change the value visitedAt of room R4
        client.call('REPLACE','DATAPROP','IND',["visitedAt","R4","Long", Anew , A ])
        client.utils.sync_buffered_reasoner()
        
        
        #inform user 
        rospy.loginfo('Executing state robotMOve TO ROOM R4 ' )
        
        
        ## return 'go_plan' to come back to planer
        return 'go_plan'
        
## @section Urgent
# - define the class that implies the motion of robot in URGENT room        
class Urgent(smach.State):
    def __init__(self):
        ## set the outcome to the other state ( in go to planner)
        smach.State.__init__(self, 
                             outcomes=['go_plan'],
                             )
                             
        
    def execute(self, userdata):
        
        ## ask to armor in wich room is robot and extractthe info
        B = client.query.objectprop_b2_ind("IsIn", "Robot1")
        B = (((B[0].split('#'))[1]).split('>'))[0]
        B = str(B)
        print("robot is in: %s" %B)
        my_vel= Twist()
        rate=rospy.Rate(1)
        
        
        Px=client.query.dataprop_b2_ind("x", "E")
        Px = float(((Px[0].split('"'))[1]))
        Py=client.query.dataprop_b2_ind("y", "E")
        Py = float(((Py[0].split('"'))[1]))
        print("X:",Px,"Y:",Py)
        res= Motion_in_Room(Px,Py)
        if res:
                rospy.loginfo("ROBOT MOVE TO E")
        else:
               rospy.logerr("Move base not available to move the robot")
               exit(0) 
        
        ## move the robot to E 
        client.call('REPLACE','OBJECTDROP','IND',["isIn","Robot1","E",B])
        client.utils.sync_buffered_reasoner()
        client.utils.apply_buffered_changes()
        
        ## ask to armor the value of visitedAt of R1 and extraxt the info
        A = client.query.dataprop_b2_ind("visitedAt", "R1")
        client.utils.sync_buffered_reasoner()
        A = ((A[0].split('"'))[1])
        ## set the value of visitedAt of R1 equal to now of robot 
        client.call('REPLACE','DATAPROP','IND',["visitedAt","R1","Long", '1665579740' , A ])
        client.utils.sync_buffered_reasoner()
        ## ask to armor the value of visitedAt of R2 and extraxt the info
        A = client.query.dataprop_b2_ind("visitedAt", "R2")
        client.utils.sync_buffered_reasoner()
        A = ((A[0].split('"'))[1])
        ## set the value of visitedAt of R2 equal to now of robot 
        client.call('REPLACE','DATAPROP','IND',["visitedAt","R2","Long", '1665579740' , A ])
        client.utils.sync_buffered_reasoner()
        ## ask to armor the value of visitedAt of R3 and extraxt the info
        A = client.query.dataprop_b2_ind("visitedAt", "R3")
        client.utils.sync_buffered_reasoner()
        A = ((A[0].split('"'))[1])
        ## set the value of visitedAt of R3 equal to now of robot 
        client.call('REPLACE','DATAPROP','IND',["visitedAt","R3","Long", '1665579740' , A ])
        client.utils.sync_buffered_reasoner()
        ## ask to armor the value of visitedAt of R4 and extraxt the info
        A = client.query.dataprop_b2_ind("visitedAt", "R4")
        client.utils.sync_buffered_reasoner()
        A = ((A[0].split('"'))[1])
        ## set the value of visitedAt of R4 equal to now of robot 
        client.call('REPLACE','DATAPROP','IND',["visitedAt","R4","Long", '1665579740' , A ])
        client.utils.sync_buffered_reasoner()
        
        rospy.loginfo('Waiting for 4 second time of recharge ' )
        ## stay it for some time (4 second)
        time.sleep(4)
        rospy.loginfo("SCAN OF THE ROOM BY ROTATION OF THE ROBOT")
        
        my_vel.angular.z=2.5
        pub.publish(my_vel)
        rate = rospy.Rate(0.2) # 0.2 Hz
        rate.sleep()
        my_vel.angular.z=0
        pub.publish(my_vel)
        
        ## inform user
        rospy.loginfo('Executing state robotMOve TO URGENCY E ' )
        
        
        ## return 'go_plan' to come back to planer
        return 'go_plan'
        
## @section Plan_action_rob:
# - define the class that implies the planing  motion of the robot         
class Plan_action_rob(smach.State):
    def __init__(self):
        ## set the outcome to the other state ( that are going in all states)
        smach.State.__init__(self, 
                             outcomes=['go_R1','go_R2','go_R3','go_R4','Urgent','go_plan'],
                             )
                             
        
    def execute(self, userdata):
        
        ## planing time (0.5 second)
        time.sleep(0.5)
        ## inform user
        rospy.loginfo('Executing state PLANING ACTION ' )
        
        
        ## return Plan_action() to come back to the function that planing
        return Plan_action()

## @section main():
# - define the main of the progect      
def main():
    rospy.loginfo("NODE STATE MACHINE start")
    print("WE MUST WAIT ANTIL THE MAP IS BUILD")
    rospy.init_node('smach_example_1')
    

    
    
    
    ## Create a SMACH state machine
    stat_m = smach.StateMachine(outcomes=['container_interface'])
    
   

    ## Open the container
    with stat_m:
        
        ## Add states Plan_Action to the container
        smach.StateMachine.add('Plan_Action', Plan_action_rob(), 
                               transitions={'go_R1':'Robot_Move_To_R1',
                                	     'go_R2':'Robot_Move_To_R2',
                                	     'go_R3':'Robot_Move_To_R3',
                                	     'go_R4':'Robot_Move_To_R4',
                                	     'Urgent':'URGENCY', 
                                            'go_plan':'Plan_Action',
                                            })
                                            
        ## Add states Robot_Move_To_R1 to the container                                   
        smach.StateMachine.add('Robot_Move_To_R1', Robot_Move_R1(), 
                               transitions={ 
                                            'go_plan':'Plan_Action',
                                           })
                                           
        ## Add states Robot_Move_To_R2 to the container
        smach.StateMachine.add('Robot_Move_To_R2', Robot_Move_R2(), 
                               transitions={ 
                                            'go_plan':'Plan_Action',
                                            })
                                            
        ## Add states Robot_Move_To_R3 to the container                                   
        smach.StateMachine.add('Robot_Move_To_R3', Robot_Move_R3(), 
                               transitions={
                                            'go_plan':'Plan_Action',
                                           })
        ## Add states Robot_Move_To_R4 to the container
        smach.StateMachine.add('Robot_Move_To_R4', Robot_Move_R4(), 
                               transitions={
                                            'go_plan':'Plan_Action',
                                            })
        
        ## Add states URGENCY to the container                                    
        smach.StateMachine.add('URGENCY', Urgent(), 
                               transitions={ 
                                            'go_plan':'Plan_Action',
                                           })
        

                               
                              
       
        
                               


    ## Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', stat_m, '/SM_ROOT')
    sis.start()

    ## Execute the state machine
    outcome = stat_m.execute()

    ## Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
