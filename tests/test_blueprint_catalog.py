import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from blueprint_catalog import load_blueprint_catalog


class BlueprintCatalogTests(unittest.TestCase):
    def test_repository_catalog(self):
        path = Path(__file__).resolve().parents[1] / "data" / "blueprints.json"
        self.assertEqual(load_blueprint_catalog(path)["schema_version"], 1)

    def test_external_entry(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "catalog.json"
            path.write_text(json.dumps({"schema_version": 1, "blueprints": [
                {"id": "example", "name": "Example", "source": "test-only"}]}), encoding="utf-8")
            self.assertEqual(load_blueprint_catalog(path)["blueprints"][0]["id"], "example")

    def test_duplicate_ids_rejected(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "catalog.json"
            path.write_text(json.dumps({"schema_version": 1, "blueprints": [
                {"id": "a", "name": "A"}, {"id": "a", "name": "B"}]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_blueprint_catalog(path)

    def test_schema_rejected(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "catalog.json"
            path.write_text('{"schema_version":2,"blueprints":[]}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_blueprint_catalog(path)


if __name__ == "__main__":
    unittest.main()
