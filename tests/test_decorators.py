from src.decorators import log
import pytest
import os


def test_log_console(capsys):

    @log()
    def my_func(x, y):
        return x + y

    result = my_func(1, 2)
    assert result == 3
    captured = capsys.readouterr()
    assert captured.out == "my_func ok\n"


def test_log(capsys):
    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_capsys(capsys):
    @log(file_name=None)
    def hello_world():
        return "Hello, world!"

    result = hello_world()
    captured = capsys.readouterr()
    assert captured.out == "hello_world ok\n"


def test_log_writes_to_file(tmp_path):
    log_file = tmp_path / "my_log.txt"

    @log(file_name=str(log_file))
    def my_function(x, y):
        return x + y

    result = my_function(10, 20)

    assert result == 30

    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "my_function ok\n" in content


def test_log_preserves_function_name():
    @log(file_name=None)
    def secret_operation():
        pass

    assert secret_operation.__name__ == "secret_operation"
