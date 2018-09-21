import glob
import os
import shutil
import re
import filecmp


#差分フォルダを作る
#隠しフォルダとバイナリファイルは無視

#データの場所
sourcedir=r'C:\Users\akayama\Documents\PyCharmProjects\cmpfiles\importantgit'
#出力フォルダ
dir3='cmpdirs'

global dir1
global dir2
def compare_lines(path):
    f1 = open(dir1 + path,'r',encoding='UTF-8')
    f2 = open(dir2 + path,'r',encoding='UTF-8')

    try:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    except:
        return 0

    relines1 = [re.sub(r'[0-9]+', '', line.replace('\t', '').replace(' ', '')) for line in lines1]
    relines2 = [re.sub(r'[0-9]+', '', line.replace('\t', '').replace(' ', '')) for line in lines2]

    f1.close()
    f2.close()

    f = open('tmp', 'w',encoding='UTF-8')
    flag=0
    for n in range(len(lines1)):
        if relines1[n] not in relines2:
            flag=1
            f.write('- ' + lines1[n])
#        else:
#            f.write('\n')
    for n in range(len(lines2)):
        if relines2[n] not in relines1:
            flag=1
            f.write('+ ' + lines2[n])
#        else:
#            f.write('\n')
    f.close()

    if flag == 0:
        os.remove('tmp')
    else:
        tmp=os.path.dirname(path)
        if not os.path.isdir(dir3 + tmp):
            os.makedirs(dir3 + tmp)
        shutil.move('tmp', dir3 + path)


def compare_files(dir):

    files1=[r.split('\\')[-1] for r in glob.glob(dir1+dir+'/*')]
    files2=[r.split('\\')[-1] for r in glob.glob(dir2+dir+'/*')]

    for file in files2:
        if file in files1:
            if os.path.isdir(dir2 + '\\' + dir +'\\'+file):
                compare_files(dir+'\\'+file)
            else:
                if not filecmp.cmp(dir1 + dir + '\\' + file, dir2 + dir + '\\' + file):
                    compare_lines(dir+'\\'+file)
        else:
            tmp=os.path.dirname(dir + '\\' + file)
            if not os.path.isdir(dir3 + tmp):
                os.makedirs(dir3 + tmp)
            if os.path.isdir(dir2 + dir + '\\' + file):
                shutil.copytree(dir2 + dir + '\\' + file, dir3 + dir + '\\-' + file)
            else:
                shutil.copy(dir2 + dir + '\\' + file, dir3 + dir + '\\-' + file)

def compare_files2(dir):

    files1=[r.split('\\')[-1] for r in glob.glob(dir1+dir+'/*')]
    files2=[r.split('\\')[-1] for r in glob.glob(dir2+dir+'/*')]

    for file in files1:
        if file in files2:
            if os.path.isdir(dir2 + '\\' + dir +'\\'+file):
                compare_files2(dir+'\\'+file)
        else:
            tmp=os.path.dirname(dir + '\\' + file)
            if not os.path.isdir(dir3 + tmp):
                os.makedirs(dir3 + tmp)
            if os.path.isdir(dir1 + dir + '\\' + file):
                shutil.copytree(dir1 + dir + '\\' + file, dir3 + dir + '\\+' + file)
            else:
                shutil.copy(dir1 + dir + '\\' + file, dir3 + dir + '\\+' + file)


if __name__ == "__main__":

    if os.path.isdir(dir3):
        shutil.rmtree(dir3)
    os.mkdir(dir3)
    dir4=dir3

    dirs=[r.split('\\')[-1] for r in glob.glob(sourcedir + '/*')]
    num1=0
    for d1 in dirs:
        num1+=1
        num2=0
        if os.path.isdir(dir4+'\\'+d1):
            shutil.rmtree(dir4+'\\'+d1)
        os.mkdir(dir4+'\\'+d1)
        dir1=sourcedir+'\\'+d1
        for d2 in dirs:
            num2+=1
            if num1 >= num2:
                continue
            if os.path.isdir(dir4 + '\\' + d1 +'\\'+d2):
                shutil.rmtree(dir4 + '\\' + d1 +'\\'+d2)
            os.mkdir(dir4 + '\\' + d1 +'\\'+d2)
            dir2=sourcedir+'\\'+d2
            dir3=dir4 + '\\' + d1 +'\\'+d2
            compare_files('')
            compare_files2('')
