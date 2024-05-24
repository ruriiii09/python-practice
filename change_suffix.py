import flet as ft
import pathlib
import shutil

def change_filetype(file_name,  from_suffix, to_suffix):
    #ファイルの拡張子を得る
    sf = pathlib.PurePath(file_name).suffix

    #変更対象かどうか判定する
    if sf == from_suffix:
        #ファイル名(拡張子なし)を得る
        st = pathlib.PurePath(file_name).stem

        #変更後のファイル名を得る
        to_name = st + to_suffix

        #ファイル名を変更する
        shutil.move(file_name,to_name)

if __name__ == '__main__':
    origin_file = input()

    change_filetype()
