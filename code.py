import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import os

class Main:
    def __init__(self):
        pass
    
    def calRange(valMax,valMin,valImg):#calculate x & y width
        return (valMax-valMin)/valImg
    
    def calCordinate(valMax,valMin,valImg):#calculate x & y coordinate
        return (valMin+(valMax-valMin)/2)/valImg

    def combine_multiple_lists(l1,l2,l3,l4,l5): 
        return list(map(lambda a,b,c,d,e:(a,b,c,d,e), l1,l2,l3,l4,l5)) 

    def combine_lists(l1,l2): 
        return list(map(lambda x,y:(x,y), l1,l2)) 

    @property
    def convert_csv_to_text(self):
        csv_read=pd.read_csv("path to csv file")
        images=csv_read['image_name']
        labels_list = csv_read['class']
        xmin=csv_read['x1']
        xmax=csv_read['x2']
        ymin=csv_read['y1']
        ymax=csv_read['y2']

        labels = labels_list.unique()
        labeldict = dict(zip(labels,range(len(labels))))
        SortedLabelDict = sorted(labeldict.items() ,  key=lambda x: x[1])

        x_width=Main.calRange(xmax,xmin,int(2272))
        y_height=Main.calRange(ymax,ymin,int(1704))
        x_cord=Main.calCordinate(xmax,xmin,int(2272))
        y_cord=Main.calCordinate(ymax,ymin,int(1704))

        data_label=[]
        for i in labels_list:
            for val in SortedLabelDict:
                if i==val[0]:
                    data_label.append(val[1])

        data_values=Main.combine_multiple_lists(data_label,x_cord,y_cord,x_width,y_height)
        data_list=Main.combine_lists(images,data_values)
        if not os.path.exists('labels'):
            os.mkdir('labels')

        data_array=defaultdict(list)
        for k,v in data_list:
            data_array[k].append(v)

        for k,v in tqdm(data_array.items()):
            file_path = os.path.join('labels', str(k).replace(".jpg",".txt"))
            fl=open(file_path, "w")
            fl.write((",".join(map(str,v))).replace(",","").replace("[","").replace("(","").replace("]","").replace(")","\n"))
            fl.close()

        classes_file = open("classes.txt","w") 
        for elem in SortedLabelDict:
            classes_file.write(elem[0]+'\n') 
        classes_file.close() 

if __name__ == "__main__":
    obj = Main()
    obj.convert_csv_to_text