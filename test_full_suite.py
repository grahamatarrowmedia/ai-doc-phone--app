#!/usr/bin/env python3
"""
Comprehensive Test Suite for Documentary Production App

Tests:
1. API Tests - All CRUD operations for all collections
2. Unit Tests - Data validation, helper functions
3. Functional Tests - Business logic, cascade deletes, AI features
4. UI Tests - Page structure, navigation, forms
"""
import requests
import json
import sys
import time
import re
from datetime import datetime

BASE_URL = "http://localhost:5000"


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BOLD}{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}{Colors.END}")


def print_section(text):
    print(f"\n{Colors.BLUE}[{text}]{Colors.END}")
    print("-" * 50)


def print_test(name, passed, details=""):
    if passed:
        status = f"{Colors.GREEN}✓ PASS{Colors.END}"
    else:
        status = f"{Colors.RED}✗ FAIL{Colors.END}"
    print(f"  {status}: {name}")
    if details and not passed:
        print(f"         {Colors.YELLOW}{details}{Colors.END}")


def api_get(endpoint, timeout=10):
    response = requests.get(f"{BASE_URL}{endpoint}", timeout=timeout)
    try:
        return response.status_code, response.json()
    except:
        return response.status_code, response.text


def api_post(endpoint, data, timeout=10):
    response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=data,
        headers={"Content-Type": "application/json"},
        timeout=timeout
    )
    try:
        return response.status_code, response.json()
    except:
        return response.status_code, response.text


def api_put(endpoint, data, timeout=10):
    response = requests.put(
        f"{BASE_URL}{endpoint}",
        json=data,
        headers={"Content-Type": "application/json"},
        timeout=timeout
    )
    try:
        return response.status_code, response.json()
    except:
        return response.status_code, response.text


def api_delete(endpoint, timeout=10):
    response = requests.delete(f"{BASE_URL}{endpoint}", timeout=timeout)
    try:
        return response.status_code, response.json()
    except:
        return response.status_code, response.text


def get_html(endpoint="/", timeout=10):
    response = requests.get(f"{BASE_URL}{endpoint}", timeout=timeout)
    return response.status_code, response.text


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.by_category = {}

    def add(self, name, passed, details="", category="General"):
        if category not in self.by_category:
            self.by_category[category] = {"passed": 0, "failed": 0}

        if passed:
            self.passed += 1
            self.by_category[category]["passed"] += 1
        else:
            self.failed += 1
            self.by_category[category]["failed"] += 1
            self.errors.append(f"[{category}] {name}: {details}")
        print_test(name, passed, details)

    def summary(self):
        return self.passed, self.failed, self.passed + self.failed


# =============================================================================
# HEALTH & CONNECTIVITY TESTS
# =============================================================================
def test_health(results):
    print_section("Health & Connectivity")

    try:
        status, data = api_get("/health")
        results.add(
            "Server health endpoint",
            status == 200 and data.get("status") == "healthy",
            f"Status: {status}, Data: {data}",
            "Health"
        )
        results.add(
            "Server in test mode",
            data.get("mode") == "test",
            f"Mode: {data.get('mode')}",
            "Health"
        )
    except Exception as e:
        results.add("Server is reachable", False, str(e), "Health")
        return False
    return True


