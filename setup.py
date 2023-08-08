from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements = []
    file = open(file_path,'r')
    
    for line in file:
        if "-e ." not in line:
            requirements.append(line.strip('\n'))
    file.close()
    
    return requirements
    
# With this setup we parse our requirements file to get the requirements installed for our project, one can make this static via use of package names in form of a list, instead of parsing a requirements file.
setup(
    name='mlproject',
    version='0.0.1',
    author='<Your Name>',
    author_email='<Your Email>',
    packages=find_packages(), # This will use the codes or modules that we write for our ML pipeline, to ensure that our every module can be used for building the package, we have a __init__.py in src, or any directory that can be reused.
    install_requires=get_requirements('requirements.txt') 
)