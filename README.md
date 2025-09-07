# Qualitative Physics with Dimensional Analysis & π-Calculus
Proof of Concept of the paper "Qualitative Physics Using Dimensional Analysis" by  "R. Bhaskar and Anil Nigam"

This repository demonstrates a **qualitative reasoning model** of a **pressure regulator system** using **dimensional analysis** and **π-calculus**.  
The project combines theoretical foundations (summarized in the included paper), algorithm design (flowcharts and pseudocode), and a Python implementation that propagates qualitative states (Increase, Decrease, Constant, Unknown) across system variables.

---

## 📂 Repository Structure

- **Paper Summary** (`.docx`, `.pdf`)  
  A detailed summary of the research foundations:
  - Dimensional Analysis
  - Buckingham-π Theorem
  - π-Calculus
  - Pressure regulator example and algorithm propagation logic
  - Future enhancement directions

- **code.py**  
  Python implementation of the qualitative reasoning algorithm:
  - Defines variables and qualitative states (`Increase`, `Decrease`, `Constant`, `Unknown`).
  - Implements **propagation functions** for π-regimes:
    - `propagate_pi_a1` – pipe orifice flow regime  
    - `propagate_pi_a2` – inlet/outlet pressure relation  
    - `propagate_pi_b1` – spring valve subsystem  
    - `propagate_pi_c1` – coupling: pressure ↔ outlet pressure  
    - `propagate_pi_c2` – coupling: valve displacement ↔ opening area  
  - Provides `solve_pressure_regulator` to iteratively propagate values until stable.
  - Reports contradictions when input states are inconsistent.

- **Flowcharts/**  
  Contains algorithm flowchart images for the pressure regulator model.

- **Test-Questions/**  
  Documents containing journal paper where this project based-on

- **demo.mkv**  
  Demonstration video showing how the program runs.

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/qualitative-physics-pi-calculus.git
   cd qualitative-physics-pi-calculus

2. Run the Python program:
    ```bash
    python code.py
3. -Choose a **scenario** or enter **manual input**:
    
    -   Example: _Scenario 1 = P_out constant, P_in increasing_
        
-   The algorithm will:
    
    -   Propagate variable states across ensembles and regimes
        
    -   Print intermediate iterations
        
    -   Report if **contradictions** are foun2.  -   d
        

----------

## ✨ Features

-   **Qualitative Reasoning:** Models changes in physical systems without requiring numeric inputs.
    
-   **π-Calculus Framework:** Uses dimensionless numbers (π-groups) as reasoning units.
    
-   **Contradiction Detection:** Identifies when user-defined states conflict with propagation logic.
    
-   **Modular Propagation Functions:** Easy to extend to other domains (thermal, electrical, etc.).
    

----------

## 📖 Research Background

This project is based on the paper summary:  
**"Qualitative Physics Using Dimensional Analysis & π-Calculus"**

Key highlights:

-   **Buckingham-π Theorem**: Identifies governing dimensionless groups.
    
-   **Hall’s Theorem**: Defines physical roles of variables.
    
-   **π-Calculus**: Provides a qualitative reasoning framework for system modeling.
    
-   **Pressure Regulator Example**: Demonstrates inter-ensemble coupling via contact variables.
    

For full details, see the **Paper Summary (DOCX/PDF)**.

----------

## 🔮 Future Enhancements

-   Accept **user input** for spring constant (K) and fluid density (ρ) instead of hard-coded constants.
    
-   Support **arrays/dictionaries** for handling multiple numerator/denominator variables.
    
-   Extend propagation rules to detect contradictions across **core physical variables**.
    
-   Add **simulation loops** for dynamic feedback behavior.
    
-   Generalize to other physical systems (thermal, electrical, mechanical).
    

----------

## 🙏 Acknowledgements

-   Based on research by **R. Bhaskar & Anil Nigam (IBM T.J. Watson Research Center)**
    
-   Special thanks to **Professor Eric Coatanéa** for guidance and references.
    
-   Thanks to peers and collaborators for discussions on qualitative reasoning frameworks.