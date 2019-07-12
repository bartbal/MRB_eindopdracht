import math

class VectorAlgebra():
    
    """vectorNumMultiply, multiply a one-dimensional vector by a number

    Parameters
    ----------
    vector : tuple(a, b)
        the vector to multiply
    num : float
        the number to multiply by

    Return
    ----------
    result : tuple(a, b)
        the resulting vector
    """
    def vectorNumMultiply(vector, num): 
        result = list(vector)

        for index in range(len(result)):
            result[index] *= num

        return result

    """vectorAdd, add two one-dimensional vectors together

    Parameters
    ----------
    va : tuple(a, b)
        vector a
    vb : tuple(a, b)
        vector b

    Return
    ----------
    : tuple(a, b)
        the resulting vector
    """
    def vectorAdd(va, vb): 
        return [va[0]+vb[0], va[1]+vb[1]]

    """dotProduct, calculate the dot product of two one-dimensional vectors. <a, b>

    Parameters
    ----------
    a : tuple(a, b)
        vector a
    b : tuple(a, b)
        vector b

    Return
    ----------
    result : tuple(a, b)
        the resulting vector
    """
    def dotProduct(a, b):
        assert len(a) == len(b), "a and b are not the same length"

        result = 0

        for index in range(len(a)):
            result += (a[index] * b[index])

        return result
    
    """unitVector, calculate the unit vector of a one-dimensional vector.

    Parameters
    ----------
    a : tuple(a, b)
        vector a

    Return
    ----------
    : tuple(a, b)
        the resulting vector
    """
    def unitVector(a):
        length = VectorAlgebra.vectorLength(a)
        return [a[0]/length, a[1]/length]

    """vectorLength, calculate the linear length of a one-dimensional vector. |a|

    Parameters
    ----------
    a : tuple(a, b)
        vector a

    Return
    ----------
    : tuple(a, b)
        the resulting vector
    """
    def vectorLength(a):
        return  math.sqrt( a[0]**2 + a[1]**2 )

    """projection, calculate the projection of a on b. Both have to be a one-dimensional vector.

    Parameters
    ----------
    a : tuple(a, b)
        vector a
    b : tuple(a, b)
        vector b

    Return
    ----------
    : tuple(a, b)
        the resulting vector
    """
    def projection(a, b):
        return VectorAlgebra.vectorNumMultiply(b, (VectorAlgebra.dotProduct(a, b) / VectorAlgebra.vectorLength(b)**2))

    """projectionLength, calculates the length of the projection of a on b

    Parameters
    ----------
    a : tuple(a, b)
        vector a
    b : tuple(a, b)
        vector b

    Return
    ----------
    : tuple(a, b)
        the resulting vector
    """
    def projectionLength(a, b):
        return (VectorAlgebra.dotProduct(a, b) / VectorAlgebra.vectorLength(b))