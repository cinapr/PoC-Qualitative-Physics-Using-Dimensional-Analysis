# This code implements qualitative reasoning logic
# for a pressure regulator system, according to the given task.
#
# The main objectives of this code are:
# a. Allow the user to specify the state (INCREASE, DECREASE, CONSTANT) for a variable.
# b. Propagate this state to other variables using the Pi relationship.
# c. Detect and report contradictions if any.

# --- 1. Defining qualitative variables ---
# Use strings to represent states, because those are qualitative.
INCREASE = "Increased"
DECREASE = "Decreased"
CONSTANT = "Constant"
UNKNOWN = 'U'


# --- 2. Defining the Model: Variables and the Pi Rule ---
# A dictionary to store the state of each variable.
# The variables 'rho' and 'K' are assumed to be CONSTANT, because machine won't changing spring and fluid in the middle of operation
# Of course in more depth modelling, we should put this as issue to modelling the situation before the machine are built
# But, due to time constraint for this task, I will skip this to decrease the complexity in pi_a1 denominator
variabel_status = {
    'P_in': UNKNOWN,
    'P_out': UNKNOWN,
    'Q': UNKNOWN,
    'A_open': UNKNOWN,
    'rho': CONSTANT,
    'x': UNKNOWN,
    'P': UNKNOWN,
    'K': CONSTANT,
}



#Global variable to record if in 1 of the iteration found CONTRADITION (only cosmetic purpose)
CONTRADICTION_FOUND = False


# --- 3. Assistive Functions for Qualitative Operations ---
#DETERMINING MULTIPLICATION AND DIVISION FOR QUALITATIVE VARIABLES
def determine_product_status(status1, status2):
    """
    Determine multiplication result of 2 qualitative variables.
    (INCREASE * INCREASE) = INCREASE, 
    (DECREASE * DECREASE) = DECREASE, 
    (INCREASE * DECREASE) = UNKNOWN
    """

    # If either variable is UNKNOWN, the result is UNKNOWN.
    if UNKNOWN in (status1, status2):
        return UNKNOWN
    # If either variable is CONSTANT, the result is the other variable.
    elif status1 == CONSTANT:
        return status2
    elif status2 == CONSTANT:
        return status1
    # If both are the same INCREASE, then INCREASE
    elif ((status1 == INCREASE) and (status2 == INCREASE) ):
        return INCREASE
    # If both are the same DECREASE, then DECREASE
    # In this prototype, we always assume both variables are positive. so it is DECREASE.
    # in quantitative calculation, when both DECREASE and the number below 0, it will turn into positive
    # Example: initially A=3, then minus 5. initially B=2, then minus 7. THen the result will be increase instead because (3-5)x(2-7) = (-2)x(-5) = 10
    elif ((status1 == DECREASE) and (status2 == DECREASE) ):
        return DECREASE
    #If contradicting status given, then we can't get the fix result without the quantitative number (To determine it is increase or decrease)
    elif (status1 == INCREASE and status2 == DECREASE) or (status1 == DECREASE and status2 == INCREASE):
        return UNKNOWN
    #Others unexpected conditions
    else:
        return UNKNOWN

def determine_division_status(status_numerator, status_denominator):
    """
    Determine division result of 2 qualitative variables.
    """
    # If either variable is UNKNOWN, the result is UNKNOWN.
    if UNKNOWN in (status_numerator, status_denominator):
        return UNKNOWN
    
    # If the denominator is constant, the result is the numerator's status.
    elif status_denominator == CONSTANT:
        return status_numerator
    
    # If the numerator and denominator have the same status, the result is CONSTANT.
    elif status_numerator == status_denominator:
        return CONSTANT
    
    # If the numerator is constant, the result is the opposite of the denominator.
    elif status_numerator == CONSTANT:
        if status_denominator == DECREASE:
            return INCREASE
        else:  # status_denominator == INCREASE
            return DECREASE
        
    # For all other scenarios, the result is UNKNOWN because the changes are opposite
    # This covers (I/D) and (D/I) - Because we can't determine increase or decrease without number, it was not always constant. Imagine top increase 100, bottom increase 20, it wont give constant.
    else:
        return UNKNOWN
    


