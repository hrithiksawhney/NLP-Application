# NLP-Application
<p align="center">
<b>Messaging Application with Next Word Prediction, Word Completion, Spelling Correction and Automatic Priority Assignment</b>
  </p>

### Next Word Prediction:

Next Word Prediction or what is also called Language Modeling is the task of predicting what word comes next. It is one of the fundamental tasks of NLP and has many applications. The app provides suggestions for words in the sentence using an N-gram Language Model to make the typing process more fast and easy.

<p align="center">
  <img src="https://user-images.githubusercontent.com/44416769/86110322-102dc900-bae3-11ea-9f4c-d21f5518a286.png">
</p>

### Word Completion:

Autocomplete, or word completion, is a feature in which an application predicts the rest of a word a user is typing. The app provides this feature by implementing DFS traversal on a trie data stucture.

<p align="center">
  <img src="https://user-images.githubusercontent.com/44416769/86111437-5e8f9780-bae4-11ea-958d-a70c30632e49.png">
</p>

### Spelling Check:

A spell checker is a software feature that checks for misspellings in a text. Spell-checking features are often embedded in software or services, such as a word processor, email client, electronic dictionary, or search engine. The app identifies misspelt words and offers alternatives using the trie data structure.

<p align="center">
  <img src="https://user-images.githubusercontent.com/44416769/86111645-a1ea0600-bae4-11ea-983b-655b5af5f754.png">
</p>

### Priority Emails:

Emails flow into the inbox and remain for eternity until we delete them or go out of storage. It is a toilsome work to find significant mails among these piled up emails. This complication is now resolved using the "word prediction and prioritization" which prioritizes the incoming mails based on the average priority of all the words present in an email. On your outlook message tab, a high prioritized mail would be shown with a red-colored exclamatory mark and a low prioritized mail with a down arrow symbol. Thus, this distinguishes various emails based on their priority and also allows users to be beware of spam mails.

Besides, it provides a user-friendly interface that suggests complete sentences in your emails so that you can draft them with ease. It helps save you time by cutting back on repetitive writing while reducing the chance of spelling and grammatical errors. It can even suggest relevant contextual phrases.

### Working :

1. Initially, A file named Chilkat main.py is run so as to start the process.

2. Second, nlp.py file is run to set up the environment. This opens up the main interface that contains a header to send the mail with subject to respective users and a message area where the actual message to be sent is typed.

3. 'Complete button' is used for word prediction that suggests a complete word to the letter typed.

4. 'Next button' is used for the next word prediction that suggests the word that is likely to come after the word typed.

5. 'Correction button' displays the corrections to be done if any present.

6. 'Send button' is used to send the mail to the addressed user with priority attached. This priority is shown with a red-colored exclamatory mark for a higher value and a down arrow symbol for low priority ones. High or low priority is based on the values obtained from the range 1-5. Number 1 or number 2 indicates high priority in emails whereas Number 4 or Number 5 indicates low priority in emails. Number 3 indicates neutrality in prioritization.

7. When a person clicks on a received email, an alert that indicates the priority of that particular email is poped up as a notice.

### Video Demo:
[![Alt text](https://user-images.githubusercontent.com/44416769/86146678-2903a200-bb16-11ea-89f4-fe1f54458081.png)](https://www.youtube.com/watch?v=ExurprktAm8)
