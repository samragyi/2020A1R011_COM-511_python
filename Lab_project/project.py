import os
# pip install sciket-learn
import shutil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tkinter import Tk     
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an Open dialog box and return the path to the selected file
#print(filename)


codefolder =  "C:\\Users\\samra\\Documents\\plag check\\"
shutil.copy(filename, codefolder)
student_files = [doc for doc in os.listdir() if doc.endswith('.txt')]
student_notes = [open(_file, encoding='utf-8').read()
                 for _file in student_files]


def vectorize(Text): return TfidfVectorizer().fit_transform(Text).toarray()
def similarity(doc1, doc2): return cosine_similarity([doc1, doc2])


vectors = vectorize(student_notes)
s_vectors = list(zip(student_files, vectors))
plagiarism_results = set()


def check_plagiarism():
    global s_vectors
    overall  = 0.0
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            Sim = similarity(text_vector_a, text_vector_b)[0][1]
            sim_score = Sim*100
            overall = overall + sim_score
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score)
            plagiarism_results.add(score)
        print("For Text File = ",student_pair[0],"&",student_pair[1])
        print("Plagiarism in Two Files is = ",sim_score, "%")
    return plagiarism_results


for data in check_plagiarism():
    print()

messagebox.showinfo("Plagarism", "Plagarism Check Complete!")
