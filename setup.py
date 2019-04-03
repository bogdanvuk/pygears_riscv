from setuptools import setup, find_packages

setup(
    name='pygears_riscv',
    version='0.0.1',
    description='PyGears RISC-V implementation',
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.6.0',
    install_requires=['pygears', 'pexpect'],
    license='MIT',
)
