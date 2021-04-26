#include <cmath>
#include <iostream>

namespace vectors {
    class Vector3 {
        public:
            float x, y, z;

            Vector3(float i=0, float j=0, float k=0) : x{i}, y{j}, z{k} {}

            float magnitude() const {
                return sqrt(x*x + y*y + z*z);
            }

            float magnitudeSqr() const {
                return x*x + y*y + z*z;
            }

            float normalize() {
                (*this) *= 1 / this->magnitude();
            }

            Vector3 normalized() const {
                Vector3 v = Vector3(x, y, z);
                v.normalize();
                return v;
            }

            void scale(float scaler) {
                (*this) *= scaler;
            }

#pragma region Operators
            // Operators
            // Adition
            // Vector-Vector addition
            Vector3 operator + (Vector3& v) const {
                return Vector3(x+v.x, y+v.y, z+v.z);
            }

            void operator += (Vector3& v) {
                x += v.x;
                y += v.y;
                z += v.z;
            }

            // Vector-Scaler addition
            Vector3 operator + (float scaler) const {
                return Vector3(x+scaler, y+scaler, z+scaler);
            }

            void operator += (float scaler) {
                x += scaler;
                y += scaler;
                z += scaler;
            }
            
            // Subtraction
            // Vector-Vector subtraction
            Vector3 operator - (Vector3& v) const {
                return Vector3(x-v.x, y-v.y, z-v.z);
            }

            void operator -= (Vector3& v) {
                x -= v.x;
                y -= v.y;
                z -= v.z;
            }

            // Vector-Scaler subtraction
            Vector3 operator - (float scaler) const {
                return Vector3(x-scaler, y-scaler, z-scaler);
            }

            void operator -= (float scaler) {
                x -= scaler;
                y -= scaler;
                z -= scaler;
            }

            // Multiplicaition
            // Vector-Vector multiplication
            float operator * (Vector3& v) const {
                Vector3 _v = Vector3(this->x, this->y, this->y);
                return Vector3::dot(_v, v);
            }

            // Vector-Scaler multiplication
            Vector3 operator * (float scaler) const {
                return Vector3(x*scaler, y*scaler, z*scaler);
            }

            void operator *= (float scaler) {
                x *= scaler;
                y *= scaler;
                z *= scaler;
            }
#pragma endregion

            friend std::ostream& operator << (std::ostream&, Vector3&);

            // Static Vector utility functions
            static float distance(Vector3 v1, Vector3 v2) {
                float dist = 0;

                float xDist = v2.x - v1.x;
                float yDist = v2.y - v1.y;
                float zDist = v2.z - v1.z;

                return sqrt(xDist*xDist + yDist*yDist + zDist*zDist);
            }
            
            static float distanceSqr(Vector3& v1, Vector3& v2) {
                float dist = 0;

                float xDist = v2.x - v1.x;
                float yDist = v2.y - v1.y;
                float zDist = v2.z - v1.z;

                return xDist*xDist + yDist*yDist + zDist*zDist;
            }

            static float dot(Vector3& v1, Vector3& v2) {
                return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z;
            }

            static Vector3 cross(Vector3& v1, Vector3& v2) {
                float x = v1.y*v2.z - v1.z*v2.y;
                float y = v1.x*v2.z - v1.z*v2.x;
                float z = v1.x*v2.y - v1.y*v2.x;
                
                return Vector3(x, y, z);
            }
    };

    std::ostream& operator << (std::ostream& dout, Vector3& v) {
        dout << "<Vector 3>: " << v.x << "i ";

        if (v.y < 0)
            dout << "- ";
        else
            dout << "+ ";

        dout << abs(v.y) << "j ";

        if (v.z < 0)
            dout << "- ";
        else
            dout << "+ ";

        dout << abs(v.z) << "k";

        return dout;
    }
}
