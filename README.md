To use the newer version of python and django, I created new app folder named "briefly"
In the new app folder, the following versions are used.

Python=3.12.7
Django=5.1.3
I have added npm package to use advanced version of CSS library called SASS.
I assume this will not cause any trouble in running the app.
In case it does, I am using these versions for node and npm.

node=v20.11.1
npm=10.2.4
After pulling the branch, create a virtual environment and run the following command, which will get you all the required packages

conda create -n briefly
conda activate briefly
conda install --file requirements.txt
