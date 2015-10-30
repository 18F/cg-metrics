#! /usr/bin/env python

##########
# This script serves as 1) a script to automate writing common variables across multiple files
# and 2) inject secret values in places.
# It reads the config.toml file for values.
##########

import pytoml as toml
import ConfigParser

# Read the toml file.
# The user should have copied config_example.toml and filled in their values.
configToml = None
with open('config.toml') as tomlFile:
    configToml = toml.load(tomlFile)

# Heka config
hekaToml = None
with open('heka/hekad_example.toml', 'r') as tomlFile:
    hekaToml = toml.load(tomlFile)
    # Inject values for Slack communication
    hekaToml["SlackEncoder"]["config"]["username"]=configToml["Slack"]["username"]
    hekaToml["SlackEncoder"]["config"]["channel"]=configToml["Slack"]["channel"]
    hekaToml["SlackOutput"]["address"]=configToml["Slack"]["address"]
    # Inject values for environment names
    for key, values in hekaToml.iteritems():
        if "message_matcher" in values:
            values["message_matcher"] = values["message_matcher"].replace("cf-np", configToml["Env"]["np"])
            values["message_matcher"] = values["message_matcher"].replace("cf-prd", configToml["Env"]["prd"])

# Write to the final hekad.toml
with open('heka/hekad.toml', 'w') as tomlFile:
    toml.dump(tomlFile, hekaToml)

# Heka Globals
with open('heka/lua_modules/sample_globals.lua', 'r') as sampleFile, open('heka/lua_modules/globals.lua', 'w') as globalFile:
    for line in sampleFile:
        line = line.replace("http://server.company.com", configToml["Host"]["protocol"] + "://" + configToml["Host"]["grafana_address"])
        line = line.replace("cf-prd", configToml["Env"]["prd"])
        line = line.replace("cf-np", configToml["Env"]["np"])
        globalFile.write(line)


# Grafana Config
grafanaConfig = ConfigParser.ConfigParser()
grafanaConfig.read("grafana/grafana_example.ini")
# Set the domain for viewing grafana
grafanaConfig.set("server", "domain", configToml["Host"]["grafana_address"])
# Write the final grafana.ini file
with open('grafana/grafana.ini', 'w') as iniFile:
    grafanaConfig.write(iniFile)

