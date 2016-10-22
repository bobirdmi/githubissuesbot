from setuptools import setup, find_packages
import pypandoc


pypandoc.convert_file('README.md', 'rst', outputfile='README.rst')

with open('README.rst') as f:
    long_description = ''.join(f.readlines())
 
 
setup(
    name='githubissuesbot',
    version='0.3',
    description='GitHub issues bot as console and web app.',
    long_description=long_description,
    author='Dmitriy Bobir',
    author_email='astercassio@gmail.com',
    url='https://github.com/bobirdmi',
    keywords='github,bot,issues',
    license='Public Domain',
    packages=find_packages(),
    install_requires=['Flask', 'markdown>=2', 'click>=6', 'requests>=2', 'pypandoc>=1'],
    entry_points={
            'console_scripts': [
                'githubbot = githubissuesbot.command_line:main',
            ],
    },
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        ],
)