from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="quick-slack",
    version="0.0.1",
    description="CLI tool to send message to mornitor status, notify process end, etc by slack.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=["click", "requests", "psutil"],
    url="https://github.com/psj8252/quick-slack.git",
    author="Park Sangjun",
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": ["qslack = quick_slack.cli:qslack"]},
    package_data={"quick_slack": ["config.json"]},
    keywords=["slack", "message"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities",
    ],
)
