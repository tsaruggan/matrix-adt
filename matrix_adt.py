## @file matrix-adt.py
#  @title Matrix ADT
#  @brief An abstract data type for matrices.
#  @author Saruggan Thiruchelvan
#  @date January 17, 2021

import random

## @brief This class represents a matrix.
#  @details This class represents a matrix object with a 2D array containing the float values stored in the matrix
#  and two integer values representing the number of rows and the number of columns
class Matrix:

    ## @brief Constructor for Matrix
    #  @details Constructor creates a matrix of zeros and accepts two parameters for the number of rows and the number of columns (ex. Matrix(2,3)).
    #  @param rows integer for number of rows
    #  @param cols integer for number of cols
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._matrix = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(0.0)
            self._matrix.append(row)

    ## @brief Informal string representation of Matrix
    #  @details Used for printing the matrix in a readable form with even spacing (ex. print(matrix))
    #  @return String of matrix values in an organized table.
    def __str__(self):
        output = ""
        mag = max(len(str(round(self.max_val(),2))) , len(str(round(self.min_val(),2))))
        for i in range(self.rows()):
            for j in range(self.cols()):
                num = self._matrix[i][j]
                num_len = len(str(abs(num)))
                diff = mag - num_len - (num < 0)
                num_str = "-" * (num < 0) + "0" * diff + str(round(abs(num),2))
                output += num_str
                if (j <= self.cols() - 1):
                    output += "  "
            if (i != self.rows() - 1):
                output += "\n"
        return output

    ## @brief Equivalnce comparison of Matrix objects
    #  @details Used for comparing if two matrix objects are equivalent (ex. matrix1 == matrix2).
    #  @param other Matrix object to compare if equal with.
    #  @return Returns True if both Matrix objects are equivalent.
    def __eq__(self, other):
        if (not self.is_same_size(other)):
            return False
        else:
            for i in range(self.rows()):
                for j in range(self.cols()):
                    if (self.get_val(i,j) != other.get_val(i,j)):
                        return False
            return True

    ## @brief Get the number of rows in the matrix.
    #  @return integer for the number of rows in the matrix.
    def rows(self):
        return self._rows

    ## @brief Get the number of columns in the matrix.
    #  @return integer for the number of columns in the matrix.
    def cols(self):
        return self._cols

    ## @brief Get the value stored in the given row and column of the matrix.
    #  @param i integer of the row index (must be greater than or equal to 0 and less than number of rows).
    #  @param j integer of the column index (must be greater than or equal to 0 and less than number of columns).
    #  @return float of value stored in the i-th row and j-th column of matrix.
    def get_val(self, i, j):
        return round(self._matrix[i][j], 2)

    ## @brief Set the value stored in the given row and column of the matrix.
    #  @param i integer of the row index (must be greater than or equal to 0 and less than number of rows).
    #  @param j integer of the column index (must be greater than or equal to 0 and less than number of columns).
    #  @param val float of value stored to be stored in the i-th row and j-th column of matrix.
    def set_val(self, i, j, val):
        self._matrix[i][j] = round(float(val),2)

    ## @brief Get the maximum value stored in the matrix.
    #  @return float of maximum value stored in matrix.
    def max_val(self):
        current_max = float('-inf')
        for row in range(self.rows()):
            current_max = max(current_max, max(self._matrix[row]))
        return current_max

    ## @brief Get the minimum value stored in the matrix.
    #  @return float of minimum value stored in matrix.
    def min_val(self):
        current_min = float('inf')
        for row in range(self.rows()):
            current_min = min(current_min, min(self._matrix[row]))
        return current_min

    ## @brief Apply a function to every element stored in the matrix. (Note: changes original matrix as well)
    #  @param f A function that takes in the float value of an element and returns a float.
    #  @return A copy of the manipulated Matrix object.
    def map(self, f): 
        for i in range(self.rows()):
            for j in range(self.cols()):
                self._matrix[i][j] = float(f(self._matrix[i][j]))
        return self.Copy()

    ## @brief Add a value to every element stored in the matrix or add another Matrix object element-wise. (Note: changes original matrix as well)
    #  @param addend float or Matrix object of same dimensions to be added element-wise
    #  @return A copy of the manipulated Matrix object.
    def add(self, addend):
        if (isinstance(addend, Matrix)):
            if (self.is_same_size(addend)):
                for i in range(self.rows()):
                    for j in range(self.cols()):
                        self._matrix[i][j] = round(self._matrix[i][j] + addend._matrix[i][j],2)
        else:
            f = lambda x : x + addend
            self.map(f)
        return self.Copy()

    ## @brief Multiply a value to every element stored in the matrix or multiply another Matrix object element-wise. (Note: changes original matrix as well)
    #  @param multiplier float or Matrix object of same dimensions to be multiplied element-wise
    #  @return A copy of the manipulated Matrix object.
    def mul(self, multiplier):
        if (isinstance(multiplier, Matrix)):
            if (self.is_same_size(multiplier)):
                for i in range(self.rows()):
                    for j in range(self.cols()):
                        self._matrix[i][j] = round(self._matrix[i][j] * multiplier._matrix[i][j],2)
        else:
            f = lambda x : x * multiplier
            self.map(f)
        return self.Copy()

    ## @brief Perform matrix multiplication with another Matrix object.
    #  @param multiplier Matrix object with same number of rows.
    #  @return A Matrix object that is the product of matrix multiplication.
    def mat_mul(self, multiplier):
        if (isinstance(multiplier, Matrix)):
            if (self.cols() == multiplier.rows()):
                product = Matrix(self.rows(), multiplier.cols())
                for i in range(product.rows()):
                    for j in range(product.cols()):
                        sum = 0
                        for k in range(self.cols()):
                            sum += self._matrix[i][k] * multiplier._matrix[k][j]
                        product.set_val(i, j, sum)
                return product
            else:
                raise ValueError("Multiplier has incorrect dimensions for matrix multiplication.")
        else:
            raise TypeError("Mulitplier must be a Matrix object instance.")

    ## @brief Check if matrix is square.
    #  @return True if matrix is square.
    def is_square(self):
        return self.rows() == self.cols()

    ## @brief Check if matrix is invertible.
    #  @return True if matrix is invertible.
    def is_invertable(self):
        return self.is_square() and self.det() != 0

    ## @brief Check if matrix is symmetric.
    #  @return True if matrix is symmetric.
    def is_symmetric(self):
        return self == self.Transpose()

    ## @brief Check if matrix is skew symmetric.
    #  @return True if matrix is skew symmetric.
    def is_skew_symmetric(self):
        return self.Transpose() == self.Copy().mul(-1)

    ## @brief Check if matrix is upper triangular.
    #  @return True if matrix is upper triangular.
    def is_upper_triangular(self):
        for i in range(self.rows()):
            for j in range(self.cols()):
                if (j < i and self.get_val(i,j) != 0):
                    return False
        return True

    ## @brief Check if matrix is lower triangular.
    #  @return True if matrix is lower triangular.
    def is_lower_triangular(self):
        for i in range(self.rows()):
            for j in range(self.cols()):
                if ( j > i and self.get_val(i,j) != 0):
                    return False
        return True

    ## @brief Check if matrix is diagonal.
    #  @return True if matrix is diagonal.
    def is_diagonal(self):
        return self.is_upper_triangular() and self.is_lower_triangular()

    ## @brief Check if matrix has the same number of rows and columns as another Matrix object.
    #  @param other Matrix object to compare sizes with.
    #  @return True if both matricies have the same size.
    def is_same_size(self, other):
        return self.rows() == other.rows() and self.cols() == other.cols()

    ## @brief Calculate the minor from deleting the given row and column of the matrix.
    #  @param i integer of the row index (must be greater than or equal to 0 and less than number of rows).
    #  @param j integer of the column index (must be greater than or equal to 0 and less than number of columns).
    #  @return float value of the minor.
    def minor(self, i, j):
        copy = self.Copy()
        matrix = copy._matrix
        del matrix[i]
        for row in matrix:
            del row[j]
        copy._rows = copy.rows() - 1
        copy._cols = copy.cols() - 1
        return copy.det()

    ## @brief Calculate the cofactor from deleting the given row and column of the matrix using the minor.
    #  @param i integer of the row index (must be greater than or equal to 0 and less than number of rows).
    #  @param j integer of the column index (must be greater than or equal to 0 and less than number of columns).
    #  @return float value of the cofactor.
    def cofactor(self, i, j):
        minor = self.minor(i, j)
        return minor * ((-1) ** (i + j + 2))

    ## @brief Calculate the determinant of the matrix if it is square using cofactor expansion.
    #  @return float value of the determinant.
    def det(self):
        if (self.is_square()):
            if (self.rows() == 2):
                return self.get_val(0,0) * self.get_val(1,1) - self.get_val(0,1) * self.get_val(1,0)
            else:
                determinant = 0
                for k in range(self.cols()):
                    cofactor = self.cofactor(0, k)
                    determinant += cofactor * self.get_val(0, k) 
            return determinant
        else:
            raise ValueError("Cannot get determinant of non-square matrix.")

    ## @brief Calculate the trace of the matrix if it is square.
    #  @return float value of the trace.
    def tr(self):
        if (self.is_square()):
            sum = 0
            for i in range(self.rows()):
                for j in range(self.cols()):
                    sum += self.get_val(i, j)
            return sum
        else:
            raise ValueError("Cannot get trace of non-square matrix.")

    ## @brief Make a copy of the Matrix object (doesn't change original).
    #  @return Matrix object that is identical in dimensions and values.
    def Copy(self):
        copy = Matrix(self.rows(), self.cols())
        for i in range(self.rows()):
            for j in range(self.cols()):
                val = self.get_val(i, j)
                copy.set_val(i, j, val)
        return copy

    ## @brief Transpose the Matrix object (doesn't change original).
    #  @return Matrix object that is a transposition of the original matrix.
    def Transpose(self):
        trans = Matrix(self.cols(), self.rows())
        for i in range(self.rows()):
            for j in range(self.cols()):
                val = self.get_val(i, j)
                trans.set_val(j, i, val)
        return trans

    ## @brief Calculate the matrix adjoint (AKA adjugate) using the cofactors if matrix is square (doesn't change original).
    #  @return Matrix object that is the adjoint of the original matrix.
    def Adjoint(self):
        if (self.is_square()):
            cofactors = Matrix(self.rows(), self.cols())
            if (self.rows() == 2):
                cofactors.set_val(0,0,self.get_val(1,1))
                cofactors.set_val(1,1,self.get_val(0,0))
                cofactors.set_val(0,1,-1 * self.get_val(0,1))
                cofactors.set_val(1,0,-1 * self.get_val(1,0))
                return cofactors
            else:
                for i in range(self.rows()):
                    for j in range(self.cols()):
                        cofactor = self.cofactor(i, j)
                        cofactors.set_val(i, j, cofactor)
                return cofactors.Transpose()
        else:
            raise ValueError("Cannot get adjoint of non-square matrix.")
    
    ## @brief Calculate the matrix inverse if matrix is invertible (doesn't change original).
    #  @return Matrix object that is the inverse of the original matrix.
    def Inverse(self):
        if (self.is_invertable()):
            determinant = self.det()
            adjoint = self.Adjoint()
            adjoint.mul(1 / determinant)
            return adjoint
        else:
            raise ValueError("Matrix is not invertible.")

    ## @brief Static method to generate an identity matrix of the given dimensions (ex. Matrix.Identity(5)).
    #  @param rows integer for number of rows (or cols) of the square identity matrix.
    #  @return Matrix object that is an identity matrix.
    @staticmethod
    def Identity(rows):
        identity = Matrix(rows,rows)
        for i in range(rows):
            identity.set_val(i,i,1)
        return identity

    ## @brief Static method to generate an matrix with random values (ex. Matrix.Random(8,9,-10,10)).
    #  @param rows integer for number of rows.
    #  @param cols integer for number of cols.
    #  @param min int for minimum value in random range (inclusive).
    #  @param max float for maximum value in random range (exclusive).
    #  @return Matrix object with random values.
    @staticmethod
    def Random(rows, cols, min, max):
        rand = Matrix(rows,cols)
        for i in range(rows):
            for j in range(cols):
                val =  random.randrange(min,max)
                rand.set_val(i,j,val)
        return rand