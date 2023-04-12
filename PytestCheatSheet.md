Oficjalna dokumentacja: https://docs.pytest.org/en/7.3.x/contents.html

# <span style="color:#049ccb"> Podstawowe Informacje
##  <span style="color:#5982DB"> Instalacja
```bash 
pip install -U pytest
```
##  <span style="color:#5982DB">  Struktura projektu
* Wszystkie testy powinny znajdować się w folderze tests.
* Nazwy plików z testami powinny zaczynać się od test_. 
* Również nazwy klas/funkcji testowych powinny zaczynać się od test_.

Stosowanie tych reguł pozwala na automatyczne wykrycie testów przez bibliotekę pytest i uruchomienie ich przy użyciu niżej opisanych komend.
## <span style="color:#5982DB"> Uruchomienie
Wszystkie testy w projekcie:
```bash
pytest
```
Testy z wybranego folderu:
```bash
pytest tests/
```
Testy z wybranego pliku:
```bash
pytest tests/test_example.py
```
Testy z wybranego pliku i wybranej klasy:
```bash
pytest tests/test_example.py::TestClass
```
 
Konkretny test z wybranego pliku i wybranej klasy (w tym przypadku test_example):
```bash
pytest tests/test_example.py::TestClass::test_example
```
Konkretny test z wybranego pliku w formie funkcji (w tym przypadku test_example):
```bash
pytest tests/test_example.py::test_example
```
### <span style="color:#665EB8"> Parametry uruchomienia
```bash
pytest -v # verbose - wyświetla więcej informacji
pytest -q # quiet - wyświetla mniej informacji
pytest -s # show - wyświetla printy
pytest -k "test_example" # wyświetla tylko testy zawierające w nazwie "test_example"
pytest -m "example" # wyświetla tylko testy oznaczone (markerami) jako "example"
pytest -x # exit first - po pierwszym błędzie zakończ testy
pytest --maxfail=2 # po 2 błędach zakończ testy
pytest --lf # run last failed - uruchamia tylko ostatnio nieudane testy
pytest --ff # run failed first - uruchamia najpierw nieudane testy
pytest --nf # run new first - uruchamia najpierw nowe testy
pytest --cache-clear # usuwa cache
pytest --durations=2 # wyświetla 2 najdłuższe testy
```
Wszystkie parametry dostępne [w dokumentacji](https://docs.pytest.org/en/7.3.x/reference/reference.html#command-line-flags).

### <span style="color:#665EB8"> Przydatna Wtyczka 
[pytest-cov](https://pypi.org/project/pytest-cov/) - Pozwala sprawdzić pokrycie kodu testami
```bash
pip install pytest-cov
```
Użycie: 
```bash
pytest --cov=app #app - nazwa folderu z kodem
pytest --cov-report term-missing --cov=app # zawiera niepokryte linijki kodu
```

# <span style="color:#049ccb"> Pliki Pytesta
## <span style="color:#5982DB">  pytest.ini - plik konfiguracyjny
Pytest ma możliwość odczytania konfiguracji z jednego z trzech plików: 
* pytest.ini - plik konfiguracyjny
* tox.ini - plik konfiguracyjny dla biblioteki tox
* setup.cfg - plik konfiguracyjny dla biblioteki setuptools

Jeżeli nasz projekt nie używa żadnej z tych bibliotek, to najlepiej jest użyć pliku pytest.ini.

W tym pliku można określić domyślne parametry, które będą używane przy uruchamianiu testów. 
```ini
[pytest]
addopts = -v -s
markers =
    example: example marker
```
Taki plik spowoduje wyświetlenie dodatkowych informacji o testach (v) oraz wyświetlenie printów(s) przy każdym uruchomieniu testów.
Dodatkowo zostanie utworzony marker o nazwie example, który będzie można używać w testach.
## <span style="color:#5982DB">  conftest.py - plik zawierający współdzielone fixtures
Każdy folder zawierający testy może posiadać swój plik conftest. 
W tym pliku można umieszczać fixtures, które będą używane w wielu testach, szczególnie jeśli znajdują się one w osobnych plikach. 
Zostaną one automatycznie zaimportowane do każdego testu z tego folderu.
```python
import pytest

@pytest.fixture
def example_fixture():
    return 1
```

# <span style="color:#049ccb"> Najważniejsze funkcjonalności Pytesta

## <span style="color:#5982DB">  Parametryzacja
Parametryzacja pozwala na przekazanie listy wartości do testu.
W tym przypadku test zostanie wykonany 3 razy, dla każdej wartości z listy.
[Oficjalna dokumentacja](https://docs.pytest.org/en/7.3.x/parametrize.html).
```python
# Przykład z jednym parametrem
@pytest.mark.parametrize("example_param", [1, 2, 3])
def test_example(example_param):
    assert example_param == 1
    
# Przykład z wieloma parametrami
@pytest.mark.parametrize("example_param, expected_result", 
                         [(1, 2), (3, 4), (5, 6)])
def test_example(example_param, expected_result):
    assert example_param == expected_result
```
## <span style="color:#5982DB">  Fixtures
Fixtures to funkcje, które są wywoływane przed lub/i po każdym testeście. 
Mogą zwracać wartości, które są przekazywane do testów jako parametry. 
Mogą być również wywoływane bezpośrednio w testach. 
Fixtures mogą być wywoływane w dowolnej kolejności. 
Więcej informacji można znaleźć w [oficjalnej dokumentacji](https://docs.pytest.org/en/7.3.x/fixture.html).
```python
@pytest.fixture
def example_fixture():
    return 1
```
**Najważniejsze parametry, które przyjmuje Fixture:**

* **autouse** - pozwala na automatyczne wywołanie tej funkcji przed każdym testem.
    ```python
    @pytest.fixture(autouse=True)
    def example_fixture():
        return 1
    ```
*  **scope** -  określa w jakim momencie ma być wywoływana funkcja. Dostępne opcje to:
    * *function* - domyślna wartość, funkcja jest wywoływana przed każdym testem
    * *class* - funkcja jest wywoływana przed każdą klasą
    * *module* - funkcja jest wywoływana przed każdym plikiem
    * *session* - funkcja jest wywoływana przed każdym sesją
    ```python
    @pytest.fixture(scope="class")
    def example_fixture():
        return 1
    ```
*  **params** -  pozwala na przekazanie listy wartości, które zostaną przekazane do funkcji jako parametry.
    ```python
    @pytest.fixture(params=[1, 2, 3])
    def example_fixture(request):
        return request.param
    ```
    * **ids** - pozwala na nadanie nazw wartościom przekazanym do funkcji.
    ```python
    @pytest.fixture(params=[1, 2, 3], ids=["one", "two", "three"])
    def example_fixture(request):
        return request.param
    ```
## <span style="color:#5982DB">  Markery
Pozwala na kategoryzowanie testów. Dzięki temu można wywoływać tylko testy z wybranymi markami.
Więcej informacji można znaleźć w [oficjalnej dokumentacji](https://docs.pytest.org/en/7.3.x/example/markers.html).
```python
@pytest.mark.example_marker
def test_example():
    assert 1 == 1
```
```bash
pytest -m example_marker # Wywołanie tylko testów z oznaczeniem (mark) example_marker
```
## <span style="color:#5982DB">  Wyłapywanie wyjątków
Umożliwia sprawdzenie, czy wyjątek został podniesiony w trakcie testu (np. czy twój try except działa prawidłowo). 
```python
def test_example():
    with pytest.raises(Exception):
        raise Exception
```
# <span style="color:#049ccb"> Mockowanie 
## <span style="color:#5982DB">  monkeypatch
Monkeypatch pozwala na zmianę wartości zmiennych w trakcie testu.
Najbardziej przydatny przy testowaniu kodu, który korzysta ze zmiennych środowiskowych 
lub łączy się ze środowiskiem zewnętrznym (np. wysyłanie zapytań HTTP), 
w celu wyizolowania środowiska testowego.
Pierwszy parametr stanowi ścieżka do zmiennej, która ma zostać zmieniona, a drugi to nowa wartość.
Więcej informacji można znaleźć w [oficjalnej dokumentacji](https://docs.pytest.org/en/7.3.x/monkeypatch.html).
```python
def test_example(monkeypatch):
    monkeypatch.setattr("example_module.example_variable", 1)
    assert example_module.example_variable == 1
```
Najczęściej stosuje się go wraz z fixture, dzięki czemu może być wykorzystywany w wielu testach.
```python
@pytest.fixture
def example_fixture(monkeypatch):
    monkeypatch.setattr("example_module.example_variable", 1)
```
## <span style="color:#5982DB">  Tmp_path
Wbudowana funkcja, która zwraca ścieżkę do tymczasowego katalogu, który jest unikalny dla każdego testu. Ścieżka jest utworzona jako podkatalog podstawowego katalogu tymczasowego. Zwracany obiekt jest obiektem pathlib.Path.
Katalog tymczasowy jest usuwany po zakończeniu testu.
Użyteczny w przypadku testowania kodu, który zapisuje/odczytuje pliki na/z dysku.
Więcej informacji można znaleźć w [oficjalnej dokumentacji](https://docs.pytest.org/en/7.3.x/tmpdir.html).
```python
def test_example(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test")
    assert file_path.read_text() == "test"
```
Najczęściej stosowany wraz z fixture, dzięki czemu może być wykorzystywany w wielu testach.
```python
@pytest.fixture
def mock_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test")
    return file_path
```
# <span style="color:#049ccb"> Baza Wiedzy 
* [Pytest Documentation](https://docs.pytest.org/en/stable/) - Oficjalna dokumentacja
* [Software Testing - General Intro to Testing in Python](https://www.youtube.com/playlist?list=PLC0nd42SBTaPYSgBqtlltw328zuafaCzA) - YouTube Playlist
* [Testing with Pytest](https://www.youtube.com/watch?v=_bm3wIu3xTg&list=PLZMWkkQEwOPkFsyal6Uq3RvAGsBbLCfZV) - YouTube Playlist
* [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/) - RealPython Tutorial
* [Pytest-Django](https://pytest-django.readthedocs.io/en/latest/) - Django Plugin
* [Testing Flask Applications](https://flask.palletsprojects.com/en/2.2.x/testing/) - Flask Testing Tips
* *"Python Testing with pytest: Simple, Rapid, Effective, and Scalable"* (edition 2022) - Book