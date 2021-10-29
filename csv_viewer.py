"""
CSVビューワー
"""

from datetime import datetime
from posixpath import basename
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import csv, itertools, re, os, sys
from tkinter import filedialog
from tkinterdnd2 import *

class ListView(ttk.Frame):
    """
    CSVをリストビューで表示する
    """
    def __init__(self, master):
        """
        画面の作成
        上のFrame: 入力用
        下のFrame: notebookで出力
        """
        super().__init__(master)
        self.csv_op = CsvOp()
        self.u_frame = tk.Frame(bg="white")     # 背景色を付けて配置を見る
        self.b_frame = tk.Frame(bg="green")     # 背景色を付けて配置を見る
        self.note = ttk.Notebook(self.b_frame)
        self.u_frame.pack(fill=tk.X)
        self.b_frame.pack(fill=tk.BOTH, expand=True)
        self.note.pack(fill=tk.BOTH, expand=True)
        self.create_input_frame(self.u_frame)

    def fixed_map(self, option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in self.style.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]

    def create_input_frame(self, parent):
        """
        入力項目の画面の作成
        上段：入力ファイルパス、ファイル選択ボタン、開くボタン、文字コード選択
        下段：メッセージ
        """
        self.lbl_csv = tk.Label(parent, text="CSV:")
        self.var_csv_path = tk.StringVar(value="")
        # リストボックス height=負 で全体表示
        self.list_csv_path = tk.Listbox(parent, height=-1, listvariable=self.var_csv_path)
        self.btn_f_sel = tk.Button(parent, text="ファイル選択", command=self.select_files)
        self.lbl_encode = tk.Label(parent, text="文字コード:")
        self.var_encode = tk.StringVar(value="")
        self.cbb_encode = ttk.Combobox(parent, values=["utf_8", "cp932"], width=5, textvariable=self.var_encode)
        self.cbb_encode.current(1)  # 第1要素を選択状態にする
        self.msg = tk.StringVar(value="msg")
        self.lbl_msg = tk.Label(parent
                                , textvariable=self.msg
                                , justify=tk.LEFT
                                , font=("Fixedsys", 11)
                                , relief=tk.RIDGE
                                , anchor=tk.W)
        self.lbl_msg.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)    # 先にpackしないと下に配置されない
        self.cbb_encode.pack(side=tk.RIGHT, fill=tk.Y)
        self.lbl_encode.pack(side=tk.RIGHT, fill=tk.Y)
        self.lbl_csv.pack(side=tk.LEFT, fill=tk.BOTH)
        self.list_csv_path.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.btn_f_sel.pack(side=tk.RIGHT)
        # bind
        self.cbb_encode.bind("<<ComboboxSelected>>", self.after_change_encode)
        self.cbb_encode.bind("<Return>", self.after_change_encode)

    def create_tree_frame(self, parent:ttk.Notebook, tab_name="") -> ttk.Treeview:
        """
        Treeviewとスクロールバーを持つframeを作成し、notebookにaddする。
        frameは、Treeviewとスクロールバーをセットする
        Treeviewは、listview形式、行は縞模様
        Args:
            ttk.Notebook:   ttk.Notebook
            string:         tab_name
        Returns:
            Treeview:       ツリービュー
        """
        # tagを有効にするためstyleを更新 tkinter8.6?以降必要みたい
        # 表の文字色、背景色の設定に必要
        self.style = ttk.Style()
        self.style.map('Treeview', foreground=self.fixed_map('foreground')
                                 , background=self.fixed_map('background'))
        # タブごとのスタイルの設定
        self.style.configure(tab_name + ".Treeview")
        # frameの作成。frameにTreeviewとScrollbarを配置する
        frame1 = tk.Frame(parent, bg="cyan")
        # Treeviewの作成
        treeview1 = ttk.Treeview(frame1, style=tab_name + ".Treeview")
        treeview1["show"] = "headings"      # 表のデータ列だけを表示する指定
        treeview1.tag_configure("odd", background="ivory2")     # 奇数行の背景色を指定するtagを作成
        # 水平スクロールバーの作成
        h_scrollbar = tk.Scrollbar(frame1, orient=tk.HORIZONTAL, command=treeview1.xview)
        treeview1.configure(xscrollcommand=h_scrollbar.set)
        # 垂直スクロールバーの作成
        v_scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=treeview1.yview)
        treeview1.configure(yscrollcommand=v_scrollbar.set)
        # pack expandがある方を後にpackしないと他が見えなくなる
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)          # 先にパックしないと表示されない
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)           # 先にパックしないと表示されない
        treeview1.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        parent.add(frame1, text=tab_name)
        return treeview1

    def update_tree_column(self, tree:ttk.Treeview, columns:list):
        """
        TreeViewの列定義と見出しを設定
        見出しの文字長で列幅を初期設定
        Args:
            Treeview:   treeviewオブジェクト
            list:       列名のリスト
        """
        tree["columns"] = columns                  # treeviewの列定義を設定
        font1 = tkFont.Font()
        for col_name in columns:
            tree.heading(col_name, text=col_name)  # 見出しの設定
            width1 = font1.measure(col_name) + 10  # 見出しの文字幅をピクセルで取得
            # width1 = min(width1, 200)              # 見出しの幅が200pxより大きい時は200pxにする
            tree.column(col_name, width=width1)    # 見出し幅の設定

    def update_tree_by_result(self, tree:ttk.Treeview, rows:list):
        """
        rows(エクセルのデータ)をTreeViewに設定
        要素の文字幅が見出しの文字幅より長い場合は、列幅を変更する。
        奇数列の背景色を変更
        Args:
            Treeview:   Treeviewインスタンス
            list:       Excel実行結果セット(行リストの列リスト)
        """
        if not rows:    # 要素が無ければ戻る
            return
        font1 = tkFont.Font()
        # 要素の長さにより列幅を修正
        for i, _ in enumerate(rows[0]):     # 列数分回す(1行目の要素数分)
            # 同じ列のデータをリストにし列の値の長さを求め、最大となる列のデータを求める。
            # 値は数字もあるので文字に変換し長さを求める。また、Noneは'None'となるので'    'とする。
            max_str = max([x[i] for x in rows], key=lambda x:len(str(x))) or "    "
            # 求めたものが文字列だったら、改行された状態での最大となるデータを求める。
            # 厳密にはこの状態で最大となるデータを探さなければならないが割愛
            if type(max_str) is str:
                max_str = max(max_str.split("\n"), key=len)
            width1 = font1.measure(max_str) + 10   # 文字幅をピクセルで取得
            header1 = tree.column(tree['columns'][i], width=None) # 現在の幅を取得
            # 設定済みの列幅より列データの幅の方が大きいなら列幅を再設定
            if width1 > header1:
                tree.column(tree['columns'][i], width=width1)    # 見出し幅の再設定
                # print(f"幅の再設定 幅:{width1}、値:{max_str}")   # debug用
        
        # treeviewに要素追加。背景はtagを切り替えて設定
        tree.delete(*tree.get_children())   # Treeviewをクリア
        for i, row in enumerate(rows):
            tags1 = []              # tag設定値の初期化
            if i & 1:               # 奇数か? i % 2 == 1:
                tags1.append("odd") # 奇数番目(treeviewは0始まりなので偶数行)だけ背景色を変える(oddタグを設定)
            tree.insert("", tk.END, values=row, tags=tags1)     # Treeviewに1行分のデータを設定

    def after_change_encode(self, event=None):
        """
        エンコード用コンボボックスの選択を変えた時の処理
        既に読んでいるファイルがある場合に再読み込みする
        """
        if len(self.file_paths) > 0:
            self.open_csv()

    def open_csv(self, event=None):
        """
        CSVファイルを開き、notebookにファイルの内容をタブとして追加する
        タブにはTreeviewを追加し、ファイルのデータを追加する
        データの幅でTreeviewの列の幅を設定する
        データの行数でTreeviewの行の高さを設定する(行ごとにはできないので一番高い行に合わせる)
        """
        self.csv_op.msg = ""
        # DnD対応
        if event:
            # DnDのファイル情報はevent.dataで取得
            # "{空白を含むパス名1} 空白を含まないパス名1"が返る
            # widget.tk.splitlistでパス名のタプルに変換
            self.file_paths = self.list_csv_path.tk.splitlist(event.data)
            
        # 取得したパスから拡張子がself.extentiosのkeyに含まれるものだけにする
        file_paths2 = tuple(path for path in self.file_paths if os.path.splitext(path)[1] in self.csv_op.extensions)
        if len(file_paths2) == 0:
            self.csv_op.msg = "対象のファイルがありません"
            self.msg.set(self.csv_op.msg)
            return
        if file_paths2 != self.file_paths:
            self.csv_op.msg = "対象外のファイルは除きました"
        self.file_paths = file_paths2
        basenames = [os.path.basename(file_path) for file_path in self.file_paths]
        self.var_csv_path.set(basenames)

        self.dict_tables = self.csv_op.get_csv_data(self.file_paths, self.var_encode.get())
        self.msg.set(self.csv_op.msg)

        # notebookの既存のタブを削除
        while self.note.tabs():
            self.note.forget("current")

        for tab_name1 in self.dict_tables:
            # noteにTreeviewを持つタブを追加する
            treeview1 = self.create_tree_frame(self.note, tab_name1)

            # 見出しの文字長で列幅を初期設定、treeviewのカラム幅を文字長に合わせて調整
            self.update_tree_column(treeview1, self.dict_tables.get(tab_name1)[1])

            # rowsをTreeViewに設定、要素の文字幅が見出しの文字幅より長い場合は、列幅を変更する。偶数列の背景色を変更
            self.update_tree_by_result(treeview1, self.dict_tables.get(tab_name1)[0])

            # 一番行数の多い行に合わせて高さを設定する
            # ２次元のデータを平坦化しstr型だけを抽出する
            cells = [s for s in itertools.chain.from_iterable(self.dict_tables.get(tab_name1)[0]) if type(s) is str]
            if not cells:
                continue    # 対象がない場合は抜ける
            # 抽出したリストの要素の中で改行の数の最も多い要素を取得
            longest_cell = max(cells, key=lambda x:x.count("\n"))
            max_row_lines = longest_cell.count("\n") + 1             # 改行の数を数える
            # Treeviewの行の高さを変更
            self.style.configure(tab_name1 + ".Treeview", rowheight = 18 * max_row_lines)
        
    def select_files(self, event=None):
        """
        ファイル選択ダイアログを表示。選択したファイルパスを保存
        """
        # 拡張子の辞書からfiletypes用のデータを作成
        # 辞書{".csv":"CSV", ".tsv":"TSV"}、filetypes=[("CSV",".csv"), ("TSV",".tsv")]
        self.file_paths = filedialog.askopenfilenames(filetypes=[(value[0], key) for key, value in self.csv_op.extensions.items()])
        basenames = [os.path.basename(file_path) for file_path in self.file_paths]
        self.var_csv_path.set(basenames)
        self.open_csv()		# オープン処理の実行

