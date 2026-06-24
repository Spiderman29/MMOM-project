#!/usr/bin/python3
import sys

def parse_lammps_dump_to_csv(filepath, output_csv):
    """
    Legge il file di LAMMPS e lo converte in un vero file CSV standard.
    Ogni riga del CSV sarà un singolo atomo con le sue coordinate e forze.
    """
    print(f"Inizio estrazione da {filepath} a {output_csv}...")
    
    # Apriamo il file di output in modalità scrittura testuale
    with open(output_csv, 'w') as out_f:
        # 1. Scriviamo l'intestazione del CSV (i nomi delle colonne)
        header = "timestep,box_x,box_y,box_z,atom_id,x,y,z,fx,fy,fz,pe_atom\n"
        out_f.write(header)
        
        # Apriamo il file di input
        with open(filepath, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break # Fine del file
                
                # Trova il timestep
                if "ITEM: TIMESTEP" in line:
                    timestep = f.readline().strip()
                    
                # Trova il numero di atomi
                elif "ITEM: NUMBER OF ATOMS" in line:
                    n_atoms = int(f.readline().strip())
                    
                # Estrai le dimensioni della scatola
                elif "ITEM: BOX BOUNDS" in line:
                    box_x_data = f.readline().split()
                    box_y_data = f.readline().split()
                    box_z_data = f.readline().split()
                    
                    # Calcoliamo la lunghezza (Max - Min) per ogni asse
                    box_x = f"{float(box_x_data[1]) - float(box_x_data[0]):.4f}"
                    box_y = f"{float(box_y_data[1]) - float(box_y_data[0]):.4f}"
                    box_z = f"{float(box_z_data[1]) - float(box_z_data[0]):.4f}"
                    
                # Estrai le coordinate e scrivi direttamente nel CSV
                elif "ITEM: ATOMS" in line:
                    for _ in range(n_atoms):
                        data = f.readline().split()
                        
                        # Struttura riga LAMMPS: id type x y z fx fy fz c_pe_atom
                        atom_id = data[0]
                        x, y, z = data[2], data[3], data[4]
                        fx, fy, fz = data[5], data[6], data[7]
                        pe_atom = data[8]
                        
                        # Creiamo la riga separata da virgole e la scriviamo sul file
                        row = f"{timestep},{box_x},{box_y},{box_z},{atom_id},{x},{y},{z},{fx},{fy},{fz},{pe_atom}\n"
                        out_f.write(row)
                        
    print("Operazione completata con successo! Il file CSV standard è pronto.")

# ==========================================
# Esecuzione principale
# ==========================================
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Utilizzo: python .\extract_dump.py <file.dump> <file.csv>")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2]
    parse_lammps_dump_to_csv(filepath=infile, output_csv=outfile)