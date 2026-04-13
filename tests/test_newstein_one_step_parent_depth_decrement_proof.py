from pathlib import Path

def test_newstein_one_step_parent_depth_decrement_proof_lock() -> None:
    text = Path("docs/math/NEWSTEIN_ONE_STEP_PARENT_DEPTH_DECREMENT_PROOF.md").read_text(encoding="utf-8")
    assert "Status: OPEN" in text
    assert "(\\eta(w),w)\\in E" in text
    assert "\\eta(w)\\ \\text{lies on a shortest path from } w \\text{ to } r" in text
    assert "d(w,r)\\le d(\\eta(w),r)+1" in text
    assert "d(\\eta(w),r)\\ge d(w,r)-1" in text
    assert "d(w,r)=1+d(\\eta(w),r)" in text
    assert "d(\\eta(w),r)\\le d(w,r)-1" in text
    assert "d(\\eta(w),r)=d(w,r)-1" in text
    assert "OneStepParentDepthDecrement is reduced to parent-edge admissibility plus the geodesic-parent law." in text
