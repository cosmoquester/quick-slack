from setuptools import find_packages, setup

setup(
    name="quick-slack",
    version="0.0.1",
    description="CLI tool to send message to mornitor status, notify process end, etc by slack.",
    python_requires=">=3.7",
    install_requires=["click", "requests"],
    url="https://github.com/psj8252/quick-slack.git",
    author="Park Sangjun",
    packages=find_packages(exclude=["tests"]),
)
