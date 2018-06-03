from flask import Blueprint,jsonify,request
from flask.views import MethodView
import redis

pages = Blueprint('pages', __name__)
pages_list = Blueprint('pages_list', __name__)

class Pages(MethodView):

    def get(self,page_id):
	r = redis.StrictRedis()
        page = r.hgetall('hy_blog:pages:%s'%page_id)
        return jsonify(page)

    def delete(self,page_id):
        r = redis.StrictRedis()
        if r.delete('hy_blog:pages:%s'%page_id):
            r.lrem('hy_blog:pages:pages_id_list',1,page_id)
            return r"{'status':'True'}"
        else:
            return r"{'status':'Error'}"


    def put(self):
        r = redis.StrictRedis()
        r.lpush('hy_blog:pages:pages_id_list',request.json['data']['title'])
        r.hmset('hy_blog:pages:%d'%num,request.json['data'])
        return r"{'status':'True'}"


class PagesList(MethodView):
    def get(self,list_id):
        r = redis.StrictRedis()
        num = llen('hy_blog:pages:pages_id_list')
        max = 0
        if num % 6:
            max = 1 + num / 6
        else:
            max = num / 6
        if list_id > max:
            return '{"message":"不存在该列表","status":"error","data":"null"}'
        else:
            page_list = r.lrange('hy_blog:pages:pages_id_list',(list_id - 1) * 6, list_id * 6 -1)
            return jsonify({"message":"成功获取文章列表","status":"success","data":page_list})




pages_view = Pages.as_view('pages_api')
pages_list_view = Pageslist.as_view('pages_list_api')

pages.add_url_rule('/pages/<str:pages>' , methods = ['GET', 'DELETE'] , view_func = pages_view)
pages.add_url_rule('/pages/' , methods = ['PUT'] , view_func = pages_view)
pages_list.add_url_rule('/pages_list/<int:list_id>',methods = ['GET'] , view_func = pages_list_view)
