# COMP9020 Math Cheat Sheet

## Number Theory

### Floor, Ceiling, Absolute Value
- Floor: ⌊x⌋
- Ceiling: ⌈x⌉
- Absolute: |x|

### Divisibility, GCD, LCM
- m | n ⇔ ∃k ∈ Z, n = km
- GCD(m,n) * LCM(m,n) = |m| * |n|

### Modular Arithmetic
- m div n = ⌊m/n⌋
- m % n = m - n⌊m/n⌋
- m ≡(n) p ⇔ n | (m - p)

### Euclidean Algorithm
GCD(m,n) = {
  m if n = 0
  n if m = 0
  GCD(n, m % n) if m > n > 0
}

## Set Theory

### Set Operations
- Union: A ∪ B = {x | x ∈ A ∨ x ∈ B}
- Intersection: A ∩ B = {x | x ∈ A ∧ x ∈ B}
- Complement: A^c = {x ∈ U | x ∉ A}
- Difference: A \ B = {x | x ∈ A ∧ x ∉ B}
- Symmetric Difference: A ⊕ B = (A \ B) ∪ (B \ A)

### Power Sets, Cardinality
- Pow(A) = {X | X ⊆ A}
- |Pow(A)| = 2^|A|
- A × B = {(a, b) | a ∈ A, b ∈ B}

### Set Laws
- A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)
- A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)
- (A ∪ B)^c = A^c ∩ B^c
- (A ∩ B)^c = A^c ∪ B^c

## Formal Languages

- Σ: alphabet
- λ: empty word
- Σ*: all finite words
- Language: L ⊆ Σ*

### Operations
- Concatenation: AB = {ab | a ∈ A, b ∈ B}
- Kleene Star: A* = ⋃(n≥0) A^n

## Relations

### Binary Relation
R ⊆ A × B

### Properties (R ⊆ A × A)
- Reflexive: ∀a ∈ A, (a, a) ∈ R
- Antireflexive: ∀a ∈ A, (a, a) ∉ R
- Symmetric: (a, b) ∈ R ⇒ (b, a) ∈ R
- Antisymmetric: (a, b) ∈ R ∧ (b, a) ∈ R ⇒ a = b
- Transitive: (a, b) ∈ R ∧ (b, c) ∈ R ⇒ (a, c) ∈ R

### Equivalence Relation
R is reflexive, symmetric, and transitive
[a] = {b ∈ A | a R b}

### Partial Order
≤ is reflexive, antisymmetric, and transitive

- Minimal: a ∈ A, ∄b ∈ A (b < a)
- Minimum: a ∈ A, ∀b ∈ A (a ≤ b)
- Maximal: a ∈ A, ∄b ∈ A (a < b)
- Maximum: a ∈ A, ∀b ∈ A (b ≤ a)

- Upper bound of B ⊆ A: u ∈ A, ∀b ∈ B (b ≤ u)
- Least upper bound (lub): min{u | u is upper bound of B}
- Lower bound of B ⊆ A: l ∈ A, ∀b ∈ B (l ≤ b)
- Greatest lower bound (glb): max{l | l is lower bound of B}

Lattice: Each pair has lub and glb
