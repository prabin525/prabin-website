import os
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader


# Load Blogs
blogs = {}
for blog_post in os.listdir('content/blogs'):
    file_path = os.path.join('content/blogs/', blog_post)
    with open(file_path, 'r') as file:
        blogs[blog_post] = markdown(file.read(), extras=['metadata'])


# Load Tech Blogs
tech_blogs = {}
for blog_post in os.listdir('content/tech_blogs'):
    file_path = os.path.join('content/tech_blogs/', blog_post)
    with open(file_path, 'r') as file:
        tech_blogs[blog_post] = markdown(file.read(), extras=['metadata'])


# Load Projects
projects = {}
for blog_post in os.listdir('content/projects'):
    file_path = os.path.join('content/projects/', blog_post)
    with open(file_path, 'r') as file:
        projects[blog_post] = markdown(file.read(), extras=['metadata'])


# Create a collection of all posts
all_posts = {**blogs, **tech_blogs, **projects}

# Sort Everything according to date

blogs = {
    post: blogs[post] for post in sorted(
        blogs,
        key=lambda post: datetime.strptime(
            blogs[post].metadata['date'], '%Y-%m-%d'
        ),
        reverse=True
    )
}

tech_blogs = {
    post: tech_blogs[post] for post in sorted(
        tech_blogs,
        key=lambda post: datetime.strptime(
            tech_blogs[post].metadata['date'], '%Y-%m-%d'
        ),
        reverse=True
    )
}

projects = {
    post: projects[post] for post in sorted(
        projects,
        key=lambda post: datetime.strptime(
            projects[post].metadata['date'], '%Y-%m-%d'
        ),
        reverse=True
    )
}

all_posts = {
    post: all_posts[post] for post in sorted(
        all_posts,
        key=lambda post: datetime.strptime(
            all_posts[post].metadata['date'], '%Y-%m-%d'
        ),
        reverse=True
    )
}


# Get first N elements of everything for home
N = 2
blogs_home = dict(list(blogs.items())[0: N])
tech_blogs_home = dict(list(tech_blogs.items())[0: N])
projects_home = dict(list(projects.items())[0: N])
all_posts_home = dict(list(all_posts.items())[0: N])

# Generate Templates

env = Environment(loader=PackageLoader('main', 'templates'))
home_template = env.get_template('home.html')
post_template = env.get_template('post.html')

# Get metadatas and tags for home related

blogs_home_metadata = [blogs_home[post].metadata for post in blogs_home]
blogs_home_tags = [post['tags'] for post in blogs_home_metadata]

tech_blogs_home_metadata = [
    tech_blogs_home[post].metadata for post in tech_blogs_home
    ]
tech_blogs_home_tags = [
    post['tags'] for post in tech_blogs_home_metadata
    ]

projects_home_metadata = [
    projects_home[post].metadata for post in projects_home
    ]
projects_home_tags = [post['tags'] for post in projects_home_metadata]

all_posts_home_metadata = [
    all_posts_home[post].metadata for post in all_posts_home
    ]
all_posts_home_tags = [
    post['tags'] for post in all_posts_home_metadata
    ]

# Render Home Template

home_html = home_template.render(
    all_posts=all_posts_home_metadata,
    all_posts_tags=all_posts_home_tags,
    blogs=blogs_home_metadata,
    blogs_tags=blogs_home_tags,
    tech_blogs=tech_blogs_home_metadata,
    tech_blogs_tags=tech_blogs_home_tags,
    projects=projects_home_metadata,
    projects_tags=projects_home_tags,
)

# Output the home file
with open('docs/index.html', 'w') as file:
    file.write(home_html)


# Render all posts

for post in all_posts:
    post_metadata = all_posts[post].metadata

    post_data = {
        'content': all_posts[post],
        'title': post_metadata['title'],
        'date': post_metadata['date']
    }

    post_html = post_template.render(post=post_data)
    post_file_path = 'docs/{slug}.html'.format(
        slug=post_metadata['slug']
    )

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)
