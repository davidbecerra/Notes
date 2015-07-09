This documentation will provide a brief outline of the steps needed to successfully install Python on a Windows computer. In addition, it describe how to set up pip, Python's package manager.

## Setting up Python
Download Python from this [link](https://www.python.org/downloads/). Here, you can download the latest version of Python 2 or 3. If there is another version you want, scroll down and download the desired release.

Navigate to your Downloads directory and double click the MSI Python file that was just downloaded.

<img src='python_download.png' style='max-width:853px; width:90%' alt="Python MSI file">

If a Security Warning window pops up, click "Run", then navigate through the installer.

<img src='download_warning.png' style='max-width:853px; width:70%' alt="Download Security Warning">

To verify Python was successfully installed, open the command prompt (Start > type "cmd" in "Search programs and files") and enter:

    python -V

You should see the currently installed Python version.

<img src='python_check.png' style='width:80%' alt='Python command line version number.'>

If instead you get a message saying `python` is not a recognized command, double check that the Python directory is in your PAtH Environment variable.

To add Python to your PATH, go to Start > Control Panel > System and Security > System > Advanced System Settings > Environment Variables. Alternatively, you can run `sysdm.cpl` in the command prompt, go to the "Advanced" tab in the popup window, then click Environment Variables.

Regardless, you should see a new popup window. In the "System variables", select "Path" and click "Edit".