import os

#dir内のバイナリファイル（.war,.class,.jar）を削除する
dir=r'C:\Users\akayama\Documents\ハッカソン\data\data5\cmpdirs_git'

def remove_bin(path='.'):
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                for tmp in  ['.war','.class','.jar']:
                    if tmp in entry.path:
                        os.remove(entry.path)
            elif entry.is_dir():
                remove_bin(entry.path)

if __name__ == "__main__":

    remove_bin(dir)
