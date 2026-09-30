"""Regression tests for the collection checker, using disposable fixtures."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.check_collection import BUNDLED, MANUAL_ONLY, REQUIRED, check


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for name in REQUIRED:
            flag = "disable-model-invocation: true\n" if name in MANUAL_ONLY else ""
            self.write(f"{name}/SKILL.md", f"---\nname: {name}\ndescription: Test fixture\n{flag}---\n# Fixture\n")
        for relative in BUNDLED:
            self.write(relative, "# Reference\n")

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def metadata(self, text):
        self.write("software-factory/SKILL.md", text)

    def assert_error(self, fragment):
        self.assertTrue(any(fragment in error for error in check(self.root)), check(self.root))

    def test_valid_collection(self):
        self.assertEqual(check(self.root), [])

    def test_required_skill_missing(self):
        (self.root / "new-feature/SKILL.md").unlink()
        self.assert_error("missing required skill")

    def test_bundle_missing(self):
        (self.root / "software-factory/PREREQUISITES.md").unlink()
        self.assert_error("missing bundled reference")

    def test_name_matches_directory(self):
        self.metadata("---\nname: other\ndescription: Test\ndisable-model-invocation: true\n---\n")
        self.assert_error("name must match directory")

    def test_frontmatter_required(self):
        self.metadata("# No frontmatter\n")
        self.assert_error("invalid frontmatter")

    def test_invalid_yaml(self):
        self.metadata("---\nname: [broken\n---\n")
        self.assert_error("invalid frontmatter")

    def test_duplicate_yaml_keys(self):
        self.metadata("---\nname: software-factory\nname: other\n---\n")
        self.assert_error("duplicate frontmatter key")

    def test_empty_description(self):
        self.metadata("---\nname: software-factory\ndescription: ''\ndisable-model-invocation: true\n---\n")
        self.assert_error("description must contain")

    def test_name_type(self):
        self.metadata("---\nname: 7\ndescription: Test\n---\n")
        self.assert_error("invalid skill name")

    def test_manual_flag_missing(self):
        self.metadata("---\nname: software-factory\ndescription: Test\n---\n")
        self.assert_error("must remain manual-only")

    def test_quoted_true_is_not_boolean(self):
        self.metadata("---\nname: software-factory\ndescription: Test\ndisable-model-invocation: 'true'\n---\n")
        self.assert_error("must be a YAML boolean")
        self.assert_error("must remain manual-only")

    def test_metadata_mapping_allowed(self):
        self.metadata("---\nname: software-factory\ndescription: Test\nmetadata:\n  version: '2.0'\ndisable-model-invocation: true\n---\n")
        self.assertEqual(check(self.root), [])

    def test_missing_local_link(self):
        self.write("README.md", "[Missing](missing.md)\n")
        self.assert_error("missing link target")

    def test_valid_relative_link_and_anchor(self):
        self.write("software-factory/PREREQUISITES.md", "# Setup\n## Review tools\n## Review tools\n")
        self.write("README.md", "[Review](software-factory/PREREQUISITES.md#review-tools-1)\n")
        self.assertEqual(check(self.root), [])

    def test_missing_anchor(self):
        self.write("README.md", "[Review](software-factory/PREREQUISITES.md#absent)\n")
        self.assert_error("missing heading anchor")

    def test_missing_image(self):
        self.write("README.md", "![Image](missing.png)\n")
        self.assert_error("missing link target")

    def test_external_links_and_fenced_examples_ignored(self):
        self.write("README.md", "[External](https://example.org/no-check#missing)\n```markdown\n[Example](missing.md)\n```\n")
        self.assertEqual(check(self.root), [])

    def test_removed_directory(self):
        (self.root / "greploop").mkdir()
        self.assert_error("removed skill directory")

    def test_removed_invocation(self):
        self.write("README.md", "Invoke `/skill:before-and-after`.\n")
        self.assert_error("invocation of removed skill")

    def test_removal_explanation_allowed(self):
        self.write("README.md", "The before-and-after skill was removed.\n")
        self.assertEqual(check(self.root), [])

    def test_cli_exit_status(self):
        script = Path(__file__).resolve().parents[1] / "tools/check_collection.py"
        success = subprocess.run([sys.executable, str(script), str(self.root)], capture_output=True, text=True)
        self.assertEqual(success.returncode, 0, success.stderr)
        self.write("README.md", "[Missing](missing.md)\n")
        failure = subprocess.run([sys.executable, str(script), str(self.root)], capture_output=True, text=True)
        self.assertEqual(failure.returncode, 1)
        self.assertIn("missing link target", failure.stderr)


if __name__ == "__main__":
    unittest.main()
