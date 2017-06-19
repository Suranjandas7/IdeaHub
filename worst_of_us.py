#Worst_of_us

import praw

class work():
    def __init__(self, limit):
        self.title = ''
        self.list_of_comments = []
        self.limit = limit

    def process(self):
        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit("worldnews")
        for s in subreddit.hot(limit=1):
            submission = s
            submission.comment_sort = 'controversial'
            self.title = submission.title
            ider = submission.id
            comments = s.comments

        i=0
        for comment in comments:
            w_o_a = str(comment.body.encode('utf-8'))

            if w_o_a == '[deleted]' or w_o_a == '[removed]':
                continue
            else:
                self.list_of_comments.append(w_o_a)
                i+=1

            if i > self.limit:
                break

    def display(self):
        print '\nTitle of the Post :'
        print '\n' + self.title
        print '\nMost Controversial Comments:'
        for element in self.list_of_comments:
            print '\n--NewComment--\n'
            print str(element)

# sd = work()
# sd.process()
# sd.display()
