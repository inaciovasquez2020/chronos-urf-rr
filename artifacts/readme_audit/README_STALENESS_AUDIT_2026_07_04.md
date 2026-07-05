# README Staleness Audit

Generated: 2026-07-05T01:06:35Z

This audit records README files and claim-status signals that should be checked against current repository state.

## .lake/packages/Cli/README.md

- lines: 367
- signal_lines: 21

```text
1: # lean4-cli
5: See [the documentation of Lake](https://github.com/leanprover/lean4/blob/master/src/lake/README.md).
10: ```Lean
11: open Cli
35:                                  which can be used to reference Lean modules like `Init.Data.Array` \
36:                                  or Lean files using a relative path like `Init/Data/Array.lean`."
53:   -- `./Cli/Extensions.lean` provides some commonly useful examples.
63: ```Lean
92: ```lean
96: #eval main <| "-i -o -p 1 --module=Lean.Compiler --set-paths=path1,path2,path3 input output1 output2".splitOn " "
104:   Flag `--module` was set to `Lean.Compiler`.
153:                                 to reference Lean modules like `Init.Data.Array`
154:                                 or Lean files using a relative path like
155:                                 `Init/Data/Array.lean`.
173: The full example can be found under `./CliTest/Example.lean`.
176: This section documents only the most common features of the library. For the full documentation, peek into `./Cli/Basic.lean` and `./Cli/Extensions.lean`! All definitions below live in the `Cli` namespace.
178: ```Lean
204: ```Lean
229: ```Lean
283: ```Lean
340: ```Lean
```

## .lake/packages/LeanSearchClient/README.md

- lines: 100
- signal_lines: 22

