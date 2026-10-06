#!/usr/bin/env python3
"""
build.py — the only way pages are made.

    python3 build.py              test everything, then build docs/
    python3 build.py --no-smoke   skip the browser smoke test
    python3 build.py --random 500 more random tests per problem (default 200)

Order (a page is only written if every check before it passes):
  1. correctness  — every approach vs the brute-force oracle on
                    LeetCode examples, tests.json and random inputs
  2. languages    — C++ (and C, if present) vs the oracle on the same inputs
  3. traces       — instrumented Python generates the animation steps
  4. assemble     — pages, catalogue.js, index, gallery, shared core
  5. smoke test   — open every page in a headless browser (if available)

No third-party packages. Needs: python3 (3.8+), a C++17 compiler (g++ or
clang++), and a C compiler for problems that have a C version.
Formats of every file read here: .claude/skills/leetcode-pattern-visualizer/schemas.md
"""
import argparse
import copy
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import zlib

ROOT = os.path.dirname(os.path.abspath(__file__))
PROBLEMS = os.path.join(ROOT, "problems")
CORE = os.path.join(ROOT, "core")
DOCS = os.path.join(ROOT, "docs")
SCHEMA_VERSION = 1
SEED = 2026
LANGS = ("python", "cpp", "c")
SRC_FILE = {"python": "solution.py", "cpp": "solution.cpp", "c": "solution.c"}


class BuildError(Exception):
    pass


def fail(msg):
    raise BuildError(msg)


def log(msg=""):
    print(msg, flush=True)


def canon(v):
    return json.dumps(v, separators=(",", ":"), sort_keys=True)


def short(v, limit=120):
    s = canon(v)
    return s if len(s) <= limit else s[: limit - 3] + "..."


# ---------------------------------------------------------------------------
# Source markers
#   Python:  # @hide   # @trace   # @a:name   # @trace-begin / # @trace-end
#   C, C++:  // @hide  // @a:name
# @trace lines run only when tracing and are never shown.
# @hide lines run but are never shown (imports, includes).
# @a:name marks the line a step with anchor "name" highlights.
# ---------------------------------------------------------------------------
MARK = {"python": "#", "cpp": "//", "c": "//"}


def parse_source(text, lang):
    """Return (clean_exec_code, display_lines, anchors)."""
    c = MARK[lang]
    marker = re.compile(r"\s*" + re.escape(c) + r"\s*@(trace-begin|trace-end|trace|hide|a:[A-Za-z0-9_-]+)\s*$")
    exec_lines, display, anchors = [], [], {}
    in_trace = False
    for raw in text.splitlines():
        m = marker.search(raw)
        tag = m.group(1) if m else None
        body = raw[: m.start()] if m else raw
        if tag == "trace-begin":
            in_trace = True
            continue
        if tag == "trace-end":
            in_trace = False
            continue
        if in_trace or tag == "trace":
            continue
        exec_lines.append(body)
        if tag == "hide":
            continue
        display.append(body)
        if tag and tag.startswith("a:"):
            name = tag[2:]
            if name in anchors:
                fail("anchor @a:%s used twice in %s code" % (name, lang))
            anchors[name] = len(display)
    while display and not display[0].strip():
        display.pop(0)
        anchors = {k: v - 1 for k, v in anchors.items()}
    while display and not display[-1].strip():
        display.pop()
    lines = []
    sep = "  " + c + " "
    for d in display:
        d = d.rstrip()
        stripped = d.lstrip()
        if stripped.startswith(c):
            lines.append({"src": d[: len(d) - len(stripped)], "comment": stripped})
        elif sep in d:
            i = d.index(sep)
            lines.append({"src": d[:i].rstrip(), "comment": d[i + 2:].strip()})
        else:
            lines.append({"src": d, "comment": ""})
    return "\n".join(exec_lines) + "\n", lines, anchors


def strip_python_for_exec(text):
    """Instrumented code: keep everything, just drop the markers' effect on blocks."""
    out = []
    for raw in text.splitlines():
        if re.search(r"#\s*@trace-(begin|end)\s*$", raw):
            continue
        out.append(raw)
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Tracer — the object solutions call as T.step(...) and T.op()
# ---------------------------------------------------------------------------
class Tracer:
    def __init__(self):
        self.steps = []
        self.ops = 0

    def op(self, n=1):
        self.ops += n

    def step(self, anchor, phase, caption, **kw):
        s = {"anchor": anchor, "phase": phase, "caption": caption}
        for key, val in kw.items():
            if val is not None:
                s[key] = val
        if "roles" in s:
            s["roles"] = {str(k): v for k, v in s["roles"].items()}
        self.steps.append(json.loads(json.dumps(s)))  # deep snapshot, JSON-safe


