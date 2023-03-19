import math


class PaginationResponseModel:
    def __init__(self, rows: list):
        self.rows = rows

    def __call__(self):
        return self.rows


class PaginationRequest:
    def __init__(self,
                 rows: list,
                 page: int = 1,
                 per_page: int = 10):
        self.rows = rows
        self.page = page
        self.per_page = per_page


class PaginationInteractor:
    def __init__(self,
                 request: PaginationRequest):
        self.request = request

    def calc_paginate(self):
        rows_len = len(self.request.rows)
        quantity_pages = math.floor(rows_len / self.request.per_page)

        if quantity_pages == 0:
            return self.request.rows

        cut_end = (self.request.page * self.request.per_page)
        cut_initial = (cut_end - self.request.per_page)

        return [cut_initial, cut_end]

    def get_rows_paginated(self):
        [cut_initial, cut_end] = self.calc_paginate()
        return self.request.rows[cut_initial:cut_end]

    def run(self):
        rows = self.get_rows_paginated()
        return PaginationResponseModel(rows)()
