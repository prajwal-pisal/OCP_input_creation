from input_gen import OCPInputGenerator

adsorbates_path = "/scratch/project_2005750/adsorbants/ocp_ecut_450"
bulk_path = "/scratch/project_2005750/bulks_opt/metals_rpbe/Pt_mp-126"
save_path = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/Pt_mp-126_ads_OCP"

ocp_inputs = OCPInputGenerator(adsorbates_path=adsorbates_path,
                              bulk_path=bulk_path,
                              is_metal=True, 
                              bulk_material_id='Pt_mp-126',
                              save_path=save_path)

ocp_inputs.create_all_adslabs()