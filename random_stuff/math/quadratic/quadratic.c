#include <stdio.h>
#include <math.h>//for sqrt() and NaN
#include <stdlib.h>//for exit()

typedef struct {
    float result1;
    float result2;
} return_type;

return_type get_roots(float a, float b, float c);
float get_float();
void display_roots(return_type roots);

int main()
{
    printf("ax^2 + bx + c = 0\n");
    printf("a = ");    
    float a = get_float();
    printf("b = ");
    float b = get_float();
    printf("c = ");
    float c = get_float();

    return_type roots = get_roots(a, b, c);
    display_roots(roots);
    return 0;
}

return_type get_roots(float a, float b, float c){
    return_type roots;

    if (a == 0){
        printf("a cannot be 0");
        exit(1);
    }

    float D = (b * b) - (4 * a * c);

    if (D < 0){
        printf("No solutions in the set of Reals\n");
        roots.result1 = NAN;
        roots.result2 = NAN;
    }
    else if (D == 0){
        float root1 = (-b + sqrt(D)) / (2*a);
        roots.result1 = root1;
        roots.result2 = NAN; //equal roots are 1 root for this code
    }
    else if (D > 0){
        float root1 = (-b + sqrt(D)) / (2*a);
        float root2 = (-b - sqrt(D)) / (2*a);
        roots.result1 = root1;
        roots.result2 = root2;
    }
    else {
        printf("The universe colapsed and math isnt mething");
    }

    return roots;
}

//idealy here i need input validation, but skill issue
float get_float(){
    float f;
    int result = 0;
    while (result != 1){
        result = scanf("%f", &f);
    }
    return f;
}

void display_roots(return_type roots){
    printf("Roots:\n1)%.6f\n2)%.6f\n", roots.result1, roots.result2);
}