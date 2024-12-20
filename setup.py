from setuptools import setup, find_packages

setup(
    name="srt_translator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'srt-translator=srt_translator.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to translate SRT subtitle files using Azure Translator",
    keywords="srt, translation, azure, subtitles",
    python_requires=">=3.6",
) 