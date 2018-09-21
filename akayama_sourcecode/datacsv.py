import glob
import os

#dir3内のデータから距離行列（差分フォルダのサイズ）csvファイルを作る

#元データの場所
sourcedir=r'C:\Users\akayama\Documents\ハッカソン\20180803_all_log_anonymous'
#参照するフォルダ
dir3=r'C:\Users\akayama\Documents\ハッカソン\data\data4\cmpdirs_git'

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def get_dir_num(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += 1
            elif entry.is_dir():
                total += get_dir_num(entry.path)
    return total

if __name__ == "__main__":

    dirs=[r.split('\\')[-1] for r in glob.glob(sourcedir + '/*')]

    num1=0
    list=[]
    for d1 in dirs:
        num1+=1
        num2=0
        tmp=[]
        for d2 in dirs:
            num2+=1
            if num1>=num2:
                size=0
                num=0
            else:
                dir=dir3+'\\'+d1+'\\'+d2
                size=get_dir_size(dir)
                num=get_dir_num(dir)
            tmp.append([size/1000,num])
        list.append(tmp)



    f=open('data.csv','w')
    for d1 in dirs:
        tmp=d1.split('-')
        f.write(','+tmp[0][4:]+'-'+tmp[1])
    for n1 in range(len(dirs)):
        tmp=dirs[n1].split('-')
        f.write('\n'+tmp[0][4:]+'-'+tmp[1])
        for n2 in range(len(dirs)):
            if n1<=n2:
                num1=n1
                num2=n2
            else:
                num1=n2
                num2=n1
#            f.write(',{0:.1f}({1:d})'.format(list[num1][num2][0],list[num1][num2][1]))
            f.write(',{0:.1f}'.format(list[num1][num2][0],list[num1][num2][1]))
#            f.write(',{1:d}'.format(list[num1][num2][0],list[num1][num2][1]))
    f.close()