# Same-specimen carbon measurement bundle

Fill all three files with measurements from one spherical specimen. Placeholder,
pending, proposed, blank, nonfinite, and fewer-than-four-row inputs are rejected.
The integrated CT mass and terminal radius must agree with metadata within five
reported standard uncertainties.

Run:

```sh
python3 carbon_sample_analysis.py \
  --metadata carbon_sample_templates/sample_metadata.json \
  --ct-density carbon_sample_templates/ct_density.csv \
  --residual-stress carbon_sample_templates/residual_stress.csv \
  --output carbon_sample_analysis.json
```

The result remains conditional on universal source/detector coupling, a massless
long-range scalar, spherical reduction, and the declared uncertainty model.
Temperature is recorded for provenance; no thermal constitutive correction is
applied without measured material coefficients.
