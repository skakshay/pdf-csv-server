""" PDF to CSV converter

This script allows the user to provide path to pdf file as a command 
line argument. It converts that pdf file to a csv file named 
`output.csv`. Only pdf files are allowed. 


This script requires that `tabula` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * convert_pdf_to_csv - converts the pdf file to csv and saves the csv in current working directory
    * main - the main function of the script
"""

import sys
import tabula
import os
import pandas as pd


# These values are for the sample BalSheet provided. These are found 
# using  crop feature and Inspector tool in Preview application on MAC-OSX

TOP1=128.08
LEFT1=46.09
TOP_HEIGHT1=496.25
LEFT_WIDTH1=372.79

TOP2=131.46
LEFT2=371.78
TOP_HEIGHT2=499.24
LEFT_WIDTH2=678.32

OUTPUT_NAME1 = 'output1.csv'
OUTPUT_NAME2 = 'output2.csv'
OUTPUT_NAME = 'output.csv'
NAMES = ['Particulars', '', '2015', '2016']



def convert_pdf_to_csv(path):
    """Converts the pdf to csv and saves the csv

    Parameters
    ----------
    path : str
        The file location of the pdf

    """

    filename_wo_ext = os.path.splitext(os.path.basename(path))[0]
    tabula.convert_into(path, OUTPUT_NAME1, format='csv', stream=True , pages=1, area=(TOP1, LEFT1, TOP_HEIGHT1, LEFT_WIDTH1))
    tabula.convert_into(path, OUTPUT_NAME2, format='csv', stream=True , pages=1, area=(TOP2, LEFT2, TOP_HEIGHT2, LEFT_WIDTH2))
    df1 = pd.read_csv(OUTPUT_NAME1)
    df2 = pd.read_csv(OUTPUT_NAME2, header=0, names=NAMES)
    pd.concat([df1, df2], axis=1).to_csv(OUTPUT_NAME, index=False)
    os.remove(OUTPUT_NAME1)
    os.remove(OUTPUT_NAME2)
    

if __name__=='__main__':
    if len(sys.argv)<2 : 
        print("Please provide path to pdf file")
        sys.exit(1)
    path = sys.argv[1]
    if os.path.splitext(path)[1]!='.pdf':
        print("Only pdf files are allowed")
        sys.exit(1)
    try:
        convert_pdf_to_csv(path);
    except FileNotFoundError : 
        print("No such file found")
        
