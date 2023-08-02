from ase.io import read, write
from ase import Atoms
import pickle
from ocdata.core import Adsorbate, Slab, Bulk, AdsorbateSlabConfig
import os
import json



class OCPInputGenerator():
    def __init__(self, adsorbates_path, is_metal : bool):
        self.adsorbates_path = adsorbates_path
        self.is_metal = is_metal
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
            
    
