import sys
import glob
import pandas as pd
pd.set_option("display.max_columns",100) #Number of columns in pandas output
pd.set_option("display.max_colwidth", 200)
pd.set_option("display.max_rows", 100)

def create_all_elapsed_list(vmname,df,step_no,correct_num):
    all_elapsed = [vmname]
    team = df.query('vmname == "'+vmname+'"')["team"].values[0]
    host = df.query('vmname == "'+vmname+'"')["host"].values[0]
    all_elapsed.append(team)
    all_elapsed.append(host)
    all_elapsed.append(correct_num)
    for step in step_no:
        try:
            step_elapsed = df.query('step == '+ str(step) +' and vmname == "'+vmname+'"')["elapsed"].values[0]
        except IndexError:
            print(vmname+":could not clear step_no " + str(step))
            step_elapsed = None
        all_elapsed.append(step_elapsed)
    return all_elapsed

if __name__ == '__main__':
    
    data = pd.DataFrame(index=[],columns=["unixtime","team","host","vmname","command","stdout","stderr","step","correct"])
    df  = pd.read_csv("./all_correct_progress.tsv", delimiter="\t", quotechar='\'',index_col=0)
    #print(df)
    unique_vmname = df.groupby('vmname').size().to_frame(name="correct_num").reset_index().sort_values('correct_num')
    print(unique_vmname)
    
    #Calculate elapsed time for each step
    trans_data_all = pd.DataFrame(index=[],columns=["unixtime","team","host","vmname","command","stdout","stderr","step","correct","elapsed"])
    for index, row in unique_vmname.iterrows():
        each_user_df = df.query('vmname == "' + row["vmname"] + '"').sort_values(['unixtime','step'])
        trans_data = pd.DataFrame(index=[],columns=["unixtime","team","host","vmname","command","stdout","stderr","step","correct","elapsed"])
        for index2,row2 in each_user_df.iterrows():
            if len(trans_data.index)<=0:
                row2["elapsed"]=0
                trans_data = trans_data.append(row2, ignore_index = True, sort=False)
                continue
            row2['elapsed']=row2['unixtime'] - trans_data.iloc[-1]['unixtime']
            trans_data = trans_data.append(row2, ignore_index = True, sort=False)
        trans_data_all = trans_data_all.append(trans_data, ignore_index = True, sort=False)
    #print(trans_data_all)
    all_elapsed_df = trans_data_all[["team","host","vmname","step","elapsed"]]
    print(all_elapsed_df)
    
    #Create all user's elapsed time dataframe
    each_user_elapsed = pd.DataFrame(index=[],columns=["vmname","team","host","correct_num","step0","step0-1","step1-1","step1-2","step1-3","step1-4","step1-5","step1-6","step1-7","step1-8","step1-9","step1-10","step2-1","step2-3","step2-5","step3-0-1","step3-0-2","step3-1","step4-2","step4-3","step4-4","step4-4-2"])
    for index, row in unique_vmname.iterrows():
        step_no = [0,1,2,3,4,5,6,7,8,9,10,11,12,14,16,18,19,20,22,23,24,25]
        correct_num = row["correct_num"]
        series = pd.Series(create_all_elapsed_list(row["vmname"],all_elapsed_df,step_no,correct_num),index=each_user_elapsed.columns)
        each_user_elapsed = each_user_elapsed.append(series, ignore_index = True, sort=False)
        
    print(each_user_elapsed.sort_values(["vmname"]).reset_index(drop = True))
    each_user_elapsed.sort_values(["vmname"]).reset_index(drop = True).to_csv("student_performance.tsv",sep='\t', encoding='utf-8',quotechar='\'')