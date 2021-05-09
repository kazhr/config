=====
todo
=====

todo is a Django app.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "todo" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'todo',
    ]

2. Include the todo URLconf in your project urls.py like this::

    path('todo/', include('todo.urls')),

3. Run ``python manage.py migrate`` to create the todo models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a todo (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/todo/
