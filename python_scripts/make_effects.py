import os
import json

#root_part = os.path.abspath(os.sep)

pa_path = "C:\Games\Uber Entertainment\Planetary Annihilation Launcher\Planetary Annihilation\stable\media"

mod_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

unit_list_path = "C:\Games\Uber Entertainment\Planetary Annihilation Launcher\Planetary Annihilation\stable\media\pa\units\unit_list.json"

unit_list = json.load(open(unit_list_path))

effect_spec = json.load(open('wtrail.pfx'))

fx_offset = {
    'type':'moving',
    'bone': 'bone_root',
    'filename':'/pa/units/sea/wtrail.pfx',
    'offset':[0, 0, 0]
}

for unit in unit_list['units']:
    # skip the units which are not naval
    if '/pa/units/sea/' not in unit: continue
    

    mod_boat = os.path.join(mod_path, unit[1:])
    pa_boat = os.path.join(pa_path, unit[1:])


    # check if we have a boat in the listed location
    if os.path.exists(pa_boat):
        # check if the current unit has base_ship as a base_spec
        # /pa/units/sea/base_ship/base_ship.json
        
        # load boat json for manipulation
        boat = json.load(open(pa_boat))
        if '/pa/units/sea/base_ship/base_ship.json' not in boat.get('base_spec',''): continue
        if not boat.get('mesh_bounds'): continue
        
        print 'Updating: ', os.path.basename(pa_boat)

        bounds = boat.get('mesh_bounds', [0, 0, 0])
        
        # create mod folder if it does not exist
        if not os.path.exists(os.path.dirname(mod_boat)):
           os.makedirs(os.path.dirname(mod_boat))

        # change our trail effect filename
        fx_offset['filename'] = os.path.dirname(unit) + '/wtrail.pfx'
        windows_pfx_path = os.path.normpath(os.path.join(mod_path, fx_offset['filename'][1:]))

        
        # change the trail offset (the Y offset is half the length of the ship minus 1
        fx_offset['offset'] = [0, float(bounds[1]) / 2 - 1, 0]

        # get offset list from the actual boat json
        #    if it doesn't exist already, return empty array to append to
        fx_offsets = boat.get('fx_offsets', [])
        # add our custom offset
        fx_offsets.append(fx_offset)

        # override boat fx_offsets array
        boat['fx_offsets'] = fx_offsets

        ## TODO: modify actualy water trail effect based on the dimensions and speed
        #        of the ship

        
        json.dump(effect_spec, open(windows_pfx_path, 'w'), indent=4, sort_keys=True)
        json.dump(boat, open(mod_boat, 'w'), indent=4, sort_keys=True)  
