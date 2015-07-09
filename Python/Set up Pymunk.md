# Set up Pymunk for Windows
This documentation willl outline the steps to properly install and run the Pymunk physics library using Pygame as a renderer. 

## Requirements
+ Python (>=2.7)
+ Windows 7
+ Pip (python's package manager)

## Installing Pymunk
In the command prompt run 

    > pip install pymunk

This will download and install the latest version of pymunk. To check if pymunk was properly installed, open Python's command line interpreter (type <code>python</code> on the command line) and run 

    >>> import pymunk

If you see
        
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    Import Error: No module named pymunk

then the package was not properly installed.

## Installing Pygame
Unfortunately, installing pygame on Windows is not as easy as pymunk. For some reason, pip does not seem to find the pygame package. Here is a work around that seems to work (not too sure why). **NOTE**: You may be able to get it working without PySDL2 but I have not checked this myself.

#### Install PySDL2 and Wheels
Install the PySDL2 package using pip:

    pip install PySDL2

You can also download and install it manually [here](https://pypi.python.org/pypi/PySDL2).

We are going to install pygame as a wheel file. As stated [here](https://pypi.python.org/pypi/wheel), "A wheel is a ZIP-format archive with a specially formatted filename and the .whl extension". Therefore we need to install the wheel Python package.

Install the wheels package using pip:

    pip install wheel

#### Getting Pygame
Finally, we can install pygame. Go to this [link](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) and you should see several Pygame files.

<img src='../_images/Pygame.png' class='' style='max-width:853px; width:100%' alt='Pygame files'>

Download the <code>*win32.whl</code> file that has the proper Python version. For example, if you have Python 2.7, download <code>pygame-1.9.2a0-cp27-none-win32.whl</code>.

On the command line, <code>cd</code> into the directory containing the .whl file you downloaded above. Then run:

    pip install <package-name>.whl

For example, if you downloaded <code>pygame-1.9.2a0-cp27-none-win32.whl</code> then run:

    pip install pygame-1.9.2a0-cp27-none-win32.whl

### Check
To check that you have all the proper packages you can run: <code>pip freeze</code>. If you correctly installed the packages, you should see:

<img src='../_images/Correct_pip.png' class='' style='max-width:853px; width:60%' alt='Pygame files'>

Of course, the version of each package may be different on your computer.

In addition, you can go to the Python command line interpreter and type <code>import pymunk</code> and <code>import pygame</code>. If you see no errors, then the packages are correctly installed.