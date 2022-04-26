# -*- coding: utf-8 -*-

'''
NOTES:
    
- Most features are added to the dataframe using a dict called parse_dict. Its keys are the search terms. Its values are empty dictionaries. 
As features are chosen, these empty dictionaries get keys based on new columns, and the values are lists containing the results for every row.
This design makes it easy to keep all columns ordered by search terms when parse_dict is finally added to the dataframe. 
It also makes it easy to iterately name columns based on search terms
Example: parse_dict[searchterm_dict][searchterm_resultcolumn] = list_of_results

- content_dict contains all the potential added features; initially set to False. Once a feature is added, it changes to True. 
True features are invisible on the menu and their functions are disabled (preventing repeat use).

- New columns are added to file in the order they are chosen

'''

import pandas as pd
import sys
from os import listdir
import re
from collections import Counter



def text(section,text_list="",dup_dict=""):
    # Stores long sections of user instrucitons that may distract from the code
    if section == "intro":
        print("\n\n"+"-"*36+"\n----- GENERAL PARSE PROGRAM -------\n"+"-"*36)
        print("\n- This file (general_parse.py) must be saved in the directory of the Excel file you wish to parse")
        print("\n- The Excel file needs a worksheet with a text column and a worksheet with a column of search terms")
        print("\n- The Excel worksheet with the text column intending for parsing should be labeled 'text'")
        print("\n- The Excel worksheet with the search terms should be labeled 'terms'")
        print("\n- The terms worksheet should list the search terms in column A with the header 'terms' in cell A1")
        print("\n- You can end a Python program at any time by pressing Ctrl + C")
        input("-"*36+"\nPress Enter to continue.")
    if section == "details":
        print("\n"+"-"*36+"\n\n\n---- INITIAL DETAILS --------")
        print("\nYour table has {} rows of text".format(len(text_list)))
        print("\nYour texts average {} characters in length".format(round(0 if len([len(ele) for ele in text_list]) == 0 else (float(sum([len(ele) for ele in text_list])) / len([len(ele) for ele in text_list])))))
        print("\nYour texts include {} kind(s) of duplicates with {} duplicate rows overall".format(len(dup_dict),sum(dup_dict.values())))
        input("-"*36+"\nPress Enter to continue.")        
    if section == "menu":
        print("     SEARCH_RESULTS finds a number (or trace) after the search term.")
        print("     VAL-FLAG-RANGE tries to parse four columns: value, high flag, units of measure, and range")
        print("     TEXT_SAMPLES shows a text sample of predetermined size after the search term.")
        print("     SEARCH_COUNTS finds how often search term appears in a text.")
        print("     DUPLICATES finds whether rows of text have duplicates.")
        print("Note: all new columns except DUPLICATES will appear in the new spreadsheet in the order added.")
        print("\n"+"-"*36)
        


def main():
    # Variables:
    content_dict = {"SEARCH_RESULTS":False,"VAL-FLAG-RANGE":False,"TEXT_SAMPLES":False,"SEARCH_COUNTS":False,"DUPLICATES":False}
    
    #INTRO SLIDE
    text("intro")
    
    #STEP 1: CHOOSE FILE
    print("\n"+"-"*36+"\n\n\n-------- STEP 1: CHOOSE FILE --------")
    for x in listdir():
        print("{} --- {}".format(listdir().index(x)+1,x))
    print("-"*36+"\nNote: see above for numbered contents of working directory. Files starting with '~$' are temp (open and unsaved).")       
    file_index = input("Step 1 - Type number of Excel file to parse:  ")
    filename = listdir()[int(file_index)-1]     
    df = pd.read_excel(filename,sheet_name = 'text')
    terms_df = pd.read_excel(listdir()[int(file_index)-1],sheet_name = 'terms')
    
    #STEP 2: CHOOSE PARSING COLUMN
    headings = list(df.columns.values)
    print("\n"+"-"*36+"\n\n\n---- STEP 2: CHOOSE PARSING COLUMN --------")
    for x in headings:
        print("{} --- {}".format(headings.index(x)+1,x))
    print("-"*36+"\nNote: see above for numbered column list of text worksheet.")  
    col_num = input("Step 2 - Type number of column to be parsed:  ") 
    col_name = headings[int(col_num)-1]
    
    #Produce data structures
    text_list = format_list_of_strings([' '.join(x.split()) for x in df[col_name].to_list()])
    search_terms = format_list_of_strings(terms_df['terms'].to_list())
    parse_dict = {i:{} for i in search_terms}
    textdict = dict(Counter(text_list))
    dup_dict = dict((k, v) for k, v in textdict.items() if v > 1)
    
    #Initial details (helps QA)
    text("details",text_list,dup_dict)
    
    # MENU
    ## Lets the user choose what features to add to the new spreadsheet.
    ## Chosen features disappear from list and cannot be picked again (thanks to content_dict)
    ## C to finish is not case-sensitive
    while True:
        contentlist = [x for x in content_dict if content_dict[x] == True]
        if len(contentlist) == 0: contentlist = ["NOTHING"]
        print("-"*36+"\n\n\n---- STEP 3: CONTENT MENU --------")
        print("The new spreadsheet currently features: {}\n".format(", ".join(contentlist)))
        text("menu")
        for number, value in enumerate(content_dict):
            if content_dict[value] == False: print("{} --- {}".format(number+1,value))
        print("C --- Finish and create spreadsheet")        
        print("-"*36)
        feature_choice = input("Step 3 - Type number to include feature or C to finish:  ")
    
        if feature_choice == "1":
            content_dict, text_list, parse_dict = searchresults(content_dict, text_list, parse_dict)
        if feature_choice == "2":
            content_dict, text_list, parse_dict = valflagrange(content_dict, text_list, parse_dict)
        if feature_choice == "3":
            content_dict, text_list, parse_dict = textsamples(content_dict, text_list, parse_dict)
        if feature_choice == "4":
            content_dict, text_list, parse_dict = searchcounts(content_dict, text_list, parse_dict)
        if feature_choice == "5":
            content_dict,df = duplicates(content_dict,dup_dict, df, col_name, text_list)
        if feature_choice == "C" or feature_choice == "c":
            finish(df, parse_dict,filename)
        else:
            pass 

