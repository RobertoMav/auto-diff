# This is a testing repo to create a python package in the most up-to-date (apr-2025) manner

## Nice links:

https://testdriven.io/blog/clean-code-python/

https://google.github.io/styleguide/pyguide.html

https://learngitbranching.js.org/?locale=en%2BUS

## Some additional recommendations were learned and are shared here:
1. Linters
2. Formatters
3. Zshell theme
4. git terminal cmds
5. Extensions: Even better TOML; mypy; Path Intellisense; pylint; Python path; isort; ruff
6. Code push in the push to branch; git pull main to branch -> resolve merge issues  -> git merge branch to main
7. GitHub Actions improving speed = improving costs


## Additional Notes: 
How to merge to main:

1. Changes → git push to branch
2. Git pull main to branch → resolve merge issues
3. Git merge branch to main

Use a settings.json under .vscode folder to have formatter

Formatter changes the multi-args to multi lines after a comma

We use that to be able to change the args without conflicts in merge

Auto formatter → black, ruff (linter?)

Static code → detect issues without running → pylint (evals code)

Flake8, radon code complexity 

mypy → static type checker

from __future__ import annotations → self-referencing types

TypeVar from typing is nice - allows many diff type, but uses only one per call

pre-commit and its yaml file

github actions → jenk/bitbucket actions replacement

Only use git act when we have a PR

[setuptools](https://setuptools.pypa.io/en/latest/) to create packages → .tar.gz

`python [setup.py](http://setup.py) build sdist`  creates the .tar.gz and then we can use `pip install {{package}}`

using `pip install —editable ./` we can use our code as mutable, adding install requires to use sub libs, issues with sdist → runs code on your machine.

1. Solution is the binary format (wheel distribution) `pip install wheel` 
2. pyproj use `pip install build` to use only building packages
3. We have too many config files the solution is pyproject.TOML
4. PEP 621 using pyproj.toml instead of setup.cfg
5. PEP 517 using pyproj instead of setup.py
6. `Path(__**file__**).parent` to access the file loc; when adding diff binary files, such as .json, yaml the wheel / dist will not add them → we need to declare them
7. Using [manifest.in](http://manifest.in) to declare the files we need, issues with recursive files - cached. Using 
    1. `python -m build --sdist (do we need this?) --wheel ./`  
    2. `cd dist` 
    3. `unzip *.whl` 
    4. `cd ..`  - let’s test this
    5. adding this to pyproj file [tools.setuptools.package-data] → we can remove the manifest 
    6. We can also use poetry
8. Reproducibility → using pyproj or requirements such as `pip install -e .` - test
9. pipdeptree to visualize the package dependencies 

106. using dev dependencies + rich print as in pip install package[dev]

107. package-index health score

Ok, so to wrap up we can use the build cmd to build our packages and we can use pip install pkg or pip install -e {{pkg_loc}} to create a direct change in our pkg (-e == editable)

110-113. Publishing to Pypi and test.pypi.org + `twine upload` + Makefile `brew install make` 
make issues: bad error messages, tiny change, big errors
makefile: file to run multiple bash commands (in this case it uses sh)

114. Just, Pyinvoke and finally just falling back to a .sh script
115. bash basics `set -e` makes the program stop when it fails, `set -x` prints every single cmd that runs
116. passing twine and pypi login - using .env. Creating the bash script to:

a. clean our /build /dist folders

b. build our proj

c. publish using twine to test pypi

117. Creating the prod release code + would be nice to automatically bump versions + testing needs -> use git actions or other cicd tool to make the deploy

Git Actions - Section 13:
    - 
