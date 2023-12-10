import os
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class ReadFiles(object):

    def __init__(self) -> None:
        self.filepath = 'E:/Git/DataEngineering/JSON_XML_Comparator/files'
        
    def read_file(self):
        try:
            for root_dir, dirs, files in os.walk(self.filepath):
                for file in files:
                    file_path = root_dir + os.sep + file

                    if 'xml' in file:
                               
                        columns = ['Id','IndexName','Date','Open','High','Low','Close','AdjClose','Volume','CloseUSD']
                        tree = ET.parse(file_path)
                        root = tree.getroot()
                        values = []

                        for ind in root:
                            result = []
                            
                            for i in columns:
                                if ind is not None and ind.find(i) is not None:
                                    val = self.find_datatype(i,ind.find(i).text)
                                    result.append(val)
                                else:
                                    result.append(None)
                            values.append(result)

                        self.XML_df = pd.DataFrame(values, columns=columns)     

                    else:
                        self.JSON_df = pd.read_json(file_path)  

           
                
        except Exception as e:
            print(str(e))

    def find_datatype(self,col,val):
        if col in ['Id','Volume']:
            return int(val)
        elif col in ['Open','High','Low','Close','AdjClose','CloseUSD']:
            return float(val)
        elif col in ["IndexName",'Date']:
            return str(val)


    def compare(self,):

        try:
            pd.options.display.max_colwidth = None
            
            columns = ['IndexName','Open','High','Low','Close','AdjClose','Volume','CloseUSD']

            id = self.XML_df['Id']
            mismatch_df = pd.DataFrame(
                    columns=['Id', 'Mismatch_Field', 'XML','JSON'])
            
            match_df = pd.DataFrame(
                    columns=['Id', 'Matching_Field', 'XML','JSON'])
            


            for i in id:
                print(i)
            
                temp_xml = self.XML_df.query('Id==@i')
                temp_xml = temp_xml.reset_index(drop=True)

                temp_json = self.JSON_df.query('Id==@i')
                temp_json = temp_json.reset_index(drop=True)

                for val in columns:

                    flag = ''
        
                    flag = np.where((temp_xml[val].equals(temp_json[val])), 'True','False')
                    
                    if flag == 'True':
                        match_df = match_df.append( {'Id': i, 'Matching_Field': val,'XML': temp_xml[val].to_string(index=False),'JSON':temp_json[val].to_string(index=False)},ignore_index=True) 
                        
                    elif flag == 'False':
                        mismatch_df = mismatch_df.append( {'Id': i, 'Mismatch_Field': val,'XML': temp_xml[val].to_string(index=False),'JSON':temp_json[val].to_string(index=False)},ignore_index=True)


        except Exception as e:
            print(e)
        
        return mismatch_df,match_df     
    
if __name__ == '__main__':

    try:
        read = ReadFiles()
        read.read_file()

        mismatch_df,match_df = read.compare()

        mismatch_df.to_csv('mismatch.csv',index=False)
        match_df.to_csv('match.csv',index=False)

        
    except Exception as e:
        print(str(e))
        

        
