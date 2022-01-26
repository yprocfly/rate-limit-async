import setuptools
from os import path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()


def read_requirements(filename):
    return [
        line.strip() 
        for line in read_file(filename).splitlines() 
        if not line.startswith('#')
    ]


setuptools.setup(
    name="rate_limit_async",
    version="1.0.1",
    author="Yang Peng",
    author_email="yp_rocfly@foxmail.com",
    description="distributed rate limiter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yprocfly/rate-limit-async",
    keywords=['rate', 'rate-limit', 'limit', 'redis-cell'],
    packages=setuptools.find_packages(),
    install_requires=read_requirements('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
