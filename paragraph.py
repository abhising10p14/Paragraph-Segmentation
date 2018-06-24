import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

tag = "/home/abhishek/Desktop/input_files/Schedule_Questions/Locations/"
tag = "/home/abhishek/Desktop/input_files/bucket1/scratchdir/7elmavenuellc_bop_03262016to03262017_bop00000065008v_ct_ajg_done/"
#mypath = tag + "11TH STREET STUDIOS LLC_INLAND MARINE_02212016 to 02212017_IM 8976455_CT_AJG_Done_enr.csv"
mypath  = tag + "STRAKE FOUNDATION_BOP_09082017 to 09082018_61 SBA VO4868 SC_CT_AJG_Done_enr.csv"
mypath  = tag + "11TH STREET STUDIOS LLC_INLAND MARINE_02212015 to 02212016_IM 8976455_PT_AJG_Done_enr.csv"
df = pd.read_csv(mypath, sep='\t')
page_num = input("Input the page number ")

df = df[df.Page==page_num]
af = df.drop_duplicates(subset= 'TextLgram')
#af.to_csv("/home/abhishek/Desktop/line_gap/temp_1.csv")

line_gap_list = []
curr_line = []
if(len(af)<=1):
	print ("no df found")
	exit()
prev_y = af.iloc[0]['y0']
for i in range(1,len(af)):
	diff = abs(af.iloc[i]['y0'] - prev_y)
	prev_y = af.iloc[i]['y0']
	curr_line.append(af.iloc[i]['TextLgram'])
	line_gap_list.append(diff)




new_df = pd.DataFrame()
new_df['line_gap'] 	= line_gap_list
new_df['TextLgram'] = curr_line
new_df.to_csv("/home/abhishek/Desktop/line_gap/line_gap_1.csv")

# normalizing the line gaps to get an average gap for detetcting the paraagarphs
X_min  = min(line_gap_list)
X_max  = max(line_gap_list)
X_diff = X_max - X_min
# now updating the line_gap list
#line_gap_list = map(lambda x: ((x-X_min)/(X_diff)),line_gap_list)


# plot the line gaps
y = line_gap_list
x = curr_line
plt.plot(y)
plt.xlabel('lines', weight='bold', size='large')
plt.ylabel('line gaps', weight='bold', size='large')
plt.xticks(range(len(y)), x, rotation=-90)
plt.show()


# Now we need the 2nd order derivative so that we can  get the 
# global maxima to get the paragraphs
# 2nd order derivative is defined as :
# f(x+1,y) + f(x-1,y) -2*f(x,y) ----> in the x direction
# f(x,y+1) + f(x,y-1) -2*f(x,y) ----> in the y direction
# we only need the derivative in the y direction here 

derivative_line_gap = line_gap_list
for i in range(1,len(line_gap_list)-1):
	derivative_line_gap[i] = line_gap_list[i] + line_gap_list[i+1] - 2*line_gap_list[i]



# now plot the 2nd order derivative line gap
# plot the line gaps
y = derivative_line_gap
x = curr_line
plt.plot(y)
plt.xlabel('lines', weight='bold', size='large')
plt.ylabel('2n_order_line gaps', weight='bold', size='large')
plt.xticks(range(len(y)), x, rotation=-90)
plt.show()

import numpy as np
# rejecting those points which are outliers
def reject_outliers(tmp):
    """tmp is a list of numbers"""
    outs = []
    mean = sum(tmp)/(1.0*len(tmp))
    var = sum((tmp[i] - mean)**2 for i in range(0, len(tmp)))/(1.0*len(tmp))
    std = var**0.5
    outs = [i for i in xrange(0, len(tmp)) if abs(tmp[i]-mean) > 1.96*std]
    return outs


filtered_derivative_list = []
rejected_list_index = reject_outliers(derivative_line_gap) 
for i in range(len(derivative_line_gap)):
	if(i not in rejected_list_index):
		filtered_derivative_list.append(derivative_line_gap[i])

#now calculating the average dip in the value
average_dip = 0.0
count_of_dips = 0.0
average_list = []
average_dip_line = []
for i in range(len(filtered_derivative_list)-1):
	if(i==0 ):
		continue
	prev_slope = derivative_line_gap[i-1]
	curr_slope = derivative_line_gap[i]
	next_slope = derivative_line_gap[i+1]
	if(curr_slope<=next_slope):
		continue
	if(curr_slope>next_slope):
		diff = curr_slope-next_slope
		average_list.append(diff)
		average_dip = average_dip + diff
		average_dip_line.append(curr_line[i])
		count_of_dips = count_of_dips + 1.0

average_dip = average_dip/count_of_dips
minimum_dip = min(average_list)
#average_list.sort()
average_dip = 1

print("average dip list:")
print(average_list)
print("lines are :")
print(average_dip_line)
print("average dip: ",average_dip)

# checkjing how many are there with a line gap of less than 1
# forming the paragraph:
paragraph = []
sub_elements = []
sub_elements.append(af.iloc[0]['TextLgram'])
prev_slope = derivative_line_gap[0]
curr_slope = derivative_line_gap[0]
next_slope = derivative_line_gap[1]

for i in range(len(derivative_line_gap)):
	if(i==0 or i == len(derivative_line_gap)-1):
		sub_elements.append(curr_line[i])
		continue
	prev_slope = derivative_line_gap[i-1]
	curr_slope = derivative_line_gap[i]
	next_slope = derivative_line_gap[i+1]
	if(curr_slope<=next_slope or  curr_slope - next_slope <average_dip ):
		sub_elements.append(curr_line[i])
	if(curr_slope>next_slope and curr_slope - next_slope >=average_dip):
		sub_elements.append(curr_line[i])
		paragraph.append(sub_elements)
		sub_elements = []



if(len(sub_elements)>0):
	paragraph.append(sub_elements)


for member in paragraph:
	print("====================================")
	for elements in member:
		print (elements)
		
	print("\n")


