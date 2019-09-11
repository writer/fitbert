#!/bin/bash

release ()
{
    VERSION=$(cat VERSION)
    twine upload --config-file .pypirc dist/fitbert-"$VERSION".tar.gz
}

main()
{
    if [ -f .pypirc ]; then
        release
    else
        echo "## MISSING .pypirc file, can't release to PyPi!"
    fi
}

#########################
# Actually run the code #
#########################
main
