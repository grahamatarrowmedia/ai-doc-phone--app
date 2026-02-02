"""Test the blueprint upload functionality."""
import requests
import io
import json

# Use the Cloud Run URL
BASE_URL = "https://doc-production-app-280939464794.us-central1.run.app"

def test_blueprint_text_file():
    """Test blueprint analysis with a text file."""
    print("Testing blueprint upload with text file...")

    # Create a sample blueprint document
    blueprint_content = """
    Documentary Project: The Hidden World of Urban Wildlife

    This documentary series explores the surprising diversity of wildlife that has adapted
    to thrive in our cities. From foxes in London to coyotes in Los Angeles, we discover
    how animals have learned to coexist with humans in urban environments.

    Key Themes:
    - Adaptation and survival strategies
    - Human-wildlife conflict and coexistence
    - The role of green spaces in cities
    - Night-time urban ecosystems
    - Conservation efforts in metropolitan areas

    Style: Observational documentary with expert interviews and stunning wildlife cinematography.

    Target audience: Nature enthusiasts, urban dwellers curious about their environment.
    """

    # Create file-like object
    files = {
        'file': ('blueprint.txt', io.BytesIO(blueprint_content.encode('utf-8')), 'text/plain')
    }
    data = {
        'numEpisodes': '4'
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/analyze-blueprint",
            files=files,
            data=data,
            timeout=120
        )

        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if 'blueprint' in result:
                blueprint = result['blueprint']
                print(f"✓ Title: {blueprint.get('title', 'N/A')}")
                print(f"✓ Description: {blueprint.get('description', 'N/A')[:100]}...")
                print(f"✓ Style: {blueprint.get('style', 'N/A')}")
                print(f"✓ Episodes: {len(blueprint.get('episodes', []))}")
                for ep in blueprint.get('episodes', []):
                    print(f"  - {ep.get('order', '?')}. {ep.get('title', 'Untitled')}")
                return True
            elif 'error' in result:
                print(f"✗ Error from API: {result['error']}")
                return False
            else:
                print(f"✗ Unexpected response: {result}")
                return False
        else:
            print(f"✗ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False

    except requests.exceptions.Timeout:
        print("✗ Request timed out (>120s)")
        return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


def test_blueprint_no_file():
    """Test that endpoint returns error when no file is provided."""
    print("\nTesting blueprint upload with no file...")

    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/analyze-blueprint",
            data={'numEpisodes': '5'},
            timeout=30
        )

        if response.status_code == 400:
            result = response.json()
            if 'error' in result:
                print(f"✓ Correctly returned error: {result['error']}")
                return True

        print(f"✗ Expected 400 error, got {response.status_code}")
        return False

    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


def test_blueprint_pdf():
    """Test blueprint analysis with a simple PDF-like content."""
    print("\nTesting blueprint upload with PDF file...")

    # Note: This is a minimal test - real PDF would need proper PDF structure
    # For now, we'll test that the endpoint accepts the file

    # Create a minimal PDF (this is a very basic PDF structure)
    pdf_content = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 12 Tf 100 700 Td (Documentary Blueprint) Tj ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000214 00000 n
trailer
<< /Size 5 /Root 1 0 R >>
startxref
307
%%EOF"""

    files = {
        'file': ('blueprint.pdf', io.BytesIO(pdf_content), 'application/pdf')
    }
    data = {
        'numEpisodes': '3'
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/ai/analyze-blueprint",
            files=files,
            data=data,
            timeout=120
        )

        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            if 'blueprint' in result:
                print("✓ PDF blueprint analysis succeeded")
                return True
            elif 'error' in result:
                print(f"✗ Error from API: {result['error']}")
                return False
        else:
            print(f"Response: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Blueprint Upload Tests")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("No file error handling", test_blueprint_no_file()))
    results.append(("Text file analysis", test_blueprint_text_file()))
    # results.append(("PDF file analysis", test_blueprint_pdf()))  # Skip for now

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    passed = 0
    failed = 0
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\nTotal: {passed} passed, {failed} failed")
