import json
import argparse


parser = argparse.ArgumentParser(description='Clean-up exercise notebooks.')
parser.add_argument('filenames', metavar='filename', type=str, nargs='+',
                   help='names of the notebooks to be cleaned')
parser.add_argument('-s','--solution_only', action='store_false', help='flag used to indicate that clean-up should only run in solution folder')

args = parser.parse_args()

# Open existing notebook
for filename in (([('',fn)
                    for fn in args.filenames
                    if fn[-6:] == '.ipynb'] if args.solution_only else [])
                +[('Solutions/',fn)
                    for fn in args.filenames
                    if fn[-6:] == '.ipynb']):
    with open(filename[0]+filename[1]) as f:
        nb = json.load(f)
        f.close()
    
    if nb['nbformat'] != 4:
        continue
    
    # Create a new dictinary with only the clean data
    nb_clean = dict()
    
    # Transfer version number
    nb_clean['nbformat'] = nb['nbformat']
    nb_clean['nbformat_minor'] = nb['nbformat_minor']
    
    # Only copy relevant metadata
    nb_clean['metadata'] = {k: v for k,v in nb['metadata'].items()
                                if k in ['kernelspec', 'authors']}
    

    # Clean up notebook cells
    for cell in nb['cells']:
        cell['metadata'] = {}
        if cell['cell_type'] == 'code' and filename[0] != 'Solutions/':
            cell['outputs'] = []
            cell['execution_count'] = None
    
    nb_clean['cells'] = nb['cells']
    json.dump(nb_clean, open(filename[0]+filename[1], 'w'), indent=1)