class NullTracer(Tracer):
    def step(self, *a, **kw):
        pass


def load_py(code, filename, tracer):
    ns = {"T": tracer, "__name__": "viz_solution"}
    try:
        exec(compile(code, filename, "exec"), ns)
    except Exception as e:
        fail("%s does not run: %s" % (filename, e))
    return ns


def call_solution(ns, sig, args, filename):
    if "Solution" not in ns:
        fail("%s has no class Solution" % filename)
    fn = getattr(ns["Solution"](), sig["python"], None)
    if fn is None:
        fail("%s: Solution has no method %s" % (filename, sig["python"]))
    a = copy.deepcopy(args)
    res = fn(*[a[p["name"]] for p in sig["params"]])
    if sig["returns"] == "void":
        return a[sig["inPlace"]]
    return res


def call_brute(ns, sig, args, filename):
    if "brute" not in ns:
        fail("%s has no function brute(...)" % filename)
    return ns["brute"](*[copy.deepcopy(args[p["name"]]) for p in sig["params"]])


# ---------------------------------------------------------------------------
# C / C++ drivers
# ---------------------------------------------------------------------------
SUPPORTED_PARAM = {"int", "long", "int[]", "long[]"}
SUPPORTED_RET = {"void", "int", "long", "bool", "int[]"}


def check_signature(sig, where):
    for p in sig["params"]:
        if p["type"] not in SUPPORTED_PARAM:
            fail("%s: param type %r is not supported by the C/C++ drivers yet (supported: %s). "
                 "Extend make_driver() in build.py." % (where, p["type"], ", ".join(sorted(SUPPORTED_PARAM))))
    if sig["returns"] not in SUPPORTED_RET:
        fail("%s: return type %r is not supported yet (supported: %s)." % (where, sig["returns"], ", ".join(sorted(SUPPORTED_RET))))
    if sig["returns"] == "void" and not sig.get("inPlace"):
        fail("%s: returns 'void' needs \"inPlace\": the param that holds the answer." % where)


def encode_input(cases, sig):
    out = [str(len(cases))]
    for args in cases:
        for p in sig["params"]:
            v = args[p["name"]]
            if p["type"].endswith("[]"):
                out.append(str(len(v)))
                out.append(" ".join(str(x) for x in v))
            else:
                out.append(str(v))
    return "\n".join(out) + "\n"


