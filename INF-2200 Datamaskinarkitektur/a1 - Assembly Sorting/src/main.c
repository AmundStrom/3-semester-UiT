#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "time.h"
#include <sys/time.h>
#include <stddef.h>


unsigned long long gettime(void)
{
    int retval;
    struct timeval tp;
    unsigned long long ctime;

    retval = gettimeofday(&tp, NULL);
    ctime = tp.tv_sec;
    ctime *= 1000000;
    ctime += tp.tv_usec;

    return ctime;
}

// Declaring that assembly function is provided elsewhere
extern void asm_function(int a[], int len);

extern void asmqs_function(int a[], int low, int high);

// This should be the C equivalent to the assembly implementation
// cocktail sort
// source: https://github.com/ismdeep/sort-algos-c
void c_function(int a[], int len) {
    int i, left = 0, right = len - 1;
    int temp;
    while (left < right) {
        for (i = left; i < right; i++) 
            if (a[i] > a[i + 1]) {
                temp = a[i];
                a[i] = a[i + 1];
                a[i + 1] = temp;
            }
        right--;
        for (i = right; i > left; i--)
            if (a[i - 1] > a[i]) {
                temp = a[i];
                a[i] = a[i - 1];
                a[i - 1] = temp;
            }
        left++;
    }
}

// Swaps the places of two elements in an array
void swap(int* a, int* b) {

    int temp = *a;
    *a = *b;
    *b = temp;
    
}

int partition(int array[], int low, int high) {
    
    int pivot = array[high];
    int i = (low - 1);

    for (int j = low; j <= high; j++) {
        
        //if element is smaller than pivot
        if(array[j] < pivot) {
            i++;
            swap(&array[i], &array[j]);
        }

    }

    swap(&array[i+1], &array[high]);

    return(i+1);
}

void quicksort(int array[], int low, int high) {
    
    if (low < high) {
        int pi = partition(array, low, high);
    
        quicksort(array, low, pi-1);
        quicksort(array, pi+1, high);
    }

}

/* Return a double pointer containing two identical arrays
 * Takes length of arrays and max number value as arguemnts */
int **create_array(int len, int max)
{
    int *a = malloc(len * sizeof(int));
    int *b = malloc(len * sizeof(int));
    int r;

    srand(2132378);

    for(int i = 0; i < len; i++)
    {
        r = rand() % max;
        a[i] = r;
        b[i] = r;
    }

    int **c = malloc(2 * sizeof(int*));
    c[0] = a;
    c[1] = b;

    return c;
}

int main(int argc, char **argv)
{

    // initialize time and declare the different variables needed for time meassurements
    srand(time(NULL));
    unsigned long long start, end;
    float total;

    printf("\n=========Quicksort========\n");

    int qslength = 20000;

    int **quickarray = create_array(qslength, qslength);

    int low = 0;
    
    printf("Array length: %d\n", qslength);

    printf("Sorting in C\n");
    start = gettime();
    quicksort(quickarray[0], low, qslength-1);
    end = gettime();
    total = (float) (end - start)/1000000;
    printf("C time: %f\n", total);

    printf("Sorting in assembly\n");
    start = gettime();
    asmqs_function(quickarray[1], low, qslength-1);
    end = gettime();
    total = (float) (end - start)/1000000;
    printf("Asm time: %f\n", total);

    free(quickarray);

    printf("===========================\n");



    printf("\n=======Cocktail-Sort=======\n");

    int length = 20000;

    int **cocktailarray = create_array(length, length);

    printf("Array length: %d\n", length);

    /* Take time of Assembly fucntion */
    start = gettime();
    printf("Sorting in assembly\n");
	    asm_function(cocktailarray[1], length);
    end = gettime();
    total = (float) (end - start)/1000000;
    printf("Asm time: %f\n", total);

    /* Take time of C function */
    start = gettime();
    printf("Sorting in C\n");
        c_function(cocktailarray[0], length);
    end = gettime();
    total = (float) (end - start)/1000000;
    printf("C time: %f\n", total);
    free(cocktailarray);
    printf("===========================\n");
}