```text
1: # LeanSearchClient
3: LeanSearchClient provides syntax for search using the [leansearch API](https://leansearch.net/) and the [LeanStateSearch](https://premise-search.com) API from within Lean. It allows you to search for Lean tactics and theorems using natural language. It also allows searches on [Loogle](https://loogle.lean-lang.org/json) from within Lean.
12: In all cases results are displayed in the Lean Infoview and clicking these replaces the query text. In the cases of a query for tactics only valid tactics are displayed.
14: Which backend is used is determined by the `leansearchclient.backend` option.
18: The following are examples of using the leansearch API. The search is triggered when the sentence ends with a full stop (period) or a question mark.
24: ```lean
30: ```lean
31: #leansearch "If a natural number n is less than m, then the successor of n is less than the successor of m."
38: ```lean
43: For `leansearch`:
45: ```lean
46: example := #leansearch "If a natural number n is less than m, then the successor of n is less than the successor of m."
53: The general command has two variants. With a string, calling LeanSearch:
55: ```lean
61: Without a string, calling LeanStateSearch
63: ```lean
71: For `leansearch`:
73: ```lean
75:   #leansearch "If a natural number n is less than m, then the successor of n is less than the successor of m."
79: For LeanStateSearch:
81: ```lean
92: ```lean
```

## .lake/packages/Qq/README.md

- lines: 188
- signal_lines: 14

```text
1: # Expression quotations for Lean 4
10: Lean 4's metaprogramming facilities.
14: ```lean
15: import Qq open Qq Lean
61: ```lean
63: open Qq
68: -- `{u v : Lean.Level}` auto-generated due to option
81:    `AppBuilder.lean` in the Lean 4 code).
113: ```lean
128: ```lean
149: in Lean notation,
152: In Lean, `Q` is not sufficiently expressive
170: ```lean
178: ```lean
```

## .lake/packages/aesop/README.md

- lines: 964
- signal_lines: 66

```text
4: for Lean 4. It is broadly similar to Isabelle's `auto`. In essence, Aesop works
28: - Aesop uses indexing methods similar to those of `simp` and other Lean tactics.
45: have questions, please create an issue or ping me (Jannis Limperg) on the [Lean
46: Zulip](https://leanprover.zulipchat.com). Pull requests are very welcome!
53: With [elan](https://github.com/leanprover/elan) installed, `lake build`
58: To use Aesop in a Lean 4 project, first add this package as a dependency. In
59: your `lakefile.lean`, add
61: ```lean
62: require aesop from git "https://github.com/leanprover-community/aesop"
65: You also need to make sure that your `lean-toolchain` file contains the same
66: version of Lean 4 as Aesop's, and that your versions of Aesop's dependencies
72: ```lean
88: ``` lean
105: ```lean
107: theorem nil_append : nil ++ xs = xs := rfl
110: theorem cons_append : cons x xs ++ ys = cons x (xs ++ ys) := rfl
119: ``` lean
146: With these rules, we can prove a theorem about `NonEmpty` and `append`:
148: ``` lean
150: theorem nonEmpty_append₁ {xs : MyList α} ys :
169: ``` lean
181: ``` lean
220: ``` lean
226: Next, we prove another simple theorem about `NonEmpty`:
228: ``` lean
229: theorem nil_not_nonEmpty (xs : MyList α) : xs = nil → ¬ NonEmpty xs := by
243: ``` lean
245: theorem append_nil {xs : MyList α} :
249: theorem append_assoc {xs ys zs : MyList α} :
255: set, Aesop can prove theorems about this function more or less by itself (though
262: particular, the file `AesopTest/List.lean` contains an Aesop-ified port of 200
263: basic list lemmas from the Lean 3 version of mathlib, and the file
264: `AesopTest/SeqCalcProver.lean` shows how Aesop can help with the formalisation
277:   (Zero means that the rule closed the goal). Each normalisation rule is
404:   ```lean
410:   ```lean
418:   ```lean
449:   theorem and_elim_right : α ∧ β → α := ...
518:   metavariable). This can be a problem because some Lean tactics, e.g. `cases`,
552: ``` lean
579: only when the current namespace is open.
586: ``` lean
599:     to Lean's default `simp` priority.
631: ``` lean
656: ``` lean
674: ```lean
680: ``` lean
693: ``` lean
699: end of the file. This is a fundamental limitation of Lean's attribute system:
706: ``` lean
718: ``` lean
737: ``` lean
799: ``` lean
825: The term is an arbitrary Lean expression of type `Aesop.Options`; see there for
845: so for now I won't document them in detail. See `Aesop/BuiltinRules.lean` and
846: `Aesop/BuiltinRules/*.lean`
866: ``` lean
876:   generated (as a Lean term). You should be able to copy-and-paste this proof
883: ``` lean
893: Mathlib's `lakefile.lean`, recompile Mathlib from scratch and create a new Lean
896: ``` lean
907: just artefacts of the Lean tracing API.
923: ``` lean
932: example, apply the theorem `∀ n, n < n + 1`. We could also use an assumption `n
942: subgoal as *additional goals*. Thus, when we apply the theorem `∀ n, n < n + 1`,
943: which closes the first goal, Aesop realises that because this theorem was
```

## .lake/packages/batteries/README.md

- lines: 95
- signal_lines: 16

```text
3: The "batteries included" extended library for Lean 4. This is a collection of data structures and tactics intended for use by both computer-science applications and mathematics applications of Lean 4.
7: To use `batteries` in your project, add the following to your `lakefile.lean`:
8: ```lean
9: require "leanprover-community" / "batteries" @ git "main"
15: scope = "leanprover-community"
19: Additionally, please make sure that you're using the version of Lean that the current version of `batteries` expects. The easiest way to do this is to copy the [`lean-toolchain`](./lean-toolchain) file from this repository to your project. Once you've added the dependency declaration, the command `lake update` checks out the current version of `batteries` and writes it the Lake manifest file. Don't run this command again unless you're prepared to potentially also update your Lean compiler version, as it will retrieve the latest version of dependencies and add them to the manifest.
23: * Get the newest version of `elan`. If you already have installed a version of Lean, you can run
29:   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
31:   If this also fails, follow the instructions under `Regular install` [here](https://leanprover-community.github.io/get_started.html).
52: [mathlib4 docs]: https://leanprover-community.github.io/mathlib4_docs/Batteries.html
68: [`proof_wanted`](https://github.com/search?q=repo%3Aleanprover-community%2Fbatteries+language%3ALean+%2F^proof_wanted%2F&type=code)
74: Batteries PRs often affect Mathlib, a key component of the Lean ecosystem.
78: Every Batteries PR has an automatically created [Mathlib Nightly Testing](https://github.com/leanprover-community/mathlib4-nightly-testing/) branch called `batteries-pr-testing-N` where `N` is the number of the Batteries PR.
84: You may need to ask for write access to [Mathlib Nightly Testing](https://github.com/leanprover-community/mathlib4-nightly-testing/) to do that.
92: ```lean
93: require "leanprover-community" / "batteries" @ git "main"
```

## .lake/packages/batteries/docs/README.md

- lines: 95
- signal_lines: 16

```text
3: The "batteries included" extended library for Lean 4. This is a collection of data structures and tactics intended for use by both computer-science applications and mathematics applications of Lean 4.
7: To use `batteries` in your project, add the following to your `lakefile.lean`:
8: ```lean
9: require "leanprover-community" / "batteries" @ git "main"
15: scope = "leanprover-community"
19: Additionally, please make sure that you're using the version of Lean that the current version of `batteries` expects. The easiest way to do this is to copy the [`lean-toolchain`](./lean-toolchain) file from this repository to your project. Once you've added the dependency declaration, the command `lake update` checks out the current version of `batteries` and writes it the Lake manifest file. Don't run this command again unless you're prepared to potentially also update your Lean compiler version, as it will retrieve the latest version of dependencies and add them to the manifest.
23: * Get the newest version of `elan`. If you already have installed a version of Lean, you can run
29:   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
31:   If this also fails, follow the instructions under `Regular install` [here](https://leanprover-community.github.io/get_started.html).
52: [mathlib4 docs]: https://leanprover-community.github.io/mathlib4_docs/Batteries.html
68: [`proof_wanted`](https://github.com/search?q=repo%3Aleanprover-community%2Fbatteries+language%3ALean+%2F^proof_wanted%2F&type=code)
74: Batteries PRs often affect Mathlib, a key component of the Lean ecosystem.
78: Every Batteries PR has an automatically created [Mathlib Nightly Testing](https://github.com/leanprover-community/mathlib4-nightly-testing/) branch called `batteries-pr-testing-N` where `N` is the number of the Batteries PR.
84: You may need to ask for write access to [Mathlib Nightly Testing](https://github.com/leanprover-community/mathlib4-nightly-testing/) to do that.
92: ```lean
93: require "leanprover-community" / "batteries" @ git "main"
```

## .lake/packages/importGraph/README.md

- lines: 130
- signal_lines: 14

```text
25: where `MyModule` follows the same module naming you would use to `import` it in lean. See `lake exe graph --help` for more options.
54: There are a few commands implemented, which help you analysing the imports of a file. These are accessible by adding `import ImportGraph.Tools` to your lean file.
70: Add `import ImportGraph.Imports.FromSource` to your Lean script to access:
77: ```lean
82:   let imports ← findTransitiveImportsFromSource "Mathlib/Algebra/Ring/Basic.lean" (some `Mathlib)
94: The installation works exactly like for any [Lake package](https://reservoir.lean-lang.org/),
95: see [Lake docs](https://github.com/leanprover/lean4/tree/master/src/lake#supported-sources).
99: You can import this in any lean projects by the following line to your `lakefile.lean`:
101: ```lean
102: require "leanprover-community" / "importGraph" @ git "main"
110: source = "leanprover-community"
118: Please open PRs/Issues if you have troubles or would like to contribute new features!
122: The main tool has been extracted from [mathlib](https://github.com/leanprover-community/mathlib4),
130: Primarily maintained by [Jon Eugster](https://leanprover.zulipchat.com/#narrow/dm/385895-Jon-Eugster), Kim Morrison, and the wider leanprover community.
```

## .lake/packages/importGraph/html-template/README.md

- lines: 33
- signal_lines: 3

```text
18: And open http://localhost:8000
26: Therefore any modifications to these lines need to be reflected in `ImportGraph/Cli.lean`!
30: This tool has been adapted from its [Lean 3 version](https://github.com/eric-wieser/mathlib-import-graph) written by Eric Wieser, which was published under the [MIT License](./LICENSE_source)
```

## .lake/packages/mathlib/.github/actions/get-mathlib-ci/README.md

- lines: 74
- signal_lines: 3

```text
4: `leanprover-community/mathlib-ci`.
9: own `actions/checkout` block for `leanprover-community/mathlib-ci`.
73:     echo "Raw URL: https://raw.githubusercontent.com/leanprover-community/mathlib-ci/${{ steps.get_mathlib_ci.outputs.ref }}/scripts/nightly/create-adaptation-pr.sh"
```

## .lake/packages/mathlib/Archive/Imo/README.md

- lines: 48
- signal_lines: 6

```text
7:   and this is a reasonable place to collect Lean samples of IMO problems.
11:   and an opportunity to teach new contributors how to write Lean code.
23:   [style guide](https://leanprover-community.github.io/contribute/style.html)
33:   after you open the pull request as before.
37:   there are often several [open pull requests about IMO problems](https://github.com/leanprover-community/mathlib4/pulls?q=is%3Aopen+is%3Apr+label%3Aimo) (and in [Lean 3](https://github.com/leanprover-community/mathlib/pulls?q=is%3Aopen+is%3Apr+label%3Aimo),
47:   or start reading about [metaprogramming](https://leanprover-community.github.io/learn.html#metaprogramming-and-tactic-writing)
```

## .lake/packages/mathlib/Archive/README.md

- lines: 16
- signal_lines: 3

```text
14: - The [style guide](https://leanprover-community.github.io/contribute/style.html) for contributors.
15: - The [git commit conventions](https://github.com/leanprover/lean4/blob/master/doc/dev/commit_convention.md).
16: - You don't have to follow the [naming conventions](https://leanprover-community.github.io/contribute/naming.html).
```

## .lake/packages/mathlib/Archive/Wiedijk100Theorems/README.md

- lines: 6
- signal_lines: 4

```text
1: # "Formalizing 100 Theorems" in Lean
3: In this folder, we keep proofs of theorems on Freek Wiedijk's [100 theorems list](https://www.cs.ru.nl/~freek/100/) which don't fit naturally elsewhere in mathlib or in other Lean repositories.
5: See [this page](https://leanprover-community.github.io/100.html) for more information about theorems from the list above which have been formalized in Lean. If you prove a new theorem from that list, you should add the appropriate data to this file:
6: https://github.com/leanprover-community/mathlib4/blob/master/docs/100.yaml
```

## .lake/packages/mathlib/Cache/README.md

- lines: 247
- signal_lines: 21

```text
3: This directory contains the implementation of Mathlib's build cache system (`lake exe cache`), which downloads pre-built `.olean` files to avoid recompiling the entire library.
17: lake exe cache get Mathlib/Algebra/Group/Basic.lean
34: | `clean`         | Delete non-linked files                                             |
35: | `clean!`        | Delete everything on the local cache                                |
36: | `lookup [ARGS]` | Show information about cache files for the given Lean files         |
53: - File paths: `Mathlib/Algebra/Group/Basic.lean`
54: - Folder names: `Mathlib/Data/` (finds all Lean files inside)
55: - Glob patterns: `Mathlib/**/Order/*.lean` (via shell expansion)
63: | `--repo=OWNER/REPO` | Override the repository to fetch cache from (e.g., `--repo=leanprover-community/mathlib4`) |
100: Each Lean file's cache is identified by a hash computed from:
103:    - `lakefile.lean` content
104:    - `lean-toolchain` content
106:    - The Lean compiler's git hash
119: Cache files use the `.ltar` format (Lean tar), handled by [leantar](https://github.com/digama0/leangz). Each `.ltar` contains:
121: - `.olean` files (compiled Lean)
122: - `.ilean` files (interface info)
136: - `LeanSearchClient`
152: - **Download URL**: `https://mathlib4.lean-cache.cloud`
226: - `{repo}` is like `leanprover-community/mathlib4` or `username/mathlib4`
235: - **leantar** - for `.ltar` compression/decompression
246: | `.lake/build/lib/lean/`     | Unpacked `.olean` files      |
```

## .lake/packages/mathlib/DownstreamTest/README.md

- lines: 6
- signal_lines: 1

```text
6: There is no `lean-toolchain` file, because CI will copy it from the main repo during testing.
```

## .lake/packages/mathlib/Mathlib/Algebra/Notation/README.md

- lines: 7
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/Mathlib/Algebra/README.md

- lines: 17
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/Mathlib/Analysis/Convex/Cone/README.md

- lines: 15
- signal_lines: 1

```text
15: * M. Riesz extension theorem
```

## .lake/packages/mathlib/Mathlib/Analysis/Convex/README.md

- lines: 18
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/Mathlib/Geometry/Convex/Cone/README.md

- lines: 13
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/Mathlib/Geometry/Convex/README.md

- lines: 10
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/Mathlib/Geometry/Group/Growth/README.md

- lines: 11
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/Mathlib/Geometry/Group/README.md

- lines: 10
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/Mathlib/Mathport/README.md

- lines: 13
- signal_lines: 3

```text
8: which still contains mathport infrastructure, and migrate your project to that tag,
11: (That tag also contains the final form of `Syntax.lean`,
12: which implicitly contained a TODO list of unported tactics from Lean 3,
```

## .lake/packages/mathlib/Mathlib/Order/README.md

- lines: 21
- signal_lines: 2

```text
9: * `Order.BooleanAlgebra` for Heyting/bi-Heyting/co-Heyting/Boolean algebras
12: * `Order.CompleteBooleanAlgebra` for complete Boolean algebras
```

## .lake/packages/mathlib/Mathlib/Probability/Combinatorics/README.md

- lines: 9
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/README.md

- lines: 168
- signal_lines: 46

```text
3: ![GitHub CI](https://github.com/leanprover-community/mathlib4/actions/workflows/build.yml/badge.svg?branch=master)
5: [![project chat](https://img.shields.io/badge/zulip-join_chat-brightgreen.svg)](https://leanprover.zulipchat.com)
6: [![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/leanprover-community/mathlib4)
8: [Mathlib](https://leanprover-community.github.io) is a user maintained library for the [Lean theorem prover](https://leanprover.github.io).
9: It contains both programming infrastructure and mathematics,
14: You can find detailed instructions to install Lean, mathlib, and supporting tools on [our website](https://leanprover-community.github.io/get_started.html).
15: Alternatively, click on one of the buttons below to open a GitHub Codespace or a Gitpod workspace containing the project.
17: [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/leanprover-community/mathlib4)
19: [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/leanprover-community/mathlib4)
24: [https://github.com/leanprover-community/mathlib4/wiki/Using-mathlib4-as-a-dependency](https://github.com/leanprover-community/mathlib4/wiki/Using-mathlib4-as-a-dependency)
28: Got everything installed? Why not start with the [tutorial project](https://leanprover-community.github.io/install/project.html)?
30: For more pointers, see [Learning Lean](https://leanprover-community.github.io/learn.html).
34: Besides the installation guides above and [Lean's general
35: documentation](https://docs.lean-lang.org/lean4/doc/), the documentation
38: - [The mathlib4 docs](https://leanprover-community.github.io/mathlib4_docs/index.html): documentation [generated
39:   automatically](https://github.com/leanprover/doc-gen4) from the source `.lean` files.
40: - A description of [currently covered theories](https://leanprover-community.github.io/theories.html),
41:   as well as an [overview](https://leanprover-community.github.io/mathlib-overview.html) for mathematicians.
42: - Some [extra Lean documentation](https://leanprover-community.github.io/learn.html) not specific to mathlib (see "Miscellaneous topics")
43: - Documentation for people who would like to [contribute to mathlib](https://leanprover-community.github.io/contribute/index.html)
46: room](https://leanprover.zulipchat.com/), and you are welcome to join, or read
49: discussions](https://leanprover-community.github.io/archive/), which is useful
55: [on the community guide contribute to mathlib](https://leanprover-community.github.io/contribute/index.html)
57: You may want to subscribe to the `mathlib4` channel on [Zulip](https://leanprover.zulipchat.com/) to introduce yourself and your plan to the community.
61: * To obtain precompiled `olean` files, run `lake exe cache get`. (Skipping this step means the next step will be very slow.)
65: * If you added a new file, run the following command to update `Mathlib.lean`
75:  - The [style guide](https://leanprover-community.github.io/contribute/style.html)
76:  - A guide on the [naming convention](https://leanprover-community.github.io/contribute/naming.html)
77:  - The [documentation style](https://leanprover-community.github.io/contribute/doc.html)
84: you can try one of `lake clean` or `rm -rf .lake` before trying `lake exe cache get` again.
92: The [mathlib4_docs repository](https://github.com/leanprover-community/mathlib4_docs)
94: [mathlib4 docs](https://leanprover-community.github.io/mathlib4_docs/index.html).
98: git clone https://github.com/leanprover-community/mathlib4_docs.git
100: cp ../mathlib4/lean-toolchain .
107: ## Transitioning from Lean 3
109: For users familiar with Lean 3 who want to get up to speed in Lean 4 and migrate their existing
110: Lean 3 code we have:
112: - A [survival guide](https://github.com/leanprover-community/mathlib4/wiki/Lean-4-survival-guide-for-Lean-3-users)
113:   for Lean 3 users
114: - [Instructions to run `mathport`](https://github.com/leanprover-community/mathport#running-on-a-project-other-than-mathlib)
116:   of `mathlib` from Lean 3 to Lean 4.
130: For a list containing more detailed information, see https://leanprover-community.github.io/teams/maintainers.html
136: * Mario Carneiro (@digama0): lean formalization, tactics, type theory, proof engineering
137: * Bryan Gin-ge Chen (@bryangingechen): documentation, infrastructure
159: * Eric Wieser (@eric-wieser): algebra, infrastructure
165: * Gabriel Ebner (@gebner): tactics, infrastructure, core, formal languages
```

## .lake/packages/mathlib/scripts/README.md

- lines: 226
- signal_lines: 33

```text
9: A script belongs in [**`leanprover-community/mathlib-ci`**](https://github.com/leanprover-community/mathlib-ci)
34:   - Inactive user cleanup: `--remove N` generates (but doesn't execute) gh commands
58: - `create_deprecated_modules.lean` defines the `#create_deprecated_modules` command that
62:   `lean_lib`). `runSkimmer.sh --on tgt1 tgt2 ...` applies only to those lake targets (libraries,
63:   modules) within mathlib. If oleans for the refactored targets are already present, it will use them;
64:   else it will build any necessary oleans. This script may be copy-pasted to other repos with altered
68:   NOTE: the functionality exposed by this script is very experimental, and subject to change.
76:   * Sets up git remotes correctly (`upstream` for leanprover-community/mathlib4, `origin` for user's fork)
90:   - The remote `upstream` points to `leanprover-community/mathlib4`
92:   - The `gh` default repo points to `leanprover-community/mathlib4`
106: These scripts help with testing Lean PRs that change backward-compatibility option
110:   Reusable parallel DAG traversal for Lean import graphs. Parses the import DAG from `.lean`
136:   **forward** (roots first) so each module is only built after all its imports are clean. For
154: - `mk_all.lean`
156:   `Mathlib.lean`, `Mathlib/Tactic.lean`, `Archive.lean` and `Counterexamples.lean`
157: - `lint-style.lean`, `lint-style.py`, `print-style-errors.sh`
158:   style linters, written in Python and Lean. Run via `lake exe lint-style`.
159:   Medium-term, the latter two scripts should be rewritten and incorporated in `lint-style.lean`.
160: - `check_title_labels.lean` verifies that a (non-WIP, non-draft) PR has a well-formed title.
164: - `yaml_check.py`, `check-yaml.lean`
166: - `autolabel.lean` is the Lean script in charge of automatically adding a `t-`label on eligible PRs.
174: - `nightly-testing-checklist.lean` reports and fixes the state of `nightly-testing` branches
178:   - Whether each repo's toolchain matches the latest lean4 nightly
180:   - CI status, with inline display of failing jobs and Lean error messages
183:   - Bumps stale `lean-toolchain` files
185:   - Removes duplicate declarations ("has already been declared" errors) using Lean's parser
194: - `find_command_range.lean` is a helper used by `nightly-testing-checklist.lean`.
195:   Given a file and position, it uses Lean's parser to find the byte range of the enclosing
197:   cloned repos at runtime and executed via `lake env lean --run`.
203: - `downstream_dashboard.py` inspects the CI infrastructure of each repository in
211:   For permanent and deliberate exceptions, add a `@[nolint lintername]` in the .lean file instead.
218: - `check_title_labels.lean` is used to check whether a PR title follows our [commit style conventions](https://leanprover-community.github.io/contribute/commit.html).
221: - `docker_build.sh` builds the `lean4`, `gitpod4`, and `gitpod4-blueprint` Docker images.
```

## .lake/packages/mathlib/scripts/bench/README.md

- lines: 38
- signal_lines: 4

```text
4: It is built around [radar](https://github.com/leanprover/radar)
6: on the [Lean FRO radar instance](https://radar.lean-lang.org/repos/mathlib4).
32: [bench repo specification](https://github.com/leanprover/radar/blob/62bffab39025a1c2039499ae7a85b1ad446286d9/README.md#bench-repo-specification).
35: [leanprover/radar-bench-mathlib4](https://github.com/leanprover/radar-bench-mathlib4).
```

## .lake/packages/mathlib/scripts/bench/build/README.md

- lines: 27
- signal_lines: 1

```text
12: The following metrics are collected from `lean --profile` and summed across all modules:
```

## .lake/packages/mathlib/scripts/bench/lint/README.md

- lines: 9
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/mathlib/scripts/bench/open-mathlib/README.md

- lines: 9
- signal_lines: 6

```text
1: # The `open-mathlib` benchmark
3: This benchmark approximates `import Mathlib` in the editor by running `lake lean Mathlib.lean`.
6: - `open-mathlib//instructions`
7: - `open-mathlib//maxrss`
8: - `open-mathlib//task-clock`
9: - `open-mathlib//wall-clock`
```

## .lake/packages/mathlib/scripts/bench/size/README.md

- lines: 8
- signal_lines: 4

```text
5: - `size/.lean//files`
6: - `size/.lean//lines`
7: - `size/.olean//files`
8: - `size/.olean//bytes`
```

## .lake/packages/mathlib/widget/src/penrose/README.md

- lines: 8
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/plausible/README.md

- lines: 63
- signal_lines: 5

```text
2: A property testing framework for Lean 4 that integrates into the tactic framework.
6: ```lean
27: ```lean
30: open Plausible
56: ```lean
```

## .lake/packages/proofwidgets/README.md

- lines: 164
- signal_lines: 31

```text
3: ProofWidgets is a library of user interface components for [Lean 4](https://leanprover.github.io/). It
15: ProofWidgets relies on the [user widgets](https://leanprover.github.io/lean4/doc/examples/widgets.lean.html)
16: mechanism built into Lean. User widgets provide the minimum of functionality needed to enable
19: backported into Lean core, but ProofWidgets overall will remain a separate library
29: git clone https://github.com/leanprover-community/ProofWidgets4 --depth 1
40: To ensure ProofWidgets works with your version of the Lean toolchain,
42: Add the following to your `lakefile.lean`:
44: ```lean
46: require "leanprover-community" / "proofwidgets" @ git "v0.0.3"
60: ```lean
62: require "leanprover-community" / "proofwidgets" @ git "v0.0.3"
66: ⚠️ [EXPERIMENTAL] To use ProofWidgets4 JS components in widgets defined in other Lean packages,
67: import [@leanprover-community/proofwidgets4](https://www.npmjs.com/package/@leanprover-community/proofwidgets4) from NPM.
75: ```lean
77: open scoped ProofWidgets.Jsx
80: #html <b>You can use HTML in Lean {.text s!"{1 + 3}"}!</b>
83: See the `Jsx.lean` and `ExprPresentation.lean` demos.
89: data. See the `Venn.lean` and `Plot.lean` demos.
91: For more purpose-specific integrations of libraries see the `Rubiks.lean` and `RbTree.lean` demos.
97: `ExprPresentation.lean` demo.
102: in the background. See the `LazyComputation.lean` demo, and the `Conv.lean` demo for an example of
109: You can see an example of how to do this in the `Plot.lean` demo.
116: and Lean modules (under `ProofWidgets/`).
120: and afterwards build all Lean modules.
121: Lean modules may use TypeScript compilation outputs.
130: into ProofWidgets Lean modules.
134: to where it is used in Lean.
136: ⚠️ Note however that due to Lake issue [#86](https://github.com/leanprover/lake/issues/86),
148:   title =	{{An Extensible User Interface for Lean 4}},
149:   booktitle =	{14th International Conference on Interactive Theorem Proving (ITP 2023)},
162:   annote =	{Keywords: user interfaces, human-computer interaction, Lean}
```

## .lake/packages/urf_core/README.md

- lines: 154
- signal_lines: 30

```text
1: # URF Core — Formal Verification Infrastructure
5: URF Core is a Lean formalization and certificate-boundary repository.
7: The repository currently contains verified bounded witnesses, reusable certificate layers, theorem surfaces, and explicit frontier records. Many underlying mathematical components are elementary or previously known; the repository contribution is the formalization architecture, reproducible verification trail, and boundary discipline.
9: Current boundary:
11: - No unrestricted graph-class theorem is claimed.
12: - No unrestricted intended-configuration theorem is claimed.
13: - No P vs NP, Clay-problem, or major open-problem closure is claimed.
16: Recent closed bounded objects:
18: - `URF.R1R2R3Path5.rich_closed_nonToy_exists`
22: - `URF.R1R2R3RepositoryNative.repositoryNativeIntendedConfiguration_path5_closed`
24: ## Verified Frontier Tracking Definitions Layer
26: This repository is the definitions layer for **Verified Frontier Tracking**.
35: | Claim boundaries | Prevents interfaces, conditions, and open frontiers from being promoted into solved theorems |
37: Boundary: this repository provides trusted definitions and verification infrastructure. It does not claim theorem-level closure unless a theorem is explicitly formalized and its assumptions are discharged.
59: - No experimental or draft material
64: - Scientific Infrastructure: https://github.com/inaciovasquez2020/scientific-infrastructure
66: - Scientific Infrastructure Environment: https://inaciovasquez2020.github.io/scientific-infrastructure/
72: - Dependencies: refer to `scientific-infrastructure` for the standard execution environment.
87: Cross-link `scientific-infrastructure` as the current reference environment layer.
91: This repository is the current reference upstream for URF definitions, theorem statements, dependency ledgers, and closure claims.
99: Current theorem-level closed surface: `docs/status/URF_CORE_NO_STATUS_PROMOTION_THEOREM_CLOSURE_2026_05_15.md`
116: Theorem status:
125: - Strongest verified theorem: `URF.no_status_promotion_closed` in `URF/TheoremClosure/NoStatusPromotion.lean`
126: - Weakest missing theorem: replace each load-bearing axiom/admit with a proof or quarantine it as an explicit assumption
127: - Obligation inventory: `docs/status/OPEN_OBLIGATION_INVENTORY_2026_04_27.md`
131: This repository is governed by [`docs/status/EXTERNAL_STATUS_LOCK.md`](docs/status/EXTERNAL_STATUS_LOCK.md). Build success, CI success, dashboards, ledgers, axioms, admits, `sorry`, or placeholder witnesses do not constitute theorem-level closure.
133: ## Lean Proof Portfolio Classification
135: This repository is governed by [`docs/status/LEAN_PROOF_PORTFOLIO_CLASSIFICATION.md`](docs/status/LEAN_PROOF_PORTFOLIO_CLASSIFICATION.md). Its role in the portfolio is explicitly classified as proof-facing, conditional frontier, infrastructure/documentation, or legacy/scaffold.
141: Boundary: selected-domain Chronos/H4.1-FGL status only; no unrestricted H4.1/FGL closure; no UniversalFiberEntropyGap, Chronos-RR, P vs NP, or Clay-problem closure.
154: Boundary: this container verifies URF spectral-gap certificate artifacts accepted by the verifier. It does not assert theorem-level closure unless the referenced theorem is formalized and all assumptions are discharged.
```

## .lake/packages/urf_core/URF/Terminal_Classification/README.md

- lines: 13
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/admissible/no_benchmarks/README.md

- lines: 12
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/atlas/README.md

- lines: 11
- signal_lines: 2

```text
1: # Counterexample Atlas (Boundary Theorems)
8: - Verification method (Lean refutation, script, or explicit check)
```

## .lake/packages/urf_core/docs/lncs/README.md

- lines: 6
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/docs/notes/glossary/README.md

- lines: 13
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/docs/referee/README.md

- lines: 19
- signal_lines: 3

```text
11:    One-page list of unconditional theorems only.
16: No other claims are made outside these documents.
19:    Explicit statement of review safety, scope, and non-claims for editors.
```

## .lake/packages/urf_core/examples/demo-cert/README.md

- lines: 7
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/final-wall-fo-k-locality/README.md

- lines: 4
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/legacy/urf-portfolio/README.md

- lines: 34
- signal_lines: 2

```text
31: ## Infrastructure
32: - scientific-infrastructure
```

## .lake/packages/urf_core/legacy/urf-prefab-system/README.md

- lines: 71
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/legacy/urf-roadmap/README.md

- lines: 14
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/manuscripts/power_graph/README.md

- lines: 9
- signal_lines: 1

```text
9: See: Bounded_ChiR_Theorem.tex
```

## .lake/packages/urf_core/papers/ac0-csp/README.md

- lines: 15
- signal_lines: 1

```text
5: - A proved normalization theorem for AC0 bounded-arity update systems
```

## .lake/packages/urf_core/papers/fo-k-locality/README.md

- lines: 6
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/papers/local-depth-bound/README.md

- lines: 9
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/standards/URF-Block-Exact/README.md

- lines: 45
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/standards/URF-SG/README.md

- lines: 27
- signal_lines: 1

```text
13:   Terminal theorem (formal statement).
```

## .lake/packages/urf_core/toolkit/URF-Core/final-wall-fo-k-locality/README.md

- lines: 15
- signal_lines: 1

```text
3: The FO^k locality wall is **conditionally closed**.
```

## .lake/packages/urf_core/urf-cli/README.md

- lines: 10
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/verification/README.md

- lines: 12
- signal_lines: 1

```text
1: ## Verified Spectral Gap Certificate
```

## .lake/packages/urf_core/verify/auditor/README_AUDITOR.md

- lines: 15
- signal_lines: 2

```text
8: 3) Lean attestation: sha256(LEAN_BUILD_ATTEST.txt) == LEAN_BUILD_ATTEST.sha256
12: 6) TSA tokens (if present): openssl ts -reply -in tsa/<TAG>/<file>.tsr -text
```

## .lake/packages/urf_core/zloop/README.md

- lines: 1
- signal_lines: 0

No claim/status signal lines found.

## .lake/packages/urf_core/zloop/certs/frozen/README.txt

- lines: 13
- signal_lines: 1

```text
8: Condition verified: S_HS(P) + T_HS(P) < 1
```

## .pytest_cache/README.md

- lines: 8
- signal_lines: 0

No claim/status signal lines found.

## .venv/lib/python3.11/site-packages/pip/_vendor/README.rst

- lines: 180
- signal_lines: 4

```text
106:   ``pyopenssl`` (Windows).
133: the patches sometimes no longer apply cleanly. In that case, the update will
137:    a clean starting point.
148:    and apply it cleanly. The patch file changes will be committed along with the
```

## .venv-gracefo/lib/python3.11/site-packages/numpy/ma/README.rst

- lines: 236
- signal_lines: 3

```text
64:  * in the same way, the comparison of two masked arrays is a masked array, not a boolean
147: each entry with the same fields as a record, but of boolean types:
151: can be done. Note that *mrecords* is still experimental...
```

## .venv-gracefo/lib/python3.11/site-packages/pip/_vendor/README.rst

- lines: 178
- signal_lines: 4

```text
106:   ``pyopenssl`` (Windows).
131: the patches sometimes no longer apply cleanly. In that case, the update will
135:    a clean starting point.
146:    and apply it cleanly. The patch file changes will be committed along with the
```

## .venv-gravity-inspect/lib/python3.11/site-packages/numpy/ma/README.rst

- lines: 236
- signal_lines: 3

```text
64:  * in the same way, the comparison of two masked arrays is a masked array, not a boolean
147: each entry with the same fields as a record, but of boolean types:
151: can be done. Note that *mrecords* is still experimental...
```

## .venv-gravity-inspect/lib/python3.11/site-packages/pip/_vendor/README.rst

- lines: 178
- signal_lines: 4

```text
106:   ``pyopenssl`` (Windows).
131: the patches sometimes no longer apply cleanly. In that case, the update will
135:    a clean starting point.
146:    and apply it cleanly. The patch file changes will be committed along with the
```

## .venv-podaac/lib/python3.11/site-packages/numpy/ma/README.rst

- lines: 236
- signal_lines: 3

```text
64:  * in the same way, the comparison of two masked arrays is a masked array, not a boolean
147: each entry with the same fields as a record, but of boolean types:
151: can be done. Note that *mrecords* is still experimental...
```

## .venv-podaac/lib/python3.11/site-packages/pip/_vendor/README.rst

- lines: 178
- signal_lines: 4

```text
106:   ``pyopenssl`` (Windows).
131: the patches sometimes no longer apply cleanly. In that case, the update will
135:    a clean starting point.
146:    and apply it cleanly. The patch file changes will be committed along with the
```

## README.md

- lines: 179
- signal_lines: 16

```text
5: This repository records verified build surfaces, Lean interface surfaces, JSON artifacts, status documents, and verifier tests for the Chronos/URF reduction program. It is a proof-facing frontier and infrastructure repository, not a repository-level theorem-closure claim.
40: The executable layer verifies that registered surfaces compile, artifacts match their expected schemas, status documents preserve required boundary language, and test/verifier suites pass.
73: ## Non-claims
75: This repository does not claim:
80: - unconditional restricted concentration monotonicity theorem
81: - unconditional restricted continuation norm theorem
89: ## Governance and boundary discipline
91: This repository is governed by explicit status locks, boundary documents, JSON artifacts, Lean frontier modules, and verifier tests.
96: CLAIMS.md
99: OPEN_INPUTS_REGISTRY.md
102: lean/Chronos/Frontier/
111: urf-core             = core definitions, theorem/library layer, shared foundations
128: Build success, CI success, dashboards, ledgers, status documents, axioms, admits, sorries, placeholders, proof surfaces, candidate estimates, or closeout stacks do not constitute theorem-level closure.
142: PASS: FGL is the sole open finite-patch assumption
144: ## Open Frontier Items
177: `PASS: FGL is the sole open finite-patch assumption`
```

## docs/lncs/README.md

- lines: 6
- signal_lines: 0

No claim/status signal lines found.

## docs/oblivion_atom/README.md

- lines: 59
- signal_lines: 1

```text
3: This directory contains experimental and diagnostic components supporting
```

## docs/oblivion_atom/README_INDEX.md

- lines: 50
- signal_lines: 1

```text
39: open_problem.md  
```

## docs/referee/README.md

- lines: 19
- signal_lines: 3

```text
11:    One-page list of unconditional theorems only.
16: No other claims are made outside these documents.
19:    Explicit statement of review safety, scope, and non-claims for editors.
```

## external-audit/README.md

- lines: 26
- signal_lines: 7

```text
4: Replay the full Chronos core build from a clean clone and confirm:
19: lean/Chronos/FinalCoercivity.lean
20: lean/Chronos/SpectralGap.lean
21: lean/Chronos/SpectralGapAxiomReplacement.lean
22: lean/Chronos/EntropyModelGeneral.lean
23: lean/Chronos/EDOmegaN.lean
24: lean/Chronos.lean
```

## lean/Oblivion/README.lean

- lines: 10
- signal_lines: 0

No claim/status signal lines found.

## manuscripts/proof_complexity_bridge/README.md

- lines: 19
- signal_lines: 0

No claim/status signal lines found.

## models/gxd_f2/README.md

- lines: 9
- signal_lines: 2

```text
5: - GxD_Spec.md (canonical definition + toolkit theorems)
7: - GxD_Closure_Theorems.tex (formal lemma-theorem closure)
```

## sidfh-kkzeta/README.md

- lines: 11
- signal_lines: 2

```text
5: STATUS := lake env lean Sidfh/KkZeta/Basic.lean PASS
8: BOUNDARY := ¬ zeta_det_closed_form_proves_any_determinant_theorem
```

## urf-core/README.md

- lines: 28
- signal_lines: 1

```text
13: multiple concrete instantiations across mathematics, physics, and
```

## urf-core/verification/README.md

- lines: 0
- signal_lines: 0

No claim/status signal lines found.

