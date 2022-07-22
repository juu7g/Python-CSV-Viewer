# Python-CSV-Viewer


## �T�v Description
CSV�r���[�A  

CSV�t�@�C����I�����A�t�@�C���̓��e�������X�g�r���[�ŕ\������  
Select CSV files and view the contents of files in a list view  

## ���� Features

- CSV,TSV,TEXT�t�@�C����ǂݍ��݂��̓��e����ʂɕ\��  
	Read CSV, TSV, TEXT files and display their contents on the screen  
- �����t�@�C�����^�u�\��  
	Tab display of multiple files  
- �^�u���Ƃɍs�̍�������������  
	Automatically adjust row height for each tab  
- **�h���b�O���h���b�v**�Ńt�@�C�����w��\  
	File can be specified by drag and drop  
- exe�Ƀh���b�O���h���b�v�Ńt�@�C�����w��\  
	File can be specified by dragging and dropping to exe  
- Tkinter��Treeview���g�p  
	Use Treeview in Tkinter  
- �P�s�����ɔw�i�F��ς���  
	Change the background color every other line  
- ��̕�����������  
	Automatically adjust column width    
- �s�̍�������������  
	Automatically adjust row height    
- �c���X�N���[���o�[��\��  
	Display vertical and horizontal scroll bars   
- �����R�[�h���w��\  
	Character code can be specified  
- ��̌��o�����N���b�N���ă\�[�g  
	Column sort by click column heading  

## �ˑ��֌W Requirement

- Python 3.8.5  
- TkinterDnD2 0.3.0  

## �g���� Usage

```dosbatch
	CSV_viewer.exe
```
�܂���CSV_viewer.exe�̃A�C�R���ɕ\���������t�@�C�����h���b�O���h���b�v���܂�

- ���� Operation  
	- �h���b�O���h���b�v�ł̑���  
		Drag and drop operation  
		- �A�v����ʏ�̔C�ӂ̈ʒu�ɕ\���������t�@�C�����h���b�O���h���b�v  
			Drag and drop the file you want to display anywhere on the application screen  
	- �t�@�C���I���ł̑���  
		Operation by file selection  
		- �t�@�C���I���{�^�����N���b�N���t�@�C����I��  
			Click the file selection button and select the file  
	- �����R�[�h�̃G���[���o���ꍇ  
		When a character code error occurs
		- �u�����R�[�h�v�̃R���{�{�b�N�X����ʂ̂��̂�I��  
			Select another from the "Character code" combo box  
		- �܂��́u�����R�[�h�v�̃R���{�{�b�N�X�ɒ��ړ���  
			Or enter directly in the "Character code" combo box  
			Python���F���ł��镶���R�[�h�łȂ��ƃG���[�ɂȂ�܂�  
			An error will occur if the character code is not recognizable by Python  
	- ��̌��o�����N���b�N���ă\�[�g  
		Column sort by click column heading  

- ��ʂ̐��� Screen description  
	- �w�肵���t�@�C���̓��e��\�`���ŕ\�����܂�  
		Displays the contents of the specified file in tabular format  
	- �����t�@�C�����w�肵���ꍇ�A�^�u��ς��ĕ\�����܂�  
		If multiple files are specified, the tabs will be changed and displayed  
	- �\�[�g�̎��Ɍ��o���Ƃ��ă\�[�g���Ȃ��s������ʎw��\  
		You can specify the number of lines that will not be sorted as a heading when sorting  

## �C���X�g�[�����@ Installation

- pip install tkinterdnd2  

## �v���O�����̐����T�C�g Program description site

- [CSV viewer�A�v���̍���(�h���b�O�A���h�h���b�v)�yPython�z - �v���O�����ł��������ł��邩��](https://juu7g.hatenablog.com/entry/Python/csv/viewer)  
- [Tkinter Treeview �̗�̃\�[�g(CSV viewer�@�\�A�b�v)�yPython�z - �v���O�����ł��������ł��邩��](https://juu7g.hatenablog.com/entry/Python/csv/viewer-column-sort)  

## ��� Authors
juu7g

## ���C�Z���X License
���̃\�t�g�E�F�A�́AMIT���C�Z���X�̂��ƂŌ��J����Ă��܂��BLICENSE.txt���m�F���Ă��������B  
This software is released under the MIT License, see LICENSE.txt.

