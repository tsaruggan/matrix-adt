# matrix_adt_test.py

import pytest
import math
from matrix_adt import Matrix

# Test of mul method

def test_mul1():
    a = Matrix(2,2)
    a.set_val(0,0,1)
    a.set_val(0,1,2)
    a.set_val(1,0,3)
    a.set_val(1,1,4)
    a.mul(-1/2)

    a_sol = Matrix(2,2)
    a_sol.set_val(0,0,-1/2)
    a_sol.set_val(0,1,-2/2)
    a_sol.set_val(1,0,-3/2)
    a_sol.set_val(1,1,-4/2)
    assert a == a_sol

def test_mul2():
    rand = Matrix.Random(24,8,-100,100)
    rand.mul(0)
    zero = Matrix(24,8)
    assert rand == zero

## Test of mat_mul method

def test_mat_mul1():
    r = Matrix.Random(2,3, 0, 9)
    s = Matrix.Random(3,4, 0, 9)
    t = r.mat_mul(s)
    assert t.rows() == 2 and t.cols() == 4

def test_mat_mul2():
    u = Matrix(2,2)
    u.set_val(0,0,1)
    u.set_val(0,1,2)
    u.set_val(1,0,3)
    u.set_val(1,1,4)
    v = u.Copy()
    w = u.mat_mul(v)
    assert w.get_val(0,0) == 7

def test_mat_mul3():
    x = Matrix.Random(100,100,0,100)
    x.mul(math.sqrt(2))
    i = Matrix.Identity(100)
    assert x.mat_mul(i) == x

def test_mat_mul_raises_exception_on_non_Matrix_argument():
    x = Matrix.Random(100,100,0,100)
    with pytest.raises(TypeError):
        x.mat_mul(6) 

def test_mat_mul_raises_exception_on_Matrix_arguement_with_incorrect_dimensions():
    x = Matrix.Random(2,3,0,100)
    y = Matrix.Random(4,3,0,100)
    with pytest.raises(ValueError):
        x.mat_mul(y) 

## Test of det method

def test_det1():
    m = Matrix(2,2)
    m.set_val(0,0,1)
    m.set_val(0,1,2)
    m.set_val(1,0,3)
    m.set_val(1,1,4)
    assert m.det() == -2

def test_det2(): # fails due to summing irrational numbers (rounding errors)
    m = Matrix(3,3)
    m.set_val(0,0,1)
    m.set_val(0,1,2)
    m.set_val(0,2,3)
    m.set_val(1,0,4)
    m.set_val(1,1,5)
    m.set_val(1,2,6)
    m.set_val(2,0,7)
    m.set_val(2,1,8)
    m.set_val(2,2,9)
    m.mul(math.sqrt(2)) 
    assert m.det() == 0

def test_det3():
    count = 0
    for size in range(2,7):
        a = Matrix.Random(size,size,0, 10)
        b = Matrix.Random(size,size,0, 10)
        ab = a.mat_mul(b)
        det_a = a.det()
        det_b = b.det()
        det_ab = ab.det()
        count += det_a * det_b == det_ab
    assert count == 5

def test_det_exception_on_non_square_Matrix_arguments():
    x = Matrix.Random(50,49,0,100)
    with pytest.raises(ValueError):
        x.det()

## Test of Inverse method

def test_Inverse1():
    k = Matrix(2,2)
    k.set_val(0,0,1)
    k.set_val(0,1,2)
    k.set_val(1,0,3)
    k.set_val(1,1,4)
    j = Matrix(2,2)
    j.set_val(0,0,-2)
    j.set_val(0,1,1)
    j.set_val(1,0,3/2)
    j.set_val(1,1,-1/2)
    assert k.Inverse() == j

def test_Inverse2():
    count = 0
    for size in range(2,7):
        a = Matrix.Random(size,size,0, 10)
        if (a.is_invertable()):
            a_inv = a.Inverse()
            prod = a.mat_mul(a_inv)
            count += prod == Matrix.Identity(size)
        else:
            count+=1
    assert count == 5

def test_Inverse3():
    count = 0
    for size in range(2,7):
        a = Matrix.Random(size,size,0, 10)
        b = Matrix.Random(size,size,0, 10)
        if (a.is_invertable() and b.is_invertable() ):
            a_inv = a.Inverse()
            b_inv = b.Inverse()
            ab = a.mat_mul(b)
            ab_inv = ab.Inverse()
            count += b_inv.mat_mul(a_inv) == ab_inv
        else:
            count+=1
    assert count == 5

def test_Inverse_exception_non_invertible_Matrix_arguement():
    x = Matrix.Random(50,49,0,100)
    with pytest.raises(ValueError):
        x.Inverse()