import pytest
from swirl.bs4 import bs


def test_bs():
    html = {'_expandable': {'editor': '', 'atlas_doc_format': '', 'view': '', 'export_view': '', 'styled_view': '', 'dynamic': '', 'storage': '', 'editor2': '', 'anonymous_export_view': ''}}
    soup = bs(html, "html.parser")
