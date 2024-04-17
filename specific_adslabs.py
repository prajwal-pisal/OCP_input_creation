from input_gen import OCPInputGenerator

adsorbates_path = "/scratch/project_2005750/adsorbants/ocp_ecut_450"
material_id = "NiZn_mp-1486"
bulk_path = "/scratch/project_2005750/bulks_opt/metals_rpbe/{}".format(material_id)
save_path = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/equiformer_v2/bimetallics/{}_eq2/adslabs".format(material_id)
#best_slabs_csv = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/ZnO_mp-2133_ads_OCP/slabs/best_surfaces.txt"
precom_slab_pkl = "/scratch/project_2005750/Surf_adsorprion_energy_calc_OCP/short_list/NiZn_mp-1486_ads_OCP/slabs.pkl"

ocp_inputs = OCPInputGenerator(adsorbates_path=adsorbates_path,
                              bulk_path=bulk_path,
                              is_metal=True, 
                              bulk_material_id=material_id,
                              save_path=save_path)

ocp_inputs.create_specific_adslabs(precom_slab_pkl=precom_slab_pkl)