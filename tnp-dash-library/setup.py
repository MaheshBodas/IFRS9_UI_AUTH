import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tnp_dash_library",
    version="0.1.4",
    author="True North Partners LLP",
    author_email="Stefan.vonBuddenbrock@tnp.eu, David.Brown@tnp.eu",
    description="A boilerplate package for setting up a standardised TNP style dashboard using Dash.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/true-north-partners/tnp-dash-library",
    project_urls={
        "Bug Tracker": "https://github.com/true-north-partners/tnp-dash-library/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
    package_data={'tnp_dash_library': ['assets/*', 'Authentication/templates/*']},
    include_package_data=True
)
