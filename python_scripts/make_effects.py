import os
import json
import utils

import copy
import math

import random

pa_path = utils.pa_dir()

mod_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

unit_list_path = "/pa/units/unit_list.json"

unit_list = utils.load_base_json(unit_list_path)

# above water trail
water_trail = utils.load_local_json('wtrail.pfx')

water_trail['emitters'].append(water_trail['emitters'][2].copy())
water_trail['emitters'][3]['velocityX'] = -water_trail['emitters'][2]['velocityX']
water_trail['emitters'][3]['offsetX'] = -water_trail['emitters'][2]['offsetX']

base_trail = copy.deepcopy(water_trail)

fx_offset = {
    'type':'moving',
    'bone': 'bone_root',
    'filename':'',
    'offset':[0, 0, 0]
}

for unit in unit_list['units']:
    # skip the units which are not naval
    if '/pa/units/sea/' not in unit: continue
    

    mod_boat = os.path.join(mod_path, unit[1:])
    pa_boat = os.path.join(pa_path, unit[1:])

    # reset our trail
    water_trail = copy.deepcopy(base_trail)

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
        fx_offset['filename'] = os.path.dirname(unit) + '/wtrail_generated.pfx'
        windows_pfx_path = os.path.normpath(os.path.join(mod_path, fx_offset['filename'][1:]))

        # trying to get the died path effect to be removed
        events ['died'] = 
        
        # change the trail offset (the Y offset is half the length of the ship minus 1
        fx_offset['offset'] = [0, float(bounds[1]) / 2, 0]

        # get offset list from the actual boat json
        #    if it doesn't exist already, return empty array to append to
        fx_offsets = boat.get('fx_offsets', [])
        # add our custom offset
        fx_offsets.append(fx_offset)

        # override boat fx_offsets array
        boat['fx_offsets'] = fx_offsets

        
        ## TODO: modify actualy water trail effect based on the dimensions and speed
        #        of the ship
        water_trail['emitters'][2]['velocity'] = float(boat['navigation']['move_speed']) / 2
        water_trail['emitters'][3]['velocity'] = float(boat['navigation']['move_speed']) / 2

        # add kick up for fast boats
        if "WL_Underwater" not in boat['spawn_layers']:
            emitter = copy.deepcopy(water_trail['emitters'][1])
            
            emitter["velocityY"] = 0.5
            emitter["velocityZ"] = 1

            emitter["velocity"] = boat['navigation']['move_speed']
            emitter["gravity"] = -20

            v = emitter['velocityZ'] / math.sqrt(emitter['velocityZ'] ** 2 + emitter['velocityY'] ** 2) * emitter["velocity"]
            g = emitter["gravity"]
            
            emitter["lifetime"] = (2 * v) / math.fabs(g)
            emitter["lifetimeRange"] = 0.1
            water_trail['emitters'].append(emitter)
                
        else:
            # "spawn_layers": "WL_Underwater",
            # make special effects for the subs!
            # remove the wakes
            water_trail['emitters'] = water_trail['emitters'][:-2]
            # remove the random offset
            for i in xrange(2):
                water_trail['emitters'][i]['offsetRangeX'] = 0
                water_trail['emitters'][i]['offsetRangeY'] = 0
                water_trail['emitters'][i]['offsetRangeZ'] = 0
                water_trail['emitters'][i]['offsetX'] = {'keys':[], 'stepped':True}
                water_trail['emitters'][i]['offsetY'] = {'keys':[], 'stepped':True}
                water_trail['emitters'][i]['offsetZ'] = {'keys':[], 'stepped':True}

                time_end = water_trail['emitters'][i]['emitterLifetime']
                rate = water_trail['emitters'][i]['emissionRate']

                steps = int(time_end * rate)

                coils = 4
                
                radius = bounds[0] / 3
                
                for j in xrange(steps):
                    o = random.randint(0, 1)
                    # o = i

                    d = 1
                    
                    a = float(j) / steps
                    water_trail['emitters'][i]['offsetX']['keys'].append([time_end * a, radius * math.cos(o * math.pi + d * a * math.pi * 2 * coils)])
                    water_trail['emitters'][i]['offsetZ']['keys'].append([time_end * a, radius * math.sin(o * math.pi + d * a * math.pi * 2 * coils)])

                #water_trail['emitters'][i]['gravity'] = 1
                water_trail['emitters'][i]['velocity'] = float(boat['navigation']['move_speed']) / 2
                
                water_trail['emitters'][i]['velocityY'] = 1
                water_trail['emitters'][i]['velocityZ'] = 0.5

                water_trail['emitters'][i]['drag'] = 0.9887
                
        
        
        
        json.dump(water_trail, open(windows_pfx_path, 'w'), indent=4, sort_keys=True)
        json.dump(boat, open(mod_boat, 'w'), indent=4, sort_keys=True)  
