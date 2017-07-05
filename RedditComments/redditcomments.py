import sqlite3
import praw
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import configparser

class work():
    def __init__(self, limitP, limitC, database_name, r_name, c_type):
        self.title = ''
        self.list_of_comments = []
        self.limitP = limitP
        self.limitC = limitC
        self.post_id = ''
        self.tags = ''
        self.database_name = str(database_name)
        self.r_name = str(r_name)
        self.c_type = str(c_type)

    def data_count(self):
        def control(mode):
            def shortcut(data):
                container = []
                for lines in data:
                    container.append(lines)
                return len(container)

            conn = sqlite3.connect(self.database_name)
            c = conn.cursor()
            data = c.execute("SELECT DISTINCT * from {}".format(mode))
            count = shortcut(data)
            c.close()
            conn.close()
            return count

        no_of_comments = control('Comments')
        no_of_posts = control('Posts')

        print 'No of Posts - {}\nNo of comments - {}'.format(
                                                        no_of_posts,
                                                        no_of_comments)

    def make_wordcloud(self, w, h):
        conn = sqlite3.connect(self.database_name)
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
        conn = sqlite3.connect(self.database_name)
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
        conn = sqlite3.connect(str(self.database_name)+'.db')
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
        def addtodb(post_title, post_id, list_of_comments):
            conn = sqlite3.connect(self.database_name)
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
        subreddit = reddit.subreddit(self.r_name)
        counter = 0
        for s in subreddit.hot(limit=self.limitP):
            submission = s
            submission.comment_sort = self.c_type
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
    reader = configparser.ConfigParser()
    reader.read('config.ini')
    flag = False
    while flag==False:
        choice = str(raw_input('''
            1 - Read
            2 - Catch
            3 - WordCloud
            4 - DataCount
            5 - Create Database


            'Exit' - Exit

            Enter Your Choice :
            '''))
        if choice == '1':
            name_of_db = str(raw_input('Enter name of db : '))
            sd = work(0,0, name_of_db, 'NA', 'NA')
            sd.read()
        elif choice == '2':
            name_of_db = str(raw_input('Enter name of db : '))
            subreddit_name = reader.get(name_of_db, 'subreddit')
            comment_type = reader.get(name_of_db, 'comments')
            sd = work(15,45, name_of_db, subreddit_name, comment_type)
            sd.process()
        elif choice == '3':
            name_of_db = str(raw_input('Enter name of db : '))
            sd = work(0,0, name_of_db, 'NA', 'NA')
            sd.make_wordcloud(1920,1080)
        elif choice == '4':
            name_of_db = str(raw_input('Enter name of db : '))
            sd = work(0,0, name_of_db, 'NA', 'NA')
            sd.data_count()
        elif choice == '5':
            name_of_db = str(raw_input('Enter name of database: '))
            sd = work(0,0,name_of_db, 'NA', 'NA')
            sd.create_database()
        elif choice == 'Exit':
            flag = True
        else:
            print 'INVALID OPTIOEN'

if __name__ == '__main__':
    main()
