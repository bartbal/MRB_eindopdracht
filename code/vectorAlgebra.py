import math

class VectorAlgebra():
    
    # multiply a one-dimensional vector by a number
    def vectorNumMultiply(vector, num): 
        result = list(vector)

        for index in range(len(result)):
            result[index] *= num

        return result

    # multiply a one-dimensional vector by a number
    def vectorAdd(va, vb): 
        return [va[0]+vb[0], va[1]+vb[1]]

    # calculate the dot product of two one-dimensional vectors. <a, b>
    def dotProduct(a, b):
        assert len(a) == len(b), "a and b are not the same length"

        result = 0

        for index in range(len(a)):
            result += (a[index] * b[index])

        return result
    
    # calculate the unit vector of a one-dimensional vector.
    def unitVector(a):
        length = VectorAlgebra.vectorLength(a)
        return [a[0]/length, a[1]/length]

    # calculate the linear length of a one-dimensional vector. |a|
    def vectorLength(a):
        return  math.sqrt( a[0]**2 + a[1]**2 )

    # calculate the projection of a on b. Both have to be a one-dimensional vector.
    def projection(a, b):
        return VectorAlgebra.vectorNumMultiply(b, (VectorAlgebra.dotProduct(a, b) / VectorAlgebra.vectorLength(b)**2))

    # calculates the length of the projection of a on b
    def projectionLength(a, b):
        return (VectorAlgebra.dotProduct(a, b) / VectorAlgebra.vectorLength(b))