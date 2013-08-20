You can reach me at bahniks@seznam.cz
See COPYING.txt for the licence of Carousel Maze Manager.


WARNING: DO NOT PUT ANYTHING IN 'MODULES' AND 'HELP' DIRECTORIES!
	 They are rewritten when the program is updated.


Known issues in this version:
Internal representation of files changed in this version. Therefore, when files
are loaded from outputs of previous versions (i.e. from saved selected files or 
from a log), their representation does not match the current representation. 
That may lead to duplication of files in loaded files if the same file is 
loaded with both new and old representation. The old representation still 
works. There is no problem with duplication if a file is loaded by two ways 
using the current version (e.g. when a file is added by loading from a log 
that was created by the current version and by 'Add files'). 