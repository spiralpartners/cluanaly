import sys
import glob
import pandas as pd
pd.set_option("display.max_columns",100) #Number of columns in pandas output
pd.set_option("display.max_colwidth", 200)
pd.set_option("display.max_rows", 100)

def exchange_step_no(df):
    df["step"] = df["step"].str.replace('step5-2','28')
    df["step"] = df["step"].str.replace('step5-1','27')
    df["step"] = df["step"].str.replace('step4-5','26')
    df["step"] = df["step"].str.replace('step4-4-2','25')
    df["step"] = df["step"].str.replace('step4-4','24')
    df["step"] = df["step"].str.replace('step4-3','23')
    df["step"] = df["step"].str.replace('step4-2','22')
    df["step"] = df["step"].str.replace('step4-1-2','22')
    df["step"] = df["step"].str.replace('step4-1','21')
    df["step"] = df["step"].str.replace('step3-1','20')
    df["step"] = df["step"].str.replace('step3-0-2','19')
    df["step"] = df["step"].str.replace('step3-0-1','18')
    df["step"] = df["step"].str.replace('step2-6','17')
    df["step"] = df["step"].str.replace('step2-5','16')
    df["step"] = df["step"].str.replace('step2-4','15')
    df["step"] = df["step"].str.replace('step2-3','14')
    df["step"] = df["step"].str.replace('step2-2','13')
    df["step"] = df["step"].str.replace('step2-1','12')
    df["step"] = df["step"].str.replace('step1-10','11')
    df["step"] = df["step"].str.replace('step1-9','10')
    df["step"] = df["step"].str.replace('step1-8','9')
    df["step"] = df["step"].str.replace('step1-7','8')
    df["step"] = df["step"].str.replace('step1-6','7')
    df["step"] = df["step"].str.replace('step1-5','6')
    df["step"] = df["step"].str.replace('step1-4','5')
    df["step"] = df["step"].str.replace('step1-3','4')
    df["step"] = df["step"].str.replace('step1-2','3')
    df["step"] = df["step"].str.replace('step1-1','2')
    df["step"] = df["step"].str.replace('step0-1','1')
    df["step"] = df["step"].str.replace('step0','0')
    df["step"] = df["step"].str.replace('exception','-1')
    #print(df["step"])
    df["step"] = df["step"].astype(int)
    return df

def add_all_data(files, data):
    for tsvfile in files:
        #print(tsvfile) # newest tsv file for each team
        df  = pd.read_csv(tsvfile, delimiter="\t", quotechar='\'',index_col=0)
        #df = df.apply(lambda d: d.replace('\n',' '))
        df["stdout"] = df["stdout"].str.replace('"',' ')
        df["stdout"] = df["stdout"].str.replace("'",' ')
        df["stdout"] = df["stdout"].str.replace('\n',' ')
        #df["stdout"] = df["stdout"].str.strip()
        df["stderr"] = df["stderr"].str.replace('"',' ')
        df["stderr"] = df["stderr"].str.replace("'",' ')
        df["stderr"] = df["stderr"].str.replace('\n',' ')
        #df["stderr"] = df["stderr"].str.strip()
        data = data.append(exchange_step_no(df), ignore_index = True, sort=False)
    return data
    
# extract unique combination of vmname and step (without exception of vmname)
def get_unique_vmname_step(data):
    
    unique_data_vs = data.groupby(['vmname','step']).size().to_frame(name="count").reset_index()
    unique_data_vs = unique_data_vs[unique_data_vs.vmname != "exception"]
    return unique_data_vs

def is_equal_stdout_err(series1,series2):
    if series1["stdout"] != series2["stdout"]:
        return False
    if series1["stderr"] != series2["stderr"]:
        return False
    return True

def is_correct_output(series):
    if series["step"]==0:
        if ("SpiralTemplate") in series["stdout"]:
            return True
    if series["step"]==1:
        if ("git-commit.sh") in series["stdout"]:
            return True
    if series["step"]==2:
        if ("JST") in series["stdout"]:
            return True
    if series["step"]==3:
        if ("openjdk") in series["stderr"]:
            return True
    if series["step"]==4:
        if ("is running") in series["stdout"]:
            return True
    if series["step"]==5:
        if ("Tomcat/8.5.29") in series["stdout"]:
            return True
    if series["step"]==6:
        if ("2:on") in series["stdout"]:
            return True
    if series["step"]==7:
        if ("Tomcat/8.5.29") in series["stdout"]:
            return True
    if series["step"]==8:
        if ("is running") in series["stdout"]:
            return True
    if series["step"]==9:
        if ("LISTEN") in series["stdout"]:
            return True
    if series["step"]==10:
        if ("LISTEN") in series["stdout"]:
            return True
    if series["step"]==11:
        if ("blank") in series["stdout"] and ("blank") in series["stderr"]:
            return True
    if series["step"]==11:
        if series["stdout"].find("#") < series["stdout"].find("bindIp"):
            return True
    if series["step"]==12:
        if (".war") in series["stdout"]:
            return True
    if series["step"]==14:
        if ("{ likes") in series["stdout"]:
            return True
    if series["step"]==16:
        if ("Tomcat Web Application Manager") in series["stdout"]:
            return True
    if series["step"]==18:
        if int(series["stdout"]) > 100:
            return True
    if series["step"]==19:
        if ("blank") in series["stdout"] and ("blank") in series["stderr"]:
            return True
    if series["step"]==20:
        if (".html") in series["stdout"]:
            return True
    if series["step"]==22:
        if ("/root/.keystore") in series["stdout"]:
            return True
    if series["step"]==23:
        if (" 443 ") in series["stdout"]:
            return True
    if series["step"]==24:
        if ("TOMCAT_USER=root") in series["stdout"]:
            return True
    if series["step"]==25:
        if ("Peer certificate cannot be authenticated") in series["stderr"]:
            return True
    return False
    
if __name__ == '__main__':
    
    data = pd.DataFrame(index=[],columns=["unixtime","team","host","vmname","command","stdout","stderr","step"])
    file_list = sorted(glob.glob("./*aws*.tsv"))
    data = add_all_data(file_list,data)
    unique_data_vs = get_unique_vmname_step(data)
    #print(unique_data_vs)
    
    trans_data_all = pd.DataFrame(index=[],columns=["unixtime","team","host","vmname","command","stdout","stderr","step","correct"])
    for index, row in unique_data_vs.iterrows():
        each_data_vs = data.query('step == '+str(row["step"])+' and vmname == "'+str(row["vmname"])+'"').sort_values('unixtime')
        each_data_vs = each_data_vs.fillna("blank") # convert NAN to string "blank"
        trans_data = pd.DataFrame(index=[],columns=["unixtime","team","host","vmname","command","stdout","stderr","step","correct"])
        for index, row in each_data_vs.iterrows():
            if is_correct_output(row) and len(trans_data.index)<=0:
                row['correct']=True
                trans_data = trans_data.append(row, ignore_index = True, sort=False)
                break
        trans_data_all = trans_data_all.append(trans_data, ignore_index = True, sort=False)
    trans_data_all.to_csv("all_correct_progress.tsv",sep='\t', encoding='utf-8',quotechar='\'')
