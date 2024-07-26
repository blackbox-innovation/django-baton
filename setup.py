import os
from setuptools import setup

# Adjust this path if your README.md file is located elsewhere in your fork.
with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# New repository URL
REPO_URL = "https://github.com/blackbox-innovation/django-baton"

setup(
    name="django-baton-alt-theme",
    version="4.1.0.1",
    packages=["baton", "baton.autodiscover", "baton.templatetags"],
    include_package_data=True,
    license="MIT License",
    description="A cool, modern and responsive django admin application with an alternate theme",
    long_description=README,
    long_description_content_type="text/markdown",
    url=REPO_URL,
    author="Krystof Beuermann",
    author_email="krystof@blackbox.ms",
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Topic :: Software Development",
        "Topic :: Software Development :: User Interfaces",
    ],
    project_urls={
        "Documentation": "https://django-baton.readthedocs.io/en/latest/",
        "Demo": "https://django-baton.sqrt64.it/admin",
        "Source": REPO_URL,
        "Tracker": REPO_URL + "/issues",
    },
)
