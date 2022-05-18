#!/usr/bin/env python3

import sys, os

def parseKinetic(kin_file, the_file):

    with open(kin_file) as f:
        lines = f.readlines()
    f.close()

    lines = [item.replace('\t',' ') for item in lines ]
    lines = [item.replace('\n','') for item in lines ]

    idx_specie = lines.index('SPECIES')+1
    species = lines[idx_specie].split(' ')
    species[:] = [x for x in species if x]

    with open(the_file) as f:
        lines = f.readlines()
    f.close()

    out_thermo = []
    out_thermo.append('THERMO ALL\n')
    out_thermo.append('   300.000  1000.000  3000.000\n')

    for j in range(len(species)):
        for k in range(2,len(lines)):
            if(lines[k].find(species[j]+' ')==0):
                out_thermo.append(lines[k])
                out_thermo.append(lines[k+1])
                out_thermo.append(lines[k+2])
                out_thermo.append(lines[k+3])
                break
                
    out_thermo.append(lines[-1])
    with open('Thermo_of.tdc','w') as f:
        f.writelines(out_thermo)
    f.close()
    
def inputOS(kin_file,the_file,sur_file,tra_file):
    lines = []
    lines.append('Dictionary CHEMKIN_PreProcessor\n{\n')
    lines.append('\t@Thermodynamics\t'+the_file+';\n')
    lines.append('\t@Kinetics\t'+kin_file+';\n')
    lines.append('\t@Surface\t'+sur_file+';\n')
    lines.append('\t@Transport\t'+tra_file+';\n')
    lines.append('\t@Output\t'+'kinetics'+';\n')
    lines.append('}\n')
    
    with open('input.dic','w') as f:
        f.writelines(lines)
    f.close()
     
def main():
    kin_file = sys.argv[1]
    the_file = sys.argv[2]
    sur_file = sys.argv[3]
    tra_file = sys.argv[4]
    print('\n|-------------------------------------------------------------|')
    print('|                                                             |')
    print('|   Kinetic scheme preprocessor for catalyticFOAM             |')
    print('|                                                             |')
    print('|-------------------------------------------------------------|')
    print('|   Mauro Bracconi & Matteo Maestri                           |')
    print('|   mauro.bracconi@polimi.it - matteo.maestri@polimi.it       |')
    print('|   Politecnico di Milano - Dipartimento di Energia           |')
    print('|                                                             |')
    print('|-------------------------------------------------------------|\n')
    
    parseKinetic(kin_file,the_file)
    inputOS(kin_file,the_file,sur_file,tra_file)
    os.system('catalyticFoam_CHEMKINPreProcessor > log.os')
    print(' * Kinetic scheme preprocessed with OpenSMOKE++/catalyticSMOKE')
    os.system('catalyticFoam_TransportPreProcessor kinetics > log.ctt && mv transportProperties kinetics/')
    print(' * Transport properties parsed')
    os.system('chemkinToFoam '+ kin_file + ' Thermo_of.tdc ' + ' kinetics/transportProperties  kinetics/kineticOF kinetics/thermoOF > log.ctf')
    print(' * Kinetic scheme preprocessed with OpenFOAM')
    os.system('rm -rf log.* input.dic Thermo_of.tdc ')
    print('\n =========== Kinetic scheme parsed and ready to use ===========\n')
    
if __name__ == "__main__":
    main()
