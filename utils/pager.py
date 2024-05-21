import copy
from django.utils.safestring import mark_safe


class PagerHtmlModel:

    def __init__(self, request, queryset, per_page_row):
        # queryset row count
        total_row = queryset.count()
        # total page count
        total_page, plus = divmod(total_row, per_page_row)
        if plus:
            total_page += 1
        self.total_page = total_page

        self.query_dict = copy.deepcopy(request.GET)
        # current page
        page = self.query_dict.get('page')
        if page and page.isnumeric() and 0 < int(page) <= self.total_page:
            self.page = int(page)
        else:
            self.page = 1
        # row count in each page
        self.per_page_row = per_page_row

        # queryset within pagination range
        start = (self.page - 1) * self.per_page_row
        end = self.page * self.per_page_row + 1
        self.queryset = queryset[start:end]

    @property
    def page_html_string(self):
        self.query_dict._mutable = True
        # 首页
        self.query_dict.setlist('page', [1])
        html_list = ["""<li class="page-item"><a class="page-link" href="?{}" aria-label="First">
                        <span aria-hidden="true">首页</span></a></li>""".format(self.query_dict.urlencode()),]
        # 上一页
        self.query_dict.setlist('page', [self.page - 1 if self.page > 1 else 1])
        html_list.append("""<li class="page-item"><a class="page-link" href="?{}" aria-label="Previous">
                            <span aria-hidden="true">上一页</span></a></li>""".format(self.query_dict.urlencode()))
        # 下一页
        self.query_dict.setlist('page', [self.page + 1 if self.page < self.total_page else self.total_page])
        html_list.append("""<li class="page-item"><a class="page-link" href="?{}" aria-label="Next">
                            <span aria-hidden="true">下一页</span></a></li>""".format(self.query_dict.urlencode()))
        # 尾页
        self.query_dict.setlist('page', [self.total_page])
        html_list.append("""<li class="page-item"><a class="page-link" href="?{}" aria-label="End">
                            <span aria-hidden="true">尾页</span></a></li>""".format(self.query_dict.urlencode()))

        start_page = self.page - 5 if self.page > 5 else 1
        end_page = self.page + 5 if self.page + 5 <= self.total_page else self.total_page
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist('page', [i])
            if i == self.page:
                # active current page
                item = """<li class="page-item"><a class="page-link active" href="?{}">{}</a></li>
                        """.format(self.query_dict.urlencode(), i)
            else:
                item = """<li class="page-item"><a class="page-link" href="?{}">{}</a></li>
                        """.format(self.query_dict.urlencode(), i)
            html_list.insert(-2, item)

        return mark_safe("".join(html_list))