# --- 3. Propagation Function for Every regime ---
def propagate_pi_a1(variables):
    """
    Logika untuk Pi_A1 = (Q * rho^1/2) / (A_open * Pin^3/2)
    Asumsi: Pi_A1 dan rho adalah KONSTAN.
    """
    global CONTRADICTION_FOUND
    changes_made = False

    # NUMERATOR
    # (Q * rho^1/2), as rho is constant, it will always depends on Q
    numerator_status = variables['Q']

    # DENOMINATOR
    # (A_open * Pin^3/2) -> As there are 2 qualitative variables, the denominator will come from determine_product_status(AOpen, Pin):
    denominator_status = determine_product_status(variables['A_open'], variables['P_in'])

    # DETERMINE Pi_A1
    # Calculate New Pi_A1
    new_pi_a1_status = determine_division_status(numerator_status, denominator_status)

    # If new_pi_a1_status not UNKNOWN
    if new_pi_a1_status != 'U':
        # if initial status unkwnown then update Pi_A1
        if variables['Pi_A1'] == 'U':
            variables['Pi_A1'] = new_pi_a1_status
            changes_made = True
        # If new_pi_a1_status not same with inputted Pi_A1, then CONTRADICTION
        else:
            #If initial Pi_A1 different than new Pi_A1
            if variables['Pi_A1'] != new_pi_a1_status:
                CONTRADICTION_FOUND = True
                print(f"CONTRADICTION FOUND ON PI_A1: User defined PI_A1 IS '{variables['Pi_A1']}'. It is CONTRADICTED the calculation result '{new_pi_a1_status}'.")
                # In a more complete implementation, note this contradiction (FUTURE ENHANCEMENT)
                return False # Stop propagation
            #else If: initial Pi_A1 same with new Pi_A1, you can just ignore it
    
    # If Pi_A1 is CONSTANT, Numerator and denomitor should be the same
    elif variables['Pi_A1'] == 'C':
        # If denominator is known, the numerator should have same value. As numerator only Q, the Q have same value with Pi_A1
        if denominator_status != 'U' and numerator_status == 'U':
            variables['Q'] = denominator_status
            changes_made = True
        
        elif denominator_status != 'U' and numerator_status == 'U':
            if variables['Q'] == 'U':
                variables['Q'] = denominator_status
                changes_made = True
            elif variables['Q'] != denominator_status:
                CONTRADICTION_FOUND = True
                print(f"CONTRADICTION FOUND: Q is '{variables['Q']}', but propagation says '{denominator_status}'.")
                return False
            
    return changes_made


def propagate_pi_a2(variables):
    """
    Pi_A2 = P_out / P_in.
    """
    global CONTRADICTION_FOUND
    changes_made = False
    
    # Determine Pi_A2 status from Pout and Pin
    new_pi_a2_status = determine_division_status(variables['P_out'], variables['P_in'])
    
    if new_pi_a2_status != 'U':
        # If Pi_A2 UNKNOWN
        if variables['Pi_A2'] == 'U':
            variables['Pi_A2'] = new_pi_a2_status
            changes_made = True
        # If PI_A2 is not UNKNOWN, then CONTRADICTION
        elif variables['Pi_A2'] != new_pi_a2_status:
            CONTRADICTION_FOUND = True
            print(f"CONTRADICTION FOUND IN PI_A2: Initial status '{variables['Pi_A2']}' contradicted with current calculation '{new_pi_a2_status}'.")
            return False # Hentikan propagasi

    # Determine POut or Pin
    if variables['Pi_A2'] != 'U' and variables['P_out'] != 'U':
        new_pin_status = determine_division_status(variables['P_out'], variables['Pi_A2'])
        if new_pin_status != 'U':
            if variables['P_in'] == 'U':
                variables['P_in'] = new_pin_status
                changes_made = True
            elif variables['P_in'] != new_pin_status:
                CONTRADICTION_FOUND = True
                print(f"CONTRADICTION FOUND: P_in is '{variables['P_in']}', but propagation says '{new_pin_status}'.")
                return False

    elif variables['Pi_A2'] != 'U' and variables['P_in'] != 'U':
        new_pout_status = determine_product_status(variables['Pi_A2'], variables['P_in'])
        if new_pout_status != 'U':
            if variables['P_out'] == 'U':
                variables['P_out'] = new_pout_status
                changes_made = True
            elif variables['P_out'] != new_pout_status:
                CONTRADICTION_FOUND = True
                print(f"CONTRADICTION FOUND: P_out is '{variables['P_out']}', but propagation says '{new_pout_status}'.")
                return False

            
    return changes_made


