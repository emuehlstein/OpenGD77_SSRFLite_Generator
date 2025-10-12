"""Smoke tests for profile selection and generator outputs."""

from __future__ import annotations

import csv
import pathlib
import tempfile
import unittest

import sys

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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

            gmrs_rows = [row for row in rows if "GMRS" in row[1]]
            if gmrs_rows:
                self.assertTrue(
                    all(row[17] == "Yes" for row in gmrs_rows),
                    "GMRS channels should default to Rx Only when no GMRS TX flag is provided",
                )

    def test_gmrs_tx_service_flag_enables_transmit(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = pathlib.Path(tmpdir)
            gen.main(
                [
                    "--profile",
                    "chicago_light",
                    "--output-dir",
                    str(output_dir),
                    "--tx-service",
                    "gmrs",
                ]
            )

            channels_path = output_dir / "Channels.csv"
            self.assertTrue(channels_path.exists(), "Channels.csv not generated")

            with channels_path.open(newline="") as fh:
                reader = csv.reader(fh)
                next(reader, None)  # skip header
                gmrs_rows = [row for row in reader if "GMRS" in row[1]]
            self.assertTrue(
                gmrs_rows, "Expected GMRS rows when GMRS service is included"
            )
            self.assertTrue(
                any(row[17] == "No" for row in gmrs_rows),
                "At least one GMRS channel should allow transmit when GMRS service is permitted",
            )


if __name__ == "__main__":
    unittest.main()
