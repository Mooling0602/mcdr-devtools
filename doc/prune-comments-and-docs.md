---
name: prune-comments-and-docs
description: Review and tighten code comments, docstrings, and prose docs (README, guides, design notes). Use when asked to review, clean up, cut, or improve comments or documentation.
origin: https://github.com/MidAutumnMoon/TaysiTsuki/blob/master/home/agents/skills/prune-comments-and-docs/SKILL.md
---

# Prune comments and docs

Write for a reader who sees only the current code, has never seen a previous version, and doesn't know who wrote it. A comment earns its place when it tells that reader something they need, where they're reading, that the code doesn't already say. The same fact told twice to the same audience is told once too many.

Bad comments are usually written during a change and describe the change: what was replaced, what was split, what was just implemented and how. That belongs in the commit message. If you made the change, you're the worst judge of this. Read each comment as if opening the file for the first time.

## Who reads what

- **Docstrings** (`"""..."""` on modules, classes, and functions) serve callers. State the contract: what it does, what the signature doesn't say, when it raises, what it mutates, what the caller must ensure. A docstring should stay true if the body is rewritten with the same behavior.
- **Inline comments** (`#`) serve maintainers. Explain why the code is this way where the code alone would mislead: a constraint, a workaround, a rejected obvious alternative. Don't narrate what the next lines do.
- **Prose docs** serve someone arriving cold. Cover concepts, usage, and decisions that span files. Don't mirror the code, report progress, or restate contracts that docstrings own.

Each kind holds the facts its audience needs. The same fact may serve two audiences (a README and a docstring), but not two spots for one audience.

The best home for a fact is often not a comment: a name, a type hint, an exception message, an assertion, a test. Prefer those; a comment is the home of last resort. Suggest such moves in your summary; this pass reviews comments, not code.

## The pass

Comments written during a change re-explain its decisions at every site. Map the duplicates before pruning: cluster the comments and surviving plan-prose around repeated domain terms ("state", "rendered", "atomic", "converge") and give each recurring fact one home per audience, on the item it's about. If two spots both want the fact, the item it's about wins within an audience; otherwise the one the reader reaches first.

Then check each comment in order. Act on the first failure.

1. **True?** Read the code it describes. If they disagree and you can't tell which is wrong, flag it. Don't make the comment match what might be a bug.
2. **Needed?** If the name, signature, type hints, or next few lines already say it, delete it. Also delete it if the fact's home already gives this reader everything they need here.
3. **Free of time?** If it only makes sense to someone who saw an earlier version ("now", "no longer", "instead of", "replaced", "split", "moved", "refactored", "originally", "ported from"), delete it. Plans are the mirror image ("will", "could", "eventually", "in the future", "not implemented yet"); delete them too. If it guards against a real regression, restate it as a present-tense constraint. A limitation that still bites ("teardown is not implemented") is plain prose and joins the map. An intended action becomes a TODO or an issue link, not prose.
4. **Is this the fact's home?** If not, keep only what this reader must do about it: an obligation, not a re-explanation. Implementation detail in a docstring moves inline if it explains a why. Otherwise it goes.
5. **As short as it can be?** Point first. Most docstrings need one sentence. Cut filler, hedges, and asides.

A comment that passes all five and holds its fact's home stays untouched, word for word.

Delete is the default: a comment goes unless it holds a fact with no other home; shorten, move, or rewrite to rescue that fact. Add a comment only when a reader would otherwise get something wrong: a missing why, or a missing contract (what it raises, what it mutates, what a lock protects). If a comment exists only to explain an unclear name, suggest the rename in your summary instead of polishing the comment.

Judge blocks, not just sentences. For a comment over two lines: if deleting it loses no fact, delete it. If you can predict a comment from the code's structure (bare numbering, section rules, a gloss per `Enum` member that restates its name), it's narration; cut on sight. Re-judge each file as a whole: when comments track the code's structure one to one, the file is over-commented even if each comment survives alone. Cut the class, not the instances, unless a project convention enforces them. Only within one class: bare numbering is one class, labeled decisions another.

