# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 09:21:51 2019

@author: xkadj
"""

import os
import pandas as pd

dir = r"C:\Users\xkadj\OneDrive\PROJEKTY\IGA\IGA19 - Smartphone\MERENI\200313_kedluben"

output_dataframe = pd.DataFrame()
folders_list = [x[0] for x in os.walk(dir)]

for measurement_dir in folders_list[1:]:
    if "unused" in measurement_dir: continue    #filter using by "unused" in any folder name
    variant_name = measurement_dir.split('\\')[-2]
    leaf_name = measurement_dir.split('\\')[-1]
    
    files = os.listdir(measurement_dir)    
    csvs = [i for i in files if 'csv' in i]
    csvfilepaths = [os.path.join(dir, variant_name, leaf_name, name) for name in csvs]

    for csv_path in csvfilepaths:
        print(" - variant name: " + str(variant_name) + " - leaf name: " + str(leaf_name) + "csv path: " + str(csv_path))
        leaf = pd.read_csv(csv_path,';')
        leaf = leaf.iloc[:, :-1]        #erase last column
        for measurement_number in leaf.measurement.drop_duplicates():
            measurement = leaf.where(leaf.measurement == measurement_number).dropna()
            measurement_mean = measurement.mean()
            measurement_mean.at['leaf'] = leaf_name
            measurement_mean.at['variant'] = variant_name
            output_dataframe = output_dataframe.append(measurement_mean,ignore_index=True)

output_dataframe = output_dataframe[['variant', 'leaf', 'measurement',  #reordering of columns in output dataframe
                                     'r', 'g', 'b', 'R', 'G', 'B',
                                     'mean_rgb', 'ExG', 'ExG_n',
                                     'honza_1', 'vasek_1',
                                     'kawa','yuzhu','adam','perez','geor','nas']]

output_file = open(os.path.join(dir, dir.split('\\')[-1] + ".csv"),"w")
output_file.write(output_dataframe.to_csv(index=False,line_terminator='\n'))
output_file.close()


        
        