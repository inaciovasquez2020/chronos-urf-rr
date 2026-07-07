#!/usr/bin/env python3
import json
from pathlib import Path


receipt_path = Path(
    "artifacts/status/sidfh_tach_speed_external_time_reference_receipt_2026_07_07.json"
)
lean_path = Path("lean/Chronos/Frontier/SIDFHTachSpeedInputSurface.lean")

receipt = json.loads(receipt_path.read_text())
lean_text = lean_path.read_text()

required = {
    "receipt": "sidfh_tach_speed_external_time_reference_receipt_2026_07_07",
    "repo": "chronos-urf-rr",
    "local_surface": "lean/Chronos/Frontier/SIDFHTachSpeedInputSurface.lean",
    "local_object": "SIDFHTachSpeedInputSurface",
    "external_reference_repo": "inaciovasquez2020/urf-core",
    "link_status": "bounded reference only; no derivation imported into chronos",
    "boundary": "BOUNDARY := ¬ chronos_derives_RelativeTimeScale_physical_time_dilation",
}

for key, value in required.items():
    assert receipt.get(key) == value, f"{key} mismatch"

for token in [
    "structure SIDFHTachSpeedInputSurface where",
    "properTimeRate : State → ℝ",
    "v_min : ℝ",
    "admissible_speed_below_light",
    "admissible_moving_speed_lower_bound",
    "slower_moves_faster_in_time",
]:
    assert token in lean_text, f"missing Lean surface token: {token}"

fields = set(receipt.get("local_input_fields", []))
for field in [
    "properTimeRate",
    "v_min",
    "c",
    "admissible_speed_below_light",
    "admissible_moving_speed_lower_bound",
    "slower_moves_faster_in_time",
]:
    assert field in fields, f"missing local input field: {field}"

refs = receipt.get("external_reference_objects", {})
assert refs["MotionBandShadow"]["definition"] == "MotionBandShadow(V,c,v) := V < v ∧ v < c"
assert refs["MotionBandShadow"]["status"] == "external bounded-reference object only"
assert (
    refs["MotionBandShadow"]["restriction"]
    == "does not prove a universal physical minimum nonzero speed"
)
assert (
    refs["RelativeTimeScale"]["definition"]
    == "RelativeTimeScale(S,t) := elapsed_time(S,t) / natural_cycle_time(S)"
)
assert refs["RelativeTimeScale"]["status"] == "external bounded-reference object only"
assert refs["RelativeTimeScale"]["restriction"] == "does not prove physical time dilation"

forbidden = set(receipt.get("forbidden_promotions", []))
for claim in [
    "chronos proves v_min from SIDFHTachSpeedInputSurface",
    "v_min proves physical time dilation",
    "MotionBandShadow proves physical time dilation",
    "RelativeTimeScale proves physical time dilation",
    "SIDFHTachSpeedInputSurface proves physical time dilation",
    "ShadowOfInfinity implies physical time dilation",
]:
    assert claim in forbidden, f"missing forbidden promotion: {claim}"

print("SIDFH_TACH_SPEED_EXTERNAL_TIME_REFERENCE_RECEIPT_OK")