## Keep

- Invariants the code relies on: what a lock protects, who closes a resource, what a caller must already hold or have validated.
- Contract details that callers rely on: which exceptions propagate, what the call mutates.
- Justifications for a suppressed check: a `# type: ignore[...]`, a `# noqa`, a deliberately broad `except`.
- Why the obvious approach wasn't taken.
- "N.B." and test labels that flag a deliberate decision ("N.B. we deliberately allow src to not exist") or name the case under construction ("# not ours", "# ancestor is a regular file").
- Links to issues, specs, or upstream bugs behind a workaround.
- License and attribution notices, even when cutting "ported from" narrative.
- Examples that a test module executes. Running the unittest suite checks them; nothing checks prose.
- Conventions the language or project enforces: Sphinx reStructuredText fields (`:param name:`, `:returns:`, `:raises ValueError:`), the docstring lint rules in use, the existing doc style.

## Cut on sight

- Restated signatures and types: "Takes a `str` and returns `list[str]`"; a `:type:` field duplicating a type hint.
- Narration of the body: "First iterates..., then...".
- Change logs and process: "Refactored to...", "Fixed the bug where...", "Added support for...".
- Mappings to code, designs, or reference implementations the code no longer follows.
- Commented-out code. TODOs that are done.
- Throat-clearing openers: "Note:", "Important:", "This function...", "Helper to...", "This ensures that...". Bare sequence markers: "# 1.", "# step 2", "# Case 3".
- Assertion predictions in tests: a comment that announces what the next `self.assert...()` call checks. Name the case or the setup intent instead.
- Hype and padding: "robust", "seamless", "comprehensive", "simply", "just".
- Cross-references to types the signature already annotates.
- Doc files that are work logs (summaries, plans, migration notes, status reports). Delete the file and name it in your summary.

No em dashes. An em dash usually attaches an aside that should be cut. Restructure the sentence rather than swapping in `;`, `:`, ` - `, or parentheses.

## Examples

**Over-explained contract**

```python
# Before
def discover(root: Path) -> list[AgentDef]:
    """Discovers agent definitions in the given directory.

    This function recursively walks the provided ``root`` path, reads each
    ``.toml`` file it encounters, and parses it into an :class:`AgentDef`. The
    parsed definitions are collected into a :class:`list` and returned.

    :raises AgentDefError: if a directory cannot be read or a file fails to
        parse. The exception includes the failing path.
    """


# After
def discover(root: Path) -> list[AgentDef]:
    """Loads every ``.toml`` agent definition under ``root``, recursively.

    :raises AgentDefError: if a directory cannot be read or a file does not
        parse. The exception names the file.
    """
```

The annotation already says `list[AgentDef]`. "Walks, reads, parses, collects" narrates the body. What's left is the contract.

**History**

```python
# Before
# Switched from a set plus a final sort to a dict, which keeps first-seen
# order, so the output is deterministic. The sort pass that used to follow
# collection is gone.
seen: dict[str, None] = {}

# After
# Keeps first-seen order so the output is stable across runs.
seen: dict[str, None] = {}
```

The reason survives. The history doesn't. Nobody reading this has seen the `set`.

**Cross-reference told as a story**

```python
# Before
def download(url: str) -> bytes:
    """Downloads the archive from ``url``.

    The fetch-and-verify pipeline was split into two steps: this function only
    downloads, and checksum validation now lives in :func:`verify_archive`.
    The old ``fetch_verified`` helper has been removed.
    """


# After
def download(url: str) -> bytes:
    """Downloads the archive from ``url`` without verifying it.

    Pass the bytes to :func:`verify_archive` before use.
    """
```

The caller needs their obligation, not the architecture's history. `fetch_verified` doesn't exist, so that sentence can't help anyone.

**The same fact in several places**

