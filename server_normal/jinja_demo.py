from jinja2 import Environment, FileSystemLoader
import os.path
import time


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)

template = env.get_template('jinja_demo.html')

ns = list(range(3))
us = [
    {
        'id': 1,
        'name': 'one',
    },
    {
        'id': 2,
        'name': 'two',
    },
]

class A(object):
    def __init__(self):
        self.id = 1
        self.time = time.time()

    def foo(self):
        return 'Time to show!'

a = A()
print(template.render(name='kiwi', numbers=ns, users=us, a=a))


"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>jinja demo</title>
</head>
<body>
    <!--变量替换-->
    <h1>kiwi</h1>
    <h1>1</h1>
    <h1>1519703733.142705</h1>
    <h1>Time to show!</h1>

    <!--循环-->
    
        <span class="number">0</span>
    
        <span class="number">1</span>
    
        <span class="number">2</span>
    

    <!--循环加对象/字典访问-->
    <div class="user-container">
        
            <div class="user-cell">
                <span>one</span>
                <span>1</span>
            </div>
        
            <div class="user-cell">
                <span>two</span>
                <span>2</span>
            </div>
        
    </div>
</body>
</html>
"""
