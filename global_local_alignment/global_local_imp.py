'''
Created on Oct 13, 2014

@author: Abanoub Milad Nassief
'''

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
  Takes as input a set of characters alphabet 
  and three scores diag_score, off_diag_score,
  and dash_score. The function returns a dictionary
  of dictionaries whose entries are indexed by pairs 
  of characters in alphabet plus '-'. The score for 
  any entry indexed by one or more dashes is dash_score.
  The score for the remaining diagonal entries is diag_score. 
  Finally, the score for the remaining off-diagonal entries is off_diag_score
    """
    alphabet.add('-')
    scoring_matri = {}
    for first_ltr in alphabet:
        temp = {}
        for sec_ltr in alphabet:
            if first_ltr == sec_ltr and first_ltr != '-':
                temp[sec_ltr] = diag_score
            elif first_ltr == '-' or sec_ltr == '-':
                temp[sec_ltr] = dash_score
            else:
                temp[sec_ltr] = off_diag_score
        scoring_matri[first_ltr] = temp
    return scoring_matri

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y
    whose elements share a common alphabet with
    the scoring matrix scoring_matrix. The function
    computes and returns the alignment matrix for 
    seq_x and seq_y as described in the Homework.
    If global_flag is True, each entry of the alignment
    matrix is computed using the method described in Question 8 of the Homework.
    If global_flag is False, each entry is computed 
    using the method described in Question 12 of the Homework.
    """
    rows = len(seq_x) + 1
    cols = len(seq_y) + 1
    s_matrix = [[_ for _ in range(cols)] for _ in range(rows)]

    s_matrix[0][0] = 0     
        
    if global_flag:         
        for row in range(1, rows):
            s_matrix[row][0] = s_matrix[row - 1][0] + scoring_matrix[seq_x[row - 1]]['-']
        for col in range(1, cols):
            s_matrix[0][col] = s_matrix[0][col - 1] + scoring_matrix['-'][seq_y[col - 1]]
        
        for row in range(1, rows):
            for col in range(1, cols):
                s_matrix[row][col] = max(s_matrix[row - 1][col - 1]
                 + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]],
                 
                max(s_matrix[row - 1][col]
                + scoring_matrix[seq_x[row - 1]]['-'],
                                       
                s_matrix[row][col - 1]
                + scoring_matrix['-'][seq_y[col - 1]]))    
    else:     
        for row in range(1, rows):
            s_matrix[row][0] = max(0, s_matrix[row - 1][0] + 
                                    scoring_matrix[seq_x[row - 1]]['-'])
        for col in range(1, cols):
            s_matrix[0][col] = max(0, s_matrix[0][col - 1] + 
                                    scoring_matrix['-'][seq_y[col - 1]])
                   
        for row in range(1, rows):
            for col in range(1, cols):
                s_matrix[row][col] = max(s_matrix[row - 1][col - 1]
                 + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]],
                 
                max(s_matrix[row - 1][col]
                + scoring_matrix[seq_x[row - 1]]['-'],
                                       
                s_matrix[row][col - 1]
                + scoring_matrix['-'][seq_y[col - 1]]))
                
                if s_matrix[row][col] < 0:
                    s_matrix[row][col] = 0
                
    return s_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    implement the method ComputeAlignment discussed in Question 9 of the Homework.
    Takes as input two sequences seq_x and seq_y whose elements 
    share a common alphabet with the scoring matrix scoring_matrix.
    This function computes a global alignment of seq_x and seq_y using
    the global alignment matrix alignment_matrix.
    The function returns a tuple of the form (score, align_x, align_y)
    where score is the score of the global alignment align_x and align_y.
    Note that align_x and align_y should have the same length and may
    include the padding character '-'.
    
    """
    rows = len(seq_x)
    cols = len(seq_y)
    par_x = ''
    par_y = ''
    score = 0
    
    while rows != 0 and cols != 0:
        if alignment_matrix[rows][cols] == \
        alignment_matrix[rows - 1][cols - 1] + \
        scoring_matrix[seq_x[rows - 1]][seq_y[cols - 1]]:
                                       
            par_x = seq_x[rows - 1] + par_x
            par_y = seq_y[cols - 1] + par_y
            score += scoring_matrix[seq_x[rows - 1]][seq_y[cols - 1]]
            rows -= 1
            cols -= 1
  
        else:
            if alignment_matrix[rows][cols] == \
                alignment_matrix[rows - 1][cols] + \
                scoring_matrix[seq_x[rows - 1]]['-']:
                                               
                par_x = seq_x[rows - 1] + par_x
                par_y = '-' + par_y
                score += scoring_matrix[seq_x[rows - 1]]['-']
                rows -= 1
            else:
                par_x = '-' + par_x
                par_y = seq_y[cols - 1] + par_y
                score += scoring_matrix['-'][seq_y[cols - 1]]
                cols -= 1
    
    while rows != 0:
            par_x = seq_x[rows - 1] + par_x
            par_y = '-' + par_y
            score += scoring_matrix[seq_x[rows - 1]]['-']
            rows -= 1
    while cols != 0:
            par_x = '-' + par_x
            par_y = seq_y[cols - 1] + par_y
            score += scoring_matrix['-'][seq_y[cols - 1]]
            cols -= 1
    return (score, par_x, par_y)
        
def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    This second function will compute an optimal local alignment 
    starting at the maximum entry of the local alignment matrix 
    and working backwards to zero as described in Question 13 
    of the Homework.
    
     Takes as input two sequences seq_x and seq_y whose elements 
     share a common alphabet with the scoring matrix scoring_matrix.
     This function computes a local alignment of seq_x and seq_y using
     the local alignment matrix alignment_matrix.
     The function returns a tuple of the form (score, align_x, align_y)
     where score is the score of the optimal local alignment align_x and
     align_y. Note that align_x and align_y should have the same length
     and may include the padding character '-'.
    
    """
    max_val = float("-inf")
    max_tuple = (0, 0)
    for row in range(len(seq_x) + 1):
        for col in range(len(seq_y) + 1):
            if alignment_matrix[row][col] > max_val:
                max_val = alignment_matrix[row][col]
                max_tuple = (row, col)
    par_x = ''
    par_y = ''
    score = 0
    rows = max_tuple[0]
    cols = max_tuple[1]

    while rows != 0 and cols != 0 and alignment_matrix[rows][cols] != 0:
        if alignment_matrix[rows][cols] == \
        alignment_matrix[rows - 1][cols - 1] + \
        scoring_matrix[seq_x[rows - 1]][seq_y[cols - 1]]:
                                       
            par_x = seq_x[rows - 1] + par_x
            par_y = seq_y[cols - 1] + par_y
            score += scoring_matrix[seq_x[rows - 1]][seq_y[cols - 1]]
            rows -= 1
            cols -= 1
  
        else:
            if alignment_matrix[rows][cols] == \
                alignment_matrix[rows - 1][cols] + \
                scoring_matrix[seq_x[rows - 1]]['-']:
                                               
                par_x = seq_x[rows - 1] + par_x
                par_y = '-' + par_y
                score += scoring_matrix[seq_x[rows - 1]]['-']
                rows -= 1
            else:
                par_x = '-' + par_x
                par_y = seq_y[cols - 1] + par_y
                score += scoring_matrix['-'][seq_y[cols - 1]]
                cols -= 1
    return (score, par_x, par_y)


# m1=build_scoring_matrix(set(['A','C','T','G']), 10, 4, -6)
# m2=compute_alignment_matrix('AA', 'TAAT', m1, False)
# print(compute_local_alignment('AA', 'TAAT', m1, m2))

