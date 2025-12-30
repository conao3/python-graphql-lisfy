# graphql-lisfy

A Python library for parsing GraphQL syntax and converting it to S-expression (Lisp-style) representations.

## Overview

graphql-lisfy provides a parser that transforms GraphQL queries, mutations, and type definitions into structured S-expressions. This makes GraphQL documents easier to analyze, manipulate, and process programmatically using familiar Lisp-inspired data structures.

## Installation

```bash
pip install graphql-lisfy
```

Or with Poetry:

```bash
poetry add graphql-lisfy
```

## Usage

### Interactive REPL

Launch the interactive shell to experiment with GraphQL parsing:

```bash
graphql-lisfy
```

```
graphql-lisfy> String!
Type_(type_='String', is_list=False, is_non_null=True)
```

### As a Library

```python
from graphql_lisfy import rep

# Parse GraphQL types
result = rep.rep("String!")
print(result)
```

## Features

- Parse GraphQL type definitions including lists and non-null modifiers
- Support for GraphQL values: Int, Float, String, Boolean, Null, Enum, List, Object
- Parse operation definitions (query, mutation, subscription)
- Interactive REPL for quick experimentation
- Built on Pydantic for robust data validation

## Requirements

- Python 3.11 or higher
- pydantic
- more-itertools

## License

Apache-2.0
