#!/usr/bin/env node

import { execFileSync } from "node:child_process";

const COMMIT_LIMIT = 15;
const PR_LIMIT = 20;
const ISSUE_LIMIT = 50;
const BRANCH_LIMIT = 40;
const ISSUE_VIEW_LIMIT = 8;

const options = parseArgs(process.argv.slice(2));

if (options.help) {
  printHelp();
  process.exit(0);
}

const skipped = [];
const local = gatherLocal(skipped);
const github = options.skipGithub ? null : gatherGithub(local, skipped);
const snapshot = {
  generatedAt: new Date().toISOString(),
  github,
  local,
  skipped,
};

if (options.format === "json") {
  console.log(JSON.stringify(snapshot, null, 2));
} else {
  console.log(formatMarkdown(snapshot));
}

function gatherLocal(skippedList) {
  const local = {
    aheadBehind: "",
    branch: "",
    dirty: false,
    recentCommits: [],
    shortStatus: "",
    worktrees: [],
  };

  try {
    local.branch = git(["rev-parse", "--abbrev-ref", "HEAD"]).trim();
  } catch (error) {
    skippedList.push(`git branch: ${error.message}`);
    return local;
  }

  try {
    local.shortStatus = git(["status", "-sb"]).trim();
    const first = local.shortStatus.split("\n")[0] || "";
    local.dirty = local.shortStatus.split("\n").length > 1;
    const track = first.match(/\[([^\]]+)\]/);
    local.aheadBehind = track ? track[1] : "";
  } catch (error) {
    skippedList.push(`git status: ${error.message}`);
  }

  try {
    const log = git([
      "log",
      `-${COMMIT_LIMIT}`,
      "--pretty=format:%h\t%ad\t%s",
      "--date=short",
    ]).trim();
    local.recentCommits = log
      ? log.split("\n").map((line) => {
          const [hash, date, ...rest] = line.split("\t");
          return { date, hash, subject: rest.join("\t") };
        })
      : [];
  } catch (error) {
    skippedList.push(`git log: ${error.message}`);
  }

  try {
    local.worktrees = parseWorktrees(git(["worktree", "list", "--porcelain"]));
  } catch (error) {
    skippedList.push(`git worktree: ${error.message}`);
  }

  try {
    const refs = git([
      "for-each-ref",
      "--format=%(refname:short)\t%(upstream:track)",
      "refs/heads",
    ]).trim();
    local.branches = refs
      ? refs
          .split("\n")
          .slice(0, BRANCH_LIMIT)
          .map((line) => {
            const [name, track] = line.split("\t");
            return { name, upstream: (track || "").replace(/[\[\]]/g, "") };
          })
      : [];
    if (refs.split("\n").filter(Boolean).length > BRANCH_LIMIT) {
      skippedList.push(`git branches: listed first ${BRANCH_LIMIT} only`);
    }
  } catch (error) {
    skippedList.push(`git branches: ${error.message}`);
  }

  return local;
}

function gatherGithub(local, skippedList) {
  const github = {
    issuesBlocked: [],
    issuesDoing: [],
    openIssueCount: 0,
    openIssuesCapped: false,
    openPrs: [],
    relatedIssues: [],
  };

  try {
    github.openPrs = ghJson([
      "pr",
      "list",
      "--state",
      "open",
      "--limit",
      String(PR_LIMIT),
      "--json",
      "number,title,headRefName,url,updatedAt,isDraft",
    ]);
  } catch (error) {
    skippedList.push(error.message);
    return github;
  }

  try {
    github.issuesDoing = slimIssues(
      ghJson([
        "issue",
        "list",
        "--state",
        "open",
        "--label",
        "status:doing",
        "--limit",
        String(ISSUE_LIMIT),
        "--json",
        "number,title,labels,updatedAt,url",
      ]),
    );
  } catch (error) {
    skippedList.push(error.message);
  }

  try {
    github.issuesBlocked = slimIssues(
      ghJson([
        "issue",
        "list",
        "--state",
        "open",
        "--label",
        "status:blocked",
        "--limit",
        String(ISSUE_LIMIT),
        "--json",
        "number,title,labels,updatedAt,url",
      ]),
    );
  } catch (error) {
    skippedList.push(error.message);
  }

  try {
    const open = ghJson([
      "issue",
      "list",
      "--state",
      "open",
      "--limit",
      String(ISSUE_LIMIT),
      "--json",
      "number,title,labels,updatedAt,url",
    ]);
    github.openIssueCount = open.length;
    github.openIssuesCapped = open.length >= ISSUE_LIMIT;
    github.openIssuesPreview = slimIssues(open);
  } catch (error) {
    skippedList.push(error.message);
  }

  const numbers = collectIssueNumbers(github, local);
  github.relatedIssues = viewIssues(numbers, skippedList);
  return github;
}

function collectIssueNumbers(github, local) {
  const ordered = [];
  const add = (number) => {
    if (!number || ordered.includes(number)) {
      return;
    }
    ordered.push(number);
  };

  for (const tree of local.worktrees || []) {
    for (const number of tree.issueNumbers || []) {
      add(number);
    }
  }
  for (const branch of local.branches || []) {
    for (const number of extractIssueNumbers(branch.name || "", true)) {
      add(number);
    }
  }
  for (const issue of [
    ...(github.issuesDoing || []),
    ...(github.issuesBlocked || []),
  ]) {
    add(issue.number);
  }
  for (const pr of github.openPrs || []) {
    for (const number of extractIssueNumbers(pr.title || "")) {
      add(number);
    }
    for (const number of extractIssueNumbers(pr.headRefName || "", true)) {
      add(number);
    }
  }
  return ordered.slice(0, ISSUE_VIEW_LIMIT);
}

