"""Smoke tests for profile selection and generator outputs."""

from __future__ import annotations

import csv
import pathlib
import tempfile
import unittest

import generate_opengd_import as gen


class ProfileSmokeTest(unittest.TestCase):
    def test_chicago_light_profile_produces_channels(self) -> None:
        profile = gen.load_profile("chicago_light")
        files = gen.resolve_ssrf_files(profile)
        self.assertGreaterEqual(len(files), 1)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = pathlib.Path(tmpdir)
            gen.main(["--profile", "chicago_light", "--output-dir", str(output_dir)])

            channels_path = output_dir / "Channels.csv"
            self.assertTrue(channels_path.exists(), "Channels.csv not generated")

            with channels_path.open(newline="") as fh:
                reader = csv.reader(fh)
                header = next(reader, None)
                self.assertEqual(header, gen.CHANNELS_HEADER)
                rows = list(reader)
                self.assertGreaterEqual(
                    len(rows), 1, "Expected at least one channel row"
                )


if __name__ == "__main__":
    unittest.main()
