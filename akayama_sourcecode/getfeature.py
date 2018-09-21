import glob
import os

#dir3内のデータから各差分ファイルのサイズをcsvファイルにまとめる

#元データの場所
sourcedir=r'C:\Users\akayama\Documents\ハッカソン\20180803_all_log_anonymous'
#参照するフォルダ
dir3=r'C:\Users\akayama\Documents\ハッカソン\data\data4\cmpdirs_git'

def get_dir_size(path='.'):
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def get_each_size(path='.'):
    fname=[]
    fsize=[]
    with os.scandir(path) as it:
        for entry in it:
            file=entry.path.split('\\')[-1]
            if file[0]=='+' or file[0]=='-':
                fname.append(path+'\\'+file[1:])
                fsize.append(get_dir_size(entry.path))
            else:
                if entry.is_file():
                    fname.append(path+'\\'+file)
                    fsize.append(entry.stat().st_size)
                elif entry.is_dir():
                    list = get_each_size(entry.path)
                    fname.extend(list[0])
                    fsize.extend(list[1])
    return [fname,fsize]

if __name__ == "__main__":

    dirs=[r.split('\\')[-1] for r in glob.glob(sourcedir + '/*')]

    num1=0
    for d1 in dirs:
        num1+=1
        num2=0
        fname=[]
        fsize=[]
        for d2 in dirs:
            num2+=1
            if num1 == num2:
                continue
            if num1 < num2:
                dir=dir3+'\\'+d1+'\\'+d2
            else:
                dir = dir3 + '\\' + d2 + '\\' + d1
            list=get_each_size(dir)
            fname.append([x.split(dir+'\\')[1] for x in list[0]])
            fsize.append(list[1])

        allfname=[]
        for l in fname:
            for n in l:
                if n not in allfname:
                    allfname.append(n)
        allfname.sort()

        f = open(d1 + '.csv', 'w')
        for n in allfname:
            f.write(','+n)
        for i in range(len(fname)):
            if i+1 < num1:
                f.write('\n'+dirs[i])
            else:
                f.write('\n'+dirs[i+1])
            for n in allfname:
                if n in fname[i]:
                    f.write(','+str(fsize[i][fname[i].index(n)]))
                else:
                    f.write(',0')
        f.close()