class CsvOp():
    """
    CSVデータの操作を行う
    """
    def __init__(self):
        self.msg = ""   # メッセージ受渡し用
        # 対象拡張子	辞書(key:拡張子、値:(表示文字, 区切り文字))
        self.extensions = {".csv":("CSV", ","), ".tsv":("TSV", "\t"), ".txt":("Text", "\n")}

    def get_csv_data(self, file_names:tuple, encode_:str) -> dict:
        """
        CSVファイルを読みデータを返す
        Args:
            str:    ファイル名
        Returns:
            dict:   CSVのrowsとカラム定義をファイル名をキーにした辞書
        """
        try:
            # self.msg = ""   # メッセージクリア
            tables = {}
            for file_name in file_names:   # パス名で回す
                rows1 = None
                basename = os.path.basename(file_name)
                # 拡張子によってcsvのdelimiterを変える(辞書から取得)
                delimiter_ = self.extensions.get(os.path.splitext(file_name)[1])[1]
                with open(file_name, encoding=encode_, newline="") as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=delimiter_)
                    rows1 = [row for row in spamreader]
                    # 最大列数を求める
                    column_len = max(len(v) for v in rows1)
                    # 列の不足を空文字で補完する
                    rows1 = [x + [""] * (column_len - len(x)) for x in rows1]
                # 列定義の作成(現状は1開始の整数)
                columns1 = [i for i in range(1, column_len + 1)]    # 列定義を列数分行う。1スタート
                # セル値の取得
                tables[basename] = (rows1, columns1)
        except Exception as e:
            self.msg = e
        finally:
            return tables
    
if __name__ == '__main__':
    root = TkinterDnD.Tk()              # トップレベルウィンドウの作成  tkinterdnd2の適用
    root.title("CSV viewer")  # タイトル
    root.geometry("600x600")    # サイズ
    listview = ListView(root)   # ListViewクラスのインスタンス作成
    root.drop_target_register(DND_FILES)            # ドロップ受け取りを登録
    root.dnd_bind("<<Drop>>", listview.open_csv)    # ドロップ後に実行するメソッドを登録
    # コマンドライン引数からドラッグ＆ドロップされたファイル情報を取得
    if len(sys.argv) > 1:
        listview.file_paths = tuple(sys.argv[1:])
        listview.open_csv()							# オープン処理の実行
    root.mainloop()
