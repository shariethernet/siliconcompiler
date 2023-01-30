import os
import re
import shutil

def setup(chip):

    tool = 'vpr'
    refdir = 'tools/'+tool
    step = chip.get('arg','step')
    index = chip.get('arg','index')
    task = 'apr'

    chip.set('tool', tool, 'exe', tool, clobber=False)
    chip.set('tool', tool, 'version', '0.0', clobber=False)

    chip.set('tool', tool, 'task', task, 'threads', step, index, os.cpu_count(), clobber=False)

    #TO-DO: PRIOROTIZE the post-routing packing results?
    design = chip.top()
    chip.set('tool', tool, 'task', task, 'output', step, index, design + '.net')
    chip.add('tool', tool, 'task', task, 'output', step, index, design + '.place')
    chip.add('tool', tool, 'task', task, 'output', step, index, design + '.route')
    chip.add('tool', tool, 'task', task, 'output', step, index, 'vpr_stdout.log')

    topmodule = chip.top()
    blif = "inputs/" + topmodule + ".blif"

    options = []
    for arch in chip.get('fpga','arch'):
        options.append(arch)

    options.append(blif)

    if 'sdc' in chip.getkeys('input'):
        options.append(f"--sdc_file {chip.get('input', 'fpga', 'sdc')}")

    threads = chip.get('tool', tool, 'task', task, 'threads', step, index)
    options.append(f"--num_workers {threads}")

    chip.add('tool', tool, 'task', task, 'option', step, index,  options)

#############################################
# Runtime pre processing
#############################################

def pre_process(chip):

    #have to rename the net connected to unhooked pins from $undef to unconn
    # as VPR uses unconn keywords to identify unconnected pins

    step = chip.get('arg','step')
    index = chip.get('arg','index')
    design = chip.top()
    blif_file = f"{chip._getworkdir()}/{step}/{index}/inputs/{design}.blif"
    print(blif_file)
    with open(blif_file,'r+') as f:
        netlist = f.read()
        f.seek(0)
        netlist = re.sub(r'\$undef', 'unconn', netlist)
        f.write(netlist)
        f.truncate()

################################
# Post_process (post executable)
################################

def post_process(chip):
    ''' Tool specific function to run after step execution
    '''

    step = chip.get('arg','step')
    index = chip.get('arg','index')
    task = chip._get_task(step, index)

    for file in chip.get('tool', 'vpr', 'task', task, 'output', step, index):
        shutil.copy(file, 'outputs')
    design = chip.top()
    shutil.copy(f'inputs/{design}.blif', 'outputs')
    #TODO: return error code
    return 0