# NeLang Syntax Guide

NeLang utilizes standard structural indentation blocks identical to Python syntax. 

## Keywords

| Nepali Keyword | English Equivalent | Description |
| --- | --- | --- |
| `lekha` | `print` | Output to stdout |
| `lina` | `input` | Prompt user for stdin |
| `rakha` | (None) | Syntactic sugar for assignment (e.g. `rakha x = 5`) |
| `yadi` | `if` | Conditional branch |
| `tyasovaye` | `else` | Alternative branch |
| `jaba` | `while` | Loop statement |
| `lagi ... vitra` | `for ... in` | Iterator statement |
| `karya` | `def` | Function declaration |
| `firta` | `return` | Return from function |
| `satya` / `jhuto` | `True` / `False` | Booleans |
| `ra` / `wa` / `hoina` | `and` / `or` / `not` | Logical Operators |
| `lyaau` | `import` | Module loading |

## Standard Library
- `math`: Contains all constants and functions from Python's math layout (`math.pi`, `math.sin()`).
- `string`: Contains specific string mutations (`string.uppercase(val)`, `string.lowercase(val)`, `string.length(val)`).

## Imports
You can import external `.nl` files from the working directory:
```nelang
lyaau my_module
my_module.say_hello()
```
