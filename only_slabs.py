from input_gen import OCPInputGenerator

adsorbates_path = "/scratch/project_2005750/adsorbants/ocp_ecut_450"
bulk_path = "/scratch/project_2005750/bulks_opt/trimetallics_rpbe/Zn2CuAu_mp-12759"
save_path = "./test/"

ocp_inputs = OCPInputGenerator(adsorbates_path=adsorbates_path,
                              bulk_path=bulk_path,
                              is_metal=True, 
                              bulk_material_id='Zn2CuAu_mp-12759',
                              save_path=save_path)

ocp_inputs.write_slab_inputs()