from distutils.core import setup

setup(
    name='dirlistgen',
    packages=['dirlistgen'],
    version='1.0.1',
    description=' A minimal representation of the inclusion/exclusion list of directories',
    long_description='''
    This program can efficiently include and exclude directories from a directory tree,
    producing a minimal representation of the resulting inclusion/exclusion list.
    It can be used in a variety of scenarios including, but not limited to,
    music/video/other material sharing and library management.''',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Users",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: MIT License"
    ],
     author='Anastasiia Korobka',
    author_email='anastasiiakora205@gmail.com',
    url='https://github.com/boxgirl/dirlistgen'
)