def make_driver(lang, sig, src_path):
    fn = sig[lang]
    scalar = {"int": "int", "long": "long long"}
    lines = []
    if lang == "cpp":
        lines += ['#include "%s"' % src_path, "#include <iostream>", "#include <vector>", "#include <cstdlib>",
                  "static long long rd() { long long x; if (!(std::cin >> x)) std::exit(2); return x; }",
                  "template <class V> static void pr(const V& v) { std::cout << '['; for (size_t i = 0; i < v.size(); i++) { if (i) std::cout << ','; std::cout << v[i]; } std::cout << \"]\\n\"; }",
                  "int main() {", "  long long T = rd();", "  while (T--) {"]
        call = []
        for p in sig["params"]:
            n, t = p["name"], p["type"]
            if t.endswith("[]"):
                et = scalar[t[:-2]]
                lines.append("    std::vector<%s> %s((size_t)rd()); for (auto& x : %s) x = (%s)rd();" % (et, n, n, et))
            else:
                lines.append("    %s %s = (%s)rd();" % (scalar[t], n, scalar[t]))
            call.append(n)
        expr = "Solution().%s(%s)" % (fn, ", ".join(call))
        r = sig["returns"]
        if r == "void":
            lines += ["    %s;" % expr, "    pr(%s);" % sig["inPlace"]]
        elif r == "bool":
            lines.append('    std::cout << (%s ? "true" : "false") << "\\n";' % expr)
        elif r == "int[]":
            lines.append("    pr(%s);" % expr)
        else:
            lines.append('    std::cout << %s << "\\n";' % expr)
        lines += ["  }", "  return 0;", "}"]
    else:  # C
        lines += ["#include <stdio.h>", "#include <stdlib.h>", "#include <stdbool.h>", '#include "%s"' % src_path,
                  "static inline long long rd(void) { long long x; if (scanf(\"%lld\", &x) != 1) exit(2); return x; }",
                  "static inline void pr(const int* v, int n) { putchar('['); for (int i = 0; i < n; i++) { if (i) putchar(','); printf(\"%d\", v[i]); } printf(\"]\\n\"); }",
                  "static inline void prl(const long long* v, int n) { putchar('['); for (int i = 0; i < n; i++) { if (i) putchar(','); printf(\"%lld\", v[i]); } printf(\"]\\n\"); }",
                  "int main(void) {", "  (void)pr; (void)prl;  /* clang warns about unused static inline helpers */", "  long long T = rd();", "  while (T--) {"]
        call, frees, sizes = [], [], {}
        for p in sig["params"]:
            n, t = p["name"], p["type"]
            if t.endswith("[]"):
                et = scalar[t[:-2]]
                lines.append("    int %sSize = (int)rd(); %s* %s = malloc(sizeof(%s) * (%sSize ? %sSize : 1)); for (int i = 0; i < %sSize; i++) %s[i] = (%s)rd();"
                             % (n, et, n, et, n, n, n, n, et))
                call += [n, n + "Size"]
                frees.append(n)
                sizes[n] = (n + "Size", t)
            else:
                lines.append("    %s %s = (%s)rd();" % (scalar[t], n, scalar[t]))
                call.append(n)
        r = sig["returns"]
        if r == "void":
            lines.append("    %s(%s);" % (fn, ", ".join(call)))
            sz, t = sizes[sig["inPlace"]]
            lines.append("    %s(%s, %s);" % ("prl" if t == "long[]" else "pr", sig["inPlace"], sz))
        elif r == "int[]":
            lines.append("    int returnSize = 0; int* res = %s(%s); pr(res, returnSize); free(res);" % (fn, ", ".join(call + ["&returnSize"])))
        elif r == "bool":
            lines.append('    printf("%%s\\n", %s(%s) ? "true" : "false");' % (fn, ", ".join(call)))
        elif r == "long":
            lines.append('    printf("%%lld\\n", (long long)%s(%s));' % (fn, ", ".join(call)))
        else:
            lines.append('    printf("%%d\\n", %s(%s));' % (fn, ", ".join(call)))
        for f in frees:
            lines.append("    free(%s);" % f)
        lines += ["  }", "  return 0;", "}"]
    return "\n".join(lines) + "\n"


def compiler(lang):
    env = os.environ.get("CXX" if lang == "cpp" else "CC")
    cands = [env] if env else (["g++", "clang++"] if lang == "cpp" else ["gcc", "clang", "cc"])
    for c in cands:
        if c and shutil.which(c):
            return c
    fail("No %s compiler found. Install Xcode Command Line Tools (macOS: xcode-select --install) "
         "or set %s." % ("C++" if lang == "cpp" else "C", "CXX" if lang == "cpp" else "CC"))


