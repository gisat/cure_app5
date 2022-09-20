from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cure_app5',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        'console_scripts': [
            'cureApp05 = cure_app5.main:cli',
        ],
    },
)