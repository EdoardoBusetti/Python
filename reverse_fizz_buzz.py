def reverse_fizz_buzz(seq):
    """
    Reverse engineer the fizz buzz problem
    
    Parameters:
        seq - list of letter_ocurrenceings
    
    Returns:
        list of possibilities corresponding to each letter present in the sequences (smallest possible possibilities)
        (in alphabetical order)
    
    Example use
    >>> reverse_fizz_buzz(["a", "ab", "c", "a", "ab", "ac"])
    [2, 4, 5]
    >>> reverse_fizz_buzz(["b", "bc", "ab", "bc", "b", "abc", "b"])
    [3, 1, 2]
    >>> reverse_fizz_buzz(["a", "b", "d", "c", "a", "ab"])
    [6, 9, 11, 10]
    """
    
    # Getting the letters in the seq and the order (from lower to higher val)
    s = ""
    for i in seq:
        s+=i
    let_set = set()
    let_list_ordered = []
    for c in s:
        if c in let_set:
            pass
        else:
            let_list_ordered.append(c)
            let_set.add(c)

    
    letter_ocurrence = dict() # Needed to add the letter occurrence of each letter to the decomposing_seq dict
    decomposing_seq = []
    # Make a dict with the occurance of each letter
    # Make a list containing seq decomposed as follows: for each str in seq make a dict with letter_occurrence
    for st in seq :
        decomposing_seq_i = {}
        for ch in st:
            if ch in letter_ocurrence.keys():
                letter_ocurrence[ch] +=1
            else:
                letter_ocurrence[ch] = 1
            decomposing_seq_i[ch] = letter_ocurrence[ch]
        decomposing_seq.append(decomposing_seq_i)


    seq_index = 1
    possibilities = dict()
    for key in decomposing_seq[0].keys() : # initialize the dict with the letters in seq[0] --> First guess
        possibilities[key] = 1
    
    
    # loop until we reach the last str in the sequence
    while seq_index < len(seq) :
        # comparing the fist letter of seq_t an seq_t-1 --> We are using multipliers to know the guessed value corresponding to the letter (e.g. if we saw "a" 3 times and "a" = 2 --> Value = 2*3 = 6)
        letter_t = list(decomposing_seq[seq_index].keys())[0]
        letter_t_minus_1 = list(decomposing_seq[seq_index - 1].keys())[0]
        total_t = possibilities.get(letter_t, 0) * decomposing_seq[seq_index][letter_t] # 0 if the letter is not in possibilities --> We dont yet have a guess for the letter
        total_t_minus_1 = possibilities[letter_t_minus_1] * decomposing_seq[seq_index - 1][letter_t_minus_1]
        if total_t_minus_1 >= total_t :
            # Letter_t guess was wrong, set new value to the letter, start over seq and rerun loop
            t_letter_occurrence = decomposing_seq[seq_index][letter_t]
            """ our best guess for the letter_t is the value of the number at t minus 1 
            divided by the number of occurrences of letter_t, + 1"""
            possibilities[letter_t] = int(total_t_minus_1 / t_letter_occurrence + 1) # set the value of the current letter to the previous value encountered / the number of times the letter occurred
            # restart seq_index to 1
            seq_index = 1
            continue

        # If the totals are right --> i.e. the supposed letters make sense
        all_letters_t = list(decomposing_seq[seq_index].keys())
        reset_seq_index = False
        for i,letter in enumerate(all_letters_t[:len(all_letters_t) - 1]) : # empty if only 1 letter --> Skip block
            for letter_2 in all_letters_t[i + 1:len(all_letters_t)]: 
                total_letter = possibilities.get(letter,0) * decomposing_seq[seq_index][letter]
                total_letter_2 = possibilities.get(letter_2,0) * decomposing_seq[seq_index][letter_2]
                if total_letter == total_letter_2 : # If the two letters amount to the same total --> Guess is coherent, go ahead
                    continue
                elif total_letter < total_letter_2 : # If the total_letter is lower than total_letter_2 --> we are underguessing  "letter"
                    possibilities[letter] = max(int(total_letter_2 / decomposing_seq[seq_index][letter]),possibilities.get(letter,0) + 1) # We have to at least add 1 to the value of the letter. The best guess would be the letter_2 val / num occurences of letter
                    reset_seq_index = True  # since we modified our guess we hve to check that all the values are still coherent
                else :
                    possibilities[letter_2] = max(int(total_letter / decomposing_seq[seq_index][letter_2]),possibilities.get(letter_2,0) + 1)
                    reset_seq_index = True # since we modified our guess we hve to check that all the values are still coherent
        if reset_seq_index ==True:
            seq_index = 1
            continue
        else :
            seq_index += 1
    
    
    alphabet = "abcdefghijklmnopqrstuvwxyz" 
    ret = []
    for i in alphabet:
        if i in possibilities.keys():
            ret.append(possibilities[i])
    return(ret)

print(reverse_fizz_buzz(["a", "ab", "c", "a", "ab", "ac"]))