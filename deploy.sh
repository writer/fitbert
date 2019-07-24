#!/bin/bash

deploy ()
{
    VERSION=`cat VERSION`
    twine upload --config-file ./.pypirc dist dist/fitbert-"$VERSION".tar.gz
}

main()
{
    if [ -f .pypirc ]; then
        deploy
    else
        echo "## MISSING .pypirc file, can't deploy!"
    fi
}

#########################
# Actually run the code #
#########################
main
