#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pylexique` package."""

import pytest
from collections import OrderedDict
from click.testing import CliRunner

from pylexique import Lexique383

from pylexique import pylexique, cli


def test_content():
    """Sample pytest test of pylexique."""
    Lexique_dict = OrderedDict()
    test = Lexique383('Lexique383/Lexique383.xlsb')
    # test1 = Lexique383()  # Use only if the hdf5 file exists.
    others = []
    verbs = []
    for x in Lexique_dict.values():
        if x.cgram == 'VER':
            assert x.cgram == 'VER'
        else:
            others.append(x)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'pylexique.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
