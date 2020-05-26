from flask import Flask, request, render_template, url_for, redirect
from pymongo import MongoClient
from slugify import slugify

cluster = MongoClient(
    'mongodb+srv://mofe_iv:zabimaru64@cluster0-a2dxz.mongodb.net/test?retryWrites=true&w=majority')

db = cluster['portfolio_1stIt']
collection = db['projects']

app = Flask(__name__)


def add_new_project(projectname, project_disc, project_highlight, project_images, link):
    new_project = {'name': projectname,
                   'description': project_disc, 'highlight': project_highlight, 'images': project_images, 'link': link, 'slug': slugify(projectname)}
    collection.insert_one(new_project)


def get_all_projects():
    projects_list = []
    projects = collection.find()
    for project in projects:
        projects_list.append(project)
    return projects_list


def get_single_project(slug):
    project = collection.find_one({'slug': slug})

    return project,


# print(get_single_project('e-tutors-api'))

test_list = get_all_projects()

# print(test_list)


def split_projects(lst, chunk):

    for i in range(0, len(lst), chunk):
        yield lst[i:i + chunk]


split_listof_projects = list(split_projects(test_list, 3))
# print(len(split_listof_projects))
# print(split_listof_projects[:len(split_listof_projects)])


@ app.route('/')
def get_home():
    return render_template('index.html')


@ app.route('/work/<string:slug>')
def get_project(slug):
    # print(slug)
    return render_template('work.html', project=get_single_project(slug))


@ app.route('/works')
def get_works_page():
    get_all_projects()
    return render_template('works.html', projects=split_listof_projects, length=len)


@ app.route('/<string:page>')
def get_page(page):
    return render_template(f'{page}.html')


@ app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        # print(data)
        return 'form submitted'


# add_new_project('E_tutors Api', 'Rest API for an online Tutoring Service', 'Built with NodeJs, ExpressJsand MongoDb', [
#                'https://res.cloudinary.com/duxais9hy/image/upload/v1590526464/Portfolio1stIt_images/Screenshot_85_liikqu.png'], 'https://github.com/mofe64/e_tutors-startng')


# add_new_project('Citadel', 'Online Ebook Library', 'Built with NodeJs, ExpressJsand MongoDb', [
#    'https://res.cloudinary.com/duxais9hy/image/upload/v1590527659/Portfolio1stIt_images/Screenshot_88_xt8gg8.png'], 'https://mylibra.herokuapp.com/')


# results = collection.find()
# print(results)
# results_list = []
# for result in results:
#    results_list.append(result)
# print(results_list)
