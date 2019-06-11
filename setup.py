from setuptools import setup



setup(
    name = 'cgccli',
    version = '0.1.0',
    packages = ['cgccli'],
    install_requires = ['click',
			'requests'],
    entry_points = {
        'console_scripts': [
            'cgccli = cgccli.__main__:main'
        ]
    })
