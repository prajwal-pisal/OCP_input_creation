from input_gen import OCPInputGenerator

adsorbates_path = "/scratch/project_2005750/adsorbants/ocp_ecut_450"
bulk_path = "/scratch/project_2005750/bulks_opt/ZnO/"
save_path = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/ZnO_mp-2133_ads_OCP"

ocp_inputs = OCPInputGenerator(adsorbates_path=adsorbates_path,
                              bulk_path=bulk_path,
                              is_metal=False, 
                              bulk_material_id='ZnO_mp-2133',
                              save_path=save_path)

ocp_inputs.write_slab_inputs()