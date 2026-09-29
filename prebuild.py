import subprocess


subprocess.run(
	[
		"uv",
		"export",
		"--no-dev",
		"--no-hashes",
		"--format",
		"requirements.txt",
		"--output-file",
		"requirements.txt",
	],
	check=True,
)
subprocess.run(
	[
		"uv",
		"export",
		"--no-dev",
		"--group",
		"docs",
		"--no-hashes",
		"--format",
		"requirements.txt",
		"--output-file",
		"docs/requirements.txt",
	],
	check=True,
)