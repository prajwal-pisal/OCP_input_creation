from ase.io import read, write
import pickle
from ocdata.core import Adsorbate, Slab, Bulk, AdsorbateSlabConfig
import os, gzip, json
import pandas as pd



class OCPInputGenerator():
    def __init__(self, adsorbates_path, bulk_path, is_metal : bool, bulk_material_id: str, save_path = None):
        self.adsorbates_path = adsorbates_path
        self.bulk_path = bulk_path
        self.bulk_material_id = bulk_material_id
        self.is_metal = is_metal
        self.save_path = save_path
        self.adsorbates_info = {'d_H': {"suffix": "-H" ,
                                       "binding_index":[0],
                                        } ,
                               'd_OH': {"suffix": "-OH",
                                       "binding_index":[0],
                                        }, 
                               'm_CO': {"suffix": "-CO",
                                       "binding_index":[0],
                                        },
                               'd_OCH3':{"suffix": "-OCH3",
                                       "binding_index":[4],
                                        },
                               'd_OCHO':{"suffix": "-OCHO",
                                       "binding_index":[1],
                                        }
                               }
        if self.save_path == None:
            self.save_path = os.path.join(os.getcwd(), bulk_material_id)
            os.makedirs(self.save_path, exist_ok=True)
        else: 
            os.makedirs(self.save_path, exist_ok=True)
        self.ocp_bulk = self.read_bulk_and_create_bulk_obj()
        pass
        

    def update_adsorbates_info(self):
        for adsorbate_dir, ads_info in self.adsorbates_info.items():
            adsorbate_path = os.path.join(self.adsorbates_path, adsorbate_dir, 'vasprun.xml')
            ads_atoms_obj = read(adsorbate_path)
            ads_info['atoms_obj'] = ads_atoms_obj
            ocp_adsorbate = Adsorbate(adsorbate_atoms=ads_atoms_obj,
                                      adsorbate_binding_indices=ads_info['binding_index'])
            ads_info['ocp_adsorbate'] = ocp_adsorbate
        return self.adsorbates_info

    def get_optimized_suffix_custodian(self, path_to_vasp_dir):
        custodian_file = [file for file in os.listdir(path_to_vasp_dir) if file.startswith("custodian")][0]
        custodian_file_path = os.path.join(path_to_vasp_dir, custodian_file)
        if custodian_file_path.endswith('.gz'):
            with gzip.open(custodian_file_path) as f:
                custodian_handler = json.load(f)
        else:
            with open(custodian_file_path, 'r') as f:
                custodian_handler = json.load(f) 
        if custodian_handler[-1]['job']['final']==True:
            output_tag = custodian_handler[-1]['job']['suffix']
        return output_tag

    
    def read_bulk_and_create_bulk_obj(self):
        bulk_path = os.path.join(self.bulk_path,'vasprun.xml')
        if os.path.exists(bulk_path):
            bulk_atoms_obj = read(bulk_path)
        else:
            custodian_suffix = self.get_optimized_suffix_custodian(self.bulk_path)
            bulk_path = os.path.join(self.bulk_path, 'vasprun.xml{}.gz'.format(custodian_suffix))
            bulk_atoms_obj = read(bulk_path, format='vasp-xml')
        ocp_bulk = Bulk(bulk_atoms=bulk_atoms_obj)
        return ocp_bulk
            
    def create_ocp_slabs_from_bulk(self):
        slabs = Slab.from_bulk_get_all_slabs(bulk=self.ocp_bulk)
        only_slabs_pickle = os.path.join(self.save_path, 'slabs.pkl')
        with open(only_slabs_pickle, 'wb') as f:
            pickle.dump(slabs, f)
        return slabs
    
    def _name_for_slab(self, slab, adslab_num, adsorbate_suffix):
        miller = slab.millers
        miller_str = ''.join(['+' + str(num) if num >= 0 else str(num) for num in miller])
        inverted = 'T' if slab.top == True else 'F'
        shift = str(slab.shift)[2:4]
        if adslab_num == None and adsorbate_suffix == None:
            slab_filename = "{}_{}_{}_{}.json".format(self.bulk_material_id,
                                                miller_str,
                                                inverted,
                                                shift)  
            return slab_filename  
        else:
                    
            adslab_filename = "{}_{}_{}_{}{}_{}.json".format(self.bulk_material_id,
                                                miller_str,
                                                inverted,
                                                shift, 
                                                adsorbate_suffix,
                                                adslab_num)
            return adslab_filename
    
    def create_and_save_all_adslabs(self):
        slabs = self.create_ocp_slabs_from_bulk()
        for slab in slabs:
            for adsorbate_dir, ads_info in self.adsorbates_info.items():
                adslabs = AdsorbateSlabConfig(slab=slab,
                                              adsorbate=ads_info['ocp_adsorbate'],
                                              mode='heuristic')
                for adslab_num, adslab in enumerate(adslabs.atoms_list):
                    save_filepath = os.path.join(self.save_path, 
                                                 self._name_for_slab(slab,
                                                                       adslab_num, 
                                                                       ads_info['suffix']))
                    write(save_filepath, adslab, format='json')    
    
    def write_slab_inputs(self):
        slabs = self.create_ocp_slabs_from_bulk()
        save_filepath = os.path.join(self.save_path,
                                         'slabs')
        if not os.path.exists(save_filepath):
                os.makedirs(save_filepath)
        for slab in slabs:
            slabname = self._name_for_slab(slab, adslab_num=None, adsorbate_suffix=None)
            write(os.path.join(save_filepath, slabname), slab.atoms, format='json')


    def get_best_slabs_from_csv(self, path_to_best_slabs_csv, precom_slab_pkl):
        best_surfaces_df = pd.read_csv(path_to_best_slabs_csv, delimiter=" ", header=None)
        _best_surface_list = list(best_surfaces_df.sort_values(by=1).iloc[:,0])
        best_surfaces_list = [surface.replace('traj', 'json') for surface in _best_surface_list]
        best_slabs_dict = dict()
        slab_from_pkl = Slab.from_precomputed_slabs_pkl(bulk=self.ocp_bulk, precomputed_slabs_pkl=precom_slab_pkl)
        all_slabs_dict = dict()
        for slab in slab_from_pkl:
            slabname = self._name_for_slab(slab=slab, adslab_num=None, adsorbate_suffix=None)
            all_slabs_dict[slabname] = slab
        for slab in best_surfaces_list:
            best_slabs_dict[slab] = all_slabs_dict[slab]
        return best_slabs_dict

    def create_specific_adslabs(self, path_to_best_slabs_csv, precom_slab_pkl):
        self.update_adsorbates_info()
        best_slabs_dict = self.get_best_slabs_from_csv(path_to_best_slabs_csv, precom_slab_pkl)
        all_adslabs = dict()
        for slabname, slab in best_slabs_dict.items():
             for adsorbate_id, adsorbate in self.adsorbates_info.items():
                adslabs = AdsorbateSlabConfig(slab=slab, adsorbate=adsorbate['ocp_adsorbate'], mode='heuristic')
                for adslab_num, adslab in enumerate(adslabs.atoms_list):
                            adslab_filename = self._name_for_slab(slab,
                                                                adslab_num, 
                                                                adsorbate['suffix'])
                            save_filepath = os.path.join(self.save_path, 
                                                        adslab_filename)
                            all_adslabs[adslab_filename] = adslab 
                            write(save_filepath, adslab, format='json')
        return all_adslabs 
    
    def create_all_adslabs(self):
        self.update_adsorbates_info()
        self.create_and_save_all_adslabs()
        return None
    
    
