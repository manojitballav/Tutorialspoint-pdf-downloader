# Tutorialspoint-pdf-downloader
Download complete pdf's of Tutorial points tutorials.

## Requirements
Python 3.6 or newer. No third-party packages — the standard library is enough.

## Usage
Pass the tutorial name as an argument:

```
python3 pdf-generator.py python
```

Or run it with no arguments and it will prompt:

```
python3 pdf-generator.py
Name of tutorial? (e.g. 'python')
```

Save somewhere other than the current directory with `-o` / `--output-dir`:

```
python3 pdf-generator.py python --output-dir ~/Downloads
```

The name is case-insensitive, and you can paste the tutorial's URL instead of
its name — `https://www.tutorialspoint.com/java/index.htm` works as well as
`java`. Run `python3 pdf-generator.py --help` for the full list of options.

### Exit codes
| Code | Meaning |
| --- | --- |
| `0` | PDF downloaded |
| `1` | Download failed (not found, unreachable, or not a PDF) |
| `2` | Invalid or missing tutorial name |
| `130` | Cancelled with Ctrl-C |

## Finding the tutorial name
* Open https://www.tutorialspoint.com/index.htm
* Scroll down to find your required tutorial library
![image](https://user-images.githubusercontent.com/10193961/110669097-002dc380-81f2-11eb-82b9-5be6b387ae61.png)
* Select the tutorial you would like to download
![image](https://user-images.githubusercontent.com/10193961/110669480-60246a00-81f2-11eb-9d2e-b3411b5ce8ae.png)
* Copy the name of the tutorial

## Running the script
* Clone this project or open terminal and run the following: 
``` git clone https://github.com/manojitballav/Tutorialspoint-pdf-downloader.git ```
* Run the pdf-downloader script using Python
``` python3 pdf-generator.py```
![image](https://user-images.githubusercontent.com/10193961/110670152-125c3180-81f3-11eb-9fe7-0b95352dc35c.png)
* Enter the name of tutorial
![image](https://user-images.githubusercontent.com/10193961/110670265-3881d180-81f3-11eb-815f-4dc34e1aa941.png)
* The file will be downloaded in the same directory as the script file
![image](https://user-images.githubusercontent.com/10193961/110670383-57806380-81f3-11eb-89c0-d4fd11358a32.png)
![image](https://user-images.githubusercontent.com/10193961/110670433-6535e900-81f3-11eb-9d9f-d48aca492492.png)
![image](https://user-images.githubusercontent.com/10193961/110670517-7a127c80-81f3-11eb-89dc-332840afed5a.png)
![image](https://user-images.githubusercontent.com/10193961/110670559-8991c580-81f3-11eb-9ab8-267c4d78f683.png)

Happy Learning !
