Ian Setia, Andrew Linares
isetia@nd.edu, alinare2@nd.edu

Flask:
- Set Upload Folder: put the location of toscan directory relative to where the flaskinterface.py script is being run from
- The code is hardcoded to Ian's machine where the scandata directory is directly under the repos directory and contains all the necessary subdirectories (approved, quarantined, log, toscan)
- If the number of files in the extracted archive is too large, it may require the user to put in another file (if the process time of the initial inputted file exceeds 2 seconds e.g. Scalebox repo)

testscript.sh
- The first argument is where the toscan directory is located
- The second argument is where the directory holding all archive files to be moved is located
