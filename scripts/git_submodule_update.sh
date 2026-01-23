git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | \
    while read key path; do \
        url=$(git config -f .gitmodules ${key%.path}.url); \
        git clone --depth 1 $url $path; \
        pushd $path
            git submodule update --init --recursive
        popd
    done
