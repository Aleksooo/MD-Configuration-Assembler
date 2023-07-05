#include <iostream>
#include <iomanip>
#include <filesystem>
#include "handler.hpp"
#include "struct/Atom.hpp"
#include "struct/Molecule.hpp"
#include "struct/System.hpp"
#include "IO/io_gro.hpp"
#include "shapes/Box.hpp"
#include "shapes/Cylinder.hpp"
#include "shapes/AntiCylinder.hpp"
#include "alg/generator.hpp"
#include "random"

const double MIN_DIST2 = 0.08 * 0.08;
const double MAX_DIST2= 0.12 * 0.12;
const double PACKAGE = 0.4;


int main() {
    std::random_device rd;
    std::mt19937 gen(rd());

    System sys("Test", vec({3, 3, 3}));

    // Decane
    std::filesystem::path decane_inp("../ff/gromos/gro/decane.gro");
    Molecule decane = read_mol(decane_inp);
    Cylinder cylinder(sys.get_center(), 1, 3, vec({1, 0, 0}));

    std::cout << "Inserting decane with densicty " << std::setprecision(3) << 26 / cylinder.get_volume() << std::endl;
    for (size_t mol_id = 1; mol_id <= 26; mol_id++) {
        insert_mol_into_shape(sys, cylinder, decane, mol_id, gen, MIN_DIST2, PACKAGE);
    }


    // Water
    std::filesystem::path water_inp("../ff/gromos/gro/water.gro");
    Molecule water = read_mol(water_inp);
    AntiCylinder anticylinder(cylinder, Box(sys.get_center(), sys.box));

    std::cout << "Inserting water with densicty " << std::setprecision(3) << 580 / anticylinder.get_volume() << std::endl;
    for (size_t mol_id = 1; mol_id <= 580; mol_id++) {
        insert_mol_into_shape(sys, anticylinder, water, mol_id, gen);
    }

    push_atoms_apart(sys, gen, MIN_DIST2, MAX_DIST2);

    std::filesystem::path outp("../decane_test.gro");
    write_sys(sys, outp);

    return 0;
}