def run_native(lang, sig, src_path, cases, where):
    tmp = tempfile.mkdtemp(prefix="viz-")
    try:
        ext = "cpp" if lang == "cpp" else "c"
        drv = os.path.join(tmp, "driver." + ext)
        with open(drv, "w") as f:
            f.write(make_driver(lang, sig, src_path))
        exe = os.path.join(tmp, "a.out")
        std = "-std=c++17" if lang == "cpp" else "-std=c11"
        cmd = [compiler(lang), std, "-O1", "-Wall", "-Wextra", "-Werror", drv, "-o", exe]
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode != 0:
            fail("%s: %s does not compile with %s:\n%s" % (where, os.path.basename(src_path), " ".join(cmd[:6]), p.stderr.strip()))
        p = subprocess.run([exe], input=encode_input(cases, sig), capture_output=True, text=True, timeout=60)
        if p.returncode != 0:
            fail("%s: %s crashed (exit code %d). %s" % (where, os.path.basename(src_path), p.returncode, p.stderr.strip()))
        return p.stdout.strip().splitlines()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def native_canon(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    return canon(v)


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------
def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def read_json(path):
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as e:
        fail("%s is not valid JSON: %s" % (os.path.relpath(path, ROOT), e))


REQUIRED_PROBLEM = ["source", "title", "difficulty", "nMax", "signature", "constraints", "bruteForce", "examples"]
REQUIRED_APPROACH = ["name", "pattern", "ds", "time", "space", "card", "invariant", "legend"]


def load_problem(pdir):
    name = os.path.basename(pdir)
    meta = read_json(os.path.join(pdir, "problem.json"))
    for k in REQUIRED_PROBLEM:
        if k not in meta:
            fail("%s/problem.json: missing \"%s\"" % (name, k))
    if meta.get("schemaVersion") != SCHEMA_VERSION:
        fail("%s/problem.json: schemaVersion must be %d" % (name, SCHEMA_VERSION))
    check_signature(meta["signature"], name)
    src = meta["source"]
    for k in ("site", "url"):
        if not src.get(k):
            fail("%s/problem.json: source needs \"%s\"" % (name, k))
    approaches = []
    for sub in sorted(os.listdir(pdir)):
        adir = os.path.join(pdir, sub)
        if not os.path.isdir(adir):
            continue
        if not os.path.exists(os.path.join(adir, "approach.json")):
            fail("%s/%s: folder without approach.json" % (name, sub))
        a = read_json(os.path.join(adir, "approach.json"))
        for k in REQUIRED_APPROACH:
            if k not in a:
                fail("%s/%s/approach.json: missing \"%s\"" % (name, sub, k))
        a["id"] = sub
        a["dir"] = adir
        for f in ("solution.py", "solution.cpp", "canvas.js"):
            if not os.path.exists(os.path.join(adir, f)):
                fail("%s/%s: missing %s (Python3 and C++17 are required for every approach)" % (name, sub, f))
        has_c = os.path.exists(os.path.join(adir, "solution.c"))
        if not has_c and not a.get("noC"):
            fail("%s/%s: no solution.c, so approach.json needs \"noC\": one sentence on why." % (name, sub))
        approaches.append(a)
    if not approaches:
        fail("%s: no approach folders" % name)
    approaches.sort(key=lambda a: (a.get("order", 99), a["id"]))
    for f in ("brute.py", "gen.py"):
        if not os.path.exists(os.path.join(pdir, f)):
            fail("%s: missing %s" % (name, f))
    tests = read_json(os.path.join(pdir, "tests.json")) if os.path.exists(os.path.join(pdir, "tests.json")) else []
    return {"name": name, "dir": pdir, "meta": meta, "approaches": approaches, "tests": tests}


# ---------------------------------------------------------------------------
# Per-problem pipeline
# ---------------------------------------------------------------------------
def build_problem(pb, n_random):
    name, meta, sig = pb["name"], pb["meta"], pb["meta"]["signature"]
    pdir = pb["dir"]
    log("■ %s" % name)

    # --- oracle
    brute_src = read(os.path.join(pdir, "brute.py"))
    brute_exec, brute_lines, _ = parse_source(brute_src, "python")
    brute_ns = load_py(brute_exec, name + "/brute.py", NullTracer())
    gen_ns = load_py(read(os.path.join(pdir, "gen.py")), name + "/gen.py", NullTracer())
    if "gen" not in gen_ns:
        fail("%s/gen.py has no function gen(rng)" % name)

    # --- test cases: examples + tests.json + random
    cases = []
    seen_ids = set()
    for ex in meta["examples"]:
        if ex["id"] in seen_ids:
            fail("%s: example id %r used twice" % (name, ex["id"]))
        seen_ids.add(ex["id"])
        cases.append(("example " + ex["id"], ex["args"], ex.get("expected")))
    for i, t in enumerate(pb["tests"]):
        cases.append(("tests.json #%d %s" % (i + 1, t.get("name", "")), t["args"], t.get("expected")))
    rng = random.Random(SEED + zlib.crc32(name.encode()))
    for i in range(n_random):
        cases.append(("random #%d" % (i + 1), gen_ns["gen"](rng), None))

    expected = []
    for label, args, exp in cases:
        b = call_brute(brute_ns, sig, args, name + "/brute.py")
        if exp is not None and canon(b) != canon(exp):
            fail("%s: the brute-force oracle is wrong on %s\n  input:    %s\n  expected: %s (from the statement)\n  brute:    %s"
                 % (name, label, short(args), short(exp), short(b)))
        expected.append(b)
    log("  oracle ok on %d cases (%d with answers from the statement)" % (len(cases), sum(1 for c in cases if c[2] is not None)))

    approaches_out = []
    for a in pb["approaches"]:
        where = "%s/%s" % (name, a["id"])
        code_out = {}
        # Python: clean version (what people see and submit)
        py_src = read(os.path.join(a["dir"], "solution.py"))
        py_exec, py_lines, py_anchors = parse_source(py_src, "python")
        clean_ns = load_py(py_exec, where + "/solution.py (clean)", NullTracer())
        for (label, args, _), b in zip(cases, expected):
            got = call_solution(clean_ns, sig, args, where + "/solution.py")
            if canon(got) != canon(b):
                fail("%s: Python answer differs from brute force on %s\n  input: %s\n  brute: %s\n  got:   %s"
                     % (where, label, short(args), short(b), short(got)))
        code_out["python"] = {"lines": py_lines, "anchors": py_anchors}
        langs_ok = ["python"]
        # C++ and C
        for lang in ("cpp", "c"):
            src = os.path.join(a["dir"], SRC_FILE[lang])
            if not os.path.exists(src):
                continue
            src_text = read(src)
            _, lines, anchors = parse_source(src_text, lang)
            out = run_native(lang, sig, src, [c[1] for c in cases], where)
            if len(out) != len(cases):
                fail("%s: %s printed %d answers for %d cases" % (where, SRC_FILE[lang], len(out), len(cases)))
            for (label, args, _), b, got in zip(cases, expected, out):
                if got.strip() != native_canon(b):
                    fail("%s: %s answer differs from brute force on %s\n  input: %s\n  brute: %s\n  got:   %s"
                         % (where, SRC_FILE[lang], label, short(args), native_canon(b), got.strip()))
            code_out[lang] = {"lines": lines, "anchors": anchors}
            langs_ok.append(lang)
        log("  %-34s ok: %s on %d cases" % (a["id"], ", ".join(langs_ok), len(cases)))

        # --- traces for the examples shown on the page
        inst = strip_python_for_exec(py_src)
        examples_out = []
        for ex, b in zip(meta["examples"], expected):
            tr = Tracer()
            ns = load_py(inst, where + "/solution.py (traced)", tr)
            got = call_solution(ns, sig, ex["args"], where + "/solution.py")
            if canon(got) != canon(b):
                fail("%s: traced Python gives a different answer on example %s. The @trace lines must not change the logic."
                     % (where, ex["id"]))
            if not tr.steps:
                fail("%s: no steps recorded for example %s (missing T.step calls?)" % (where, ex["id"]))
            for i, s in enumerate(tr.steps):
                for lang, c in code_out.items():
                    if s["anchor"] not in c["anchors"]:
                        fail("%s: step %d of example %s uses anchor %r, but %s code has no @a:%s"
                             % (where, i + 1, ex["id"], s["anchor"], lang, s["anchor"]))
            kind = ex.get("kind", "main")
            if kind == "main" and not 15 <= len(tr.steps) <= 40:
                log("  ! warning: example %s has %d steps (aim for 15–40 on main examples)" % (ex["id"], len(tr.steps)))
            n = max((len(v) for v in ex["args"].values() if isinstance(v, list)), default=0)
            if n > 20:
                fail("%s: example %s has %d elements; the renderer limit is 20" % (where, ex["id"], n))
            if kind == "main" and n > 10:
                log("  ! warning: main example %s has %d elements (presets should stay ≤ 10 to fit a phone)" % (ex["id"], n))
            btr = Tracer()
            bns = load_py(strip_python_for_exec(brute_src), name + "/brute.py (traced)", btr)
            call_brute(bns, sig, ex["args"], name + "/brute.py")
            examples_out.append({
                "id": ex["id"], "label": ex["label"], "kind": kind,
                "args": ex["args"], "inputText": ", ".join("%s = %s" % (k, json.dumps(v)) for k, v in ex["args"].items()),
                "output": got, "ops": {"brute": btr.ops, "approach": tr.ops}, "steps": tr.steps,
            })
        canvas_src = read(os.path.join(a["dir"], "canvas.js")).strip().rstrip(";")
        approaches_out.append({
            "id": a["id"], "name": a["name"], "pattern": a["pattern"], "ds": a["ds"],
            "time": a["time"], "space": a["space"], "card": a["card"], "invariant": a["invariant"],
            "phases": a.get("phases", {}), "legend": a["legend"], "whenToUse": a.get("whenToUse", ""),
            "accepted": a.get("accepted", []), "noC": a.get("noC"), "canvas": name + "/" + a["id"],
            "code": code_out, "examples": examples_out, "_canvas_src": canvas_src,
        })

    page = {
        "schemaVersion": SCHEMA_VERSION,
        "problem": {
            "source": meta["source"], "title": meta["title"], "difficulty": meta["difficulty"], "nMax": meta["nMax"],
            "constraints": meta["constraints"],
            "bruteForce": {"summary": meta["bruteForce"].get("summary", ""), "opsUnit": meta["bruteForce"].get("opsUnit", "operations"),
                           "code": brute_lines},
        },
        "approaches": approaches_out,
    }
    return page


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
PAGE_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="core/tokens.css">
<link rel="stylesheet" href="core/viz.css">
</head>
<body>
<!-- Generated by build.py from problems/{name}/. Do not edit: change the sources and rebuild. -->
<div class="wrap" id="app"></div>
<script src="core/viz.js"></script>
{canvases}
<script>window.PAGE = {data};</script>
<script>VIZ.mount(window.PAGE);</script>
</body>
</html>
"""


def source_label(src):
    """'LC 283' for LeetCode; '<short> <id>' when given; '' when the source has no id."""
    short = src.get("short") or {"LeetCode": "LC", "NeetCode": "NC"}.get(src.get("site", ""), "")
    return ("%s %s" % (short, src["id"])).strip() if src.get("id") else ""


def js_safe(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def html_escape(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


WRITTEN = set()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    WRITTEN.add(os.path.relpath(path, DOCS))


def copy_to_docs(src, rel):
    write(os.path.join(DOCS, rel), read(src))


def remove_stale(written):
    """Delete files in docs/ that this build did not write (e.g. a renamed problem)."""
    keep = {"CNAME", ".nojekyll"}
    stale = []
    for base, dirs, files in os.walk(DOCS):
        for f in files:
            p = os.path.join(base, f)
            if os.path.relpath(p, DOCS) not in written and f not in keep:
                stale.append(p)
    for p in stale:
        try:
            os.remove(p)
        except OSError as e:
            log("  ! could not delete stale file %s (%s) — delete it by hand" % (os.path.relpath(p, ROOT), e.strerror))


def emit(pages, site):
    write(os.path.join(DOCS, ".nojekyll"), "")
    for f in ("tokens.css", "viz.css", "viz.js", "index.js"):
        copy_to_docs(os.path.join(CORE, f), "core/" + f)
    for f in ("index.html", "gallery.html"):
        copy_to_docs(os.path.join(CORE, f), f)
    catalogue = []
    for name, page in pages:
        tags = []
        for a in page["approaches"]:
            rel = "canvas/%s--%s.js" % (name, a["id"])
            write(os.path.join(DOCS, rel), "/* Generated from problems/%s/%s/canvas.js */\nVIZ.canvas.register(%s, %s);\n"
                  % (name, a["id"], json.dumps(a["canvas"]), a.pop("_canvas_src")))
            tags.append('<script src="%s"></script>' % rel)
        page["site"] = {k: site.get(k, "") for k in ("notionPatterns", "bigO", "leetcodeProfile")}
        p = page["problem"]
        title = "%s · %s" % (source_label(p["source"]), p["title"]) if source_label(p["source"]) else p["title"]
        desc = "Step-by-step visualisation: " + "; ".join(a["name"] for a in page["approaches"])
        write(os.path.join(DOCS, name + ".html"), PAGE_HTML.format(
            title=html_escape(title), desc=html_escape(desc), name=name, canvases="\n".join(tags), data=js_safe(page)))
        catalogue.append({
            "file": name + ".html", "source": p["source"], "label": source_label(p["source"]), "title": p["title"], "difficulty": p["difficulty"],
            "approaches": [{"id": a["id"], "name": a["name"], "pattern": a["pattern"], "ds": a["ds"], "time": a["time"],
                            "space": a["space"], "hasC": "c" in a["code"], "accepted": a["accepted"]} for a in page["approaches"]],
        })
    catalogue.sort(key=lambda c: (c["source"].get("site", ""), int(c["source"]["id"]) if str(c["source"].get("id", "")).isdigit() else 10**9, c["title"]))
    cat = {"schemaVersion": SCHEMA_VERSION, "problems": catalogue, "articles": site.get("articles", []),
           "site": {k: site.get(k, "") for k in ("title", "intro", "notionPatterns", "patternGuides", "bigO", "leetcodeProfile", "repoUrl")}}
    write(os.path.join(DOCS, "catalogue.js"), "/* Generated by build.py. Do not edit. */\nwindow.CATALOGUE = %s;\n" % js_safe(cat))
    remove_stale(WRITTEN)


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
SMOKE_JS = """
async () => {
  const P = window.VIZ && VIZ._page;
  if (!P) return {error: "VIZ._page missing"};
  const A = window.PAGE.approaches;
  let steps = 0;
  for (let a = 0; a < A.length; a++) {
    P.selectApproach(a, false);
    for (let e = 0; e < A[a].examples.length; e++) {
      P.selectExample(e);
      for (let s = 0; s < P.nSteps(); s++) { P.go(s, true); steps++; }
    }
  }
  return {steps, overflow: document.documentElement.scrollWidth - window.innerWidth};
}
"""


def smoke(pages):
    try:
        from playwright.sync_api import sync_playwright  # noqa
    except ImportError:
        node = shutil.which("node")
        if not node:
            log("smoke test skipped: no Playwright and no Node.js (pip3 install playwright to enable)")
            return
        files = [os.path.join(DOCS, "core", "viz.js"), os.path.join(DOCS, "core", "index.js")]
        cdir = os.path.join(DOCS, "canvas")
        files += [os.path.join(cdir, f) for f in sorted(os.listdir(cdir))] if os.path.isdir(cdir) else []
        for f in files:
            p = subprocess.run([node, "--check", f], capture_output=True, text=True)
            if p.returncode != 0:
                fail("JavaScript syntax error in %s:\n%s" % (os.path.relpath(f, ROOT), p.stderr.strip()))
        log("smoke test: JavaScript syntax ok (node --check). For a full browser check: pip3 install playwright")
        return
    from playwright.sync_api import sync_playwright
    exe = os.environ.get("VIZ_CHROMIUM") or (("/opt/pw-browsers/chromium") if os.path.exists("/opt/pw-browsers/chromium") else None)
    targets = [n + ".html" for n, _ in pages] + ["index.html", "gallery.html"]
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
        except Exception as e:
            log("smoke test skipped: Playwright is installed but Chromium is not (python3 -m playwright install chromium). %s" % str(e).splitlines()[0])
            return
        for width in (1280, 375):
            for t in targets:
                page = browser.new_page(viewport={"width": width, "height": 900})
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                page.goto("file://" + os.path.join(DOCS, t.split("?")[0]) + ("?" + t.split("?")[1] if "?" in t else ""))
                page.wait_for_timeout(150)
                if t not in ("index.html", "gallery.html"):
                    r = page.evaluate(SMOKE_JS)
                    if r.get("error"):
                        errors.append(r["error"])
                    elif r["overflow"] > 1:
                        errors.append("page scrolls sideways at %dpx (%dpx too wide)" % (width, r["overflow"]))
                else:
                    ov = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                    if ov > 1:
                        errors.append("page scrolls sideways at %dpx (%dpx too wide)" % (width, ov))
                page.close()
                if errors:
                    fail("smoke test failed on %s at %dpx:\n  %s" % (t, width, "\n  ".join(errors[:10])))
        browser.close()
    log("smoke test: %d pages ok in a headless browser at 1280px and 375px" % len(targets))


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-smoke", action="store_true", help="skip the browser smoke test")
    ap.add_argument("--random", type=int, default=200, help="random tests per problem (default 200)")
    args = ap.parse_args()
    try:
        site = read_json(os.path.join(ROOT, "site.json"))
        names = sorted(d for d in os.listdir(PROBLEMS) if os.path.isdir(os.path.join(PROBLEMS, d)) and not d.startswith("."))
        problems = [load_problem(os.path.join(PROBLEMS, d)) for d in names]
        pages = [(pb["name"], build_problem(pb, args.random)) for pb in problems]
    except BuildError as e:
        log("\n✗ BUILD FAILED — docs/ was not touched.\n" + str(e))
        sys.exit(1)
    emit(pages, site)
    log("written: docs/ (%d problem pages, index, gallery, catalogue)" % len(pages))
    if not args.no_smoke:
        try:
            smoke(pages)
        except BuildError as e:
            log("\n✗ SMOKE TEST FAILED — docs/ was rebuilt but is broken. Do not push until this is fixed.\n" + str(e))
            sys.exit(1)
    log("✓ build ok")


if __name__ == "__main__":
    main()