def propagate_pi_b1(variables):
    """
    Pi_B1 = (x * P) / K
    Assumption: K is CONSTANT.
    """
    global CONTRADICTION_FOUND
    changes_made = False

    # Determine Pi_B1
    # Pi_B1 = is came from multiplication of x and P, divided with K (Constant)
    new_pi_b1_status = determine_product_status(variables['x'], variables['P'])
    # As K assumed as constant, the propagate will only look the result of x.P, because anything divide by CONSTANT is same result with its numerator
    
    if new_pi_b1_status != 'U':
        # IF initially no Pi_B1, we can just replaced it
        if variables['Pi_B1'] == 'U':
            variables['Pi_B1'] = new_pi_b1_status
            changes_made = True
        elif variables['Pi_B1'] != new_pi_b1_status:
            CONTRADICTION_FOUND = True
            print(f"CONTRADICTION FOUND IN PI_B1: The initial state of '{variables['Pi_B1']}' contradicts the calculated result of '{new_pi_b1_status}'.")
            return False

    if variables['Pi_B1'] != 'U':
        if variables['x'] == 'U' and variables['P'] != 'U':
            new_x_status = determine_division_status(variables['Pi_B1'], variables['P'])
            if new_x_status != 'U':
                if variables['x'] == 'U':
                    variables['x'] = new_x_status
                    changes_made = True
                elif variables['x'] != new_x_status:
                    CONTRADICTION_FOUND = True
                    print(f"CONTRADICTION FOUND: x is '{variables['x']}', but propagation says '{new_x_status}'.")
                    return False

        elif variables['P'] == 'U' and variables['x'] != 'U':
            new_p_status = determine_division_status(variables['Pi_B1'], variables['x'])
            if new_p_status != 'U':
                if variables['P'] == 'U':
                    variables['P'] = new_p_status
                    changes_made = True
                elif variables['P'] != new_p_status:
                    CONTRADICTION_FOUND = True
                    print(f"CONTRADICTION FOUND: P is '{variables['P']}', but propagation says '{new_p_status}'.")
                    return False


    return changes_made


def propagate_pi_c1(variables):
    """
    Pi_C1 = P / Pout.
    """
    global CONTRADICTION_FOUND
    changes_made = False

    # Determine Pi_C1
    new_pi_c1_status = determine_division_status(variables['P'], variables['P_out'])

    if new_pi_c1_status != 'U':
        if variables['Pi_C1'] == 'U':
            variables['Pi_C1'] = new_pi_c1_status
            changes_made = True
        elif variables['Pi_C1'] != new_pi_c1_status:
            CONTRADICTION_FOUND = True
            print(f"CONTRADICTION FOUND IN PI_C1: The initial state of '{variables['Pi_C1']}' contradicts the calculated result of '{new_pi_c1_status}'.")
            return False

    if variables['Pi_C1'] != 'U':
        if variables['P_out'] == 'U' and variables['P'] != 'U':
            new_pout_status = determine_division_status(variables['P'], variables['Pi_C1'])
            if new_pout_status != 'U':
                if variables['P_out'] == 'U':
                    variables['P_out'] = new_pout_status
                    changes_made = True
                elif variables['P_out'] != new_pout_status:
                    CONTRADICTION_FOUND = True
                    print(f"CONTRADICTION FOUND: P_out is '{variables['P_out']}', but propagation says '{new_pout_status}'.")
                    return False

        elif variables['P'] == 'U' and variables['P_out'] != 'U':
            new_p_status = determine_product_status(variables['Pi_C1'], variables['P_out'])
            if new_p_status != 'U':
                if variables['P'] == 'U':
                    variables['P'] = new_p_status
                    changes_made = True
                elif variables['P'] != new_p_status:
                    CONTRADICTION_FOUND = True
                    print(f"CONTRADICTION FOUND: P is '{variables['P']}', but propagation says '{new_p_status}'.")
                    return False

    return changes_made


