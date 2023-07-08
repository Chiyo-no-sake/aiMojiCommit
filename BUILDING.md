To build the software from source, you will need python 3.17 or newer installed.

The builder used is pyinstaller, that build pyhon code to a single platform dependent executable. 
It can be installed by running `pip install pyinstaller`.

You will also need to install the dependencies, which can be done by running `pip install -r requirements.txt`.

After this, you can run the script `build.sh` to build the executable, which will be located in the `dist` folder.