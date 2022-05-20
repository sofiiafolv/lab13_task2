# lab13_task2
## demo_bst
### find_in_list
This function finds 10,000 in a list. As random.choice() always generate the same word, I created a list of random words and use loop to find the words and just add them to a list. 10,000 words are found in average in 10 seconds with 65 000 words, and 20 seconds with all words in a document.
### finding_2
Finds a word in BST created from sorted list.
Function works just if BTS consists of 1100 nodes. Program crashes with 1200 words, so I decided to use a rounded number. 10,000 words are found in average in 3.5 seconds.
### finding_3
Finds a word in BST created from list of random words.
I also use 65 000 nodes, and it works in 1 second. It works in 3 or 4 seconds if BST has more than 200,000 nodes.
### finding_4
Finds a word in a balanced tree
The reason that I choose 65 000 nodes, because rebalancing does not work with a bigger amount of words. So I also decreased a number of nodes in previous functions. It works also 1 second, but usually even longer than with a previous function(BST of random words). Also rebalancing doesn't work all the time.
