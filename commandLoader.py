import importlib;
import glob;

def loadCommands(bot):

    #Read all files in runnables folder
    runnables = glob.glob("runnables/*.py")
    
    for runnable in runnables:

        #Import the file
        runnable = runnable.replace("runnables\\", "").replace(".py", "")
        commandClass = importlib.import_module("runnables." + runnable)

        #Get the command
        command = commandClass.command(bot)