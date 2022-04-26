from os import listdir
import pandas as pd
import re

def pick_file_from_directory():
    #Prints numbered list of files in local directory. User types number to return string of file name.
    for x in listdir():
        print("{} --- {}".format(listdir().index(x)+1,x))  
    file_index = input("Type number of desired file:  ")    
    return listdir()[int(file_index)-1]


def increment_file_name_output(output_label="Working_Py_Output",suffix=".xlsx"):
    #Creates numbered file name for script to produce. If name exists in local directory, will increment number and try again.
    #Requires the 'from os import listdir' library 
    version_count = 1
    while True:
        proposed_file_name = output_label+"_v"+str(version_count)+suffix
        if proposed_file_name in listdir():
            version_count += 1
        else:
            return proposed_file_name

def make_df_from_excel(excel_file,worksheet=0):
    #Imports Excel file by name into a Pandas DataFrame. Optional arguement: worksheet name; defaults to first worksheet.    
    return pd.read_excel(excel_file,sheet_name = worksheet)

def make_excel_from_df(df,title='df_test.xlsx',index=False):
    df.to_excel(title)

def df_replace_NaN_w_string(df,string=""):
    #Replaces all NaNs in a given DataFrame with a string. Optional arguement: string content; defaults to empty "".
    return df.fillna(string)


def pick_columns_for_new_df(df):
    #Prints all column names from inputed dataframe. User types column numbers seperated by commas that they wish included in the updated version. Returns dataframe.
    headings = list(df.columns.values)

    for x in headings:
        print("{} --- {}".format(headings.index(x)+1,x))

    select_index = input("Type desired column numbers seperated by commas (eg, 1,3,5):  ")
    selections = [headings[int(x)-1] for x in select_index.split(",")]
    return df[selections]


def turn_df_column_into_list(df,col_name=""):
    #Returns list of values from a df column. If arguement col_name is empty,  user can pick desired column from a list.
    headings = list(df.columns.values)
    if col_name == "":
        for x in headings:
            print("{} --- {}".format(headings.index(x)+1,x))
        col_num = input("Type desired column:  ") 
        col_name = headings[int(col_num)-1]
    return df[col_name].to_list()


def turn_list_into_new_df_column(df,target_list,column_name="new_column"):
    #Add column to dataframe and returns expanded dataframe. List must be same length as df. Column name added in arguement.
    df[column_name] = target_list    
    return df

def string_modification(txt,space_strip=True,lowercase=True,regex_prep=False):
    if space_strip == True:
        txt = re.sub('\\s+', ' ', txt)    
    if lowercase == True:
        txt = txt.lower()
    if regex_prep == True:
        txt = txt.replace("(", "\(")
        txt = txt.replace(")", "\)")
        txt = txt.replace("=", "\=")        
    return txt


def remove_excess_spaces_from_string(str):
    return ' '.join(str.split())

def find_substrings_in_list_of_texts(substring_list,text_list):
    #Tries to find string index of each of a list of search terms (substring_list) inside each of a list of large texts (text_list). Returns dataframe.
    parse_dict = {i:"" for i in range(0,len(text_list))}

    for idx, observ in enumerate(text_list):
        observ_list = [observ.find(x) for x in substring_list]
        parse_dict[idx] = {substring_list[i]: observ_list[i] for i in range(len(substring_list))}

    return pd.DataFrame(parse_dict).T


def make_df_and_txtlist_from_excel_extended():
    for x in listdir():
        print("{} --- {}".format(listdir().index(x)+1,x))  
    file_index = input("Type number of desired file:  ")    
    df = pd.read_excel(listdir()[int(file_index)-1],sheet_name = 0)
    headings = list(df.columns.values)
    for x in headings:
        print("{} --- {}".format(headings.index(x)+1,x))
    col_num = input("Type column to be parsed:  ") 
    col_name = headings[int(col_num)-1]
    text_list = [' '.join(x.split()) for x in df[col_name].to_list()]
    return df, text_list

def return_text_between_strings(txt,startstr,endstr):
    start = txt.find(startstr)+len(startstr)
    end = txt.find(endstr)    
    return txt[start:end]    

def reg_match(text,regex):
    match = re.search(regex, text)
    if match == None:
        return ["","","",""]
    else:
        return [match.group(x) for x in range(1,5)]

def escape_char_formatting(term):
    charlist = ["\\","(",")","[","]","{","}","+","^","$","?","|",".","/"]
    for char in charlist:
        term = term.replace(char,"\\"+char)
    return term

def sort_df(df,col_list):
    # df.sort_values(by=['col1', 'col2'])
    return df.sort_values(by=[col_list])


def build_df_from_parse(txtlist,col):
    mastertxtlist = []
    for txt in txtlist:
        resultlist = reg_match(txt,regex_dict[col])
        mastertxtlist.append(resultlist)

    r0 = [row[0] for row in mastertxtlist]
    r1 = [row[1] for row in mastertxtlist]
    r2 = [row[2] for row in mastertxtlist]
    r3 = [row[3] for row in mastertxtlist]
    txtdict = {
        col+"_Value": r0
        ,col+"_Flag": r1
        ,col+"_UoM": r2
        ,col+"_Range": r3
        }   
    return pd.DataFrame.from_dict(txtdict)

def df_concat(main_df,new_df):
    df = pd.concat([main_df,new_df])
    return df
