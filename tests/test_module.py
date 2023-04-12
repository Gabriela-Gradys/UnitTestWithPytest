"""Test our module.

moduł = funkcja/metoda/atrybut/zmienna/klasa/biblioteka

monkeypatch
    .setattr("ścieżka_do_modułu_który_blokujemy", funkcja_która_zastąpi_moduł)
    .setenv("ZMIENNA_ŚRODOWISKOWA_KTÓRĄ_BLOKUJEMY", "zmienna_która_zastąpi_env")

tmp_path = faktyczna ścieżka do tymczasowego pliku - każda ścieżka oraz pliki
    zostaną utworzone podczas testu i usunięte od razu po zakończeniu.

requests_mock = specjalna biblioteka służąca do symulowania requests.
"""

from example_codes.module import BritishGentleman
from pytest import fixture


def safe_the_world(*_, **__):
    """Mock the destroyer!"""

    print("The world is safe now!")


@fixture
def gentleman():
    """Create British Gentleman instance."""

    instance = BritishGentleman()
    return instance


def test_greeting(monkeypatch, gentleman):
    """Check greeting function from module."""

    monkeypatch.setattr(
        "example_codes.module.BritishGentleman.destroy_the_world", safe_the_world
    )
    assert "Have a nice day!" in gentleman.greeting()


def test_show_me_env(monkeypatch, gentleman):
    """Test if env is given properly."""

    monkeypatch.setenv("OUR_MISTERIOUS_ENV", "OUR_MISTERIOUS_VALUE")
    assert "OUR_MISTERIOUS_VALUE" in gentleman.show_me_your_variable()


def test_check_file(tmp_path, gentleman):
    """Check if path is opened properly."""

    filepath = tmp_path / "test.txt"
    filepath.write_text("It's a pleasure to meet you.")
    assert "pleasure to meet" in gentleman.check_file(filepath)


def test_request_data(requests_mock, gentleman):
    """Check connection with Google.com"""

    requests_mock.get("https://www.google.com/", text="text")
    assert "text" in gentleman.get_website_text("https://www.google.com/")
