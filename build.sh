#!/bin/bash

NOW="$(date +'%B %d, %Y')"
BASE_STRING=$(cat VERSION)
BASE_LIST=($(echo "$BASE_STRING" | tr '.' ' '))
V_MAJOR=${BASE_LIST[0]}
V_MINOR=${BASE_LIST[1]}
V_PATCH=${BASE_LIST[2]}
echo -e "Current version: $BASE_STRING"
V_MINOR=$((V_MINOR + 1))
V_PATCH=0
SUGGESTED_VERSION="$V_MAJOR.$V_MINOR.$V_PATCH"

update_deps ()
{
    pip3 install -U setuptools wheel
    pip3 install -r requirements-dev.txt
    pip3 install -r requirements.txt
}

bump_version ()
{
    echo "$SUGGESTED_VERSION" > VERSION
}

update_changelog ()
{
    # requires git access
    # this is buggy, pls fx kthxbye

    echo "## $SUGGESTED_VERSION ($NOW)" > tmpfile
    git log --pretty=format:"  - %s" "v$BASE_STRING"...HEAD >> tmpfile
    echo "" >> tmpfile
    echo "" >> tmpfile
    cat CHANGELOG.md >> tmpfile
    mv tmpfile CHANGELOG.md

    git add CHANGELOG.md VERSION fitbert/version.py
    git commit -m "Bump version to ${SUGGESTED_VERSION}."
    git tag -a -m "Tag version ${SUGGESTED_VERSION}." "v$SUGGESTED_VERSION"
    git push origin --tags
}

create_dist ()
{
    python3 setup.py sdist
}

main ()
{
    update_deps
    bump_version
    create_dist
    update_changelog
}

#########################
# Actually run the code #
#########################
main
