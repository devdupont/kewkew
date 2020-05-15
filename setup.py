"""
kewkew Package Setup
"""

from setuptools import setup

setup(
    name="kewkew",
    version="0.1.0",
    description="A tiny queue library leveraging asyncio",
    url="https://github.com/flyinactor91/kewkew",
    author="Michael duPont",
    author_email="michael@mdupont.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">= 3.7",
    py_modules=["kewkew"],
)
