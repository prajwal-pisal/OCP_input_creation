from ase.io import read, write
import pickle
from ocdata.core import Adsorbate, Slab, Bulk, AdsorbateSlabConfig
import os, gzip



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
            
    def create_ocp_slabs_from_bulk(self):
        bulk_path = os.path.join(self.bulk_path,'vasprun.xml')
        if os.path.exists(bulk_path):
            bulk_atoms_obj = read(bulk_path)
        else:
            bulk_path = os.path.join(self.bulk_path, 'vasprun.xml.gz')
            bulk_atoms_obj = read(bulk_path)
        ocp_bulk = Bulk(bulk_atoms=bulk_atoms_obj)
        slabs = Slab.from_bulk_get_all_slabs(bulk=ocp_bulk)
        only_slabs_pickle = os.path.join(self.save_path, 'slabs.pkl')
        with open(only_slabs_pickle, 'wb') as f:
            pickle.dump(slabs, f)
        return slabs
    
    def _name_for_adslab(self, slab, adslab_num, adsorbate_suffix):
        miller = slab.millers
        miller_str = ''.join(['+' + str(num) if num >= 0 else str(num) for num in miller])
        inverted = 'T' if slab.top == True else 'F'
        shift = str(slab.shift)[2:4]
        adslab_filename = "{}_{}_{}_{}_{}_{}.xyz".format(self.bulk_material_id,
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
                                                 self._name_for_adslab(slab,
                                                                       adslab_num, 
                                                                       ads_info['suffix']))
                    write(save_filepath, adslab, format='extxyz')    
    
    def run(self):
        self.update_adsorbates_info()
        self.create_and_save_all_adslabs()
        return None
    
    
