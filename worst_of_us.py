import sqlite3
import praw
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class work():
    def __init__(self, limitP, limitC):
        self.title = ''
        self.list_of_comments = []
        self.limitP = limitP
        self.limitC = limitC
        self.post_id = ''
        self.tags = ''

    def make_wordcloud(self, w, h):
        conn = sqlite3.connect('woa.db')
        c = conn.cursor()
        lines = c.execute("SELECT DISTINCT * from Comments")
        all_text = []
        s = ''

        for l in lines:
            all_text.append(l[0].encode('utf-8'))
        for at in all_text:
            s = s+at

        wordcloud = WordCloud(
            width=w,
            height=h,
        ).generate(s)

        c.close()
        conn.close()

        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show()

    def read(self):
        f = open('output.txt', 'w')
        conn = sqlite3.connect('woa.db')
        c = conn.cursor()
        post_dict = {}

        list_of_unique_posts = c.execute(
            "SELECT DISTINCT Title, PostID from Posts"
        )

        for post in list_of_unique_posts:
            post_dict[post[1]] = post[0]

        for key in post_dict:
            current_parent_id = (key,)
            f.write('\n\n[Title : {}]\n\n'.format(post_dict[key].encode('utf-8')))
            list_of_unique_comments = c.execute(
                "SELECT DISTINCT * from Comments WHERE ParentId=?",
                current_parent_id
            )
            for comment in list_of_unique_comments:
                f.write('\n{}'.format(comment[0].encode('utf-8')))
                f.write('\n---END COMMENT---\n')

        f.close()
        c.close()
        conn.close()

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
        counter = 0
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
            counter +=1
            print '[Writing to database]\t {} out of {}'.format(
                str(counter),
                str(self.limitP))
            addtodb(self.title, self.post_id, self.list_of_comments)
            self.title = ''
            self.list_of_comments = []
            self.tags = ''

def main():
    flag = False
    while flag==False:
        choice = str(raw_input('1 - Read\n2 - Catch\n3 - WordCloud\n\nEnter Your Choice : '))
        if choice == '1':
            sd = work(0,0)
            sd.read()
            flag = True
        elif choice == '2':
            sd = work(15,45)
            sd.process()
            flag = True
        elif choice == '3':
            sd = work(0,0)
            sd.make_wordcloud(1920,1080)
            flag = True
        else:
            print 'INVALID OPTION'

if __name__ == '__main__':
    main()