```python
# Before
"""An interrupted run retries against the previous state and converges."""


class State:
    def write(self) -> None:
        """Atomically installs the state. A failure leaves the previous state
        intact, so a retry converges.
        """


import unittest


class StateTest(unittest.TestCase):
    # Retry converges and records the new generation.
    def test_retry_converges(self) -> None:
        first = State(self.state_dir)
        with self.assertRaises(OSError):
            first.write()
        retried = State(self.state_dir)
        retried.write()
        self.assertEqual(retried.generation, first.generation + 1)


# After
"""An interrupted run retries against the previous state and converges."""


class State:
    def write(self) -> None:
        """Atomically installs the state. On failure the previous state is
        intact.
        """


import unittest


class StateTest(unittest.TestCase):
    def test_retry_converges(self) -> None:
        first = State(self.state_dir)
        with self.assertRaises(OSError):
            first.write()
        retried = State(self.state_dir)
        retried.write()
        self.assertEqual(retried.generation, first.generation + 1)
```

The module docstring holds the fact for maintainers and stays word for word. `write()` keeps its local obligation and drops the re-explanation. The test comment restates the fact to the same audience, and the test body already shows a retry succeeding and the generation advancing. A README promising convergent retries would hold it for users, not count as a fourth copy.

**Implementation detail in the contract**

```python
# Before
def thumbnail(self, image_id: ImageId) -> Thumbnail:
    """Returns the thumbnail for ``image_id``, generating it on a cache miss.

    Uses an LRU cache (a ``dict`` plus a list for recency) holding 256 entries.
    On a miss, decodes with :func:`PIL.Image.open`, resizes, and inserts,
    evicting the least recently used entry. Lanczos is used because bilinear
    softened the line art visibly.
    """


# After
def thumbnail(self, image_id: ImageId) -> Thumbnail:
    """Returns the thumbnail for ``image_id``, generating and caching it on
    first use.
    """
    # ...
    # BILINEAR is faster but softens the line art.
    small = img.resize((w, h), Image.Resampling.LANCZOS)
```

Cache layout and decode steps can change without the contract changing. The filter choice is a real why, so it moves to the line it explains.

**Reference implementation**

```python
# Before
"""Token-bucket rate limiter, ported from the Java reference implementation
(``RateLimiter.java``). Unlike the Java version, there is no background refill
thread. Instead, ``acquire`` computes refills lazily, mirroring Java's
``reserveEarliestAvailable()``.
"""

# After
"""Token-bucket rate limiter. Tokens refill lazily inside ``acquire``, so an
idle limiter costs nothing.
"""
```

The reader won't open the Java code, and mappings to it rot as the code diverges. Keep the fact a user cares about. Keep a license notice if one is required.

**Leave these alone**

```python
# Callers hold `self._lock`; `self._rows` is only rebound under it.
self._rows = rows

# `os.replace` fails across filesystems, and the temp dir is often tmpfs.
shutil.copyfile(tmp, dest)
os.unlink(tmp)
```

Each says something the code can't, and stays true as long as the code below it does.

**Prose docs**

```markdown
<!-- Before, in README.md -->
## Recent Improvements ✅
- **Refactored** config loading for better maintainability
- **Added** comprehensive error handling
- **Removed** legacy `config.ini` support
```

Delete the section. A README describes the project as it is. If users need the config format, document the format that exists.

## Finish

1. Re-scan the survivors. For each fact you assigned a home, grep the fact, not one keyword: every wording it might wear ("rendered", "literal", "template text"). One hit per audience; more means a missed duplicate. Search every file that could hold a home, including prose docs outside the reviewed set.
2. Search comments and docstrings in the reviewed files for `—` and time markers: history (`now`, `no longer`, `instead`, `previously`, `old`, `new`, `refactor`) and plans (`will`, `could`, `eventually`, `not implemented yet`). Recheck each hit.
3. Build the Sphinx docs and run the unittest suite if the project has tests. Deletions break cross-references.
4. Report briefly: scope covered (files examined), facts that had several homes and where they ended up, deleted files, comments flagged as possibly wrong, suggested renames and other code moves. No per-edit changelog.
