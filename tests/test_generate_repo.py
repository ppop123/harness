import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

import generate_repo as gen


ROOT = Path(__file__).resolve().parents[1]


class GenerateRepoContractTests(unittest.TestCase):
    def _run_layer_check(self, script: str, files: dict[str, str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            script_path = tmp_path / "layer-check.sh"
            src_dir = tmp_path / "src"
            script_path.write_text(script, encoding="utf-8")
            for rel_path, content in files.items():
                path = src_dir / rel_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            return subprocess.run(
                ["bash", str(script_path), str(src_dir)],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_ts_nextjs_layer_check_flags_types_importing_services(self) -> None:
        script = gen.gen_layer_check(gen.STACKS["ts-nextjs"])
        result = self._run_layer_check(
            script,
            {
                "types/user.ts": 'import { svc } from "../services/svc";\n',
                "services/svc.ts": "export const svc = 1;\n",
            },
        )

        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"layer-check should fail on obvious violations:\n{result.stdout}\n{result.stderr}",
        )
        self.assertIn("VIOLATION", result.stdout)

    def test_ts_nextjs_layer_check_does_not_confuse_leaf_filename_with_api_layer(self) -> None:
        script = gen.gen_layer_check(gen.STACKS["ts-nextjs"])
        result = self._run_layer_check(
            script,
            {
                "types/user.ts": 'import { api } from "../services/api";\n',
                "services/api.ts": "export const api = 1;\n",
            },
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("higher-layer dependency 'services'", result.stdout)
        self.assertNotIn("higher-layer dependency 'api'", result.stdout)

    def test_ts_nextjs_layer_check_ignores_comment_only_reference(self) -> None:
        script = gen.gen_layer_check(gen.STACKS["ts-nextjs"])
        result = self._run_layer_check(
            script,
            {
                "types/user.ts": "// services stay in the service layer\nexport type UserId = string;\n",
            },
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"comments should not trigger layer violations:\n{result.stdout}\n{result.stderr}",
        )

    def test_python_fastapi_layer_check_flags_services_import(self) -> None:
        script = gen.gen_layer_check(gen.STACKS["python-fastapi"])
        result = self._run_layer_check(
            script,
            {
                "models/user.py": "from src.services.user import load_user\n",
                "services/user.py": "def load_user() -> None:\n    return None\n",
            },
        )

        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"python imports should be parsed as real dependencies:\n{result.stdout}\n{result.stderr}",
        )
        self.assertIn("VIOLATION", result.stdout)

    def test_python_fastapi_layer_check_ignores_string_and_comment_literals(self) -> None:
        script = gen.gen_layer_check(gen.STACKS["python-fastapi"])
        result = self._run_layer_check(
            script,
            {
                "models/user.py": '# services should stay below models\nNOTE = "services live elsewhere"\n',
            },
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"strings/comments should not trigger python violations:\n{result.stdout}\n{result.stderr}",
        )

    def test_platform_docs_use_neutral_progress_file_and_self_contained_claude(self) -> None:
        claude_doc = gen.gen_claude_md(gen.STACKS["ts-nextjs"])
        agents_doc = gen.gen_agents_md(gen.STACKS["ts-nextjs"])

        self.assertIn("agent-progress.txt", claude_doc)
        self.assertIn("agent-progress.txt", agents_doc)
        self.assertNotIn("claude-progress.txt", claude_doc)
        self.assertNotIn("claude-progress.txt", agents_doc)
        self.assertNotIn("请先读 `AGENTS.md` 获取全局上下文", claude_doc)

    def test_root_readme_has_skill_install(self) -> None:
        self.assertTrue(hasattr(gen, "gen_root_readme"))
        readme = gen.gen_root_readme()

        self.assertIn("unzip", readme)
        self.assertIn("harness-init.skill", readme)
        self.assertIn("/harness-init", readme)
        self.assertNotIn("$skill-installer", readme)
        self.assertNotIn("方式 2", readme)
        self.assertNotIn("方式 3", readme)
        self.assertNotIn("方式 4", readme)
        self.assertNotIn("\\n|", readme)

    def test_swift_check_command_and_stack_readme_text_are_clean(self) -> None:
        self.assertIn("-scheme App", gen.STACKS["swift-ios"]["commands"]["check"])
        readme = gen.gen_readme("swift-ios", gen.STACKS["swift-ios"])
        self.assertNotIn("��", readme)

    def test_root_entry_docs_are_short_and_consistent(self) -> None:
        for path in (ROOT / "AGENTS.md", ROOT / "CLAUDE.md"):
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertLessEqual(len(content.splitlines()), 100)
                self.assertNotIn("Codex-progress.txt", content)
                self.assertNotIn("Codex/AGENTS.md", content)

    def test_stack_readme_recommends_stack_specific_load_prompt_after_skill_install(self) -> None:
        readme = gen.gen_readme("ts-nextjs", gen.STACKS["ts-nextjs"])
        self.assertIn("需先安装 `harness-init` skill", readme)
        self.assertIn(
            '从 https://github.com/ppop123/harness 装载 ts-nextjs 栈的 harness 工程结构到当前目录',
            readme,
        )
        self.assertIn("Claude 用户可复制 `claude/CLAUDE.md`", readme)

    def test_all_generated_stack_entry_docs_use_neutral_progress_file_and_stay_short(self) -> None:
        for stack in gen.STACKS.values():
            claude_doc = gen.gen_claude_md(stack)
            agents_doc = gen.gen_agents_md(stack)
            with self.subTest(stack=stack["name"], doc="claude"):
                self.assertIn("agent-progress.txt", claude_doc)
                self.assertLessEqual(len(claude_doc.splitlines()), 100)
            with self.subTest(stack=stack["name"], doc="agents"):
                self.assertIn("agent-progress.txt", agents_doc)
                self.assertLessEqual(len(agents_doc.splitlines()), 100)

    def test_generated_layer_check_scripts_are_shell_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for stack_id, stack in gen.STACKS.items():
                script_path = tmp_path / f"{stack_id}-layer-check.sh"
                script_path.write_text(gen.gen_layer_check(stack), encoding="utf-8")
                result = subprocess.run(
                    ["bash", "-n", str(script_path)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                with self.subTest(stack=stack_id):
                    self.assertEqual(
                        result.returncode,
                        0,
                        msg=f"generated shell script should be parseable:\n{result.stderr}",
                    )

    def test_harness_init_skill_source_is_thin_loader(self) -> None:
        skill_md = (ROOT / "skills" / "harness-init" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("从 GitHub", skill_md)
        self.assertIn("实时拉取", skill_md)
        self.assertNotIn("本 skill 自带", skill_md)
        self.assertNotIn("assets/", skill_md)

    def test_harness_init_skill_build_contains_no_bundled_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "harness-init.skill"
            result = subprocess.run(
                [
                    "python3",
                    str(ROOT / "scripts" / "build_harness_init_skill.py"),
                    "--output",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            with zipfile.ZipFile(output_path) as archive:
                names = sorted(archive.namelist())
            self.assertEqual(names, ["harness-init/", "harness-init/SKILL.md"])


if __name__ == "__main__":
    unittest.main()