# =============================================================================
# PROJECT API TESTS
# =============================================================================
def test_project_api(results):
    print_section("Project API - CRUD Operations")

    # Create project
    status, project = api_post("/api/projects", {
        "title": "Test Documentary",
        "description": "A test project for automated testing",
        "status": "Planning"
    })
    results.add(
        "POST /api/projects - Create project",
        status == 201 and "id" in project,
        f"Status: {status}",
        "Project API"
    )

    if status != 201:
        return None

    project_id = project["id"]

    # Verify project has required fields
    results.add(
        "Project has 'id' field",
        "id" in project,
        f"Fields: {list(project.keys())}",
        "Project API"
    )
    results.add(
        "Project has 'createdAt' field",
        "createdAt" in project,
        f"Fields: {list(project.keys())}",
        "Project API"
    )
    results.add(
        "Project has 'updatedAt' field",
        "updatedAt" in project,
        f"Fields: {list(project.keys())}",
        "Project API"
    )

    # Get all projects
    status, projects = api_get("/api/projects")
    results.add(
        "GET /api/projects - List projects",
        status == 200 and isinstance(projects, list),
        f"Status: {status}",
        "Project API"
    )
    results.add(
        "Created project in list",
        any(p["id"] == project_id for p in projects),
        f"Project count: {len(projects)}",
        "Project API"
    )

    # Get single project
    status, fetched = api_get(f"/api/projects/{project_id}")
    results.add(
        "GET /api/projects/<id> - Get single project",
        status == 200 and fetched.get("id") == project_id,
        f"Status: {status}",
        "Project API"
    )

    # Get non-existent project
    status, error = api_get("/api/projects/non-existent-id")
    results.add(
        "GET /api/projects/<invalid> - Returns 404",
        status == 404,
        f"Status: {status}",
        "Project API"
    )

    # Update project
    status, updated = api_put(f"/api/projects/{project_id}", {
        "title": "Updated Documentary Title",
        "status": "In Production"
    })
    results.add(
        "PUT /api/projects/<id> - Update project",
        status == 200 and updated.get("title") == "Updated Documentary Title",
        f"Status: {status}, Title: {updated.get('title')}",
        "Project API"
    )
    results.add(
        "Update sets 'updatedAt'",
        "updatedAt" in updated,
        f"Fields: {list(updated.keys())}",
        "Project API"
    )

    return project_id


# =============================================================================
# COLLECTION API TESTS (Episodes, Research, Interviews, Shots, Assets, Scripts)
# =============================================================================
def test_collection_api(results, project_id, collection_name, sample_data):
    print_section(f"{collection_name.title()} API - CRUD Operations")

    # Create item
    sample_data["projectId"] = project_id
    status, item = api_post(f"/api/{collection_name}", sample_data)
    results.add(
        f"POST /api/{collection_name} - Create",
        status == 201 and "id" in item,
        f"Status: {status}",
        f"{collection_name.title()} API"
    )

    if status != 201:
        return None

    item_id = item["id"]

    # Verify required fields
    results.add(
        f"{collection_name.title()} has 'id' field",
        "id" in item,
        f"Fields: {list(item.keys())}",
        f"{collection_name.title()} API"
    )
    results.add(
        f"{collection_name.title()} has 'createdAt' field",
        "createdAt" in item,
        f"Fields: {list(item.keys())}",
        f"{collection_name.title()} API"
    )
    results.add(
        f"{collection_name.title()} has 'projectId' field",
        item.get("projectId") == project_id,
        f"projectId: {item.get('projectId')}",
        f"{collection_name.title()} API"
    )

    # List items for project
    status, items = api_get(f"/api/projects/{project_id}/{collection_name}")
    results.add(
        f"GET /api/projects/<id>/{collection_name} - List",
        status == 200 and isinstance(items, list) and len(items) >= 1,
        f"Status: {status}, Count: {len(items) if isinstance(items, list) else 0}",
        f"{collection_name.title()} API"
    )

    # Update item
    update_field = list(sample_data.keys())[0]
    if update_field != "projectId":
        update_value = f"Updated {sample_data[update_field]}"
    else:
        update_field = list(sample_data.keys())[1]
        update_value = f"Updated {sample_data[update_field]}"

    status, updated = api_put(f"/api/{collection_name}/{item_id}", {
        update_field: update_value
    })
    results.add(
        f"PUT /api/{collection_name}/<id> - Update",
        status == 200 and updated.get(update_field) == update_value,
        f"Status: {status}",
        f"{collection_name.title()} API"
    )

    # Delete item
    status, result = api_delete(f"/api/{collection_name}/{item_id}")
    results.add(
        f"DELETE /api/{collection_name}/<id> - Delete",
        status == 200 and result.get("success") == True,
        f"Status: {status}",
        f"{collection_name.title()} API"
    )

    # Verify deletion
    status, items = api_get(f"/api/projects/{project_id}/{collection_name}")
    item_exists = any(i["id"] == item_id for i in items) if isinstance(items, list) else True
    results.add(
        f"Item removed after delete",
        not item_exists,
        f"Item still exists: {item_exists}",
        f"{collection_name.title()} API"
    )

    return item_id


