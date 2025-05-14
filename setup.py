from setuptools import find_packages, setup

# Always bump the version here for new releases
setup(
    name="format_time_engine",
    version="1.0.1",
    description=(
        "A modular time and calendar engine with customizable ticks, "
        "sun/moon altitude tables, and dynamic parameter propagation."
    ),
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Simon DeFrisco",
    author_email="formatlifeofficial@gmail.com",
    url="https://github.com/ProphetGang/format_time",
    license="MIT",
    python_requires=">=3.12",
    packages=find_packages(exclude=["tests", ".venv", "venv"]),
    install_requires=[
        "numpy",
        "SQLAlchemy",
    ],
    extras_require={
        "geo": [
            "rasterio",
            "scipy",
            "geoPandas",
            "shapely",
            "pyproj",
        ],
        "ui": [
            "PyQt5",
            "matplotlib",
        ],
        "dev": [
            "black",
            "isort",
            "flake8",
            "pre-commit",
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "format_time = time_engine.clock:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
