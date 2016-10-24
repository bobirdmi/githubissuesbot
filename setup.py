from setuptools import setup, find_packages


with open('githubissuesbot/README.md', 'w') as file_out:
    with open('README.md', 'r') as file_in:
        print(file_in.read())
        file_out.write(file_in.read())


"""Uncomment the following code if there is README.rst, otherwise see next section."""
with open('README.rst', 'r') as file:
    long_description = file.read()

"""
If there is only README.md:
    1) install 'pypandoc' (pip install pypandoc)
    2) uncomment the following code
    3) create distribution package (python setup.py sdist)
    3) if your PC satisfies 'pandoc' requirements, README.rst will be created, otherwise README.txt.
    4) comment this code section and uncomment the section above
    5) run again (python setup.py sdist)
"""

# long_description = ''
# try:
#     import pypandoc
#     print('======== pypandoc ready ======')
# except ImportError:
#     pypandoc = None
#     print('======== pypandoc not ready ======')
#
# if pypandoc:

# try:
#     import pypandoc
#     from pypandoc.pandoc_download import download_pandoc
#
#     try:
#         pypandoc.get_pandoc_version()
#     except OSError as e:
#         print('Warning: ' + str(e))
#         print('Downloading pandoc...')
#         download_pandoc()
#
#     pypandoc.convert_file('README.md', 'rst', outputfile='README.rst')
#     with open('README.rst', 'r') as file:
#         long_description = file.read()
# except (ImportError,RuntimeError) as e:
#     print('Warning: ' + str(e) + ': could not convert Markdown to RST.')
#
#     with open('README.txt', 'w') as file_out:
#         with open('README.md', 'r') as file_in:
#             long_description = file_in.read()
#             file_out.write(long_description)

setup(
    name='githubissuesbot',
    version='0.3.1',
    description='GitHub issues bot as console and web app.',
    long_description=long_description,
    author='Dmitriy Bobir',
    author_email='astercassio@gmail.com',
    url='https://github.com/bobirdmi',
    keywords='github,bot,issues',
    license='Public Domain',
    packages=find_packages(),
    setup_requires=['pypandoc>=1'],
    install_requires=['Flask', 'markdown>=2', 'click>=6', 'requests>=2', 'appdirs>=1'],
    entry_points={
            'console_scripts': [
                'githubbot = githubissuesbot.command_line:main',
            ],
    },
    package_data={
            'githubissuesbot': [
                'config/*',
                'templates/*.html'
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

