from click.testing import CliRunner

from fling.bin.fling import fling


def test_fling_search_cli():
    runner = CliRunner()
    result = runner.invoke(fling, ["search", "foo"])
    assert result.exit_code == 0
    assert "contoso" in result.output
