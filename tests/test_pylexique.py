#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pylexique` package."""

import pytest
from collections import OrderedDict
from click.testing import CliRunner

from pylexique import Lexique383

from pylexique import pylexique, cli, vdir


def test_content():
    """Sample pytest test of pylexique."""
    others = []
    lexicon = Lexique383()
    x = 'a posteriori'
    if x in lexicon.lexique:
        if lexicon.lexique[x].cgram == 'ADV':
            assert lexicon.lexique[x].freqlemfim2== 'ADV'
        else:
            others.append(x)


def test_command_line_interface():
    """Test the CLI for ."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Pylexique is a Python wrapper around Lexique83.' in help_result.output
