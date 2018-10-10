from setuptools import setup, find_packages

setup(
    name='pygears_riscv',
    version='0.0.1',
    description='PyGears RISC-V implementation',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
)
