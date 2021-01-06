from flask import Flask, render_template, request
import instaloader
import matplotlib.pyplot as plt
import matplotlib as mp
import numpy as np

# import os
# os.remove('static/plot1.png') 

L = instaloader.Instaloader()

# f = open('input.txt','r')
# accounts = f.read()
# p = accounts.split('\n')

# PROFILE = p[:]
#print(PROFILE)

def plot(handles,count, **kwargs):
    ylabel = kwargs.pop( 'ylabel' )
    likeability_scores = np.array(count)
    
    data_normalizer = mp.colors.Normalize()
    color_map = mp.colors.LinearSegmentedColormap(
        "my_map",
        {
            "red": [(0, 1.0, 1.0),
                    (1.0, .5, .5)],
            "green": [(0, 0.5, 0.5),
                    (1.0, 0, 0)],
            "blue": [(0, 0.50, 0.5),
                    (1.0, 0, 0)]
            
            
        }
    )

    fig, ax = plt.subplots()
    #plt.bar(usernames,followers_count)
    bars = ax.bar(handles,count,color=color_map(data_normalizer(likeability_scores)))
    plt.xticks(rotation=25, fontname='dejavu sans')

    # Axis formatting.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    # Add text annotations to the top of the bars.
    bar_color = bars[0].get_facecolor()
    for bar in bars:
        ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 14.0,
        round(bar.get_height()),
        horizontalalignment='center',
        color='red'
    )
        
    ax.set_xlabel('Daur Insta handles', labelpad=25, color='#333333', fontsize=12, weight='bold')
    ax.set_ylabel(ylabel, labelpad=25, color='#333333', fontsize=12, weight='bold')
    ax.set_title('Daurs Verticals on Insta', pad=35, color='#333333', fontsize=15,
                weight='bold')

    fig.tight_layout()
    #plt.savefig('static/followers.png')


app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('first.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/compare', methods=['POST'])
def home():
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data4 = request.form['d']
    data5 = request.form['e']
    arr = []
    arr.extend([data1,data2,data3,data4,data5])

    followers_count=[]
    post_count=[]
    for ind in range(len(arr)):
        pro = arr[ind]
        profile = instaloader.Profile.from_username(L.context, pro)
        followers_count.append(profile.followers)
        post_count.append(profile.mediacount)

    plot_conf = {'ylabel': 'Followers_count'}
    plot(arr,followers_count, **plot_conf)
    plt.savefig('static/followers.png')

    plot_conf1 = {'ylabel': 'Posts_count'}
    plot(arr,post_count, **plot_conf1)
    plt.savefig('static/posts.png')

    return render_template('display1.html', name = plt.show())


if __name__ == "__main__":
    app.run(debug=True)