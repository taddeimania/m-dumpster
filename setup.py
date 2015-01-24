from setuptools import setup, find_packages


def readme():
    try:
        return open('README.md').read()
    except:
        pass
    return ''


setup(
    name='m-dumpster',
    version='0.0.1',
    author="Joel Taddei @taddeimania",
    author_email="jtaddei@gmail.com",
    description="Export your related MySQL data to .sql files",
    long_description=readme(),
    url='http://github.com/taddeimania/m-dumpster',
    packages=find_packages(),
    test_suite="nose.collector",
    entry_points={
        'console_scripts': {
            "dumpster = dumpster.scripts:main",
        },
    },
)
