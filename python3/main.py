"""IBD X Caller, main function.
Pulls together other modules and directs loading/running them.
@author: Harald Ringbauer, 2020
"""


import os as os
import sys as sys   # For piping the output
import numpy as np

from emission import load_emission_model
from transition import load_transition_model
from loaddata import load_loaddata
from hmm import load_fwd_bwd_func
from postprocessing import load_Postprocessing

class HMM_Full(object):
    """Analyze Class for HMMs. Wrapper for various subclasses, making them
    work together.
    Contains objects as field for pre-processing, transition as well as
    emission probabilities, loading and post-processing
    Contains most Parameters (but some of them like the output folders are decided
    by pre-processing subclass)"""
    folder_in = ""
    folder_out = "" # For book keeping of the output path
    
    l_model = "" # simulated
    e_model = "" # haploid_gl
    t_model = "" # standard
    p_model = ""
    h_model = "" # FiveState FiveStateFast
    post_model = ""
    
    l_obj, t_obj, e_obj = 0, 0, 0 # Placeholder for the objects
    fwd_bwd = 0 # Placeholder Forward Backward Function
    submat33 = True
    in_val = 1e-4 # The initial prob. in each first/last IBD state
    output = True
    

    def __init__(self, folder_in="", l_model="simulated", t_model="standard", 
                 e_model="haploid_gl", h_model = "FiveStateFast", p_model="hapROH",
                 output=True, load=True):
        """Initialize Class.
        Keywords for which subclasses to load (via factory functions from there.
        load: Whether to load all models at intialization. True per Default."""
        self.set_params(folder_in=folder_in, l_model=l_model, 
                        t_model=t_model, e_model=e_model, 
                        h_model=h_model, p_model=p_model, output=output)
        
        if load:
            self.load_objects()

    def load_objects(self):
        """Load all the required Objects in right order"""
        self.l_obj = load_loaddata(l_model = self.l_model, path=self.folder_in)
        self.t_obj = load_transition_model(t_model = self.t_model)
        self.e_obj = load_emission_model(e_model = self.e_model)
        self.p_obj = l = load_Postprocessing(p_model=self.p_model)
        self.fwd_bwd = load_fwd_bwd_func(h_model=self.h_model)
        
        ### pass on output parameter
        for o in [self.l_obj, self.t_obj, self.e_obj, self.p_obj]:
            o.set_params(output=self.output)
        
    def run_fwd_bwd(self, full=True):
        """Run Forward Backward algorithm."""
        htsl, p, r_vec =  self.l_obj.load_all_data()
        e_mat = self.e_obj.give_emission_matrix(htsl, p)
        t_mat = self.t_obj.full_transition_matrix(r_vec, n=4, submat33=self.submat33)
        
        if full:
            post, fwd, bwd, tot_ll = self.fwd_bwd(np.log(e_mat), t_mat, in_val = self.in_val, 
                                                  full=full, output=self.output)
            self.p_obj.call_roh(r_vec, post)
            return post, r_vec, fwd, bwd, tot_ll
        else:
            post = self.fwd_bwd(np.log(e_mat), t_mat, in_val = self.in_val, 
                                full=full, output=self.output)
            self.p_obj.call_roh(r_vec, post)
            return post, r_vec                                                                    
                 
    def set_params(self, **kwargs):
        """Set the Parameters.
        Takes keyworded arguments"""
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    ##################################################
    ### Prepping output folder and piping output there
    
    def prepare_path(self, base_path, iid, ch, prefix_out="", logfile=False):
        """Prepare the output path and pipe printing for one Individual.
        Create Path if not already existing.
        prefix_out: Optional additonal folder.
        logfile: Whether to pipe output to log-file [Warning: it is a hack]"""  
        if isinstance(iid, (list, np.ndarray)):
            iid = "_".join(iid) # If multiple individual names given (for X IBD)
        path_out = os.path.join(base_path, iid, "chr" + str(ch), prefix_out, "")
        if not os.path.exists(path_out):
                os.makedirs(path_out)
        self.folder_out = path_out
        
        ### Activate LOG FILE output if given
        if logfile == True:
            path_log = os.path.join(path_out, "hmm_run_log.txt")
            print(f"Set Output Log to path: {path_log}")
            sys.stdout = open(path_log, 'w') 
        return path_out
    
    def reset_print(self):
        """Resets output to console."""
        sys.stdout = sys.__stdout
        if self.output:
            print("Output was reset to standard console.")