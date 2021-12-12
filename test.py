import os
import pandas as pd

def pickle_to_csv(pathname, outfile):
    df = pd.read_pickle(pathname)
    df = df.sample(n=1000)
    df = df.drop(columns=['Unnamed: 0', 'channel_id', 'commenter_id', 'commenter_type', 'fragments', 'offset', 'video_id', 'updated_at'], inplace=True, axis=1)
    print("Now converting df to CSV!")
    print(df)
    df.to_csv(outfile)
    print("Finished with " + outfile)

def score_csv(pathname, outfile):
    df = pd.read_csv("finished/xqcow.csv")
    df.drop('Unnamed: 0', inplace=True, axis=1)

    keywords_doc = open("keywords.txt", "r")
    keywords ={}
    for line in keywords_doc:
        line = line.replace("\n","")
        split_line = line.split(",")
        keywords[split_line[0]] = float(split_line[1])
    print(keywords)

    score = 0.0
    scores = []
    for message in df.body:
        message_arr = message.split()
        high_engagement = 0.0
        word_count = 0.0
        for word in message_arr:
            word_count += 1.0
            if word.isupper():
                high_engagement += .5
            if word in keywords:
                high_engagement += keywords[word]
        score = high_engagement / word_count
        if(score > 1.0):
            score = 1.0
        scores.append(score)
        print("This is the message: %s" %(message))
        print("This is word count: " + str(word_count))
        print("This is the number of high_engagement words: " + str(high_engagement))
        print("This is the calculated Score: %f\n" %(score))
    df['scores'] = scores

    df.to_csv("scored/xqcow.csv")

def main():
    outfile = "finished"
    score_dir = "scored"
    
    for filename in os.listdir(outfile):
        filepath = os.path.join(outfile, filename)
        outfile_path = os.path.join(score_dir,filename)
        score_csv(filepath, outfile_path)
    


main()