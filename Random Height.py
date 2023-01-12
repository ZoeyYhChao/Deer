"""Provides a scripting component.
    Inputs:
        List: The list of heights data from osm.
        MPStorey: number slider input for meters per storey.
        MINStoreys: number slider input for minimum number of storey.
        MAXStoreys: number slider input for maximum number of storey.
    Output:
        Heights: Create random heights for null"""
        
__author__ = "zoeyYhChao"

#Random Heights Generator

import rhinoscriptsyntax as rs
import xml.etree.ElementTree as ET
import ghpythonlib.treehelpers as th
import random
import math

def height():
    
    def MPStorey(meters):
        for mps in range(meters):
            print MINStoreys(meters)
                
    def MINStoreys(minimum):
        for mins in range(minimum):
            print MAXStoreys(minimum)
                
    def MAXStoreys(maximum):
        for maxs in range(maximum):
            print()
            
height()

for i in range (len(List)):
    if List[i] == None:
        List[i] = random.randrange(MPStorey * MINStoreys, MPStorey * MAXStoreys + 1)


Heights = th.list_to_tree(List)
