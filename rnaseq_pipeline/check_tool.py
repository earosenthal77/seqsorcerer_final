import subprocess

def check_tool_version(tool_name, command):
    # Run the command to get tool version
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    # Decode stdout and stderr
    stdout_str = result.stdout.decode('utf-8').strip()
    stderr_str = result.stderr.decode('utf-8').strip()
    
    if result.returncode == 0:
        return stdout_str
    else:
        return f"Error: {stderr_str}"
    
def define_tools():
    # Define tools and their corresponding commands to check versions
    tools = {
        "hisat2": "hisat2 --version",
        "trim_galore": "trim_galore --version",
        "featureCounts": "featureCounts -v"
    }
    return tools