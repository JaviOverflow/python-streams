# Python Streams

## Motivation
Python has always lacked a modern rich functional streams API over lists, maps and tuples. Some attempts have been done such as [PyFunctional](https://github.com/EntilZha/PyFunctional), but after being users of those libraries for a some times, we felt the lack of some core features that are hard to add without a redesign of the whole library.

## Guidelines
- Support for latest typing Python 3.6+ features.
- Implement methods from already successful streams API such as the ones already existing in modern languages as Kotlin or Swift. Rich operators suit is always best than poor due to the lack of function extension in Python.
- Support for multiple argument lambdas in order to handle streams of tuples.
- Concurrency design when possible such in operations as map or filter.
