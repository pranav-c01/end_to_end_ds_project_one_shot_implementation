from setuptools import find_packages,setup
# from typing import List

def get_requirements(file_path):    
    '''
        This func return list of requirements
    '''

    requirements = []
    with open("requirements.txt") as f:
        requirements = f.readlines()
        ## replace  \n with ""
        requirements = [req.replace("\n","") for req in requirements]

        ## note that add -e . at last of requirements.txt so that ater executing requirements.txt file setup.py file automatically runs

        # remove -e . from requiremetns string
        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements

setup(
    name = "ML_project",
    version = '0.0.1',
    author = 'Pranav',
    author_email= "pranavjindal43@gmail.com",
    ## find_packages() un folder ko jaake build karega , jaha pe __init.py__ file hgi
    packages = find_packages(),  # note that __init__.py file jaha pe hogi, vaha pe package run karega ye
    install_requires = get_requirements('requirements.txt')
)