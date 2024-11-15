Ian Setia, Andrew Linares
isetia@nd.edu, alinare2@nd.edu

Flask:
- Set Upload Folder: put the location of toscan directory relative to where the flaskinterface.py script is being run from
- The code is hardcoded to Ian's machine where the scandata directory is directly under the repos directory and contains all the necessary subdirectories (approved, quarantined, log, toscan)

testscript.sh
- The first argument is where the toscan directory is located
- The second argument is where the directory holding all archive files to be moved is located
