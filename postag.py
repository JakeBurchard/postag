import sys
from math import log
def accuracy(data, test):
    num_items = len(data)
    correct = 0
    for p in data:
        if str(p) == str(test[data.index(p)]):
            correct += 1
    return float(correct)/num_items
               
#Takes a list of lists as an argument
def print_results(data):
    for l in data:
        print l[0] + " " + l[1]
    

def hmm(train, test):
    tag_set = ['<s>','C','D','E','F','G','I','J','L','M','N','P','R','T','U','V','X','Y','Z']
    vocab_size = len(train)
    poses = {}
    pos_a_b = {}
    pos_and_word = {}
    for i in range(len(train) -1):
        #pos frequency dict
        if train[i][0] not in poses:
            poses[train[i][0]] = 1
        else:
            poses[train[i][0]] += 1
        
        #pos bigram frequency dict
        if i != len(train)-1:
            if (train[i][0], train[i+1][0]) not in pos_a_b:
                pos_a_b[(train[i][0], train[i+1][0])] = 1
            else:
                pos_a_b[(train[i][0], train[i+1][0])] += 1

        #word and pos frequency dict    
        if tuple(train[i]) not in pos_and_word:
            pos_and_word[tuple(train[i])] = 1
        else:
            pos_and_word[tuple(train[i])] += 1
            
        
    #vocab size and pos dict
    diff_words = {}
    for pos in tag_set:
        freq = []
        for item in train:
            if item[0] == pos and item[1] not in freq:
                freq.append(item[1])
        diff_words[pos] = len(freq)

        
    def get_emission_prob():
        e_probs = {}
        for item in train:
            if tuple(item) not in e_probs:
                e_probs[tuple(item)] = float(.000001 + pos_and_word[tuple(item)])/(.000001 * diff_words[item[0]] + poses[item[0]])
                
        #add remaining items to dict with smoothed 0 probabilities
        for pos in tag_set:
            for item in train:
                if (pos, item[1]) not in e_probs:
                    e_probs[(pos, item[1])] = float(.000001)/(.000001 * diff_words[pos] + poses[pos])
            
            #add an entry for every pos/unknown word combination
            e_probs[(pos, '!!@@##$$')] = float(.000001)/(.000001 * diff_words[pos] + poses[pos])
        return e_probs
            
    def get_transition_prob():
        t_probs = {}
        for item in pos_a_b:
            if item not in t_probs:
                t_probs[item] = float(.000001 + pos_a_b[item])/(.000001 * len(poses) + poses[item[1]])
        
        #add remaining items to dict with smoothed 0 probabilities        
        for pos_a in tag_set:
            for pos_b in tag_set:
                if (pos_a, pos_b) not in t_probs:
                    t_probs[(pos_a, pos_b)] = float(.000001)/(.000001 * len(poses) + poses[pos_a])
        return t_probs
          
    
    e_probs = get_emission_prob()
    t_probs = get_transition_prob()
    
    
    final = []
    
    #viterbi calculations
    for i in range(len(test) - 1):
        current_word = test[i][1]
        temp_probs = {}
        for pos in tag_set:
            if (pos, current_word) in e_probs:
                emission = e_probs[(pos, current_word)]
            else:
                #assign probabilities to unknown words
                emission = e_probs[(pos, '!!@@##$$')]
                
            if current_word == "<s>":
                transition = 1
                prev_prob = 1
            else:
                prev_pos = final[i-1][0]
                transition = t_probs[(prev_pos, pos)]
                prev_prob = final[i-1][2]
            temp_probs[pos] = emission * transition * prev_prob
        #find the highest probability
        final_prob = max(temp_probs.values())
        final_pos = ''
        
        #find the pos with the highest probability
        for pos in temp_probs.keys():
            if temp_probs[pos] == final_prob:
                final_pos = pos
                break
        final.append([final_pos, current_word, final_prob])
        
    #remove the extra probability value in each sub-list
    for i in range(len(final) -1):
        final[i].pop()
        
    print_results(final)
        
    

        
def baseline(train, test):
    test_list = []
    train_dict = {}

    def most_common(lst):
        return max(set(lst), key=lst.count)
        
    for word in train:
        if word[1] in train_dict:
            train_dict[word[1]].append(word[0])
        else:
            train_dict[word[1]] = [word[0]]
            
    #pick the most common pos for the word
    for word, pos_list in train_dict.iteritems():
        train_dict[word] = most_common(pos_list)
       
    for word in test:
        if train_dict.has_key(word[1]):
            test_list.append([train_dict[word[1]], word[1]])

        else:
            test_list.append(['N', word[1]])

    print_results(test_list)
        
    
if __name__ == "__main__":
    train = []
    test = []
    train_data = open(sys.argv[2], 'r').read().splitlines()
    test_data = open(sys.argv[3], 'r').read().splitlines()
    
    for line in train_data:
        d = line.split()
        train.append(d)
    for line in test_data:
        d = line.split()
        test.append(d)
    if sys.argv[1] == "baseline":
        baseline(train, test)
    elif sys.argv[1] == "hmm":
        hmm(train, test)