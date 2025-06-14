import pytest
from maradmin_processor import MaradminProcessor

def test_enlisted_promotion_processing(monkeypatch):
    processor = MaradminProcessor()
    # Load contacts for testing
    processor.contacts = processor.load_contacts()

    # Sample MARADMIN entry with enlisted promotion title
    entry = {
        'id': 'test123',
        'title': 'FY 2025 APPROVED SELECTIONS TO STAFF SERGEANT',
        'link': 'https://example.com/fake-maradmin'
    }

    # Monkeypatch extract_page_text to return sample text containing enlisted promotion lines
    sample_text = """
    SMITH  J  0311/12345
    DOE  A  0311/67890
    """
    monkeypatch.setattr(processor, 'extract_page_text', lambda url: sample_text)

    # Run process_maradmin and check if search_enlisted_promotions is called and returns matches
    matches = processor.process_maradmin(entry)

    # Assert that matches are found and that search_enlisted_promotions was used
    assert matches, "No matches found for enlisted promotion MARADMIN"
    for match in matches:
        assert 'contact' in match, "Match does not contain contact info"
        assert 'matched_text' in match, "Match does not contain matched_text"
