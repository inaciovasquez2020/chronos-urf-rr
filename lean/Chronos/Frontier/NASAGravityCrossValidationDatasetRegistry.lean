import Chronos.Frontier.RealGRACEFOTidalDerivativeModelRun

namespace Chronos.Frontier

structure NASAGravityCrossValidationDatasetEntry where
  shortName : String
  sourceCenter : String
  role : String
  registryStatus : String
  realPayloadRequiredBeforeUse : Bool
  boundaryLocked : Bool
deriving Repr, Inhabited

def NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_2026_05_29 :
    List NASAGravityCrossValidationDatasetEntry :=
  [
    {
      shortName := "GRACEFO_L2_JPL_MONTHLY_0063"
      sourceCenter := "PO.DAAC / JPL / NASA"
      role := "authenticated monthly spherical-harmonic gravity payload already bound"
      registryStatus := "BOUND_AUTHENTICATED_PAYLOAD"
      realPayloadRequiredBeforeUse := false
      boundaryLocked := true
    },
    {
      shortName := "TELLUS_GRAC-GRFO_MASCON_GRID_RL06.3_V4"
      sourceCenter := "PO.DAAC / JPL / NASA"
      role := "global monthly mass anomaly / equivalent-water-height cross-validation"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.3_V4"
      sourceCenter := "PO.DAAC / JPL / NASA"
      role := "coastal-resolution-improved mass anomaly cross-validation"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "GRC-GFO_GRIDDED_AOD1B_JPL_MASCON_RL06.3"
      sourceCenter := "PO.DAAC / JPL / NASA"
      role := "atmosphere-ocean de-aliasing control for gravity payload"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "GLDAS_NOAH025_3H_2.1"
      sourceCenter := "GES DISC / NASA"
      role := "land hydrology and soil-water control"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "SPL4SMGP.008"
      sourceCenter := "NSIDC DAAC / NASA"
      role := "SMAP surface and root-zone soil-moisture control"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "ATL06.007"
      sourceCenter := "NSIDC DAAC / NASA"
      role := "ICESat-2 land-ice height control"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "SWOT_L2_HR_RiverSP_2.0"
      sourceCenter := "PO.DAAC / NASA"
      role := "river surface elevation, slope, width, and discharge control"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "GPM_3IMERGDF.07"
      sourceCenter := "GES DISC / NASA"
      role := "daily precipitation forcing control"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "MERRA2_SURFACE_ATMOSPHERE_PRODUCTS"
      sourceCenter := "GES DISC / NASA GMAO"
      role := "atmospheric pressure and surface flux control"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "CDDIS_GNSS_SLR_PRODUCTS"
      sourceCenter := "CDDIS / NASA"
      role := "independent geodetic deformation and orbit-control evidence"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    },
    {
      shortName := "NASA_LAMBDA_CMB_PRODUCTS"
      sourceCenter := "NASA LAMBDA / GSFC"
      role := "cosmology-side archive for cross-domain boundary discipline"
      registryStatus := "REGISTERED_SOURCE_ONLY_PAYLOAD_NOT_BOUND"
      realPayloadRequiredBeforeUse := true
      boundaryLocked := true
    }
  ]

def NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_STATUS_2026_05_29 : String :=
  "NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_CREATED"

theorem nasaGravityCrossValidationDatasetRegistryCount :
    NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_2026_05_29.length = 12 := by
  rfl

theorem nasaGravityCrossValidationDatasetRegistryStatus :
    NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_STATUS_2026_05_29 =
      "NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_CREATED" := by
  rfl

theorem nasaGravityCrossValidationFirstPayloadBound :
    (NASA_GRAVITY_CROSS_VALIDATION_DATASET_REGISTRY_2026_05_29.head!).registryStatus =
      "BOUND_AUTHENTICATED_PAYLOAD" := by
  rfl

end Chronos.Frontier
