import flet as ft
from flet import(FilePicker,FilePickerResultEvent,Page)
import pathlib
from pathlib import (Path,PurePath)
import shutil
from pdf2image import convert_from_path

def change_filetype(target_file, output_folder,  from_suffix, to_suffix):
    #ファイルの拡張子を得る
    sf = PurePath(target_file).suffix

    #変更対象かどうか判定する
    if sf == from_suffix:
        #ファイル名(拡張子なし)を得る
        #st = PurePath(target_file).stem

        #変更後のファイル名を得る
        #to_name = output_folder + "/" + st +"."+ to_suffix

        convert_from_path(target_file, output_folder=output_folder, fmt=to_suffix, output_file=PurePath(target_file).stem ,poppler_path='/usr/local/Cellar/poppler/24.04.0/bin')

        #ファイル名を変更する
        #shutil.copyfile(target_file,to_name)



def main(page: ft.Page):
    page.title = "拡張子変換"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = "light"

    #各変数名と種別を先に定義、Refで内容をリンクさせる
    target_file = ft.Ref[ft.Text]()
    output_folder = ft.Ref[ft.Text]()
    result_message = ft.Ref[ft.Text]()
    from_suffix = ft.Ref[ft.Text]()
    to_suffix = ft.Ref[ft.TextField]()

    #許可する拡張子一覧
    file_extensions = ["jpeg", "jpg", "png","pdf","mp3","mp4"]
    ui_rows = []

    ###################################
    # file picker　-　ファイル選択ボタン
    ###################################
    def pick_files_result(e: FilePickerResultEvent):
        if e.files:
            target_file.current.value = e.files[0].path
            from_suffix.current.value = str(PurePath(target_file.current.value).suffix)
            #output_folder.current.value = str(PurePath(target_file.current.value).parent)
            page.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)

    def show_pick_file(_: ft.ControlEvent):
        pick_files_dialog.pick_files(
            allow_multiple=False,
            file_type="custom",
            allowed_extensions=file_extensions
        )

    ui_rows.append(ft.Row(controls=[
        ft.ElevatedButton("Select File", on_click=show_pick_file),
        ft.Text(ref=target_file)
    ],
    
    ))

    ###################################
    # folder picker　-　出力ディレクトリ選択
    ###################################
    def on_folder_picked(e: FilePickerResultEvent):
        if e.path:
            output_folder.current.value = e.path
            page.update()

    folder_pick_dialog = FilePicker(on_result=on_folder_picked)

    def show_pick_folder(_: ft.ControlEvent):
        folder_pick_dialog.get_directory_path()

    ui_rows.append(ft.Row(controls=[
        ft.ElevatedButton("Select Output Folder", on_click=show_pick_folder),
        ft.Text(ref=output_folder)]
        ))
    
    #スタック追加
    page.overlay.extend([folder_pick_dialog,pick_files_dialog])

    ###################################
    # excute button　-　実行ボタン
    ###################################
    def execute(_: ft.ControlEvent):
        if not target_file.current.value or not output_folder.current.value:
            return
        result_message.current.value = ""
        page.update()

        if str(Path(target_file.current.value).suffix)[1:].lower() in file_extensions:
            ui_controls.disabled = True
            change_filetype(
                target_file.current.value,
                output_folder.current.value,
                from_suffix.current.value,
                to_suffix.current.value
            )
            ui_controls.disabled = False
            result_message.current.value = "FINISHED!"
            #result_message.current.value = from_suffix.current.value
        else:
            result_message.current.value = "failed..."
        page.update()

    ui_rows.append(ft.Row(controls=[
        ft.Text(ref=from_suffix),
        ft.TextField(ref=to_suffix, label="変換後の拡張子", width=200,  hint_text="png,pdf...")
        ],
        alignment=ft.MainAxisAlignment.CENTER))
        
    ui_rows.append(ft.Row(controls=[
        ft.FilledButton("GO!", on_click=execute),
        ft.Text(ref=result_message)
        ],
        alignment=ft.MainAxisAlignment.CENTER))

    ###################################
    # render page
    ###################################
    ui_controls = ft.Column(controls=ui_rows)
    page.add(ui_controls)


ft.app(target=main)
