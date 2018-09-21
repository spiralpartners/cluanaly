import glob
import os
import shutil

#git/のimportantdataを作成する

#データの場所
sourcedir=r'C:\Users\akayama\Documents\ハッカソン\20180803_all_log_anonymous'
#出力フォルダ名
dir3='important_git'

if __name__ == "__main__":

    dirs=[r.split('\\')[-1] for r in glob.glob(sourcedir + '/*')]

    if os.path.isdir(dir3):
        shutil.rmtree(dir3)
    os.mkdir(dir3)
    for d in dirs:
        os.mkdir(dir3+'\\'+d)
        os.mkdir(dir3+'\\'+d+'\\git')
        os.mkdir(dir3 + '\\' + d + '\\git\\etc')
        os.mkdir(dir3 + '\\' + d + '\\git\\etc\\init.d')
        shutil.copy(sourcedir + '\\' + d + '\\git\\etc\\init.d\\tomcat8',dir3 + '\\' + d + '\\git\\etc\\init.d')

        os.mkdir(dir3 + '\\' + d + '\\git\\etc\\sysconfig')
        shutil.copy(sourcedir + '\\' + d + '\\git\\etc\\sysconfig\\clock',dir3 + '\\' + d + '\\git\\etc\\sysconfig')

        files = glob.glob(sourcedir + '\\' + d + '\\git\\etc\\*.conf')
        for f in files:
            shutil.copy(f,dir3 + '\\' + d + '\\git\\etc')

        shutil.copytree(sourcedir + '\\' + d + '\\git\\etc\\tomcat8',dir3 + '\\' + d + '\\git\\etc\\tomcat8')

        os.mkdir(dir3 + '\\' + d + '\\git\\var')
        os.mkdir(dir3 + '\\' + d + '\\git\\var\\lib')
        shutil.copytree(sourcedir + '\\' + d + '\\git\\var\\lib\\tomcat8', dir3 + '\\' + d + '\\git\\var\\lib\\tomcat8')


