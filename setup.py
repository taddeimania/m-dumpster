from setuptools import setup, find_packages


def readme():
    try:
        return open('README.md').read()
    except:
        pass
    return ''


setup(
    name='MySQL Field Dumper (MDumpster)',
    version='0.0.1',
    author="Joel Taddei @taddeimania",
    author_email="jtaddei@gmail.com",
    description="Export your related MySQL data to .sql files",
    long_description=readme(),
    url='http://github.com/taddeimania/mdumpster',
    packages=find_packages(),
    setup_requires=['nose', 'mock'],
    test_suite="nose.collector",
    entry_points={
        'console_scripts': {
            "dumpster = dumpster.scripts:main",
        },
    },
)
