from setuptools import setup, find_packages

setup(
    name='aiohttp2pydantic',
    version='0.8',
    license='MIT',
    author="Oboro Works LLC",
    author_email='dev@oboroworks.com',
    packages=find_packages(where='aiohttp2pydantic'),
    package_dir={'': 'aiohttp2pydantic'},
    url='https://github.com/oboroworks/aiohttp2pydantic',
    keywords='aiohttp, pydantic',
    install_requires=[
        'aiohttp',
        'pydantic',
    ],
)
