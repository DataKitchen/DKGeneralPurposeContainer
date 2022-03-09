import unittest
from unittest.mock import patch
from AnalyticContainerLibrary.ACSingletons import ACHelpers


class TestACSingletons(unittest.TestCase):

    @patch.dict('os.environ', {'SECRET_SECRET1': 'value1'})
    def test_resolve_vault_references(self):

        self.assertEqual('value1', ACHelpers.resolve_vault_references('#{vault://secret1}'))
        self.assertEqual('x value1 x', ACHelpers.resolve_vault_references('x #{vault://secret1} x'))
        self.assertEqual({'x': 'value1'}, ACHelpers.resolve_vault_references({'x': '#{vault://secret1}'}))
