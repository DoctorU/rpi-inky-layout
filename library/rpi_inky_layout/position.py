class Position:

    @staticmethod
    def average(_tuple):
        return (_tuple[0] - _tuple[1])/2

    @staticmethod
    def middle_centre(box_wh, object_wh):
        sizes = zip(box_wh, object_wh)
        return tuple([Position.average(size) for size in sizes])

    @staticmethod
    def middle_left(box_wh, object_wh):
        box_h = box_wh[1]
        object_h = object_wh[1]
        return (0, Position.average((box_h, object_h)))

    @staticmethod
    def middle_right(box_wh, object_wh):
        box_w, box_h = box_wh
        object_w, object_h = object_wh
        return (box_w - object_w, Position.average((box_h, object_h)))

    @staticmethod
    def top_left(box_wh, object_wh):
        return (0, 0)

    @staticmethod
    def top_centre(box_wh, object_wh):
        box_w = box_wh[0]
        object_w = object_wh[0]
        return (Position.average((box_w, object_w)), 0)

    @staticmethod
    def top_right(box_wh, object_wh):
        box_w, box_h = box_wh
        object_w, object_h = object_wh
        return (box_h - object_h, 0)

    @staticmethod
    def bottom_left(box_wh, object_wh):
        box_h = box_wh[1]
        object_h = object_wh[1]
        return (0, box_h - object_h)

    @staticmethod
    def bottom_centre(box_wh, object_wh):
        box_w, box_h = box_wh
        object_w, object_h = object_wh
        return (Position.average((box_w, object_w)), box_h - object_h)

    @staticmethod
    def bottom_right(box_wh, object_wh):
        b_w, b_h = box_wh
        o_w, o_h = object_wh
        return (b_w - o_w, b_h - o_h)