def propagate_pi_c2(variables):
    """
    Pi_C2 = x / A_open.
    """
    global CONTRADICTION_FOUND
    changes_made = False

    # Determine Pi_C2
    new_pi_c2_status = determine_division_status(variables['x'], variables['A_open'])

    if new_pi_c2_status != 'U':
        if variables['Pi_C2'] == 'U':
            variables['Pi_C2'] = new_pi_c2_status
            changes_made = True
        elif variables['Pi_C2'] != new_pi_c2_status:
            CONTRADICTION_FOUND = True
            print(f"CONTRADICTION FOUND IN PI_C2: The initial state of '{variables['Pi_C2']}' contradicts the calculated result of '{new_pi_c2_status}'.")
            return False

    # return propagation to determine AOpen or x
    if variables['Pi_C2'] != 'U':
        if variables['A_open'] == 'U' and variables['x'] != 'U':
            new_a_open_status = determine_division_status(variables['x'], variables['Pi_C2'])
            if new_a_open_status != 'U':
                if variables['A_open'] == 'U':
                    variables['A_open'] = new_a_open_status
                    changes_made = True
                elif variables['A_open'] != new_a_open_status:
                    CONTRADICTION_FOUND = True
                    print(f"CONTRADICTION FOUND: A_open is '{variables['A_open']}', but propagation says '{new_a_open_status}'.")
                    return False

        elif variables['x'] == 'U' and variables['A_open'] != 'U':
            new_x_status = determine_product_status(variables['Pi_C2'], variables['A_open'])
            if new_x_status != 'U':
                if variables['x'] == 'U':
                    variables['x'] = new_x_status
                    changes_made = True
                elif variables['x'] != new_x_status:
                    CONTRADICTION_FOUND = True
                    print(f"CONTRADICTION FOUND: x is '{variables['x']}', but propagation says '{new_x_status}'.")
                    return False


    return changes_made







# --- 4. Wrapper Function for Each Ensemble ---
def propagate_ensemble_a(variables):
    """
    #Ensemble Pi_A1 and Pi_A2 into ensemble_A
    """
    changes_made = False
    if propagate_pi_a1(variables): 
        changes_made = True
    if propagate_pi_a2(variables): 
        changes_made = True
    return changes_made



def propagate_ensemble_b(variables):
    """
    #Ensemble Pi_B1 into ensemble B
    But, as ENsemble_B only have 1 regime, the result always the same.
    """
    
    #changes_made = False
    #if propagate_pi_b1(variables):  # Pi_B1 Propagation
    #    changes_made = True
    #return changes_made

    return propagate_pi_b1(variables)



def merge_contact_variable_pi_c1_pi_c2 (variables):
    """
    # Merge the Pi_C1 and Pi_C2 just as to make it easier to be called. 
    # In actual, these should be separated as these 2 are contact variables of inter-ensemble components, not an ensemble
    """
    changes_made = False
    if propagate_pi_c1(variables): changes_made = True
    if propagate_pi_c2(variables): changes_made = True
    return changes_made





# --- 5. Main part of algorithm. Propagate all rules ---
def solve_pressure_regulator(initial_variables):
    global CONTRADICTION_FOUND
    CONTRADICTION_FOUND = False

    variables = initial_variables.copy()
    changes_made = True
    iteration = 0

    print("--- INITIAL STATUS ---")
    print(variables)
    print("-" * 20)

    while changes_made:
        changes_made = False
        iteration += 1
        print(f"Iteration {iteration}:")

        # Call propagation iteration
        changes_made = propagate_ensemble_a(variables) or changes_made
        changes_made = merge_contact_variable_pi_c1_pi_c2(variables) or changes_made
        changes_made = propagate_ensemble_b(variables) or changes_made
        
        print(variables)

    print("\n--- END STATUS ---")

    # If a contradiction is found in the middle of iterations, the algorithm will not stop immediately.
    # It will just get a flag, that at least one of the variables face CONTRADICTION
    # It continues running other propagations until the system reaches stability,
    # then exits the loop. 
    # Finally, the contradiction flag is checked here.
    # Future Enhancement :
    # 1. Able to log which iteration make which contradition
    # 2. Now we mostly only cover the contradiction on Pi-* variables, 
    # other variables only covered when it is so clear like INCREASE against DECREASE in some variable.
    # if variable changes due to propagation and contradict, only Pi-variables are showing the warning
    # Introduce enhanced propagation rules so the system can check contradictions not only on Pi-* variables, 
    # but also on the core physical variables (e.g.Pin,Pout,Q,Aopen,x, P). 
    if CONTRADICTION_FOUND:
        print(">>> CONTRADICTION FOUND <<<")
    else:
        print(">>> NO CONTRADICTION FOUND <<<")

    print("Last Variables Stage:")
    print(variables)
    

