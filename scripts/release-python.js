#!/usr/bin/env node
/**
 * Release orchestration script for Python sub-projects (backend, frontend, ai).
 *
 * Usage: node scripts/release-python.js <project> <bump>
 *   project: backend | frontend | ai
 *   bump:    patch | minor | major
 *
 * Steps:
 *   1. bump-my-version bumps VERSION + pyproject.toml
 *   2. git-cliff regenerates RELEASE.md scoped to the project's commits
 *   3. Commits the changed files with a conventional release commit
 *   4. Creates a git tag: <project>-v<new_version>
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const [, , project, bump] = process.argv;

const VALID_PROJECTS = ['backend', 'frontend', 'ai'];
const VALID_BUMPS = ['patch', 'minor', 'major'];

if (!VALID_PROJECTS.includes(project)) {
  console.error(`Error: project must be one of: ${VALID_PROJECTS.join(', ')}`);
  process.exit(1);
}
if (!VALID_BUMPS.includes(bump)) {
  console.error(`Error: bump must be one of: ${VALID_BUMPS.join(', ')}`);
  process.exit(1);
}

const root = path.resolve(__dirname, '..');
const projectDir = path.join(root, project);
const venvBin = path.join(root, '.venv', 'bin');

function run(cmd, cwd = root) {
  console.log(`  $ ${cmd}`);
  execSync(cmd, { cwd, stdio: 'inherit' });
}

function readVersion() {
  return fs.readFileSync(path.join(projectDir, 'VERSION'), 'utf8').trim();
}

console.log(`\n🚀 Releasing ${project} (${bump} bump)\n`);

// Step 1: Bump version
console.log('Step 1: Bumping version...');
run(`${venvBin}/bump-my-version bump ${bump}`, projectDir);

const newVersion = readVersion();
console.log(`  New version: ${newVersion}\n`);

// Step 2: Regenerate RELEASE.md with git-cliff
console.log('Step 2: Generating RELEASE.md...');
run(
  `${venvBin}/git-cliff --config ${project}/cliff.toml --repository . --tag ${project}-v${newVersion} -o ${project}/RELEASE.md`
);
console.log('');

// Step 3: Commit the release files
console.log('Step 3: Committing release files...');
run(`git add ${project}/VERSION ${project}/pyproject.toml ${project}/RELEASE.md`);
run(
  `git commit --no-verify -m "chore(${project}): release v${newVersion}"`,
  root
);
console.log('');

// Step 4: Tag the release
console.log('Step 4: Creating git tag...');
run(`git tag -a ${project}-v${newVersion} -m "Release ${project} v${newVersion}"`);

console.log(`\n✅ ${project} v${newVersion} released successfully!`);
console.log(`   Tag: ${project}-v${newVersion}`);
console.log(`   Run: git push --follow-tags origin main\n`);