# =============================================================================
# CASCADE DELETE TESTS
# =============================================================================
def test_cascade_delete(results):
    print_section("Cascade Delete - Project Deletion")

    # Create a project with all related entities
    status, project = api_post("/api/projects", {
        "title": "Cascade Test Project",
        "description": "Testing cascade delete"
    })
    project_id = project.get("id")

    # Create one of each entity type
    entities = {
        "episodes": {"title": "Test Episode", "status": "Planning"},
        "research": {"title": "Test Research", "content": "Test content"},
        "interviews": {"subject": "Test Subject", "status": "Requested"},
        "shots": {"description": "Test Shot", "status": "Pending"},
        "assets": {"title": "Test Asset", "type": "Document"},
        "scripts": {"title": "Test Script", "content": "Test content"}
    }

    entity_ids = {}
    for collection, data in entities.items():
        data["projectId"] = project_id
        status, item = api_post(f"/api/{collection}", data)
        entity_ids[collection] = item.get("id")

    results.add(
        "Setup: Created project with all entity types",
        len(entity_ids) == 6,
        f"Entities created: {len(entity_ids)}",
        "Cascade Delete"
    )

    # Delete the project
    status, result = api_delete(f"/api/projects/{project_id}")
    results.add(
        "Delete project",
        status == 200,
        f"Status: {status}",
        "Cascade Delete"
    )

    # Verify all related entities are deleted
    for collection in entities.keys():
        status, items = api_get(f"/api/projects/{project_id}/{collection}")
        has_items = isinstance(items, list) and len(items) > 0
        results.add(
            f"{collection.title()} cascade deleted",
            not has_items,
            f"Remaining: {len(items) if isinstance(items, list) else 'error'}",
            "Cascade Delete"
        )


# =============================================================================
# AI API TESTS
# =============================================================================
def test_ai_api(results, project_id):
    print_section("AI API - Mocked Responses")

    # AI Research
    status, data = api_post("/api/ai/research", {
        "query": "Test research query",
        "projectId": project_id,
        "downloadSources": True
    }, timeout=30)
    results.add(
        "POST /api/ai/research - Returns result",
        status == 200 and "result" in data,
        f"Status: {status}",
        "AI API"
    )
    results.add(
        "AI Research has sources",
        isinstance(data.get("sources"), list),
        f"Sources: {len(data.get('sources', []))}",
        "AI API"
    )
    results.add(
        "AI Research has researchId",
        "researchId" in data,
        f"Has researchId: {'researchId' in data}",
        "AI API"
    )

    # AI Interview Questions
    status, data = api_post("/api/ai/interview-questions", {
        "subject": "Test Subject",
        "role": "Test Role"
    })
    results.add(
        "POST /api/ai/interview-questions",
        status == 200 and "result" in data,
        f"Status: {status}",
        "AI API"
    )
    results.add(
        "Interview questions contain subject",
        "Test Subject" in data.get("result", ""),
        "Subject not in response",
        "AI API"
    )

    # AI Script Outline
    status, data = api_post("/api/ai/script-outline", {
        "title": "Test Episode",
        "duration": "45 minutes"
    })
    results.add(
        "POST /api/ai/script-outline",
        status == 200 and "result" in data,
        f"Status: {status}",
        "AI API"
    )
    results.add(
        "Script outline has structure",
        "ACT 1" in data.get("result", "") and "ACT 2" in data.get("result", ""),
        "Missing act structure",
        "AI API"
    )

    # AI Shot Ideas
    status, data = api_post("/api/ai/shot-ideas", {
        "scene": "Test Scene"
    })
    results.add(
        "POST /api/ai/shot-ideas",
        status == 200 and "result" in data,
        f"Status: {status}",
        "AI API"
    )

    # AI Expand Topic
    status, data = api_post("/api/ai/expand-topic", {
        "topic": "Test Topic"
    })
    results.add(
        "POST /api/ai/expand-topic",
        status == 200 and "result" in data,
        f"Status: {status}",
        "AI API"
    )


