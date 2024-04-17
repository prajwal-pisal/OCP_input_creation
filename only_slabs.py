from input_gen import OCPInputGenerator


bulk_material_id = 'Co2_mp-54'
adsorbates_path = "/scratch/project_2005750/adsorbants/ocp_ecut_450"
bulk_path = "/scratch/project_2005750/bulks_opt/metals_rpbe/{}".format(bulk_material_id)
save_path = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/z_done/short_list/{}".format(bulk_material_id)

ocp_inputs = OCPInputGenerator(adsorbates_path=adsorbates_path,
                              bulk_path=bulk_path,
                              is_metal=True, 
                              bulk_material_id=bulk_material_id,
                              save_path=save_path)

ocp_inputs.write_slab_inputs()
