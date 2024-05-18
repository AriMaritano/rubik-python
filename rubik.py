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

    def rotate_left(self, return_copy=False, n=1):
        grid = self.grid
        for _ in range(n):
            new_grid = [
                grid[2], grid[5], grid[8],
                grid[1], grid[4], grid[7],
                grid[0], grid[3], grid[6],
            ]
            grid = new_grid
        if return_copy:
            return new_grid
        self.grid = new_grid

    def rotate_right(self, return_copy=False, n=1):
        grid = self.grid
        for _ in range(n):
            new_grid = [
                grid[6], grid[3], grid[0],
                grid[7], grid[4], grid[1],
                grid[8], grid[5], grid[2],
            ]
            grid = new_grid
        if return_copy:
            return new_grid
        self.grid = new_grid

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
        for row in self.vertical_grid[1].rows:
            for square in row:
                repr += f' {square} '
            repr += '\n'
        repr += '\n'
        for i in range(3):
            for face in self.horizontal_grid:
                for square in face.rows[i]:
                    repr += f' {square} '
                repr += '   '
            repr += '\n'
        repr += '\n'
        for row in self.vertical_grid[-1].rows:
            for square in row:
                repr += f' {square} '
            repr += '\n'
        return repr

    def shift_row_right(self, row_index, row=None):
        source_orientation = 'left'
        if row_index == 0:
            self.top.rotate_left()
        elif row_index == 2:
            self.bottom.rotate_right()
        new_row = None
        for face in self.horizontal_grid: 
            prev_row = face.rows[row_index]
            if not new_row:
                new_row = getattr(face, source_orientation).rows[row_index]
            for i, square in enumerate(new_row):
                face.grid[i + 3 * row_index] = square	
            new_row = prev_row
        self.vertical_grid[2] = Face(
            color = self.horizontal_grid[2].color,
            grid = self.horizontal_grid[2].rotate_right(True, 2),
        )
    def shift_row_left(self, row_index, row=None):
        source_orientation = 'right'
        if row_index == 0:
            self.top.rotate_right()
        elif row_index == 2:
            self.bottom.rotate_left()
        new_row = None
        for face in self.horizontal_grid[::-1]: 
            prev_row = face.rows[row_index]
            if not new_row:
                new_row = getattr(face, source_orientation).rows[row_index]
            for i, square in enumerate(new_row):
                face.grid[i + 3 * row_index] = square	
            new_row = prev_row
        self.vertical_grid[2] = Face(
            color = self.horizontal_grid[2].color,
            grid = self.horizontal_grid[2].rotate_right(True, 2),
        )

    def shift_col_up(self, col_index, col=None):
        source_orientation = 'down'
        if col_index == 0:
            self.left.rotate_left()
        elif col_index == 2:
            self.right.rotate_right()
        new_col = None
        for face in self.vertical_grid: 
            prev_col = face.cols[col_index]
            if not new_col:
                new_col = getattr(face, source_orientation).cols[col_index]
            for i, square in enumerate(new_col):
                face.grid[i * 3 + col_index] = square	
            new_col = prev_col
        self.horizontal_grid[2] = Face(
            color = self.vertical_grid[2].color,
            grid = self.vertical_grid[2].rotate_right(True, 2),
        )

    def shift_col_down(self, col_index, col=None):
        source_orientation = 'up'
        if col_index == 0:
            self.left.rotate_right()
        elif col_index == 2:
            self.right.rotate_left()
        new_col = None
        for face in self.vertical_grid[::-1]: 
            prev_col = face.cols[col_index]
            if not new_col:
                new_col = getattr(face, source_orientation).cols[col_index]
            for i, square in enumerate(new_col):
                face.grid[i * 3 + col_index] = square	
            new_col = prev_col
        self.horizontal_grid[2] = Face(
            color = self.vertical_grid[2].color,
            grid = self.vertical_grid[2].rotate_right(True, 2),
        )

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

    def shift(self, index, direction, orientation):

        '''
        idea to have a single method to rotate, just tell it up/down/right/left
        (direction=1, orientation=1) => right
        (direction=-1, orientation=1) => left
        (direction=1, orientation=0) => up
        (direction=-1, orientation=0) => down
         
        
        if orientation == 0:
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

c = Cube()
