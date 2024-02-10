import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='gando',
    author='Hydra',
    author_email='navidsoleymani@ymail.com',
    description="A framework based on Django that has tried to gather together the tools "
                "needed in the process of creating a large project.",
    keywords='django',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/horinsoftwaregroup/gando.git',
    project_urls={
        'Documentation': 'https://github.com/horinsoftwaregroup/gando.git',
        'Bug Reports':
            'https://github.com/horinsoftwaregroup/gando.git/issues',
        'Source Code': 'https://github.com/horinsoftwaregroup/gando.git',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Framework :: Django :: 4.2',
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'Django',
        'pydantic',
        'djangorestframework',
        'markdown',
        'django-filter',
        'django-simple-history',
        'Pillow',
        'httpx',
    ],
)
