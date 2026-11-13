"""Fail-closed CodeQL SARIF gate: independently produced security findings.

Exit 0 iff exactly one valid Python CodeQL SARIF run is present, with no
security-rule results. Non-security diagnostics are reported but not counted
as confirmed vulnerabilities. This is NOT proof of zero vulnerabilities.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys

def fail(message):
    print("CODEQL_AUDIT := INCOMPLETE_OR_BLOCKED:", message, file=sys.stderr)
    raise SystemExit(2)

path=os.environ.get("CODEQL_RESULTS_DIR")
if not path:
    fail("missing analyzer SARIF output binding")
root=Path(path)
if not root.is_dir():
    fail("analyzer SARIF output directory missing")
files=sorted(root.rglob("*.sarif"))
if len(files)!=1:
    fail("expected one SARIF; found %d" % len(files))
try:
    raw=json.loads(files[0].read_text(encoding="utf-8"))
except (OSError,UnicodeError,ValueError) as exc:
    fail("unreadable SARIF: "+repr(exc))
if (type(raw) is not dict or raw.get("version")!="2.1.0"
    or type(raw.get("runs")) is not list or len(raw["runs"])!=1):
    fail("unexpected SARIF version or run count")
run=raw["runs"][0]
if type(run) is not dict or type(run.get("results")) is not list:
    fail("missing SARIF results")
tool=run.get("tool")
if type(tool) is not dict or type(tool.get("driver")) is not dict:
    fail("missing SARIF tool metadata")
driver=tool["driver"]
if "CodeQL" not in str(driver.get("name","")):
    fail("result not from CodeQL")
# SARIF producers may omit the rule catalog when no result refers to it.
# Any reported result MUST still resolve to explicit rule metadata.
rules=driver.get("rules",[])
if type(rules) is not list:
    fail("malformed rule metadata")
by_id={}
for rule in rules:
    if type(rule) is not dict or type(rule.get("id")) is not str:
        fail("malformed rule")
    if rule["id"] in by_id:
        fail("duplicate rule ID")
    by_id[rule["id"]]=rule
findings=[]
diagnostics=0
for result in run["results"]:
    if type(result) is not dict or type(result.get("ruleId")) is not str:
        fail("malformed result or missing ruleId")
    rule=by_id.get(result["ruleId"])
    if rule is None:
        fail("unresolved rule ID "+result["ruleId"])
    props=rule.get("properties") or {}
    if type(props) is not dict:
        fail("malformed rule metadata")
    tags=props.get("tags",[])
    if type(tags) is not list:
        fail("malformed rule tags")
    if ("security" in tags or "security-severity" in props):
        findings.append((result["ruleId"],result.get("message",{}).get("text","")[:250]))
    else:
        diagnostics+=1
print("CODEQL_SARIF_FILE :=",files[0].name)
print("CODEQL_CODEQL_RULES :=",len(rules))
print("CODEQL_NON_SECURITY_DIAGNOSTICS :=",diagnostics)
print("CODEQL_SECURITY_FINDINGS :=",len(findings))
for rule,message in findings[:30]:
    print("SECURITY_FINDING :",rule,repr(message))
if findings:
    print("CODEQL_SECURITY_GATE := FAIL")
    raise SystemExit(1)
print("CODEQL_SECURITY_GATE := PASS (no reported security-rule findings in scoped analysis)")
