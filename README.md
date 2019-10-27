# Background changer

This project aims to write a python script that will change the wall paper of the desktop.

This project can be split into parts:

1. Change the background to a single image saved in a specific place on the HDD.
2. Change the background to cycle through a list of images in a folder.
3. Change the background to a single image online.
4. Change the background to cycle through a list of images from a website. Maybe a particular theme and pull the images off google.


## Running the program

To run the program, you must have python installed. This has been written for Python 3.6.4.

To run the program, type in your command prompt

```bat
REM Use the argument --help to know how to use the program.

REM If installed into site-packages
start python -m WallpaperChanger --help

REM If running from the project directory
start python __main__.py --help
```

## Maintaining

When adding new modules downloaded by pip, be sure to update the `requirements.txt` file. To do this, use the following command.

```bash
# To save dependencies
pip freeze &> requirements.txt

# To load dependencies
pip install -R requirements.txt
```