def escape_char_formatting(term):
    #Used to sanitize regex text
    charlist = ["\\","(",")","[","]","{","}","+","^","$","?","|",".","/"]
    for char in charlist:
        term = term.replace(char,"\\"+char)
    return term

def valflagrange(content_dict, text_list, parse_dict):
    # Returns columns for value, high flag, unit of measure, and range. 
    # Only recognized unit of measure is pg/ml
    if content_dict['VAL-FLAG-RANGE'] == False:    
        print("-"*36+"\n\n\n---- SEARCH RESULTS --------")
        print("Note: This will add columns in the new spreadsheet for each search term and return any number (incl. decimals and < or > symbols) within one colon and space of the search term. Also returns 'trace'.")
        
        for term in parse_dict:
            regex = escape_char_formatting(term)
            regex += "[:]*[ ]?([><0-9.=]+|trace) ([h ]*)(pg\/ml) ([><=0-9.-]+) "
            valuelist = []
            flaglist = []
            uomlist = []
            rangelist = []
            for text in text_list:
                match = re.search(regex, text)
                #print("\n\n\n",regex,"\n",match,"\n"+text)
                if match != None:
                    ## Captures matches for values, uom, and range
                    valuelist.append(match.group(1))
                    uomlist.append(match.group(3))
                    rangelist.append(match.group(4))
                
                    ## Captures regular flag 'h'; also captures weirdly-formatted flags by comparing RANGE AND VALUE instead of finding text
                    if match.group(2) == "h":
                        rangecode = "h"
                    else:
                        rangecode = ""
                        range_regex = "([<0-9.]*)[><=-]+([<0-9.]+)"
                        rangematch = re.search(range_regex, match.group(4))
                        if rangematch != None:
                            rangemax = rangematch.group(2).replace("<", "")
                            rangemax = rangemax.replace("=", "")
                            valuestring = match.group(1).replace("<", "")
                            if float(valuestring) > float(rangemax):
                                rangecode = "h"                            
                    flaglist.append(rangecode)
                    
                else:
                    valuelist.append("")
                    flaglist.append("")
                    uomlist.append("")
                    rangelist.append("")
            parse_dict[term][term+"_value"] = valuelist
            parse_dict[term][term+"_flag"] = flaglist
            parse_dict[term][term+"_uom"] = uomlist
            parse_dict[term][term+"_range"] = rangelist

        content_dict['VAL-FLAG-RANGE'] = True
        print("\n VAL-FLAG-RANGE ADDED")
        input("-"*36+"\nPress Enter to continue.")
    return content_dict, text_list, parse_dict


