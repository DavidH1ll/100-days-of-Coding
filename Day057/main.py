from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# Sample blog post data
blog_posts = [
    {
        'id': 1,
        'title': 'The Life of Cactus',
        'subtitle': 'Who knew that cacti lived such interesting lives.',
        'author': 'Angela Yu',
        'date': 'May 5, 2024',
        'body': '''
        <p>Nori grape silver beet broccoli kombu beet greens fava bean potato quandong celery. 
        Bunya nuts black-eyed pea prairie turnip leek lentil turnip greens parsnip. Sea lettuce 
        lettuce water chestnut eggplant winter purslane fennel azuki bean earthnut pea sierra leone 
        bologi leek soko chicory celtuce parsley jícama salsify.</p>
        
        <p>Celery quandong swiss chard chicory earthnut pea potato. Salsify taro catsear garlic gram 
        celery bitterleaf wattle seed collard greens nori. Grape wattle seed kombu beetroot horseradish 
        carrot squash brussels sprout chard.</p>
        
        <p>Pea horseradish azuki bean lettuce avocado asparagus okra. Kohlrabi radish okra azuki bean 
        corn fava bean mustard tigernut jícama green bean celtuce collard greens avocado quandong fennel 
        gumbo black-eyed pea. Grape silver beet watercress potato tigernut corn groundnut.</p>
        '''
    },
    {
        'id': 2,
        'title': 'Top 15 Things to Do When You Are Bored',
        'subtitle': 'Are you bored? Don\'t know what to do? Try these top 15 activities.',
        'author': 'Jack Bauer',
        'date': 'June 12, 2024',
        'body': '''
        <p>Veggies es bonus vobis, proinde vos postulo essum magis kohlrabi welsh onion daikon amaranth 
        tatsoi tomatillo melon azuki bean garlic.</p>
        
        <p>Gumbo beet greens corn soko endive gumbo gourd. Parsley shallot courgette tatsoi pea sprouts 
        fava bean collard greens dandelion okra wakame tomato. Dandelion cucumber earthnut pea peanut 
        soko zucchini.</p>
        
        <p>Turnip greens yarrow ricebean rutabaga endive cauliflower sea lettuce kohlrabi amaranth water 
        spinach avocado daikon napa cabbage asparagus winter purslane kale. Celery potato scallion desert 
        raisin horseradish spinach carrot soko.</p>
        '''
    },
    {
        'id': 3,
        'title': 'Introduction to Jinja',
        'subtitle': 'Learn about the Jinja templating engine.',
        'author': 'Emily Rodriguez',
        'date': 'July 20, 2024',
        'body': '''
        <p>Jinja is a modern and designer-friendly templating language for Python, modelled after Django's 
        templates. It is fast, widely used and secure with the optional sandboxed template execution environment.</p>
        
        <p>Features include template inheritance, automatic HTML escaping to prevent XSS attacks, sandboxed 
        execution, and extensive filter support. Jinja templates are just text files that contain variables 
        and/or expressions, which get replaced with values when a template is rendered.</p>
        
        <p>The syntax is very intuitive and makes it easy to write templates that are both powerful and easy 
        to maintain. With Jinja, you can create reusable components and avoid repetitive HTML code across your 
        web application.</p>
        '''
    }
]


@app.route('/')
def home():
    """Render the homepage with all blog posts"""
    return render_template('index.html', posts=blog_posts, current_year=datetime.now().year)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Render a specific blog post"""
    # Find the post with the matching id
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    
    if post:
        return render_template('post.html', post=post, current_year=datetime.now().year)
    else:
        return "Post not found", 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
