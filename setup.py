# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

setup (
    name = 'langacore.kit.common',
    version = '0.1.2',
    author = 'LangaCore, Lukasz Langa',
    author_email = 'support@langacore.org, lukasz@langa.pl',
    description = "A library of various simple common routines that keep being " \
                  "rewritten all over again in every project we're working on.",
    long_description = '',
    keywords = '',
    platforms = ['any'],
    license = 'GPL v3', 
    packages = find_packages('src'),
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['langacore', 'langacore.kit'],
    zip_safe = True,
    install_requires = [
        'setuptools',
        ],
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