# --- 6. Example ---
# Main function to run the simulation with user-selectable options.
def main():
    print("Select the scenario you want to run:")
    print("1. Scenario 1: P_out constant, P_in increasing")
    print("2. Scenario 2: P_in constant, P_out decreasing")
    print("3. Scenario 3: P_in increasing, P_out increasing")
    print("4. Scenario 4: P_in increasing, P_out is not determined")
    print("5. Scenario 5: P_in constant, P_out increasing")
    print("6. Manual Input")

    choice = input("Make your choice (1/2/3/4/5/6): ")
    
    if choice == '1':
        initial_state = {
            'P_in': INCREASE,
            'P_out': CONSTANT,
            'Q': UNKNOWN,
            'A_open': UNKNOWN,
            'x': UNKNOWN,
            'P': UNKNOWN,
            'Pi_A1': CONSTANT,
            'Pi_A2': UNKNOWN,
            'Pi_B1': UNKNOWN,
            'Pi_C1': UNKNOWN,
            'Pi_C2': UNKNOWN,
        }
        solve_pressure_regulator(initial_state)
    
    elif choice == '2':
        initial_state = {
            'P_in': CONSTANT,
            'P_out': DECREASE,
            'Q': UNKNOWN,
            'A_open': UNKNOWN,
            'x': UNKNOWN,
            'P': UNKNOWN,
            'Pi_A1': CONSTANT,
            'Pi_A2': UNKNOWN,
            'Pi_B1': UNKNOWN,
            'Pi_C1': UNKNOWN,
            'Pi_C2': UNKNOWN,
        }
        solve_pressure_regulator(initial_state)

    elif choice == '3':
        initial_state = {
            'P_in': INCREASE,
            'P_out': INCREASE,
            'Q': UNKNOWN,
            'A_open': UNKNOWN,
            'x': UNKNOWN,
            'P': UNKNOWN,
            'Pi_A1': CONSTANT,
            'Pi_A2': UNKNOWN,
            'Pi_B1': UNKNOWN,
            'Pi_C1': UNKNOWN,
            'Pi_C2': UNKNOWN,
        }
        solve_pressure_regulator(initial_state)

    elif choice == '4':
        initial_state = {
            'P_in': INCREASE,
            'P_out': UNKNOWN,
            'Q': CONSTANT,
            'A_open': INCREASE,
            'x': UNKNOWN,
            'P': UNKNOWN,
            'Pi_A1': UNKNOWN,
            'Pi_A2': UNKNOWN,
            'Pi_B1': UNKNOWN,
            'Pi_C1': UNKNOWN,
            'Pi_C2': UNKNOWN,
        }
        solve_pressure_regulator(initial_state)

    elif choice == '5':
        initial_state = {
            'P_in': CONSTANT,
            'P_out': INCREASE,
            'Q': UNKNOWN,
            'A_open': UNKNOWN,
            'x': UNKNOWN,
            'P': UNKNOWN,
            'Pi_A1': UNKNOWN,
            'Pi_A2': UNKNOWN,
            'Pi_B1': UNKNOWN,
            'Pi_C1': UNKNOWN,
            'Pi_C2': UNKNOWN,
        }
        solve_pressure_regulator(initial_state)

    elif choice == '6':
        status_mapping = {
            'I': INCREASE,
            'D': DECREASE,
            'C': CONSTANT,
            'U': UNKNOWN,
        }
        initial_state = {
            'P_in': UNKNOWN,
            'P_out': UNKNOWN,
            'Q': UNKNOWN,
            'A_open': UNKNOWN,
            'x': UNKNOWN,
            'P': UNKNOWN,
            'Pi_A1': CONSTANT,
            'Pi_A2': UNKNOWN,
            'Pi_B1': UNKNOWN,
            'Pi_C1': UNKNOWN,
            'Pi_C2': UNKNOWN,
        }
        core_variables = ['P_in', 'P_out', 'Q', 'A_open', 'x', 'P']
        print("Enter the status for the following variables (I, D, C, U)")
        
        for var_to_set in core_variables:
            status = input(f"Status of {var_to_set}: ").strip().upper()
            if status in status_mapping:
                initial_state[var_to_set] = status_mapping[status]
            elif status == '':
                initial_state[var_to_set] = UNKNOWN
            else:
                print(f"WARNING: Input '{status}' invalid. Status {var_to_set} set to '{UNKNOWN}'.")
                
        solve_pressure_regulator(initial_state)
            
    else:
        print("Invalid option")


# Run the main function when the script is executed.
if __name__ == "__main__":
    main()
