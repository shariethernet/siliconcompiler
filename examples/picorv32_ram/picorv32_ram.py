
import importlib
import os
import siliconcompiler

def build_top():
    # Core settings.
    design = 'picorv32_top'
    target = 'skywater130_demo'
    die_w = 800
    die_h = 800

    # Create Chip object.
    chip = siliconcompiler.Chip(design)

    # Set default Skywater130 PDK / standard cell lib / flow.
    target_module = importlib.import_module(f'targets.{target}')
    chip.use(target_module)

    # Set design source files.
    rootdir = os.path.dirname(__file__)
    chip.input(os.path.join(rootdir, f"{design}.v"))
    chip.input(os.path.join(rootdir, "picorv32.v"))
    chip.input(os.path.join(rootdir, "sky130_sram_2k.bb.v"))
    chip.input(os.path.join(rootdir, f"{design}.sdc"))

    # Optional: Relax linting and/or silence each task's output in the terminal.
    chip.set('option', 'relax', True)
    chip.set('option', 'quiet', True)

    # Set die outline and core area.
    chip.set('constraint', 'outline', [(0,0), (die_w, die_h)])
    chip.set('constraint', 'corearea', [(10,10), (die_w-10, die_h-10)])

    # Setup SRAM macro library.
    from sram import sky130_sram_2k
    chip.use(sky130_sram_2k)
    chip.add('asic', 'macrolib', 'sky130_sram_2k')

    # SRAM pins are inside the macro boundary; no routing blockage padding is needed.
    chip.set('tool', 'openroad', 'task', 'route', 'var', 'route', '0', 'grt_macro_extension', '0')

    # Place macro instance.
    chip.set('constraint', 'component', 'sram', 'placement', (400.0, 250.0, 0.0))
    chip.set('constraint', 'component', 'sram', 'rotation', 270)

    # Run the build.
    chip.run()

    return chip

if __name__ == '__main__':
    # Build results.
    chip = build_top()
    # Print results.
    chip.summary()
    # Display results.
    chip.show()