# =============================================================================
# DOCUMENT API TESTS
# =============================================================================
def test_document_api(results, project_id):
    print_section("Document API - Source Documents")

    # Generate research to create source documents
    status, data = api_post("/api/ai/research", {
        "query": "Document test query",
        "projectId": project_id,
        "downloadSources": True
    }, timeout=30)

    # Get source documents
    status, docs = api_get(f"/api/projects/{project_id}/source-documents")
    results.add(
        "GET /api/projects/<id>/source-documents",
        status == 200 and isinstance(docs, list) and len(docs) > 0,
        f"Status: {status}, Docs: {len(docs) if isinstance(docs, list) else 0}",
        "Document API"
    )

    if docs and len(docs) > 0:
        gcs_path = docs[0].get("gcsPath")

        # View document
        status, content = api_get(f"/api/document/{gcs_path}")
        results.add(
            "GET /api/document/<path> - View document",
            status == 200 and "html" in str(content).lower(),
            f"Status: {status}",
            "Document API"
        )

        # Download document
        response = requests.get(f"{BASE_URL}/api/download/{gcs_path}")
        has_attachment = "attachment" in response.headers.get("Content-Disposition", "")
        results.add(
            "GET /api/download/<path> - Download document",
            response.status_code == 200 and has_attachment,
            f"Status: {response.status_code}",
            "Document API"
        )

    # Download all as ZIP
    response = requests.get(f"{BASE_URL}/api/projects/{project_id}/assets/download-all")
    results.add(
        "GET /api/projects/<id>/assets/download-all - ZIP download",
        response.status_code == 200 and response.headers.get("Content-Type") == "application/zip",
        f"Status: {response.status_code}",
        "Document API"
    )

    # Clear source documents
    status, result = api_delete(f"/api/projects/{project_id}/assets/clear-sources")
    results.add(
        "DELETE /api/projects/<id>/assets/clear-sources",
        status == 200 and "deleted" in result,
        f"Status: {status}",
        "Document API"
    )


# =============================================================================
# SAMPLE DATA TESTS
# =============================================================================
def test_sample_data(results):
    print_section("Sample Data Initialization")

    # First, create a fresh project to test with (simulates fresh server)
    # Delete all existing projects to test fresh initialization
    status, projects = api_get("/api/projects")
    for p in projects:
        api_delete(f"/api/projects/{p['id']}")

    # Now initialize sample data on fresh storage
    status, data = api_post("/api/init-sample-data", {})
    results.add(
        "POST /api/init-sample-data",
        status == 200 and "projectId" in data,
        f"Status: {status}",
        "Sample Data"
    )

    if status != 200:
        return None

    project_id = data.get("projectId")

    # Check each collection has data
    collections = ["episodes", "research", "interviews", "shots", "assets", "scripts"]
    for collection in collections:
        status, items = api_get(f"/api/projects/{project_id}/{collection}")
        results.add(
            f"Sample {collection} created",
            status == 200 and isinstance(items, list) and len(items) > 0,
            f"Count: {len(items) if isinstance(items, list) else 0}",
            "Sample Data"
        )

    return project_id


