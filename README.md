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
# Make sure you activate your virtual environment.
source ./venv/Scripts/activate

# To save dependencies
pip freeze &> requirements.txt

# To load dependencies
pip install -R requirements.txt
```

## Installing editable WallpaperChanger module.

This is handy if you want to run the WallpaperChanger module outside of the `./src` directory. It also makes importing the WallpaperChanger module from within the test modules easier. This all assumes that you have your virtual environment setup!

After loading your dependencies, you will want to install an editable package of the Wallpaper Changer. This can be done by running the following command within the `./src` directory.

```bash
pip install -e .
```

## Setting up pytest

See [this](https://docs.pytest.org/en/latest/getting-started.html) tutorial for running pytest.

See [this](http://doc.pytest.org/en/latest/goodpractices.html) for good practices.


### Naming Tests

**pytest** will search for test files that start with `test_*.py` or `*_test.py`.

Since this is a relatively small module, we will keep all tests in the same directory. The naming convention will be:

```
test_<module_name>.py

eg:
test_wallpaper.py
```

Each module should have its own test.

