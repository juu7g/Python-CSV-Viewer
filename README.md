# Python-CSV-Viewer


## 概要 Description
CSVビューア  

CSVファイルを選択し、ファイルの内容ををリストビューで表示する  
Select CSV files and view the contents of files in a list view  

## 特徴 Features

- CSV,TSV,TEXTファイルを読み込みその内容を画面に表示  
	Read CSV, TSV, TEXT files and display their contents on the screen  
- 複数ファイルをタブ表示  
	Tab display of multiple files  
- タブごとに行の高さを自動調整  
	Automatically adjust row height for each tab  
- **ドラッグ＆ドロップ**でファイルを指定可能  
	File can be specified by drag and drop  
- exeにドラッグ＆ドロップでファイルを指定可能  
	File can be specified by dragging and dropping to exe  
- TkinterのTreeviewを使用  
	Use Treeview in Tkinter  
- １行おきに背景色を変える  
	Change the background color every other line  
- 列の幅を自動調整  
	Automatically adjust column width    
- 行の高さを自動調整  
	Automatically adjust row height    
- 縦横スクロールバーを表示  
	Display vertical and horizontal scroll bars   
- 文字コードを指定可能  
	Character code can be specified  
- 列の見出しをクリックしてソート  
	Column sort by click column heading  

## 依存関係 Requirement

- Python 3.8.5  
- TkinterDnD2 0.3.0  

## 使い方 Usage

```dosbatch
	CSV_viewer.exe
```
またはCSV_viewer.exeのアイコンに表示したいファイルをドラッグ＆ドロップします

- 操作 Operation  
	- ドラッグ＆ドロップでの操作  
		Drag and drop operation  
		- アプリ画面上の任意の位置に表示したいファイルをドラッグ＆ドロップ  
			Drag and drop the file you want to display anywhere on the application screen  
	- ファイル選択での操作  
		Operation by file selection  
		- ファイル選択ボタンをクリックしファイルを選択  
			Click the file selection button and select the file  
	- 文字コードのエラーが出た場合  
		When a character code error occurs
		- 「文字コード」のコンボボックスから別のものを選択  
			Select another from the "Character code" combo box  
		- または「文字コード」のコンボボックスに直接入力  
			Or enter directly in the "Character code" combo box  
			Pythonが認識できる文字コードでないとエラーになります  
			An error will occur if the character code is not recognizable by Python  
	- 列の見出しをクリックしてソート  
		Column sort by click column heading  

- 画面の説明 Screen description  
	- 指定したファイルの内容を表形式で表示します  
		Displays the contents of the specified file in tabular format  
	- 複数ファイルを指定した場合、タブを変えて表示します  
		If multiple files are specified, the tabs will be changed and displayed  
	- ソートの時に見出しとしてソートしない行数を画面指定可能  
		You can specify the number of lines that will not be sorted as a heading when sorting  

## インストール方法 Installation

- pip install tkinterdnd2  

## プログラムの説明サイト Program description site

- [CSV viewerアプリの作り方(ドラッグアンドドロップ)【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/csv/viewer)  
- [Tkinter Treeview の列のソート(CSV viewer機能アップ)【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/csv/viewer-column-sort)  

## 作者 Authors
juu7g

## ライセンス License
このソフトウェアは、MITライセンスのもとで公開されています。LICENSE.txtを確認してください。  
This software is released under the MIT License, see LICENSE.txt.

