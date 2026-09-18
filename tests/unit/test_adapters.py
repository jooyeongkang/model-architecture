from model_architecture.adapters.data_repos import InMemoryDataRepo


def test_in_memory_data_repo_returns_preloaded_data() -> None:
    repo = InMemoryDataRepo[str, tuple[int, ...]]((1, 2, 3))

    assert repo.retrieve("ignored") == (1, 2, 3)
