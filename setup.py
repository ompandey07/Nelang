from setuptools import setup, find_packages

setup(
    name="nelang",
    version="0.2.0",
    description="A programming language interpreter with Nepali keywords.",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "nelang=nelang.__main__:main",
        ]
    },
)
