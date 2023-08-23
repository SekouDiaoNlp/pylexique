import pytest
import json
from pylexique import Lexique383, LexItem
from pylexique import _get_results, _display_results
from pylexique import cli
from click.testing import CliRunner

# Basic unit tests for pylexique.py
def test_lexique383_initialization():
    lexique = Lexique383()
    assert isinstance(lexique.lexique, dict)
    assert isinstance(lexique.lemmes, dict)
    assert isinstance(lexique.anagrams, dict)

def test_lexique383_get_lex():
    lexique = Lexique383()
    results = lexique.get_lex("bonjour")
    assert "bonjour" in results

def test_lexique383_get_all_forms():
    lexique = Lexique383()
    forms = lexique.get_all_forms("amour")
    assert isinstance(forms, list)
    assert all(isinstance(item, LexItem) for item in forms)

def test_lexique383_get_anagrams():
    lexique = Lexique383()
    anagrams = lexique.get_anagrams("marteau")
    assert isinstance(anagrams, list)
    assert all(isinstance(item, LexItem) for item in anagrams)

# Basic unit tests for cli.py
def test_get_results():
    lexique = Lexique383()
    words = ["bonjour", "amour"]
    results = _get_results(lexique, words, all_forms=False)
    assert "bonjour" in results
    assert "amour" in results

# def test_display_results(capsys):
    # lexique = Lexique383()
    # words = ["bonjour"]
    # results = _get_results(lexique, words, all_forms=False)
    # _display_results(results, output=None)
    # captured = capsys.readouterr()
    # assert "Lexical Information for 'bonjour'" in captured.out

def test_cli_integration():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.main, ["bonjour"])
        assert result.exit_code == 0
        assert "Lexical Information for" in result.output
        assert "'bonjour'" in result.output

# Mocking external dependencies
@pytest.fixture
def mock_lexique():
    return Lexique383()

def test_mocked_get_results(mock_lexique):
    words = ["bonjour", "amour"]
    results = _get_results(mock_lexique, words, all_forms=False)
    assert "bonjour" in results
    assert "amour" in results

# Testing JSON output
# def test_json_output(tmp_path):
    # lexique = Lexique383()
    # output_path = tmp_path / "output.json"
    # words = ["bonjour", "amour"]
    # results = _get_results(lexique, words, all_forms=False)

    # _display_results(results, str(output_path))

    # with open(output_path, "r") as f:
        # json_data = json.load(f)
        # assert "bonjour" in json_data
        # assert "amour" in json_data

# Run the tests
if __name__ == "__main__":
    pytest.main()
