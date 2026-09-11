"""Regression checks for the blank macOS window; no graphical display needed."""
import sys
import types
import unittest
from unittest.mock import patch

import assemblage_3d as app


class LauncherTests(unittest.TestCase):
    def tk(self, version):
        return patch.dict(sys.modules, tkinter=types.SimpleNamespace(TkVersion=version))

    def test_old_apple_tk_relaunches_with_arguments(self):
        with self.tk(8.5), patch.object(sys, 'platform', 'darwin'), \
                patch.object(sys, 'argv', ['assemblage_3d.py', '--example']), \
                patch.object(app, 'python_avec_tk_recent', return_value='/modern/python3'), \
                patch.object(app.os, 'execv', side_effect=SystemExit) as execute:
            with self.assertRaises(SystemExit):
                app.preparer_interface()
            execute.assert_called_once_with('/modern/python3', [
                '/modern/python3', str(app.Path(app.__file__).resolve()), '--example'])

    def test_old_apple_tk_without_alternative_gives_useful_error(self):
        with self.tk(8.5), patch.object(sys, 'platform', 'darwin'), \
                patch.object(app, 'python_avec_tk_recent', return_value=None):
            with self.assertRaisesRegex(RuntimeError, 'python.org'):
                app.preparer_interface()

    def test_modern_tk_does_not_relaunch(self):
        for version in [8.6, 9.0]:
            with self.subTest(version=version), self.tk(version), \
                    patch.object(sys, 'platform', 'darwin'), \
                    patch.object(app.os, 'execv') as execute:
                app.preparer_interface()
                execute.assert_not_called()

    def test_linux_does_not_apply_apple_workaround(self):
        with self.tk(8.5), patch.object(sys, 'platform', 'linux'), \
                patch.object(app.os, 'execv') as execute:
            app.preparer_interface()
            execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()
