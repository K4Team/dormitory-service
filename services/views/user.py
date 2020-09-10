from django.db import connection
from django.http import JsonResponse


def getUser(request):
    sql = "SELECT id,name,title,mobile,email,income,create_date FROM sys_user"
    db = connection.cursor()
    db.execute(sql)

    desc = db.description

    data = list([dict(zip([de[0] for de in desc], row))for row in db.fetchall()])


    # dataObject = data.
    return JsonResponse({'data': data})
