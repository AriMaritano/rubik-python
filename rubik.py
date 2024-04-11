class Face:
    def __init__(self, color, grid=[]):
        self.color = color
        self.grid = grid or self.create_grid()
    def create_grid(self):
        c = self.color[0] # first letter of color
        return [f'{c}{i}' for i in range(1, 10)]
    @property
    def cols(self):
        return [
            [self.grid[0], self.grid[3], self.grid[6]],
            [self.grid[1], self.grid[4], self.grid[7]],
            [self.grid[2], self.grid[5], self.grid[8]],
        ]
    @property
    def rows(self):
        return [
            [self.grid[0], self.grid[1], self.grid[2]],
            [self.grid[3], self.grid[4], self.grid[5]],
            [self.grid[6], self.grid[7], self.grid[8]],
        ]

    def rotate_left(self, return_=False, n=1):
        grid = self.grid
        for _ in range(n):
            new_grid = [
                grid[2], grid[5], grid[8],
                grid[1], grid[4], grid[7],
                grid[0], grid[3], grid[6],
            ]
            grid = new_grid
        if return_:
            return new_grid
        self.grid = new_grid

    def rotate_right(self, return_=False, n=1):
        grid = self.grid
        for _ in range(n):
            new_grid = [
                grid[6], grid[3], grid[0],
                grid[7], grid[4], grid[1],
                grid[8], grid[5], grid[2],
            ]
            grid = new_grid
        if return_:
            return new_grid

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
        self.front = Face('Blue')
        self.right = Face('Red')
        self.back = Face('Green')
        self.left = Face('Yellow')
        self.top = Face('White')
        self.bottom = Face('Orange')
        self.create_horizontal_grid()
        self.create_vertical_grid()


    def create_horizontal_grid(self):
        self.horizontal_grid = [
            self.front,
            self.right,
            self.back,
            self.left,
        ]
        
        self.front.right = self.right
        self.right.right = self.back
        self.back.right = self.left
        self.left.right = self.front
        
        self.front.left = self.left
        self.right.left = self.front
        self.back.left = self.right
        self.left.left = self.back

    def create_vertical_grid(self):
        self.vertical_grid = [
            self.front,
            self.top,
            Face(self.back.color, self.back.rotate_right(True, 2)), # rotated 180
            self.bottom,
        ]

        self.front.up = self.top
        self.top.up = self.vertical_grid[2]
        self.vertical_grid[2].up = self.bottom
        self.bottom.up = self.front
        
        self.front.down = self.bottom
        self.top.down = self.front
        self.vertical_grid[2].down = self.top
        self.bottom.down = self.vertical_grid[2]
        
    @property
    def faces(self):
        return [
            self.front,    
            self.right,    
            self.back,    
            self.left,    
        ]
    def __repr__(self):
        repr = ''
        for row in self.top.rows:
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
            for square in row:
                repr += f' {square} '
            repr += '\n'
        return repr

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
            self.back = self.vertical_grid[3].rotate() still need to see direction

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
            face.rows[row_index] = (
                rows or next_face.rows[row_index]
            )
            
            rows = prev_row
    def shift_row_left(self, row_index, row=None):
        orientation = 'right'
        if row_index == 0:
            self.top.rotate_right()
        elif row_index == 2:
            self.bottom.rotate_left()
        rows = None
        for face in self.faces[::-1]: 
            prev_row = face.rows[row_index]
            next_face = getattr(face, orientation)
            face.rows[row_index] = (
                rows or next_face.rows[row_index]
            )
            
            rows = prev_row

    def shift_col_up(self, col_index):
        orientation = 'down'
        if col_index == 0:
            self.left.rotate_left()
        elif col_index == 2:
            self.right.rotate_right()
        col = None
        for face in self.vertical_grid: 
            prev_col = face.cols[col_index]
            next_face = getattr(face, orientation)
            '''
            change this:
            instead of having rows and cols in init, we'l
            have just an array of 9 values.
            values = ['1','2','3','4','5','6','7','8','9']
            rows will just be:
            rows = [
               [values[0], values[1], values[2]],
               [values[3], values[4], values[5]],
               [values[6], values[7], values[8]],
            ]
            cols = [
               [values[0], values[3], values[6]],
               [values[1], values[4], values[7]],
               [values[2], values[5], values[8]],
            ]

            '''
            face.rows = (
                col or next_face.cols[col_index]
            )
            col = prev_col
            
        self.back = Face(
            self.back.color,
            self.vertical_grid[2].get_rotate_right(2)
        )

    def shift_col_down(self):
        orientation = 'up'
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
    def show(self):
        repr = ''
        for face in self.vertical_grid[1:][::-1]:
            for row in face.rows:
                for square in row:
                    repr += f' {square} '
                repr += '  '
                repr += '\n'
            repr += '\n'
        for i in range(3):
            for face in self.horizontal_grid:
                for square in face.rows[i]:
                    repr += f' {square} '
                repr += '   '
            repr += '\n'
        print(repr)


c = Cube()