function viewIssues(numbers, skippedList) {
  const issues = [];
  for (const number of numbers) {
    try {
      const issue = ghJson([
        "issue",
        "view",
        String(number),
        "--json",
        "number,title,state,labels,url",
      ]);
      issues.push({
        labels: (issue.labels || []).map((label) => label.name),
        number: issue.number,
        state: issue.state,
        title: issue.title,
        url: issue.url,
      });
    } catch (error) {
      skippedList.push(`issue #${number}: ${error.message}`);
    }
  }
  return issues;
}

function slimIssues(issues) {
  return (issues || []).map((issue) => ({
    labels: (issue.labels || []).map((label) => label.name),
    number: issue.number,
    title: issue.title,
    updatedAt: issue.updatedAt,
    url: issue.url,
  }));
}

function extractIssueNumbers(text, fromRef = false) {
  const numbers = new Set();
  const patterns = [/#(\d+)/g, /\bissue[-_\/]?(\d+)\b/gi];
  if (fromRef) {
    patterns.push(/(^|[-/_])(\d+)(?=[-_])/g);
  }
  for (const pattern of patterns) {
    let match = pattern.exec(text);
    while (match) {
      numbers.add(Number(match[match.length - 1]));
      match = pattern.exec(text);
    }
  }
  return [...numbers];
}

function parseWorktrees(porcelain) {
  const trees = [];
  let current = {};
  for (const line of porcelain.split("\n")) {
    if (line.startsWith("worktree ")) {
      if (current.path) {
        trees.push(current);
      }
      current = { path: line.slice("worktree ".length) };
    } else if (line.startsWith("HEAD ")) {
      current.head = line.slice("HEAD ".length);
    } else if (line.startsWith("branch ")) {
      current.branch = line.slice("branch ".length).replace(/^refs\/heads\//, "");
    } else if (line === "detached") {
      current.detached = true;
    }
  }
  if (current.path) {
    trees.push(current);
  }

  for (const tree of trees) {
    const haystack = `${tree.branch || ""} ${tree.path || ""}`;
    tree.issueNumbers = extractIssueNumbers(haystack, true);
  }
  return trees;
}

function formatMarkdown(snapshot) {
  const lines = ["# Catch-up gather", "", `At: ${snapshot.generatedAt}`, ""];
  const local = snapshot.local;
  lines.push("## This machine", "");
  lines.push(`- Branch: ${local.branch || "unknown"}`);
  if (local.aheadBehind) {
    lines.push(`- Upstream: ${local.aheadBehind}`);
  }
  lines.push(`- Dirty: ${local.dirty ? "yes" : "no"}`);
  lines.push(`- Worktrees: ${local.worktrees.length}`);
  for (const tree of local.worktrees) {
    const extra = tree.issueNumbers?.length
      ? ` (#${tree.issueNumbers.join(", #")})`
      : "";
    lines.push(`  - ${tree.branch || tree.head || "?"} @ ${tree.path}${extra}`);
  }
  lines.push("", "## Recent commits", "");
  for (const commit of local.recentCommits) {
    lines.push(`- ${commit.hash} ${commit.date} ${commit.subject}`);
  }
  if (snapshot.github) {
    lines.push("", "## GitHub", "");
    lines.push(`- Open PRs: ${snapshot.github.openPrs.length}`);
    lines.push(
      `- Open issues: ${snapshot.github.openIssueCount}${
        snapshot.github.openIssuesCapped ? "+" : ""
      }`,
    );
    lines.push(`- doing: ${snapshot.github.issuesDoing.length}`);
    lines.push(`- blocked: ${snapshot.github.issuesBlocked.length}`);
  }
  if (snapshot.skipped.length) {
    lines.push("", "## Skipped", "");
    for (const item of snapshot.skipped) {
      lines.push(`- ${item}`);
    }
  }
  lines.push("");
  return lines.join("\n");
}

function git(args) {
  return execFileSync("git", args, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
}

function ghJson(args) {
  try {
    return JSON.parse(
      execFileSync("gh", args, {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "pipe"],
      }),
    );
  } catch (error) {
    const detail = (error.stderr || error.message || "").toString().trim();
    throw new Error(`gh failed: ${detail || args.join(" ")}`);
  }
}

function parseArgs(argv) {
  const parsed = { format: "markdown", skipGithub: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--help" || arg === "-h") {
      parsed.help = true;
    } else if (arg === "--skip-github") {
      parsed.skipGithub = true;
    } else if (arg === "--format") {
      parsed.format = argv[index + 1];
      index += 1;
      if (parsed.format !== "json" && parsed.format !== "markdown") {
        console.error("Unknown --format (use json or markdown)");
        process.exit(2);
      }
    } else {
      console.error(`Unknown option: ${arg}`);
      process.exit(2);
    }
  }
  return parsed;
}

function printHelp() {
  console.log(`Usage: node scripts/catch-up-gather.mjs [options]

Bounded read-only snapshot for backlog catch-up. Does not write.

Options:
  --format json|markdown  Output format. Default: markdown.
  --skip-github           Skip gh (issues/PRs).
  --help                  Show this help message.
`);
}
