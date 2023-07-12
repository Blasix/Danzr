import importlib
import glob
import os


def loadCommands(bot):
    # Read all files in runnables folder
    runnables = glob.glob(os.path.join("runnables", "*.py"))

    for runnable in runnables:
        # Import the file
        runnable = os.path.basename(runnable).replace(".py", "")
        commandClass = importlib.import_module(f"runnables.{runnable}")

        # Get the command
        command = commandClass.command(bot)