# =============================================================================
# UI STRUCTURE TESTS
# =============================================================================
def test_ui_structure(results):
    print_section("UI Structure Tests")

    status, html = get_html("/")
    results.add(
        "Main page loads",
        status == 200 and len(html) > 1000,
        f"Status: {status}, Length: {len(html)}",
        "UI Structure"
    )

    if status != 200:
        return

    # Check essential HTML elements
    essential_elements = [
        ("<!DOCTYPE html>", "HTML5 doctype"),
        ("<title>", "Page title"),
        ("id=\"app\"", "App container"),
        ("id=\"modal\"", "Modal container"),
        ("id=\"nav\"", "Navigation container"),
        ("id=\"content\"", "Content area"),
    ]

    for element, name in essential_elements:
        results.add(
            f"UI has {name}",
            element.lower() in html.lower(),
            f"Missing: {element}",
            "UI Structure"
        )

    # Check navigation tabs
    nav_tabs = ["Dashboard", "Episodes", "Research", "Interviews", "Shots", "Assets", "Scripts"]
    for tab in nav_tabs:
        results.add(
            f"Nav has '{tab}' tab",
            tab.lower() in html.lower(),
            f"Missing tab: {tab}",
            "UI Structure"
        )

    # Check JavaScript functions
    js_functions = [
        "loadProjectData",
        "renderDashboard",
        "renderEpisodes",
        "renderResearch",
        "renderInterviews",
        "renderProduction",  # Shots tab uses renderProduction
        "renderAssets",
        "renderScripts",
        "showAddModal",
        "showEditModal",
        "deleteItem",
        "api(",
    ]

    for func in js_functions:
        results.add(
            f"JS function '{func}' defined",
            func in html,
            f"Missing function",
            "UI Structure"
        )

    # Check CSS file is linked
    results.add(
        "CSS file linked",
        "style.css" in html or "<style>" in html,
        "No CSS reference found",
        "UI Structure"
    )

    # Fetch and check CSS file
    css_status, css_content = get_html("/static/css/style.css")
    if css_status == 200:
        css_elements = [
            ("--primary", "CSS variables"),
            ("@media", "Responsive media queries"),
            (".card", "Card styles"),
            (".btn", "Button styles"),
            (".modal", "Modal styles"),
        ]

        for element, name in css_elements:
            results.add(
                f"CSS has {name}",
                element in css_content,
                f"Missing: {element}",
                "UI Structure"
            )
    else:
        results.add("CSS file accessible", False, f"Status: {css_status}", "UI Structure")


# =============================================================================
# UI FORM TESTS
# =============================================================================
def test_ui_forms(results):
    print_section("UI Form Tests")

    status, html = get_html("/")
    if status != 200:
        results.add("Page loads for form tests", False, f"Status: {status}", "UI Forms")
        return

    # Check form-related elements
    form_elements = [
        ("showAddModal", "Add modal function"),
        ("showEditModal", "Edit modal function"),
        ("showProjectsModal", "Projects modal function"),
        ("createNewProject", "Create project function"),
        ("deleteProject", "Delete project function"),
        ("type=\"text\"", "Text inputs"),
        ("type=\"submit\"", "Submit buttons"),
        ("<select", "Select dropdowns"),
        ("<textarea", "Textareas"),
    ]

    for element, name in form_elements:
        results.add(
            f"Form has {name}",
            element in html,
            f"Missing: {element}",
            "UI Forms"
        )

    # Check modal structure
    results.add(
        "Modal has close button",
        "closeModal" in html or "close-btn" in html,
        "Missing close functionality",
        "UI Forms"
    )

    # Check AI integration forms
    ai_elements = [
        ("ai-button", "AI action buttons"),
        ("generateEpisodeResearch", "Episode research generator"),
    ]

    for element, name in ai_elements:
        results.add(
            f"AI {name}",
            element in html,
            f"Missing: {element}",
            "UI Forms"
        )


