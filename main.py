import os
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader


# Remove all the files in docs folder

filelist = [f for f in os.listdir("docs/")]
NON_DELETE_FILES_FOLDER = [
    "CNAME",
    "css",
    "img",
    "js",
    "lib"
]
for f in filelist:
    if f in NON_DELETE_FILES_FOLDER:
        pass
    else:
        os.remove(os.path.join("docs/", f))


# Load Blogs
blogs = {}
for blog_post in os.listdir('content/blogs'):
    file_path = os.path.join('content/blogs/', blog_post)
    with open(file_path, 'r') as file:
        blogs[blog_post] = markdown(file.read(), extras=['metadata'])


# Load Projects
projects = {}
for blog_post in os.listdir('content/projects'):
    file_path = os.path.join('content/projects/', blog_post)
    with open(file_path, 'r') as file:
        projects[blog_post] = markdown(file.read(), extras=['metadata'])


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


projects = {
    post: projects[post] for post in sorted(
        projects,
        key=lambda post: datetime.strptime(
            projects[post].metadata['date'], '%Y-%m-%d'
        ),
        reverse=True
    )
}


# Get first N elements of everything for home
N = 5
blogs_home = dict(list(blogs.items())[0: N])
projects_home = dict(list(projects.items())[0: N])


# Generate Templates
env = Environment(loader=PackageLoader('main', 'templates'))
home_template = env.get_template('home.html')
blog_template = env.get_template('blog.html')
project_template = env.get_template('projects.html')
post_template = env.get_template('post.html')
post_project_template = env.get_template('post_project.html')
cv_template = env.get_template('cv.html')

# Get metadatas and tags for home related

blogs_home_metadata = [blogs_home[post].metadata for post in blogs_home]
blogs_home_tags = [post['tags'] for post in blogs_home_metadata]
projects_home_metadata = [
    projects_home[post].metadata for post in projects_home
    ]
projects_home_tags = [post['tags'] for post in projects_home_metadata]


# Render Home Template

home_html = home_template.render(
    blogs=blogs_home_metadata,
    blogs_tags=blogs_home_tags,
    projects=projects_home_metadata,
    projects_tags=projects_home_tags,
)

with open('docs/index.html', 'w') as file:
    file.write(home_html)


# Render Project Listing Template

projects_metadata = [projects[post].metadata for post in projects]
projects_tags = [post['tags'] for post in projects_metadata]
project_html = project_template.render(
    projects=projects_metadata,
    projects_tags=projects_tags,
)

with open('docs/projects.html', 'w') as file:
    file.write(project_html)


# Render Blog Listing Template

blogs_metadata = [blogs[post].metadata for post in blogs]
blogs_tags = [post['tags'] for post in blogs_metadata]
blog_html = blog_template.render(
    blogs=blogs_metadata,
    blogs_tags=blogs_tags,
)

with open('docs/blog.html', 'w') as file:
    file.write(blog_html)


# CV page

cv_html = cv_template.render()
with open('docs/cv.html', 'w') as file:
    file.write(cv_html)

# Render all posts

for post in blogs:
    post_metadata = blogs[post].metadata

    post_data = {
        'content': blogs[post],
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


# Render all Projects

for post in projects:
    post_metadata = projects[post].metadata

    post_data = {
        'content': projects[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
        'thumbnail': post_metadata['thumbnail']
    }

    post_html = post_project_template.render(post=post_data)
    post_file_path = 'docs/{slug}.html'.format(
        slug=post_metadata['slug']
    )

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)
