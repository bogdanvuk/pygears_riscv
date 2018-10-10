from setuptools import setup, find_packages

setup(
    name='pygears',
    version='0.1.1',
    description='PyGears RISC-V implementation',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
)
