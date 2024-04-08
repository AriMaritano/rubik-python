class Face:
    def __init__(self, color):
        self.color = color
        self.rows = self.create_rows()
    def create_rows(self):
        c = self.color[0]
        return [
            [f"{c}1", f"{c}2", f"{c}3",],
            [f"{c}4", f"{c}5", f"{c}6",],
            [f"{c}7", f"{c}8", f"{c}9",],
        ]
    @property
    def cols(self):
        return [
            [self.rows[0][0], self.rows[1][0], self.rows[2][0]],
            [self.rows[0][1], self.rows[1][1], self.rows[2][1]],
            [self.rows[0][2], self.rows[1][2], self.rows[2][2]],
        ]
    def rotate_left(self):
        rows = self.rows
        self.rows = [
            [rows[0][2], rows[1][2], rows[2][2]],
            [rows[0][1], rows[1][1], rows[2][1]],
            [rows[0][0], rows[1][0], rows[2][0]],
        ]
    def rotate_right(self):
        rows = self.rows
        self.rows = [
            [rows[2][0], rows[1][0], rows[0][0]],
            [rows[2][1], rows[1][1], rows[0][1]],
            [rows[2][2], rows[1][2], rows[0][2]],
        ]
    def __repr__(self):
        return f"{self.color} face"
    def show(self):
        repr = ''
        for row in self.rows:
            for square in row:
                repr += f' {square} '
            repr += '\n'
        print(repr)

class Cube:
    def __init__(self, faces=None):
        if not faces:
            self.create_cube()
    def create_cube(self):
        self.face_1 = Face('Blue')
        self.face_2 = Face('Red')
        self.face_3 = Face('Green')
        self.face_4 = Face('Yellow')
        self.top = Face('White')
        self.bottom = Face('Orange')

        self.face_1.right = self.face_2
        self.face_2.right = self.face_3
        self.face_3.right = self.face_4
        self.face_4.right = self.face_1
        
        self.face_1.left = self.face_4
        self.face_2.left = self.face_1
        self.face_3.left = self.face_2
        self.face_4.left = self.face_3
    @property
    def faces(self):
        return [
            self.face_1,    
            self.face_2,    
            self.face_3,    
            self.face_4,    
        ]
    def __repr__(self):
        repr = ''
        for row in self.top.rows:
            repr += ' '*12 + '   '
            for square in row:
                repr += f' {square} '
            repr += '\n'
        repr += '\n'
        for i in range(3):
            for face in self.faces:
                for square in face.rows[i]:
                    repr += f' {square} '
                repr += '   '
            repr += '\n'
        repr += '\n'
        for row in self.bottom.rows:
            repr += ' '*12 + '   '
            for square in row:
                repr += f' {square} '
            repr += '\n'
        return repr
    '''
    representation of the cube will be horizontal grid (4 left-right linked faces)
    and vertical grid (4 up-down linked face), where the front and back 
    faces are included in both grids. Back face will be rotated 180º in the vertical grid.
    
    shift_row right and left should be just one
    function, just use positive and negative direction

    shift_row alters the horizontal grid.
    After each row shift, we need to update the rotated back face in the vertical grid 
    
    shift_col alters the vertical grid.
    After each col shift, we need to update the back face in the horizontal grid 

    probably shift is just one method that takes orientation as argument to know
    whether to shift_row or shift_col

    '''
    def shift(self, index, direction, orientation):

        '''
        if orientation == 'v':
            if index == 0:
                rotate left face direction %4 or sth like that
            if index == 2:
                rotate right face direction %4 or sth like that
            col = None
            for face in self.vertical_grid: 
                prev_col = face.rows[row_index]
                target = (
                    col or getattr(face, up? down?).rows[
                    [0][index],
                    [1][index],
                    [2][index],
                )
                face.rows[0][index], face.rows[1][index], face.rows[2][index] = target
                col = prev_col
            # after updating columns, update back face in horizontal grid
            self.face_3 = self.vertical_grid[3].rotate() still need to see direction

        '''
        ...
    def shift_row(self, index, direction):
        self.shift(index, direction, 'h')
    def shift_col(self, index, direction):
        self.shift(index, direction, 'v')
    def shift_row_right(self, row_index, row=None):
        orientation = 'left'
        if row_index == 0:
            self.top.rotate_left()
        elif row_index == 2:
            self.bottom.rotate_right()
        rows = None
        for face in self.faces: 
            prev_row = face.rows[row_index]
            next_face = getattr(face, orientation)
            target_rows = (
                rows or next_face.rows[row_index]
            )
            
            face.rows[row_index] = target_rows
            rows = prev_row
    def shift_row_left(self, row_index, row=None):
        orientation = 'right'
        if row_index == 0:
            self.top.rotate_right()
        elif row_index == 2:
            self.bottom.rotate_left()
        rows = None
        for face in self.faces: 
            prev_row = face.rows[row_index]
            face.rows[row_index] = (
                rows or getattr(face, orientation).rows[row_index]
            )
            rows = prev_row

    def shift_col_up(self):
        orientation = 'top'
        if row_index == 0:
            self.left.rotate_left()
        elif row_index == 2:
            self.bottom.rotate_right()
        rows = None
        for face in self.faces: 
            prev_row = face.rows[row_index]
            next_face = getattr(face, orientation)
            target_rows = (
                rows or next_face.rows[row_index]
            )
            
        ...

    def shift_col_down(self):
        orientation = 'bottom'
        if row_index == 0:
            self.top.rotate_left()
        elif row_index == 2:
            self.bottom.rotate_right()
        rows = None
        for face in self.faces: 
            prev_row = face.rows[row_index]
            next_face = getattr(face, orientation)
            target_rows = (
                rows or next_face.rows[row_index]
            )
            
        ...

