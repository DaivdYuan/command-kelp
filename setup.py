from setuptools import setup, find_packages

setup(
    name='command_kelp',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'command-kelp = src.helper:main',
            'kelp-alias = src.main:get_alias',
            'kelp = src.main:configure' 
        ]
    },
    install_requires=[
        'openai',
        'pathlib2',
        'psutil'
    ],
)
