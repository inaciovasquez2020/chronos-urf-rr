# sidfh_kkzeta
## KKZeta input-surface status

STATUS := KKZETA_INPUT_SURFACE_OK
STATUS := lake env lean Sidfh/KkZeta/Basic.lean PASS
STATUS := lake build PASS

BOUNDARY := ¬ zeta_det_closed_form_proves_any_determinant_theorem

CHECK :=
./check_kkzeta.sh