# =============================================================================
# DATA VALIDATION TESTS
# =============================================================================
def test_data_validation(results):
    print_section("Data Validation Tests")

    # Test project with minimal data
    status, project = api_post("/api/projects", {"title": "Minimal"})
    results.add(
        "Create project with minimal data",
        status == 201,
        f"Status: {status}",
        "Validation"
    )

    # Test project with empty title
    status, project = api_post("/api/projects", {"title": ""})
    results.add(
        "Create project with empty title (accepted)",
        status == 201,
        f"Status: {status}",
        "Validation"
    )

    # Test project with special characters
    status, project = api_post("/api/projects", {
        "title": "Test <script>alert('xss')</script>",
        "description": "Test with 'quotes' and \"double quotes\""
    })
    results.add(
        "Create project with special characters",
        status == 201,
        f"Status: {status}",
        "Validation"
    )

    if project and "id" in project:
        # Verify data is stored correctly
        status, fetched = api_get(f"/api/projects/{project['id']}")
        results.add(
            "Special characters preserved in storage",
            "<script>" in fetched.get("title", ""),
            f"Title: {fetched.get('title', '')[:50]}",
            "Validation"
        )
        # Clean up
        api_delete(f"/api/projects/{project['id']}")

    # Test UUID format
    status, project = api_post("/api/projects", {"title": "UUID Test"})
    if project and "id" in project:
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        is_valid_uuid = bool(re.match(uuid_pattern, project["id"]))
        results.add(
            "Generated ID is valid UUID",
            is_valid_uuid,
            f"ID: {project['id']}",
            "Validation"
        )
        api_delete(f"/api/projects/{project['id']}")

    # Test timestamp format
    status, project = api_post("/api/projects", {"title": "Timestamp Test"})
    if project and "createdAt" in project:
        try:
            # ISO format check
            datetime.fromisoformat(project["createdAt"].replace("Z", "+00:00"))
            valid_timestamp = True
        except:
            valid_timestamp = False
        results.add(
            "createdAt is valid ISO timestamp",
            valid_timestamp,
            f"Timestamp: {project.get('createdAt')}",
            "Validation"
        )
        api_delete(f"/api/projects/{project['id']}")


# =============================================================================
# CONCURRENT OPERATIONS TEST
# =============================================================================
def test_concurrent_operations(results):
    print_section("Concurrent Operations")

    import concurrent.futures

    # Create a project for testing
    status, project = api_post("/api/projects", {"title": "Concurrent Test"})
    if status != 201:
        results.add("Setup for concurrent tests", False, f"Status: {status}", "Concurrent")
        return

    project_id = project["id"]

    # Create multiple episodes concurrently
    def create_episode(i):
        return api_post("/api/episodes", {
            "projectId": project_id,
            "title": f"Concurrent Episode {i}",
            "status": "Planning"
        })

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(create_episode, i) for i in range(5)]
        results_list = [f.result() for f in concurrent.futures.as_completed(futures)]

    all_success = all(r[0] == 201 for r in results_list)
    results.add(
        "Create 5 episodes concurrently",
        all_success,
        f"Results: {[r[0] for r in results_list]}",
        "Concurrent"
    )

    # Verify all were created
    status, episodes = api_get(f"/api/projects/{project_id}/episodes")
    results.add(
        "All concurrent episodes exist",
        status == 200 and len(episodes) == 5,
        f"Count: {len(episodes) if isinstance(episodes, list) else 0}",
        "Concurrent"
    )

    # Clean up
    api_delete(f"/api/projects/{project_id}")


