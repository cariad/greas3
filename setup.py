from pathlib import Path

from setuptools import setup

from greas3 import __version__

readme_path = Path(__file__).parent / "README.md"

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Typing :: Typed",
]

if "a" in __version__:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in __version__:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@cariad.earth",
    classifiers=classifiers,
    description="Synchronises S3 buckets with local directories",
    include_package_data=True,
    install_requires=[
        "boto3~=1.0",
        "cline~=1.0",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="greas3",
    packages=[
        "greas3",
        "greas3.cli",
    ],
    package_data={
        "greas3": ["py.typed"],
        "greas3.cli": ["py.typed"],
    },
    python_requires=">=3.9",
    url="https://github.com/cariad/greas3",
    version=__version__,
)
