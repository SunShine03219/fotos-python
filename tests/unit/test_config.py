import pytest
from config import Config


@pytest.mark.integration
@pytest.mark.high
def test_singleton():
    instance1 = Config()
    instance2 = Config()
    assert instance1 == instance2
