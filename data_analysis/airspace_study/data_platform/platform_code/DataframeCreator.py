# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:42:34 2022
@author: jpedrero
"""
import pandas as pd
from pyproj import  Transformer
import os
import EFF_metrics
import SAF_metrics
import AEQ_metrics
import CAP_metrics
import ENV_metrics
import util_functions
import math
from multiprocessing import Pool
import dill
import numpy as np

path_to_logs="input_logs/"
time_filtering=False #If true the data are filtered for the first 1.5 hours of simulation
transformer_2_utm = Transformer.from_crs('epsg:4326','epsg:32633')

def calc_flst_spawn_col(row):

    if type(row["SPAWN_time"])!=float or math.isnan(row["SPAWN_time"]) or (row["SPAWN_time"]>5400 and time_filtering):
        return False
    else:
        return True
    
def calc_flst_mission_completed_col(row):

    if row["DEL_time"]==row["Last_sim_time"] or (row["SPAWN_time"]>5400 and time_filtering) or (row["DEL_time"]>5400 and time_filtering) or row["Spawned"]==False or row["ACID"][0]=="R" or (row["Dest_x"]-row["DEL_x"])*(row["Dest_x"]-row["DEL_x"])+(row["Dest_y"]-row["DEL_y"])*(row["Dest_y"]-row ["DEL_y"])>8000*8000:
        return False
    else:
        return True
 
def check_transition_type_coherence(row):

     if row[ "Transition_type"]!=row[ "Int_transition_type"] and row[ "Transition_type"]!=1 :
         return 1
     else:
         return 0   


def update_scenario_name(row):
    return row["scenario_name"][:-1]

#concept_names=["noflow","noflowfulldenalloc","noflowrandomalloc","noflowdistalloc"]        

##Keep one concept only for testing
concept_names=["noflow","noflowfulldenalloc","noflowrandomalloc","noflowdistalloc", "noflowMP20", "noflowdistallocMP20"]


class DataframeCreator():

    def __init__(self,threadnum):


        
        self.log_names=[]
        self.flight_intention_names=[]
        self.get_file_names()
        self.threads=threadnum        
        input_file=open("data/baseline_routes.dill", 'rb')
        self.baseline_length_dict=dill.load(input_file)
        
    def compute_env3_statistics(self):
        return
    
    def create_dataframes(self):

        self.create_flstlog_dataframe() 
        self.create_loslog_dataframe() 
        self.create_conflog_dataframe() 
        self.create_env_metrics_dataframe()
        self.create_density_dataframe()
        self.create_density_constrained_dataframe()
        self.create_layer_transitions_dataframe()
        self.create_metrics_dataframe()
        
        
        return
    
    def get_file_names(self):
        self.flight_intention_names=os.listdir(path_to_logs+"Flight_intentions")
        self.log_names=os.listdir(path_to_logs+"Logs")
     
 
        

    ##LOSLOG dataframe
    def create_loslog_dataframe(self):
        
        col_list = ["LOS_id", "Scenario_name", "LOS_exit_time", "LOS_start_time", "LOS_duration_time", "LAT1", "LON1", "ALT1", "LAT2", "LON2", "ALT2", "DIST","crash","in_time","constrained"]
        
        loslog_list = list()
        constrained_airspace=util_functions.Constrained_airspace()
        los_id=0
        ##Read LOSLOGs
        for ii,file_name in enumerate(self.log_names):
            log_type = file_name.split("_")[0]
            if log_type=="LOSLOG":
                log_file=path_to_logs+"Logs/"+file_name
                

                file_name=file_name.split(".")[0]
                scenario_var = file_name.split("_")
                if scenario_var[3]=="very": 
                    density="very_low"
                    distribution=scenario_var[5]
                    repetition=scenario_var[6]
                    if len(scenario_var)==7 :
                        concept="baseline"
                    else:
                        concept=scenario_var[7]
                        if not concept in concept_names:
                            concept="baseline"
                else:
                    density=scenario_var[3]
                    distribution=scenario_var[4]
                    repetition=scenario_var[5]
                    if len(scenario_var)==6 :
                        concept="baseline"
                    else:
                        concept=scenario_var[6] 
                        if not concept in concept_names:
                            concept="baseline"
                
                scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
                loslog_file = open(log_file, "r")
        
                
                cnt = 0
                for line in loslog_file:
                    cnt = cnt + 1
                    
                    if cnt < 10:
                        continue
                    line_list = line.split(",")
                    tmp_list = [los_id, scenario_name]
                    los_id=los_id+1
                    for iv, value in enumerate(line_list):
                        if iv<2:
                            tmp_list.append(float(value))
                        elif iv==2:
                            tmp_list.append(float(line_list[0])-float(line_list[1]))
                        elif iv>4 and iv <11:
                            tmp_list.append(float(value))
                        elif iv==11:
                            tmp_list.append(float(value[:-2]))
        
        
                    crash=False
                    #If the aircarft are closer than 1.7 in the horizontal diraction and 0.75 in the vetrical teh LOS is considere a crash
                    #Aircraft dimmensions from https://www.dji.com/gr/matrice600-pro/info#specs
                    if float(line_list[11][:-2])<=1.7 and abs(float(line_list[7])-float(line_list[10]))<2.46:
                        crash=True
                        
                    tmp_list.append(crash)
                    
                    in_time=True
                    if time_filtering:
                        if tmp_list[3]>5400:
                            in_time=False
                    
                    tmp_list.append(in_time)
                    
                    
                    lat=float(line_list[5])
                    lon=float(line_list[6])
                    
                    constrained=constrained_airspace.inConstrained([lon,lat])
                    
                    tmp_list.append(constrained)

                    loslog_list.append(tmp_list)
        
        loslog_data_frame = pd.DataFrame(loslog_list, columns=col_list)
                
        print("LOSLOG dataframe created!")
    
        
        output_file=open("dills/loslog_dataframe.dill", 'wb')
        dill.dump(loslog_data_frame,output_file)
        output_file.close()


    ####
    def ccthread(self,x):
        file_name = x[1]
        tmp_list=[]
        tmp2_list=[]     
        constrained_airspace=util_functions.Constrained_airspace()
        log_file=path_to_logs+"Logs/"+file_name

            
        file_name=file_name.split(".")[0]
        scenario_var = file_name.split("_")

        if scenario_var[3]=="very": 
            density="very_low"
            distribution=scenario_var[5]
            repetition=scenario_var[6]
            if len(scenario_var)==7 :
                concept="baseline"
            else:
                concept=scenario_var[7]
                if concept not in concept_names:
                    concept="baseline"

        else:
            density=scenario_var[3]
            distribution=scenario_var[4]
            repetition=scenario_var[5]
            if len(scenario_var)==6 :
                concept="baseline"
            else:
                concept=scenario_var[6] 
                if concept not in concept_names:
                    concept="baseline"

        scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
        conflog_file = open(log_file, "r")

        
        cnt = 0
        for line in conflog_file:
            cnt = cnt + 1
            if cnt < 10:
                continue
            line_list = line.split(",")
            tmp_list = [scenario_name]
            for iv, value in enumerate(line_list):
                if iv==0 or iv==9:
                    tmp_list.append(float(value))
                elif iv==10:
                    tmp_list.append(float(value[:-2]))
                    
            in_time=True
            if time_filtering:
                if tmp_list[2]>5400:
                    in_time=False
            
            tmp_list.append(in_time)
            
            lat=float(line_list[3])
            lon=float(line_list[4])
            
            constrained=constrained_airspace.inConstrained([lon,lat])
            
            tmp_list.append(constrained)
            
            tmp2_list.append(tmp_list)
        return tmp2_list
    ##CONFLOG dataframe
    def create_conflog_dataframe(self):
        col_list = ["CONF_id", "Scenario_name", "CONF_detected_time", "CPALAT", "CPALON","in_time","constrained"] 
        conflog_list = list()
        maplist=[]        
        ##Read CONFLOGs
        for ii,file_name in enumerate(self.log_names):
            log_type = file_name.split("_")[0]
            if log_type=="CONFLOG":
                maplist.append([ii,file_name]) 
        pool = Pool(processes=self.threads) 
        conflog_list=pool.map(self.ccthread, maplist)
        pool.close()
        pool.join()
        conflog_list = [x for row in conflog_list for x in row]  
        for i in range(len(conflog_list)):
            conflog_list[i].insert(0, i)        

        conflog_data_frame = pd.DataFrame(conflog_list, columns=col_list)

                
        print("CONFLOG Dataframe created!")
        
        
        output_file=open("dills/conflog_dataframe.dill", 'wb')
        dill.dump(conflog_data_frame,output_file)
        output_file.close()
        

    
    def flst_stage1_thread(self,x):
       
        file_name = x[1]
     
        tmp_list=[]
        flint_list=[]
        flight_file=path_to_logs+"Flight_intentions/"+file_name        
        file_name=file_name.split(".")[0]
        scenario_var = file_name.split("_")
        if scenario_var[2]=="very": 
            density="very_low"
            distribution=scenario_var[4]
            repetition=scenario_var[5]
 
        else:
            density=scenario_var[2]
            distribution=scenario_var[3]
            repetition=scenario_var[4]


            
        if 1:

            flight_int_file = open(flight_file, "r")
            
            for line in  flight_int_file:

                flight_data=line.split(",")
                acid=flight_data[1]
                aircraft_type=flight_data[2]
                time_data=flight_data[3].split(":")
                time=int(time_data[2])+int(time_data[1])*60+int(time_data[0])*3600
                priority=flight_data[8]
                origin_lon=round(float(flight_data[4].split("(")[1]),10)
                dest_lon=round(float(flight_data[6].split("(")[1]),10)
                origin_lat=round(float(flight_data[5].split(")")[0]),10)
                dest_lat=round(float(flight_data[7].split(")")[0]) ,10)
                
                transformer = Transformer.from_crs('epsg:4326','epsg:32633')
                p=transformer.transform( dest_lat,dest_lon)
                dest_x=p[0]
                dest_y=p[1]
                
                loitering=False
                
                    
                cruising_speed=10.29 # m/s
                if aircraft_type=="MP30": 
                    cruising_speed=15.43 # m/s
                    
                base_2d_dist=self.baseline_length_dict[str(origin_lat)+"-"+str(origin_lon)+"-"+str(dest_lat)+"-"+str(dest_lon)] 
                base_vertical_dist=util_functions.compute_baseline_vertical_distance(loitering)
                base_ascending_dist=util_functions.compute_baseline_ascending_distance()
                base_3d_dist=base_2d_dist+base_vertical_dist
                base_flight_time= util_functions.compute_baseline_flight_time(base_2d_dist,aircraft_type)
            
                base_arrival_time=base_flight_time+time
            
            
            
                for concept in concept_names:
                    scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
       
                
                
                    tmp_list = [scenario_name, acid,origin_lat,origin_lon,dest_lat,dest_lon,time,cruising_speed,priority,loitering,base_2d_dist,base_vertical_dist,base_ascending_dist,\
                            base_3d_dist,base_flight_time,base_arrival_time,dest_x,dest_y]
                    flint_list.append(tmp_list)
              
        return flint_list
    
    def flst_stage2_thread(self,x): 
        file_name = x[1]
        tmp_list=[]
        flstlog_list = list() 
        log_file=path_to_logs+"Logs/"+file_name

            
        file_name=file_name.split(".")[0]
        scenario_var = file_name.split("_")

        if scenario_var[3]=="very": 
            density="very_low"
            distribution=scenario_var[5]
            repetition=scenario_var[6]
            if len(scenario_var)==7 :
                concept="baseline"
            else:
                concept=scenario_var[7]
                if not concept in concept_names:
                    concept="baseline"

        else:
            density=scenario_var[3]
            distribution=scenario_var[4]
            repetition=scenario_var[5]
            if len(scenario_var)==6:
                concept="baseline"
            else:
                concept=scenario_var[6]   
                if not concept in concept_names:
                    concept="baseline"

      
        scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"  

   
        flstlog_file = open(log_file, "r")


        for line in flstlog_file:
            last_sim_time=line.split(",")[0]
            
        flstlog_file = open(log_file, "r")
        cnt = 0
        for line in flstlog_file:
            cnt = cnt + 1
            if cnt < 10:
                continue
            line_list = line.split(",")
            
            ascend_dist=util_functions.compute_ascending_distance(float(line_list[6]),float(line_list[10]))
            work_done=util_functions.compute_work_done(ascend_dist,float(line_list[3])) 
            
            transformer = Transformer.from_crs('epsg:4326','epsg:32633')
            p=transformer.transform(  float(line_list[8]), float(line_list[9]))
            del_x=p[0]
            del_y=p[1]
            
        
            
            actual_horizontal_distance=float(line_list[4]) 
            actual_3d_distance=float(line_list[5])
            actual_flight_duration=float(line_list[3]) 
            actual_deletion_time=float(line_list[0]) 
            

            
            
            tmp_list = [scenario_name, line_list[1], actual_deletion_time, float(line_list[2]),actual_flight_duration,actual_horizontal_distance, actual_3d_distance, float(line_list[6]),\
                        float(line_list[8]), float(line_list[9]), float(line_list[10]),ascend_dist,work_done,del_x,del_y,last_sim_time]

            flstlog_list.append(tmp_list)
            
            
            
        return flstlog_list
    ##FLSTLOG dataframe
    def create_flstlog_dataframe(self):

        col_list = ['Flight_id', "scenario_name", "ACID", "Origin_LAT","Origin_LON", "Dest_LAT","Dest_LON", "Baseline_deparure_time", "cruising_speed",
                    "Priority","loitering","Baseline_2D_distance","Baseline_vertical_distance","Baseline_ascending_distance","Baseline_3D_distance",\
                        "Baseline_flight_time","Baseline_arrival_time","Dest_x","Dest_y"]
            

        
        agg_list=[]
        maplist=[]         
        flint_list = list()
                    
        for ii,file_name in enumerate(self.flight_intention_names):
            maplist.append([ii,file_name]) 
        pool = Pool(processes=self.threads) 
        agg_list=pool.map(self.flst_stage1_thread, maplist)
        pool.close()
        pool.join()        
        pool.close()
        pool.join()        
        flint_list = [x for row in agg_list for x in row]
     
        for i in range(len(flint_list)):
            flint_list[i].insert(0, i)

        flstlog_data_frame = pd.DataFrame(flint_list, columns=col_list)
        
      
        agg_list=[]
        flint_list=[]
        maplist=[]  
        
        
        col_list = ["scenario_name", "ACID", "DEL_time", "SPAWN_time",
                     "FLIGHT_time", "2D_dist", "3D_dist", "ALT_dist",  "DEL_LAT" \
             , "DEL_LON", "DEL_ALT","Ascend_dist","work_done","DEL_x","DEL_y" ,"Last_sim_time"]
        flstlog_list = list()
       
     
        pool = Pool(processes=self.threads) 
         ##Read FLSTLOGs
        for ii,file_name in enumerate(self.log_names):
             log_type = file_name.split("_")[0]
             if log_type=="FLSTLOG":
                 maplist.append([ii,file_name])
        agg_list=pool.map(self.flst_stage2_thread, maplist)
        pool.close()
        pool.join()        
        flstlog_list = [x for row in agg_list for x in row]
 
        flst_data_frame = pd.DataFrame(flstlog_list, columns=col_list)


        flstlog_data_frame=pd.merge(flst_data_frame,flstlog_data_frame,on=["ACID","scenario_name"],how="outer")
        


        
        flstlog_data_frame['Arrival_delay']  =   flstlog_data_frame["DEL_time"] -flstlog_data_frame["Baseline_arrival_time"]
        flstlog_data_frame['Departure_delay']=flstlog_data_frame["SPAWN_time"] -flstlog_data_frame["Baseline_deparure_time"]
        flstlog_data_frame['Spawned'] =flstlog_data_frame.apply(calc_flst_spawn_col,axis=1)
        flstlog_data_frame['Mission_completed'] =flstlog_data_frame.apply(calc_flst_mission_completed_col,axis=1)
        
        
        flstlog_data_frame=flstlog_data_frame.drop(["Dest_x","Dest_y","DEL_x","DEL_y"],axis=1)  
        


        print("FLSTLOG Dataframe created!")

        ##check if baseline 2d distance is larger than actual 2d distance
        df_shape=flstlog_data_frame[(flstlog_data_frame["2D_dist"]<flstlog_data_frame["Baseline_2D_distance"]) &(flstlog_data_frame["Mission_completed"]) ].shape[0]
        if df_shape:
            print("Baseline_2D disatnce is larger than actual 2d distance in ",df_shape," cases")
        

        ##check if baseline flight time is larger than actual flight time
        df_shape=flstlog_data_frame[(flstlog_data_frame["FLIGHT_time"]<flstlog_data_frame["Baseline_flight_time"]) &(flstlog_data_frame["Mission_completed"]) ].shape[0]
        if df_shape:
            print("Baseline_flight_time is larger than actual flight time in ",df_shape," cases")
        
        
        
        
        output_file=open("dills/flstlog_dataframe.dill", 'wb')
        dill.dump(flstlog_data_frame,output_file)
        output_file.close()
          
    ##FlowLOG dataframe
    def read_flowlog(self, log_file):
        reglog_file = open(log_file, "r")
 
        number_of_replans=0
        number_of_attempted_replans=0
        number_update_graph_no_replan=0
        number_high_traffic_no_replan=0
        number_last_point_no_replan=0
        


        cnt_modulo = 0
        cnt = 0
        for line in reglog_file:
            cnt = cnt + 1
            if cnt < 10:
                continue

            if cnt_modulo % 12 == 5:
                l=line[:-2]
                airspace_type=l.split(",")
              
            elif cnt_modulo % 12 == 6:
                l=line[:-2]
                k=l.split(",")
                for r in k[1:]:
                    if int(float(r))==1:
                        number_of_replans=number_of_replans+1
                
              
            elif cnt_modulo % 12 == 7:
                l=line[:-2]
                k=l.split(",")
                for r in k[1:]:
                    if int(float(r))==1:
                        number_of_attempted_replans=number_of_attempted_replans+1
            elif cnt_modulo % 12 == 8:
                l=line[:-2]
                k=l.split(",")
                for r in k[1:]:
                    if int(float(r))==1:
                        number_update_graph_no_replan=number_update_graph_no_replan+1
            elif cnt_modulo % 12 == 9:
                l=line[:-2]
                k=l.split(",")
                for r in k[1:]:
                    if int(float(r))==1:
                        number_high_traffic_no_replan=number_high_traffic_no_replan+1
            elif cnt_modulo % 12 == 10:
                l=line[:-2]
                k=l.split(",")
                for r in k[1:]:
                    if int(float(r))==1:
                        number_last_point_no_replan=number_last_point_no_replan+1             
                
            cnt_modulo = cnt_modulo + 1

        return number_of_replans, number_of_attempted_replans, number_update_graph_no_replan, number_high_traffic_no_replan, number_last_point_no_replan 


   
                        
    def cflowthread(self,x):
        file_name = x[1]
        tmp_list=[] 
        log_file=path_to_logs+"Logs/"+file_name
            
        file_name=file_name.split(".")[0]
        scenario_var = file_name.split("_")
        if scenario_var[3]=="very": 
            density="very_low"
            distribution=scenario_var[5]
            repetition=scenario_var[6]
            if len(scenario_var)==7:
                concept="baseline"
            else:
                concept=scenario_var[7]
                if not concept in concept_names:
                    concept="baseline"

        else:
            density=scenario_var[3]
            distribution=scenario_var[4]
            repetition=scenario_var[5]
            if len(scenario_var)==6:
                concept="baseline"
            else:
                concept=scenario_var[6]    
                if not concept in concept_names:                
                    concept="baseline"

        
        scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
        #print(scenario_name)
        
        

        number_of_replans, number_of_attempted_replans, number_update_graph_no_replan, number_high_traffic_no_replan, number_last_point_no_replan = self.read_flowlog(log_file)


        tmp_list = [ scenario_name,number_of_replans, number_of_attempted_replans, number_update_graph_no_replan, number_high_traffic_no_replan, number_last_point_no_replan]
        return tmp_list          

    def create_flow_metrics_dataframe(self):
        
        col_list = ["Scenario_name","Replans","Attempted_replans","Update_graph_no_replan","High_traffic_no_replan","Last_point_no_replan"]
        
        flow_mertics_list = list()
        maplist=[]        
        ##Read REGLOGs
        for ii,file_name in enumerate(self.log_names):
 
            log_type = file_name.split("_")[0]
            if log_type=="FLOWLOG":
                maplist.append([ii,file_name]) 
        pool = Pool(processes=self.threads) 
        env_mertics_list=pool.map(self.cflowthread, maplist)
        pool.close()
        pool.join()    
        flow_metrics_data_frame = pd.DataFrame(env_mertics_list, columns=col_list)

        print("FLOW_MERTICS Dataframe created!")
        
        output_file=open("dills/flow_metrics_dataframe.dill", 'wb')
        dill.dump(flow_metrics_data_frame,output_file)
        output_file.close()
        
        return
     

    ####

    ##REGLOG dataframe
    def read_reglog(self, log_file):
        reglog_file = open(log_file, "r")

        acid_lines_list = []
        alt_lines_list = []
        lon_lines_list = []
        lat_lines_list = []

        cnt_modulo = 0
        cnt = 0
        for line in reglog_file:
            cnt = cnt + 1
            if cnt < 10:
                continue

            if cnt_modulo % 7 == 0:
                acid_lines_list.append(line[:-2])
            elif cnt_modulo % 7 == 1:
                alt_lines_list.append(line[:-2])
            elif cnt_modulo % 7 == 2:
                lat_lines_list.append(line[:-2])
            elif cnt_modulo % 7 == 3:

                lon_lines_list.append(line[:-2])
            cnt_modulo = cnt_modulo + 1

        return acid_lines_list, alt_lines_list, lon_lines_list, lat_lines_list

   
    def read_flowlog_as_reglog(self, log_file):
         reglog_file = open(log_file, "r")

         acid_lines_list = []
         alt_lines_list = []
         lon_lines_list = []
         lat_lines_list = []

         cnt_modulo = 0
         cnt = 0
         for line in reglog_file:
             cnt = cnt + 1
             if cnt < 10:
                 continue

             if cnt_modulo % 12 == 0:
                 acid_lines_list.append(line[:-2])
             elif cnt_modulo % 12 == 1:
                 alt_lines_list.append(line[:-2])
             elif cnt_modulo % 12 == 2:
                 lat_lines_list.append(line[:-2])
             elif cnt_modulo % 12 == 3:

                 lon_lines_list.append(line[:-2])
             cnt_modulo = cnt_modulo + 1

         return acid_lines_list, alt_lines_list, lon_lines_list, lat_lines_list       

   
                        
    def cemthread(self,x):
        file_name = x[1]
        tmp_list=[] 
        log_file=path_to_logs+"Logs/"+file_name
            
        file_name=file_name.split(".")[0]
        scenario_var = file_name.split("_")
        if scenario_var[3]=="very": 
            density="very_low"
            distribution=scenario_var[5]
            repetition=scenario_var[6]
            if len(scenario_var)==7:
                concept="baseline"
            else:
                concept=scenario_var[7]
                if not concept in concept_names:
                    concept="baseline"

        else:
            density=scenario_var[3]
            distribution=scenario_var[4]
            repetition=scenario_var[5]
            if len(scenario_var)==6:
                concept="baseline"
            else:
                concept=scenario_var[6]    
                if not concept in concept_names:                
                    concept="baseline"

        
        scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
        #print(scenario_name)
        
        log_type = file_name.split("_")[0]
            
        if log_type=="FLOWLOG" :
            acid_lines_list, alt_lines_list, lon_lines_list, lat_lines_list = self.read_flowlog_as_reglog(log_file)
        elif log_type=="REGLOG":
            acid_lines_list, alt_lines_list, lon_lines_list, lat_lines_list = self.read_reglog(log_file)
        acid_reg_dict={}


        for i, line in enumerate(acid_lines_list):
            acid_line_list = line.split(",")
            if (float(acid_line_list[0])>5400 and time_filtering) or len(acid_line_list)==1:
                break
            
            try :
                alt_line_list = alt_lines_list[i].split(",")
                lat_line_list = lat_lines_list[i].split(",")
                lon_line_list = lon_lines_list[i].split(",")
            except:
                print('Problem with',file_name)
            
            ##The next lines where in the outer intention
            if i>len(lon_lines_list)-1:
                print('Problem with',file_name)
                continue
    
            for iv, value in enumerate(acid_line_list):
                if iv == 0:
                    continue
                if value in acid_reg_dict.keys():
                    acid_reg_dict[value].append([float(alt_line_list[iv]),float(lat_line_list[iv]),float(lon_line_list[iv])])
                else:
                    acid_reg_dict[value]=[]
                    acid_reg_dict[value].append([float(alt_line_list[iv]),float(lat_line_list[iv]),float(lon_line_list[iv])])

        flight_levels_dict={}
        for j in range(30,510,30):
            flight_levels_dict[j]=0
        flight_levels_list=flight_levels_dict.keys()

        length=0

        for acid in    acid_reg_dict.keys():
            if acid[0]=="R":
                continue
            for j in range(len(acid_reg_dict[acid])-1):
                alt1=acid_reg_dict[acid][j][0]
                lat1=acid_reg_dict[acid][j][1]
                lon1=acid_reg_dict[acid][j][2]
                alt2=acid_reg_dict[acid][j+1][0]
                lat2=acid_reg_dict[acid][j+1][1]
                lon2=acid_reg_dict[acid][j+1][2]
                l=ENV_metrics.compute_eucledean_distance(lat1, lon1, lat2, lon2)
                length+=l
                dict_index=int((alt1+alt2)/(2*30)+0.5)+1
                if dict_index<0:
                    dict_index=0
                if dict_index>len(flight_levels_list)-1:
                    dict_index=len(flight_levels_list)-1
                flight_levels_dict[dict_index*30]+=l
                

        env4_values=list(flight_levels_dict.values())
        env4=(max(env4_values)-min(env4_values))/(length/len(flight_levels_list))

        tmp_list = [ scenario_name,env4]
        return tmp_list      
                  
##REGLOG dataframe
    def create_env_metrics_dataframe(self):
        
        col_list = ["Scenario_name","ENV4"]
        
        env_mertics_list = list()
        maplist=[]        
        
        check_scn_names=[]
        ##Read REGLOGs
        for ii,file_name in enumerate(self.log_names):
 
            log_type = file_name.split("_")[0]
            
            if log_type=="REGLOG" or log_type=="FLOWLOG":
                maplist.append([ii,file_name]) 
                file_name=file_name.split(".")[0]
                scenario_var = file_name.split("_")
                if scenario_var[3]=="very": 
                    density="very_low"
                    distribution=scenario_var[5]
                    repetition=scenario_var[6]
                    if len(scenario_var)==7:
                        concept="baseline"
                    else:
                        concept=scenario_var[7]
                        if not concept in concept_names:
                            concept="baseline"

                else:
                    density=scenario_var[3]
                    distribution=scenario_var[4]
                    repetition=scenario_var[5]
                    if len(scenario_var)==6:
                        concept="baseline"
                    else:
                        concept=scenario_var[6]    
                        if not concept in concept_names:                
                            concept="baseline"

                
                scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
                if scenario_name in check_scn_names:
                    print("Both REG and FLOW for ",scenario_name )
                check_scn_names.append(scenario_name)
                
                
        pool = Pool(processes=self.threads) 
        env_mertics_list=pool.map(self.cemthread, maplist)
        pool.close()
        pool.join()    
        env_emtrics_data_frame = pd.DataFrame(env_mertics_list, columns=col_list)

        print("ENV_MERTICS Dataframe created!")
        
        output_file=open("dills/env_metrics_dataframe.dill", 'wb')
        dill.dump(env_emtrics_data_frame,output_file)
        output_file.close()
        
        return
 

        
  #constrained denisty thread  
    def cdcthread(self,x):
        utils=util_functions.Constrained_airspace()
        file_name = x[1]
        tmp_list=[]
        log_file=path_to_logs+"Logs/"+file_name


            
        file_name=file_name.split(".")[0]
        scenario_var = file_name.split("_")
        if scenario_var[3]=="very": 
            density="very_low"
            distribution=scenario_var[5]
            repetition=scenario_var[6]
            if len(scenario_var)==7:
                concept="baseline"
            else:
                concept=scenario_var[7]
                if not concept in concept_names:
                    concept="baseline"

        else:
            density=scenario_var[3]
            distribution=scenario_var[4]
            repetition=scenario_var[5]
            if len(scenario_var)==6:
                concept="baseline"
            else:
                concept=scenario_var[6]  
                if not concept in concept_names:
                    concept="baseline"

        scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
        
        log_type = file_name.split("_")[0]
            
        if log_type=="FLOWLOG" :
            acid_lines_list, alt_lines_list, lon_lines_list, lat_lines_list = self.read_flowlog_as_reglog(log_file)
        elif log_type=="REGLOG":
            acid_lines_list, alt_lines_list, lon_lines_list, lat_lines_list = self.read_reglog(log_file)

    

        for i, line in enumerate(acid_lines_list):
            acid_line_list = line.split(",")
            if len(acid_line_list)==1:
                break
            try :
                lat_line_list = lat_lines_list[i].split(",")
                lon_line_list = lon_lines_list[i].split(",")
            except:
                print('Problem with',file_name)
            
            ##The next lines where in the outer intention
            if i>len(lon_lines_list)-1:
                print('Problem with',file_name)
                continue
            
            dens=0
    
            for iv, value in enumerate(acid_line_list):
                if iv == 0:
                    continue
                
                if utils.inConstrained([float(lon_line_list[iv]),float(lat_line_list[iv])]):
                    dens+=1
                
             
            tmp_list.append([ scenario_name, float(acid_line_list[0]),dens])
    
        return tmp_list     
    ##DENSITY dataframe
    def create_density_constrained_dataframe(self):
        maplist=[]        
        col_list = [ "scenario_name", "Time_stamp", "Density_constrained"]
        
        densitylog_list = list()
        check_scn_names=[]
        
        ##Read REGLOGs
        for ii,file_name in enumerate(self.log_names):
 
            log_type = file_name.split("_")[0]
            if log_type=="REGLOG" or log_type=="FLOWLOG":
                maplist.append([ii,file_name]) 
                file_name=file_name.split(".")[0]
                scenario_var = file_name.split("_")
                if scenario_var[3]=="very": 
                    density="very_low"
                    distribution=scenario_var[5]
                    repetition=scenario_var[6]
                    if len(scenario_var)==7:
                        concept="baseline"
                    else:
                        concept=scenario_var[7]
                        if not concept in concept_names:
                            concept="baseline"

                else:
                    density=scenario_var[3]
                    distribution=scenario_var[4]
                    repetition=scenario_var[5]
                    if len(scenario_var)==6:
                        concept="baseline"
                    else:
                        concept=scenario_var[6]    
                        if not concept in concept_names:                
                            concept="baseline"

                
                scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
                if scenario_name in check_scn_names:
                    print("Both REG and FLOW for ",scenario_name )
                check_scn_names.append(scenario_name)
        pool = Pool(processes=self.threads)   
        densitylog_list = list()
        densitylog_list=pool.map(self.cdcthread, maplist)
        pool.close()
        pool.join()        
        densitylog_list = [x for row in densitylog_list if row for x in row]
        desnistylog_data_frame = pd.DataFrame(densitylog_list, columns=col_list)
        print("Density constrained Dataframe created!")

        
        
        output_file=open("dills/density_constrained_dataframe.dill", 'wb')
        dill.dump(desnistylog_data_frame,output_file)
        output_file.close()
               
#density thread   
    def cdthread(self,x):
        file_name = x[1]
        tmp_list=[]   
        log_file=path_to_logs+"Logs/"+file_name

            
        file_name=file_name.split(".")[0]
        scenario_var = file_name.split("_")
        if scenario_var[3]=="very": 
            density="very_low"
            distribution=scenario_var[5]
            repetition=scenario_var[6]
            if len(scenario_var)==7:
                concept="baseline"
            else:
                concept=scenario_var[7]
                if not concept in concept_names:
                    concept="baseline"

        else:
            density=scenario_var[3]
            distribution=scenario_var[4]
            repetition=scenario_var[5]
            if len(scenario_var)==6:
                concept="baseline"
            else:
                concept=scenario_var[6]     
                if not concept in concept_names:
                    concept="baseline"
     
        scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
        
        log_type = file_name.split("_")[0]
            
        if log_type=="FLOWLOG" :
            acid_lines_list, alt_lines_list, lon_lines_list, lat_lines_list = self.read_flowlog_as_reglog(log_file)
        elif log_type=="REGLOG":
            acid_lines_list, alt_lines_list, lon_lines_list, lat_lines_list = self.read_reglog(log_file)
            
            
        for i, line in enumerate(acid_lines_list):
            acid_line_list = line.split(",")
             
            tmp_list.append([ scenario_name, float(acid_line_list[0]),len(acid_line_list)-1] )  
    
        return tmp_list 
    ##DENSITY dataframe
    def create_density_dataframe(self):
        
        col_list = [ "scenario_name", "Time_stamp", "Density"]
        
        densitylog_list = list()
        maplist=[]    

        ##Read REGLOGs
        for ii,file_name in enumerate(self.log_names):
 
            log_type = file_name.split("_")[0]
            if log_type=="REGLOG" or log_type=="FLOWLOG":
                maplist.append([ii,file_name])        
        pool = Pool(processes=self.threads) 
        densitylog_list=pool.map(self.cdthread, maplist)
        pool.close()
        pool.join()        
        densitylog_list = [x for row in densitylog_list for x in row]                
        desnistylog_data_frame = pd.DataFrame(densitylog_list, columns=col_list)


        print("DensityLOG Dataframe created!")
        
        
        output_file=open("dills/densitylog_dataframe.dill", 'wb')
        dill.dump(desnistylog_data_frame,output_file)
        output_file.close()
        
        return

    def trans_thread(self,x):
        file_name = x[1]
        tmp_list=[]
        tmp2_list=[]     
        log_file=path_to_logs+"Logs/"+file_name

            
        file_name=file_name.split(".")[0]
        scenario_var = file_name.split("_")

        if scenario_var[3]=="very": 
            density="very_low"
            distribution=scenario_var[5]
            repetition=scenario_var[6]
            if len(scenario_var)==7 :
                concept="baseline"
            else:
                concept=scenario_var[7]
                if concept not in concept_names:
                    concept="baseline"

        else:
            density=scenario_var[3]
            distribution=scenario_var[4]
            repetition=scenario_var[5]
            if len(scenario_var)==6 :
                concept="baseline"
            else:
                concept=scenario_var[6] 
                if concept not in concept_names:
                    concept="baseline"

        scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
        translog_file = open(log_file, "r")
        
        cnt = 0
        for line in translog_file:
            cnt = cnt + 1
            if cnt < 10:
                continue
            line_list = line.split(",")
            end_time=float(line_list[0])
            start_time=float(line_list[1])
            acid=line_list[2]
            trans_type=int(line_list[3])
            if trans_type==12:
                continue #If the transition type is 12, ignore the transition
            int_trans_type=int(line_list[4])
            tmp2_list.append([scenario_name,acid,end_time,start_time,trans_type,int_trans_type])
            
        
        return tmp2_list

    def create_layer_transitions_dataframe(self):
        col_list = ["Transition_id","scenario_name","ACID","End_time", "Start_time", "Transition_type", "Int_transition_type"] 

        
        transition_list = list()
        maplist=[]        
        ##Read CONFLOGs
        for ii,file_name in enumerate(self.log_names):
            log_type = file_name.split("_")[0]
            if log_type=="TRANSLOG":             
                maplist.append([ii,file_name]) 
        pool = Pool(processes=self.threads) 
        transition_list=pool.map(self.trans_thread, maplist)
        pool.close()
        pool.join()
        transition_list = [x for row in transition_list for x in row]  
        for i in range(len(transition_list)):
            transition_list[i].insert(0, i)    


        tranistion_data_frame = pd.DataFrame(transition_list, columns=col_list)
        
        ##Check intend type matches trans type 
        ddf=tranistion_data_frame[tranistion_data_frame["Transition_type"]!=1]
        ddf['Type_coher'] =ddf.apply(check_transition_type_coherence,axis=1)
        dif_types_cnt=ddf['Type_coher'].sum()
        if dif_types_cnt>0:
            print("Number of interrrupted transitions with transition type !=1 is ",dif_types_cnt)
        
        
        ##Filter teh cruise transitions to detect take off
        input_file=open("dills/flstlog_dataframe.dill", 'rb')
        flst_log_dataframe=dill.load(input_file)
        input_file.close()  
        
        tranistion_data_frame=pd.merge(tranistion_data_frame,flst_log_dataframe[["ACID","scenario_name", "Origin_LAT","Origin_LON", "Dest_LAT","Dest_LON","cruising_speed"]],on=["ACID","scenario_name"],how="left")        
        
        
        #Load the constrained length dataframe
        input_file=open("data/constrained_length.dill", 'rb')
        constr_len_dataframe=dill.load(input_file)
        input_file.close() 


        #Add the length of the constarine path as a column for every transistion event logged
        tranistion_data_frame=pd.merge(tranistion_data_frame,constr_len_dataframe,on=[ "Origin_LAT","Origin_LON", "Dest_LAT","Dest_LON","cruising_speed"],how="left")

        
        ##Compute the metrics per scenario
        col_list=["Scenario_name","Trans_per_flight","Inter_trans_per_flgt","Recov_trans_per_flgt","Cr_trans_per_flgt","Ascnhop_trans_per_flgt",\
                  "Dscnhop_trans_per_flgt","Cruise_trans_per_flgt","Turn_trans_per_flgt","Tk-off_trans_per_flgt","Free_trans_per_flgt","Missed_trans_per_flgt",\
                  "Trans_per_km","Inter_trans_per_km","Recov_trans_per_km","Cr_trans_per_km","Ascnhop_trans_per_km",\
                            "Dscnhop_trans_per_km","Cruise_trans_per_km","Turn_trans_per_km","Tk-off_trans_per_km","Free_trans_per_km","Missed_trans_per_km"]
                
        trans_metrics_list=[]
        scenarios=tranistion_data_frame["scenario_name"].unique()
   
        for scn in scenarios:
            df=tranistion_data_frame[tranistion_data_frame["scenario_name"]==scn]
            acid_number=df["ACID"].unique().shape[0]
            ddf=df.drop_duplicates(subset = ["ACID"])
            length_sum=ddf["Constrained_length"].sum()/1000
            tmp_list=[scn]
            
            tmp_list.append(df.shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==1].shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==2].shape[0]/acid_number)
            tmp_list.append(df[(df["Transition_type"]==3) | (df["Transition_type"]==4)].shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==5].shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==6].shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==7].shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==8].shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==9].shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==10].shape[0]/acid_number)
            tmp_list.append(df[df["Transition_type"]==11].shape[0]/acid_number)
            
            tmp_list.append(df.shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==1].shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==2].shape[0]/length_sum)
            tmp_list.append(df[(df["Transition_type"]==3) | (df["Transition_type"]==4)].shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==5].shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==6].shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==7].shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==8].shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==9].shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==10].shape[0]/length_sum)
            tmp_list.append(df[df["Transition_type"]==11].shape[0]/length_sum)



            
            trans_metrics_list.append(tmp_list)
            
 
        trans_metrics_data_frame = pd.DataFrame(trans_metrics_list, columns=col_list)
        
        
        inter_trans_df=tranistion_data_frame[tranistion_data_frame["Transition_type"]==1]
        col_list=["Scenario_name","Recov","CR","Ascnhop","Dscnhop","Cruise","Turn","Tk-off","Free","Missed"]
        inter_trans_metrics_list=[]
        inter_trans_df["Scenario_name"]=inter_trans_df.apply(update_scenario_name,axis=1)
        scenarios=inter_trans_df["Scenario_name"].unique()
        for scn in scenarios:
            df=inter_trans_df[inter_trans_df["Scenario_name"]==scn]
            tmp_list=[scn[:-1]]
            tmp_list.append(df[df["Int_transition_type"]==2].sum())
            tmp_list.append(df[(df["Int_transition_type"]==3) | (df["Int_transition_type"]==4)].sum())
            tmp_list.append(df[df["Int_transition_type"]==5].sum())
            tmp_list.append(df[df["Int_transition_type"]==6].sum())
            tmp_list.append(df[df["Int_transition_type"]==7].sum())
            tmp_list.append(df[df["Int_transition_type"]==8].sum())
            tmp_list.append(df[df["Int_transition_type"]==9].sum())
            tmp_list.append(df[df["Int_transition_type"]==10].sum())
            tmp_list.append(df[df["Int_transition_type"]==11].sum())

            inter_trans_metrics_list.append(tmp_list)

        inter_trans_dataframe= pd.DataFrame(inter_trans_metrics_list, columns=col_list)


        print("Transition Dataframe created!")
        
        
        output_file=open("dills/transition_dataframe.dill", 'wb')
        dill.dump(tranistion_data_frame,output_file)
        output_file.close()
        
        output_file=open("dills/transition_metrics_dataframe.dill", 'wb')
        dill.dump(trans_metrics_data_frame,output_file)
        output_file.close()
        
        output_file=open("dills/interrupted_transition_metrics_dataframe.dill", 'wb')
        dill.dump(inter_trans_dataframe,output_file)
        output_file.close()
                

    ##metrics dataframe
    def create_metrics_dataframe(self):
        col_list = ["Scenario_name","SAF1","SAF1_3","SAF1_4", "SAF2", "SAF2_1","SAF2_2","SAF2_3","SAF3","SAF4", "SAF5","SAF5_1" ]
            
        
        
        input_file=open("dills/loslog_dataframe.dill", 'rb')
        los_log_dataframe=dill.load(input_file)
        input_file.close()
        input_file=open("dills/conflog_dataframe.dill", 'rb')
        conf_log_dataframe=dill.load(input_file)
        input_file.close()

        metrics_list = list()
          
        for ii,file_name in enumerate(self.log_names):
            log_type = file_name.split("_")[0]
            if log_type=="CONFLOG":

                
                file_name=file_name.split(".")[0]
                scenario_var = file_name.split("_")
                if scenario_var[3]=="very": 
                    density="very_low"
                    distribution=scenario_var[5]
                    repetition=scenario_var[6]
                    if len(scenario_var)==7:
                        concept="baseline"
                    else:
                        concept=scenario_var[7]
                        if not concept in concept_names:
                            concept="baseline"

                else:
                    density=scenario_var[3]
                    distribution=scenario_var[4]
                    repetition=scenario_var[5]
                    if len(scenario_var)==6:
                        concept="baseline"
                    else:
                        concept=scenario_var[6]   
                        if not concept in concept_names:
                            concept="baseline"

                
                scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
                #print(scenario_name)

                
                filtered_los_dataframe=los_log_dataframe[los_log_dataframe["Scenario_name"]==scenario_name] 
                filtered_conf_dataframe=conf_log_dataframe[conf_log_dataframe["Scenario_name"]==scenario_name] 
                saf1=SAF_metrics.compute_saf1(filtered_conf_dataframe) 
                saf2=SAF_metrics.compute_saf2(filtered_los_dataframe) 
                saf2_1=SAF_metrics.compute_saf2_1(filtered_los_dataframe) 
                saf3=((saf1-saf2)/saf1)*100
                saf4=SAF_metrics.compute_saf4(filtered_los_dataframe) 
                saf5=SAF_metrics.compute_saf5(filtered_los_dataframe)
               
                saf1_3=SAF_metrics.compute_saf1_3(filtered_conf_dataframe) 
                saf1_4=SAF_metrics.compute_saf1_4(filtered_conf_dataframe) 
                saf2_2=SAF_metrics.compute_saf2_2(filtered_los_dataframe) 
                saf2_3=SAF_metrics.compute_saf2_3(filtered_los_dataframe) 
                saf5_1=SAF_metrics.compute_saf5_1(filtered_los_dataframe)


                tmp_list = [scenario_name, saf1,saf1_3,saf1_4,saf2,saf2_1,saf2_2,saf2_3,saf3,saf4,saf5,saf5_1]
                    
 

                metrics_list.append(tmp_list)
                #print(metrics_list)
                

        
        metrics_data_frame = pd.DataFrame(metrics_list, columns=col_list)
        
        del los_log_dataframe
        del conf_log_dataframe
        
        input_file=open("dills/flstlog_dataframe.dill", 'rb')
        flst_log_dataframe=dill.load(input_file)
        input_file.close()
        

        
        
        col_list = ["Scenario_name", "#Aircraft_number","#Succeful_aircraft_number","#Spawned_aircraft_number","AEQ3","CAP1", "EFF1", "EFF2", "EFF3", "EFF4", "EFF5"]        
        
        metrics_list = list()
              
        
  
        for ii,file_name in enumerate(self.log_names):
            log_type = file_name.split("_")[0]
            if log_type=="CONFLOG":

                
                file_name=file_name.split(".")[0]
                scenario_var = file_name.split("_")
                if scenario_var[3]=="very": 
                    density="very_low"
                    distribution=scenario_var[5]
                    repetition=scenario_var[6]
                    if len(scenario_var)==7:
                        concept="baseline"
                    else:
                        concept=scenario_var[7]
                        if not concept in concept_names:
                            concept="baseline"

                else:
                    density=scenario_var[3]
                    distribution=scenario_var[4]
                    repetition=scenario_var[5]
                    if len(scenario_var)==6:
                        concept="baseline"
                    else:
                        concept=scenario_var[6]   
                        if not concept in concept_names:
                            concept="baseline"

               
                scenario_name=concept+"_"+density+"_"+distribution+"_"+repetition+"_"
                #print(scenario_name,"2")
                
                #Filtered flstlog by scenario name
                filtered_flst_dataframe=flst_log_dataframe[flst_log_dataframe["scenario_name"]==scenario_name]
                

                aircraft_number=filtered_flst_dataframe.shape[0]
                aircraft_succesful_number=filtered_flst_dataframe[filtered_flst_dataframe["Mission_completed"]==True].shape[0]
                aircraft_spawned_number=filtered_flst_dataframe[filtered_flst_dataframe["Spawned"]==True].shape[0]
                
                aeq3=AEQ_metrics.compute_aeq3(filtered_flst_dataframe)
               
                eff1=EFF_metrics.compute_eff1(filtered_flst_dataframe) 
                eff2=EFF_metrics.compute_eff2(filtered_flst_dataframe) 
                eff3=EFF_metrics.compute_eff3(filtered_flst_dataframe) 
                eff4=EFF_metrics.compute_eff4(filtered_flst_dataframe) 
                eff5=EFF_metrics.compute_eff5(filtered_flst_dataframe) 
                cap1=CAP_metrics.compute_cap1(filtered_flst_dataframe)
               
                

                tmp_list = [scenario_name, aircraft_number,aircraft_succesful_number,aircraft_spawned_number, aeq3,cap1,eff1,eff2,eff3,eff4,eff5]
        
                metrics_list.append(tmp_list)
                
           
        metrics_data_frame2 = pd.DataFrame(metrics_list, columns=col_list)
        metrics_data_frame=pd.merge(metrics_data_frame,metrics_data_frame2,on=["Scenario_name"],how="outer")
        
        metrics_data_frame["SAF1_2"]=metrics_data_frame["SAF1"]/metrics_data_frame["#Spawned_aircraft_number"]

        del flst_log_dataframe            
                    
      
               
        input_file=open("dills/env_metrics_dataframe.dill", 'rb')
        env_metrics_dataframe=dill.load(input_file)
        input_file.close()
        
        metrics_data_frame=pd.merge(metrics_data_frame,env_metrics_dataframe,on=["Scenario_name"],how="outer")
        

        
        print("Metrics dataframes created!")
        
        
         
        output_file=open("dills/metrics_dataframe.dill", 'wb')
        dill.dump(metrics_data_frame,output_file)
        output_file.close()
        
        
        
        metrics_data_frame.to_csv("metrics.csv")
        return metrics_data_frame

    ####

 

