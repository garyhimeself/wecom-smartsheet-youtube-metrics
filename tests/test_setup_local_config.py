from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "setup-local-config.ps1"


class SetupLocalConfigScriptTests(unittest.TestCase):
    def test_uses_a_masked_windows_dialog_and_writes_only_local_env(self):
        content = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("System.Windows.Forms", content)
        self.assertIn("UseSystemPasswordChar", content)
        self.assertIn("AcceptButton", content)
        self.assertIn("YOUTUBE_API_KEY=", content)
        self.assertIn("Set-Content -LiteralPath $envPath", content)
        self.assertNotIn("Write-Host $apiKey", content)


if __name__ == "__main__":
    unittest.main()
