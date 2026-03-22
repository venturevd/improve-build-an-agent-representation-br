from setuptools import setup, find_packages

setup(
    name="agent-representation-broker-test",
    version="0.1.0",
    description="Improved test script for the Agent Representation Broker with port conflict handling",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "flask",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            'agent-broker-test=test_api:test_api',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)