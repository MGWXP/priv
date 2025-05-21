from src.config import load_integrations_config


def test_load_integrations_config(monkeypatch):
    monkeypatch.setenv("NOTION_API_KEY", "abc")
    monkeypatch.setenv("GITHUB_TOKEN", "def")
    monkeypatch.setenv("SLACK_TOKEN", "ghi")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    cfg = load_integrations_config()

    assert cfg.notion_api_key == "abc"
    assert cfg.github_token == "def"
    assert cfg.slack_token == "ghi"
    assert cfg.database_url == "sqlite:///:memory:"
