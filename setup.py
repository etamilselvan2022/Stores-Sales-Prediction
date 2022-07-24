from setuptools import setup,find_packages
from typing import List


#Declaring Variables
PROJECT='store-sales-predictor'
VERSION='0.0.0'
AUTHOR='Tamil'
DESCRIPTION='Store Sales Prediction Machine Learning Project'
REQUIREMENT_FILE_NAME='requirements.txt'
HYPHEN_E_DOT='-e .'

def get_requirements_list()-> List[str]:
    """
    Description: This function is going to return list of requirement
    mention in requirements.txt file
    return This function is going to return a list which contain name
    of libraries mentioned in requirements.txt file
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirements_list=requirement_file.readlines()
        requirements_list=[requirement_name.replace('\n','') for requirement_name in requirements_list]
        if HYPHEN_E_DOT in requirements_list:
            requirements_list.remove(HYPHEN_E_DOT)
        return requirements_list



setup(
    name=PROJECT,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=get_requirements_list()
)            