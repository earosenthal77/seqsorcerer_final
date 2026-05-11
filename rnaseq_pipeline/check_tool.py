# import packages
import subprocess

def check_tool_version(tool_name, command):
    # run the command to get tool version
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    # decode stdout and stderr
    stdout_str = result.stdout.decode('utf-8').strip()
    stderr_str = result.stderr.decode('utf-8').strip()
    
    if result.returncode == 0:
        return stdout_str
    else:
        return f"Error: {stderr_str}"
    
def define_tools():
    # define tools and their commands to check versions
    tools = {
        "hisat2": "hisat2 --version",
        "trim_galore": "trim_galore --version",
        "featureCounts": "featureCounts -v"
    }
    return tools