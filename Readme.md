# Readme

## About
This is a search tool to index large local drives by file name and folders. It is based off a Youtube tutorial (https://youtu.be/IWDC9vcBIFQ). The GUI is based on PySimpleGUI for which the cookbook can be found here: https://pysimplegui.readthedocs.io/en/latest/

## How to use
### Setting up the evironment
* Install anaconda, python 3.9.*, VS Code
* Open VS Code through Anaconda prompt (i.e. inside Anaconda prompt use cd ##path to Jsearch folder##, then code . to open VS Code in that folder location). That will activate the conda environment.
* `conda install -c conda-forge pysimplegui`
* Press F5 in VS Code to run (make sure in View / Command Palette you have selected Anaconda as your 'Python interpreter')
* You can update the *.bat files with the correct paths and then it can be a shortcut on your desktop
* You can remove the _ from the end of `settings_.txt` and set your default drive there

### Using the program
* `python Jsearch.py` for the main program
* The file `Jsearch.bat` can have the paths updated in it (see file) then it can be used as a shortcut in Windows

## Improvements made
* Indexing and opening previously indexed drives now possible

## Improvements to do
* Add feature so does api call to github to check that lastest version of "master" branch is used
* Allow searches of two phrases
* Have hyperlink to open document
* Index file creation date and sort results by date
* Do far more detailed indexing with project started here https://github.com/jbjbjb1/file-metadata-scanner