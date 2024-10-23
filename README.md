# eose-api

Earth Observing Systems Engineering APIs

## Overview

The eose-api project develops common application programming interfaces (APIs) for multiple computational tools that systems engineering analysis for Earth-observing satellite systems. The APIs consist of object models and analysis functions. Object models define data structures. Analysis functions define the inputs (requests) and outputs (responses) to analysis capabilities.


## Installation and Use

This project is packaged per PEP 518 using a `pyproject.toml` configuration file.

To install necessary dependencies and register the `eose` library in your Python environment as an editable library, run:

```shell
pip install -e "."
```

To install necessary dependencies to run certain examples stored in the `docs/examples` directory (excluding OrbitPy and InstruPy examples), run:

```shell
pip install -e ".[examples]"
```

## Documentation

This project includes source code documentation per PEP 257 that can be built with Sphinx.

To install necessary dependencies to build documentation, run:

```shell
pip install -e ".[docs]"
```

Then, from the `docs/` directory, run:

```shell
./make html
```

to build HTML documentation.