#!/usr/bin/env python3
 
import rospy
import time
from std_msgs.msg import Float64
from assignment2.srv import RoomInformation
from armor_api.armor_client import ArmorClient 
from os.path import dirname, realpath
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal




global Room
Room = [] 
def mar_id(msg):

    A=int(msg.data)
    if (11<= A <=17):

    
        rospy.wait_for_service('/room_info')
        room = rospy.ServiceProxy('/room_info', RoomInformation)
        data_room = room(A)
        
        if Room.count(data_room) == 0:
            Room.append(data_room)
	
	

def joint_move():    

    for marker in range(11, 18):
    
        rate = rospy.Rate(0.4) # 0.4 Hz
        rate2 = rospy.Rate(2) # 2 Hz
        
        
        if marker == 16:
        
            q =[ -1.55, 2.3, -2, 0.2 , 0.2,-0.4] 
            rospy.loginfo("q_joint= %s" % q[2]  )
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[2])
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[1])
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[0])
            pub0.publish(q[0])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[3])
            pub3.publish(q[3])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[4])
            pub4.publish(q[4])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[5])
            pub5.publish(q[5])
            rate2.sleep()
        
            
            rospy.Subscriber("/marker_id", Float64, mar_id)
            rospy.loginfo("position of marker : %s "%marker )
            rate.sleep()
                
        elif marker == 12:
            
         # second Pose for detecting markers 
            q =[ 1.6, 2.3, -2, 0.3 , 0.3,-0.4] 
            rospy.loginfo("q_joint= %s" % q[2]  )
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[2])
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[1])
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[0])
            pub0.publish(q[0])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[3])
            pub3.publish(q[3])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[4])
            pub4.publish(q[4])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[5])
            pub5.publish(q[5])
            rate2.sleep()
        
            
            rospy.Subscriber("/marker_id", Float64, mar_id)
            rospy.loginfo("position of marker : %s "%marker )
            rate.sleep()
        
        elif marker == 17:
        
         # Third Pose for detecting markers 
            q =[ 2.3, 2.8, -2.6, 0.2 , 0.2,-0.4] 
            rospy.loginfo("q_joint= %s" % q[2]  )
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[2])
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[1])
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[0])
            pub0.publish(q[0])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[3])
            pub3.publish(q[3])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[4])
            pub4.publish(q[4])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[5])
            pub5.publish(q[5])
            rate2.sleep()
        
            
            rospy.Subscriber("/marker_id", Float64, mar_id)
            rospy.loginfo("position of marker : %s "%marker )
            rate.sleep()
        
        elif marker == 14:
        
         # fourth Pose for detecting markers 
            q =[ 2.9 , 2.3, -2.3, 0.0 , 0.0, 0.7] 
            rospy.loginfo("q_joint= %s" % q[2]  )
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[2])
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[1])
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[0])
            pub0.publish(q[0])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[3])
            pub3.publish(q[3])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[4])
            pub4.publish(q[4])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[5])
            pub5.publish(q[5])
            rate2.sleep()
        
            
            rospy.Subscriber("/marker_id", Float64, mar_id)
            rospy.loginfo("position of marker : %s "%marker )
            rate.sleep()
        
        elif marker == 15:
        
         # fiveth Pose for detecting markers 
            q =[ -1.5, 2.2, -3.14, 0.3 , 0.3,1] 
            rospy.loginfo("q_joint= %s" % q[1]  )
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[1])
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[2])
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[0])
            pub0.publish(q[0])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[3])
            pub3.publish(q[3])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[4])
            pub4.publish(q[4])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[5])
            pub5.publish(q[5])
            rate2.sleep()
        
            
            rospy.Subscriber("/marker_id", Float64, mar_id)
            rospy.loginfo("position of marker : %s "%marker )
            rate.sleep()
            
        
        elif marker == 13:
        
        # sixth Pose for detecting markers 
            q =[ 0.6, 1.8, -3.14, 0.3 , 0.3,1.4] 
            rospy.loginfo("q_joint= %s" % q[1]  )
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[1])
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[2])
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[0])
            pub0.publish(q[0])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[3])
            pub3.publish(q[3])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[4])
            pub4.publish(q[4])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[5])
            pub5.publish(q[5])
            rate2.sleep()
        
            
            rospy.Subscriber("/marker_id", Float64, mar_id)
            rospy.loginfo("position of marker : %s "%marker )
            rate.sleep()
            
        elif marker == 11:
        # seventh Pose for detecting markers
            
            rospy.Subscriber("/marker_id", Float64, mar_id)
             
            q =[ 1.5708, 2, -3.14, 0.3 , 0.3,1.4] 
            rospy.loginfo("q_joint= %s" % q[1]  )
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[1])
            pub1.publish(q[1])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[2])
            pub2.publish(q[2])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[0])
            pub0.publish(q[0])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[3])
            pub3.publish(q[3])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[4])
            pub4.publish(q[4])
            rate2.sleep()
            rospy.loginfo("q_joint= %s " % q[5])
            pub5.publish(q[5])
            rate2.sleep()
       
            
            rospy.Subscriber("/marker_id", Float64, mar_id)
            rospy.loginfo("position of marker : %s "%marker )
            rate.sleep()
            
        else:
            break
         
         
