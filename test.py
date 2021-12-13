import os
import string
import pandas as pd

def pickle_to_csv(pathname, outfile):
    df = pd.read_pickle(pathname)
    df = df.sample(n=1000)
    df.drop(columns=['channel_id', 'commenter_id', 'commenter_type', 'fragments', 'offset', 'video_id', 'updated_at'], inplace=True, axis=1)
    print("Now converting df to CSV!")
    base = os.path.splitext(outfile)[0]
    outfile = base + ".csv"
    outfile.replace(".pkl", ".csv")
    print(outfile)
    print(df)
    df.to_csv(outfile)
    print("Finished with " + outfile)

def score_csv(pathname, outfile):
    df = pd.read_csv(pathname)
    print(df)
    df.drop('Unnamed: 0', inplace=True, axis=1)
    df.dropna(inplace=True)

    keywords_doc = open("keywords.txt", "r")
    keywords ={}
    for line in keywords_doc:
        line = line.replace("\n","").lower()
        split_line = line.split(",")
        keywords[split_line[0]] = float(split_line[1])
    print(keywords)

    score = 0.0
    scores = []
    for message in df.body:
        print(message)
        message_arr = message.split()
        high_engagement = 0.0
        word_count = 0.0
        for word in message_arr:
            word_count += 1.0
            if word.isupper():
                high_engagement += .5
            if word.lower() in keywords:
                if word.isupper():
                    high_engagement += .5
                high_engagement += keywords[word.lower()]
            for letter in word:
                if letter == "?" or letter =="!":
                    high_engagement += 1.0
        score = high_engagement / word_count
        if(score > 1.0):
            score = 1.0
        scores.append(score)
        print("This is the message: %s" %(message))
        print("This is word count: " + str(word_count))
        print("This is the number of high_engagement words: " + str(high_engagement))
        print("This is the calculated Score: %f\n" %(score))
    df['scores'] = scores

    df.to_csv(outfile)

def main():
    data_dir = "data"
    outfile = "finished"
    score_dir = "scored"
    for filename in os.listdir(data_dir):
        print(filename)
        filepath = os.path.join(data_dir, filename)
        outpath = os.path.join(outfile, filename)
        pickle_to_csv(filepath, outpath)

    for filename in os.listdir(outfile):
        filepath = os.path.join(outfile, filename)
        outfile_path = os.path.join(score_dir,filename)
        score_csv(filepath, outfile_path)
    
main()