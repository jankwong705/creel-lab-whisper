import pandas as pd
import numpy as np
import string
from jiwer import wer 

translator = str.maketrans('', '', string.punctuation)

def lookup_actual(lookup_file, query, type='Sentence'):
    df = pd.read_excel(lookup_file)
    result = df.loc[df['lookupval'] == query].iloc[0]
    return result[type].lower().translate(translator)

def lookupval_check(file_name):
    check = "sensical" not in file_name and "senseless" not in file_name and "nonword" not in file_name
    return check

def calculate_wer(results, output_file, mode="default", lookup_file="lookup_file"):
    input_excel = pd.ExcelFile(results)
    match mode:
        case "KT":
            with pd.ExcelWriter(output_file) as writer:
                for sheet in input_excel.sheet_names:
                    # read excel files
                    df = pd.read_excel(results, sheet_name=sheet)
                    df = df.drop(0)                                   # drop the separator row
                    produced = np.array(df['Predicted'].astype(str))  # columns of whisper-produced sentences
                    file_list = np.array(df['File'].astype(str)) 

                    # convert to all lower cases
                    produced = np.array([string.lower() for string in produced])

                    # remove all puncutations
                    produced = np.array([string.translate(translator) for string in produced])
                    expected = np.array([file_name[file_name.rfind('_')+1:file_name.rfind('.')] for file_name in file_list])

                    # compute wer
                    wer_s = np.array([wer(e, p) for e, p in zip(expected, produced)])

                    # add WER to the csv file 
                    df['WER'] = wer_s

                    # output to output_file 
                    df.to_excel(writer, sheet_name=sheet, index=False)
        case "default":
            with pd.ExcelWriter(output_file) as writer:
                for sheet in input_excel.sheet_names:
                    # read excel files 
                    df = pd.read_excel(results, sheet_name=sheet)
                    df = df.drop(0)                                   # drop the separator row
                    expected = np.array(df['Actual'].astype(str))     # columns of actual sentences
                    produced = np.array(df['Predicted'].astype(str))  # columns of whisper-produced sentences

                    # convert to all lower cases
                    expected = np.array([string.lower() for string in expected])
                    produced = np.array([string.lower() for string in produced])

                    # remove all puncutations
                    expected = np.array([string.translate(translator) for string in expected])
                    produced = np.array([string.translate(translator) for string in produced])

                    # compute wer
                    wer_s = np.array([wer(e, p) for e, p in zip(expected, produced)])

                    # add WER to the csv file 
                    df['WER'] = wer_s

                    # output to output_file 
                    df.to_excel(writer, sheet_name=sheet, index=False)
        case "lookup":  
            with pd.ExcelWriter(output_file) as writer:
                # read excel files 
                df = pd.read_excel(results)
                df = df.drop(0)                                   # drop the separator row
                produced = np.array(df['Predicted'].astype(str))  # columns of whisper-produced sentences
                file_list = np.array(df['File'].astype(str))

                # convert to all lower cases
                produced = np.array([string.lower().rstrip() for string in produced])

                # remove all puncutations
                produced = np.array([string.translate(translator) for string in produced])

                # compute wer
                wer_l = []
                expect_l = []
                for p in range(produced.shape[0]):
                    file_name = file_list[p]
                    # check to see if file_name matches format
                    if lookupval_check(file_name):
                        expect_l.append("Query not found!")
                        print("Query not found:", file_name)
                        wer_l.append(-1)                        # -1 will be appended if query not found
                        continue
                    if "WRONG" in file_name:
                        expect_l.append("Query not found!")
                        print("Query not found:", file_name)
                        wer_l.append(-1)
                        continue
                    # extract query from file_name for lookups
                    query = file_name[file_name.index('_') + 1:-4] + file_name[8:file_name.index('_')]
                    word = produced[p]
                    if ' ' in word:
                        word = word[word.rfind(' '):]   # extract last word: remove if want to compare full sentences 
                        expected = lookup_actual(lookup_file, query, type='FinalWord')
                        expect_l.append(expected)
                        wer_s = wer(expected, word)
                        wer_l.append(wer_s)
                    else:
                        expected = lookup_actual(lookup_file, query, type='FinalWord')
                        expect_l.append(expected)
                        wer_s = wer(expected, produced[p])
                        wer_l.append(wer_s)
                        
                # add WER to the csv file 
                df['Actual'] = np.array(expect_l)
                df['WER'] = np.array(wer_l)

                # output to output_file 
                df.to_excel(writer)
    return 

results = input("Input Excel filename:")
output = input("Input output filename:")
mode = input("lookup / default / KT:")
if mode == "lookup":
    lookup_file = input("Lookup filename:")
else:
    lookup_file = "default"
print("Calculating...")
print("This may take a while...")
calculate_wer(results, output, mode=mode, lookup_file=lookup_file)
print("Calculations finished.\nOutput to {}".format(output))
