# Avorion Mod Manager


The goal of this shell script is to provide a linux server admin the ability to install and remove mods easily from Avorion without worry about damaging game files.



## Mods.json

This file serves as the main mod list powering the installer.  It contains references to where to download files, their relative path inside game directories & any additional meta available.


##### Example Mod Config Object

```
{
	"author": "author_name",
	"name": "Name of Mod", 
	"url": "URL for mod homepage",
	"description": "short description about the mod here",
	"files": [
		{
			"file_name": "file-a",
			"url": "http://avorion.net/path/to/mode_file_a.lua",
			"relative_path": "data/scripts/commands/"
		},
		{
			"file_name": "file-b",
			"url": "http://avorion.net/path/to/mode_file_b.lua",
			"relative_path": "data/scripts/player/cmd/"
		},
	]
}
```