def searchresults(content_dict, text_list, parse_dict):
    # Basic function to search for number following search term (also finds "trace").
    if content_dict['SEARCH_RESULTS'] == False:    
        print("-"*36+"\n\n\n---- SEARCH RESULTS --------")
        print("Note: This will add columns in the new spreadsheet for each search term and return any number (incl. decimals and < or > symbols) within one colon and space of the search term. Also returns 'trace'.")
        
        for term in parse_dict:
            regex = escape_char_formatting(term)
            regex += "[:]*[ ]?([><0-9.]+|trace)"

            resultlist = []
            for text in text_list:
                match = re.search(regex, text)
                if match != None:
                    resultlist.append(match.group(1))
                else:
                    resultlist.append("")
            parse_dict[term][term+"_results"] = resultlist

    
        content_dict['SEARCH_RESULTS'] = True
        print("\n SEARCH RESULTS ADDED")
        input("-"*36+"\nPress Enter to continue.")
    return content_dict, text_list, parse_dict
    

def textsamples(content_dict, text_list, parse_dict):
    #Finds chunk of text of specified size after first instance of search term. May be useful for QA.
    if content_dict['TEXT_SAMPLES'] == False:    
        print("-"*36+"\n\n\n---- TEXT SAMPLES --------")
        print("Note: This will add columns in the new spreadsheet for each search term returning a user-decided number of characters after the first instance (if any) of the search term in the text. All surplus spaces have already been removed from the texts. Warning: non-alphanumeric symbols in the search terms may cause errors.")
        while True:
            charcount = input("-"*36+"\nType number of characters (1 to 1000):  ") 
            
            try: 
                if int(charcount) > 0 and int(charcount) <= 1000:
                    break
            except:
                print("You must type a number between 1 and 1000 inclusive.")

        for term in parse_dict:
            textsamplelist = []
            for text in text_list:
                if text.find(term) != -1:
                    textsamplelist.append(text[text.find(term)+len(term):text.find(term)+len(term)+int(charcount)])
                else:
                    textsamplelist.append("")

            parse_dict[term][term+"_textsample"] = textsamplelist
        content_dict['TEXT_SAMPLES'] = True
        print("\n TEXT SAMPLES ADDED")
        input("-"*36+"\nPress Enter to continue.")
    return content_dict, text_list, parse_dict
    

def searchcounts(content_dict,text_list,parse_dict):
    #Finds number of times a search term appears in a row
    if content_dict['SEARCH_COUNTS'] == False:    
        print("-"*36+"\n\n\n---- SEARCH COUNTS --------")
        print("Note: This will add columns in the new spreadsheet for each search term counting how many instances of the search term appear in a row of text. This can be useful for QA, as the parse matching in other columns might be matching the wrong instance.")     
        for term in parse_dict:
            countlist = [text.count(term) for text in text_list]
            parse_dict[term][term+"_count"] = countlist
        content_dict['SEARCH_COUNTS'] = True
        print("\n SEARCH COUNTS ADDED")
        input("-"*36+"\nPress Enter to continue.")
    return content_dict, text_list, parse_dict

def duplicates(content_dict,dup_dict,df, col_name, text_list):
    #Finds whether a text record has duplicate records in the file.
    if content_dict['DUPLICATES'] == False:
        print("-"*36+"\n\n\n---- DUPLICATES --------")
        print("Note: This will create a column in the new spreadsheet to the right of {} called Duplicate_Flag. Rows will be marked Duplicate or Unique.".format(col_name))
        dupmatchlist = []
        for text in text_list:
            if text in dup_dict:
                dupmatchlist.append("Duplicate")
            else:
                dupmatchlist.append("Unique")
        df.insert(df.columns.get_loc(col_name)+1,'Duplicate_Flag', dupmatchlist)
        content_dict['DUPLICATES'] = True
        print("\n DUPLICATES ADDED")
        input("-"*36+"\nPress Enter to continue.")
    return content_dict, df

def finish(df, parse_dict,filename):
    #Combines the parse_dict with the df, invents a new file name with an iteratated version number, and creates the file.         
    for term in parse_dict:
        for col in parse_dict[term]:
            df.insert(len(df.columns),col, parse_dict[term][col])
    version_count = 1
    filename = filename.replace(".xlsx", "")
    while True:
        proposed_filename = filename+"_parse-results_v"+str(version_count)+".xlsx"
        if proposed_filename in listdir():
            version_count += 1
        else:
            break
    df.to_excel(proposed_filename,index=False)
    print("-"*36+"\n"+"-"*36+"\n"+"-"*36+"\n{} has been created.\n\nEXITING PROGRAM".format(proposed_filename))
    sys.exit()

def format_list_of_strings(strlist):
    strlist = [text.lower() for text in strlist]
    strlist = [' '.join(text.split()) for text in strlist]
    return strlist


##MAIN CODE
main()
