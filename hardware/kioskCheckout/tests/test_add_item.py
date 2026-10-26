import sqlite3
import sys

import pytest

import add_item


@pytest.fixture
def cli(kiosk, monkeypatch, capsys):
    """Run `add_item.py <args>` and return (exit_code, stdout)."""
    def run(*args):
        monkeypatch.setattr(sys, 'argv', ['add_item.py', *args])
        try:
            add_item.main()
            code = 0
        except SystemExit as e:
            code = e.code
        return code, capsys.readouterr().out
    return run


def rows():
    with sqlite3.connect('kiosk.db') as conn:
        try:
            return conn.execute(
                "SELECT name, category, price, weight_g, tolerance_g, stock FROM items").fetchall()
        except sqlite3.OperationalError:  # table never created because the command failed early
            return []


def test_add_creates_table_and_item(cli):
    code, out = cli('add', 'Cola', '15', '532', '--category', 'drinks', '--stock', '24')
    assert code == 0 and 'Added #1' in out
    assert rows() == [('Cola', 'drinks', 15.0, 532.0, 5.0, 24)]


def test_add_defaults(cli):
    cli('add', 'Bar', '10', '45')
    assert rows() == [('Bar', None, 10.0, 45.0, 5.0, 0)]


def test_duplicate_name_is_rejected(cli):
    cli('add', 'Cola', '15', '532')
    code, _ = cli('add', 'Cola', '20', '500')
    assert code != 0
    assert len(rows()) == 1


@pytest.mark.parametrize('args', [
    ('add', 'X', '-1', '5'),
    ('add', 'X', '1', '0'),
    ('add', 'X', '1', '5', '--stock', '-2'),
    ('add', 'X', 'abc', '5'),
    ('add', 'X'),
])
def test_invalid_add_is_rejected(cli, args):
    code, _ = cli(*args)
    assert code != 0
    assert rows() == []


def test_update_changes_only_given_fields(cli):
    cli('add', 'Cola', '15', '532', '--stock', '3')
    code, _ = cli('update', 'Cola', '--price', '16.5')
    assert code == 0
    assert rows() == [('Cola', None, 16.5, 532.0, 5.0, 3)]


def test_update_can_rename(cli):
    cli('add', 'Cola', '15', '532')
    cli('update', 'Cola', '--name', 'Coke')
    assert [r[0] for r in rows()] == ['Coke']


def test_update_rename_to_existing_name_fails(cli):
    cli('add', 'Cola', '15', '532')
    cli('add', 'Fanta', '15', '535')
    code, _ = cli('update', 'Fanta', '--name', 'Cola')
    assert code != 0


def test_update_unknown_item_or_nothing_to_change_fails(cli):
    cli('add', 'Cola', '15', '532')
    assert cli('update', 'Nope', '--stock', '1')[0] != 0
    assert cli('update', 'Cola')[0] != 0


def test_delete(cli):
    cli('add', 'Cola', '15', '532')
    assert cli('delete', 'Cola')[0] == 0
    assert rows() == []
    assert cli('delete', 'Cola')[0] != 0


def test_list(cli):
    assert 'No items yet' in cli('list')[1]
    cli('add', 'Cola', '15', '532')
    assert 'Cola' in cli('list')[1]
