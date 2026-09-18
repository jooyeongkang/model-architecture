# CLAUDE.md

Guidance for working in this repository.

## What this is

A framework-neutral baseline for data-driven model applications. The core
package has no runtime dependencies. `src/model_architecture/examples/` holds
a small reference implementation; replace it when building a real model.

## Commands

```bash
uv sync --dev                 # create the locked environment
uv run pytest --cov           # tests, 90% coverage gate
uv run ruff check .           # lint
uv run ruff format --check .  # format
uv run mypy                   # strict, covers src/ and tests/
```

CI runs all four on every push to `main` and every pull request. Run them
locally before pushing; a red CI costs a review cycle.

## Architecture rules

`Pipeline` is the only object that knows the workflow. It calls each
collaborator in turn; collaborators never call each other.

```
DataSource.retrieve() -> DataProcessor.process() -> Model.run() -> OutputRenderer.render()
```

Non-negotiable:

- **`Model` never does I/O.** No clients, no file reads, no printing. Keeping
  it pure is what makes business logic testable with plain literals.
- **`domain/`, `ports/`, and `artifacts.py` import nothing else in the
  package.** They are the stable core; every other module depends inward on
  them. `grep -r "adapters" src/model_architecture/domain/` must stay empty.
- **Only `DataSource` implementations reach the outside world.** Databases,
  object stores, and APIs live there and nowhere else.
- **Rendering is not delivering.** A renderer returns an artifact describing
  the output; the entrypoint prints, uploads, or plots it. Never import
  matplotlib or pandas into a renderer.
- **Contracts are `typing.Protocol`.** Conformance is structural, so no
  adapter imports the protocol it satisfies. `mypy` verifies the match where
  the pipeline is assembled in `bootstrap.py`.
- **`bootstrap.py` is the only module that names every layer.** Entrypoints
  call it; nothing else imports adapters directly.

## Where to define types

Concrete `Request`, `RawData`, `ModelInput`, and `ModelResult` types belong in
`domain/`, which keeps it a leaf that adapters depend on rather than the
reverse. Artifacts already live in `artifacts.py`; do not add a parallel home
for them.

Nothing vendor-shaped crosses a port: a `DataSource` returns a type this
package owns. Raw DB tuples and vendor JSON stop inside the adapter, which
converts them. That way swapping Postgres for an API touches one file.

## Gotchas

- All renderers on one `Pipeline` must agree on a single `ArtifactT`. To mix a
  table and a plot, widen the parameter to `TableArtifact | PlotArtifact` and
  dispatch in the entrypoint.
- `mypy --strict` covers `tests/` too, so test helpers need annotations.
- Expected failures inherit from `ModelArchitectureError`, so an entrypoint
  catches that one type. Let anything else propagate — it is a bug.

## Conventions

- Frozen, slotted dataclasses for value objects.
- Positional-only parameters (`/`) on protocol methods.
- PEP 695 generics (`class Foo[T]`), not `TypeVar` assignments.
- Test names state the behaviour being asserted, not the method being called.
