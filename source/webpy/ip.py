from flask import Blueprint, render_template, request
from myclass import mydb

ip_info = Blueprint('ip_info', __name__)
@ip_info.route("/ip", methods=["GET", "POST"])
def display_database():
    order_by = request.args.get('order_by')
    is_desc = request.args.get('is_desc')
    limit = request.args.get('limit')
    fuzz_filter = request.args.get('fuzz_filter')
    the_filter = request.args.get('the_filter')

    x=mydb()
    # res=x.query_sqlite("select * from ip_info")
    res=x.query_sqlite_with_parameter("select * from url",order_by=order_by,limit=limit,is_desc=is_desc)
    content=res["result"]
    labels=res["field_names"]
    # {"result":result, "field_names":field_names}
        # args={
        #     "order_by":None,
        #     "is_desc":None,
        #     "limit":None,
        #     "fuzz_filter":None,
        #     "the_filter":None
        #     }


    return render_template('info.html', content=content, labels=labels)



