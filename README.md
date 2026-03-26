# NeLang

<p align="center">
  <img src="NavLogo.png" alt="NeLang Logo" width="200"/>
</p>

> Python-like syntax. Nepali-inspired logic.

NeLang is a statically designed Python transpiler and custom AST runner utilizing Nepali-centric keywords and familiar Pythonic formatting. It embraces Python's beautiful indentation-based formatting rules while injecting localized cultural terminologies.

NeLang exists to bridge modern language capabilities to Nepali syntax readers—perfect for localized logic mapping, education, and general-purpose development applications.

## Features

- **Nepali-inspired Keywords**: Syntax mapped cleanly against translated logical components for cultural clarity.
- **Python-like Syntax**: Drop braces and semi-colons. Maintain visual uniformity through strict structural indentation checks.
- **Easy to Learn**: Built extensively focusing on the simplest AST paths, reducing onboarding cognitive load globally.
- **Native Bytecode Compilation**: Executes securely over `ast.Module` configurations mirroring Python C speed.
- **Built-in Standard Library**: Integrates underlying math and string capabilities implicitly.

## Installation

You can install NeLang locally via pip.

1. Clone the repository:
```bash
git clone https://github.com/ompandey07/Nelang.git
cd Nelang
```

2. Install the package locally:
```bash
pip install -e .
```

## Usage

To execute a NeLang script, use the `run` command followed by the `.nl` file.

```bash
nelang run filename.nl
```

## Syntax Overview

### Variables
Variables in NeLang are dynamically typed and can be assigned directly.

```py
name = "Sagarmatha"
x = 10
```

### Print (`lekha`)
Outputs data to the standard console.

```py
lekha("Hello, World!")
lekha("Value is:", x)
```

### Conditionals (`yadi` / `tyasovaye`)
Conditional blocks using standard indentation.

```py
yadi x > 5:
    lekha("Thulo")
tyasovaye:
    lekha("Sano")
```

### Loops (`jaba`)
Standard `while` loop bounds.

```py
x = 0
jaba x < 5:
    lekha(x)
    x = x + 1
```

### Functions (`karya`)
Define closures implicitly capturing scoped arguments.

```py
karya greet(name):
    lekha("Namaste", name)
```

### Return (`firta`)
Escapes active functional closures resolving back to the caller.

```py
karya multiply(a, b):
    firta a * b
```

### Boolean (`satya` / `jhuto`)
Literal semantic truth states mapping to True and False.

```py
is_valid = satya
has_failed = jhuto
```

### Logical (`ra` / `wa` / `hoina`)
Logical connectors enabling chain evaluations (and, or, not).

```py
yadi satya ra hoina jhuto:
    lekha("Logic works!")
```

### Lists
Standard contiguous collections.

```py
nums = [1, 2, 3]
```

### For Loop (`lagi ... vitra`)
Iterate securely over sequence collections.

```py
lagi x vitra nums:
    lekha(x)
```

### Input (`lina`)
Polls raw standard inputs for user string data.

```py
name = lina("Enter name: ")
```

### Comments
Ignores lexical structures from the execution tree.

```py
# yo comment ho
lekha("Executing...")
```

## Code Examples

### Hello World
```py
karya main():
    lekha("Namaste, World!")

main()
```

### Loop Example
```py
nums = [10, 20, 30]
lagi number vitra nums:
    lekha("Item:", number)
```

### Function Example
```py
karya calculate_area(width, height):
    firta width * height

lekha("Area:", calculate_area(5, 10))
```

### Combined Example
```py
lyaau math

karya compute_circle(radius):
    yadi radius <= 0:
        lekha("Invalid radius")
        firta 0
    tyasovaye:
        firta math.pi * math.pow(radius, 2)

r = 5
lekha("Area:", compute_circle(r))
```

## CLI Commands

The `nelang` command-line utility supports structural subcommands to assist debugging and execution.

- `nelang run file.nl` - Executes a NeLang script natively caching the AST bytecode into memory. Include `--debug` for tokenized logging mapping.
- `nelang version` - Exposes the locally bounded framework version globally registered.
- `nelang help` - Renders the integrated helpful manual listing explicitly available tools.

## Project Structure

```text
nelang/
├── nelang/
│   ├── ast_nodes.py      # Abstract tree hierarchical mapping
│   ├── compiler.py       # Custom Native Bytecode generator
│   ├── errors.py         # Standardized exception bounds
│   ├── interpreter.py    # Runtime execution mapping
│   ├── lexer.py          # Sequence filtering
│   └── parser.py         # Recursive descent logic tracking
├── vscode-nelang/        # VS Code syntax highlighting extension
├── docs/                 # Documentation references
├── setup.py              # Packaging distributions
└── README.md             # Project definition layout
```

## Roadmap

- Implement Classes and Object Instantiation mechanisms.
- Standardize extensible module registry layout definitions.
- Set up an official remote Package Manager pipeline infrastructure.
- Expand standard library built-ins for explicit HTTP processing.

## Contributing

Contributions to NeLang are highly encouraged! When integrating, please follow our structural indentation standards securely. Make sure tests pass prior to submitting PR configurations bounding into the AST parsers cleanly.

To get started:
1. Fork the repository.
2. Create a structural hotfix branch: `git checkout -b feature/new-syntax`
3. Commit optimizations.
4. Push and submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
