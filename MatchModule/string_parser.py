import csv
from nltk.tokenize import word_tokenize
import json
import string


class string_parser(object):
    rows = []
    scores = []
    title = []
    puct_list = []
    f = None

    def __init__(self, word):
        self.path = "new.csv"
        self.search_string = word_tokenize(word)
        self.j = self.open_file()
        self.title = next(self.j)
        self.do_punct()


    def do_punct(self):
        for char in string.punctuation:
            self.puct_list.append(char)

    def open_file(self):
        self.f = open(self.path, "r", encoding='ISO-8859-1', )
        j = csv.reader(self.f, delimiter=',')
        return j

    def tokenize_string(self, word):
        words = word_tokenize(word)
        our_list = []
        new_words = word_tokenize(words)
        for w in new_words:
            if w not in self.puct_list:
                our_list.append(w.lower())
        return w

    def generate_score(self, row):
        score_list = []
        score = 0
        for element in row:
            x = word_tokenize(element)
            for w in x:
                if w not in self.puct_list:
                    score_list.append(w.lower())
        for word in score_list:
            if word in self.search_string:
                score += 1
        return score

    def run_through_rows(self):
        previous = self.title
        line = 1
        for row in self.j:
            line = line + 1
            if row == previous:
                break
            previous = row
            score = self.generate_score(row)
            self.getResults(row, score)
        self.f.close()

    def getResults(self, row, score):
        if len(self.rows) < 5:
            self.add_row(row, score)
            return
        elif score > self.scores[0]:
            self.add_row(row, score)
            return

    def add_row(self, row, score):
        if self.scores == []:
            self.scores.append(score)
            self.rows.append(row)
        for i in range(len(self.rows)):
            if self.scores[i] > score and i == 0 and len(self.rows) < 5:
                self.rows.insert(0, row)
                self.scores.insert(0, score)
                return
            elif self.scores[i] > score and i > 0:
                self.rows[i - 1] = row
                self.scores[i - 1] = score
                return
            if score > self.scores[- 1]:
                if len(self.scores) < 5 and len(self.rows) < 5:
                    self.scores.append(score)
                    self.rows.append(row)
                else:
                    self.scores.pop(0)
                    self.rows.pop(0)
                    self.scores.append(score)
                    self.rows.append(row)

    def ship_values(self, rows, scores):
        val_dict = {}
        rows = reversed(rows)
        scores = reversed(scores)
        x = 1
        val_dict["title"] = self.title
        for i in rows:
            val_dict["row " + str(x)] = i
            x += 1
        return val_dict

    def run(self):
        self.run_through_rows()
        vals = self.ship_values(self.rows, self.scores)
        return vals
