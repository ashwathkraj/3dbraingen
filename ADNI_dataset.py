import csv
import numpy as np
import torch
from torch.utils.data.dataset import Dataset
import os
from torchvision import transforms
from skimage.transform import resize
from nilearn import surface
import nibabel as nib

class ADNIdataset(Dataset):
    def __init__(self, augmentation=False):
        self.root = os.path.join('..', 'ADNI')
        self.basis = 'FreeSurfer_Cross-Sectional_Processing_brainmask'
        self.filename = 'CN_list.csv'
        self.augmentation = augmentation
        
        self.sids = []
        for line in open("sids.txt"):
            self.sids.append(line.strip())
            
        self.name = self.sids

    def __len__(self):
        return len(self.name)

    def __getitem__(self, index):
        fn = os.path.join(self.root, self.sids[index] + ".nii.gz")
        img = nib.load(fn)

        img = np.swapaxes(img.get_data(),1,2)
        img = np.flip(img,1)
        img = np.flip(img,2)
        sp_size = 64
        img = resize(img, (sp_size,sp_size,sp_size), mode='constant')
        if self.augmentation:
            random_n = torch.rand(1)
            random_i = 0.3*torch.rand(1)[0]+0.7
            if random_n[0] > 0.5:
                img = np.flip(img,0)

            img = img*random_i.data.cpu().numpy()

        imageout = torch.from_numpy(img).float().view(1,sp_size,sp_size,sp_size)
        imageout = imageout*2-1

        return imageout

