import os
import sys
import shutil
import shlex
import tempfile
from PyInstaller import __main__ as pyi


def move_project(src, dst):
    """ Move the output package to the desired path (default is output/ - set in script.js) """
    # Make sure the destination exists
    if not os.path.exists(dst):
        os.makedirs(dst)

    # Move all files/folders in dist/
    for file_or_folder in os.listdir(src):
        _dst = os.path.join(dst, file_or_folder)
        # If this already exists in the destination, delete it
        if os.path.exists(_dst):
            if os.path.isfile(_dst):
                os.remove(_dst)
            else:
                shutil.rmtree(_dst)
        # Move file
        shutil.move(os.path.join(src, file_or_folder), dst)


def convert(command):
    temporary_directory = tempfile.mkdtemp()
    dist_path = os.path.join(temporary_directory, 'application')
    build_path = os.path.join(temporary_directory, 'build')
    extra_args = ['--distpath', dist_path] + ['--workpath', build_path] + ['--specpath', temporary_directory]
    sys.argv = shlex.split(command) + extra_args
    output_directory = os.path.abspath('./')
    pyi.run()
    move_project(dist_path, output_directory)
    shutil.rmtree(temporary_directory)


scoringPath = os.path.abspath('scoring_engine.py')
configPath = os.path.abspath('configurator.py')
balloonPath = os.path.abspath('balloontip.py')
iconPath = os.path.abspath('Scoring_Engine_Logo_Linux_Icon.png')
command_score = 'pyinstaller -y -F -w -i "' + iconPath + '" "' + scoringPath + '"'
command_config = 'pyinstaller -y -F -c -i "' + iconPath + '" "' + configPath + '"'
while True:
    ask = input("To rebuild the configurator type: config. To rebuild the scoring engine type: score. To rebuild both type: both. To exit type: exit.\n")
    if ask.lower() == 'config':
        convert(command_config)
    elif ask.lower() == 'score':
        convert(command_score)
    elif ask.lower() == 'both':
        convert(command_score)
        convert(command_config)
    else:
        exit()

# 'pyinstaller -y -F -w "/home/cyberpatriot/Desktop/configurator.py"'