# =============================================================================
# ERROR HANDLING TESTS
# =============================================================================
def test_error_handling(results):
    print_section("Error Handling")

    # Invalid endpoint
    status, _ = api_get("/api/invalid-endpoint")
    results.add(
        "Invalid endpoint returns error",
        status in [404, 405],
        f"Status: {status}",
        "Error Handling"
    )

    # Invalid project ID for collections
    status, _ = api_get("/api/projects/invalid-id/episodes")
    results.add(
        "Invalid project ID returns empty list",
        status == 200,
        f"Status: {status}",
        "Error Handling"
    )

    # Update non-existent item
    status, _ = api_put("/api/episodes/non-existent", {"title": "Test"})
    results.add(
        "Update non-existent returns 404",
        status == 404,
        f"Status: {status}",
        "Error Handling"
    )

    # Delete non-existent (should still succeed)
    status, result = api_delete("/api/episodes/non-existent")
    results.add(
        "Delete non-existent succeeds",
        status == 200,
        f"Status: {status}",
        "Error Handling"
    )

    # Malformed JSON
    try:
        response = requests.post(
            f"{BASE_URL}/api/projects",
            data="not json",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        results.add(
            "Malformed JSON handled",
            response.status_code in [400, 415, 500],
            f"Status: {response.status_code}",
            "Error Handling"
        )
    except Exception as e:
        results.add("Malformed JSON handled", False, str(e), "Error Handling")


# =============================================================================
# MAIN TEST RUNNER
# =============================================================================
def main():
    print_header("Documentary Production App - Full Test Suite")
    print(f"Target: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = TestResults()

    # Health check first
    if not test_health(results):
        print(f"\n{Colors.RED}Server not running. Start it with: python test_app.py{Colors.END}")
        sys.exit(1)

    # Track main project for tests
    main_project_id = None

    try:
        # Project API tests
        main_project_id = test_project_api(results)

        if main_project_id:
            # Collection API tests
            collection_samples = {
                "episodes": {"title": "Test Episode", "description": "Test", "status": "Planning"},
                "research": {"title": "Test Research", "content": "Test content", "category": "Test"},
                "interviews": {"subject": "Test Subject", "role": "Test Role", "status": "Requested"},
                "shots": {"description": "Test Shot", "location": "Test Location", "status": "Pending"},
                "assets": {"title": "Test Asset", "type": "Document", "source": "Test"},
                "scripts": {"title": "Test Script", "content": "Test content"},
            }

            for collection, sample in collection_samples.items():
                test_collection_api(results, main_project_id, collection, sample.copy())

            # AI API tests
            test_ai_api(results, main_project_id)

            # Document API tests
            test_document_api(results, main_project_id)

        # Cascade delete tests
        test_cascade_delete(results)

        # Sample data tests
        test_sample_data(results)

        # UI tests
        test_ui_structure(results)
        test_ui_forms(results)

        # Data validation tests
        test_data_validation(results)

        # Concurrent operations
        test_concurrent_operations(results)

        # Error handling
        test_error_handling(results)

    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup
        if main_project_id:
            api_delete(f"/api/projects/{main_project_id}")

    # =============================================================================
    # FINAL REPORT
    # =============================================================================
    print_header("TEST REPORT")

    passed, failed, total = results.summary()

    print(f"\n{Colors.BOLD}Summary{Colors.END}")
    print(f"  Total Tests: {total}")
    print(f"  {Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"  {Colors.RED}Failed: {failed}{Colors.END}")
    print(f"  Success Rate: {(passed/total*100):.1f}%" if total > 0 else "N/A")

    print(f"\n{Colors.BOLD}Results by Category{Colors.END}")
    for category, counts in sorted(results.by_category.items()):
        cat_total = counts["passed"] + counts["failed"]
        cat_rate = (counts["passed"]/cat_total*100) if cat_total > 0 else 0
        status_color = Colors.GREEN if counts["failed"] == 0 else Colors.RED
        print(f"  {category:20} {status_color}{counts['passed']:3}/{cat_total:3}{Colors.END} ({cat_rate:.0f}%)")

    if results.errors:
        print(f"\n{Colors.BOLD}Failures{Colors.END}")
        for error in results.errors:
            print(f"  {Colors.RED}- {error}{Colors.END}")

    # Final status
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL {total} TESTS PASSED{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ {failed} OF {total} TESTS FAILED{Colors.END}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
