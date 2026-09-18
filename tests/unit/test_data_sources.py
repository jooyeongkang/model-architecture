from model_architecture.adapters.data_sources import InMemoryDataSource


def test_in_memory_data_source_returns_preloaded_data() -> None:
    source = InMemoryDataSource[str, tuple[int, ...]]((1, 2, 3))

    assert source.retrieve("ignored") == (1, 2, 3)
