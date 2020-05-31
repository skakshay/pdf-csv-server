

import sys
import tabula
import os
import pandas as pd

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
	filename_wo_ext = os.path.splitext(os.path.basename(path))[0]
	tabula.convert_into(path, OUTPUT_NAME1, format='csv', stream=True , pages=1, area=(TOP1, LEFT1, TOP_HEIGHT1, LEFT_WIDTH1))
	tabula.convert_into(path, OUTPUT_NAME2, format='csv', stream=True , pages=1, area=(TOP2, LEFT2, TOP_HEIGHT2, LEFT_WIDTH2))
	df1 = pd.read_csv(OUTPUT_NAME1)
	df2 = pd.read_csv(OUTPUT_NAME2, header=0, names=NAMES)
	pd.concat([df1, df2], axis=1).to_csv(OUTPUT_NAME, index=False)
	

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
		
