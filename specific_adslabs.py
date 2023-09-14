from input_gen import OCPInputGenerator

adsorbates_path = "/scratch/project_2005750/adsorbants/ocp_ecut_450"
bulk_path = "/scratch/project_2005750/bulks_opt/ZnO/"
save_path = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/ZnO_mp-2133_ads_OCP/adslabs"
best_slabs_csv = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/ZnO_mp-2133_ads_OCP/slabs/best_surfaces.txt"

ocp_inputs = OCPInputGenerator(adsorbates_path=adsorbates_path,
                              bulk_path=bulk_path,
                              is_metal=False, 
                              bulk_material_id='ZnO_mp-2133',
                              save_path=save_path)

ocp_inputs.create_specific_adslabs(path_to_best_slabs_csv=best_slabs_csv)