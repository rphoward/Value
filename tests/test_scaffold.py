"""Portable scaffold smoke test."""

import unittest

from value.presentation.app import create_app


class ScaffoldTests(unittest.TestCase):
    def test_app_factory(self):
        app = create_app()
        self.assertIsNotNone(app)


if __name__ == "__main__":
    unittest.main()
