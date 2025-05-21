import importlib
import types


def test_auth_modules_importable():
    """Confirm that authentication modules can be imported."""

    modules = [
        "src.auth.user",
        "src.auth.password",
        "src.auth.token_management",
    ]
    for name in modules:
        module = importlib.import_module(name)
        assert isinstance(module, types.ModuleType)


def test_auth_init_all_is_list():
    """Verify that src.auth exposes __all__ as a list."""

    auth = importlib.import_module("src.auth")
    assert isinstance(auth.__all__, list)
