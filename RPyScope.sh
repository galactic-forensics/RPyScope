#!/bin/bash

# Change the following variable to your configuration
export RPYSCOPE_HOME=$HOME/RPyScope

cd $RPYSCOPE_HOME
source venv/bin/activate
rpyscope
