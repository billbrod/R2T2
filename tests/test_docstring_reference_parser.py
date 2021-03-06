from pathlib import Path

from r2t2.core import Biblio, FunctionReference
from r2t2.docstring_reference_parser import (
    DOCSTRING_SHORT_PURPOSE,
    parse_and_add_docstring_references_from_files
)

DOI_URL_HTTPS_PREFIX = 'https://doi.org/'

DOI_1 = '10.1234/zenodo.1234567'


class TestParseAndAddDocstringReferencesFromFiles:
    def test_should_parse_docstring_reference(
        self, temp_dir: Path
    ):
        file_path = temp_dir / 'test.py'
        file_path.write_text('\n'.join([
            'def some_function():'
            '    """',
            '    ' + DOI_1,
            '    """'
        ]))
        biblio = Biblio()
        parse_and_add_docstring_references_from_files(
            [file_path],
            biblio=biblio
        )
        expected_identifier = '{source}:{line_num}'.format(
            source=str(file_path),
            line_num=1
        )
        assert biblio.keys() == {expected_identifier}
        function_reference = biblio[expected_identifier]
        assert function_reference.name == 'some_function'
        assert function_reference.source == str(file_path)
        assert function_reference.line == 1
        assert function_reference.references == [DOI_URL_HTTPS_PREFIX + DOI_1]
        assert function_reference.short_purpose == [DOCSTRING_SHORT_PURPOSE]

    def test_should_not_override_existing_reference(
        self, temp_dir: Path
    ):
        file_path = temp_dir / 'test.py'
        file_path.write_text('\n'.join([
            'def some_function():'
            '    """',
            '    ' + DOI_1,
            '    """'
        ]))
        expected_identifier = '{source}:{line_num}'.format(
            source=str(file_path),
            line_num=1
        )
        biblio = Biblio()
        existing_function_reference = FunctionReference(
            name='other',
            source='other.py',
            line=-1,
            short_purpose=['For testing'],
            references=['test/123']
        )
        biblio[expected_identifier] = existing_function_reference
        parse_and_add_docstring_references_from_files(
            [file_path],
            biblio=biblio
        )
        assert biblio == {expected_identifier: existing_function_reference}

    def test_should_not_add_function_reference_without_references(
        self, temp_dir: Path
    ):
        file_path = temp_dir / 'test.py'
        file_path.write_text('\n'.join([
            'def some_function():'
            '    """',
            '    some docstring',
            '    """'
        ]))
        biblio = Biblio()
        parse_and_add_docstring_references_from_files(
            [file_path],
            biblio=biblio
        )
        assert not biblio
