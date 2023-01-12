"""Provides a scripting component.
    Inputs:
        List: The list of heights data from osm
    Output:
        Heights: Create random heights for null"""
        
__author__ = "zoeyYhChao"

#Random Heights Generator

import rhinoscriptsyntax as rs
import xml.etree.ElementTree as ET
import ghpythonlib.treehelpers as th
import random
import math

m_per_storey = 3
min_storeys = 2
max_storeys = 11

for i in range (len(List)):
    if List[i] == None:
        List[i] = random.randrange(min_storeys, max_storeys+1)

Heights = th.list_to_tree(List)
