import yaml
import sLOUT as lout

# writeConfig() configuration reader
# Usage:
#   file: string, file to read from, you probably want 'hardwareIntegration/status.yml'
#   parameter: string, name of "varible" in config file, must be exact.
def writeConfig(file, parameter, newValue):
    with open(file, 'r') as f:
            WholeAssYAMLFile = yaml.safe_load(f)
    with open(file, 'w+') as f:
        WholeAssYAMLFile[parameter] = newValue
        yaml.safe_dump(WholeAssYAMLFile, f)
                
    return True