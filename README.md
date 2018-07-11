# FileContentSearch
Small tool to look into all files of a directory and it's subdirectories and mark the files in which a given term appears.

![FileContentSearch](https://ibb.co/gLRNxT)

## Install
**Building the executable yourself:**
1. Download source: *git clone https://github.com/Ste-Tis/FileContentSearch.git*
2. Install cx_Freeze: *pip install cx_Freeze*
3. Execute the build process in the main dir of the project: *python36 setup.py build*

**Use the provided Win executable:**
1. Download all files inside *build/exe.win-amd64-3.6* onto your PC
2. Add the directory with fcs.exe to your PATH

## Usage
**Using the source:**
```python
python36 fcs.py [term] -d [target-dir] -e [extensions] -l
```

**Using the executable:**
```python
fcs.exe [term] -d [target-dir] -e [extensions] -l
```

## Parameter
Combine the following commandline are supported in the current version.

**Search for multiple terms at once:**
```
fcs.exe "Egon Olsen" 
```
Separate terms by space and use double quotes to include whitespaces in the term.

**Choose the root directory for the search:**
```
fcs.exe [term] -d C:\My\Path\To\Root\
fcs.exe [term] --dir C:\My\Path\To\Root\
```
If no directory is given, the current active directory in the commandline tool is searched.

**Only look into files with given extensions:**
```
fcs.exe [term] -e .py .txt
fcs.exe [term] -extensions .py .txt
```
Only files with the given extensions are searched. Separathe multiple extensions by space.

**Show in which line term appears:**
```
fcs.exe [term] -l
fcs.exe [term] --lines
```
Also show in which line of the file the term appears. Search will take longer.

**Active case sensitive search:**
```
fcs.exe [term] -cs
fcs.exe [term] --case-sensitive
```
By default the search ignores upper- and lower case.

**Display full path to file:**
```
fcs.exe [term] --long
```
The path to the file is shortened, display the full path with this option.

**Don't look into subdirectories:**
```
fcs.exe [term] -ns
fcs.exe [term] --no-subdirectories
```
By default also subdirectories of the root directory are searched. Only look into files in the root directory with this option.

## License

This project is licensed under the MIT license. See the [LICENSE](https://github.com/Ste-Tis/FileContentSearch/blob/master/LICENSE) file for more info.




