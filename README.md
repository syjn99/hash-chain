# Hash Chain

## Prerequisite

- Python (>= 3.9)

## Execute the program

```bash
python3 main.py -h
```

```
usage: main.py [-h] {analyze,cycle,check,collision} ...

MD5 Hash Chain Analyzer

positional arguments:
  {analyze,cycle,check,collision}
    analyze             Analyze hash graph (4-a)
    cycle               Find cycle in hash function (4-d)
    check               Check if cycle prints valid output
    collision           Find hash collision (4-e)

optional arguments:
  -h, --help            show this help message and exit
```

### Analyze (Problem 4-a)

```bash
python3 main.py analyze --k 16
```

```
Run analysis for k=16
==== Result of analysis ====
Number of components: 5
Average of tail length: 105.53507827383417
Max of tail length: 257
Min of cycle length: 4
Average of cycle length: 69.8
Max of cycle length: 242
```

### Cycle (Problem 4-d)

```bash
python3 main.py cycle --k 64
```

### Collision (Problem 4-e)

```bash
python3 main.py collision --k 64
```