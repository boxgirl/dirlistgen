## A minimal representation of the inclusion/exclusion list of directories

This program can efficiently include and exclude directories from a directory tree, producing a minimal representation of the resulting inclusion/exclusion list. It can be used in a variety of scenarios including, but not limited to, music/video/other material sharing and library management.

## How to install

```python setup.py install```

## How to use
'--add', '-a' - Folder to add, multiple=True

'--delete', '-d' - Folder to delete, multiple=True

'--root', '-r' - Start folder  
'--file','-f' - File with directories of folders ( 1st line = root)  
Example of file:
```
   r PATH //root
   + PATH //include
   - PATH //exclude
```
```python3 dirlistgen.py -r "PATH" -a "PATH" -d "PATH" -a "PATH"... -d "PATH"...```
