#!/usr/bin/env python3
"""Laptop-scale search for an effective Rowley (5,5,3) template.

This is a search program, not an independent verifier.  Its acceptance oracle
does nevertheless test the full repeated-distance condition on vertices
0,...,repeat_span.  Any emitted candidate remains provisional until the two
independent project verifiers accept it.

The key implementation device is lazy exact separation.  A monochromatic K_5
on five integer positions gives a valid constraint on the (periodic) distance
colour variables.  We keep only constraints actually exposed by the exact
bitset oracle, score their violation incidences incrementally during local
search, and ask the oracle for more constraints whenever the current database
is satisfied.  Thus memory usage depends on the hard boundary encountered by
the search rather than on the roughly millions of a-priori K_5 constraints.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator, Sequence


RED = 0
BLUE = 1
TEMPLATE = 2
COLOR_CHARS = "123"


@dataclasses.dataclass(frozen=True)
class Candidate:
    order: int
    phi_min: int
    repeat_span: int
    colors: tuple[int, ...]

    @property
    def period(self) -> int:
        return self.order - 1


def read_candidate(path: Path) -> Candidate:
    """Read the deliberately tiny, strict project candidate format."""
    fields: dict[str, str] = {}
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2 or parts[0] not in {
            "order",
            "phi_min",
            "repeat_span",
            "colors",
        }:
            raise ValueError(f"{path}:{line_number}: malformed candidate line")
        key, value = parts
        if key in fields:
            raise ValueError(f"{path}:{line_number}: duplicate key {key}")
        fields[key] = value
    missing = {"order", "phi_min", "repeat_span", "colors"} - fields.keys()
    if missing:
        raise ValueError(f"{path}: missing keys: {sorted(missing)}")
    order = int(fields["order"])
    phi_min = int(fields["phi_min"])
    repeat_span = int(fields["repeat_span"])
    word = fields["colors"]
    if order < 2 or len(word) != order - 1 or any(ch not in COLOR_CHARS for ch in word):
        raise ValueError(f"{path}: invalid colour word for order {order}")
    return Candidate(
        order=order,
        phi_min=phi_min,
        repeat_span=repeat_span,
        colors=tuple(COLOR_CHARS.index(ch) for ch in word),
    )


def write_candidate(path: Path, candidate: Candidate, comment: str) -> None:
    word = "".join(COLOR_CHARS[color] for color in candidate.colors)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# PROVISIONAL search output: {comment}\n"
        "# Must pass both independent project verifiers before use.\n"
        f"order {candidate.order}\n"
        f"phi_min {candidate.phi_min}\n"
        f"repeat_span {candidate.repeat_span}\n"
        f"colors {word}\n",
        encoding="ascii",
    )


@dataclasses.dataclass(frozen=True)
class Partition:
    """A partition of distance variables into search units."""

    period: int
    units: tuple[tuple[int, ...], ...]  # zero-based distance indices
    variable_to_unit: tuple[int, ...]
    allowed: tuple[tuple[int, ...], ...]

    @classmethod
    def build(cls, period: int, phi_min: int, symmetry: str) -> "Partition":
        if not 0 <= phi_min < period:
            raise ValueError("phi_min must be in [0, period)")

        if symmetry == "none":
            raw_units = [(index,) for index in range(period)]
        elif symmetry == "reflection":
            # Reflection is d <-> period-d for 1 <= d < period.  The distance
            # period itself is a singleton and is forced to template colour.
            seen: set[int] = set()
            raw_units: list[tuple[int, ...]] = []
            for distance in range(1, period):
                if distance in seen:
                    continue
                mate = period - distance
                orbit = tuple(sorted({distance - 1, mate - 1}))
                raw_units.append(orbit)
                seen.add(distance)
                seen.add(mate)
            raw_units.append((period - 1,))
        else:
            raise ValueError(f"unknown symmetry {symmetry!r}")

        variable_to_unit = [-1] * period
        allowed_units: list[tuple[int, ...]] = []
        for unit_id, unit in enumerate(raw_units):
            allowed = {RED, BLUE, TEMPLATE}
            for index in unit:
                distance = index + 1
                if distance <= phi_min:
                    allowed.discard(TEMPLATE)
                if distance == period:
                    allowed.intersection_update({TEMPLATE})
                variable_to_unit[index] = unit_id
            if not allowed:
                raise ValueError(
                    f"symmetry orbit {unit} conflicts with phi/template constraints"
                )
            allowed_units.append(tuple(sorted(allowed)))
        if any(unit < 0 for unit in variable_to_unit):
            raise AssertionError("partition omitted a distance variable")
        return cls(
            period=period,
            units=tuple(raw_units),
            variable_to_unit=tuple(variable_to_unit),
            allowed=tuple(allowed_units),
        )

    @classmethod
    def rowley_t12(
        cls,
        period: int,
        phi_min: int,
        published_seed_colors: Sequence[int],
    ) -> "Partition":
        """The natural twelve-variable Rowley extension subclass.

        For the specific order-94 attack this fixes distances 1..40 to the
        published order-93 seed, fixes 41, 54..80, and 93 to template colour,
        and identifies d with 134-d for d=42,...,53.  The twelve pair-orbits
        are the only mutable units.
        """
        if period != 93 or phi_min != 40 or len(published_seed_colors) != 92:
            raise ValueError(
                "rowley-t12 requires target period 93, phi_min 40, "
                "and the order-93 (period-92) seed"
            )
        unit_specs: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
        covered: set[int] = set()

        def add(distances: Iterable[int], allowed: Iterable[int]) -> None:
            indices = tuple(sorted(distance - 1 for distance in distances))
            if any(index in covered for index in indices):
                raise AssertionError("overlapping rowley-t12 unit")
            covered.update(indices)
            unit_specs.append((indices, tuple(sorted(set(allowed)))))

        for distance in range(1, 41):
            add((distance,), (published_seed_colors[distance - 1],))
        add((41,), (TEMPLATE,))
        for distance in range(42, 54):
            add((distance, 134 - distance), (RED, BLUE, TEMPLATE))
        for distance in range(54, 81):
            add((distance,), (TEMPLATE,))
        add((93,), (TEMPLATE,))
        if covered != set(range(period)):
            raise AssertionError(
                f"rowley-t12 coverage error: missing {sorted(set(range(period)) - covered)}"
            )

        variable_to_unit = [-1] * period
        for unit_id, (unit, _) in enumerate(unit_specs):
            for index in unit:
                variable_to_unit[index] = unit_id
        return cls(
            period=period,
            units=tuple(unit for unit, _ in unit_specs),
            variable_to_unit=tuple(variable_to_unit),
            allowed=tuple(allowed for _, allowed in unit_specs),
        )

    def expand(self, unit_colors: Sequence[int]) -> tuple[int, ...]:
        if len(unit_colors) != len(self.units):
            raise ValueError("wrong number of unit colours")
        return tuple(unit_colors[self.variable_to_unit[index]] for index in range(self.period))

    def project(
        self, distance_colors: Sequence[int], rng: random.Random
    ) -> list[int]:
        if len(distance_colors) != self.period:
            raise ValueError("wrong number of distance colours")
        result: list[int] = []
        for unit, allowed in zip(self.units, self.allowed):
            counts = Counter(distance_colors[index] for index in unit)
            best_count = max(counts.get(color, 0) for color in allowed)
            best = [color for color in allowed if counts.get(color, 0) == best_count]
            result.append(rng.choice(best))
        return result


@dataclasses.dataclass(frozen=True)
class Clause:
    forbidden_color: int
    units: tuple[int, ...]
    origin: str
    witness: tuple[int, ...] | None


class ClauseDatabase:
    """Constraint store with unit-level incidence lists."""

    def __init__(self, partition: Partition):
        self.partition = partition
        self.clauses: list[Clause] = []
        self.incident: list[list[int]] = [[] for _ in partition.units]
        self._keys: set[tuple[int, tuple[int, ...]]] = set()
        self.origin_counts: Counter[str] = Counter()

    def add(
        self,
        forbidden_color: int,
        distance_indices: Iterable[int],
        origin: str,
        witness: Sequence[int] | None = None,
    ) -> bool:
        units = tuple(
            sorted(
                {
                    self.partition.variable_to_unit[index]
                    for index in distance_indices
                }
            )
        )
        if not units:
            raise ValueError("empty forbidden-colour clause")
        key = (forbidden_color, units)
        if key in self._keys:
            return False
        clause_id = len(self.clauses)
        clause = Clause(
            forbidden_color=forbidden_color,
            units=units,
            origin=origin,
            witness=None if witness is None else tuple(witness),
        )
        self._keys.add(key)
        self.clauses.append(clause)
        for unit in units:
            self.incident[unit].append(clause_id)
        self.origin_counts[origin] += 1
        return True

    def contains(self, forbidden_color: int, units: tuple[int, ...]) -> bool:
        return (forbidden_color, units) in self._keys

    def violated(self, clause_id: int, unit_colors: Sequence[int]) -> bool:
        clause = self.clauses[clause_id]
        return all(unit_colors[unit] == clause.forbidden_color for unit in clause.units)

    def score(self, unit_colors: Sequence[int]) -> int:
        return sum(
            self.violated(clause_id, unit_colors)
            for clause_id in range(len(self.clauses))
        )

    def add_all_sum_free_constraints(self) -> None:
        p = self.partition.period
        for a in range(1, p + 1):
            for b in range(a, p + 1 - a):
                total = a + b
                self.add(
                    TEMPLATE,
                    (a - 1, b - 1, total - 1),
                    origin="sum",
                    witness=(a, b, total),
                )


class SearchState:
    """A colouring plus an exactly maintained violated-clause set."""

    def __init__(
        self, database: ClauseDatabase, unit_colors: Sequence[int]
    ) -> None:
        self.database = database
        self.unit_colors = list(unit_colors)
        self.violated: set[int] = {
            clause_id
            for clause_id in range(len(database.clauses))
            if database.violated(clause_id, self.unit_colors)
        }

    @property
    def score(self) -> int:
        return len(self.violated)

    def refresh_new_clauses(self, first_new_clause: int) -> None:
        for clause_id in range(first_new_clause, len(self.database.clauses)):
            if self.database.violated(clause_id, self.unit_colors):
                self.violated.add(clause_id)

    def delta_if(self, unit: int, new_color: int) -> int:
        old_color = self.unit_colors[unit]
        if new_color == old_color:
            return 0
        delta = 0
        self.unit_colors[unit] = new_color
        for clause_id in self.database.incident[unit]:
            was = clause_id in self.violated
            now = self.database.violated(clause_id, self.unit_colors)
            delta += int(now) - int(was)
        self.unit_colors[unit] = old_color
        return delta

    def recolor(self, unit: int, new_color: int) -> int:
        old_score = self.score
        self.unit_colors[unit] = new_color
        for clause_id in self.database.incident[unit]:
            if self.database.violated(clause_id, self.unit_colors):
                self.violated.add(clause_id)
            else:
                self.violated.discard(clause_id)
        return self.score - old_score


class RepeatedCliqueOracle:
    """Exact K_5 separator for periodic distance colourings.

    Translation invariance lets us anchor the least vertex of any violating
    clique at zero.  We therefore search for a K_4 inside the target-colour
    neighbours of zero, using Python integer bitsets for exact intersections.
    """

    def __init__(self, period: int, repeat_span: int):
        if period < 1 or repeat_span < 1:
            raise ValueError("positive period and repeat span required")
        self.period = period
        self.repeat_span = repeat_span

    def _residue_index(self, positive_distance: int) -> int:
        return (positive_distance - 1) % self.period

    def _higher_adjacency(
        self, distance_colors: Sequence[int], target_color: int
    ) -> list[int]:
        n = self.repeat_span + 1
        adjacency = [0] * n
        for left in range(n):
            mask = 0
            for right in range(left + 1, n):
                if (
                    distance_colors[self._residue_index(right - left)]
                    == target_color
                ):
                    mask |= 1 << right
            adjacency[left] = mask
        return adjacency

    def _directed_residue_adjacency(
        self, distance_colors: Sequence[int], target_color: int
    ) -> list[int]:
        """Return target-colour out-neighbours on Z/period Z.

        The arc u -> v receives the colour of the positive modular difference
        v-u in {1,...,period-1}.  Self differences are excluded: in the repeated
        integer graph they are positive multiples of the period and receive the
        forced template colour.
        """
        adjacency = [0] * self.period
        for left in range(self.period):
            mask = 0
            for right in range(self.period):
                if right == left:
                    continue
                difference = (right - left) % self.period
                if distance_colors[difference - 1] == target_color:
                    mask |= 1 << right
            adjacency[left] = mask
        return adjacency

    def _lift_residue_word(self, residues: Sequence[int]) -> tuple[int, ...]:
        """Lift an ordered residue word to increasing integer positions."""
        positions = [0]
        for previous, current in zip(residues, residues[1:]):
            gap = (current - previous) % self.period
            if gap == 0:
                raise AssertionError("residue word must have distinct consecutive terms")
            positions.append(positions[-1] + gap)
        if positions[-1] > self.repeat_span:
            raise AssertionError("residue lift exceeds certified repetition span")
        return tuple(positions)

    def _iter_residue_cliques(
        self, distance_colors: Sequence[int], target_color: int
    ) -> Iterator[tuple[int, int, int, int, int]]:
        """Enumerate ordered monochromatic K_5s in the residue relation.

        If repeat_span >= 4(period-1), this is equivalent to the full repeated
        integer-line condition.  Translation puts the first residue at zero.
        Each later residue must lie in the common target-colour out-neighbourhood
        of all earlier residues.  Conversely, lift consecutive residues by their
        least positive modular gaps; the resulting four gaps total at most
        4(period-1), so every residue witness is realised inside the tested span.
        """
        adjacency = self._directed_residue_adjacency(distance_colors, target_color)

        def extend(
            chosen: tuple[int, ...], candidates: int, needed: int
        ) -> Iterator[tuple[int, int, int, int, int]]:
            if needed == 0:
                residues = (0,) + chosen
                yield self._lift_residue_word(residues)
                return
            choices = candidates
            while choices:
                lowest_bit = choices & -choices
                vertex = lowest_bit.bit_length() - 1
                choices ^= lowest_bit
                # Numeric residue order is irrelevant: choosing u then v and
                # choosing v then u impose different directed differences.
                remaining = (candidates ^ lowest_bit) & adjacency[vertex]
                if remaining.bit_count() >= needed - 1:
                    yield from extend(chosen + (vertex,), remaining, needed - 1)

        yield from extend((), adjacency[0], 4)

    def _iter_interval_cliques(
        self, distance_colors: Sequence[int], target_color: int
    ) -> Iterator[tuple[int, int, int, int, int]]:
        adjacency = self._higher_adjacency(distance_colors, target_color)

        def extend(
            chosen: tuple[int, ...], candidates: int, needed: int
        ) -> Iterator[tuple[int, int, int, int, int]]:
            if needed == 0:
                yield (0, chosen[0], chosen[1], chosen[2], chosen[3])
                return
            while candidates.bit_count() >= needed:
                lowest_bit = candidates & -candidates
                vertex = lowest_bit.bit_length() - 1
                candidates ^= lowest_bit
                yield from extend(
                    chosen + (vertex,),
                    candidates & adjacency[vertex],
                    needed - 1,
                )

        yield from extend((), adjacency[0], 4)

    def iter_cliques(
        self, distance_colors: Sequence[int], target_color: int
    ) -> Iterator[tuple[int, int, int, int, int]]:
        if self.repeat_span >= 4 * (self.period - 1):
            yield from self._iter_residue_cliques(distance_colors, target_color)
            return

        # Fallback for deliberately small test spans where not every ordered
        # residue pattern is guaranteed to have a lift inside the interval.
        yield from self._iter_interval_cliques(distance_colors, target_color)

    def clause_distances(self, clique: Sequence[int]) -> tuple[int, ...]:
        indices = {
            self._residue_index(clique[j] - clique[i])
            for i in range(5)
            for j in range(i + 1, 5)
        }
        return tuple(sorted(indices))

    def find_first(
        self, distance_colors: Sequence[int], target_color: int
    ) -> tuple[int, int, int, int, int] | None:
        return next(self.iter_cliques(distance_colors, target_color), None)

    def separate(
        self,
        distance_colors: Sequence[int],
        database: ClauseDatabase,
        limit_new_per_color: int,
        max_examined_per_color: int,
    ) -> dict[int, dict[str, int | tuple[int, ...] | None]]:
        report: dict[int, dict[str, int | tuple[int, ...] | None]] = {}
        for target in (RED, BLUE):
            added = 0
            examined = 0
            first_witness: tuple[int, ...] | None = None
            for clique in self.iter_cliques(distance_colors, target):
                examined += 1
                if first_witness is None:
                    first_witness = clique
                if database.add(
                    target,
                    self.clause_distances(clique),
                    origin=f"k5-{COLOR_CHARS[target]}",
                    witness=clique,
                ):
                    added += 1
                    if added >= limit_new_per_color:
                        break
                if examined >= max_examined_per_color:
                    break
            report[target] = {
                "added": added,
                "examined": examined,
                "first_witness": first_witness,
            }
        return report

    def exact_report(self, distance_colors: Sequence[int]) -> dict[str, object]:
        witnesses = {
            COLOR_CHARS[target]: self.find_first(distance_colors, target)
            for target in (RED, BLUE)
        }
        return {
            "red_k5": witnesses["1"],
            "blue_k5": witnesses["2"],
            "repeated_k5_free": all(value is None for value in witnesses.values()),
        }


def sum_free_witness(distance_colors: Sequence[int]) -> tuple[int, int, int] | None:
    p = len(distance_colors)
    for a in range(1, p + 1):
        if distance_colors[a - 1] != TEMPLATE:
            continue
        for b in range(a, p + 1 - a):
            total = a + b
            if (
                distance_colors[b - 1] == TEMPLATE
                and distance_colors[total - 1] == TEMPLATE
            ):
                return (a, b, total)
    return None


def basic_report(
    distance_colors: Sequence[int], phi_min: int
) -> dict[str, object]:
    p = len(distance_colors)
    low_template = next(
        (distance for distance in range(1, p + 1) if distance_colors[distance - 1] == TEMPLATE),
        None,
    )
    return {
        "period_template": distance_colors[-1] == TEMPLATE,
        "low_template": low_template,
        "phi_at_least_required": low_template is not None and low_template - 1 >= phi_min,
        "sum_witness": sum_free_witness(distance_colors),
    }


def lift_seed_words(
    seed: Candidate,
    target_period: int,
    phi_min: int,
    rng: random.Random,
) -> list[tuple[int, ...]]:
    """Generate all one-position lifts, plus colour-swapped variants."""
    if seed.period == target_period:
        base_words = [seed.colors]
    elif seed.period + 1 == target_period:
        base_words = []
        old = list(seed.colors)
        for insertion in range(target_period):
            allowed = [RED, BLUE] if insertion + 1 <= phi_min else [RED, BLUE, TEMPLATE]
            if insertion == target_period - 1:
                allowed = [TEMPLATE]
            for inserted_color in allowed:
                word = tuple(old[:insertion] + [inserted_color] + old[insertion:])
                if word[-1] == TEMPLATE:
                    base_words.append(word)
    else:
        raise ValueError(
            f"seed period {seed.period} is not target period {target_period} or one less"
        )

    unique: dict[tuple[int, ...], None] = {}
    for word in base_words:
        unique[word] = None
        unique[
            tuple(
                BLUE if color == RED else RED if color == BLUE else TEMPLATE
                for color in word
            )
        ] = None
    words = list(unique)
    rng.shuffle(words)
    return words


def partition_from_args(args: argparse.Namespace) -> Partition:
    if args.symmetry == "rowley-t12":
        if args.seed is None:
            raise ValueError("--symmetry rowley-t12 requires --seed")
        seed = read_candidate(args.seed)
        return Partition.rowley_t12(
            args.order - 1,
            args.phi_min,
            seed.colors,
        )
    return Partition.build(args.order - 1, args.phi_min, args.symmetry)


def random_assignment(partition: Partition, rng: random.Random) -> list[int]:
    assignment: list[int] = []
    for allowed in partition.allowed:
        if len(allowed) == 3:
            # Template colour is useful but too much of it quickly violates
            # sum-freeness; bias the initial distribution toward the K_5 colours.
            assignment.append(rng.choices(allowed, weights=(5, 5, 2), k=1)[0])
        else:
            assignment.append(rng.choice(allowed))
    return assignment


@dataclasses.dataclass(frozen=True)
class FullProfile:
    """The exact set of constraints violated by one colouring."""

    clauses: frozenset[tuple[int, tuple[int, ...]]]
    raw_k5_witnesses: int
    truncated: bool

    @property
    def score(self) -> int:
        if self.truncated:
            return 1_000_000_000 + self.raw_k5_witnesses
        return len(self.clauses)

    def objective(self, sum_weight: int) -> int:
        if self.truncated:
            return self.score
        sum_defects = sum(
            forbidden == TEMPLATE for forbidden, _ in self.clauses
        )
        return self.score + (sum_weight - 1) * sum_defects


def full_violation_profile(
    distance_colors: Sequence[int],
    partition: Partition,
    oracle: RepeatedCliqueOracle,
    raw_k5_cap: int,
) -> FullProfile:
    """Enumerate all currently violated residue constraints, deduplicated.

    Near the Rowley seed this is much smaller than the global constraint
    universe.  ``truncated`` is explicit and receives an overwhelming penalty;
    a truncated profile is never a success and is never reported as exact.
    """
    clauses: set[tuple[int, tuple[int, ...]]] = set()
    p = len(distance_colors)
    for a in range(1, p + 1):
        if distance_colors[a - 1] != TEMPLATE:
            continue
        for b in range(a, p + 1 - a):
            total = a + b
            if (
                distance_colors[b - 1] == TEMPLATE
                and distance_colors[total - 1] == TEMPLATE
            ):
                units = tuple(
                    sorted(
                        {
                            partition.variable_to_unit[a - 1],
                            partition.variable_to_unit[b - 1],
                            partition.variable_to_unit[total - 1],
                        }
                    )
                )
                clauses.add((TEMPLATE, units))

    raw = 0
    for target in (RED, BLUE):
        for clique in oracle.iter_cliques(distance_colors, target):
            raw += 1
            indices = oracle.clause_distances(clique)
            units = tuple(
                sorted({partition.variable_to_unit[index] for index in indices})
            )
            clauses.add((target, units))
            if raw >= raw_k5_cap:
                return FullProfile(frozenset(clauses), raw, True)
    return FullProfile(frozenset(clauses), raw, False)


def repair_sum_constraints(
    assignment: Sequence[int],
    partition: Partition,
    rng: random.Random,
    steps: int = 20000,
) -> list[int] | None:
    database = ClauseDatabase(partition)
    database.add_all_sum_free_constraints()
    state = SearchState(database, assignment)
    anneal(
        state,
        partition,
        rng,
        steps=steps,
        noise=0.12,
        start_temperature=0.8,
        end_temperature=0.01,
    )
    return state.unit_colors if state.score == 0 else None


def run_direct_search(args: argparse.Namespace) -> int:
    """Exact near-seed min-conflicts with full live-profile recomputation."""
    rng = random.Random(args.random_seed)
    partition = partition_from_args(args)
    oracle = RepeatedCliqueOracle(args.order - 1, args.repeat_span)
    deadline = time.monotonic() + args.time_limit

    starts: list[list[int]] = []
    if args.seed is not None:
        seed = read_candidate(args.seed)
        words = lift_seed_words(seed, args.order - 1, args.phi_min, rng)
        # Put the lifts with the fewest additive defects first.  In particular,
        # the literal right extension of the order-93 seed has only 41+52=93.
        sum_database = ClauseDatabase(partition)
        sum_database.add_all_sum_free_constraints()
        projected = [partition.project(word, rng) for word in words]
        projected.sort(key=sum_database.score)
        for assignment in projected[: args.direct_starts]:
            repaired = repair_sum_constraints(assignment, partition, rng)
            if repaired is not None:
                starts.append(repaired)
    while len(starts) < args.direct_starts:
        repaired = repair_sum_constraints(
            random_assignment(partition, rng), partition, rng
        )
        if repaired is not None:
            starts.append(repaired)

    cache: dict[tuple[int, ...], FullProfile] = {}

    def objective(result: FullProfile) -> int:
        return result.objective(args.direct_sum_weight)

    def profile(unit_colors: Sequence[int]) -> FullProfile:
        key = tuple(unit_colors)
        result = cache.get(key)
        if result is None:
            result = full_violation_profile(
                partition.expand(key),
                partition,
                oracle,
                args.direct_profile_cap,
            )
            if len(cache) >= args.direct_cache:
                cache.pop(next(iter(cache)))
            cache[key] = result
        return result

    ranked: list[tuple[int, int, list[int], FullProfile]] = []
    for index, assignment in enumerate(starts):
        if time.monotonic() >= deadline:
            break
        current_profile = profile(assignment)
        ranked.append((objective(current_profile), index, assignment, current_profile))
        event(
            args.log,
            "direct-start",
            index=index,
            score=current_profile.score,
            objective=objective(current_profile),
            clauses=len(current_profile.clauses),
            raw=current_profile.raw_k5_witnesses,
            truncated=current_profile.truncated,
        )
    if not ranked:
        event(args.log, "direct-no-start")
        return 1
    ranked.sort(key=lambda item: item[:2])

    global_best_score = ranked[0][0]
    global_best = list(ranked[0][2])
    global_best_profile = ranked[0][3]
    restart = 0
    iterations = 0

    while time.monotonic() < deadline and iterations < args.direct_steps:
        _, _, initial, current_profile = ranked[restart % len(ranked)]
        state = list(initial)
        if restart >= len(ranked):
            state = list(global_best)
            for _ in range(1 + restart % max(args.restart_kicks, 1)):
                unit = rng.randrange(len(partition.units))
                alternatives = [
                    color
                    for color in partition.allowed[unit]
                    if color != state[unit]
                ]
                if alternatives:
                    state[unit] = rng.choice(alternatives)
            current_profile = profile(state)
        tabu_until: dict[tuple[int, int], int] = {}
        local_best = objective(current_profile)
        plateau = 0

        for local_step in range(args.direct_restart_steps):
            if time.monotonic() >= deadline or iterations >= args.direct_steps:
                break
            iterations += 1
            current_profile = profile(state)
            if not current_profile.truncated and current_profile.score == 0:
                colors = partition.expand(state)
                report = internal_check(
                    Candidate(
                        order=args.order,
                        phi_min=args.phi_min,
                        repeat_span=args.repeat_span,
                        colors=colors,
                    )
                )
                if not report["valid"]:
                    raise AssertionError(
                        f"direct profile/internal-check disagreement: {report}"
                    )
                candidate = Candidate(
                    order=args.order,
                    phi_min=args.phi_min,
                    repeat_span=args.repeat_span,
                    colors=colors,
                )
                write_candidate(
                    args.output,
                    candidate,
                    f"direct exact search oracle passed; seed={args.random_seed}",
                )
                event(
                    args.log,
                    "provisional-candidate",
                    strategy="direct",
                    output=str(args.output),
                    report=report,
                    iterations=iterations,
                )
                return 0

            break_count: Counter[tuple[int, int]] = Counter()
            for forbidden, units in current_profile.clauses:
                weight = (
                    args.direct_sum_weight if forbidden == TEMPLATE else 1
                )
                for unit in units:
                    for new_color in partition.allowed[unit]:
                        if new_color != forbidden:
                            break_count[(unit, new_color)] += weight
            moves = sorted(
                break_count,
                key=lambda move: (
                    -break_count[move],
                    rng.random(),
                ),
            )
            shortlist = [
                move
                for move in moves
                if state[move[0]] != move[1]
                and (
                    tabu_until.get(move, -1) <= iterations
                    or objective(current_profile) < global_best_score
                )
            ][: args.direct_candidates]
            for _ in range(args.direct_random_candidates):
                unit = rng.randrange(len(partition.units))
                alternatives = [
                    color
                    for color in partition.allowed[unit]
                    if color != state[unit]
                ]
                if alternatives:
                    move = (unit, rng.choice(alternatives))
                    if move not in shortlist:
                        shortlist.append(move)
            if not shortlist:
                break

            evaluated: list[tuple[int, int, int, FullProfile]] = []
            for unit, new_color in shortlist:
                trial = list(state)
                trial[unit] = new_color
                trial_profile = profile(trial)
                evaluated.append(
                    (objective(trial_profile), unit, new_color, trial_profile)
                )
            evaluated.sort(key=lambda item: (item[0], rng.random()))
            next_score, unit, new_color, next_profile = evaluated[0]
            delta = next_score - objective(current_profile)
            fraction = local_step / max(args.direct_restart_steps - 1, 1)
            temperature = args.start_temperature * (
                args.end_temperature / args.start_temperature
            ) ** fraction
            if delta > 0 and rng.random() >= math.exp(
                -delta / max(temperature, 1e-9)
            ):
                plateau += 1
                if plateau >= args.direct_plateau:
                    break
                continue

            old_color = state[unit]
            state[unit] = new_color
            tabu_until[(unit, old_color)] = iterations + args.direct_tabu
            current_profile = next_profile
            if objective(current_profile) < local_best:
                local_best = objective(current_profile)
                plateau = 0
            else:
                plateau += 1
            if objective(current_profile) < global_best_score:
                global_best_score = objective(current_profile)
                global_best = list(state)
                global_best_profile = current_profile
                event(
                    args.log,
                    "direct-best",
                    score=global_best_profile.score,
                    objective=global_best_score,
                    raw=global_best_profile.raw_k5_witnesses,
                    clauses=len(global_best_profile.clauses),
                    iteration=iterations,
                    restart=restart,
                    word="".join(
                        COLOR_CHARS[color] for color in partition.expand(global_best)
                    ),
                )
            if plateau >= args.direct_plateau:
                break
        restart += 1

    event(
        args.log,
        "timeout",
        strategy="direct",
        iterations=iterations,
        restarts=restart,
        best_score=global_best_score,
        best_constraint_count=global_best_profile.score,
        best_raw=global_best_profile.raw_k5_witnesses,
        best_word="".join(
            COLOR_CHARS[color] for color in partition.expand(global_best)
        ),
    )
    return 1


def anneal(
    state: SearchState,
    partition: Partition,
    rng: random.Random,
    steps: int,
    noise: float,
    start_temperature: float,
    end_temperature: float,
) -> dict[str, int]:
    mutable = [unit for unit, allowed in enumerate(partition.allowed) if len(allowed) > 1]
    accepted = 0
    improving = 0
    best = state.score
    for step in range(steps):
        if state.score == 0:
            break
        fraction = step / max(steps - 1, 1)
        temperature = start_temperature * (
            end_temperature / start_temperature
        ) ** fraction

        clause_id = rng.choice(tuple(state.violated))
        clause = state.database.clauses[clause_id]
        clause_mutable = [
            unit for unit in clause.units if len(partition.allowed[unit]) > 1
        ]
        if not clause_mutable:
            break
        unit = rng.choice(clause_mutable)
        alternatives = [
            color
            for color in partition.allowed[unit]
            if color != state.unit_colors[unit]
        ]
        deltas = [(state.delta_if(unit, color), color) for color in alternatives]
        if rng.random() < noise:
            delta, new_color = rng.choice(deltas)
        else:
            minimum = min(delta for delta, _ in deltas)
            delta, new_color = rng.choice(
                [(value, color) for value, color in deltas if value == minimum]
            )
        accept = delta <= 0 or rng.random() < math.exp(-delta / max(temperature, 1e-9))
        if accept:
            state.recolor(unit, new_color)
            accepted += 1
            if delta < 0:
                improving += 1
            best = min(best, state.score)
        elif rng.random() < noise * 0.05:
            # A very occasional unconstrained kick breaks deterministic two-cycles.
            kick = rng.choice(mutable)
            state.recolor(
                kick,
                rng.choice(
                    [
                        color
                        for color in partition.allowed[kick]
                        if color != state.unit_colors[kick]
                    ]
                ),
            )
    return {
        "accepted": accepted,
        "improving": improving,
        "best": best,
        "final": state.score,
    }


def cnf_variable(unit: int, color: int) -> int:
    return 3 * unit + color + 1


def render_cnf(database: ClauseDatabase) -> str:
    partition = database.partition
    clauses: list[list[int]] = []
    for unit, allowed in enumerate(partition.allowed):
        clauses.append([cnf_variable(unit, color) for color in (RED, BLUE, TEMPLATE)])
        clauses.extend(
            [
                [-cnf_variable(unit, RED), -cnf_variable(unit, BLUE)],
                [-cnf_variable(unit, RED), -cnf_variable(unit, TEMPLATE)],
                [-cnf_variable(unit, BLUE), -cnf_variable(unit, TEMPLATE)],
            ]
        )
        for color in (RED, BLUE, TEMPLATE):
            if color not in allowed:
                clauses.append([-cnf_variable(unit, color)])
    for clause in database.clauses:
        clauses.append(
            [
                -cnf_variable(unit, clause.forbidden_color)
                for unit in clause.units
            ]
        )
    lines = [f"p cnf {3 * len(partition.units)} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return "\n".join(lines) + "\n"


@dataclasses.dataclass(frozen=True)
class SatResult:
    status: str
    unit_colors: tuple[int, ...] | None
    stdout_tail: str


def run_kissat(
    database: ClauseDatabase,
    executable: str,
    timeout_seconds: float,
    keep_cnf: Path | None = None,
    proof_path: Path | None = None,
) -> SatResult:
    cnf_text = render_cnf(database)
    if keep_cnf is not None:
        keep_cnf.parent.mkdir(parents=True, exist_ok=True)
        keep_cnf.write_text(cnf_text, encoding="ascii")
        cnf_path = keep_cnf
        temporary = None
    else:
        temporary = tempfile.NamedTemporaryFile(
            mode="w", suffix=".cnf", encoding="ascii", delete=False
        )
        temporary.write(cnf_text)
        temporary.close()
        cnf_path = Path(temporary.name)
    command = [executable, "--quiet", str(cnf_path)]
    if proof_path is not None:
        proof_path.parent.mkdir(parents=True, exist_ok=True)
        command.append(str(proof_path))
    try:
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return SatResult("timeout", None, "")
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary.name)
            except FileNotFoundError:
                pass

    output = completed.stdout
    tail = "\n".join(output.splitlines()[-10:])
    if completed.returncode == 20 or "s UNSATISFIABLE" in output:
        return SatResult("unsat", None, tail)
    if completed.returncode != 10 and "s SATISFIABLE" not in output:
        return SatResult("error", None, tail)

    positive: set[int] = set()
    for line in output.splitlines():
        if line.startswith("v "):
            positive.update(
                literal
                for literal in map(int, line[2:].split())
                if literal > 0
            )
    unit_colors: list[int] = []
    for unit in range(len(database.partition.units)):
        selected = [
            color
            for color in (RED, BLUE, TEMPLATE)
            if cnf_variable(unit, color) in positive
        ]
        if len(selected) != 1:
            return SatResult("error", None, tail)
        unit_colors.append(selected[0])
    return SatResult("sat", tuple(unit_colors), tail)


def event(log_path: Path | None, kind: str, **payload: object) -> None:
    record = {"time": time.time(), "kind": kind, **payload}
    line = json.dumps(record, sort_keys=True, default=list)
    print(line, flush=True)
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def internal_check(candidate: Candidate) -> dict[str, object]:
    basic = basic_report(candidate.colors, candidate.phi_min)
    oracle = RepeatedCliqueOracle(candidate.period, candidate.repeat_span)
    repeated = oracle.exact_report(candidate.colors)
    valid = (
        basic["period_template"]
        and basic["phi_at_least_required"]
        and basic["sum_witness"] is None
        and repeated["repeated_k5_free"]
    )
    return {"valid": valid, "basic": basic, "repeated": repeated}


def run_search(args: argparse.Namespace) -> int:
    rng = random.Random(args.random_seed)
    partition = partition_from_args(args)
    database = ClauseDatabase(partition)
    database.add_all_sum_free_constraints()
    oracle = RepeatedCliqueOracle(args.order - 1, args.repeat_span)

    lifted: list[tuple[int, ...]] = []
    if args.seed is not None:
        seed = read_candidate(args.seed)
        lifted = lift_seed_words(seed, args.order - 1, args.phi_min, rng)
        event(
            args.log,
            "seed-lifts",
            seed=str(args.seed),
            count=len(lifted),
            seed_order=seed.order,
        )

    initial_assignments: list[list[int]] = [
        partition.project(word, rng) for word in lifted
    ]
    if not initial_assignments:
        initial_assignments.append(random_assignment(partition, rng))

    # Bootstrap the exact clause database with a portfolio of lifted and random
    # assignments.  Every learned clause comes with an actual integer witness.
    bootstrap_pool = initial_assignments[: args.bootstrap_assignments]
    while len(bootstrap_pool) < args.bootstrap_assignments:
        bootstrap_pool.append(random_assignment(partition, rng))
    for index, assignment in enumerate(bootstrap_pool):
        colors = partition.expand(assignment)
        before = len(database.clauses)
        report = oracle.separate(
            colors,
            database,
            args.oracle_batch,
            args.oracle_max_examined,
        )
        event(
            args.log,
            "bootstrap",
            index=index,
            clauses_before=before,
            clauses_after=len(database.clauses),
            red=report[RED],
            blue=report[BLUE],
        )

    deadline = time.monotonic() + args.time_limit
    best_score = sys.maxsize
    best_colors: tuple[int, ...] | None = None
    round_number = 0
    assignment_index = 0

    while time.monotonic() < deadline and round_number < args.max_rounds:
        if (
            args.kissat is not None
            and round_number > 0
            and round_number % args.sat_every == 0
        ):
            remaining = max(1.0, deadline - time.monotonic())
            sat = run_kissat(
                database,
                args.kissat,
                min(args.sat_timeout, remaining),
            )
            event(
                args.log,
                "sat",
                round=round_number,
                status=sat.status,
                clauses=len(database.clauses),
                tail=sat.stdout_tail,
            )
            if sat.status == "unsat":
                # A subset of globally valid clauses is already inconsistent in
                # this explicitly named symmetry class.  Freeze CNF + DRAT.
                if args.unsat_prefix is not None:
                    cnf_path = args.unsat_prefix.with_suffix(".cnf")
                    proof_path = args.unsat_prefix.with_suffix(".drat")
                    rerun = run_kissat(
                        database,
                        args.kissat,
                        min(args.sat_timeout, max(1.0, deadline - time.monotonic())),
                        keep_cnf=cnf_path,
                        proof_path=proof_path,
                    )
                    event(
                        args.log,
                        "unsat-artifact",
                        status=rerun.status,
                        cnf=str(cnf_path),
                        proof=str(proof_path),
                    )
                return 2
            if sat.status == "sat" and sat.unit_colors is not None:
                state = SearchState(database, sat.unit_colors)
            else:
                state = SearchState(database, random_assignment(partition, rng))
        else:
            if assignment_index < len(initial_assignments):
                start = initial_assignments[assignment_index]
                assignment_index += 1
            elif best_colors is not None and rng.random() < 0.35:
                start = partition.project(best_colors, rng)
                for _ in range(args.restart_kicks):
                    unit = rng.randrange(len(partition.units))
                    if len(partition.allowed[unit]) > 1:
                        start[unit] = rng.choice(partition.allowed[unit])
            else:
                start = random_assignment(partition, rng)
            state = SearchState(database, start)

        stats = anneal(
            state,
            partition,
            rng,
            args.round_steps,
            args.noise,
            args.start_temperature,
            args.end_temperature,
        )
        colors = partition.expand(state.unit_colors)
        if state.score < best_score:
            best_score = state.score
            best_colors = colors
        event(
            args.log,
            "anneal",
            round=round_number,
            score=state.score,
            best_score=best_score,
            clauses=len(database.clauses),
            origins=dict(database.origin_counts),
            **stats,
        )

        if state.score == 0:
            first_new_clause = len(database.clauses)
            separated = oracle.separate(
                colors,
                database,
                args.oracle_batch,
                args.oracle_max_examined,
            )
            state.refresh_new_clauses(first_new_clause)
            added = len(database.clauses) - first_new_clause
            event(
                args.log,
                "separate",
                round=round_number,
                added=added,
                score_after=state.score,
                red=separated[RED],
                blue=separated[BLUE],
            )
            if added == 0:
                report = internal_check(
                    Candidate(
                        order=args.order,
                        phi_min=args.phi_min,
                        repeat_span=args.repeat_span,
                        colors=colors,
                    )
                )
                if not report["valid"]:
                    raise AssertionError(
                        f"separator/internal-check disagreement: {report}"
                    )
                candidate = Candidate(
                    order=args.order,
                    phi_min=args.phi_min,
                    repeat_span=args.repeat_span,
                    colors=colors,
                )
                write_candidate(
                    args.output,
                    candidate,
                    f"internal search oracle passed; seed={args.random_seed}",
                )
                event(
                    args.log,
                    "provisional-candidate",
                    output=str(args.output),
                    report=report,
                )
                return 0
        round_number += 1

    event(
        args.log,
        "timeout",
        rounds=round_number,
        best_score=best_score,
        clauses=len(database.clauses),
        origins=dict(database.origin_counts),
    )
    return 1


def self_test(fixtures: Path) -> int:
    expectations = {
        "cpp_valid_small.template": True,
        "cpp_invalid_sum.template": False,
        "cpp_invalid_repeated_k5.template": False,
    }
    failed = False
    for name, expected in expectations.items():
        candidate = read_candidate(fixtures / name)
        report = internal_check(candidate)
        print(json.dumps({"fixture": name, **report}, sort_keys=True, default=list))
        if report["valid"] is not expected:
            failed = True

    published_seed = fixtures.parents[1] / "seeds" / "rowley_order93.template"
    if published_seed.exists():
        report = internal_check(read_candidate(published_seed))
        print(
            json.dumps(
                {"fixture": "published-rowley-order93", **report},
                sort_keys=True,
                default=list,
            )
        )
        if not report["valid"]:
            failed = True
    # Exercise incremental scoring against recomputation.
    rng = random.Random(90210)
    partition = Partition.build(11, 2, "none")
    database = ClauseDatabase(partition)
    database.add_all_sum_free_constraints()
    state = SearchState(database, random_assignment(partition, rng))
    for _ in range(200):
        unit = rng.randrange(len(partition.units))
        new_color = rng.choice(partition.allowed[unit])
        predicted = state.delta_if(unit, new_color)
        before = state.score
        actual = state.recolor(unit, new_color)
        if actual != predicted or state.score != database.score(state.unit_colors):
            failed = True
            print("incremental scoring mismatch", file=sys.stderr)
            break
        if state.score != before + actual:
            failed = True
            print("score delta mismatch", file=sys.stderr)
            break

    # Independently compare the residue compression against the literal
    # interval oracle on small random periodic colourings.
    for period in range(5, 9):
        oracle = RepeatedCliqueOracle(period, 4 * (period - 1))
        for _ in range(50):
            colors = [rng.randrange(3) for _ in range(period - 1)] + [TEMPLATE]
            for target in (RED, BLUE):
                via_residues = next(
                    oracle._iter_residue_cliques(colors, target), None
                )
                via_interval = next(
                    oracle._iter_interval_cliques(colors, target), None
                )
                if (via_residues is None) != (via_interval is None):
                    failed = True
                    print(
                        "residue/interval oracle disagreement",
                        period,
                        colors,
                        target,
                        via_residues,
                        via_interval,
                        file=sys.stderr,
                    )
                    break
    return int(failed)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "tests" / "fixtures",
    )
    parser.add_argument("--check-only", type=Path)
    parser.add_argument("--strategy", choices=("lazy", "direct"), default="lazy")
    parser.add_argument("--order", type=int, default=94)
    parser.add_argument("--phi-min", type=int, default=40)
    parser.add_argument("--repeat-span", type=int, default=368)
    parser.add_argument(
        "--symmetry",
        choices=("none", "reflection", "rowley-t12"),
        default="none",
    )
    parser.add_argument("--seed", type=Path)
    parser.add_argument("--random-seed", type=int, default=1)
    parser.add_argument("--time-limit", type=float, default=3600.0)
    parser.add_argument("--max-rounds", type=int, default=100000)
    parser.add_argument("--round-steps", type=int, default=200000)
    parser.add_argument("--noise", type=float, default=0.08)
    parser.add_argument("--start-temperature", type=float, default=1.0)
    parser.add_argument("--end-temperature", type=float, default=0.03)
    parser.add_argument("--restart-kicks", type=int, default=5)
    parser.add_argument("--bootstrap-assignments", type=int, default=8)
    parser.add_argument("--oracle-batch", type=int, default=256)
    parser.add_argument("--oracle-max-examined", type=int, default=50000)
    parser.add_argument("--kissat", default=shutil.which("kissat"))
    parser.add_argument("--sat-every", type=int, default=8)
    parser.add_argument("--sat-timeout", type=float, default=300.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/provisional_order94.template"),
    )
    parser.add_argument("--log", type=Path)
    parser.add_argument("--unsat-prefix", type=Path)
    parser.add_argument("--direct-starts", type=int, default=24)
    parser.add_argument("--direct-steps", type=int, default=100000)
    parser.add_argument("--direct-restart-steps", type=int, default=250)
    parser.add_argument("--direct-candidates", type=int, default=20)
    parser.add_argument("--direct-random-candidates", type=int, default=4)
    parser.add_argument("--direct-profile-cap", type=int, default=250000)
    parser.add_argument("--direct-cache", type=int, default=10000)
    parser.add_argument("--direct-plateau", type=int, default=20)
    parser.add_argument("--direct-tabu", type=int, default=7)
    parser.add_argument("--direct-sum-weight", type=int, default=1000)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.self_test:
        return self_test(args.fixtures)
    if args.check_only is not None:
        candidate = read_candidate(args.check_only)
        report = internal_check(candidate)
        print(json.dumps(report, indent=2, sort_keys=True, default=list))
        return 0 if report["valid"] else 1
    if args.strategy == "direct":
        return run_direct_search(args)
    return run_search(args)


if __name__ == "__main__":
    raise SystemExit(main())
