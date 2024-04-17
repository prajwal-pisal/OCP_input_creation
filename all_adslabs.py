from input_gen import OCPInputGenerator

adsorbates_path = "/scratch/project_2005750/adsorbants/ocp_ecut_450"
material_id = "VGaFe2_mp-21883"
bulk_path = "/scratch/project_2005750/bulks_opt/trimetallics_rpbe/{}".format(material_id)
save_path = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/equiformer_v2/trimetallics/{}_eq2/adslabs/".format(material_id)


ocp_inputs = OCPInputGenerator(adsorbates_path=adsorbates_path,
                              bulk_path=bulk_path,
                              is_metal=True, 
                              bulk_material_id=material_id,
                              save_path=save_path)

ocp_inputs.create_all_adslabs()