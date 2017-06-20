import sqlite3
import praw

class work():
    def __init__(self, limitP, limitC):
        self.title = ''
        self.list_of_comments = []
        self.limitP = limitP
        self.limitC = limitC
        self.post_id = ''
        self.tags = ''

    def create_database(self):
        conn = sqlite3.connect('woa.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE Posts
            (Title text, PostId text)'''
        )
        c.execute('''CREATE TABLE Comments
            (Content text, ParentId text, CommentId text)'''
        )
        conn.commit()
        c.close()
        conn.close()

    def process(self):
        def display(title, list_of_comments, postid):
            print '\nTitle of the Post :'
            print str(title).encode('utf-8')
            print '\nPost ID:'
            print str(postid).encode('utf-8')
            print '\nMost Controversial Comments:'
            for element in list_of_comments:
                raw_input('\nPress enter for next comment...')
                print '\n'
                print str(element[0]).encode('utf-8')
            print '\n\nWait for next post...'

        def addtodb(post_title, post_id, list_of_comments):
            conn = sqlite3.connect('woa.db')
            c = conn.cursor()

            post_insert = (
                post_title,
                post_id,
            )
            c.execute("INSERT INTO Posts VALUES (?,?)", post_insert)

            for comment in list_of_comments:
                comment_insert = (
                    comment[0],
                    post_id,
                    comment[1],
                )
                c.execute("INSERT INTO comments VALUES (?,?,?)", comment_insert)

            conn.commit()
            c.close()
            conn.close()

        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit("worldnews")
        for s in subreddit.hot(limit=self.limitP):
            submission = s
            submission.comment_sort = 'controversial'
            self.title = submission.title
            self.post_id = submission.id
            comments = s.comments

            i=0
            for comment in comments:
                w_o_a = comment.body
                comment_id = comment.id

                if w_o_a == '[deleted]' or w_o_a == '[removed]':
                    continue
                else:
                    output = [w_o_a, comment_id]
                    self.list_of_comments.append(output)
                    i+=1

                if i == self.limitC:
                    break
            #display(self.title, self.list_of_comments, self.post_id)
            addtodb(self.title, self.post_id, self.list_of_comments)
            self.title = ''
            self.list_of_comments = []
            self.tags = ''

sd = work(15,45)
sd.process()
