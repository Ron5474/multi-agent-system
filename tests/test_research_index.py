import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def tmp_research(tmp_path, monkeypatch):
    research_dir = tmp_path / "research"
    research_dir.mkdir()
    monkeypatch.setattr("tools.research_index._RESEARCH_DIR", research_dir)
    return research_dir


def test_find_related_returns_match(tmp_research):
    (tmp_research / "transformer-fine-tuning.md").write_text(
        "# Transformer Fine-Tuning Methods\nLoRA and QLoRA are transformer fine-tuning methods."
    )
    from tools.research_index import find_related_research
    result = find_related_research("transformer fine tuning project")
    assert "Transformer Fine-Tuning Methods" in result


def test_find_related_returns_empty_when_no_match(tmp_research):
    (tmp_research / "transformer-fine-tuning.md").write_text(
        "# Transformer Fine-Tuning\nLoRA is a fine-tuning method."
    )
    from tools.research_index import find_related_research
    result = find_related_research("basketball sports game")
    assert result == ""


def test_find_related_returns_empty_when_no_research_dir(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.research_index._RESEARCH_DIR", tmp_path / "nonexistent")
    from tools.research_index import find_related_research
    result = find_related_research("anything")
    assert result == ""


def test_find_related_ranks_by_hit_count(tmp_research):
    (tmp_research / "responsible-ai.md").write_text(
        "# Responsible AI\nResponsible AI regulation frontier models policy ethics."
    )
    (tmp_research / "lora.md").write_text(
        "# LoRA\nLoRA fine-tuning responsible adaptation."
    )
    from tools.research_index import find_related_research
    result = find_related_research("responsible AI regulation policy")
    lines = result.strip().splitlines()
    assert "Responsible AI" in lines[1]
