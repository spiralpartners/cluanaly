import os

#dir内の空フォルダを削除する
dir=r'C:\Users\akayama\Documents\ハッカソン\data\data5\cmpdirs_git'

def remove_space(path='.'):
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                try:
                    os.removedirs(entry.path)
                except:
                    remove_space(entry.path)

if __name__ == "__main__":

    remove_space(dir)