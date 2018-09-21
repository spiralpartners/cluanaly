import glob
import os
import shutil

#log/のimportantdataと.bash_historyを作成する
#log/script/????????ec2-user.logのファイルをまとめる

#データの場所
sourcedir=r'C:\Users\akayama\Documents\ハッカソン\20180803_all_log_anonymous'
#出力フォルダ名
dir3='important_log'

if __name__ == "__main__":

    dirs=[r.split('\\')[-1] for r in glob.glob(sourcedir + '/*')]

    if os.path.isdir(dir3):
        shutil.rmtree(dir3)
    os.mkdir(dir3)
    for d in dirs:
        os.mkdir(dir3+'\\'+d)

        files = glob.glob(sourcedir + '\\' + d + '\\*.bash_history')
        for f in files:
            shutil.copy(f,dir3 + '\\' + d + '\\team.bash_history')

        os.mkdir(dir3+'\\'+d+'\\log')
        shutil.copy(sourcedir + '\\' + d + '\\log\\lsyncd.log', dir3 + '\\' + d + '\\log')
        os.mkdir(dir3 + '\\' + d + '\\log\\mongodb')
        shutil.copy(sourcedir + '\\' + d + '\\log\\mongodb\\mongod.log', dir3 + '\\' + d + '\\log\\mongodb')
        shutil.copy(sourcedir + '\\' + d + '\\log\\yum.log', dir3 + '\\' + d + '\\log')

        os.mkdir(dir3 + '\\' + d + '\\log\\script')
        files = glob.glob(sourcedir + '\\' + d + '\\log\\script\\*')
        fw=open(dir3+'\\' + d + '\\log\\script\\ec2-user.log','w',encoding='UTF-8')
        for f in files:
            fr = open(f, 'r', encoding='UTF-8')
            fw.write(fr.read())
            fr.close()
        fw.close()

        shutil.copytree(sourcedir + '\\' + d + '\\log\\tomcat8', dir3 + '\\' + d + '\\log\\tomcat8')