def ZERO_pose():

    rate2 = rospy.Rate(2) # 2 Hz
    
    q = [ 0, 0, 0, 0 , 0 ,0] 
    rospy.loginfo("q_joint= %s" % q[5]  )
    pub5.publish(q[5])
    rate2.sleep()
    rospy.loginfo("q_joint= %s" % q[4]  )
    pub4.publish(q[4])
    rate2.sleep()
    rospy.loginfo("q_joint= %s" % q[3]  )
    pub3.publish(q[3])
    rate2.sleep()
    rospy.loginfo("q_joint= %s" % (q[2]-1))
    pub2.publish((q[2] - 1))
    rate2.sleep()
    rospy.loginfo("q_joint= %s" % q[0]  )
    pub0.publish(q[0])
    rate2.sleep()
    rospy.loginfo("q_joint= %s" % q[1]  )
    pub1.publish(q[1])
    rate2.sleep()
    rospy.loginfo("q_joint= %s" % q[2]  )
    pub2.publish(q[2])
    rate2.sleep()
    rospy.loginfo(" Pose ZERO Achieved" )
    
              
def Build_Ont_map():
    
    path = dirname(realpath(__file__))
    path = path + "/topological_map/"

    client = ArmorClient("My_client", "My_reference")
    client.utils.load_ref_from_file(path + "topologicalMap.owl", "http://bnc/exp-rob-lab/2022-23",True,"PELLET", False )
    client.call('ADD','IND','CLASS',['Robot1', 'ROBOT'])
    client.call('APPLY','','',[])
    client.call('REASON','','',[])
    rospy.loginfo("ADD IND Robot1 to ROBOT")
    client.call('ADD','DATAPROP','IND',['urgencyThreshold','Robot1', 'Long','1'])
    client.call('APPLY','','',[])
    client.call('REASON','','',[])
    rospy.loginfo("ADD DATAPROPERTY urgencyThreshold to Robot1")

    for i in range(0,len(Room)):
        
        name=Room[i].room
        if name == 'E':
            
            client.call('ADD','IND','CLASS',[name, 'URGENT'])
            client.call('APPLY','','',[])
            client.call('REASON','','',[])
            rospy.loginfo("ADD %s URGENT"%name)
        else:
            
            client.call('ADD','IND','CLASS',[name, 'ROOM'])
            client.call('APPLY','','',[])
            client.call('REASON','','',[])
            rospy.loginfo("ADD %s ROOM" %name)
        
        xy_prop=str(Room[i].x)
        
        client.call('ADD','DATAPROP','IND',['x',name, 'Float',xy_prop])
        client.call('APPLY','','',[])
        client.call('REASON','','',[])
        print("ADD DATAPROPERTY x:" , xy_prop , " to" , name)
        xy_prop=str(Room[i].y)
        
        client.call('ADD','DATAPROP','IND',['y',name, 'Float',xy_prop])
        client.call('APPLY','','',[])
        client.call('REASON','','',[])
        print("ADD DATAPROPERTY y:",xy_prop, " to" ,name)
        client.call('ADD','DATAPROP','IND',['visitedAt',name, 'Long','1665579740'])
        client.call('APPLY','','',[])
        client.call('REASON','','',[])
        print("ADD DATAPROPERTY visitedAt: 1665579740 to %s " %name)
        con=Room[i].connections
        for j in range(0,len(con)):
            
            door=con[j].through_door
            door= "'" + door + "'"
            client.call('ADD','IND','CLASS',[door, 'DOOR'])
            client.call('APPLY','','',[])
            client.call('REASON','','',[])
            print("ADD IND %s to DOOR " %name)
            client.call('ADD','OBJECTPROP','IND',['hasDoor',name, door])
            client.call('APPLY','','',[])
            client.call('REASON','','',[])
            print("ADD OBJECTPROPERTY hasDoor:", name, "to", door)
            conect=con[j].connected_to
            conect= "'" + conect + "'"
            client.call('ADD','OBJECTPROP','IND',['connect_to',name, conect]) 
            client.call('APPLY','','',[])
            client.call('REASON','','',[])
            print("ADD OBJECTPROPERTY connected_to: ", name," to ",conect)  
        
    client.call('ADD','OBJECTPROP','IND',['IsIn','Robot1', 'E'])
    client.call('APPLY','','',[])
    client.call('REASON','','',[])
    rospy.loginfo("ADD OBJECTPROPERTY IsIn: Robot1 to 'E' " )
    client.call('ADD','DATAPROP','IND',['now','Robot1', 'Long','1665579740'])
    client.call('APPLY','','',[])
    client.call('REASON','','',[])
    rospy.loginfo("ADD DATAPROP now:1665579740 to Robot1 " )
    client.call('DISJOINT','IND','CLASS',['URGENT'])
    client.call('DISJOINT','IND','CLASS',['ROOM'])
    client.call('DISJOINT','IND','CLASS',['DOOR'])
    client.call('APPLY','','',[])
    client.call('REASON','','',[])
    rospy.loginfo("CLASSES DISJOINT ")
    path=path + "Assignment.owl"
    client.call('SAVE','INFERENCE','',[path])
    rospy.loginfo("SAVE ontological map in /topological_map with name Assignment.owl")
 

 
if __name__ == '__main__':
   
    pub1 = rospy.Publisher('/arm/joint0_position_controller/command', Float64, queue_size=10)
    pub2 = rospy.Publisher('/arm/joint1_position_controller/command', Float64, queue_size=10)
    pub3 = rospy.Publisher('/arm/joint2_position_controller/command', Float64, queue_size=10)
    pub4 = rospy.Publisher('/arm/joint3_position_controller/command', Float64, queue_size=10)
    pub5 = rospy.Publisher('/arm/joint4_position_controller/command', Float64, queue_size=10)
    pub0 = rospy.Publisher('/arm/joint5_position_controller/command', Float64, queue_size=10)
	
    
    rospy.init_node('My_onto_Map', anonymous=True)

    try:
    	tic=time.time()	
    	joint_move()
    	rospy.loginfo("ROBOT ARE DETECTED %s ROOMS " %len(Room))
    	Build_Ont_map()
    	toc=time.time()
    	print("TIME: of BUILD map: %f " %(toc-tic))
    	ZERO_pose()
    except rospy.ROSInterruptException:
        pass
